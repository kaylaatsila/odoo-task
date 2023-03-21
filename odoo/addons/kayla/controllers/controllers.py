# -*- coding: utf-8 -*-
from odoo import http

# class Kayla(http.Controller):
#     @http.route('/kayla/kayla/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kayla/kayla/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('kayla.listing', {
#             'root': '/kayla/kayla',
#             'objects': http.request.env['kayla.kayla'].search([]),
#         })

#     @http.route('/kayla/kayla/objects/<model("kayla.kayla"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kayla.object', {
#             'object': obj
#         })