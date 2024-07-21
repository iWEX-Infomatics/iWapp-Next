frappe.listview_settings['Expense Claim'] = {
    refresh: function (frm) {
        // Check if the user does not have HR Manager and does not have System Manager roles
        if (!frappe.user.has_role('HR Manager') && !frappe.user.has_role('System Manager')) {
            // Get the current date
            const now = new Date();
            // Get the day of the week (0 = Sunday, 1 = Monday, ..., 6 = Saturday)
            const dayOfWeek = now.getDay();
            // Convert the day number to the name of the day
            const daysOfWeek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
            const dayName = daysOfWeek[dayOfWeek];
            frappe.call({
                method: "iwapp_next.iwapp_next.doctype.employee_app_settings.employee_app_settings.expense_claim_days",
                args: {},
                callback: function (r) {
                    // Flag to track if claiming is allowed today
                    let canClaim = false;

                    // Check if claiming is allowed today
                    $.each(r.message, function (idx, day) {
                        if (day === "All" || day === dayName) {
                            canClaim = true;
                            return false; // Exit the loop as we found a matching day
                        }
                    });
                    // hide the Buttom
                    if (!canClaim) {
                        frm.page.set_primary_action(__("Add Expense Claim"), function() {
                        }).addClass('hidden');
                    }
                }
            });
        }
    }
};
