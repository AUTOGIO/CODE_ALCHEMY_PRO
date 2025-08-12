#!/bin/bash

# CODE_ALCHEMY Professional - N8N Credentials Setup Script
# Creates and configures all necessary credentials for n8n workflows

set -e

echo "🔐 CODE_ALCHEMY Professional - N8N Credentials Setup"
echo "===================================================="

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

# Create credentials directory
CREDENTIALS_DIR="$HOME/.n8n/credentials"
mkdir -p "$CREDENTIALS_DIR"

print_status "Creating N8N credentials..."

# Create CODE_ALCHEMY API credentials
cat > "$CREDENTIALS_DIR/n8n-api-credentials.json" << 'EOF'
{
  "id": "n8n-api-credentials",
  "name": "CODE_ALCHEMY API",
  "type": "httpHeaderAuth",
  "data": {
    "name": "CODE_ALCHEMY API",
    "httpHeaderAuth": {
      "name": "CODE_ALCHEMY API",
      "value": "Bearer sk_codealchemy_n8n_2025"
    }
  },
  "createdAt": "2025-01-28T00:00:00.000Z",
  "updatedAt": "2025-01-28T00:00:00.000Z"
}
EOF

print_success "Created CODE_ALCHEMY API credentials"

# Create webhook credentials
cat > "$CREDENTIALS_DIR/n8n-webhook-credentials.json" << 'EOF'
{
  "id": "n8n-webhook-credentials",
  "name": "CODE_ALCHEMY Webhook",
  "type": "httpHeaderAuth",
  "data": {
    "name": "CODE_ALCHEMY Webhook",
    "httpHeaderAuth": {
      "name": "CODE_ALCHEMY Webhook",
      "value": "Bearer sk_codealchemy_n8n_2025"
    }
  },
  "createdAt": "2025-01-28T00:00:00.000Z",
  "updatedAt": "2025-01-28T00:00:00.000Z"
}
EOF

print_success "Created webhook credentials"

# Create system integration credentials
cat > "$CREDENTIALS_DIR/n8n-system-credentials.json" << 'EOF'
{
  "id": "n8n-system-credentials",
  "name": "CODE_ALCHEMY System",
  "type": "httpHeaderAuth",
  "data": {
    "name": "CODE_ALCHEMY System",
    "httpHeaderAuth": {
      "name": "CODE_ALCHEMY System",
      "value": "Bearer sk_codealchemy_n8n_2025"
    }
  },
  "createdAt": "2025-01-28T00:00:00.000Z",
  "updatedAt": "2025-01-28T00:00:00.000Z"
}
EOF

print_success "Created system integration credentials"

# Create credential import script
IMPORT_CREDENTIALS_SCRIPT="$HOME/import_n8n_credentials.sh"
print_status "Creating credential import script: $IMPORT_CREDENTIALS_SCRIPT"

cat > "$IMPORT_CREDENTIALS_SCRIPT" << 'EOF'
#!/bin/bash

# CODE_ALCHEMY Professional - N8N Credentials Import Script

echo "📥 Importing N8N Credentials"
echo "============================="

# Get the credentials directory
CREDENTIALS_DIR="$HOME/.n8n/credentials"

if [ ! -d "$CREDENTIALS_DIR" ]; then
    echo "❌ Credentials directory not found: $CREDENTIALS_DIR"
    exit 1
fi

echo "🔍 Found credentials in: $CREDENTIALS_DIR"

# Check if N8N is running
if ! pgrep -f "n8n" > /dev/null; then
    echo "⚠️  N8N is not running. Please start N8N first:"
    echo "   ./start_n8n.sh"
    exit 1
fi

echo "✅ N8N is running"

