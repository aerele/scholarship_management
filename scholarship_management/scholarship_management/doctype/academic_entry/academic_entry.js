frappe.ui.form.on("Academic Entry", {
	refresh(frm) {
		if (!frm.is_new() && frm.doc.docstatus === 1) {
			frm.add_custom_button(
				__("Create Scheduled Entry"),
				function () {
					frm.trigger("create_schedule_entry");
				}, __("Create"))
		} 
	},

	create_schedule_entry: function (frm) {
		frappe.new_doc("Scheduled Entry", {
			student_academic_record: frm.doc.name,
			student_record: frm.doc.select_student
		})
	}
});
