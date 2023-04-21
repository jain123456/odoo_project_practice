from odoo import models, fields

class BuildProductsTag(models.Model):
    _name = 'build.products.tag'
    _description = 'Build Products Tag'

    name = fields.Char('Products Tags', required=True)
    color = fields.Integer('Color')

    _sql_constraints = [
        ('check_products_tags', 'UNIQUE(name)', 'Product Tag already exists.')
    ]