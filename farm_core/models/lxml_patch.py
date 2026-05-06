# -*- coding: utf-8 -*-
import lxml.etree as ET
import logging

_logger = logging.getLogger(__name__)

# Store the original fromstring method
original_fromstring = ET.fromstring

def safe_fromstring(text, parser=None, base_url=None):
    """
    Odoo 19 / LXML Patch:
    Prevents "ValueError: Unicode strings with encoding declaration are not supported"
    when parsing XML/HTML strings that contain an encoding declaration (common in Odoo App Store index.html).
    """
    if isinstance(text, str) and text.startswith('<?xml') and 'encoding=' in text:
        # Convert unicode string with declaration to bytes to satisfy lxml
        try:
            return original_fromstring(text.encode('utf-8'), parser=parser, base_url=base_url)
        except Exception as e:
            _logger.error("LXML Patch failed to parse encoded bytes: %s", e)
            
    return original_fromstring(text, parser=parser, base_url=base_url)

# Apply the patch globally within the Odoo process
ET.fromstring = safe_fromstring
_logger.info("Odoo Farm: Applied LXML Safety Patch for Unicode XML declarations.")
