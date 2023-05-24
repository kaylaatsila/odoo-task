from odoo import models, fields, api

class Rejeksi(models.TransientModel):
    _name = 'rejeksi.transaksi'

    justification = fields.Text(string='Justifikasi', default='_justification')
    transaction_id = fields.Many2one(comodel_name='transaksi', string='Transaksi')

    @api.multi
    def _justification(self):
        for r in self.transaction_id:
            r.justification = self.justification
            return {}