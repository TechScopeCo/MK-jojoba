
from odoo import fields, models


class InheritResCompany(models.Model):
    _inherit = "res.company"

    contract_expiration_reminder = fields.Integer(
        string="Contract Expiration Reminder",
        default=7
    )
    hr_manager_contract_id = fields.Many2one(
        comodel_name="res.users",
        string="HR Manager",
    )
