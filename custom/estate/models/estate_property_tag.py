from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = "name"

    name = fields.Char('Property Tags', required=True)
    color = fields.Integer('Color')

    _sql_constraints = [
        ('unique_property_tag', 'UNIQUE(name)', 'Property Tag already exists.')
    ]