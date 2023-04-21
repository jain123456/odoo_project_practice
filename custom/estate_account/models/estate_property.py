from odoo import models, fields, api, Command

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):  
        result = super(EstateProperty, self).action_sold()
        print('Property sold!')
        invoice = self.env['account.move'].create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids':[
                Command.create({
                    'name':'Brokerage',
                    'quantity':1,
                    'price_unit': self.selling_price*0.06,
                    'tax_ids': False,
                }),
                Command.create({
                   'name':'Administrative Fees',
                    'quantity':1,
                    'price_unit': 100.00, 
                    'tax_ids': False,
                })
            ]
        })
        return result