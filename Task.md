# Project Management System Documentation

## Task 3: Data Management

### Project Management System Schema Design

```json
// Project DocType
{
    "name": "Project",
    "doctype": "DocType",
    "module": "Project Management",
    "fields": [
        {
            "fieldname": "title",
            "label": "Project Title",
            "fieldtype": "Data",
            "required": 1
        },
        {
            "fieldname": "description",
            "label": "Project Description",
            "fieldtype": "Text Editor"
        },
        {
            "fieldname": "project_code",
            "label": "Project Code",
            "fieldtype": "Data",
            "unique": 1
        },
        {
            "fieldname": "status",
            "label": "Project Status",
            "fieldtype": "Select",
            "options": [
                "Planning",
                "In Progress",
                "On Hold",
                "Completed",
                "Cancelled"
            ],
            "default": "Planning"
        },
        {
            "fieldname": "start_date",
            "label": "Start Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "expected_end_date",
            "label": "Expected End Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "actual_end_date",
            "label": "Actual End Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "project_manager",
            "label": "Project Manager",
            "fieldtype": "Link",
            "options": "User"
        },
        {
            "fieldname": "client",
            "label": "Client",
            "fieldtype": "Link",
            "options": "Customer"
        }
    ],
    "search_fields": ["title", "project_code", "status"],
    "title_field": "title"
}

// Project Task DocType
{
    "name": "Project Task",
    "doctype": "DocType",
    "module": "Project Management",
    "fields": [
        {
            "fieldname": "title",
            "label": "Task Title",
            "fieldtype": "Data",
            "required": 1
        },
        {
            "fieldname": "project",
            "label": "Project",
            "fieldtype": "Link",
            "options": "Project",
            "required": 1
        },
        {
            "fieldname": "description",
            "label": "Task Description",
            "fieldtype": "Text Editor"
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Select",
            "options": [
                "Not Started",
                "In Progress",
                "Pending",
                "Completed",
                "Cancelled"
            ],
            "default": "Not Started"
        },
        {
            "fieldname": "priority",
            "label": "Priority",
            "fieldtype": "Select",
            "options": [
                "Low",
                "Medium",
                "High",
                "Urgent"
            ],
            "default": "Medium"
        },
        {
            "fieldname": "assigned_to",
            "label": "Assigned To",
            "fieldtype": "Link",
            "options": "User"
        },
        {
            "fieldname": "start_date",
            "label": "Start Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "expected_end_date",
            "label": "Expected End Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "actual_end_date",
            "label": "Actual End Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "parent_task",
            "label": "Parent Task",
            "fieldtype": "Link",
            "options": "Project Task"
        }
    ]
}

// Time Log DocType
{
    "name": "Time Log",
    "doctype": "DocType",
    "module": "Project Management",
    "fields": [
        {
            "fieldname": "project_task",
            "label": "Project Task",
            "fieldtype": "Link",
            "options": "Project Task",
            "required": 1
        },
        {
            "fieldname": "user",
            "label": "User",
            "fieldtype": "Link",
            "options": "User",
            "required": 1
        },
        {
            "fieldname": "hours",
            "label": "Hours Worked",
            "fieldtype": "Float",
            "required": 1
        },
        {
            "fieldname": "billable",
            "label": "Billable",
            "fieldtype": "Check"
        },
        {
            "fieldname": "billing_rate",
            "label": "Billing Rate",
            "fieldtype": "Currency"
        },
        {
            "fieldname": "date",
            "label": "Date",
            "fieldtype": "Date",
            "default": "Today"
        },
        {
            "fieldname": "description",
            "label": "Description",
            "fieldtype": "Small Text"
        }
    ]
}
```

### Database Normalization Principles Applied

#### First Normal Form (1NF)
- Each table has a primary key
- Atomic values in each column
- No repeating groups

#### Second Normal Form (2NF)
- Removed partial dependencies
- Created separate tables for distinct entities
- Used foreign key relationships

#### Third Normal Form (3NF)
- Eliminated transitive dependencies
- Separated billable information in Time Log
- Minimized data redundancy

### Relationships
- One Project can have multiple Tasks
- One Project can have multiple Milestones
- One Task can have multiple Time Logs
- One Task can have sub-tasks
- One Project belongs to one Customer

## Task 4: API Optimization

### Performance Optimization Strategies
-  Use frappe.get_all with specific fields instead of frappe.get_list or frappe.get_doc
-  Add indexing on frequently queried fields like status and due_date
-  Use pagination for large data retrieval


### Caching Implementation

- Use Frappe's cache (frappe.cache()) to store frequently accessed data
-  Cache the results of get_all_tasks() and get_task(name) using a unique key


## Task 5: Problem Solving and Debugging

### Example Scenario
Problem: Slow-loading report with large datasets

### Debugging Process
```python
import frappe
import time

def my_report(filters):
    start_time = time.time()
    frappe.logger().debug("Report started")

    # Initial data retrieval
    data = frappe.db.sql("SELECT * FROM `tabTask` WHERE status = 'Open'", as_dict=True)
    end_time_data = time.time()
    frappe.logger().debug(f"Data Retrieval took: {end_time_data - start_time} seconds")

    # Processing the data
    processed_data = []
    for row in data:
        processed_data.append({
            "task_name": row["task_name"],
            "description": row["description"]
        })
    end_time_processing = time.time()
    frappe.logger().debug(f"Data Processing took: {end_time_processing - end_time_data} seconds")

    columns = ["Task Name:Data", "Description:Data"]
    return columns, processed_data
```

### Optimization Steps
1. Identify Bottleneck using Frappe's logging and profiling tools
2. Optimize Queries using EXPLAIN in MariaDB/MySQL
3. Reduce Data with filters and pagination
4. Implement Caching
5. Optimize Code using efficient operations

### Resolution Example
The report performance was improved by:
- Adding index to the 'status' field
- Implementing 1-hour result caching
- Optimizing SELECT statement columns
