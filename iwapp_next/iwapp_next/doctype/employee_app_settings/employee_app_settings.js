// Copyright (c) 2024, Iwex Informatics and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee App Settings', {
	update_users: function(frm) {
		frm.clear_table("employee_app_users");
		frm.refresh_fields("employee_app_users")
		frappe.call({
			method:"iwapp_next.iwapp_next.doctype.employee_app_settings.employee_app_settings.get_user_id_details",
			args:{},
			callback:function(r){
				if(r.message){
					$.each(r.message, function(idx, emp){
					var child = frm.add_child("employee_app_users");
						child.employee_id = emp.employee_id
						child.employee_name = emp.employee_id
						child.user_id = emp.user_id
						child.user_api_key = emp.user_key
						child.user_api_secret = emp.api_secret
						frm.refresh_fields("employee_app_users");
					})
					frm.save()
					
				}
			}
		})
	}
});
