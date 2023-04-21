from odoo import models, fields
from odoo import api
from odoo.exceptions import ValidationError, UserError

class BuildProductsOrder(models.Model):
    _name = 'build.products.order'
    _description = 'Build Products Order'
    _order = 'total_amount desc'
    
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    order_date = fields.Date(string='Order Date', default=fields.Date.today())
    qty_ordered = fields.Float(string='Quantity Ordered', required=True)
    delivery_address = fields.Text(string='Delivery Address', required=True)
    delivery_date = fields.Date('Expected Delivery Date' , default=fields.Date.add(fields.Date.today(), days=2))
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('in_delivery', 'In Delivery'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled')
    ], string='State', default='new')
    product_id = fields.Many2one('build.products', string='Product', required=True)
    total_amount = fields.Float(compute='_compute_total_amount' , inverse='_inverse_total_amount' , string='Total Amount' , store=True)

    @api.depends('qty_ordered', 'product_id.product_price')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = order.qty_ordered * order.product_id.product_price

    def _inverse_total_amount(self):
        for order in self:
            order.qty_ordered = order.total_amount / order.product_id.product_price

    def action_canceled(self):
        for order in self:
            if order.state == 'delivered':
                raise UserError('Delivered Order cannot be marked canceled')
            order.state = 'canceled'
            # # order.product_id.product_quantity += order.qty_ordered
            order.total_amount = 0
            order.qty_ordered = 0
            # if order.product_id:
            #     order.product_id.product_quantity += order.qty_ordered
            #     order.product_id.total_sale -= order.total_amount
            # this will not work because afterwards when a new record is created then it will again add the total_amount to total_sale.

    def action_delivered(self):
        for order in self:
            if order.state == 'canceled':
                raise UserError('Canceled order cannot be marked delivered')
            order.state = 'delivered'

    # @api.constrains('total_amount', 'product_id.product_price')
    # def _check_total_amount(self):
    #     for order in self:
    #         if order.total_amount <= order.product_id.product_price:
    #             raise ValidationError('Total Amount cannot be less than Product Price!')

    @api.model
    def create(self, vals):
        order = super(BuildProductsOrder, self).create(vals)
        if vals['total_amount'] <= order.product_id.product_price:
            raise ValidationError('Total Amount cannot be less than Product Price!')
        order.product_id.product_quantity -= order.qty_ordered
        return order
    
    def write(self, vals):
        if 'qty_ordered' in vals and self.product_id:
            qty_diff = vals['qty_ordered'] - self.qty_ordered
            self.product_id.product_quantity -= qty_diff
        return super(BuildProductsOrder, self).write(vals)
    
    def unlink(self):
        for order in self:
            if order.product_id:
                order.product_id.product_quantity += order.qty_ordered
            if order.state not in ['new', 'canceled']:
                raise ValidationError("You can not delete a property that is not in 'New' or 'Canceled' state.")
        return super(BuildProductsOrder, self).unlink()
   