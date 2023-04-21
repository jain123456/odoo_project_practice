from odoo import models, fields, api, Command

class BuildProductsOrder(models.Model):
    _inherit = 'build.products.order'

    def action_delivered(self):
        result = super(BuildProductsOrder, self).action_delivered()
        print('Order Delivered')
        invoice = self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids':[
                 Command.create({
                'product': self.product_id.name,
                'quantity': self.qty_ordered,
                'price_unit': self.product_id.product_price,
                'tax_ids': False,
                 }),
                Command.create({
                    'name':'Loading Charge',
                    'quantity':1,
                    'price_unit': self.total_amount*0.02,
                    'tax_ids': False,
                })
            ]
        })
        return result