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
		self.validate_create_scholarship_sanction()
			
	def create_scholarship_sanction(self):
		if self.workflow_state == "Approved":
			doc = frappe.new_doc("Scholarship Sanction")
			doc.student_record = self.student_record
			doc.student_academic_record = self.student_academic_record
			doc.status = 'Not Paid'
			doc.scheduled_entry = self.name
			doc.insert()
			frappe.msgprint("Scholarship Sanction created successfully for student record {}".format(get_link_to_form("Scholarship Sanction", doc.name)))

	def validate_create_scholarship_sanction(self):
		existing_scholarship_sanction = frappe.get_list(
			"Scholarship Sanction", 
			filters={"student_record": self.student_record,"student_academic_record":self.student_academic_record, "docstatus": 1}, 
			fields=["name"])
		if existing_scholarship_sanction:
			frappe.throw(f"Scholarship Sanction already created for student record {existing_scholarship_sanction[0].name}")
		else:
			self.create_scholarship_sanction()
	
	def check_mandatory_fields(self):
		if not self.number_of_call_times:
			frappe.throw("Number of call times is mandatory.")
		if not self.remarks:
			frappe.throw("Remarks is mandatory.")
		if not self.call_date:
			frappe.throw("Call Date is mandatory.")
		if not self.call_time:
			frappe.throw("Call Time is mandatory.")