frappe.ui.form.on("User", {
    refresh: function (frm) {
        if (frm.doc.api_key) {
            frm.add_custom_button("Employee", function () {
                frappe.db.get_value('Employee', { user_id: frm.doc.name }, 'name')
                    .then(r => {
                        let values = r.message;
                        if (values.name) {
                            frappe.set_route('Form', 'Employee', values.name)
                        }
                    })
            })
        }
    }
})