# WP Migration Automation Tool (EC2 Headless Script)

This Python script automates the complete **WordPress site backup and file transfer process** using **Playwright**. It logs into the WordPress admin interface, ensures the **All-in-One WP Migration** plugin is active, triggers a full export, and downloads the resulting `.wpress` file directly to a **site-specific folder** on the host (AWS EC2) server.

---

## Features

- **Headless Automation:** Runs entirely without a GUI, ideal for servers or CI pipelines.  
- **Robust Plugin Management:** Automatically checks for the plugin and activates or installs it if needed.  
- **Site-Specific Storage:** Creates dedicated directories (`/home/ubuntu/.../wp_site_name/`) for organized backups.  
- **Resilient Export Workflow:** Uses retry loops and explicit visibility waits to handle WordPress UI and AJAX timing issues reliably.

---

## Prerequisites

**Host Machine:** Ubuntu server (e.g., AWS EC2) with SSH access.  
**Dependencies:** Python 3, pip, and Playwright installed on the host:
```bash
sudo apt install -y python3 python3-pip
pip install playwright
playwright install

```

## Setup & Configuration

#### Open migrate.py and update global variables


| Variable | Description     | Example                |
| :-------- | :------- | :------------------------- |
| `WP_URL` | `Full URL of the WordPress site` | `https://wp.t4gc.in` |
| `USERNAME` | `WordPress Administrator username` | `wp_admin` |
| `PASSWORD` | `WordPress Administrator password` | `wp_password` |
| `BASE_EC2_DIR` | `Absolute path on EC2 where backups will be saved` | `"/home/ubuntu/backup-receiver/recieved_wp"` |
## Usage

``` bash
python3 migrate.py

```
## Authors

- [@ajith4Tech](https://www.github.com/ajith4Tech)