# List available credentials
echo ""
echo "📋 Available credentials:"
ls -la "$CREDENTIALS_DIR"/*.json | while read -r file; do
    filename=$(basename "$file")
    echo "   🔐 $filename"
done

echo ""
echo "📚 To import these credentials:"
echo "   1. Open N8N at: http://localhost:5678"
echo "   2. Login with admin/codealchemy2025"
echo "   3. Go to Settings → Credentials"
echo "   4. Click 'Add Credential'"
echo "   5. Select 'HTTP Header Auth'"
echo "   6. Use the following details:"
echo ""
echo "   🔑 CODE_ALCHEMY API:"
echo "      Name: CODE_ALCHEMY API"
echo "      Header Name: Authorization"
echo "      Header Value: Bearer sk_codealchemy_n8n_2025"
echo ""
echo "   🔑 CODE_ALCHEMY Webhook:"
echo "      Name: CODE_ALCHEMY Webhook"
echo "      Header Name: Authorization"
echo "      Header Value: Bearer sk_codealchemy_n8n_2025"
echo ""
echo "   🔑 CODE_ALCHEMY System:"
echo "      Name: CODE_ALCHEMY System"
echo "      Header Name: Authorization"
echo "      Header Value: Bearer sk_codealchemy_n8n_2025"
echo ""
echo "🔗 Or use the N8N API to import programmatically:"
echo "   curl -X POST http://localhost:5678/api/v1/credentials \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -H 'Authorization: Basic YWRtaW46Y29kZWFsY2hlbXkyMDI1' \\"
echo "     -d @$CREDENTIALS_DIR/filename.json"
EOF

chmod +x "$IMPORT_CREDENTIALS_SCRIPT"
print_success "Credential import script created"

# Create credential verification script
VERIFY_CREDENTIALS_SCRIPT="$HOME/verify_n8n_credentials.sh"
print_status "Creating credential verification script: $VERIFY_CREDENTIALS_SCRIPT"

cat > "$VERIFY_CREDENTIALS_SCRIPT" << 'EOF'
#!/bin/bash

# CODE_ALCHEMY Professional - N8N Credentials Verification Script

echo "🔍 Verifying N8N Credentials"
echo "============================="

# Check if N8N is running
if ! pgrep -f "n8n" > /dev/null; then
    echo "❌ N8N is not running"
    exit 1
fi

echo "✅ N8N is running"

# Check credentials directory
CREDENTIALS_DIR="$HOME/.n8n/credentials"
if [ -d "$CREDENTIALS_DIR" ]; then
    echo "✅ Credentials directory exists: $CREDENTIALS_DIR"
    echo "   Available credentials:"
    ls -la "$CREDENTIALS_DIR"/*.json | while read -r file; do
        filename=$(basename "$file")
        echo "   🔐 $filename"
    done
else
    echo "❌ Credentials directory not found: $CREDENTIALS_DIR"
fi

# Test API connectivity
echo ""
echo "🌐 Testing API connectivity..."

# Test CODE_ALCHEMY API
echo "🔍 Testing CODE_ALCHEMY API..."
if curl -s -H "Authorization: Bearer sk_codealchemy_n8n_2025" http://localhost:8000/health > /dev/null; then
    echo "✅ CODE_ALCHEMY API is accessible"
else
    echo "❌ CODE_ALCHEMY API is not accessible"
fi

# Test webhook endpoints
echo "🔍 Testing webhook endpoints..."
if curl -s -H "Authorization: Bearer sk_codealchemy_n8n_2025" http://localhost:8000/webhook/results > /dev/null; then
    echo "✅ Webhook endpoints are accessible"
else
    echo "❌ Webhook endpoints are not accessible"
fi

echo ""
echo "🎯 Credential verification complete!"
EOF

chmod +x "$VERIFY_CREDENTIALS_SCRIPT"
print_success "Credential verification script created"

# Final setup summary
echo ""
echo "🎉 N8N Credentials Setup Complete!"
echo "=================================="
echo ""
echo "📁 Files created:"
echo "   • Credentials directory: $CREDENTIALS_DIR"
echo "   • CODE_ALCHEMY API credentials: $CREDENTIALS_DIR/n8n-api-credentials.json"
echo "   • Webhook credentials: $CREDENTIALS_DIR/n8n-webhook-credentials.json"
echo "   • System credentials: $CREDENTIALS_DIR/n8n-system-credentials.json"
echo "   • Import script: $IMPORT_CREDENTIALS_SCRIPT"
echo "   • Verification script: $VERIFY_CREDENTIALS_SCRIPT"
echo ""
echo "🔐 Credentials created:"
echo "   • CODE_ALCHEMY API (HTTP Header Auth)"
echo "   • CODE_ALCHEMY Webhook (HTTP Header Auth)"
echo "   • CODE_ALCHEMY System (HTTP Header Auth)"
echo ""
echo "📥 To import credentials manually:"
echo "   ./import_n8n_credentials.sh"
echo ""
echo "🔍 To verify credentials:"
echo "   ./verify_n8n_credentials.sh"
echo ""
echo "🌐 Access N8N at: http://localhost:5678"
echo "   Username: admin"
echo "   Password: codealchemy2025"
echo ""
print_success "N8N Credentials setup complete!"
