# Copyright (c) 2025, sakthi and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	gender = ["Male", "Female", "Others"]
	return [
		{"label": "Maa Code", "fieldname": "maa_code", "fieldtype": "Data", "width": 120},
		{"label": "Student Name", "fieldname": "student_name", "fieldtype": "Data", "width": 200},
		{"label": "Gender", "fieldname": "gender", "fieldtype": "Select",
			"options": "\n".join(gender), 
			"width": 120},
		{"label": "Contact No", "fieldname": "mobile_no", "fieldtype": "Data", "width": 200},
		{"label": "District", "fieldname": "district", "fieldtype": "Data", "width": 120},
		{"label": "Town/Village", "fieldname": "town_village", "fieldtype": "Data", "width": 120},
		{"label": "Academic Year", "fieldname": "academic_year", "fieldtype": "Link","options": "Academic Year", "width": 120},
		{"label": "Course", "fieldname": "course", "fieldtype": "Link","options": "Course Master", "width": 120},
		{"label": "Year Studying", "fieldname": "year_studying", "fieldtype": "Link","options": "Year Studying", "width": 120},
		{"label": "Academic Entry", 
			"fieldname": "academic_entry",
			"fieldtype": "Link",
			"options": "Academic Entry",
			"width": 150},
		{"label": "Percentage", "fieldname": "percentage", "fieldtype": "Data", "width": 120},
	]

def get_data(filters):
	data = []

	academic_filters = {"docstatus": 1}

	if filters.get("maa_code"):
		academic_filters["maa_code"] = filters["maa_code"]

	if filters.get("student_name"):
		academic_filters["student_name"] = ["like", f"%{filters['student_name']}%"]

	if filters.get("academic_year"):
		academic_filters["present_academic_year"] = filters["academic_year"]


	if filters.get("course"):
		academic_filters["present_studyingcourse"] = filters["course"]

	if filters.get("year_studying"):
		academic_filters["present_yearstudying"] = filters["year_studying"]

	if filters.get("study_group"):
		academic_filters["present_studygroup"] = filters["study_group"]

	if filters.get("repeat") and filters["repeat"] not in ["Both", ""]:
		academic_filters["repeat"] = filters["repeat"]
		
	academic_entry = frappe.get_list(
		"Academic Entry",
		filters=academic_filters,
		fields=["name", "maa_code", "student_name", "present_academic_year", "present_studyingcourse", "present_yearstudying", "select_student","repeat","present_studygroup", "percentage_application_done"]
	)

	for academic in academic_entry:
		academic_doc = frappe.get_doc("Academic Entry", academic.name)
		student_doc = frappe.get_doc("Student", academic_doc.select_student)

		# Apply filters from Student Doctype
		if filters.get("gender") and filters["gender"] != student_doc.gender:
			continue

		if filters.get("category") and filters["category"] != student_doc.category:
			continue

		if filters.get("widow") and filters["widow"] not in ["Both", ""] and filters["widow"] != student_doc.widow_case:
			continue

		if filters.get("ganchi") and filters["ganchi"] not in ["Both", ""] and filters["ganchi"] != student_doc.ganchi:
			continue


		if filters.get("case") and filters["case"] != student_doc.case:
			continue

		address = frappe.get_list("Address",
			filters={
				"link_doctype": "Student",
				"link_name": student_doc.name
			},
			fields=["name", "mobile_no", "custom_district", "town_village","taluka"],
			limit=1
		)

		mobile_no = district = town_village = taluka = ""

		if address:
			mobile_no = address[0].mobile_no
			district = address[0].custom_district
			town_village = address[0].town_village
			taluka = address[0].taluka

		if filters.get("district") and filters["district"] != district:
			continue
		if filters.get("mobile_no") and filters["mobile_no"] != mobile_no:
			continue
		if filters.get("town_village") and filters["town_village"] != town_village:
			continue
		if filters.get("taluka") and filters["taluka"] != taluka:
			continue
		

		data.append({
			"maa_code": academic_doc.maa_code,
			"student_name": academic_doc.student_name,
			"gender": student_doc.gender,
			"mobile_no": mobile_no,
			"district": district,
			"town_village": town_village,
			"academic_year": academic_doc.present_academic_year,
			"course": academic_doc.present_studyingcourse,
			"year_studying": academic_doc.present_yearstudying,
			"academic_entry": academic_doc.name,
			"percentage": academic_doc.percentage_application_done,
		})

	return data


@frappe.whitelist()
def get_select_fields():
	maa_codes = frappe.get_all(
		"Student",
		filters={"maa_code": ["like", "MFVA%"]},
		fields=["maa_code", "student_name"],
		distinct=True
	)

	return {"maa_codes": maa_codes}