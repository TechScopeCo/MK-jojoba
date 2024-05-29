from odoo import api, fields, models, _
from datetime import datetime, timedelta

class TSAttendanceLog(models.Model):
    _name = 'ts.attendance.log'
    _description = 'Attendance Log'
    

    def fetch_data_from_temp(self):
        return self.env['ts.attendance.log.temp'].sudo().move_correct_data_to_main()

    def process_data(self):
        # this method to combine check in and check out in one record
        # and to calculate the working hours
        # first check if the check in line is xisit in ht.attendance if not create it then search for it is log out
        records = self.sudo().search(
            [('punch_type', '=', '0'), ('attendance_line_id', '=', False), ('employee_id', '!=', False)])
        for rec in records:
            att_line = rec.env['hr.attendance'].search([('employee_id', '=', rec.employee_id.id), ('check_in', '=', rec.punching_time)])
            if not att_line:
                # Create the line with employee_id and check_in
                new_line = rec.env['hr.attendance'].create({'employee_id': rec.employee_id.id, 'check_in': rec.punching_time})
                rec.attendance_line_id = new_line.id
                # Search for check ou record in ts.attendance.log
                first_hour = rec.punching_time.replace(hour=0, minute=0, second=0, microsecond=0)
                las_hour = rec.punching_time.replace(hour=23, minute=59, second=59, microsecond=0)
                chk_out = rec.env['ts.attendance.log'].search([('employee_id', '=', rec.employee_id.id), (
                    'punching_time', '>=', first_hour), (
                    'punching_time', '<=', las_hour), ('punch_type', '=', '1')], limit=1, order='punching_time desc')
 
                if chk_out:
                    chk_out.attendance_line_id = new_line.id
                    new_line.check_out = chk_out.punching_time
            else:
                rec.attendance_line_id = att_line.id
                first_hour = rec.punching_time.replace(
                    hour=0, minute=0, second=0, microsecond=0)
                las_hour = rec.punching_time.replace(
                    hour=23, minute=59, second=59, microsecond=0)
                chk_out = rec.env['ts.attendance.log'].search([('employee_id', '=', rec.employee_id.id), (
                    'punching_time', '>=', first_hour), (
                    'punching_time', '<=', las_hour), ('punch_type', '=', '1')], limit=1, order='punching_time desc')
                if chk_out:
                    chk_out.attendance_line_id = att_line.id
                    att_line.check_out = chk_out.punching_time
                    

    employee_id = fields.Many2one('hr.employee', string='Employee', compute="_compute_employee_id", store=True)
    @api.depends("employee_code")
    def _compute_employee_id(self):
        for rec in self:
            emp = self.env['hr.employee'].search([('pin', '=', rec.employee_code)], limit=1)
            rec.employee_id = emp.id
                
    employee_code = fields.Char(string='Employee Code',required=True, index=True)
    device_id = fields.Char(string='Biometric Device ID')
    punch_type = fields.Selection([('0', 'Check In'),
                                   ('1', 'Check Out'),
                                   ('2', 'Break Out'),
                                   ('3', 'Break In'),
                                   ('4', 'Overtime In'),
                                   ('5', 'Overtime Out')],
                                  string='Punching Type')

    attendance_type = fields.Selection([('1', 'Finger'),
                                        ('15', 'Face'),
                                        ('2', 'Type_2'),
                                        ('3', 'Password'),
                                        ('4', 'Card')], string='Category')
    punching_time = fields.Datetime(string='Punching Time')
    
    attendance_line_id = fields.Many2one('hr.attendance', string='Attendance Line', ondelete='cascade')
    
    hash_code = fields.Char(string='Hash', compute="_compute_hash", store=True, index=True)
    
    @api.depends("employee_code", "device_id", "punch_type", "attendance_type", "punching_time")
    def _compute_hash(self):
        # Used to improve search only
        for rec in self:
            if rec.punching_time:
                rec.hash_code = rec.employee_code + rec.device_id + rec.punch_type + \
                    rec.attendance_type + \
                    rec.punching_time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                rec.hash_code = False

class TSAttendanceLogTemp(models.Model):
    _name = 'ts.attendance.log.temp'
    _inherit = 'ts.attendance.log'
    _description = 'Attendance Log Temp'

    def button_move_to_main(self):
        self.move_correct_data_to_main()

    def move_correct_data_to_main(self):
        # This method will check if the record is already exist in the main table if not it will move it then clear the temp table
        att_obj = self.env['ts.attendance.log'].sudo() 
        for rec in self.search([]):
            
            main_rec = self.env['ts.attendance.log'].search([('hash_code', '=', rec.hash_code)])
            if not main_rec:
                att_obj.create({
                    'employee_code': rec.employee_code,
                    'device_id': rec.device_id,
                    'punch_type': rec.punch_type,
                    'attendance_type': rec.attendance_type,
                    'punching_time': rec.punching_time,
                                })
        
        # for faster perfmonce we will truncate the temp table
        self.env.cr.execute("TRUNCATE TABLE ts_attendance_log_temp")
                
