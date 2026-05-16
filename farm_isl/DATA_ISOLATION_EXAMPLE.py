# ISL Data Migration for Industry Isolation

# The ISL architecture should ensure proper data isolation between industries
# This script demonstrates how data should be properly assigned to industries

# Example: Migrate existing production records to proper industry types
def migrate_production_to_industries():
    """
    Example migration to assign proper industry types to existing production records
    """
    # Get all base production records
    base_productions = env['mrp.production'].search([])

    for base_prod in base_productions:
        # Determine industry type based on product, location, or other factors
        industry_type = determine_industry_type(base_prod)

        # Create ISL record with proper industry type
        if industry_type == 'field_crop':
            # Create processing-specific ISL record
            env['farm.processing.production'].create({
                'production_id': base_prod.id,
                'industry_type': 'field_crop',
                'energy_reading_start': 0,
                'energy_reading_end': 0,
            })
        elif industry_type == 'livestock':
            # Create livestock-specific ISL record
            env['farm.livestock.production'].create({
                'production_id': base_prod.id,
                'industry_type': 'livestock',
                'initial_total_weight': 0,
                'final_total_weight': 0,
            })

def determine_industry_type(base_record):
    """
    Determine industry type for a base record based on various factors
    """
    # Example logic - in practice this would be more sophisticated
    if 'livestock' in base_record.product_id.name.lower():
        return 'livestock'
    elif 'food' in base_record.product_id.name.lower() or 'process' in base_record.product_id.name.lower():
        return 'field_crop'
    else:
        return 'general'

# The ISL architecture ensures data isolation through:
# 1. Industry Type Field: Each record is tagged with its industry
# 2. Access Controls: Security rules restrict access by industry
# 3. UI Filtering: Views show only relevant fields based on industry
# 4. Business Logic: Methods execute only for matching industry types

# Industry-specific data isolation example:
# - Food Processing: HACCP plans, allergen controls, temperature logs
# - Livestock: Health records, breeding status, feed conversion ratios
# - Aquaculture: Water quality parameters, stocking density, harvest timing
# - General: Basic manufacturing parameters without industry-specific fields

# The system maintains proper separation while allowing shared infrastructure