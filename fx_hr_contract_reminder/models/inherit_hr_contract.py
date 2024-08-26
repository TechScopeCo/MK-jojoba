
from datetime import date, datetime, timedelta

from odoo import fields, models


class InheritContract(models.Model):
    _inherit = 'hr.contract'

    def _send_email_to_hr_manager(self, hr_manager_contract_id, contracts):
        """
            Sends an email reminder to the HR manager about expiring contracts.
        """

        template_hr_manager_id = self.env.ref('fx_hr_contract_reminder.mail_template_reminder_contract_hr_manager',
            raise_if_not_found=False)

        ctx_hr_manager = {
            'hr_manager_contract_id': hr_manager_contract_id.employee_id.name,
            'contracts': [contract.employee_id.name + " - " + (contract.date_end).strftime("%d-%m-%Y") for contract in
                contracts],
            'email_from': self.env.user.company_id.email,
            'email_to': str(hr_manager_contract_id.employee_id.work_email),
            'company_name': self.env.user.company_id.name
        }
        template_hr_manager_id.with_context(ctx_hr_manager).send_mail(self.id, force_send=True, raise_exception=False)

    def _send_email_to_employee(self, employee, contract):
        """
            Sends an email reminder to an employee about their expiring contract.
        """

        template_employee_id = self.env.ref('fx_hr_contract_reminder.mail_template_reminder_contract_employee',
            raise_if_not_found=False)

        ctx_employee = {
            'employee_name': employee.name,
            'contract_date': (contract.date_end).strftime("%d-%m-%Y"),
            'email_from': self.env.user.company_id.email,
            'email_to': str(employee.work_email),
            'company_name': self.env.user.company_id.name
        }
        template_employee_id.with_context(ctx_employee).send_mail(self.id, force_send=True, raise_exception=False)

    def _cron_auto_reminder_hr_contract(self):
        """
            Cron job function to automatically send contract expiration reminders.
        """
        company = self.env['res.company'].sudo().search([], limit=1)
        if company:
            contract_expiration_reminder = company.contract_expiration_reminder
            hr_manager_contract_id = company.hr_manager_contract_id

            reminder = date.today() + timedelta(days=contract_expiration_reminder)

            contracts = self.search([("date_end", "=", reminder)])

            if contracts:
                self._send_email_to_hr_manager(hr_manager_contract_id, contracts)

                for contract in contracts:
                    employee = contract.employee_id
                    if employee:
                        self._send_email_to_employee(employee, contract)