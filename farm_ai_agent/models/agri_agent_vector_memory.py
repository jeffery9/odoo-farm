# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AgriAgentVectorMemory(models.Model):
    _name = 'agri.agent.vector.memory'
    _description = 'Agricultural Agent Spatio-Temporal Vector Memory'
    _order = 'timestamp desc'

    name = fields.Char("Memory Abstract (记忆摘要)", required=True, index=True)
    content = fields.Text("Raw Context (详细上下文内容)", required=True)
    timestamp = fields.Datetime("Captured Time", required=True, default=fields.Datetime.now, index=True)
    
    # Traceability fields (Late-binding reference parameters)
    source_model = fields.Char("Source Model (溯源模型)", index=True)
    source_id = fields.Integer("Source ID (溯源物理主键)", index=True)
    
    # Multi-company RLS Row level protection context
    company_id = fields.Many2one('res.company', string="Company", required=True, default=lambda self: self.env.company)

    def init(self):
        """ Ensure PostgreSQL pgvector extension exists, add the vector(384) column, and register HNSW index """
        # 1. Register native pgvector extension
        self.env.cr.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        
        # 2. Check and alter table to add vector(384) column
        self.env.cr.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'agri_agent_vector_memory' AND column_name = 'embedding';
        """)
        if not self.env.cr.fetchone():
            self.env.cr.execute("ALTER TABLE agri_agent_vector_memory ADD COLUMN embedding vector(384);")
            
        # 3. Inject native Hierarchical Navigable Small World (HNSW) index for Cosine similarity operations
        self.env.cr.execute("""
            CREATE INDEX IF NOT EXISTS agri_agent_vector_memory_embedding_hnsw_idx 
            ON agri_agent_vector_memory 
            USING hnsw (embedding vector_cosine_ops);
        """)

    @api.model
    def search_semantic_memory(self, query_text, limit=5):
        """
        Execute high-performance cosine similarity searches leveraging the pgvector operator <=>
        Strictly restricts results to visible companies (Self-contained RLS filter).
        """
        if not query_text:
            return []
            
        # Call provider to obtain query embedding vector
        query_vector = self.env['agri.embedding.provider'].get_embedding(query_text)
        
        visible_companies = self.env.companies.ids
        
        # Order by Cosine Distance ASC (Smaller distance = Higher similarity)
        self.env.cr.execute("""
            SELECT id, name, content, timestamp, source_model, source_id,
                   (embedding <=> %s::vector) AS cosine_distance
            FROM agri_agent_vector_memory
            WHERE company_id IN %s
            ORDER BY embedding <=> %s::vector ASC
            LIMIT %s;
        """, (query_vector, tuple(visible_companies), query_vector, limit))
        
        return self.env.cr.dictfetchall()

    @api.model
    def run_incremental_sync_pipeline(self):
        """
        Incremental self-healing memory compilation sync pipeline.
        Pulls latest mail.messages (Chatter cards) and extreme telemetry.series warnings.
        """
        # 1. Retrieve the timestamp threshold of last run
        try:
            last_sync_param = self.env['ir.config_parameter'].sudo().get_param('agri_agent.memory_last_sync_time', '1970-01-01 00:00:00')
        except Exception:
            last_sync_param = '1970-01-01 00:00:00'
        
        # 2. Extract Chatter cards
        messages = self.env['mail.message'].search([
            ('create_date', '>', last_sync_param),
            ('model', 'in', ['farm.water.valve', 'stock.matter.tracking', 'agri.clearing.ledger']),
            ('body', '!=', '')
        ])
        
        for msg in messages:
            plain_text = self.env['mail.thread']._html_to_plain_text(msg.body).strip()
            if not plain_text:
                continue
                
            exists = self.search([('source_model', '=', 'mail.message'), ('source_id', '=', msg.id)], limit=1)
            if exists:
                continue
                
            vector = self.env['agri.embedding.provider'].get_embedding(plain_text)
            
            # Write structured vector memory
            self.create({
                'name': f"Chatter: {plain_text[:40]}...",
                'content': plain_text,
                'timestamp': msg.create_date,
                'source_model': 'mail.message',
                'source_id': msg.id,
                'company_id': msg.company_id.id or self.env.company.id,
                'embedding': vector
            })

        # 3. Extract extreme pressure WAL telemetries (Pressure exceeded 110 PSI threshold)
        telemetries = self.env['agri.telemetry.series'].search([
            ('timestamp', '>', last_sync_param),
            ('sensor_type', '=', 'pressure_psi'),
            ('value', '>', 110.0)
        ])
        
        for telemetry in telemetries:
            exists = self.search([('source_model', '=', 'agri.telemetry.series'), ('source_id', '=', telemetry.id)], limit=1)
            if exists:
                continue
                
            alert_text = f"IIoT PRESSURE WARNING: valve pressure reached {telemetry.value} PSI (超压报警时空记录)"
            vector = self.env['agri.embedding.provider'].get_embedding(alert_text)
            
            self.create({
                'name': "Telemetry Pressure Warning (高频压强越限异常)",
                'content': alert_text,
                'timestamp': telemetry.timestamp,
                'source_model': 'agri.telemetry.series',
                'source_id': telemetry.id,
                'company_id': self.env.company.id,
                'embedding': vector
            })

        # 4. Save latest runtime timestamp
        try:
            self.env['ir.config_parameter'].sudo().set_param('agri_agent.memory_last_sync_time', fields.Datetime.now())
        except Exception:
            pass
        return True
