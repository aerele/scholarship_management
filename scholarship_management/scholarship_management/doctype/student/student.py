import frappe
from datetime import datetime, date
from frappe.model.document import Document

from frappe.desk.page.setup_wizard.setup_wizard import make_records

class Student(Document):
    def validate(doc):
        if doc.date_of_birth:
            doc.age = calculate_age(doc.date_of_birth)

    def onload(doc):
        doc.load_address()

    def load_address(doc, key=None) -> None:
        """Loads address list in `__onload`"""
        doc.set_onload("addr_list", doc.get_address_display_list())
        frappe.db.commit()

    def get_address_display_list(doc):
        """Fetch addresses linked to the student"""
        addr_list = frappe.get_list(
            "Address",
            filters=[
                ["Dynamic Link", "link_doctype", "=", doc.doctype],
                ["Dynamic Link", "link_name", "=", doc.name],
                ["Dynamic Link", "parenttype", "=", "Address"],
			],
            fields=["*"],
            order_by="`tabAddress`.creation ASC",
        )

        return addr_list
    
def calculate_age(date_of_birth):
    if not date_of_birth:
        return 0 

    dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
    today = date.today()

    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    
    return age

    
def party_setup():
    records = [{"doctype": "Party Type", "party_type": "Student", "account_type": "Payable"}]
    make_records(records, debug=False)
