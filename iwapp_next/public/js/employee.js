frappe.ui.form.on("Employee", {
    refresh:function(frm){
        if(frm.doc.status == "Active" && frm.doc.user_id && frm.doc.custom_user_api_secret){
            frm.add_custom_button(__("Create App User"), function(){
                console.log("kkkkk", frm.doc.name)
                frappe.call({
                    method:"iwapp_next.iwapp_next.doctype.employee_app_settings.employee_app_settings.update_user_id_details",
                    args:{
                        "employee_id":frm.doc.name,
                        "api_secret":frm.doc.custom_user_api_secret,
                        "user_id":frm.doc.user_id
                    },
                    callback:function(r){
                        // console.log(r.message)
                    }
                })
            })
        }
    }
})