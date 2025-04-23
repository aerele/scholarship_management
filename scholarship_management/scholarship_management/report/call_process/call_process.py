import frappe

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns()
	data = get_data(filters)

	return columns, data

def get_columns():
	return [
		{"label": "Maa Code", "fieldname": "maa_code", "fieldtype": "Data", "width": 120},
		{"label": "Student Name", "fieldname": "student_name", "fieldtype": "Data", "width": 200},
		{"label": "District", "fieldname": "district", "fieldtype": "Data", "width": 120},
		{"label": "Taluka", "fieldname": "taluka", "fieldtype": "Data", "width": 120},
		{"label": "Town/Village", "fieldname": "town_village", "fieldtype": "Data", "width": 120},
		{"label": "Mobile No", "fieldname": "mobile_no", "fieldtype": "Data", "width": 200},
		{"label": "Phone No", "fieldname": "phone_no", "fieldtype": "Data", "width": 200},
		{"label": "Call Time", "fieldname": "call_time", "fieldtype": "Time", "width": 120},
		{"label": "Call Date", "fieldname": "call_date", "fieldtype": "Date", "width": 120},
		{"label": "Remarks", "fieldname": "remarks", "fieldtype": "Data", "width": 120},
		{"label": "Scheduled Entry", "fieldname": "scheduled_entry", "fieldtype": "Link", "options": "Scheduled Entry", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
	]
def get_data(filters):
    data = []
    scheduled_filters = {
        "docstatus": ["in", [0, 1]]
    }

    if filters.get("status"):
        scheduled_filters["workflow_state"] = filters["status"]

    scheduled_entries = frappe.get_list(
        "Scheduled Entry",
        filters=scheduled_filters,
        fields=["*"]
    )
    
    for entry in scheduled_entries:
        # Get Academic Entry
        if not entry.get("student_academic_record"):
            continue

        academic_doc = frappe.get_doc("Academic Entry", entry.student_academic_record)

        # Academic filters
        if filters.get("maa_code") and filters["maa_code"] != academic_doc.maa_code:
            continue
        if filters.get("student_name") and filters["student_name"] != academic_doc.student_name:
            continue
        if filters.get("academic_year") and filters["academic_year"] != academic_doc.present_academic_year:
            continue
        if filters.get("course") and filters["course"] != academic_doc.present_studyingcourse:
            continue
        if filters.get("year_studying") and filters["year_studying"] != academic_doc.present_yearstudying:
            continue
        if filters.get("study_group") and filters["study_group"] != academic_doc.present_studygroup:
            continue
        if filters.get("school_college") and filters["school_college"] != academic_doc.schoolcollege:
            continue
        if filters.get("repeat") and filters["repeat"] not in ["Both", ""] and filters["repeat"] != academic_doc.repeat:
            continue

        # Get Student Doc
        student_doc = frappe.get_doc("Student", academic_doc.student_id)

        # Student filters
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

        # Address info
        address = frappe.get_list(
            "Address",
            filters={"link_doctype": "Student", "link_name": student_doc.name},
            fields=["mobile_no", "custom_district", "town_village", "taluka", "phone"],
            limit=1
        )

        mobile_no = district = town_village = taluka = phone_no = ""
        if address:
            addr = address[0]
            mobile_no = addr.mobile_no
            phone_no = addr.phone
            district = addr.custom_district
            town_village = addr.town_village
            taluka = addr.taluka

        # Address filters
        if filters.get("district") and filters["district"] != district:
            continue
        if filters.get("mobile_no") and filters["mobile_no"] != mobile_no:
            continue
        if filters.get("town_village") and filters["town_village"] != town_village:
            continue
        if filters.get("taluka") and filters["taluka"] != taluka:
            continue

        # Append record
        data.append({
            "maa_code": academic_doc.maa_code,
            "student_name": academic_doc.student_name,
            "district": district,
            "taluka": taluka,
            "town_village": town_village,
            "mobile_no": mobile_no,
            "phone_no": phone_no,
            "call_time": entry.call_time,
            "call_date": entry.call_date,
            "remarks": entry.remarks,
            "scheduled_entry": entry.name,
            "status": entry.workflow_state
        })

    return data
