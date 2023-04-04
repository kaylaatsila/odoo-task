from odoo import models, fields, api


class Transaksi(models.Model):
    _name = 'transaksi'
    _rec_name = 'division'

    product_transaction = fields.One2many(comodel_name='produk.transaksi', inverse_name='transaction',
                                          required=True, states={'draft': [('readonly', False)]})

    division = fields.Many2one(comodel_name='divisi',
                               required=True, states={'draft': [('readonly', False)]})

    grand_total = fields.Integer(string='Grand Total', compute='_set_grand_total',
                                 readonly=True)

    date = fields.Date(string='Tanggal Transaksi',
                       required=True, states={'draft': [('readonly', False)]})

    @api.multi
    def _set_grand_total(self):
        for r in self:
            r.grand_total = sum(r.product_transaction.mapped('sub_total'))

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Request'),
        ('reject', 'Rejected'),
        ('approve', 'Approved'),
    ], string='State', readonly=True, copy=False, default='draft')

    @api.multi
    def action_draft(self):
        self.write({'state': 'draft'})

    @api.multi
    def action_send(self):
        self.write({'state': 'sent'})

        for r in self.product_transaction:
            if r.quantity > r.order_limit or r.quantity <= 0:
                self.write({'state': 'reject'})
            else:
                self.write({'state': 'approve'})


class ProdukTransaksi(models.Model):
    _name = 'produk.transaksi'

    transaction = fields.Many2one(comodel_name='transaksi')

    product = fields.Many2one(comodel_name='produk',
                              string='Nama Produk', required=True)

    product_price = fields.Integer(related='product.product_price')

    order_limit = fields.Integer(related='product.order_limit')

    quantity = fields.Integer(string='Jumlah', required=True)

    sub_total = fields.Integer(
        string='Sub Total', compute='_set_price', readonly=True)

    @api.multi
    def _set_price(self):
        for r in self:
            r.sub_total = r.product_price * r.quantity
