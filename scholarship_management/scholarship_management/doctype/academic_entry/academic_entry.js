frappe.ui.form.on("Academic Entry", {
	refresh(frm) {
		if (!frm.is_new() && frm.doc.docstatus === 1) {
			frm.add_custom_button(
				__("Create Scheduled Entry"),
				function () {
					frm.trigger("create_schedule_entry");
				}, __("Create"))
		}
		if (frm.doc.student_id) {
			frm.trigger("student_id")
		}
	},

	student_id: function (frm) {
		if (frm.doc.student_id) {
			frm.trigger("update_student_mark_for_existing_student");
		}
	},

	update_student_mark_for_existing_student: function (frm) {
		frappe.call({
			method: "scholarship_management.scholarship_management.doctype.academic_entry.academic_entry.update_student_mark_for_existing_student",
			args: {
				student_id: frm.doc.student_id
			},
			callback: function (r) {
				if (r.message.ssc_result && r.message.hsc_result) {
					frm.set_value("ssc_result", r.message.ssc_result);
					frm.set_value("hsc_result", r.message.hsc_result);
				}
			}
		});
	},

	previous_studygroup: function (frm) {
		if (frm.doc.previous_studygroup) {
			frm.set_query("previous_studying_course", function () {
				return {
					filters: {
						"study_group": frm.doc.previous_studygroup
					}
				};
			});
		}
	},

	present_studygroup: function (frm) {
		if (frm.doc.present_studygroup) {
			frm.set_query("present_studyingcourse", function () {
				return {
					filters: {
						"study_group": frm.doc.present_studygroup
					}
				};
			});
		}
	},

	create_schedule_entry: function (frm) {
		frappe.new_doc("Scheduled Entry", {
			student_academic_record: frm.doc.name,
			student_record: frm.doc.student_id
		})
	}
});
