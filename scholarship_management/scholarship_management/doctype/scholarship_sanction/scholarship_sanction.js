frappe.ui.form.on("Scholarship Sanction", {
    refresh(frm) {
        frm.set_query("student_academic_record", function() { 
            if (frm.doc.student_record) {
                return {
                    filters: {
                        "student_id": frm.doc.student_record,
                        "docstatus": 1
                    }
                };
            } else {
                return {};
            }
        });
    }
});
