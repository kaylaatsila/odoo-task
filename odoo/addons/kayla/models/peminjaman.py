from odoo import models, fields, api
from datetime import timedelta


class Peminjaman(models.Model):
    _name = 'peminjaman.perpustakaan'

    date_start = fields.Date(string='Tanggal Peminjaman',
                             required=True)

    date_end = fields.Date(string='Tanggal Pengembalian',
                           readonly=True, compute='_get_date_end', store=True)

    borrow_member_id = fields.Many2one(comodel_name='anggota.perpustakaan', string='Nama',
                                       required=True, ondelete='cascade')

    borrow_book_id = fields.Many2one(comodel_name='buku.perpustakaan', string='Judul',
                                     required=True, ondelete='cascade')

    return_ids = fields.One2many(
        comodel_name='pengembalian.perpustakaan', inverse_name='return_id', string='ID Pengembalian')

    @api.depends('date_start')
    def _get_date_end(self):
        for r in self:
            if not r.date_start:
                r.date_end = r.date_start
                continue

            start = fields.Datetime.from_string(r.date_start)
            r.date_end = start + timedelta(days=7, seconds=-1)


