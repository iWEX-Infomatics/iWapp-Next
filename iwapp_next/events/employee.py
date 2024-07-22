import frappe


def before_insert(doc, method):
    doc.custom_beneficiary_name = doc.employee_name

@frappe.whitelist()
def hourly_employee_app_schedular():
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
        emp_app = frappe.get_doc("Employee App Settings")
        if emp_app.employee_app_users:
            emp_app.employee_app_users = []
            for user in user_details:
                emp_app.append("employee_app_users", {
                    "employee_id": user.employee_id,
                    "employee_name":user.employee_id,
                    "user_api_key":user.user_key,
                    "user_api_secret":user.api_secret,
                    "user_id":user.user_id,
                    "last_mac_id":user.mac_id,
                    "last_pinged_on":user.last_pinged
                })
            emp_app.save()
            frappe.db.commit()  # Ensure changes are committed to the database