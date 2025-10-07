# WordPress Migration Tool - Clean Setup

## Core Files (Essential)

### Main Scripts
- `wp-migration-orchestrator.sh` - Main orchestrator that runs everything
- `migrate.py` - Creates backup from source WordPress
- `import.py` - Imports backup to target WordPress  
- `deploy-client.sh` - Deploys new WordPress on Kubernetes

### Supporting Tools
- `check-prerequisites.sh` - Validates environment setup
- `run-migration.bat` - Windows wrapper for easy execution
- `test-environment.sh` - Tests the Python environment

### Configuration
- `templates/` - Kubernetes YAML templates
- `wp_migration_venv/` - Python virtual environment (auto-created)
- `.gitignore` - Essential Git ignore rules

### Documentation
- `README.md` - Main documentation
- `ORCHESTRATOR_README.md` - Detailed orchestrator guide
- `SETUP_COMPLETE.md` - Setup completion reference

## Quick Usage

**Windows**: Double-click `run-migration.bat`
**Linux/WSL**: Run `./wp-migration-orchestrator.sh`

The orchestrator handles everything automatically - just follow the prompts!