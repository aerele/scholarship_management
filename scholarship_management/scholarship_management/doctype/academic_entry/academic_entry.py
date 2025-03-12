import frappe
from frappe.model.document import Document

class AcademicEntry(Document):
	def before_save(self):
		self.validate_academic_entry()

		existing_entry = frappe.get_value("Academic Entry",{"student_id": self.student_id, "docstatus":1},["maa_code", "ssc_result", "hsc_result"])
		if existing_entry:
			existing_maa_code, ssc_marks, hsc_marks = existing_entry
			self.maa_code = existing_maa_code
			self.ssc_result = ssc_marks  
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


	def validate_academic_entry(self):
		"""Validate duplicate academic entry"""
		academic_entry = frappe.get_list(
			"Academic Entry",
			filters={
				"student_id": self.student_id,
				"previous_studygroup": self.previous_studygroup,
				"previous_academic_year": self.previous_academic_year,
				"previous_yearstudying": self.previous_yearstudying,
				"present_academic_year": self.present_academic_year,
				"present_yearstudying": self.present_yearstudying,
				"stream": self.stream,
				"present_studyingcourse": self.present_studyingcourse,
				"present_studygroup": self.present_studygroup,
				"previous_studying_course": self.previous_studying_course,
				"docstatus": 1
			},
			fields=["name"]
		)

		if academic_entry:
			frappe.throw(f"Academic Entry already exists for this student {academic_entry[0].name}")
