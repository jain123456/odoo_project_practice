from odoo import models, fields
from odoo import api, exceptions
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = "price desc"

    price = fields.Float('Price')
    status = fields.Selection([
        ('accepted' , 'Accepted'),
        ('refused' , 'Refused')
    ], string='Status')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date('Date Deadline' , compute='_compute_date_deadline' , inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends("create_date","validity")
    def _compute_date_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - date).days

    def action_accept(self):
        for record in self:
            for record in self.property_id.offer_ids:
                record.status = "refused"
            self.status = "accepted"
            self.property_id.buyer_id = self.partner_id
            self.property_id.selling_price = self.price
            self.property_id.state = "offer_accepted"
        return True
    
    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK(price > 0)', 'Offer Price must be greater than 0.'),
    ]

    @api.model
    def create(self,vals):
        offer_check = self.env['estate.property'].browse(vals['property_id'])
        offer_check.state='offer_received'
        if offer_check.best_price > vals['price']:
            raise exceptions.ValidationError(f'The offer must be greater than {offer_check.best_price}')
        return super(EstatePropertyOffer, self).create(vals)