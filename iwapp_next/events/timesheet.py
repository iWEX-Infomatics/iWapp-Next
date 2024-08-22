import frappe

def after_insert(doc, method):
    fetch_timesheet_list(doc)

def after_delete(doc, method):
   fetch_timesheet_list(doc)

def fetch_timesheet_list(doc):
    timesheet_list = []
    for time in doc.time_logs:
        if time.task:
            timesheet_details = frappe.db.get_list(
                "Timesheet Detail",
                filters={"task": time.task},
                fields=["parent"],
                ignore_permissions=True
            )
            timesheet_list.extend(timesheet_details)
            
            parent_list = [timesheet.get('parent') for timesheet in timesheet_list]
            if parent_list:
                parent_str = ", ".join(parent_list)
                frappe.db.set_value("Task", time.task, "custom_linked_timesheets", parent_str)


