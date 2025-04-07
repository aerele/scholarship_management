import frappe

def after_install():
	frappe.get_attr("scholarship_management.scholarship_management.doctype.student.student.party_setup")()
	frappe.get_attr("scholarship_management.customization.address.address_customization.customize_address_doctype")()
	create_workflow()

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
