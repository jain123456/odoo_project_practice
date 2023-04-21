from odoo import models, fields
from odoo import api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id desc"

    name = fields.Char('Property Name' , required=True)
    image = fields.Image()
    description = fields.Char('Description', required=True)
    postcode = fields.Char('Postcode' , required=True)
    date_availability = fields.Date('Date of Availability' , default=fields.Date.add(fields.Date.today(),months=3) , copy=False)
    expected_price = fields.Float('Expected Price')
    selling_price = fields.Float('Selling Price' , readonly=True , copy=False)
    bedrooms = fields.Integer('No. of Bedrooms' , default=2)
    property_type_id = fields.Many2one('estate.property.type' , string='Property Types')
    living_area = fields.Integer('Living Area (sqm)' , required=True)
    facades = fields.Integer('Facades' , required=True)
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden' )
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(selection=[('north', 'North'), ('south','South'), ('west','West'), ('east', 'East')])
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], string='State', default='new')
    active = fields.Boolean(string='Active' , default=True)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag' , string='Property Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    total_area = fields.Float(string='Total Area' , compute='_compute_total_area')
    best_price = fields.Float(string='Best Offer' , compute='_compute_best_price')
    
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
    
    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('Canceled Property cannot be marked sold')
            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold Property cannot be marked cancel')
            record.state = 'canceled'

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)', 'Expected Price must be greater than 0.'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'Selling Price must be greater than 0.'),
    ]

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2) and float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                raise ValidationError("Selling price cannot be lower than 90% of expected price!")
            
    def unlink(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise ValidationError("You can not delete a property that is not in 'New' or 'Canceled' state.")
        return super(EstateProperty, self).unlink()
    
    @api.ondelete(at_uninstall=False)
    def _unlink_state(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise ValidationError("You can not delete a property that is not in 'New' or 'Canceled' state.")