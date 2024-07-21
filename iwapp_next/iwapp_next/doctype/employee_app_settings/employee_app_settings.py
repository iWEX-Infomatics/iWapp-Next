# Copyright (c) 2024, Iwex Informatics and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, time_diff_in_seconds

class EmployeeAppSettings(Document):
	pass
	def before_save(self):
		if self.employee_app_users:
			self.total_app_users = len(self.employee_app_users)
			for emp in self.employee_app_users:
				emp.duration = calculate_duration(emp.last_pinged_on)

@frappe.whitelist()
def get_user_id_details():
	user_details = frappe.db.sql("""
			SELECT
				emp.name as employee_id,
				user.name as user_id,
				user.api_key as user_key,
				emp.custom_user_api_secret as api_secret,
				emp.custom_last_pinged_on as last_pinged,
				emp.attendance_device_id as mac_id
			FROM
				`tabEmployee` as emp LEFT JOIN
				`tabUser` as user ON emp.user_id = user.name
			WHERE
				emp.status = "Active" and user.api_key != ""
					   """, as_dict = True)
	if user_details:
		return user_details

@frappe.whitelist()
def update_user_id_details(employee_id, api_secret, user_id, mac_id = None, last_pinged = None):
	user_api_key = frappe.db.get_value("User", user_id, "api_key")
	emp_settings = frappe.get_doc('Employee App Settings')
	employee_found = False
	if user_api_key:
		if emp_settings.employee_app_users:
			for emp in emp_settings.employee_app_users:
				if emp.employee_id == employee_id:
					emp.employee_name = employee_id
					emp.user_id = user_id
					emp.user_api_key = user_api_key
					emp.user_api_secret = api_secret,
					emp.last_mac_id = mac_id,
					emp.last_pinged_on = last_pinged
					employee_found = True
					break

		if not employee_found:
			emp_settings.append('employee_app_users', {
				'employee_name': employee_id,
				'employee_id': employee_id,
				'user_id': user_id,
				'user_api_key': user_api_key,
				'user_api_secret': api_secret,
				'last_mac_id': mac_id,
				'last_pinged_on' : last_pinged
			})

		# Save the updated emp_settings document
		emp_settings.save()
		frappe.msgprint("Employee App Settings updated.")
	else:
		frappe.msgprint(f"Please generate a API key for <b>{user_id}</b>")

@frappe.whitelist()
def expense_claim_days():
    expense_days = frappe.get_doc("Employee App Settings")
    cl_days = []
    if expense_days.expense_claiming_days:
        for exp in expense_days.expense_claiming_days:
            if exp.day:
                cl_days.append(exp.day)
    return cl_days

def calculate_duration(last_ping):
    now = now_datetime()
    seconds_diff = time_diff_in_seconds(now, last_ping)

    seconds = seconds_diff
    minutes = seconds_diff // 60
    hours = seconds_diff // 3600
    days = seconds_diff // 86400
    weeks = days // 7
    months = days // 30
    years = days // 365

    if seconds < 60:
        return f"{int(seconds)} s"
    elif minutes < 60:
        return f"{int(minutes)} m"
    elif hours < 24:
        return f"{int(hours)} h"
    elif days < 7:
        return f"{int(days)} d"
    elif weeks < 4:
        return f"{int(weeks)} w"
    elif months < 12:
        return f"{int(months)} M"
    else:
        return f"{int(years)} y"
