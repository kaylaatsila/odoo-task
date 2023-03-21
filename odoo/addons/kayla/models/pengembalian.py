from odoo import models, fields, api
import datetime


class Pengembalian(models.Model):
    _name = 'pengembalian.perpustakaan'

    date_return = fields.Date(string='Tanggal Pengembalian',
                              required=True)

    return_id = fields.Many2one(comodel_name='peminjaman.perpustakaan', string='Peminjaman',
                                required=True, ondelete='cascade')

    return_member_id = fields.Many2one(related='return_id.borrow_member_id', string='Nama',
                                       readonly=True)

    return_book_id = fields.Many2one(related='return_id.borrow_book_id', string='Judul',
                                     readonly=True)

    return_deadline_id = fields.Date(related='return_id.date_end', string='Tenggat Pengembalian',
                                     readonly=True)

    penalty = fields.Float(string='Denda', compute='_get_penalty',
                           readonly=True)

    status = fields.Selection([
        ('returned', 'Dikembalikan'),
        ('late', 'Terlambat'),
    ], string='Status', compute='_get_penalty', store=True)

    @api.depends('date_return')
    def _get_penalty(self):
        for r in self:
            if not r.date_return or not r.return_deadline_id:
                r.penalty = 0.0
                continue

            date_return = fields.Datetime.from_string(r.date_return)
            date_end = fields.Datetime.from_string(r.return_deadline_id)

            if date_return > date_end:
                penalty = (date_return - date_end).days * 10000
                r.penalty = penalty
                r.status = 'late'
            else:
                r.penalty = 0.0
                r.status = 'returned'
