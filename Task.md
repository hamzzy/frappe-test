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
### Debugging Example: Sales Analysis Report Performance Issue

#### Problem
- Slow report generation for large date ranges (1+ month)
- High CPU usage during report generation
- Several minutes completion time

#### Investigation Steps
1. Enable Frappe profiler in site_config.json
2. Add logging timestamps around key operations
3. Use EXPLAIN for SQL query analysis
4. Monitor system resources (CPU, memory)

#### Solution Components
1. Database Optimization
    ```sql
    -- Add index to posting_date
    ALTER TABLE `tabSales Order` ADD INDEX `idx_posting_date` (posting_date);
    ```

2. Query Optimization
    ```python
    # Use efficient SQL aggregates
    total_sales = frappe.db.sql("""
         SELECT SUM(grand_total)
         FROM `tabSales Order`
         WHERE posting_date BETWEEN %(from_date)s AND %(to_date)s
    """, filters)[0][0] or 0
    ```

3. Caching Implementation
    - Use Redis cache for frequent queries
    - Implement background jobs for large reports

#### Results
- Report generation time reduced by 80%
- CPU usage normalized
- Improved user experience
