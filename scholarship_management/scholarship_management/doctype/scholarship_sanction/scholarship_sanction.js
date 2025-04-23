frappe.ui.form.on("Scholarship Sanction", {
	refresh(frm) {

		if (!frm.is_new() && frm.doc.docstatus === 1) {
			frm.add_custom_button(
				__("Create Payment Entry"),
				function () {
					frm.trigger("create_payment_entry");
				}, __("Create"))
		}

		// Filter applied in Student Academic Record field
		frm.set_query("student_academic_record", function () {
			if (frm.doc.student_record) {
				return {
					filters: {
						"name": frm.doc.student_record,
						"docstatus": 1
					}
				};
			} else {
				return {};
			}
		});

		frm.set_query('scheduled_entry', function () {
			return {
				filters: {
					"student_academic_record": frm.doc.student_academic_record,
					"student_record": frm.doc.student_record,
					"workflow_state": "Approved"
				}
			};

		});

		frm.set_query('bank_account', function () {
			return {
				filters: {
					"party": frm.doc.student_record
				}
			};

		});

	},
	create_payment_entry: function (frm) {
		frappe.model.open_mapped_doc({
			method: "scholarship_management.scholarship_management.doctype.scholarship_sanction.scholarship_sanction.set_payment_entry",
			frm: cur_frm,
		});
	},
	validate: function (frm) {
		// Update outstanding amount before saving
		if ((!frm.doc.outstanding_amount || frm.doc.outstanding_amount !== frm.doc.grand_total) && (frm.doc.docstatus !== 1)) {
			frm.set_value("outstanding_amount", frm.doc.grand_total);
		}
	},
	onload: function (frm) {
		if (frm.is_new()) {
			frm.set_value("outstanding_amount", frm.doc.grand_total);
		}
	},
});

frappe.listview_settings['Scholarship Sanction'] = {
	get_indicator: function (doc) {
		let status_map = {
			"Partially Paid": ["Partially Paid", "orange", "status,=,Partially Paid"],
			"Not Paid": ["Not Paid", "red", "status,=,Not Paid"],
			"Paid": ["Paid", "green", "status,=,Paid"],
		};
		return status_map[doc.status] || ["Unknown", "gray"];
	}
};