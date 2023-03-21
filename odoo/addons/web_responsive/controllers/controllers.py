# -*- coding: utf-8 -*-
from odoo import http

# class Atk(http.Controller):
#     @http.route('/atk/atk/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/atk/atk/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('atk.listing', {
#             'root': '/atk/atk',
#             'objects': http.request.env['atk.atk'].search([]),
#         })

#     @http.route('/atk/atk/objects/<model("atk.atk"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('atk.object', {
#             'object': obj
#         })