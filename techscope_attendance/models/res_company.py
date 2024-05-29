from odoo import fields, models, api, _

from datetime import datetime, timedelta
import secrets


class ResCompany(models.Model):
    _inherit = 'res.company'
    att_app_passwd = fields.Char(
        string='Attendance Desktop Password'
    )
