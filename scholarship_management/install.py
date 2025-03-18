import frappe

def after_install():
    frappe.get_attr("scholarship_management.scholarship_management.doctype.student.student.party_setup")()
    frappe.get_attr("scholarship_management.customization.address.address_customization.customize_address_doctype")()
