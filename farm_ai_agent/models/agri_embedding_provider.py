# -*- coding: utf-8 -*-
import hashlib
import numpy as np
from odoo import models, fields, api, _

class AgriEmbeddingProvider(models.AbstractModel):
    _name = 'agri.embedding.provider'
    _description = 'Pluggable Embedding Provider Service'

    @api.model
    def get_embedding(self, text):
        """
        Get high-dimensional 384 float embedding vector.
        Follows bilingual validation errors when necessary.
        """
        try:
            # Read system parameter, default is 'sandbox' for isolated tests
            provider_mode = self.env['ir.config_parameter'].sudo().get_param('agri_iot.embedding_mode', 'sandbox')
        except Exception:
            provider_mode = 'sandbox'
        
        if provider_mode == 'sandbox':
            return self._generate_deterministic_sandbox_embedding(text)
        else:
            return self._call_production_embedding_api(text)

    def _generate_deterministic_sandbox_embedding(self, text):
        """
        Deterministic pseudo-random vector generator based on SHA-256 seed.
        Ensures 100% reliable unit tests in isolated disconnected sandbox environments.
        """
        if not text:
            return [0.0] * 384
            
        # Parse stable hash seed from text
        seed = int(hashlib.sha256(text.encode('utf-8')).hexdigest(), 16) % (2**32 - 1)
        rng = np.random.default_rng(seed)
        
        # Draw 384-dimensional Gaussian sample and normalize to unit hypersphere (L2 Normalized)
        vector = rng.standard_normal(384)
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
            
        return vector.tolist()

    def _call_production_embedding_api(self, text):
        """
        Production stub for connecting to local transformers or Vertex AI.
        """
        return self._generate_deterministic_sandbox_embedding(text)
