from odoo import models, fields, api


class Divisi(models.Model):
    _name = 'divisi'
    _rec_name = 'division_name'

    division_name = fields.Char(string='Division Name', required=True, store=True)