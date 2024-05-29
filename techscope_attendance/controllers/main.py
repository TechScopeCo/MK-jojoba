# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.addons.website_sale.controllers.main import WebsiteSale

from odoo import http, _
from odoo.http import request, Response
from datetime import datetime, timedelta


class ETAWebController(http.Controller):

    @http.route("/post_attendance_log", type="json", auth="public", method=["POST"])
    def post_attendance_log(self, **kw):
        request_headers = http.request.httprequest.headers.environ
        comp = request.env.company
        if not comp:
            comp = request.env['res.company'].sudo().search([], limit=1)
        att_app_passwd = comp.att_app_passwd
        rec_passwd = request_headers.get("HTTP_APIKEY", '')
        if rec_passwd != att_app_passwd:
            return "Not Authorized"
        else:
            jsonreq = request.dispatcher.jsonrequest
            # dic = json.dumps(jsonreq)
            # for doc in jsonreq["docs"]:
            att_obj = request.env["ts.attendance.log.temp"].sudo()
            records = att_obj.create(jsonreq["docs"])
            for rec in records:
                # our time in time zon UTC +2 or Africe/Cairo
                rec.punching_time = rec.punching_time + timedelta(hours=-2)

            return "DATA RECEIVED"
