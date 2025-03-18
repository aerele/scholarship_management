app_name = "scholarship_management"
app_title = "Scholarship Management"
app_publisher = "sakthi"
app_description = "Scholarship Management"
app_email = "sakthi@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "scholarship_management",
# 		"logo": "/assets/scholarship_management/logo.png",
# 		"title": "Scholarship Management",
# 		"route": "/scholarship_management",
# 		"has_permission": "scholarship_management.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/scholarship_management/css/scholarship_management.css"
# app_include_js = "/assets/scholarship_management/js/scholarship_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/schoverrideolarship_management/css/scholarship_management.css"
# web_include_js = "/assets/scholarship_management/js/scholarship_management.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "scholarship_management/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Payment Entry" : "public/js/payment_entry.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "scholarship_management/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "scholarship_management.utils.jinja_methods",
# 	"filters": "scholarship_management.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "scholarship_management.install.before_install"
after_install = "scholarship_management.install.after_install"
# Uninstallation
# ------------

# before_uninstall = "scholarship_management.uninstall.before_uninstall"
# after_uninstall = "scholarship_management.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "scholarship_management.utils.before_app_install"
# after_app_install = "scholarship_management.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "scholarship_management.utils.before_app_uninstall"
# after_app_uninstall = "scholarship_management.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "scholarship_management.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Payment Entry": {
        "on_submit": "scholarship_management.customization.payment_entry.payment_entry.on_submit",
        "on_cancel": "scholarship_management.customization.payment_entry.payment_entry.on_cancel"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"scholarship_management.tasks.all"
# 	],
# 	"daily": [
# 		"scholarship_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"scholarship_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"scholarship_management.tasks.weekly"
# 	],
# 	"monthly": [
# 		"scholarship_management.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "scholarship_management.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
    "erpnext.accounts.doctype.payment_entry.payment_entry.get_reference_details": "scholarship_management.customization.payment_entry.payment_entry.get_reference_details"
}
override_doctype_class = {"Payment Entry": "scholarship_management.customization.payment_entry.payment_entry.CustomPaymentEntry"}

#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "scholarship_management.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["scholarship_management.utils.before_request"]
# after_request = ["scholarship_management.utils.after_request"]

# Job Events
# ----------
# before_job = ["scholarship_management.utils.before_job"]
# after_job = ["scholarship_management.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"scholarship_management.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

