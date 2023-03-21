from odoo import models, fields, api

class Master(models.Model):
    _name = 'master'
    _rec_name = 'product_name'

    product_name = fields.Char(string='Nama Produk',
                               required=True, store=True)

    order_limit = fields.Integer(string='Limit Order',
                                 required=True, store=True)

    product_price = fields.Integer(string='Harga Produk',
                                   required=True, store=True)

    @api.onchange('product_name')
    def set_title(self):
        for r in self:
            if r.product_name:
                r['product_name'] = r['product_name'].title()
