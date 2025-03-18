frappe.ui.form.on("Schedule Call", {
	refresh(frm) {
		frm.add_custom_button(__("Schedule Selected Entry"),
			function(){
				frm.trigger("schedule_entry")
		})

		frm.add_custom_button("Search", function () {
			frm.call({
				doc: frm.doc,
				method: "search_records",
				args: {
					present_academic_year: frm.doc.present_academic_year,
					from: frm.doc.from,
					to: frm.doc.to,
					interview_place: frm.doc.interview_place,
					stream: frm.doc.stream,
					study_group: frm.doc.study_group,
					course: frm.doc.course,
					maa_code: frm.doc.maa_code,
					acceptreject: frm.doc.acceptreject,
					widow: frm.doc.widow,
					type_of_postage: frm.doc.type_of_postage,
					name1: frm.doc.name1,
					repeat: frm.doc.repeat
				},
				callback: () => {
					frm.refresh();
				},
			});

		});
	},

    schedule_entry: function(frm) {
        let selected_rows = frm.fields_dict["record"].grid.get_selected_children();
        if (selected_rows.length > 0) {
            let current_date = frappe.datetime.now_date();
            let current_time = frappe.datetime.now_time();

            let selected_maa_codes = selected_rows.map(row => row.maa_code);
            frm.call({
				doc: frm.doc,
                method: "schedule_selected_entry",
                args: {
                    maa_codes: selected_maa_codes,
                    call_date: current_date,
                    call_time: current_time
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint(`Scheduled Entries created successfully.`);
                        frm.refresh(); 
                    }
                }
            });
        } else {
            frappe.msgprint(__("Please select at least one row."));
        }
	},

	study_group: function(frm) {
        if (frm.doc.study_group) {
            frm.set_query("course", function() {
                return {
                    filters: {
                        "study_group": frm.doc.study_group
                    }
                };
            });
        }
    },
});