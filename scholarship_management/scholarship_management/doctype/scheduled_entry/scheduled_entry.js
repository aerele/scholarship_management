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