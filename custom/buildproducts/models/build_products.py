from odoo import models, fields
from odoo import api

class BuildProducts(models.Model):
    _name = "build.products"
    _description = "Build Products"
    _order = 'id desc'
     
    name = fields.Char('Product Name' , required=True)
    description = fields.Char('Description', required=True)
    product_type = fields.Selection(selection=[('opc', 'OPC'), ('ppc', 'PPC')])
    product_grade = fields.Selection(selection=[('33', '33'), ('43', '43'), ('53', '53')])
    product_price = fields.Float('Product Price')
    product_quantity = fields.Integer('Product Quantity')
    active = fields.Boolean(string='Active', default=True)
    order_ids = fields.One2many('build.products.order', 'product_id', string='Orders')
    tag_ids = fields.Many2many('build.products.tag' , string='Product Tags')
    total_sale = fields.Float(string='Total Sales' , compute='_compute_total_sales', store=True)

    @api.depends('order_ids.total_amount')
    def _compute_total_sales(self):
        for record in self:
            if record.order_ids:
                record.total_sale = sum(record.order_ids.mapped('total_amount'))
            else:
                record.total_sale=0.0

    def action_opc(self):
        for record in self:
            record.product_type = 'opc'

    def action_ppc(self):
        for record in self:
            record.product_type = 'ppc'

    _sql_constraints = [
        ('check_price', 'CHECK(product_price > 0)', 'Product Price must be Positive.')
    ]