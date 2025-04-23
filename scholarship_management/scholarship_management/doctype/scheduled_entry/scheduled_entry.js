frappe.ui.form.on('Scheduled Entry', {
    refresh: function (frm) {
        frm.set_query('student_academic_record', function () {
            return {
                filters: {
                    docstatus: 1,
                }
            };

        });
        if (frm.doc.workflow_state == "Approved") {
            frm.add_custom_button(
                __("Create Scholarship Sanction"),
                function () {
                    frm.trigger("create_scholarship_sanction");
                }, __("Create"))
        }
    },

    create_scholarship_sanction: function (frm) {
        frm.call({
            doc: frm.doc,
            method: "create_scholarship_sanction",
        });
    }
})