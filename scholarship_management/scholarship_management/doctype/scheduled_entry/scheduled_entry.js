frappe.listview_settings['Scheduled Entry'] = {
    get_indicator: function(doc) {
        let status_map = {
            "Draft": ["Draft", "orange", "status,=,Draft"],
            "Accept": ["Accepted", "green", "status,=,Accept"],
            "Reject": ["Rejected", "red", "status,=,Reject"]
        };
        return status_map[doc.status] || ["Unknown", "gray"];
    }
};

frappe.ui.form.on('Scheduled Entry',{
    refresh: function(frm){
        frm.set_query('student_academic_record',function(){
            return{
                filters:{
                    docstatus: 1,
                }
            };

        });
    }
})