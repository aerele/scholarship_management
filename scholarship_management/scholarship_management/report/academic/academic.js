frappe.query_reports["Academic"] = {
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
			"fieldname": "academic_entry",
			"fieldtype": "Link",
			"label": "Academic Entry",
			"options": "Academic Entry",
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
		}
	],
	"onload": function (report) {
		frappe.call({
			method: "scholarship_management.scholarship_management.report.academic.academic.get_select_fields",
			callback: function (r) {
				if (r.message && r.message.maa_codes) {

					let maa_codes = r.message.maa_codes.map(item => item.maa_code);

					let maa_code_filter = report.get_filter("maa_code");
					if (maa_code_filter) {
						maa_code_filter.df.options = ["", ...maa_codes].join('\n');
						maa_code_filter.refresh();
					}

					let student_names = r.message.maa_codes.map(item => item.student_name);

					let student_filter = report.get_filter("student_name");
					if (student_filter) {
						student_filter.df.options = ["", ...student_names].join('\n');
						student_filter.refresh();
					}
				}

			}
		});
	}

};
