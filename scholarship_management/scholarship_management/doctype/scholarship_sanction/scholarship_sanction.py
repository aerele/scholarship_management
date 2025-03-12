# # Copyright (c) 2025, sakthi and contributors
# # For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ScholarshipSanction(Document):
	def before_save(self):
		self.validate_scholarship_sanction()
				
	def validate_scholarship_sanction(self):
		existing_scholarship_sanction = frappe.get_list(
			"Scholarship Sanction", 
			filters={"student_record": self.student_record,"student_academic_record":self.student_academic_record, "docstatus": 1}, 
			fields=["name"])
		if existing_scholarship_sanction:
			frappe.throw(f"Scholarship Sanction already created for student record {existing_scholarship_sanction[0].name}")