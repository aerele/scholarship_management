import frappe

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	gender = ["Male", "Female", "Others"]
	widow_case = ["", "Yes", "No"]
	return [
		{"label": "Maa Code", "fieldname": "maa_code", "fieldtype": "Data", "width": 120},
		{"label": "Student Name", "fieldname": "student_name", "fieldtype": "Data", "width": 200},
		{"label": "Gender", "fieldname": "gender", "fieldtype": "Select",
			"options": "\n".join(gender), 
			"width": 120},
		{"label": "Widow Case", "fieldname": "widow", "fieldtype": "Select",
			"options": "\n".join(widow_case), 
			"width": 120},
		{"label": "District", "fieldname": "district", "fieldtype": "Data", "width": 120},
		{"label": "Taluka", "fieldname": "taluka", "fieldtype": "Data", "width": 120},
		{"label": "Town/Village", "fieldname": "town_village", "fieldtype": "Data", "width": 120},
		{"label": "Academic Year", "fieldname": "academic_year", "fieldtype": "Link","options": "Academic Year", "width": 120},
		{"label": "Sanctioned Amount", "fieldname": "sanctioned_amount", "fieldtype": "Float", "width": 120},
		{"label": "Trust", "fieldname": "trust", "fieldtype": "Link","options": "Trust", "width": 120},
		{"label": "Percentage", "fieldname": "percentage", "fieldtype": "Data", "width": 120},
		{"label": "Course", "fieldname": "course", "fieldtype": "Link","options": "Course Master", "width": 120},
		{"label": "Year Studying", "fieldname": "year_studying", "fieldtype": "Link","options": "Year Studying", "width": 120},
		{"label": "Scholarship Sanction",
			"fieldname": "scholarship_sanction",
			"fieldtype": "Link",
			"options": "Scholarship Sanction",
			"width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
	]

def get_data(filters):
    data = []

    scholarship_sanctions = frappe.get_all(
        "Scholarship Sanction",
        filters={"docstatus": 1},
        fields=["name", "student_academic_record", "grand_total", "trust", "status"]
    )

    for sanction in scholarship_sanctions:
        if filters.get("status") and filters["status"] != sanction.status:
            continue
        academic_doc = frappe.get_doc("Academic Entry", sanction.student_academic_record)

        # Academic filters
        if filters.get("maa_code") and filters["maa_code"] != academic_doc.maa_code:
            continue
        if filters.get("student_name") and filters["student_name"].lower() not in academic_doc.student_name.lower():
            continue
        if filters.get("academic_year") and filters["academic_year"] != academic_doc.present_academic_year:
            continue
        if filters.get("course") and filters["course"] != academic_doc.present_studyingcourse:
            continue
        if filters.get("year_studying") and filters["year_studying"] != academic_doc.present_yearstudying:
            continue
        if filters.get("study_group") and filters["study_group"] != academic_doc.present_studygroup:
            continue
        if filters.get("repeat") and filters["repeat"] not in ["Both", ""] and filters["repeat"] != academic_doc.repeat:
            continue

        # Student filters
        student_doc = frappe.get_doc("Student", academic_doc.student_id)

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

        # Address filters
        address = frappe.get_list(
            "Address",
            filters={"link_doctype": "Student", "link_name": student_doc.name},
            fields=["mobile_no", "custom_district", "town_village", "taluka"],
            limit=1
        )

        mobile_no = district = town_village = taluka = ""
        if address:
            addr = address[0]
            mobile_no = addr.mobile_no
            district = addr.custom_district
            town_village = addr.town_village
            taluka = addr.taluka

        if filters.get("district") and filters["district"] != district:
            continue
        if filters.get("mobile_no") and filters["mobile_no"] != mobile_no:
            continue
        if filters.get("town_village") and filters["town_village"] != town_village:
            continue
        if filters.get("taluka") and filters["taluka"] != taluka:
            continue

        if filters.get("trust") and filters["trust"] != sanction.trust:
            continue
        if filters.get("sanctioned_amount") and filters["sanctioned_amount"] != sanction.grand_total:
            continue

        data.append({
            "maa_code": academic_doc.maa_code,
            "student_name": academic_doc.student_name,
            "gender": student_doc.gender,
            "widow": student_doc.widow_case,
            "district": district,
            "taluka": taluka,
            "town_village": town_village,
            "academic_year": academic_doc.present_academic_year,
            "sanctioned_amount": sanction.grand_total,
            "trust": sanction.trust,
            "percentage": academic_doc.percentage_application_done,
            "course": academic_doc.present_studyingcourse,
            "year_studying": academic_doc.present_yearstudying,
            "scholarship_sanction": sanction.name,
            "status": sanction.status
        })

    return data
