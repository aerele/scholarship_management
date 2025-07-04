# # Copyright (c) 2025, sakthi and contributors
# # For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ScholarshipSanction(Document):
	def on_submit(self):
		self.check_mandatory_fields()
		self.update_outstanding_status()

	def before_save(self):
		self.validate_scholarship_sanction()
				
	def validate_scholarship_sanction(self):
		existing_scholarship_sanction = frappe.get_list(
			"Scholarship Sanction", 
			filters={"student_record": self.student_record,"student_academic_record":self.student_academic_record, "docstatus": 1}, 
			fields=["name"])
		if existing_scholarship_sanction:
			frappe.throw(f"Scholarship Sanction already created for student record {existing_scholarship_sanction[0].name}")

	def update_outstanding_status(self):
		if (self.outstanding_amount == 0 and self.docstatus == 1):
			self.status = "Paid"
		elif (self.outstanding_amount > 0 and self.outstanding_amount < self.grand_total and self.docstatus == 1):
			self.status = "Partially Paid"
		elif (self.outstanding_amount == self.grand_total and self.docstatus == 1):
			self.status = "Not Paid"

	def check_mandatory_fields(self):
		missing_fields = []

		if not self.annual_house_hold_income:
			missing_fields.append("• Annual House Hold Income")
		if not self.affordability_of_educational_expenses:
			missing_fields.append("• Affordability Of Educational Expenses")
		if not self.grand_total:
			missing_fields.append("• Amount Sanctioned")
		if not self.target_percentage:
			missing_fields.append("• Target Percentage")
		if not self.mode_of_payment:
			missing_fields.append("• Mode Of Payment")
		if not self.annual_educational_expenses:
			missing_fields.append("• Annual Educational Expenses")
		if not self.expected_scholarship_amount:
			missing_fields.append("• Expected Scholarship Amount")

		if missing_fields:
			frappe.throw("The following fields are mandatory:<br>" + "<br>".join(missing_fields))


@frappe.whitelist()
def set_payment_entry(source_name, target_doc=None):
	from frappe.model.mapper import get_mapped_doc

	def post_process(source_doc, target_doc):
		target_doc.payment_type = "Pay"
		target_doc.mode_of_payment = source_doc.mode_of_payment
		target_doc.party_type = "Student"
		target_doc.party = source_doc.student_record
		target_doc.party_bank_account = source_doc.bank_account
		target_doc.party_name = source_doc.student_name
		target_doc.bank_account = None
		
	doclist = get_mapped_doc(
		"Scholarship Sanction",
		source_name,
		{
			"Scholarship Sanction": {
				"doctype": "Payment Entry",
				"validation": {"docstatus": ["=", 1]},
			}
		},
		target_doc,
		post_process,
	)

	return doclist