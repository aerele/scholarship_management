# Copyright (c) 2025, sakthi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, nowtime

class ScheduledEntry(Document):
    pass
	# def after_save(self):
	# 	self.set_up_current_time
	# def set_up_current_time(self):
	# 	self.call_date = today() 
	# 	self.call_time = nowtime()