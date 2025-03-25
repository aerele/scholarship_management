import frappe
from frappe.permissions import add_permission, update_permission_property

def after_install():
	frappe.get_attr("scholarship_management.scholarship_management.doctype.student.student.party_setup")()
	frappe.get_attr("scholarship_management.customization.address.address_customization.customize_address_doctype")()
	setup_scholarship_roles()
	create_workflow()

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


def create_workflow():
    states = [
        "Pending",
        "Approved",
        "Rejected"
    ]

    # Create workflow states if they don't exist
    for state in states:
        if not frappe.db.exists("Workflow State", state):
            workflow_state = frappe.get_doc(
                {
                    "doctype": "Workflow State",
                    "workflow_state_name": state,
                    "style": "Success"
                    if state == "Transaction Completed"
                    else "Danger",
                }
            )
            workflow_state.insert()

    # Create workflow if it doesn't exist
    if not frappe.db.exists("Workflow", "Scheduled Entry Workflow"):
        workflow = frappe.get_doc(
            {
                "doctype": "Workflow",
                "workflow_name": "Scheduled Entry Workflow",
                "document_type": "Scheduled Entry",
                "is_active": 1,
                "send_email_alert": 0,
                "states": [
                    {
                        "state": "Pending",
                        "allow_edit": "Scholarship User",
                        "doc_status": 0,
                    },
                    {
                        "state": "Approved",
                        "allow_edit": "Scholarship Manager",
                        "doc_status": 1,
                    },
                    {
                        "state": "Rejected",
                        "allow_edit": "Scholarship Manager",
                        "doc_status": 1,
                    },
                ],
                "transitions": [
                    {
                        "state": "Pending",
                        "action": "Reject",
                        "next_state": "Rejected",
                        "allowed": "Scholarship Manager",
                        "allow_self_approval": 1,
                    },
                    {
                        "state": "Pending",
                        "action": "Approve",
                        "next_state": "Approved",
                        "allowed": "Scholarship Manager",
                        "allow_self_approval": 1,
                    },
                ],
            }
        )
        workflow.insert()
        frappe.db.commit()
