from odoo import models, fields

class AddOfferWizard(models.TransientModel):
    _name = "add.offers.wizard"

    price = fields.Float("Price")
    partner_id = fields.Many2one('res.partner', string='Partner')

    def create_offer(self):
        property = self.env['estate.property'].browse(self._context.get('active_ids'))
        for record in self:
            for data in property:
                self.env['estate.property.offer'].create({
                    'price' : record.price,
                    'partner_id' : record.partner_id.id,
                    'property_id' : data.id
                })




