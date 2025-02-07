### Task Manager

task manager app
# Task 1 instruction
## Prerequisites

Before installing Task Manager, ensure you have the following prerequisites:

- Python
- MariaDB
- Redis

### System Dependencies Installation

1. Install Python:
```bash
brew install python
brew link python
```

2. Install MariaDB and Redis:
```bash
brew install mariadb redis
```

### MariaDB Configuration

1. Configure MariaDB by editing the configuration file:
```bash
nano /usr/local/etc/my.cnf
```

2. Set your MariaDB root password:
```bash
mysql_secure_installation
```

## Frappe Installation

1. Install Frappe Bench:
```bash
pip3 install frappe-bench
```

2. Initialize a new Frappe environment:
```bash
bench init frappe-dev
cd frappe-dev
```

3. Create a new site:
```bash
bench new-site mysite.local
```

4. Start the Frappe server:
```bash
bench start
```

### App Installation

1. Create a new app:
```bash
bench new-app task_manager
```

2. Install the app to your site:
```bash
bench --site mysite.local install-app task_manager
```
change directory to the app you create and run

```
bench --site mysite.local  serve
```
remember to migrate
```
bench --site mysite.local migrate

```
Other anwser to the Test are inside <a href="./Task.md">Task.md Markdown</a>
