frappe.query_reports["Sanctioned Amount"] = {
	"filters": [
		{
			"fieldname": "maa_code",
			"fieldtype": "Select",
			"label": "Maa Code",
			"options": [],
			"mandatory": 0
		},
		{
			"fieldname": "student_name",
			"fieldtype": "Select",
			"label": "Student Name",
			"options": [],
			"mandatory": 0
		},
		{
			"fieldname": "trust",
			"fieldtype": "Link",
			"label": "Trust",
			"options": "Trust",
			"mandatory": 0
		},
		{
			"fieldname": "gender",
			"fieldtype": "Select",
			"label": "Gender",
			"options": ["", "Male", "Female", "Other"].join('\n'),
			"mandatory": 0
		},
		{
			"fieldname": "mobile_no",
			"fieldtype": "Data",
			"label": "Contact No",
			"mandatory": 0
		},
		{
			"fieldname": "district",
			"fieldtype": "Link",
			"label": "District",
			"options": "District",
			"mandatory": 0
		},
		{
			"fieldname": "town_village",
			"fieldtype": "Link",
			"label": "Town/Village",
			"options": "Town Village",
			"mandatory": 0
		},
		{
			"fieldname": "taluka",
			"fieldtype": "Link",
			"label": "Taluka",
			"options": "Taluka",
			"mandatory": 0
		},
		{
			"fieldname": "academic_year",
			"fieldtype": "Link",
			"label": "Academic Year",
			"options": "Academic Year",
			"mandatory": 0
		},
		{
			"fieldname": "course",
			"fieldtype": "Link",
			"label": "Course",
			"options": "Course Master",
			"mandatory": 0
		},
		{
			"fieldname": "year_studying",
			"fieldtype": "Link",
			"label": "Studying Year",
			"options": "Year Studying",
			"mandatory": 0
		},
		{
			"fieldname": "study_group",
			"fieldtype": "Link",
			"label": "Study Group",
			"options": "Study Group",
			"mandatory": 0
		},
		{
			"fieldname": "postage",
			"fieldtype": "Link",
			"label": "Postage",
			"options": "Type of Postage Master",
			"mandatory": 0
		},
		{
			"fieldname": "category",
			"fieldtype": "Select",
			"label": "Category",
			"options": [
				"",
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
			].join('\n'),
			"mandatory": 0
		},
		{
			"fieldname": "repeat",
			"fieldtype": "Select",
			"label": "Repeat",
			"options": [
				"",
				"Yes",
				"No",
				"Both"
			].join('\n'),
			"mandatory": 0
		},
		{
			"fieldname": "sanctioned_amount",
			"fieldtype": "Float",
			"label": "Sanctioned Amount",
			"mandatory": 0
		},
		{
			"fieldname": "widow",
			"fieldtype": "Select",
			"label": "Widow",
			"options": [
				"",
				"Yes",
				"No",
				"Both"
			].join('\n'),
			"mandatory": 0
		},
		{
			"fieldname": "ganchi",
			"fieldtype": "Select",
			"label": "Ganchi",
			"options": [
				"",
				"Yes",
				"No",
				"Both"
			].join('\n'),
			"mandatory": 0
		},
		{
			"fieldname": "status",
			"fieldtype": "Select",
			"label": "Status",
			"options": [
				"",
				"Paid",
				"Not Paid",
				"Partially Paid"
			].join('\n'),
			"mandatory": 0
		}
	],
	"onload": function (report) {
		frappe.call({
			method: "scholarship_management.scholarship_management.report.academic.academic.get_select_fields",
			callback: function (r) {
				if (r.message) {

					const maa_codes = r.message.maa_codes || [];

					const maa_code_filter = report.get_filter("maa_code");
					const student_name_filter = report.get_filter("student_name");

					if (maa_code_filter && student_name_filter) {
						maa_code_filter.df.options = ["", ...maa_codes.map(x => x.maa_code)].join('\n');
						maa_code_filter.refresh();

						student_name_filter.df.options = ["", ...maa_codes.map(x => x.student_name)].join('\n');
						student_name_filter.refresh();
					}
				}

			}
		});
	}

};