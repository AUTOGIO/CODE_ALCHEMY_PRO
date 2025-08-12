#!/bin/bash

# local-llm-n8n-bridge.sh
# macOS automation script to bridge LM Studio OpenAI server with n8n workflows
# Role: DevOps + macOS automation engineer
# Goal: Zero-touch LM Studio server startup + n8n workflow patching

set -euo pipefail

# Configuration (CLI overrides via env vars)
LMSTUDIO_APP_NAME="${LMSTUDIO_APP_NAME:-LM Studio}"
BASE_URL="${BASE_URL:-http://127.0.0.1:1234/v1}"
MODEL_ID="${MODEL_ID:-qwen3-14b-mlx}"
TEMP="${TEMP:-0.2}"
N8N_URL="${N8N_URL:-}"
N8N_TOKEN="${N8N_TOKEN:-}"
N8N_WORKFLOW_ID="${N8N_WORKFLOW_ID:-}"
OPENAI_API_KEY_PLACEHOLDER="${OPENAI_API_KEY_PLACEHOLDER:-lmst-local}"
PATCH_JSON_PATH="${PATCH_JSON_PATH:-$HOME/Desktop/workflow.json}"

# Colors for output
if command -v tput >/dev/null 2>&1; then
    RED=$(tput setaf 1)
    GREEN=$(tput setaf 2)
    YELLOW=$(tput setaf 3)
    BLUE=$(tput setaf 4)
    RESET=$(tput sgr0)
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    RESET=''
fi

# Helper functions
log() {
    echo -e "${BLUE}[$(date +'%H:%M:%S')]${RESET} $1"
}

success() {
    echo -e "${GREEN}✅ $1${RESET}"
}

warn() {
    echo -e "${YELLOW}⚠️  $1${RESET}"
}

error() {
    echo -e "${RED}❌ $1${RESET}"
}

need() {
    local cmd="$1"
    local desc="$2"
    if ! command -v "$cmd" >/dev/null 2>&1; then
        error "Required command '$cmd' not found: $desc"
        exit 1
    fi
}

retry() {
    local max_attempts="$1"
    local delay="$2"
    local cmd="$3"
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if eval "$cmd"; then
            return 0
        fi
        
        if [ $attempt -lt $max_attempts ]; then
            warn "Attempt $attempt failed, retrying in ${delay}s..."
            sleep "$delay"
            delay=$((delay * 2))
        fi
        
        attempt=$((attempt + 1))
    done
    
    return 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    need curl "HTTP client for API calls"
    need jq "JSON processor for API responses"
    need python3 "Python for potential fallback operations"
    
    if [[ "$OSTYPE" != "darwin"* ]]; then
        error "This script requires macOS"
        exit 1
    fi
    
    success "Prerequisites check passed"
}

# Health check for LM Studio server
check_lmstudio_server() {
    log "Checking LM Studio server health..."
    if curl -s --max-time 10 "$BASE_URL/models" >/dev/null 2>&1; then
        success "LM Studio server is already running on $BASE_URL"
        return 0
    fi
    return 1
}

