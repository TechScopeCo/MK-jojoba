{
    "name": "Send Payslip By Email",
    "summary": "Shipping per product module allows customer to select delivery method for each product separately and delivery amount will be calculated for each product.",
    "category": "Website",
    "version": "16.0.0.1",
    "sequence": 1,
    "author": "Synodica Solutions Pvt.Ltd",
    "license": "Other proprietary",
    "website": "",
    "description": """ Just One Click and it's Gone!
Save a lot of time by simplifying the process of dispatching payslips to your much valued employees.
 Use less effort and reduce delays in serving your employees.
""",
    "live_test_url": "",
    "depends": ['hr_holidays', 'hr', 'mail','hr_payroll', 'hr_payroll_holidays'],
    "data": [
        'security/ir.model.access.csv',
        'data/mail_template_employee.xml',
        'wizard/payslip_wizard.xml',
        'views/view_hr_payslip.xml',
        'views/view_hr_payslip_run.xml',
        'views/hr_employee_view.xml',
    ],
    "images": ["static/description/Payslip.gif"],
    "application": True,
    "installable": True,
    "auto_install": False,
    "price": 00.00,
    "currency": "USD",
}