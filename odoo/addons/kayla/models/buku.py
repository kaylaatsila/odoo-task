from odoo import models, fields, api


class Buku(models.Model):
    _name = 'buku.perpustakaan'

    name = fields.Char(string='Judul',
                       required=True)

    author = fields.Many2one(comodel_name='res.partner', string='Pengarang',
                             required=True)

    stocks = fields.Integer(string='Jumlah Stok')

    taken_stocks = fields.Float(string='Jumlah Stok Terpinjam',
                                compute='_stocks_taken')

    left_stocks = fields.Float(string='Sisa Stok',
                               compute='_stocks_left')

    borrow_book_ids = fields.One2many(comodel_name='peminjaman.perpustakaan',
                                      inverse_name='borrow_book_id')

    @api.depends('borrow_book_ids')
    def _stocks_taken(self):
        for book in self:
            book.taken_stocks = len(book.borrow_book_ids)

    def _stocks_left(self):
        for book in self:
            if book.stocks:
                book.left_stocks = (
                    (book.stocks - book.taken_stocks) / book.stocks) * 100
            else:
                book.left_stocks = 0.0

    @api.model
    def create(self, book):
        if book.get('name'):
            book['name'] = book['name'].title()
        return super(Buku, self).create(book)

    def write(self, book):
        if 'name' in book:
            book['name'] = book['name'].title()
        return super(Buku, self).write(book)
