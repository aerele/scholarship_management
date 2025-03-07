import frappe
from frappe.model.document import Document

class AcademicEntry(Document):
	def validate(self):
		print('validate')
		existing_entry = frappe.get_value("Academic Entry",{"student_id": self.student_id, "docstatus":1},["maa_code", "ssc_result", "hsc_result"])
		print("existing entry", existing_entry)
		if existing_entry:
			existing_maa_code, ssc_marks, hsc_marks = existing_entry
			self.maa_code = existing_maa_code
			if not self.ssc_result and ssc_marks is not None:
				self.ssc_result = ssc_marks  
			if not self.hsc_result and hsc_marks is not None:
				self.hsc_result = hsc_marks  

	def on_submit(self):
		existing_maa_code = frappe.get_value("Academic Entry",{"student_id": self.student_id},"maa_code")
		if existing_maa_code:
			self.maa_code = existing_maa_code
		else:
			self.maa_code = self.generate_new_maa_code()
			self.db_set("maa_code", self.maa_code) 

		self.update_student_maa_code()

	def generate_new_maa_code(self):
		"""Generate maa code for new student"""
		last_code = frappe.db.get_value(
			"Academic Entry",
			filters={
				"maa_code": ["like", "MFVA%"],
				"docstatus": ["in", [0, 1]]
			},
			fieldname="maa_code",
			order_by="creation desc"
		)

		if last_code and last_code.startswith("MFVA"):
			last_number = int(last_code[4:])  
		else:
			last_number = 0  

		new_number = last_number + 1
		return f"MFVA{new_number:05d}"

	def update_student_maa_code(self):
		"""Update student maa code only new student"""
		student_name = frappe.db.get_value("Student", {"student_id": self.student_id})
		if student_name:
			frappe.db.set_value("Student", {"student_id": self.student_id}, "maa_code", self.maa_code)
