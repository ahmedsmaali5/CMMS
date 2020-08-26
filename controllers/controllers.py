# -*- coding: utf-8 -*-
from odoo import http

# class CmmsOpenTt(http.Controller):
#     @http.route('/cmms__open_tt/cmms__open_tt/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cmms__open_tt/cmms__open_tt/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cmms__open_tt.listing', {
#             'root': '/cmms__open_tt/cmms__open_tt',
#             'objects': http.request.env['cmms__open_tt.cmms__open_tt'].search([]),
#         })

#     @http.route('/cmms__open_tt/cmms__open_tt/objects/<model("cmms__open_tt.cmms__open_tt"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cmms__open_tt.object', {
#             'object': obj
#         })