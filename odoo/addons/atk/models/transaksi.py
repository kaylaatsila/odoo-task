from odoo import models, fields, api


class Transaksi(models.Model):
    _name = 'transaksi'
    _rec_name = 'division_id'

    @api.multi
    def _set_grand_total(self):
        for r in self:
            r.grand_total = sum(r.product_transaction_id.mapped('sub_total'))
            
    grand_total = fields.Integer(string='Grand Total', compute='_set_grand_total', readonly=True)
    justification = fields.Text(string='Reason of Rejection')
    date = fields.Date(string='Transaction Date',  required=True, readonly=True, states={'draft': [('readonly', False)]})
    product_transaction_id = fields.One2many(comodel_name='produk.transaksi', inverse_name='transaction_id', required=True, readonly=True,  states={'draft': [('readonly', False)]})
    division_id = fields.Many2one(comodel_name='divisi', required=True, readonly=True, states={'draft': [('readonly', False)]},)

    state = fields.Selection([('draft', 'Draft'), 
                              ('sent', 'Request'), 
                              ('reject', 'Rejected'), 
                              ('approve', 'Approved')], string='State', readonly=True, copy=False, default='draft')

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
