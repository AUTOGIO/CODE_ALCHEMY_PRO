#!/bin/bash

# CODE_ALCHEMY Professional - N8N Setup Script
# Phase 3: N8N Workflows Implementation

set -e

echo "🚀 CODE_ALCHEMY Professional - N8N Setup"
echo "=========================================="

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

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    print_warning "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon
    if [[ $(uname -m) == "arm64" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    print_success "Homebrew already installed"
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_status "Installing Node.js..."
    brew install node
else
    print_success "Node.js already installed: $(node --version)"
fi

# Check if npm is available
if ! command -v npm &> /dev/null; then
    print_error "npm not found. Please install Node.js properly."
    exit 1
fi

print_success "npm available: $(npm --version)"

# Install N8N globally
print_status "Installing N8N globally..."
npm install -g n8n

# Verify N8N installation
if ! command -v n8n &> /dev/null; then
    print_error "N8N installation failed"
    exit 1
fi

print_success "N8N installed successfully: $(n8n --version)"

# Create N8N configuration directory
N8N_CONFIG_DIR="$HOME/.n8n"
print_status "Creating N8N configuration directory: $N8N_CONFIG_DIR"
mkdir -p "$N8N_CONFIG_DIR"

# Create N8N configuration file
print_status "Creating N8N configuration file..."
cat > "$N8N_CONFIG_DIR/.env" << EOF
# CODE_ALCHEMY Professional - N8N Configuration
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=codealchemy2025
N8N_HOST=localhost
N8N_PORT=5678
N8N_PROTOCOL=http
N8N_USER_MANAGEMENT_DISABLED=false
N8N_EMAIL_MODE=smtp
N8N_LOG_LEVEL=info
N8N_LOG_OUTPUT=console
N8N_TIMEZONE=UTC

# Database configuration (SQLite for local development)
DB_TYPE=sqlite
DB_SQLITE_DATABASE="$N8N_CONFIG_DIR/database.sqlite"

# Security settings
N8N_SECURE_COOKIE=false
N8N_SESSION_COOKIE_SECURE=false

# Webhook settings
N8N_WEBHOOK_URL=http://localhost:5678
N8N_WEBHOOK_TEST_URL=http://localhost:5678

# CODE_ALCHEMY Integration settings
CODEALCHEMY_API_URL=http://localhost:8000
CODEALCHEMY_API_KEY=sk_codealchemy_n8n_2025
EOF

print_success "N8N configuration file created"

# Create N8N startup script
N8N_STARTUP_SCRIPT="$HOME/start_n8n.sh"
print_status "Creating N8N startup script: $N8N_STARTUP_SCRIPT"
cat > "$N8N_STARTUP_SCRIPT" << 'EOF'
#!/bin/bash

# CODE_ALCHEMY Professional - N8N Startup Script

echo "🚀 Starting N8N for CODE_ALCHEMY Professional..."
echo "================================================"

# Check if N8N is already running
if pgrep -f "n8n" > /dev/null; then
    echo "⚠️  N8N is already running"
    echo "   Access at: http://localhost:5678"
    echo "   Username: admin"
    echo "   Password: codealchemy2025"
    exit 0
fi

# Start N8N
echo "🔧 Starting N8N instance..."
n8n start

echo "✅ N8N started successfully!"
echo "🌐 Access your N8N instance at: http://localhost:5678"
echo "🔑 Login credentials:"
echo "   Username: admin"
echo "   Password: codealchemy2025"
echo ""
echo "📋 Next steps:"
echo "   1. Import workflow templates from data/n8n/templates/"
echo "   2. Configure webhook endpoints"
echo "   3. Test integration with CODE_ALCHEMY_PRO"
EOF

chmod +x "$N8N_STARTUP_SCRIPT"
print_success "N8N startup script created and made executable"

# Create N8N service file for launchd (macOS)
LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"
LAUNCH_AGENT_FILE="$LAUNCH_AGENT_DIR/com.codealchemy.n8n.plist"

print_status "Creating macOS launch agent for N8N..."
mkdir -p "$LAUNCH_AGENT_DIR"

cat > "$LAUNCH_AGENT_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.codealchemy.n8n</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/n8n</string>
        <string>start</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$HOME/.n8n/n8n.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/.n8n/n8n-error.log</string>
    <key>WorkingDirectory</key>
    <string>$HOME/.n8n</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
EOF

print_success "macOS launch agent created"

# Create N8N workflow import script
IMPORT_SCRIPT="$HOME/import_n8n_workflows.sh"
print_status "Creating workflow import script: $IMPORT_SCRIPT"
cat > "$IMPORT_SCRIPT" << 'EOF'
#!/bin/bash

# CODE_ALCHEMY Professional - N8N Workflow Import Script

echo "📥 Importing N8N Workflow Templates"
echo "===================================="

# Get the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATES_DIR="$PROJECT_DIR/data/n8n/templates"

if [ ! -d "$TEMPLATES_DIR" ]; then
    echo "❌ Templates directory not found: $TEMPLATES_DIR"
    exit 1
fi

echo "🔍 Found templates in: $TEMPLATES_DIR"

# Check if N8N is running
if ! pgrep -f "n8n" > /dev/null; then
    echo "⚠️  N8N is not running. Please start N8N first:"
    echo "   ./start_n8n.sh"
    exit 1
fi

echo "✅ N8N is running"

# List available templates
echo ""
echo "📋 Available workflow templates:"
ls -la "$TEMPLATES_DIR"/*.json | while read -r file; do
    filename=$(basename "$file")
    echo "   📄 $filename"
done

echo ""
echo "📚 To import these workflows:"
echo "   1. Open N8N at: http://localhost:5678"
echo "   2. Login with admin/codealchemy2025"
echo "   3. Go to Workflows → Import from File"
echo "   4. Select each .json file from: $TEMPLATES_DIR"
echo ""
echo "🔗 Or use the N8N API to import programmatically:"
echo "   curl -X POST http://localhost:5678/api/v1/workflows/import \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d @$TEMPLATES_DIR/filename.json"
EOF

chmod +x "$IMPORT_SCRIPT"
print_success "Workflow import script created"

# Create N8N health check script
HEALTH_SCRIPT="$HOME/check_n8n_health.sh"
print_status "Creating N8N health check script: $HEALTH_SCRIPT"
cat > "$HEALTH_SCRIPT" << 'EOF'
#!/bin/bash

# CODE_ALCHEMY Professional - N8N Health Check Script

echo "🏥 N8N Health Check"
echo "==================="

# Check if N8N process is running
if pgrep -f "n8n" > /dev/null; then
    echo "✅ N8N process is running"
    N8N_PID=$(pgrep -f "n8n")
    echo "   Process ID: $N8N_PID"
else
    echo "❌ N8N process is not running"
    exit 1
fi

# Check if N8N web interface is accessible
echo "🌐 Checking N8N web interface..."
if curl -s http://localhost:5678 > /dev/null; then
    echo "✅ N8N web interface is accessible"
    echo "   URL: http://localhost:5678"
else
    echo "❌ N8N web interface is not accessible"
    echo "   Check if N8N is fully started"
fi

# Check N8N logs
echo "📋 Checking N8N logs..."
LOG_FILE="$HOME/.n8n/n8n.log"
if [ -f "$LOG_FILE" ]; then
    echo "✅ N8N log file exists: $LOG_FILE"
    echo "   Last 5 lines:"
    tail -5 "$LOG_FILE" | sed 's/^/   /'
else
    echo "⚠️  N8N log file not found: $LOG_FILE"
fi

# Check N8N configuration
echo "⚙️  Checking N8N configuration..."
CONFIG_FILE="$HOME/.n8n/.env"
if [ -f "$CONFIG_FILE" ]; then
    echo "✅ N8N config file exists: $CONFIG_FILE"
    echo "   Configuration summary:"
    grep -E "^(N8N_HOST|N8N_PORT|N8N_BASIC_AUTH_USER)" "$CONFIG_FILE" | sed 's/^/   /'
else
    echo "❌ N8N config file not found: $CONFIG_FILE"
fi

echo ""
echo "🎯 N8N Health Check Complete!"
EOF

chmod +x "$HEALTH_SCRIPT"
print_success "Health check script created"

# Create integration test script
INTEGRATION_TEST_SCRIPT="$HOME/test_n8n_integration.sh"
print_status "Creating integration test script: $INTEGRATION_TEST_SCRIPT"
cat > "$INTEGRATION_TEST_SCRIPT" << 'EOF'
#!/bin/bash

# CODE_ALCHEMY Professional - N8N Integration Test Script

echo "🧪 Testing N8N Integration with CODE_ALCHEMY_PRO"
echo "================================================"

# Check if CODE_ALCHEMY_PRO API is running
echo "🔍 Checking CODE_ALCHEMY_PRO API..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ CODE_ALCHEMY_PRO API is running"
else
    echo "❌ CODE_ALCHEMY_PRO API is not running"
    echo "   Please start the API first: python3 launch_n8n_integration.py"
    exit 1
fi

# Check if N8N is running
echo "🔍 Checking N8N..."
if curl -s http://localhost:5678 > /dev/null; then
    echo "✅ N8N is running"
else
    echo "❌ N8N is not running"
    echo "   Please start N8N first: ./start_n8n.sh"
    exit 1
fi

# Test webhook endpoints
echo ""
echo "🌐 Testing webhook endpoints..."

# Test file organization webhook
echo "📁 Testing file organization webhook..."
RESPONSE=$(curl -s -X POST http://localhost:8000/webhook/file-organization \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk_codealchemy_n8n_2025" \
  -d '{"operation": "process_documents", "test": true}')

if echo "$RESPONSE" | grep -q "success"; then
    echo "✅ File organization webhook working"
else
    echo "❌ File organization webhook failed: $RESPONSE"
fi

# Test system alert webhook
echo "🚨 Testing system alert webhook..."
RESPONSE=$(curl -s -X POST http://localhost:8000/webhook/system-alert \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk_codealchemy_n8n_2025" \
  -d '{"type": "test_alert", "message": "Integration test"}')

if echo "$RESPONSE" | grep -q "success"; then
    echo "✅ System alert webhook working"
else
    echo "❌ System alert webhook failed: $RESPONSE"
fi

echo ""
echo "🎯 Integration Test Complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Import workflow templates in N8N"
echo "   2. Configure webhook URLs in workflows"
echo "   3. Test end-to-end automation"
EOF

chmod +x "$INTEGRATION_TEST_SCRIPT"
print_success "Integration test script created"

# Final setup summary
echo ""
echo "🎉 N8N Setup Complete!"
echo "======================"
echo ""
echo "📁 Files created:"
echo "   • N8N config: $N8N_CONFIG_DIR/.env"
echo "   • Startup script: $N8N_STARTUP_SCRIPT"
echo "   • Launch agent: $LAUNCH_AGENT_FILE"
echo "   • Import script: $IMPORT_SCRIPT"
echo "   • Health check: $HEALTH_SCRIPT"
echo "   • Integration test: $INTEGRATION_TEST_SCRIPT"
echo ""
echo "🚀 To start N8N:"
echo "   ./start_n8n.sh"
echo ""
echo "🔍 To check N8N health:"
echo "   ./check_n8n_health.sh"
echo ""
echo "📥 To import workflows:"
echo "   ./import_n8n_workflows.sh"
echo ""
echo "🧪 To test integration:"
echo "   ./test_n8n_integration.sh"
echo ""
echo "🌐 N8N will be available at: http://localhost:5678"
echo "   Username: admin"
echo "   Password: codealchemy2025"
echo ""
echo "📚 Workflow templates available in: data/n8n/templates/"
print_success "Phase 3: N8N Workflows setup complete!"
