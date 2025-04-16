import frappe
from frappe.utils import getdate

def execute(filters=None):
	filters = frappe._dict(filters or {})

	# Extract date filters safely
	from_date = getdate(filters.from_date) if filters.from_date else None
	to_date = getdate(filters.to_date) if filters.to_date else None
	category = filters.category if filters.category else None
	maa_code = filters.maa_code if filters.maa_code else None
	mode_of_payment = filters.mode_of_payment if filters.mode_of_payment else None

	# Define report columns
	columns = get_report_columns()

	# Fetch filtered data
	data = get_filtered_payment_data(from_date, to_date, category, maa_code, mode_of_payment)

	return columns, data

def get_report_columns():
	category = [
		"General Category",
		"OBC",
		"SC",
		"ST",
		"EWS",
		"Muslim",
		"Non-Muslim",
		"Christian",
		"Hindu",
		"Sikh",
		"Buddhist",
		"Jain",
		"Parsi",
		"Jewish",
		"Others"
	]
	
	return [
		{"label": "MAA Code", "fieldname": "maa_code", "fieldtype": "Data", "width": 120},
		{"label": "Student Name", "fieldname": "student_name", "fieldtype": "Data", "width": 200},
		{"label": "Amount", "fieldname": "allocated_amount", "fieldtype": "Currency", "width": 100},
		{"label": "Posting Date", "fieldname": "posting_date", "fieldtype": "Date", "width": 120},
		{"label": "Town/Village", "fieldname": "town_village", "fieldtype": "Data", "width": 120},
		{"label": "Category", "fieldname": "category", "fieldtype": "Select", "options": "\n".join(category), "width": 120},
		{"label": "Scholarship Sanction", "fieldname": "scholarship_sanction", "fieldtype": "Link", "options": "Scholarship Sanction", "width": 150},
		{"label": "Payment Entry", "fieldname": "payment_entry", "fieldtype": "Link", "options": "Payment Entry", "width": 250},
	]


def get_filtered_payment_data(from_date, to_date, category, maa_code, mode_of_payment):
	data = []

	# Get all Payment Entry references linked to Scholarship Sanction
	payment_refs = frappe.get_list(
		"Payment Entry",
		filters={"party_type": "Student", "docstatus":1},
		fields=["name"]
	)

	for ref in payment_refs:
		payment_entry = frappe.get_doc("Payment Entry", ref.name)
		student = frappe.get_doc("Student", payment_entry.party)
		
		address = frappe.get_list("Address",
						filters={
							"link_doctype": "Student",
							"link_name": student.name
						},
						fields=["name", "town_village"],
						limit=1
					)

		# Apply date filters
		if from_date and payment_entry.posting_date < from_date:
			continue
		if to_date and payment_entry.posting_date > to_date:
			continue
		
		# For Category
		if category and student.category != category:
			continue
		if maa_code and student.maa_code != maa_code:
			continue
		if mode_of_payment and payment_entry.mode_of_payment != mode_of_payment:
			continue

		scholarship_sanction = payment_entry.references[0].reference_name if payment_entry.references else None

		
		data.append({
			"maa_code": student.maa_code,
			"student_name": student.student_name,
			"allocated_amount": payment_entry.paid_amount,
			"posting_date": payment_entry.posting_date,
			"scholarship_sanction": scholarship_sanction,
			"payment_entry": payment_entry.name,
			"category": student.category,
			"town_village": address[0].town_village,
			"mode_of_payment": payment_entry.mode_of_payment,
		})

	return data


@frappe.whitelist() 
def get_maa_codes():
    maa_codes = frappe.get_all(
        "Student",
        filters={"maa_code": ["like", "MFVA%"]},
        fields=["maa_code", "name"],
        distinct=True
    )
    return {"maa_codes": maa_codes}
