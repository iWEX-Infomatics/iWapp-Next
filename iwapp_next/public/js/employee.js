frappe.ui.form.on("Employee", {
    refresh:function(frm){
        if(frm.doc.status == "Active" && frm.doc.user_id && frm.doc.custom_user_api_secret){
            frm.add_custom_button(__("Create App User"), function(){
                frappe.call({
                    method:"iwapp_next.iwapp_next.doctype.employee_app_settings.employee_app_settings.update_user_id_details",
                    args:{
                        "employee_id":frm.doc.name,
                        "api_secret":frm.doc.custom_user_api_secret,
                        "user_id":frm.doc.user_id,
                        "mac_id":frm.doc.attendance_device_id,
                        "last_pinged":frm.doc.custom_last_pinged_on
                    },
                    callback:function(r){
                    }
                })
            })
        }
    },
    first_name: function(frm) {
        let first_name = frm.doc.first_name;
        if (first_name && first_name === first_name.toUpperCase()) {
            frappe.msgprint(__("Avoid using all CAPITAL letters and instead use Title Case."));
        }
    },
    middle_name: function(frm) {
        let middle_name = frm.doc.middle_name;
        if (middle_name) {
            if (middle_name.length > 1 && middle_name === middle_name.toUpperCase()) {
                frappe.msgprint(__("Avoid using all CAPITAL letters and instead use Title Case."));
            }
        }
    },
    last_name: function(frm) {
        let last_name = frm.doc.last_name;
        if (last_name) {
            if (last_name.length > 2 && last_name === last_name.toUpperCase()) {
                frappe.msgprint(__("Avoid using all CAPITAL letters and instead use Title Case."));
            }
        }
    }
})