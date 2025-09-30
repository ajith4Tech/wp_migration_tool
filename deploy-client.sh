#!/bin/bash
# A script to deploy an isolated WordPress stack to a new client namespace.
# It reads required variables and substitutes them into YAML templates before applying.

# Exit immediately if a command exits with a non-zero status
set -e

# --- 1. CONFIGURATION ---
TEMPLATE_DIR="templates"
YAML_FILES=(
    "wp-configmap.yaml"
    "wp-secret.yaml"
    "mysql-service.yaml"
    "mysql-statefulset.yaml"
    "wordpress-deployment.yaml"  # Updated name from wordpress-deployment-and-pvc.yaml
    "wp-service.yaml"
)

# Check if the templates directory exists
if [ ! -d "$TEMPLATE_DIR" ]; then
    echo "Error: Template directory '$TEMPLATE_DIR' not found." >&2
    echo "Please ensure your generalized YAML files are in a folder named 'templates/'." >&2
    exit 1
fi

# --- 2. GATHER USER INPUT ---

echo "--- Client WordPress Deployment Setup ---"
echo "This script will deploy an isolated stack to a new Kubernetes Namespace."
echo " "

# Function to get required input
get_input() {
    local prompt_text="$1"
    local var_name="$2"
    local input
    
    while true; do
        read -p "$prompt_text" input
        if [ -z "$input" ]; then
            echo "Input cannot be empty. Please try again." >&2
        else
            eval "$var_name=\"$input\""
            break
        fi
    done
}

# Gather all 5 required variables
get_input "1. Enter Client Namespace (e.g., client-a): " CLIENT_NAMESPACE
get_input "2. Enter DB Name (e.g., client_a_wp_db): " DB_NAME
get_input "3. Enter DB User (e.g., wp_client_a_user): " DB_USER
get_input "4. Enter WP DB Password: " WP_DB_PASS
get_input "5. Enter MySQL ROOT Password: " ROOT_PASS

echo "----------------------------------------"
echo "Target Namespace: $CLIENT_NAMESPACE"
echo "----------------------------------------"

# --- 3. CORE DEPLOYMENT FUNCTION ---

deploy_file() {
    local FILE=$1
    echo "  -> Applying $FILE..."
    
    # Use sed to perform substitution of all five variables on the fly
    # and pipe the result directly to kubectl apply.
    sed \
        -e "s/{{ CLIENT_NAMESPACE }}/$CLIENT_NAMESPACE/g" \
        -e "s/{{ DB_NAME }}/$DB_NAME/g" \
        -e "s/{{ DB_USER }}/$DB_USER/g" \
        -e "s/{{ WP_DB_PASS }}/$WP_DB_PASS/g" \
        -e "s/{{ ROOT_PASS }}/$ROOT_PASS/g" \
        "$TEMPLATE_DIR/$FILE" | kubectl apply -f -
}

# --- 4. EXECUTION ---

# Create the Namespace (The "|| true" prevents the script from stopping if the namespace already exists)
echo "Creating Namespace '$CLIENT_NAMESPACE'..."
kubectl create namespace "$CLIENT_NAMESPACE" || true

# Loop through the list of files and deploy each one
for FILE in "${YAML_FILES[@]}"; do
    deploy_file "$FILE"
done

# --- 5. CONCLUSION ---
echo " "
echo "✅ Deployment for client '$CLIENT_NAMESPACE' is complete!"
echo "Verify status with: kubectl get pods -n $CLIENT_NAMESPACE"