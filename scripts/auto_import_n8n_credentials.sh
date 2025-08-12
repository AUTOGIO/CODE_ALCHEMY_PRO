#!/bin/bash

# CODE_ALCHEMY Professional - N8N Auto-Credential Import Script
# Automatically imports credentials into n8n using the API

set -e

echo "🤖 CODE_ALCHEMY Professional - N8N Auto-Credential Import"
echo "========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS. Please run on a Mac system."
    exit 1
fi

print_status "Detected macOS system"

# Check if N8N is running
if ! pgrep -f "n8n" > /dev/null; then
    print_error "N8N is not running. Please start N8N first:"
    echo "   ./start_n8n.sh"
    exit 1
fi

print_success "N8N is running"

# Wait for N8N to be fully ready
print_status "Waiting for N8N to be fully ready..."
sleep 5

# Check if N8N web interface is accessible
if ! curl -s http://localhost:5678 > /dev/null; then
    print_error "N8N web interface is not accessible. Please wait for N8N to fully start."
    exit 1
fi

print_success "N8N web interface is accessible"

# Check if credentials directory exists
CREDENTIALS_DIR="$HOME/.n8n/credentials"
if [ ! -d "$CREDENTIALS_DIR" ]; then
    print_error "Credentials directory not found: $CREDENTIALS_DIR"
    echo "Please run the setup script first: ./scripts/setup_n8n_credentials.sh"
    exit 1
fi

print_success "Credentials directory found: $CREDENTIALS_DIR"

# Function to import credential
import_credential() {
    local credential_file="$1"
    local credential_name="$2"
    
    print_status "Importing $credential_name..."
    
    # Check if credential file exists
    if [ ! -f "$credential_file" ]; then
        print_error "Credential file not found: $credential_file"
        return 1
    fi
    
    # Import credential via n8n API
    local response=$(curl -s -X POST http://localhost:5678/api/v1/credentials \
        -H 'Content-Type: application/json' \
        -H 'Authorization: Basic YWRtaW46Y29kZWFsY2hlbXkyMDI1' \
        -d @"$credential_file" \
        -w "%{http_code}")
    
    local http_code="${response: -3}"
    local response_body="${response%???}"
    
    if [ "$http_code" = "200" ] || [ "$http_code" = "201" ]; then
        print_success "Successfully imported $credential_name"
        return 0
    else
        print_error "Failed to import $credential_name (HTTP $http_code)"
        echo "Response: $response_body"
        return 1
    fi
}

# Import all credentials
print_status "Starting credential import process..."

# Import CODE_ALCHEMY API credentials
if import_credential "$CREDENTIALS_DIR/n8n-api-credentials.json" "CODE_ALCHEMY API"; then
    API_IMPORTED=true
else
    API_IMPORTED=false
fi

# Import webhook credentials
if import_credential "$CREDENTIALS_DIR/n8n-webhook-credentials.json" "CODE_ALCHEMY Webhook"; then
    WEBHOOK_IMPORTED=true
else
    WEBHOOK_IMPORTED=false
fi

# Import system credentials
if import_credential "$CREDENTIALS_DIR/n8n-system-credentials.json" "CODE_ALCHEMY System"; then
    SYSTEM_IMPORTED=true
else
    SYSTEM_IMPORTED=false
fi

# Summary of import results
echo ""
echo "📊 Credential Import Summary"
echo "============================"

if [ "$API_IMPORTED" = true ]; then
    echo "✅ CODE_ALCHEMY API: Imported successfully"
else
    echo "❌ CODE_ALCHEMY API: Import failed"
fi

if [ "$WEBHOOK_IMPORTED" = true ]; then
    echo "✅ CODE_ALCHEMY Webhook: Imported successfully"
else
    echo "❌ CODE_ALCHEMY Webhook: Import failed"
fi

if [ "$SYSTEM_IMPORTED" = true ]; then
    echo "✅ CODE_ALCHEMY System: Imported successfully"
else
    echo "❌ CODE_ALCHEMY System: Import failed"
fi

# Check if all credentials were imported successfully
if [ "$API_IMPORTED" = true ] && [ "$WEBHOOK_IMPORTED" = true ] && [ "$SYSTEM_IMPORTED" = true ]; then
    echo ""
    print_success "All credentials imported successfully!"
    
    # Verify credentials in n8n
    echo ""
    print_status "Verifying credentials in n8n..."
    
    # List all credentials via API
    credentials_response=$(curl -s -X GET http://localhost:5678/api/v1/credentials \
        -H 'Authorization: Basic YWRtaW46Y29kZWFsY2hlbXkyMDI1')
    
    if echo "$credentials_response" | grep -q "CODE_ALCHEMY"; then
        print_success "Credentials verified in n8n"
        echo ""
        echo "🔐 Available credentials in n8n:"
        echo "$credentials_response" | jq -r '.data[] | "   • \(.name) (\(.type))"' 2>/dev/null || echo "   • Credentials found (JSON parsing not available)"
    else
        print_warning "Could not verify credentials in n8n API response"
    fi
    
else
    echo ""
    print_warning "Some credentials failed to import. Please check the errors above."
    echo ""
    echo "📚 Manual import instructions:"
    echo "   1. Open N8N at: http://localhost:5678"
    echo "   2. Login with admin/codealchemy2025"
    echo "   3. Go to Settings → Credentials"
    echo "   4. Add each credential manually"
fi

# Final instructions
echo ""
echo "🎯 Next Steps"
echo "============="
echo "1. Open N8N at: http://localhost:5678"
echo "2. Go to Settings → Credentials to verify"
echo "3. Import workflow templates from data/n8n/templates/"
echo "4. Test the integration with your workflows"
echo ""
echo "🔍 To verify everything is working:"
echo "   ~/verify_n8n_credentials.sh"
echo ""
echo "📚 For detailed setup instructions, see:"
echo "   docs/N8N_CREDENTIALS_SETUP.md"

if [ "$API_IMPORTED" = true ] && [ "$WEBHOOK_IMPORTED" = true ] && [ "$SYSTEM_IMPORTED" = true ]; then
    print_success "Auto-credential import complete!"
    exit 0
else
    print_warning "Auto-credential import completed with some failures"
    exit 1
fi
