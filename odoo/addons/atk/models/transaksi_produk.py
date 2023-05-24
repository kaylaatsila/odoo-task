from odoo import models, fields, api

class ProdukTransaksi(models.Model):
    _name = 'produk.transaksi'

    @api.multi
    def _set_price(self):
        for r in self:
            r.sub_total = r.product_price * r.quantity
            
    quantity = fields.Integer(string='Quantity')
    sub_total = fields.Integer(string='Sub Total', compute='_set_price', readonly=True)
    transaction_id = fields.Many2one(comodel_name='transaksi', string='Transaksi')
    product_id = fields.Many2one(comodel_name='produk', string='Product Name')
    product_price = fields.Integer(related='product_id.product_price')
    order_limit = fields.Integer(related='product_id.order_limit')

    @api.onchange('quantity')
    def verify_quantity(self):
        for r in self:
            if r.quantity > r.order_limit:
                return {
                    'value': {'quantity': r.order_limit}, 
                    'warning': {'title': "Warning", 
                                'message': "Jumlah Pemesanan Tidak Boleh Melebihi Limit Order"}  
                                
                }

            if r.quantity < 0:
                return {
                    'value': {'quantity':  1}, 
                    'warning': {'title': "Warning", 
                                'message': "Jumlah Pemesanan Tidak Boleh Negatif"} 
                                
                }