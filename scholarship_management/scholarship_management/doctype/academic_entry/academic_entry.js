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

	select_student: function(frm) {
		if (frm.doc.select_student) {
			frm.trigger("update_student_mark_for_existing_student");
		}
	},
	
	update_student_mark_for_existing_student: function(frm){
		frappe.call({
			method: "scholarship_management.scholarship_management.doctype.academic_entry.academic_entry.update_student_mark_for_existing_student",
			args:{
				student_id: frm.doc.select_student
			},
			callback: function(r){
				if (r.message){
					frm.set_value("ssc_result", r.message.ssc_result);
					frm.set_value("hsc_result", r.message.hsc_result);
				}
			}
		});
	},

	create_schedule_entry: function (frm) {
		frappe.new_doc("Scheduled Entry", {
			student_academic_record: frm.doc.name,
			student_record: frm.doc.select_student
		})
	}
});
