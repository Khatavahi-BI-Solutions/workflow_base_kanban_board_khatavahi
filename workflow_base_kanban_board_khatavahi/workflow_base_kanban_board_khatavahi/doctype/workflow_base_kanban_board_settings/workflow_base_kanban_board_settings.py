# Copyright (c) 2022, Jigar Tarpara and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from workflow_base_kanban_board_khatavahi.workflow import validate as validate_workflow
class WorkflowBaseKanbanBoardSettings(Document):
	def validate(self):
		for row in self.enabled_for:
			try:
				workflow = frappe.get_doc("Workflow",{"document_type":row.document_type,"is_active":True })
				validate_workflow(workflow)
				frappe.msgprint("Custom Field Updated for "+ row.document_type + " and Workflow " + workflow)
			except:
				frappe.log_error()
				frappe.msgprint("Active Workflow not found for " + row.document_type)