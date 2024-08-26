from odoo import fields, models


class InheritResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    contract_expiration_reminder = fields.Integer(
        string="Contract Expiration Reminder",
        related="company_id.contract_expiration_reminder",
        readonly=False
    )
    hr_manager_contract_id = fields.Many2one(
        related="company_id.hr_manager_contract_id",
        string="HR Manager",
        readonly=False
    )
