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
		if not self.annual_house_hold_income:
			frappe.throw("Annual House Hold Income is mandatory.")
		if not self.affordability_of_educational_expenses:
			frappe.throw("Affordability Of Educational Expenses is mandatory.")
		if not self.grand_total:
			frappe.throw("Amount Sanctioned is mandatory.")
		if not self.target_percentage:
			frappe.throw("Target Percentage is mandatory.")
		if not self.grand_total:
			frappe.throw("Amount Sanctioned is mandatory.")
		if not self.mode_of_payment:
			frappe.throw("Mode Of Payment is mandatory.")
		if not self.company:
			frappe.throw("Company is mandatory.")
		if not self.bank_account:
			frappe.throw("Bank Account is mandatory.")
		if not self.trust:
			frappe.throw("Trust is mandatory.")
		if not self.scholarship_sanctioned_date:
			frappe.throw("Scholarship Sanctioned Date is mandatory.")
		if not self.annual_educational_expenses:
			frappe.throw("Annual Educational Expenses is mandatory.")
		if not self.expected_scholarship_amount:
			frappe.throw("Expected Scholarship Amount is mandatory.")