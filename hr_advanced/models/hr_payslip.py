# -*- coding: utf-8 -*-
from odoo import models, fields


class Move(models.Model):
    _inherit = 'account.move'

    move_name = fields.Char(string='Number', store=True, index=True)


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def _get_existing_lines(self, line_ids, line, account_id, debit, credit):
        existing_lines = super(HrPayslip, self)._get_existing_lines(line_ids, line, account_id, debit, credit)

        payslip_run = line.slip_id.payslip_run_id
        if existing_lines and payslip_run and payslip_run.payslip_count > 1:
            return False

        return existing_lines

    def get_actual_number_of_days(self):
        contract = self.contract_id
        work_hours = contract._get_work_hours(self.date_from, self.date_to)
        work_hours_ordered = sorted(work_hours.items(), key=lambda x: x[1])
        biggest_work = work_hours_ordered[-1][0] if work_hours_ordered else 0
        add_days_rounding = 0
        number_of_days = 0
        calendar = contract.resource_calendar_id
        for work_entry_type_id, hours in work_hours_ordered:
            work_entry_type = self.env['hr.work.entry.type'].browse(work_entry_type_id)
            days = round(hours / calendar.hours_per_day, 5) if calendar.hours_per_day else 0
            if work_entry_type_id == biggest_work:
                days += add_days_rounding
            number_of_days = self._round_days(work_entry_type, days)
            add_days_rounding += (days)
        return number_of_days





class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'

    # batch get only employees have ready contracts

    def _get_available_contracts_domain(self):
        super(HrPayslipEmployees, self)._get_available_contracts_domain()
        return [('contract_ids.state', '=', 'open'), ('company_id', '=', self.env.company.id)]


