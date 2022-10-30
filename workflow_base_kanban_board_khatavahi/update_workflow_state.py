# for every doctype
import frappe
from frappe.model.workflow import  get_workflow, WorkflowPermissionError,get_transitions
from frappe import _

def on_update(doc,method):
	enabled_doctype = check_kanban_setting(doc)
	
	if not enabled_doctype:
		return
	print("Workflow Changes ",doc.workflow_state, doc.kanban_workflow)
	doc.kanban_workflow = doc.workflow_state 

def validate(doc, method):
	enabled_doctype = check_kanban_setting(doc)
	
	if not enabled_doctype:
		return
	
	if kanban_workflow_changed(doc):
		validate_workflow(doc)
		doc.workflow_state = doc.kanban_workflow
	if workflow_changed(doc):
		doc.kanban_workflow = doc.workflow_state 

def kanban_workflow_changed(doc):
	current_state = None
	if getattr(doc, "_doc_before_save", None):
		current_state = doc._doc_before_save.get("kanban_workflow")
	next_state = doc.get("kanban_workflow")
	if next_state != current_state:
		return True
	else:
		return False

def workflow_changed(doc):
	current_state = None
	if getattr(doc, "_doc_before_save", None):
		current_state = doc._doc_before_save.get("workflow_state")
	next_state = doc.get("workflow_state")
	if next_state != current_state:
		return True
	else:
		return False

def check_kanban_setting(doc):
	settings = frappe.get_single("Workflow Base Kanban Board Settings")
	enabled_doctype = settings.get("enabled_for", {"document_type": doc.doctype})
	return enabled_doctype

def validate_workflow(doc):
	"""Validate Workflow State and Transition for the current user.

	- Check if user is allowed to edit in current state
	- Check if user is allowed to transition to the next state (if changed)
	"""
	workflow = get_workflow(doc.doctype)

	current_state = None
	if getattr(doc, "_doc_before_save", None):
		current_state = doc._doc_before_save.get("kanban_workflow")
	next_state = doc.get("kanban_workflow")

	if not next_state:
		next_state = workflow.states[0].state
		doc.set("kanban_workflow", next_state)

	if not current_state:
		current_state = workflow.states[0].state

	state_row = [d for d in workflow.states if d.state == current_state]
	if not state_row:
		frappe.throw(
			_("{0} is not a valid Workflow State. Please update your Workflow and try again.").format(
				frappe.bold(current_state)
			)
		)
	state_row = state_row[0]

	# if transitioning, check if user is allowed to transition
	if current_state != next_state:
		bold_current = frappe.bold(current_state)
		bold_next = frappe.bold(next_state)

		if not doc._doc_before_save:
			# transitioning directly to a state other than the first
			# e.g from data import
			frappe.throw(
				_("Workflow State transition not allowed from {0} to {1}").format(bold_current, bold_next),
				WorkflowPermissionError,
			)

		transitions = get_transitions(doc._doc_before_save)
		transition = [d for d in transitions if d.next_state == next_state]
		if not transition:
			frappe.throw(
				_("Workflow State transition not allowed from {0} to {1}").format(bold_current, bold_next),
				WorkflowPermissionError,
			)