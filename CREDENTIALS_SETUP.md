# 🔐 CODE_ALCHEMY Professional - Credentials Setup Guide

## 📋 **Required Credentials for Production**

To complete the production setup, you need to configure the following integrations:

---

## 🐙 **GitHub Integration Setup**

### **Step 1: Create GitHub Personal Access Token**

1. **Go to GitHub Settings:**
   - Visit: https://github.com/settings/tokens
   - Click "Generate new token (classic)"

2. **Configure Token Permissions:**
   ```
   ✅ repo (Full control of private repositories)
   ✅ workflow (Update GitHub Action workflows)
   ✅ write:packages (Upload packages to GitHub Package Registry)
   ✅ delete:packages (Delete packages from GitHub Package Registry)
   ✅ admin:org (Full control of orgs and teams)
   ✅ admin:public_key (Full control of public keys)
   ✅ admin:repo_hook (Full control of repository hooks)
   ✅ admin:org_hook (Full control of organization hooks)
   ✅ gist (Create gists)
   ✅ notifications (Full control of notifications)
   ✅ user (Full control of user profile)
   ✅ delete_repo (Delete repositories)
   ✅ write:discussion (Create and edit discussions)
   ✅ admin:gpg_key (Full control of GPG keys)
   ```

3. **Generate Token:**
   - Set expiration to "No expiration" for production
   - Click "Generate token"
   - **Copy the token immediately** (you won't see it again)
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

### **Step 2: Configure GitHub in CODE_ALCHEMY**

1. **Create `.env` file:**
   ```bash
   cp env.production.example .env
   ```

2. **Edit `.env` file:**
   ```bash
   # Replace with your actual GitHub token
   GITHUB_TOKEN=ghp_your_actual_token_here
   GITHUB_USERNAME=AUTOGIO
   ```

3. **Test GitHub Integration:**
   ```bash
   source code_alchemy_env/bin/activate.fish
   python3 -c "
   from src.integrations.github_integration import create_github_integration
   github = create_github_integration()
   result = github.test_connection()
   print('GitHub Status:', result)
   "
   ```

---

## ☁️ **Google Drive Integration Setup**

### **Step 1: Create Google Cloud Project**

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com/
   - Create a new project or select existing

2. **Enable Google Drive API:**
   - Go to "APIs & Services" > "Library"
   - Search for "Google Drive API"
   - Click "Enable"

### **Step 2: Create OAuth 2.0 Credentials**

1. **Configure OAuth Consent Screen:**
   - Go to "APIs & Services" > "OAuth consent screen"
   - Choose "External" user type
   - Fill in app information:
     - App name: "CODE_ALCHEMY Professional"
     - User support email: your email
     - Developer contact email: your email

2. **Create OAuth 2.0 Client ID:**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client IDs"
   - Choose "Desktop application"
   - Name: "CODE_ALCHEMY Desktop Client"

3. **Download Credentials:**
   - Download the JSON file
   - Rename to `credentials.json`
   - Place in project root: `/Users/eduardof.giovannini/Documents/CODE_ALCHEMY_PRO/`

### **Step 3: Get Access Token**

1. **Install Google OAuth Library:**
   ```bash
   source code_alchemy_env/bin/activate.fish
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

2. **Run OAuth Flow:**
   ```bash
   python3 -c "
   from google_auth_oauthlib.flow import InstalledAppFlow
   from google.auth.transport.requests import Request
   import pickle
   import os.path
   
   SCOPES = ['https://www.googleapis.com/auth/drive']
   
   creds = None
   if os.path.exists('token.pickle'):
       with open('token.pickle', 'rb') as token:
           creds = pickle.load(token)
   
   if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
           creds = flow.run_local_server(port=0)
       
       with open('token.pickle', 'wb') as token:
           pickle.dump(creds, token)
   
   print('Access Token:', creds.token)
   "
   ```

3. **Configure Google Drive in `.env`:**
   ```bash
   # Enable Google Drive
   GOOGLE_DRIVE_ENABLED=true
   GOOGLE_DRIVE_CREDENTIALS_FILE=credentials.json
   GOOGLE_DRIVE_ACCESS_TOKEN=your_access_token_from_above
   GOOGLE_DRIVE_SYNC_FOLDERS=~/Desktop/CODE_ALCHEMY_Projects,~/Documents/AI_Projects
   ```

### **Step 4: Test Google Drive Integration**

```bash
python3 -c "
from src.integrations.google_drive_integration import create_google_drive_integration
drive = create_google_drive_integration()
result = drive.test_connection()
print('Google Drive Status:', result)
"
```

---

## 🔧 **MCP Server Setup**

### **Step 1: Verify MCP Configuration**

The MCP servers are already configured. Check the configuration:

```bash
cat ~/.cursor/mcp.json
```

### **Step 2: Test MCP Servers**

```bash
# Test LM Studio Bridge
echo "list_models" | python3 src/mcp/lm_studio_bridge.py

# Test Model Manager
echo "list_tasks" | python3 src/mcp/model_manager.py
```

---

## ✅ **Final Verification**

### **Step 1: Test All Integrations**

```bash
source code_alchemy_env/bin/activate.fish

# Test GitHub
python3 -c "
from src.integrations.github_integration import create_github_integration
github = create_github_integration()
print('GitHub:', github.test_connection())
"

# Test Google Drive
python3 -c "
from src.integrations.google_drive_integration import create_google_drive_integration
drive = create_google_drive_integration()
print('Google Drive:', drive.test_connection())
"

# Test MCP Servers
echo "list_models" | python3 src/mcp/lm_studio_bridge.py
```

### **Step 2: Restart Dashboard**

```bash
# Stop current dashboard
pkill -f streamlit

# Start with new configuration
python3 launch_dashboard.py
```

---

## 🎯 **Expected Results**

After setup, you should see:

### **GitHub Integration:**
```
GitHub: {'success': True, 'username': 'AUTOGIO', 'repos_count': X}
```

### **Google Drive Integration:**
```
Google Drive: {'success': True, 'user_email': 'your@email.com', 'quota_used': X}
```

### **MCP Servers:**
```
{"success": true, "models": [...], "count": 17}
```

---

## 🔒 **Security Notes**

1. **Never commit `.env` file** - it contains sensitive tokens
2. **Keep tokens secure** - treat them like passwords
3. **Rotate tokens regularly** - for production security
4. **Use environment variables** - for deployment

---

## 🚀 **Production Ready**

Once all credentials are configured:

✅ **GitHub:** Repository management and code sync  
✅ **Google Drive:** Cloud file synchronization  
✅ **MCP Servers:** Advanced model management  
✅ **Real Monitoring:** Live system metrics  
✅ **File Processing:** Actual data processing  

**Status: PRODUCTION ACTIVE** 🎉 