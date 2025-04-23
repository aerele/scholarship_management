# Copyright (c) 2025, sakthi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	get_link_to_form
)

class ScheduledEntry(Document):
	def on_submit(self):
		self.check_mandatory_fields()
		self.validate_existing_scholarship_sanction()
	
	@frappe.whitelist()
	def create_scholarship_sanction(self):
		existing_scholarship_sanction = self.check_existing_scholarship_sanction()
		if self.workflow_state == "Approved":
			doc = frappe.new_doc("Scholarship Sanction")
			doc.student_record = self.student_record
			doc.student_academic_record = self.student_academic_record
			doc.status = 'Not Paid'
			doc.scheduled_entry = self.name
			doc.insert(ignore_mandatory=True)
			frappe.msgprint("Scholarship Sanction created successfully for student record {}".format(get_link_to_form("Scholarship Sanction", doc.name)))

	def validate_existing_scholarship_sanction(self):
		existing_scholarship_sanction = self.check_existing_scholarship_sanction()
		if not existing_scholarship_sanction:
			self.create_scholarship_sanction()

	def check_existing_scholarship_sanction(self):
		existing_scholarship_sanction = frappe.get_list(
				"Scholarship Sanction", 
				filters={
					"student_record": self.student_record,
					"student_academic_record": self.student_academic_record,
					"docstatus": ["in", [0, 1]]
				}, 
				fields=["name"],
				limit=1
			)
		if existing_scholarship_sanction:
			frappe.throw(f"Scholarship Sanction already created for student record {existing_scholarship_sanction[0].name}")

	def check_mandatory_fields(self):
		missing_fields = []
		if not self.number_of_call_times:
			missing_fields.append("• Number of call times is mandatory.")
		if not self.remarks:
			missing_fields.append("• Remarks is mandatory.")
		if not self.call_date:
			missing_fields.append("• Call Date is mandatory.")
		if not self.call_time:
			missing_fields.append("• Call Time is mandatory.")
		if missing_fields:
			frappe.throw("The following fields are mandatory:<br>" + "<br>".join(missing_fields))