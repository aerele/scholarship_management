frappe.query_reports["Payment Entry Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"fieldtype": "Date",
			"label": "From",
			"mandatory": 0,
			"wildcard_filter": 0
		},
		{
			"fieldname": "to_date",
			"fieldtype": "Date",
			"label": "To",
			"mandatory": 0,
			"wildcard_filter": 0
		},
		// {
		// 	"fieldname": "maa_code",
		// 	"fieldtype": "Select", 
		// 	"label": "Maa Code",
		// 	"mandatory": 0,
		// 	"wildcard_filter": 0,
		// 	"options": []
		// },
		{
			"fieldname": "maa_code",
			"fieldtype": "Data", 
			"label": "Maa Code",
			"mandatory": 0,
			"wildcard_filter": 0,
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
		}
	],
	// "onload": function (report) {
	// 	frappe.call({
	// 		method: "scholarship_management.scholarship_management.report.payment_entry_report.payment_entry_report.get_maa_codes",  // Correct path to the Python function
	// 		callback: function (r) {
	// 			if (r.message) {
	// 				// Ensure valid response and that we have maa_codes
	// 				if (r.message.maa_codes) {
	// 					// Extracting MAA codes from the response
	// 					var maa_codes = r.message.maa_codes.map(function (item) {
	// 						return item.maa_code;
	// 					});

	// 					// Populate the options field for 'maa_code'
	// 					var maa_code_filter = report.filters.find(f => f.fieldname === 'maa_code');
	// 					if (maa_code_filter) {
	// 						// Joining the maa_codes with newline
	// 						maa_code_filter.options = maa_codes.join('\n');
	// 						// Refresh the field to reflect the changes
	// 						report.refresh_field('maa_code');
	// 					}
	// 				}
	// 			}
	// 		}
	// 	});
	// }
};
