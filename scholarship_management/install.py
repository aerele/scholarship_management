import frappe
from frappe.permissions import add_permission, update_permission_property

def after_install():
	frappe.get_attr("scholarship_management.scholarship_management.doctype.student.student.party_setup")()
	frappe.get_attr("scholarship_management.customization.address.address_customization.customize_address_doctype")()
	setup_scholarship_roles()

def setup_scholarship_roles():
	roles = ["Scholarship Manager", "Scholarship User"]

	for role in roles:
		if not frappe.db.exists("Role", role):
			frappe.get_doc({
				"doctype": "Role",
				"role_name": role,
				"desk_access": 1
			}).insert()
	
	# Define permissions for each role
	role_permissions = {
		"Scholarship Manager": [
			{"doctype": "Student", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "Schedule Call", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "Scholarship Sanction", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "Scheduled Entry", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "Academic Entry", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "Trust", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "Year Studying", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "Course Master", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "Grade Percentage", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "Town Village", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "Taluka", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "District", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "Reason for Rejection", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "Study Group", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "Stream", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "Type of Postage Master", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "School College", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "Present Medium", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
			{"doctype": "Academic Year", "permissions": {"read": 1, "write": 1, "create": 1, "delete": 1, "export": 1}},
		],
		"Scholarship User": [
			{"doctype": "Student", "permissions": {"read": 1, "create": 1, "write": 0, "delete": 0}},
			{"doctype": "Schedule Call", "permissions": {"read": 1, "write": 0, "create": 0, "delete": 0}},
			{"doctype": "Scholarship Sanction", "permissions": {"read": 1, "write": 0, "create": 0, "delete": 0}},
			{"doctype": "Scheduled Entry", "permissions": {"read": 1, "write": 0, "create": 0, "delete": 0}},
			{"doctype": "Academic Entry", "permissions": {"read": 1, "write": 0, "create": 0, "delete": 0}},
		],
	}
	
	# Apply permissions
	for role, doctypes in role_permissions.items():
		for item in doctypes:
			add_and_update_permissions(item["doctype"], role, item["permissions"])

def add_and_update_permissions(doctype, role, permissions):
	"""Adds and updates permissions for a given role on a specific DocType"""
	if not frappe.db.exists("Custom DocPerm", {"role": role, "parent": doctype}):
		add_permission(doctype, role)

	for perm_type, value in permissions.items():
		update_permission_property(
			doctype=doctype,
			role=role,
			permlevel=0,
			ptype=perm_type,
			value=value
		)
