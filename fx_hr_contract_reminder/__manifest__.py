{
    "name": "HR Contract Reminder",
    "summary": "HR Contract Reminder",
    "description": """HR Contract Reminder""",
    "version": "17.0.0.1.0",
    "author": "Doan Thanh Sang",
    "website": "",
    "category": "Human Resources/Contract",
    "depends": ["hr_contract"],
    "data": [
        "data/ir_cron.xml",
        "data/mail_template_data.xml",
        "views/inherit_res_config_settings_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
    "auto_install": False,
    "application": True,
    "images": [
        "static/description/icon.png",
    ],
}
