# WordPress Migration Orchestrator

A comprehensive shell script that automates the complete WordPress migration process by orchestrating three components:

1. **migrate.py** - Creates backup of source WordPress site
2. **deploy-client.sh** - Deploys new WordPress instance on Kubernetes
3. **import.py** - Imports backup with automatic upload limit management

## Features

✅ **Interactive Workflow** - Guides you through each step with clear prompts  
✅ **Automatic Upload Limit Management** - Temporarily increases limits to 512M for import, then restores to 2M  
✅ **Robust Error Handling** - Validates files, waits for services, and provides detailed feedback  
✅ **Clean Configuration** - Automatically updates script configurations without manual editing  
✅ **Comprehensive Logging** - Color-coded output with clear success/error messages  
✅ **Automatic Cleanup** - Removes temporary files on completion or failure  

## Prerequisites

### Host Requirements
- Linux/Unix environment (WSL on Windows)
- Python 3 with playwright installed
- kubectl configured for your Kubernetes cluster
- Bash shell
- curl (for service health checks)

### Python Dependencies
```bash
pip install playwright
playwright install
```

### Kubernetes Requirements
- K3s or Kubernetes cluster access
- kubectl configured and tested
- Sufficient cluster resources for WordPress deployment

## Directory Structure

Ensure your project directory contains:
```
wp_migration_tool/
├── wp-migration-orchestrator.sh    # Main orchestrator script
├── migrate.py                       # Source site backup script
├── deploy-client.sh                 # Kubernetes deployment script
├── import.py                        # Backup import script
└── templates/                       # Kubernetes YAML templates
    ├── mysql-service.yaml
    ├── mysql-statefulset.yaml
    ├── wordpress-deployment.yaml
    ├── wordpress-limit-job.yaml
    ├── wp-configmap.yaml
    ├── wp-secret.yaml
    └── wp-service.yaml
```

## Usage

### Quick Start
```bash
# Make script executable (Linux/Unix)
chmod +x wp-migration-orchestrator.sh

# Run the orchestrator
./wp-migration-orchestrator.sh
```

### Windows (using WSL)
```bash
# Switch to WSL
wsl

# Navigate to your project directory
cd /mnt/c/Users/abhir/OneDrive/Desktop/Projects/wp_migration_tool

# Make executable and run
chmod +x wp-migration-orchestrator.sh
./wp-migration-orchestrator.sh
```

## Interactive Workflow

The script will guide you through 6 phases:

### Phase 1: Source Site Backup
- Enter source WordPress URL
- Provide admin credentials
- Automated backup creation and storage

### Phase 2: Deploy New WordPress Instance
- Interactive Kubernetes deployment
- Configure client namespace, database, and credentials
- Automated pod deployment and service creation

### Phase 3: Target Site Configuration
- Specify target WordPress URL and credentials
- Service readiness validation

### Phase 4: Preparing for Import
- Automatic upload limit increase (2M → 512M)
- .htaccess backup and modification

### Phase 5: Importing Backup
- Plugin installation and activation
- Backup file upload and restoration
- WordPress configuration import

### Phase 6: Finalization
- Upload limit restoration (512M → 2M)
- Cleanup and completion summary

## Example Session

```bash
$ ./wp-migration-orchestrator.sh

===========================================
WordPress Migration Orchestrator
===========================================

ℹ️  This script will:
ℹ️  1. Backup your source WordPress site
ℹ️  2. Deploy a new WordPress instance on Kubernetes
ℹ️  3. Import the backup to the new instance

===========================================
PHASE 1: SOURCE SITE BACKUP
===========================================

Enter source WordPress URL (e.g., https://old-site.com): https://myoldsite.com
Enter source WordPress admin username: admin
Enter source WordPress admin password: [hidden]

ℹ️  Updating migrate.py configuration...
ℹ️  Starting backup process...
   -> Login successful.
   -> Plugin is already ACTIVE. Proceeding to export.
   ✅ Backup file saved to EC2 at: /home/ubuntu/backup-receiver/recieved_wp/myoldsite_com/myoldsite-20241008-143022-abc123.wpress
✅ Backup completed successfully!

===========================================
PHASE 2: DEPLOY NEW WORDPRESS INSTANCE
===========================================

--- Client WordPress Deployment Setup ---
Enter Client Namespace (e.g., client-a): client-migration
Enter DB Name (e.g., client_a_wp_db): migration_wp_db
Enter DB User (e.g., wp_client_a_user): wp_migration_user
Enter WP DB Password: [hidden]
Enter MySQL ROOT Password: [hidden]

✅ Deployment for client 'client-migration' is complete!

[... continues through all phases ...]

===========================================
MIGRATION COMPLETE!
===========================================

✅ WordPress migration completed successfully!
ℹ️  Source site: https://myoldsite.com
ℹ️  Target site: https://mynewsite.com
ℹ️  Kubernetes namespace: client-migration
ℹ️  You can now access your migrated site at: https://mynewsite.com

🎉 Migration orchestration completed successfully!
```

## Troubleshooting

### Common Issues

**Script not executable:**
```bash
chmod +x wp-migration-orchestrator.sh
```

**Python dependencies missing:**
```bash
pip install playwright
playwright install
```

**Kubernetes access issues:**
```bash
kubectl cluster-info
kubectl get nodes
```

**WordPress not ready:**
- Check pod status: `kubectl get pods -n [namespace]`
- Check services: `kubectl get svc -n [namespace]`
- Check logs: `kubectl logs -n [namespace] [pod-name]`

### File Upload Issues

If imports fail due to upload limits:
- The script automatically manages .htaccess files
- Manual recovery: Check `/var/www/html/.htaccess.backup` in WordPress pod
- Verify PHP settings in WordPress container

### Backup File Issues

If backup files aren't found:
- Check `/home/ubuntu/backup-receiver/recieved_wp/[site-folder]/`
- Verify migrate.py completed successfully
- Check disk space on backup server

## Security Considerations

- Passwords are handled securely (hidden input)
- Temporary files are automatically cleaned up
- Original .htaccess files are backed up before modification
- No credentials are stored permanently in scripts

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review individual script logs (migrate.py, import.py output)
3. Verify Kubernetes cluster status
4. Check WordPress pod logs for application-level issues

## Authors

- [@ajith4Tech](https://www.github.com/ajith4Tech)