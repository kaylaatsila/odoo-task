from odoo import models, fields, api

class Produk(models.Model):
    _name = 'produk'
    _rec_name = 'product_name'

    product_name = fields.Char(string='Product Name', required=True, store=True)
    order_limit = fields.Integer(string='Order Limit', required=True, store=True)
    product_price = fields.Integer(string='Unit Price', required=True, store=True)

    @api.onchange('product_name')
    def set_title(self):
        for r in self:
            if r.product_name:
                r['product_name'] = r['product_name'].title()



