frappe.ui.form.on("Student", {
	refresh: function (frm) {
		if (frm.doc.__islocal) {
			hide_field(["address_html"]);
			frm.trigger("clear_address");
		} else {
			unhide_field(["address_html"]);
			frm.trigger("render_address");
		}


		if (!frm.is_new()) {
			frm.add_custom_button(
				__("Create Academic Entry"),
				function () {
					frm.trigger("create_academic");
				}, __("Create"))
		}
	},

	create_academic: function (frm) {
		frappe.new_doc("Academic Entry", {
			select_student: frm.doc.name
		})
	},
	render_address: function (frm) {
		// render address
		if (frm.fields_dict["address_html"] && "addr_list" in frm.doc.__onload) {
			$(frm.fields_dict["address_html"].wrapper)
				.html(frappe.render_template(`
						<div class="clearfix"></div>
				{% for address in addr_list %}
				<div class="address-box">
						<a
						href="{%= frappe.utils.get_form_link('Address', address.name) %}"
						class="btn btn-xs btn-default edit-btn"
						title="{%= __('Edit') %}"
						>
						<svg class="icon icon-xs">
								<use href="#icon-edit"></use>
						</svg>
						</a>
						
						<p>
						{% if address.is_primary_address %}
								<span class="badge badge-primary">{{ __("Preferred Billing Address") }}</span>
						{% endif %}
						{% if address.is_shipping_address %}
								<span class="badge badge-info">{{ __("Preferred Shipping Address") }}</span>
						{% endif %}
						</p>
						
						<h6>{{ address.address_title }}</h6>
						
						<p>
						{{ address.address_line1 }}<br>
						{% if address.address_line2 %}{{ address.address_line2 }}<br>{% endif %}
						{{ address.city }}, {{ address.state }} - {{ address.pincode }}<br>
						{{ address.country }}
						</p>
						
						<p>{{ address.display }}</p>
						
						<p><strong>{{ __("Phone") }}:</strong> {{ address.phone }}</p>
						<p><strong>{{ __("Email") }}:</strong> {{ address.email_id }}</p>
						<p><strong>{{ __("Fax") }}:</strong> {{ address.fax }}</p>
						<p><strong>{{ __("Branch Code") }}:</strong> {{ address.branch_code }}</p>
						<p><strong>{{ __("Address No") }}:</strong> {{ address.addrount_no }}</p>
				</div>
				{% endfor %}

				{% if (!addr_list.length)  %}
				<p class="text-muted small">{{ __("No Address added yet.") }}</p>
				{% endif %}

				<p>
				<button class="btn btn-xs btn-default btn-address">
						{{ __("New Address") }}
				</button>
				</p>
				`, frm.doc.__onload))
				.find(".btn-address")
				.on("click", () => new_record("Address", frm.doc));
		}
	},
	clear_address: function (frm) {
		$(frm.fields_dict["address_html"].wrapper).html("");
		frm.fields_dict["address_html"] && $(frm.fields_dict["address_html"].wrapper).html("");
	},
})

function new_record(doctype, source_doc) {
	return frappe.new_doc(doctype, {
		"links": [{
			"link_doctype": source_doc.doctype,
			"link_name": source_doc.name,
			"link_title": source_doc.name
		}]
	});
}