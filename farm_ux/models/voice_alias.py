from odoo import models, fields, api, _

class VoiceRecognitionAlias(models.Model):
    _name = 'farm.voice.recognition.alias'
    _description = 'Voice Recognition Alias for Agricultural Terms'
    _order = 'alias'

    alias = fields.Char("Spoken Alias / Phonetic", required=True, help="Common spoken variation or phonetic (e.g., 'Niao Su')")
    target_term = fields.Char("Standard Term", required=True, help="The correct term in the system (e.g., '尿素')")
    
    @api.model
    def normalize_voice_text(self, text):
        """ US-26-02: Normalize voice-to-text output using registered aliases. """
        if not text or not isinstance(text, str):
            return text
            
        aliases = self.search([])
        # Sort by length descending to match longest phrases first
        for a in sorted(aliases, key=lambda x: len(x.alias), reverse=True):
            if a.alias in text:
                text = text.replace(a.alias, a.target_term)
        return text
