from odoo import models, fields, api


class Produk(models.Model):
    _name = 'produk'
    _rec_name = 'product_name'

    product_name = fields.Char(string='Nama Produk',
                               required=True, store=True)

    order_limit = fields.Integer(string='Limit Order',
                                 required=True, store=True)

    product_price = fields.Integer(string='Harga Satuan',
                                   required=True, store=True)

    @api.onchange('product_name')
    def set_title(self):
        for r in self:
            if r.product_name:
                r['product_name'] = r['product_name'].title()


class Divisi(models.Model):
    _name = 'divisi'
    _rec_name = 'division_name'

    division_name = fields.Char(string='Nama Divisi',
                                required=True, store=True)

    # @api.onchange('division_name')
    # def set_title(self):
    #     for r in self:
    #         if r.division_name:
    #             r['division_name'] = r['division_name'].upper()
