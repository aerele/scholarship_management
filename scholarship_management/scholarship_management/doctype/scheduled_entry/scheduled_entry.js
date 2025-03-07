
frappe.ui.form.on("Scheduled Entry", {
    refresh(frm) {
        frm.set_value("call_date", frappe.datetime.now_date()); 
        frm.set_value("call_time", frappe.datetime.now_time());
    }
});
