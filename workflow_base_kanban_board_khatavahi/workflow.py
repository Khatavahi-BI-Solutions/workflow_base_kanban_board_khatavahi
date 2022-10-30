import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def validate(doc,method=None):
    if not doc.is_active:
        return
    
    settings = frappe.get_single("Workflow Base Kanban Board Settings")
    enabled_doctype = settings.get("enabled_for", {"document_type": doc.document_type})

    if not enabled_doctype:
        return
    
    options = ""
    for row in doc.states:
        options += row.state + "\n"
    create_custom_fields({
        doc.document_type: [{
            "fieldname": "kanban_workflow", 
            "fieldtype": "Select",
            "options":options, 
            "label":"Kanban Workflow",
            "hidden":True
        }]
    })
    frappe.msgprint("Custom Field Updated in " + doc.document_type)