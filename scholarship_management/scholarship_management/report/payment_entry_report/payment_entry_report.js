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
		{
			"fieldname": "maa_code",
			"fieldtype": "Select",
			"label": "Maa Code",
			"mandatory": 0,
			"wildcard_filter": 0,
			"options": []
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
			"fieldname": "mode_of_payment",
			"fieldtype": "Select",
			"label": "Mode of Payment",
			"options": [
				"",
				"Cheque",
				"Wire Transfer"
			].join('\n'),
			"mandatory": 0
		}
	],
	"onload": function (report) {
		frappe.call({
			method: "scholarship_management.scholarship_management.report.payment_entry_report.payment_entry_report.get_maa_codes",
			callback: function (r) {
				if (r.message && r.message.maa_codes) {

					const maa_codes = r.message.maa_codes.map(item => item.maa_code);

					let maa_code_filter = report.get_filter("maa_code");
					if (maa_code_filter) {
						maa_code_filter.df.options = ["", ...maa_codes].join('\n');
						maa_code_filter.refresh();
					}

				}
			}
		});
	}
};
