from odoo import models, fields, api


class Anggota(models.Model):
    _name = 'anggota.perpustakaan'

    name = fields.Many2one(comodel_name='res.users', string='Nama Anggota',
                           required=True)
    
    date = fields.Date(string='Tanggal Keanggotaan',
                       required=True)

    @api.model
    def create(self, member):
        if member.get('name'):
            member['name'] = member['name'].title()
        return super(Anggota, self).create(member)

    def write(self, member):
        if 'name' in member:
            member['name'] = member['name'].title()
        return super(Anggota, self).write(member)
