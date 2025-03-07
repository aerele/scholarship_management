# Copyright (c) 2025, sakthi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class GradePercentage(Document):
	def validate(self):
		if self.min_mark >= self.max_mark:
			frappe.throw("Minimum mark should be less than Maximum mark")

		overlapping_ranges = frappe.get_all(
			"Grade Percentage",
			filters={
				"name": ["!=", self.name],  
				"min_mark": ["<=", self.max_mark], 
				"max_mark": [">=", self.min_mark]  
			},
			fields=["grade", "min_mark", "max_mark"]
		)

		if overlapping_ranges:
			existing = overlapping_ranges[0]
			frappe.throw(f"Mark range {self.min_mark}-{self.max_mark} overlaps with existing grade {existing['grade']} ({existing['min_mark']}-{existing['max_mark']})")
