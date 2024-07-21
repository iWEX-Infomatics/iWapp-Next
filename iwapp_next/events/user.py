import frappe
from frappe import _


def before_save(doc, method):
    if doc.role_profile_name:
        designation = frappe.db.get_value("Employee", {"user_id":doc.name}, "designation")
        if designation:
            if doc.role_profile_name != designation:
                frappe.throw(_("The <b>Role Profile</b> you selected is not matching with the <b>Designation</b> of the Employee."))
            else:
                doc.module_profile = doc.role_profile_name
            if doc.module_profile:
                if doc.role_profile_name != doc.module_profile:
                    frappe.throw(_("User's <b>Role Profile</b> and <b>Module Profile</b> should be the same."))
    else:
        if doc.module_profile:
            doc.module_profile = ""

def on_update(doc, method):
    if doc.role_profile_name and doc.module_profile and not doc.api_key:
        frappe.msgprint(_("Press <b>'Generate Keys'</b> in <b>API Access</b> to enable Mobile access for the Employee and copy the value."))