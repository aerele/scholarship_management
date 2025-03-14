// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
frappe.ui.form.on("Payment Entry", {
	onload: function (frm) {
		frm.set_query("reference_name", "references", function () {
			return {
				filters: {
					"student_record": frm.doc.party,
					"docstatus": 1
				}
			};
		});
		
		
		
		frm.set_query("reference_doctype", "references", function () {
				let doctypes = ["Journal Entry", "Scholarship Sanction"];
				if (frm.doc.party_type == "Customer") {
					doctypes = ["Sales Order", "Sales Invoice", "Journal Entry", "Dunning"];
				} else if (frm.doc.party_type == "Supplier") {
					doctypes = ["Purchase Order", "Purchase Invoice", "Journal Entry"];
				}
				return {
					filters: { name: ["in", doctypes] },
				};
			});
		},	
});