# Copyright (c) 2025, sakthi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	get_link_to_form
)

class ScheduledEntry(Document):
	def on_submit(self):
		self.validate_create_scholarship_sanction()
		self.validate_sanction_status()

	def validate_sanction_status(self):
		if self.status not in ["Accept","Reject"]:
			frappe.throw("Status should be either Accept or Reject")
			
	def create_scholarship_sanction(self):
		if self.status == "Accept":
			doc = frappe.new_doc("Scholarship Sanction")
			doc.student_record = self.student_record
			doc.academic_record = self.academic_record
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