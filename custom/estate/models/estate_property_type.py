from odoo import models, fields
from odoo import api

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type" 
    _order = "name , sequence"

    name = fields.Char('Property Type' , required=True)
    properties_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    sequence = fields.Integer('Sequence')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id' , string='Offers')
    offer_count = fields.Integer('Offer Count', compute="_compute_offers")

    @api.depends('offer_ids')
    def _compute_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    _sql_constraints = [
        ('unique_property_type', 'UNIQUE(name)', 'Property Type already exists.')
    ]