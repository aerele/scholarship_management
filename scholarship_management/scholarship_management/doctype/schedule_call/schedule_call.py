import frappe
from frappe.query_builder import DocType
from frappe.model.document import Document

class ScheduleCall(Document):
	@frappe.whitelist()
	def search_records(self, **kwargs):
		fields = frappe._dict(kwargs)
		
		student_name_filter = fields.get("name1")
		maa_code = fields.get("maa_code")
		present_academic_year = fields.get("present_academic_year")
		from_date = fields.get("from")
		to_date = fields.get("to")
		interview_place = fields.get("interview_place")
		stream = fields.get("stream")
		study_group = fields.get("study_group")
		course = fields.get("course")
		acceptreject = fields.get("acceptreject")
		widow = fields.get("widow")
		type_of_postage = fields.get("type_of_postage")
		repeat = fields.get("repeat")
		
		academic_entry = DocType("Academic Entry")
		student = DocType("Student")
		
		query = (
			frappe.qb.from_(academic_entry)
			.join(student)
			.on(academic_entry.name == student.name)
			.select(
				academic_entry.maa_code,
				student.student_name,
				# academic_entry.rejected,  
				student.name,
				academic_entry.name,
			)
		)

		query = query.where(academic_entry.docstatus == 1)
		if student_name_filter:
			query = query.where(student.name == student_name_filter)
		if interview_place:
			query = query.where(student.interview_place == interview_place)
		if widow:
			query = query.where(student.widow_case == widow)
		
		if maa_code:
			query = query.where(academic_entry.maa_code == maa_code)
		if present_academic_year:
			query = query.where(academic_entry.present_academic_year == present_academic_year)
		if study_group:
			query = query.where(academic_entry.present_studygroup == study_group)
		if stream:
			query = query.where(academic_entry.stream == stream)
		if course:
			query = query.where(academic_entry.present_studyingcourse == course)
		# if acceptreject:
		# 	query = query.where(academic_entry.accept == acceptreject)
		if type_of_postage:
			query = query.where(academic_entry.type_of_postage == type_of_postage)
		if repeat:
			query = query.where(academic_entry.repeat == repeat)

		if from_date and to_date:
			query = query.where(academic_entry.application_receive_date.between(from_date, to_date))
		elif from_date:
			query = query.where(academic_entry.application_receive_date >= from_date)
		elif to_date:
			query = query.where(academic_entry.application_receive_date <= to_date)

		
		results = query.run(as_dict=True)
		self.set("record", [])
		for row in results:
			child_row = self.append("record", {})
			child_row.maa_code = row.get("maa_code")
			child_row.name1 = row.get("student_name")
			child_row.rejected = "No" if row.get("accept") == "Yes" else "Yes"
			child_row.call_letter = row.get("call_letter", "")
			child_row.call_date = row.get("call_date", "")
			child_row.call_time = row.get("call_time", "")
			child_row.academic_record = row.get("name", "")

			name = row.get("name")
			address_dict = get_student_address(name)
			child_row.address = address_dict.get("address", "")
			child_row.phone_no = address_dict.get("phone", "")
		
		self.save()
	
		return results
		
	@frappe.whitelist()
	def schedule_selected_entry(self, maa_codes, call_date, call_time):
		if not isinstance(maa_codes, list):
			frappe.throw("Invalid data format. Expected a list of maa_codes.")

		for maa_code in maa_codes:
			latest_academic_entry = frappe.get_list(
				"Academic Entry",
				filters={"maa_code": maa_code, "docstatus": ["in", [0, 1]]},
				fields=["name", "creation"],
				order_by="creation DESC", 
				limit=1
			)
			if not latest_academic_entry:
				frappe.throw(f"No academic entry found for {maa_code}.")

			scheduled_entry = frappe.get_doc({
				"doctype": "Scheduled Entry",
				"student_academic_record": latest_academic_entry[0].get('name'),
				"call_date": call_date,
				"call_time": call_time,
			})
			scheduled_entry.insert() 
		return scheduled_entry.name
	
def get_student_address(name):
	address_list = frappe.get_all("Address", ["name"])
	for address in address_list:
		address_doc = frappe.get_doc("Address", address.name)
		for link in address_doc.links:
			if link.link_doctype == "Student" and link.link_name == name:
				return {
					"address": address_doc.address_line1,
					"city": address_doc.city,
					"phone": address_doc.phone or address_doc.mobile_no,
				}

	return {}  
