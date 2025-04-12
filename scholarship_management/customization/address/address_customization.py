from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from frappe.custom.doctype.custom_field.custom_field import create_custom_field
import frappe

def customize_address_doctype():
	make_property_setter(
		"Address",
		"city",
		"reqd",
		0,
		"Check"
	)

	make_property_setter(
		"Address",
		"city",
		"hidden",
		1,
		"Check"
	)

	make_property_setter(
		"Address",
		"state",
		"hidden",
		1,
		"Check" 
	)

	create_custom_field("Address", {
		"fieldname": "town_village",
		"label": "Town/Village",
		"fieldtype": "Link",
		"options": "Town Village",
		"insert_after": "city"
	})

	make_property_setter("Address", "town_village", "reqd", 1, "Check")

	create_custom_field("Address", {
		"fieldname": "custom_district",
		"label": "District",
		"fieldtype": "Data",
		"read_only": 1,
		"insert_after": "town_village",
		"fetch_from": "town_village.district"
	})

	make_property_setter("Address", "custom_district", "reqd", 1, "Check")

	create_custom_field("Address", {
		"fieldname": "mobile_no",
		"label": "Mobile No",
		"fieldtype": "Phone",
		"insert_after": "phone"
	})

	make_property_setter("Address", "mobile_no", "reqd", 1, "Check")

	state_options = "\n".join([
		"Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", 
		"Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", 
		"Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", 
		"Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", 
		"Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
	])

	create_custom_field("Address", {
		"fieldname": "custom_state",
		"label": "State",
		"fieldtype": "Select",
		"options": state_options,
		"insert_after": "custom_district"
	})
	
	make_property_setter("Address", "custom_state", "reqd", 1, "Check")

	create_custom_field("Address", {
		"fieldname": "taluka",
		"label": "Taluka",
		"fieldtype": "Data",
		"read_only": 1,
		"insert_after": "town_village",
		"fetch_from": "town_village.taluka"
	})

	make_property_setter("Address", "taluka", "reqd", 1, "Check")
	
	frappe.db.commit()

