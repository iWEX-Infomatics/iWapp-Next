# Copyright (c) 2024, Iwex Informatics and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EmployeeAppSettings(Document):
	pass
	def before_save(self):
		if self.employee_app_users:
			self.total_app_users = len(self.employee_app_users)

@frappe.whitelist()
def get_user_id_details():
	user_details = frappe.db.sql("""
			SELECT
				emp.name as employee_id,
				user.name as user_id,
				user.api_key as user_key,
				emp.custom_user_api_secret as api_secret
			FROM
				`tabEmployee` as emp LEFT JOIN
				`tabUser` as user ON emp.user_id = user.name
			WHERE
				emp.status = "Active" and user.api_key != ""
					   """, as_dict = True)
	if user_details:
		return user_details

@frappe.whitelist()
def update_user_id_details(employee_id, api_secret, user_id):
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
					emp.user_api_secret = api_secret
					employee_found = True
					break

		if not employee_found:
			emp_settings.append('employee_app_users', {
				'employee_name': employee_id,
				'employee_id': employee_id,
				'user_id': user_id,
				'user_api_key': user_api_key,
				'user_api_secret': api_secret
			})

		# Save the updated emp_settings document
		emp_settings.save()
		frappe.msgprint("Employee App Settings updated.")
	else:
		frappe.msgprint(f"Please generate a API ker for <b>{user_id}</b>")
