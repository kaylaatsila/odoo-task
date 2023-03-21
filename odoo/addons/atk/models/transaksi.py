from odoo import models, fields, api


class Transaksi(models.Model):
    _name = 'transaksi'

    product_name = fields.Many2one(comodel_name='master', inverse_name='product_name', string='Nama Produk',
                                   required=True)

    division = fields.Char(string='Divisi',
                           required=True)

    product_price = fields.Integer(related='product_name.product_price', string='Total Harga',
                                    readonly=True)
