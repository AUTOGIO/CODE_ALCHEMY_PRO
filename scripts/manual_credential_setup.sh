#!/bin/bash

# CODE_ALCHEMY Professional - N8N Manual Credential Setup Guide
# Interactive script to guide users through manual credential setup

set -e

echo "📋 CODE_ALCHEMY Professional - N8N Manual Credential Setup"
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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

print_step() {
    echo -e "${CYAN}[STEP]${NC} $1"
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

echo ""
echo "🔐 Manual Credential Setup Instructions"
echo "======================================"
echo ""
echo "Since automated import requires additional n8n configuration,"
echo "we'll guide you through the manual setup process."
echo ""

# Display credential information
echo "📋 Credential Details to Create:"
echo "================================"
echo ""

# Display CODE_ALCHEMY API credentials
echo "🔑 1. CODE_ALCHEMY API"
echo "   Type: HTTP Header Auth"
echo "   Name: CODE_ALCHEMY API"
echo "   Header Name: Authorization"
echo "   Header Value: Bearer sk_codealchemy_n8n_2025"
echo ""

# Display webhook credentials
echo "🔑 2. CODE_ALCHEMY Webhook"
echo "   Type: HTTP Header Auth"
echo "   Name: CODE_ALCHEMY Webhook"
echo "   Header Name: Authorization"
echo "   Header Value: Bearer sk_codealchemy_n8n_2025"
echo ""

# Display system credentials
echo "🔑 3. CODE_ALCHEMY System"
echo "   Type: HTTP Header Auth"
echo "   Name: CODE_ALCHEMY System"
echo "   Header Name: Authorization"
echo "   Header Value: Bearer sk_codealchemy_n8n_2025"
echo ""

# Step-by-step instructions
echo "📚 Step-by-Step Setup Instructions"
echo "=================================="
echo ""

print_step "1. Open N8N in your web browser"
echo "   URL: http://localhost:5678"
echo "   Username: admin"
echo "   Password: codealchemy2025"
echo ""

print_step "2. Navigate to Credentials"
echo "   • Click on 'Settings' in the left sidebar"
echo "   • Select 'Credentials' from the settings menu"
echo "   • Click 'Add Credential'"
echo ""

print_step "3. Create CODE_ALCHEMY API Credential"
echo "   • Select 'HTTP Header Auth' from credential types"
echo "   • Name: CODE_ALCHEMY API"
echo "   • Header Name: Authorization"
echo "   • Header Value: Bearer sk_codealchemy_n8n_2025"
echo "   • Click 'Save'"
echo ""

print_step "4. Create CODE_ALCHEMY Webhook Credential"
echo "   • Click 'Add Credential' again"
echo "   • Select 'HTTP Header Auth'"
echo "   • Name: CODE_ALCHEMY Webhook"
echo "   • Header Name: Authorization"
echo "   • Header Value: Bearer sk_codealchemy_n8n_2025"
echo "   • Click 'Save'"
echo ""

print_step "5. Create CODE_ALCHEMY System Credential"
echo "   • Click 'Add Credential' again"
echo "   • Select 'HTTP Header Auth'"
echo "   • Name: CODE_ALCHEMY System"
echo "   • Header Name: Authorization"
echo "   • Header Value: Bearer sk_codealchemy_n8n_2025"
echo "   • Click 'Save'"
echo ""

# Verification instructions
echo "🔍 Verification Steps"
echo "===================="
echo ""

print_step "6. Verify Credentials"
echo "   • In the Credentials section, you should see:"
echo "     - CODE_ALCHEMY API"
echo "     - CODE_ALCHEMY Webhook"
echo "     - CODE_ALCHEMY System"
echo ""

print_step "7. Test Integration"
echo "   • Run the verification script:"
echo "     ~/verify_n8n_credentials.sh"
echo ""

# Alternative methods
echo "🔄 Alternative Setup Methods"
echo "============================"
echo ""

echo "📥 Option A: Import Workflow Templates First"
echo "   • Go to Workflows → Import from File"
echo "   • Import templates from: data/n8n/templates/"
echo "   • The workflows will reference the credentials you create"
echo ""

echo "🔧 Option B: Enable API Key Authentication"
echo "   • Add N8N_API_KEY=your_api_key to n8n environment"
echo "   • Restart n8n"
echo "   • Use the automated import script"
echo ""

# Interactive verification
echo ""
echo "🤔 Ready to proceed?"
echo "==================="
echo ""
echo "1. Open N8N at: http://localhost:5678"
echo "2. Follow the step-by-step instructions above"
echo "3. Create all three credentials"
echo "4. Run verification when complete"
echo ""

read -p "Press Enter when you're ready to start, or 'q' to quit: " user_input

if [[ "$user_input" == "q" || "$user_input" == "Q" ]]; then
    echo ""
    print_warning "Setup cancelled. You can run this script again later."
    exit 0
fi

echo ""
print_status "Great! Let's get started with the manual setup."
echo ""

# Open N8N in default browser
print_step "Opening N8N in your default browser..."
open http://localhost:5678

echo ""
echo "🌐 N8N should now be open in your browser."
echo ""

# Wait for user to complete setup
echo "⏳ Please complete the credential setup in N8N:"
echo "   1. Login with admin/codealchemy2025"
echo "   2. Go to Settings → Credentials"
echo "   3. Create all three credentials as shown above"
echo ""

read -p "Press Enter when you've completed the credential setup: " user_input

echo ""
print_status "Let's verify that the credentials were created successfully."
echo ""

# Run verification
print_step "Running credential verification..."
if [ -f "$HOME/verify_n8n_credentials.sh" ]; then
    ~/verify_n8n_credentials.sh
else
    print_warning "Verification script not found. Please run it manually:"
    echo "   ~/verify_n8n_credentials.sh"
fi

echo ""
echo "🎯 Next Steps After Credential Setup"
echo "===================================="
echo ""

print_step "1. Import Workflow Templates"
echo "   • Go to Workflows → Import from File"
echo "   • Import from: data/n8n/templates/"
echo "   • Available templates:"
ls -la data/n8n/templates/*.json | while read -r file; do
    filename=$(basename "$file")
    echo "     📄 $filename"
done

echo ""
print_step "2. Test Workflows"
echo "   • Activate the imported workflows"
echo "   • Test webhook endpoints"
echo "   • Monitor execution logs"
echo ""

print_step "3. Configure Integration"
echo "   • Set up webhook URLs in workflows"
echo "   • Test end-to-end automation"
echo "   • Monitor system performance"
echo ""

echo ""
print_success "Manual credential setup guide complete!"
echo ""
echo "📚 For detailed documentation, see:"
echo "   docs/N8N_CREDENTIALS_SETUP.md"
echo ""
echo "🔍 For troubleshooting, run:"
echo "   ~/verify_n8n_credentials.sh"
echo ""
echo "🚀 Happy automating with CODE_ALCHEMY Professional!"
