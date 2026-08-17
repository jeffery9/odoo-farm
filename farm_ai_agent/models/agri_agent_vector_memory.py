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
