from odoo import models, fields, api


class Transaksi(models.Model):
    _name = 'transaksi'
    _rec_name = 'division'

    product_transaction = fields.One2many(comodel_name='produk.transaksi',
                                          inverse_name='transaction',
                                          required=True,
                                          readonly=True,
                                          states={'draft': [('readonly', False)]})

    division = fields.Many2one(comodel_name='divisi',
                               required=True,
                               readonly=True,
                               states={'draft': [('readonly', False)]},)

    grand_total = fields.Integer(string='Grand Total',
                                 compute='_set_grand_total',
                                 readonly=True)

    date = fields.Date(string='Transaction Date',
                       required=True,
                       readonly=True,
                       states={'draft': [('readonly', False)]})

    justification = fields.Text(string='Reason of Rejection')

    @api.multi
    def _set_grand_total(self):
        for r in self:
            r.grand_total = sum(r.product_transaction.mapped('sub_total'))

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Request'),
        ('reject', 'Rejected'),
        ('approve', 'Approved'),
    ], string='State',
        readonly=True,
        copy=False,
        default='draft')

    @api.multi
    def action_draft(self):
        self.write({'state': 'draft'})

    @api.multi
    def action_send(self):
        self.write({'state': 'sent'})

    @api.multi
    def action_reject(self):
        self.write({'state': 'reject'})

    @api.multi
    def action_approve(self):
        self.write({'state': 'approve'})

    @api.multi
    def set_reject(self):
        reference = self.env.ref('atk.reject_form_view').id
        return {
            'name': 'Reason of Rejection',
            'type': 'ir.actions.act_window',
            'res_model': 'transaksi',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(reference, 'form')],
            'target': 'new',
            'res_id': self.id}


class ProdukTransaksi(models.Model):
    _name = 'produk.transaksi'

    transaction = fields.Many2one(comodel_name='transaksi',
                                  string='Transaksi')

    product = fields.Many2one(comodel_name='produk',
                              string='Product Name')

    product_price = fields.Integer(related='product.product_price')

    order_limit = fields.Integer(related='product.order_limit')

    quantity = fields.Integer(string='Quantity')

    sub_total = fields.Integer(
        string='Sub Total',
        compute='_set_price',
        readonly=True)

    @api.multi
    def _set_price(self):
        for r in self:
            r.sub_total = r.product_price * r.quantity

    @api.onchange('quantity')
    def verify_quantity(self):
        for r in self:
            if r.quantity > r.order_limit:
                return {
                    'value': {'quantity': r.order_limit  # mengisi field seats dengan nilai  limit order
                              },
                    'warning': {'title': "Warning",  # judul pop up
                                'message': "Jumlah Pemesanan Tidak Boleh Melebihi Limit Order"  # pesan pop up
                                }
                }

            if r.quantity < 0:
                return {
                    'value': {'quantity':  1  # mengisi field seats dengan nilai  1
                              },
                    'warning': {'title': "Warning",  # judul pop up
                                'message': "Jumlah Pemesanan Tidak Boleh Negatif"  # pesan pop up
                                }
                }


class Rejeksi(models.TransientModel):
    _name = 'rejeksi.transaksi'

    transaction = fields.Many2one(comodel_name='transaksi',
                                  string='Transaksi')

    justification = fields.Text(string='Justifikasi', default='_justification')

    @api.multi
    def _justification(self):
        for r in self.transaction:
            r.justification = self.justification
            return {}
