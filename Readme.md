# WordPress Migration Tool

Automated WordPress migration solution that handles the complete process from backup to deployment.

## Overview

This tool automates WordPress migration with three main components:

1. **migrate.py** - Creates backup of source WordPress site
2. **deploy-client.sh** - Deploys new WordPress instance on Kubernetes  
3. **import.py** - Imports backup to target site with upload limit management

## Features

- **Unified Workflow**: Single orchestrator script runs entire process
- **Headless Automation**: Browser automation using Playwright
- **Kubernetes Integration**: Automated K8s deployment
- **Upload Limit Management**: Automatically handles large backup files
- **Interactive Interface**: Guided setup with progress indicators  
## Prerequisites

- Python 3.12+ with virtual environment support
- WSL (Windows Subsystem for Linux) for Windows users  
- kubectl configured for your Kubernetes cluster
- K8s cluster with appropriate permissions

## Quick Start

### Windows
```bash
# Run the migration orchestrator
run-migration.bat
```

### Linux/WSL
```bash
# Check environment first
./check-prerequisites.sh

# Run the orchestrator
./wp-migration-orchestrator.sh
```

## Migration Workflow

### Phase 1: Source Site Backup
- Interactive prompts for WordPress credentials
- Automatic plugin installation/activation
- Headless browser automation for backup creation
- Organized file storage

### Phase 2: Kubernetes Deployment  
- Interactive namespace and database configuration
- MySQL and WordPress deployment
- Service and networking setup

### Phase 3: Upload Limit Management
- Automatic .htaccess modification (2M → 512M)
- Pod-level file system access via kubectl

### Phase 4: Backup Import
- Plugin installation on target WordPress
- Large file upload handling
- Database and file restoration

### Phase 5: Finalization
- Upload limit restoration (512M → 2M)
- Configuration cleanup

## File Structure

```
wp_migration_tool/
├── wp-migration-orchestrator.sh     # Main orchestrator
├── migrate.py                        # Source backup automation
├── import.py                         # Target import automation
├── deploy-client.sh                  # Kubernetes deployment
├── check-prerequisites.sh            # Environment validation
├── run-migration.bat                 # Windows wrapper
├── templates/                        # Kubernetes YAML templates
└── wp_migration_venv/                # Python virtual environment
```

## Troubleshooting

### Python/Playwright Issues
```bash
rm -rf wp_migration_venv
./check-prerequisites.sh
```

### Kubernetes Issues
```bash
kubectl cluster-info
kubectl get nodes
```


