#!/bin/bash
# WordPress Migration Prerequisites Checker
# Validates that all required components are available before running the orchestrator

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "\n${BLUE}===========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}===========================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

check_command() {
    if command -v "$1" >/dev/null 2>&1; then
        print_success "$1 is available"
        return 0
    else
        print_error "$1 is not available"
        return 1
    fi
}

check_file() {
    if [ -f "$1" ]; then
        print_success "$1 exists"
        return 0
    else
        print_error "$1 not found"
        return 1
    fi
}

check_directory() {
    if [ -d "$1" ]; then
        print_success "$1 directory exists"
        return 0
    else
        print_error "$1 directory not found"
        return 1
    fi
}

check_python_package() {
    if python3 -c "import $1" >/dev/null 2>&1; then
        print_success "Python package '$1' is installed"
        return 0
    else
        print_error "Python package '$1' is not installed"
        return 1
    fi
}

main() {
    print_header "WordPress Migration Prerequisites Check"
    
    local errors=0
    
    # Check required commands
    print_info "Checking required commands..."
    check_command "python3" || errors=$((errors + 1))
    check_command "pip" || check_command "pip3" || errors=$((errors + 1))
    check_command "kubectl" || errors=$((errors + 1))
    check_command "bash" || errors=$((errors + 1))
    check_command "curl" || errors=$((errors + 1))
    check_command "sed" || errors=$((errors + 1))
    
    # Check Python packages
    echo
    print_info "Checking Python packages..."
    check_python_package "playwright" || errors=$((errors + 1))
    
    # Check if playwright browsers are installed
    if python3 -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); p.chromium.launch(); p.stop()" >/dev/null 2>&1; then
        print_success "Playwright browsers are installed"
    else
        print_error "Playwright browsers not installed (run: playwright install)"
        errors=$((errors + 1))
    fi
    
    # Check required files
    echo
    print_info "Checking required files..."
    check_file "migrate.py" || errors=$((errors + 1))
    check_file "deploy-client.sh" || errors=$((errors + 1))
    check_file "import.py" || errors=$((errors + 1))
    check_file "wp-migration-orchestrator.sh" || errors=$((errors + 1))
    
    # Check templates directory
    echo
    print_info "Checking template files..."
    check_directory "templates" || errors=$((errors + 1))
    
    if [ -d "templates" ]; then
        check_file "templates/wp-configmap.yaml" || errors=$((errors + 1))
        check_file "templates/wp-secret.yaml" || errors=$((errors + 1))
        check_file "templates/mysql-service.yaml" || errors=$((errors + 1))
        check_file "templates/mysql-statefulset.yaml" || errors=$((errors + 1))
        check_file "templates/wordpress-deployment.yaml" || errors=$((errors + 1))
        check_file "templates/wp-service.yaml" || errors=$((errors + 1))
    fi
    
    # Check Kubernetes connectivity
    echo
    print_info "Checking Kubernetes connectivity..."
    if kubectl cluster-info >/dev/null 2>&1; then
        print_success "Kubernetes cluster is accessible"
        
        # Get cluster info
        local nodes=$(kubectl get nodes --no-headers 2>/dev/null | wc -l)
        print_info "Cluster has $nodes node(s)"
        
        # Check if we can create/list namespaces
        if kubectl auth can-i create namespaces >/dev/null 2>&1; then
            print_success "Can create namespaces"
        else
            print_warning "Cannot create namespaces - may need cluster admin rights"
        fi
    else
        print_error "Cannot connect to Kubernetes cluster"
        errors=$((errors + 1))
    fi
    
    # Summary
    echo
    print_header "Prerequisites Check Summary"
    
    if [ $errors -eq 0 ]; then
        print_success "All prerequisites are met! ✨"
        echo
        print_info "You can now run the migration orchestrator:"
        print_info "./wp-migration-orchestrator.sh"
        echo
        return 0
    else
        print_error "Found $errors issue(s) that need to be resolved"
        echo
        print_info "Common fixes:"
        print_info "• Install Python packages: pip install playwright"
        print_info "• Install browsers: playwright install"
        print_info "• Configure kubectl: kubectl config view"
        print_info "• Check file permissions: chmod +x *.sh"
        echo
        return 1
    fi
}

if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    main "$@"
fi