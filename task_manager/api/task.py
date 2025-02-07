import frappe
import json

CACHE_TIMEOUT = 300  # Cache expiry time (in seconds)


def get_cache_timeout(resource_type):
    """Dynamically set cache timeout based on resource type."""
    timeouts = {
        "all_tasks": 300,  # 5 minutes for all tasks list
        "task": 600,        # 10 minutes for individual tasks
        "default": 180      # 3 minutes default
    }
    return timeouts.get(resource_type, timeouts["default"])


def format_error(message, code=500):
    """Formats error messages without unnecessary fields."""
    return {"error": message}, code


@frappe.whitelist(allow_guest=False)
def create_task():
    """Create a new Task."""
    if not frappe.session.user:
        return format_error("Authentication required.", 401)

    try:
        data = frappe.local.form_dict
        required_fields = ["title", "description", "status", "due_date"]

        # Validate required fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return format_error(f"Missing required fields: {', '.join(missing_fields)}", 400)

        # Create task
        doc = frappe.get_doc({
            "doctype": "Task",
            "title": data["title"],
            "description": data["description"],
            "status": data["status"],
            "due_date": data["due_date"]
        })
        doc.insert(ignore_permissions=True)

        # Clear cache after insert
        frappe.cache().delete("all_tasks")

        return {"message": "Task created successfully", "name": doc.name}, 201

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Task Creation Error")
        return format_error("Failed to create task.")


@frappe.whitelist()
def get_all_tasks(page=1, page_size=10, status=None):
    """Retrieve Tasks with pagination and optional filtering."""
    if not frappe.session.user:
        return format_error("Authentication required.", 401)

    try:
        # Generate a more specific cache key
        cache_key = f"tasks_page_{page}_size_{page_size}_status_{status}"
        cached_tasks = frappe.cache().get_value(cache_key)
        if cached_tasks:
            return {"tasks": json.loads(cached_tasks)}

        # Build dynamic filters
        filters = {}
        if status:
            filters["status"] = status

        # Fetch paginated tasks
        tasks = frappe.db.get_list(
            "Task",
            fields=["name", "title", "status", "due_date"],
            filters=filters,
            start=(page-1)*page_size,
            page_length=page_size
        )

        frappe.cache().set_value(
            cache_key,
            json.dumps(tasks),
            expires_in=get_cache_timeout("all_tasks")
        )
        return {"tasks": tasks}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Paginated Task Retrieval Error")
        return format_error("Failed to retrieve tasks.")

@frappe.whitelist()
def get_task(name):
    """Retrieve a single Task by name with caching."""
    if not frappe.session.user:
        return format_error("Authentication required.", 401)

    try:
        # Check cache first
        cache_key = f"task_{name}"
        cached_task = frappe.cache().get_value(cache_key)
        if cached_task:
            return json.loads(cached_task)

        # Fetch task from DB
        doc = frappe.db.get_value("Task", name, ["name", "title", "description", "status", "due_date"], as_dict=True)
        if not doc:
            return format_error("Task not found", 404)

        # Cache the result
        frappe.cache().set_value(cache_key, json.dumps(doc), expires_in=get_cache_timeout("task"))
        return doc

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Task Retrieval Error")
        return format_error("Failed to retrieve task.")


@frappe.whitelist()
def update_task(task_name, title=None, description=None, status=None, due_date=None, priority=None):
    """Update an existing Task."""
    if not frappe.session.user:
        return format_error("Authentication required.", 401)

    try:
        doc = frappe.get_doc("Task", task_name)

        # Update only if values are provided
        updated_fields = {}
        if title and title != doc.title:
            updated_fields["title"] = title
        if description and description != doc.description:
            updated_fields["description"] = description
        if status and status != doc.status:
            updated_fields["status"] = status
        if due_date and due_date != doc.due_date:
            updated_fields["due_date"] = due_date
        if priority and priority != doc.priority:
            updated_fields["priority"] = priority

        if updated_fields:
            doc.update(updated_fields)
            doc.save(ignore_permissions=True)
            frappe.db.commit()

            # Clear related caches
            frappe.cache().delete(f"task_{task_name}")
            frappe.cache().delete("all_tasks")

        return {"message": "Task updated successfully"}

    except frappe.DoesNotExistError:
        return format_error("Task not found", 404)

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Task Update Error")
        return format_error("Failed to update task.")


@frappe.whitelist()
def delete_task(task_name):
    """Delete a Task."""
    if not frappe.session.user:
        return format_error("Authentication required.", 401)

    try:
        frappe.delete_doc("Task", task_name, ignore_permissions=True)
        frappe.db.commit()

        # Clear related caches
        frappe.cache().delete(f"task_{task_name}")
        frappe.cache().delete("all_tasks")

        return {"message": "Task deleted successfully"}

    except frappe.DoesNotExistError:
        return format_error("Task not found", 404)

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Task Deletion Error")
        return format_error("Failed to delete task.")
