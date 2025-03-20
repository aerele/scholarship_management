import frappe
from frappe.model.document import Document

class AcademicEntry(Document):
	def before_save(self):
		self.validate_academic_entry()
		self.fetch_existing_maa_code()
		self.update_student_information()

	def on_submit(self):
		self.update_student_maa_code()
		self.update_new_student_maa_code()

	def generate_new_maa_code(self):
		"""Generate MAA code for new student"""
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

	def update_new_student_maa_code(self):
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

	def fetch_existing_maa_code(self):
		"""Fetch MAA code for an existing student"""
		existing_maa_code = frappe.get_value(
			"Academic Entry", 
			{"student_id": self.student_id, "docstatus": 1}, 
			"maa_code"
		)
		if existing_maa_code:
			self.db_set("maa_code", existing_maa_code)
			
	def update_student_maa_code(self):
		"""Update student MAA code: Keep existing, generate new only if missing"""
		if not self.maa_code:  # Generate a new maa_code only if missing
			self.maa_code = self.generate_new_maa_code()
			self.db_set("maa_code", self.maa_code)

	def update_student_information(self):
		scholarship = frappe.get_list(
			"Scholarship Sanction",
			filters={"maa_code": self.maa_code},
			fields=["grand_total","student_academic_record", "scholarship_sanctioned_date"],
			order_by="creation DESC",
			limit=1
		)

		if scholarship:
			latest_scholarship = scholarship[0]
			student_academic_records = frappe.get_list(
			"Academic Entry",
			filters={"name": latest_scholarship.get("student_academic_record")},
			fields=["percentage_application_done","present_studyingcourse"],
			order_by="creation DESC",
			limit=1
			)

			if student_academic_records:
				student_academic_record = student_academic_records[0]
				self.last_scholarship_date = latest_scholarship.get("scholarship_sanctioned_date")
				self.last_scholarship_amount = latest_scholarship.get("grand_total")
				self.last_studying_course = student_academic_record.get("present_studyingcourse")
				self.last_percentage = student_academic_record.get("percentage_application_done")

@frappe.whitelist()
def update_student_mark_for_existing_student(student_id):
	"""Update student marks for existing student"""
	existing_entry = frappe.get_value("Academic Entry", 
									  {"student_id": student_id, "docstatus": 1}, 
									  ["ssc_result", "hsc_result"])
	if existing_entry:
		ssc_result, hsc_result = existing_entry
		return {"ssc_result": ssc_result, "hsc_result": hsc_result}
	else:
		return {"ssc_result": None, "hsc_result": None}  
