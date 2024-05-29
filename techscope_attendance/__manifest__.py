# -*- coding: utf-8 -*-
{
    'name': "Techscope Attendance Integration",

    'summary': """
        Techscope Attendance Integration""",

    'description': """
        Techscope Attendance Integration
    """,

    'author': "Abdulrahman Rabie, TechScope Team",
    'website': "http://techscopeco.com/",

    'category': 'eCommerce',
    'version': '16.0.1.1.0',

    'depends': ['hr_attendance', ],

    'data': [

        'security/ir.model.access.csv',
        'views/ts_attendance_log.xml',
        'views/res_company.xml',
        'data/act.xml',
    ],
    'demo': [

    ],
}
