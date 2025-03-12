import frappe
import erpnext

from frappe.utils import flt
from erpnext.accounts.party import get_party_account
from erpnext.setup.utils import get_exchange_rate
from erpnext.accounts.doctype.payment_entry.payment_entry import get_outstanding_on_journal_entry
from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry

class CustomPaymentEntry(PaymentEntry):
	def set_missing_ref_details(
		self,
		force: bool = False,
		update_ref_details_only_for: list | None = None,
		reference_exchange_details: dict | None = None,
	) -> None:
		# frappe.throw("set_missing_ref_details in scholarship_management")
		for d in self.get("references"):
			if d.allocated_amount:
				if update_ref_details_only_for and (
					(d.reference_doctype, d.reference_name) not in update_ref_details_only_for
				):
					continue

				ref_details = get_reference_details(
					d.reference_doctype,
					d.reference_name,
					self.party_account_currency,
					self.party_type,
					self.party,
				)

				# Only update exchange rate when the reference is Journal Entry
				if (
					reference_exchange_details
					and d.reference_doctype == reference_exchange_details.reference_doctype
					and d.reference_name == reference_exchange_details.reference_name
				):
					ref_details.update({"exchange_rate": reference_exchange_details.exchange_rate})

				for field, value in ref_details.items():
					if d.exchange_gain_loss:
						# for cases where gain/loss is booked into invoice
						# exchange_gain_loss is calculated from invoice & populated
						# and row.exchange_rate is already set to payment entry's exchange rate
						# refer -> `update_reference_in_payment_entry()` in utils.py
						continue

					if field == "exchange_rate" or not d.get(field) or force:
						d.db_set(field, value)

def on_submit(doc, event):
    update_outstanding_amount(doc, action="submit")

def on_cancel(doc, event):
    update_outstanding_amount(doc, action="cancel")

def update_outstanding_amount(doc, action):
    for reference in doc.references:
        if reference.reference_doctype == "Scholarship Sanction" and reference.reference_name:
            if action == "submit":
                new_outstanding = reference.outstanding_amount - reference.allocated_amount
            elif action == "cancel":
                paid_amount = frappe.get_all(
                    "Payment Entry Reference", 
                    filters={
                        "reference_doctype": "Scholarship Sanction", 
                        "reference_name": reference.reference_name, 
                        "parent": ["!=", doc.name],
                        "docstatus": 1
                    },
                    fields=["sum(allocated_amount) as paid_amount"]
                )[0].paid_amount or 0
                new_outstanding = reference.total_amount - flt(paid_amount)
            
            frappe.db.set_value("Scholarship Sanction", reference.reference_name, "outstanding_amount", new_outstanding)



@frappe.whitelist()
def get_reference_details(
	reference_doctype, reference_name, party_account_currency, party_type=None, party=None
):
	total_amount = outstanding_amount = exchange_rate = account = None

	ref_doc = frappe.get_doc(reference_doctype, reference_name)
	company_currency = ref_doc.get("company_currency") or erpnext.get_company_currency(ref_doc.company)

	# Only applies for Reverse Payment Entries
	account_type = None
	payment_type = None
	if reference_doctype == "Dunning":
		total_amount = outstanding_amount = ref_doc.get("dunning_amount")
		exchange_rate = 1

	elif reference_doctype == "Journal Entry" and ref_doc.docstatus == 1:
		if ref_doc.multi_currency:
			exchange_rate = get_exchange_rate(party_account_currency, company_currency, ref_doc.posting_date)
		else:
			exchange_rate = 1
			outstanding_amount, total_amount = get_outstanding_on_journal_entry(
				reference_name, party_type, party
			)

	elif reference_doctype == "Payment Entry":
		if reverse_payment_details := frappe.db.get_all(
			"Payment Entry",
			filters={"name": reference_name},
			fields=["payment_type", "party_type"],
		)[0]:
			payment_type = reverse_payment_details.payment_type
			account_type = frappe.db.get_value(
				"Party Type", reverse_payment_details.party_type, "account_type"
			)
		exchange_rate = 1

	elif reference_doctype != "Journal Entry":
		if not total_amount:
			if party_account_currency == company_currency:
				# for handling cases that don't have multi-currency (base field)
				total_amount = (
					ref_doc.get("base_rounded_total")
					or ref_doc.get("rounded_total")
					or ref_doc.get("base_grand_total")
					or ref_doc.get("grand_total")
				)
				exchange_rate = 1
			else:
				total_amount = ref_doc.get("rounded_total") or ref_doc.get("grand_total")
		if not exchange_rate:
			# Get the exchange rate from the original ref doc
			# or get it based on the posting date of the ref doc.
			exchange_rate = ref_doc.get("conversion_rate") or get_exchange_rate(
				party_account_currency, company_currency, ref_doc.posting_date
			)
			
		if reference_doctype in ("Sales Invoice", "Purchase Invoice", "Scholarship Sanction"):
			outstanding_amount = ref_doc.get("outstanding_amount")
			account = (
				ref_doc.get("debit_to") if reference_doctype == "Sales Invoice" else ref_doc.get("credit_to")
			)
		else:
			outstanding_amount = flt(total_amount) - flt(ref_doc.get("advance_paid"))

		if reference_doctype in ["Sales Order", "Purchase Order"]:
			party_type = "Customer" if reference_doctype == "Sales Order" else "Supplier"
			party_field = "customer" if reference_doctype == "Sales Order" else "supplier"
			party = ref_doc.get(party_field)
			account = get_party_account(party_type, party, ref_doc.company)
	else:
		# Get the exchange rate based on the posting date of the ref doc.
		exchange_rate = get_exchange_rate(party_account_currency, company_currency, ref_doc.posting_date)

	res = frappe._dict(
		{
			"due_date": ref_doc.get("due_date"),
			"total_amount": flt(total_amount),
			"outstanding_amount": flt(outstanding_amount),
			"exchange_rate": flt(exchange_rate),
			"bill_no": ref_doc.get("bill_no"),
			"account_type": account_type,
			"payment_type": payment_type,
		}
	)
	if account:
		res.update({"account": account})
		
	return res