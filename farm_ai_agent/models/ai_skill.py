# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import base64
import json
import logging

_logger = logging.getLogger(__name__)

class AgriAiSkill(models.Model):
    """
    User-authored or uploaded AI Agent Skills.
    Contains semantic descriptions used by LLMs, Markdown guidelines, and executable JSON plans.
    """
    _name = 'agri.ai.agent.skill'
    _description = 'AI Agent Skill'
    _inherit = ['mail.thread']

    name = fields.Char('Skill Name', required=True, tracking=True)
    description = fields.Text(
        'Semantic Description', 
        required=True, 
        help="Semantic definition used by LLMs to dynamically select this skill.",
        tracking=True
    )
    skill_markdown = fields.Text(
        'Markdown Specification', 
        required=True, 
        default='# AI Agent Skill\n\n## Description\nExplain what this skill does.\n\n## Executable Blueprint\n```json\n{\n    "model": "mrp.workcenter",\n    "method": "write",\n    "args": {}\n}\n```',
        help="Detailed skill specification and guidelines written in Markdown."
    )
    skill_payload = fields.Text(
        'Skill Payload (JSON)', 
        compute='_compute_skill_payload',
        store=True,
        readonly=False,
        help="The JSON directive sequence for Re-Act execution, parsed from the Markdown JSON block."
    )
    
    # Upload support
    upload_file = fields.Binary('Upload Skill / Attachment', help="Upload a .md file to overwrite the specification, or any other file format to save as a companion attachment.")
    upload_filename = fields.Char('File Name')
    
    attachment_ids = fields.Many2many('ir.attachment', 'agri_ai_agent_skill_ir_attachment_rel', 'skill_id', 'attachment_id', 
        string='Skill Attachments',
        help="Companion configuration files, auxiliary scripts, or schemas associated with this skill."
    )
    
    is_active = fields.Boolean('Is Active', default=True, tracking=True)

    @api.depends('skill_markdown')
    def _compute_skill_payload(self):
        """ Dynamically parse the executable JSON code block inside the Markdown specification """
        import re
        import json
        for record in self:
            if not record.skill_markdown:
                record.skill_payload = '{}'
                continue
                
            # Regular expression to extract JSON code blocks
            pattern = re.compile(r'```(?:json)?\s*(\{.*?\})\s*```', re.DOTALL)
            match = pattern.search(record.skill_markdown)
            
            if match:
                try:
                    json_str = match.group(1).strip()
                    # Validate JSON structure
                    parsed = json.loads(json_str)
                    record.skill_payload = json.dumps(parsed, indent=4)
                except Exception as e:
                    _logger.warning("Failed to parse embedded JSON from Markdown: %s", str(e))
                    record.skill_payload = '{}'
            else:
                record.skill_payload = '{}'

    @api.onchange('upload_file')
    def _onchange_upload_file(self):
        """ Automatically decode, validate, and fill skill_markdown or link as attachments upon file upload (supports packaged zip/skill format) """
        if self.upload_file and self.upload_filename:
            filename = self.upload_filename.lower()
            try:
                decoded_data = base64.b64decode(self.upload_file)
                
                # Support packaged .zip or .skill formats
                if filename.endswith('.zip') or filename.endswith('.skill'):
                    import zipfile
                    import io
                    
                    zip_stream = io.BytesIO(decoded_data)
                    attachments_to_create = []
                    markdown_content = False
                    
                    with zipfile.ZipFile(zip_stream, 'r') as zfile:
                        for zinfo in zfile.infolist():
                            # Skip directories
                            if zinfo.is_dir():
                                continue
                                
                            file_data = zfile.read(zinfo.filename)
                            base_name = zinfo.filename.split('/')[-1]
                            
                            # Extract SKILL.md as the main specification
                            if base_name.upper() == 'SKILL.MD':
                                markdown_content = file_data.decode('utf-8')
                            else:
                                # Process other files as auxiliary companion attachments
                                attachments_to_create.append({
                                    'name': zinfo.filename,
                                    'datas': base64.b64encode(file_data),
                                    'res_model': self._name,
                                    'res_id': self.id or 0,
                                })
                                
                    if markdown_content:
                        # Robust YAML frontmatter parser
                        import re
                        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', markdown_content, re.DOTALL)
                        if frontmatter_match:
                            yaml_block = frontmatter_match.group(1)
                            body_content = frontmatter_match.group(2)
                            
                            name_match = re.search(r'^name:\s*(.*?)\s*$', yaml_block, re.MULTILINE)
                            desc_match = re.search(r'^description:\s*(.*?)\s*$', yaml_block, re.MULTILINE)
                            
                            if name_match:
                                self.name = name_match.group(1).strip().strip('"\'')
                            if desc_match:
                                self.description = desc_match.group(1).strip().strip('"\'')
                                
                            self.skill_markdown = body_content
                        else:
                            self.skill_markdown = markdown_content
                            
                    # Register and link attachments in Odoo
                    created_attachments = []
                    for att_vals in attachments_to_create:
                        attachment = self.env['ir.attachment'].create(att_vals)
                        created_attachments.append((4, attachment.id))
                    if created_attachments:
                        self.attachment_ids = created_attachments
                        
                    self.upload_file = False
                    self.upload_filename = False
                    return

                # Support single .md or .txt file upload
                elif filename.endswith('.md') or filename.endswith('.txt'):
                    text_content = decoded_data.decode('utf-8')
                    
                    # Robust YAML frontmatter parser
                    import re
                    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', text_content, re.DOTALL)
                    if frontmatter_match:
                        yaml_block = frontmatter_match.group(1)
                        body_content = frontmatter_match.group(2)
                        
                        name_match = re.search(r'^name:\s*(.*?)\s*$', yaml_block, re.MULTILINE)
                        desc_match = re.search(r'^description:\s*(.*?)\s*$', yaml_block, re.MULTILINE)
                        
                        if name_match:
                            self.name = name_match.group(1).strip().strip('"\'')
                        if desc_match:
                            self.description = desc_match.group(1).strip().strip('"\'')
                            
                        self.skill_markdown = body_content
                    else:
                        self.skill_markdown = text_content
                        
                    self.upload_file = False
                    self.upload_filename = False
                else:
                    # Parse as single auxiliary companion attachment
                    attachment = self.env['ir.attachment'].create({
                        'name': self.upload_filename,
                        'datas': self.upload_file,
                        'res_model': self._name,
                        'res_id': self.id or 0,
                    })
                    # Link to attachment list
                    self.attachment_ids = [(4, attachment.id)]
                    self.upload_file = False
                    self.upload_filename = False
            except Exception as e:
                return {
                    'warning': {
                        'title': _("Upload Error"),
                        'message': _("Failed to process the uploaded file:\n%s") % str(e)
                    }
                }

    @api.onchange('attachment_ids')
    def _onchange_attachment_ids(self):
        """ Automatically scan uploaded companion files to find and parse SKILL.md specification """
        if not self.attachment_ids:
            return
            
        # Find an attachment named SKILL.md (case-insensitive)
        skill_md_att = self.attachment_ids.filtered(lambda a: a.name and a.name.upper() == 'SKILL.MD')
        if not skill_md_att:
            # Fallback to any markdown file if SKILL.md is not found
            skill_md_att = self.attachment_ids.filtered(lambda a: a.name and a.name.lower().endswith('.md'))
            
        if skill_md_att:
            skill_md_att = skill_md_att[0]
            if skill_md_att.datas:
                try:
                    decoded_data = base64.b64decode(skill_md_att.datas).decode('utf-8')
                    
                    # Robust YAML frontmatter parser
                    import re
                    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', decoded_data, re.DOTALL)
                    if frontmatter_match:
                        yaml_block = frontmatter_match.group(1)
                        body_content = frontmatter_match.group(2)
                        
                        name_match = re.search(r'^name:\s*(.*?)\s*$', yaml_block, re.MULTILINE)
                        desc_match = re.search(r'^description:\s*(.*?)\s*$', yaml_block, re.MULTILINE)
                        
                        if name_match:
                            self.name = name_match.group(1).strip().strip('"\'')
                        if desc_match:
                            self.description = desc_match.group(1).strip().strip('"\'')
                            
                        self.skill_markdown = body_content
                    else:
                        self.skill_markdown = decoded_data
                except Exception as e:
                    _logger.warning("Failed to parse SKILL.md attachment: %s", str(e))

    def action_export_agent_skill(self):
        """ Export this skill as a standard Agent SKILL.md specification file """
        self.ensure_one()
        yaml_frontmatter = (
            "---\n"
            f"name: {self.name}\n"
            f"description: {self.description}\n"
            "---\n\n"
        )
        full_markdown = yaml_frontmatter + (self.skill_markdown or '')
        
        # Link output as an Odoo attachment for user download
        attachment = self.env['ir.attachment'].create({
            'name': "SKILL.md",
            'datas': base64.b64encode(full_markdown.encode('utf-8')),
            'res_model': self._name,
            'res_id': self.id,
        })
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