# Start LM Studio and OpenAI server via GUI automation
start_lmstudio_server() {
    log "Starting LM Studio and OpenAI server..."
    
    # Launch LM Studio
    if ! open -a "$LMSTUDIO_APP_NAME" 2>/dev/null; then
        error "Failed to launch $LMSTUDIO_APP_NAME. Please install it first."
        exit 1
    fi
    
    # Wait for app to launch
    sleep 3
    
    # AppleScript to start OpenAI server
    local applescript='
    tell application "System Events"
        tell process "LM Studio"
            -- Bring to front
            set frontmost to true
            delay 1
            
            -- Try to click Developer menu
            try
                click menu item "Developer" of menu bar 1
                delay 0.5
                
                -- Try to click OpenAI Compatible Server submenu
                try
                    click menu item "OpenAI Compatible Server" of menu "Developer" of menu bar 1
                    delay 0.5
                    
                    -- Try to click Start
                    try
                        click menu item "Start" of menu "OpenAI Compatible Server" of menu "Developer" of menu bar 1
                        return "success"
                    on error
                        return "start_menu_not_found"
                    end try
                on error
                    return "openai_menu_not_found"
                end try
            on error
                return "developer_menu_not_found"
            end try
        end tell
    end tell
    '
    
    local result
    result=$(osascript -e "$applescript" 2>/dev/null || echo "script_failed")
    
    case "$result" in
        "success")
            log "OpenAI server start command sent to LM Studio"
            ;;
        "developer_menu_not_found")
            warn "Developer menu not found. Please manually navigate to Developer → OpenAI Compatible Server → Start"
            ;;
        "openai_menu_not_found")
            warn "OpenAI Compatible Server menu not found. Please manually navigate to Developer → OpenAI Compatible Server → Start"
            ;;
        "start_menu_not_found")
            warn "Start menu not found. Please manually navigate to Developer → OpenAI Compatible Server → Start"
            ;;
        *)
            warn "AppleScript execution failed. Please manually start the OpenAI server in LM Studio"
            ;;
    esac
    
    # Wait for server to start with exponential backoff
    log "Waiting for server to start..."
    if retry 6 5 "check_lmstudio_server"; then
        success "LM Studio server is now running"
        return 0
    else
        error "LM Studio server not responding on :1234 (open Developer → OpenAI Compatible Server → Start)"
        exit 1
    fi
}

# Model sanity check and selection
check_model() {
    log "Checking available models..."
    
    local models_response
    models_response=$(curl -s --max-time 10 "$BASE_URL/models")
    
    if [ $? -ne 0 ]; then
        error "Failed to fetch models from $BASE_URL"
        exit 1
    fi
    
    # Check if specified model exists
    if echo "$models_response" | jq -e ".data[] | select(.id == \"$MODEL_ID\")" >/dev/null; then
        success "Using specified model: $MODEL_ID"
    else
        # Fallback to first available model
        local first_model
        first_model=$(echo "$models_response" | jq -r '.data[0].id // empty')
        
        if [ -n "$first_model" ]; then
            warn "Model '$MODEL_ID' not found, falling back to: $first_model"
            MODEL_ID="$first_model"
        else
            error "No models available"
            exit 1
        fi
    fi
    
    # Test the model with a simple chat
    log "Testing model with sample chat..."
    local test_response
    test_response=$(curl -s --max-time 30 "$BASE_URL/chat/completions" \
        -H "Content-Type: application/json" \
        -d "{
            \"model\": \"$MODEL_ID\",
            \"messages\": [
                {\"role\": \"system\", \"content\": \"You are a helpful assistant.\"},
                {\"role\": \"user\", \"content\": \"Say 'Hello from LM Studio!' and nothing else.\"}
            ],
            \"temperature\": $TEMP,
            \"max_tokens\": 50
        }")
    
    if [ $? -eq 0 ]; then
        local content
        content=$(echo "$test_response" | jq -r '.choices[0].message.content // empty')
        if [ -n "$content" ]; then
            success "Model test successful: $content"
        else
            warn "Model test response empty or malformed"
        fi
    else
        warn "Model test failed, but continuing..."
    fi
}

# Patch n8n workflow via API
patch_n8n_api() {
    log "Patching n8n workflow via API..."
    
    # Fetch current workflow
    local workflow_response
    workflow_response=$(curl -s --max-time 10 \
        -H "Authorization: Bearer $N8N_TOKEN" \
        "$N8N_URL/rest/workflows/$N8N_WORKFLOW_ID")
    
    if [ $? -ne 0 ]; then
        error "Failed to fetch workflow from n8n API"
        return 1
    fi
    
    # Check if workflow exists
    if echo "$workflow_response" | jq -e '.id' >/dev/null; then
        log "Workflow found: $(echo "$workflow_response" | jq -r '.name // .id')"
    else
        error "Workflow not found or invalid response"
        return 1
    fi
    
    # Create updated workflow JSON
    local updated_workflow
    updated_workflow=$(echo "$workflow_response" | jq --arg model "$MODEL_ID" \
        --arg temp "$TEMP" \
        --arg base_url "$BASE_URL" \
        --arg api_key "$OPENAI_API_KEY_PLACEHOLDER" \
        '
        .nodes |= map(
            if .name == "OpenAI Model" and .type == "@n8n/n8n-nodes-langchain.lmChatOpenAi" then
                .parameters.modelName = $model |
                .parameters.temperature = ($temp | tonumber) |
                (.parameters.options // {}) + {baseURL: $base_url} |
                (.parameters.credentials // {}) + {openAiApiKey: $api_key}
            else . end
        )
        ')
    
    # Check if any changes were made
    if [ "$workflow_response" = "$updated_workflow" ]; then
        warn "No changes needed - workflow already configured correctly"
        return 0
    fi
    
    # Show diff summary
    log "Changes to be applied:"
    echo "$workflow_response" | jq -r '.nodes[] | select(.name == "OpenAI Model" and .type == "@n8n/n8n-nodes-langchain.lmChatOpenAi") | .parameters' > /tmp/before.json
    echo "$updated_workflow" | jq -r '.nodes[] | select(.name == "OpenAI Model" and .type == "@n8n/n8n-nodes-langchain.lmChatOpenAi") | .parameters' > /tmp/after.json
    
    echo "  modelName: $(jq -r '.modelName // "not set"' /tmp/before.json) → $MODEL_ID"
    echo "  temperature: $(jq -r '.temperature // "not set"' /tmp/before.json) → $TEMP"
    echo "  baseURL: $(jq -r '.options.baseURL // "not set"' /tmp/before.json) → $BASE_URL"
    echo "  apiKey: $(jq -r '.credentials.openAiApiKey // "not set"' /tmp/before.json) → $OPENAI_API_KEY_PLACEHOLDER"
    
    # Update workflow via API
    local update_response
    update_response=$(curl -s --max-time 30 \
        -X PUT \
        -H "Authorization: Bearer $N8N_TOKEN" \
        -H "Content-Type: application/json" \
        -d "$updated_workflow" \
        "$N8N_URL/rest/workflows/$N8N_WORKFLOW_ID")
    
    if [ $? -eq 0 ] && echo "$update_response" | jq -e '.id' >/dev/null; then
        success "Workflow updated successfully via API"
        return 0
    else
        error "Failed to update workflow via API"
        return 1
    fi
}

# Patch n8n workflow via JSON file
patch_n8n_json() {
    log "Patching n8n workflow via JSON file..."
    
    if [ ! -f "$PATCH_JSON_PATH" ]; then
        warn "JSON file not found: $PATCH_JSON_PATH"
        return 1
    fi
    
    # Create backup
    local backup_path="$HOME/Desktop/workflow_backup_$(date +%Y%m%d_%H%M%S).json"
    cp "$PATCH_JSON_PATH" "$backup_path"
    log "Backup created: $backup_path"
    
    # Patch the JSON file
    local temp_file
    temp_file=$(mktemp)
    
    jq --arg model "$MODEL_ID" \
       --arg temp "$TEMP" \
       --arg base_url "$BASE_URL" \
       --arg api_key "$OPENAI_API_KEY_PLACEHOLDER" \
       '
       .nodes |= map(
           if .name == "OpenAI Model" and .type == "@n8n/n8n-nodes-langchain.lmChatOpenAi" then
               .parameters.modelName = $model |
               .parameters.temperature = ($temp | tonumber) |
               (.parameters.options // {}) + {baseURL: $base_url} |
               (.parameters.credentials // {}) + {openAiApiKey: $api_key}
           else . end
       )
       ' "$PATCH_JSON_PATH" > "$temp_file"
    
    if [ $? -eq 0 ]; then
        mv "$temp_file" "$HOME/Desktop/workflow_local_llm.json"
        success "Workflow JSON patched and saved to: $HOME/Desktop/workflow_local_llm.json"
        log "Next step: Import this file in n8n UI (Workflows → Import from File)"
        return 0
    else
        error "Failed to patch JSON file"
        rm -f "$temp_file"
        return 1
    fi
}

# Print guardrails and one-liners
print_guardrails() {
    log "Guardrails and one-liners:"
    echo ""
    echo "${YELLOW}Health check before inference:${RESET}"
    echo "Add this HTTP Request node in n8n before your LLM node:"
    echo "  Method: GET"
    echo "  URL: $BASE_URL/models"
    echo "  On failure: Set node to 'Error Trigger' or short-circuit workflow"
    echo ""
    
    echo "${YELLOW}Token & latency guardrails:${RESET}"
    echo "  max_tokens: 512-1024 (prevents runaway responses)"
    echo "  temperature: 0.2-0.4 (maintains consistency)"
    echo "  Memory truncation: For Agent nodes, consider limiting context window"
    echo ""
    
    echo "${YELLOW}Quick one-liners:${RESET}"
    echo "A) Server check:"
    echo "   /usr/bin/curl -s $BASE_URL/models | /usr/bin/jq . || echo \"LM Studio server not responding on :1234 (open Developer → OpenAI Compatible Server → Start)\""
    echo ""
    echo "B) Test model:"
    echo "   curl -s $BASE_URL/chat/completions -H \"Content-Type: application/json\" -d '{\"model\": \"$MODEL_ID\", \"messages\": [{\"role\": \"user\", \"content\": \"Hello\"}], \"temperature\": $TEMP}' | jq -r '.choices[0].message.content'"
    echo ""
}

# Show help
show_help() {
    cat << EOF
Usage: $0 [OPTIONS]

Automates LM Studio OpenAI server startup and n8n workflow patching.

OPTIONS:
    --help              Show this help message
    
ENVIRONMENT VARIABLES:
    LMSTUDIO_APP_NAME  LM Studio application name (default: "LM Studio")
    BASE_URL           LM Studio server URL (default: http://127.0.0.1:1234/v1)
    MODEL_ID           Model to use (default: qwen3-14b-mlx)
    TEMP               Temperature setting (default: 0.2)
    N8N_URL            n8n instance URL for API mode
    N8N_TOKEN          n8n Personal Access Token for API mode
    N8N_WORKFLOW_ID    n8n workflow ID for API mode
    PATCH_JSON_PATH    Path to workflow JSON for fallback mode

EXAMPLES:
    # Basic usage with defaults
    $0
    
    # With custom model and n8n API
    MODEL_ID="llama-3.1-8b" N8N_URL="http://localhost:5678" N8N_TOKEN="your-token" N8N_WORKFLOW_ID="123" $0
    
    # JSON fallback mode
    PATCH_JSON_PATH="/path/to/workflow.json" $0

EOF
}

# Main execution
main() {
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --help)
                show_help
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    log "Starting local-llm-n8n-bridge.sh"
    log "Configuration:"
    echo "  LM Studio App: $LMSTUDIO_APP_NAME"
    echo "  Base URL: $BASE_URL"
    echo "  Model ID: $MODEL_ID"
    echo "  Temperature: $TEMP"
    echo "  n8n URL: ${N8N_URL:-not set}"
    echo "  n8n Workflow ID: ${N8N_WORKFLOW_ID:-not set}"
    echo "  JSON Path: $PATCH_JSON_PATH"
    echo ""
    
    # Check prerequisites
    check_prerequisites
    
    # Check/start LM Studio server
    if ! check_lmstudio_server; then
        start_lmstudio_server
    fi
    
    # Check model
    check_model
    
    # Patch n8n workflow
    local patch_success=false
    local patch_method=""
    
    if [ -n "$N8N_URL" ] && [ -n "$N8N_TOKEN" ] && [ -n "$N8N_WORKFLOW_ID" ]; then
        if patch_n8n_api; then
            patch_success=true
            patch_method="API"
        fi
    fi
    
    if [ "$patch_success" = false ] && [ -f "$PATCH_JSON_PATH" ]; then
        if patch_n8n_json; then
            patch_success=true
            patch_method="JSON"
        fi
    fi
    
    if [ "$patch_success" = false ]; then
        warn "No n8n patching performed (missing API credentials or JSON file)"
    fi
    
    # Print guardrails
    print_guardrails
    
    # Final summary
    echo ""
    success "Bridge setup complete!"
    echo "  ✅ LM Studio server: $BASE_URL"
    echo "  ✅ Model: $MODEL_ID"
    if [ "$patch_success" = true ]; then
        echo "  ✅ n8n patched via: $patch_method"
    else
        echo "  ⚠️  n8n not patched"
    fi
    
    exit 0
}

# Run main function
main "$@"
