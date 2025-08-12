# N8N Credentials Setup Guide

## Overview

This guide explains how to set up and import the necessary credentials for n8n to integrate with CODE_ALCHEMY Professional. The credentials enable secure communication between n8n workflows and the CODE_ALCHEMY API.

## Prerequisites

- N8N is installed and running on your system
- CODE_ALCHEMY Professional API is accessible at `http://localhost:8000`
- You have access to the n8n web interface

## Available Credentials

The following credentials have been created for you:

### 1. CODE_ALCHEMY API
- **Type**: HTTP Header Authentication
- **Purpose**: Main API communication for triggering operations
- **Header**: `Authorization: Bearer sk_codealchemy_n8n_2025`

### 2. CODE_ALCHEMY Webhook
- **Type**: HTTP Header Authentication
- **Purpose**: Webhook communication for results and notifications
- **Header**: `Authorization: Bearer sk_codealchemy_n8n_2025`

### 3. CODE_ALCHEMY System
- **Type**: HTTP Header Authentication
- **Purpose**: System-level integrations and alerts
- **Header**: `Authorization: Bearer sk_codealchemy_n8n_2025`

## Method 1: Manual Import (Recommended for First-Time Setup)

### Step 1: Access N8N
1. Open your web browser and navigate to: `http://localhost:5678`
2. Login with:
   - **Username**: `admin`
   - **Password**: `codealchemy2025`

### Step 2: Navigate to Credentials
1. Click on **Settings** in the left sidebar
2. Select **Credentials** from the settings menu
3. Click **Add Credential**

### Step 3: Create CODE_ALCHEMY API Credential
1. Select **HTTP Header Auth** from the credential types
2. Fill in the following details:
   - **Name**: `CODE_ALCHEMY API`
   - **Header Name**: `Authorization`
   - **Header Value**: `Bearer sk_codealchemy_n8n_2025`
3. Click **Save**

### Step 4: Create CODE_ALCHEMY Webhook Credential
1. Click **Add Credential** again
2. Select **HTTP Header Auth**
3. Fill in the following details:
   - **Name**: `CODE_ALCHEMY Webhook`
   - **Header Name**: `Authorization`
   - **Header Value**: `Bearer sk_codealchemy_n8n_2025`
4. Click **Save**

### Step 5: Create CODE_ALCHEMY System Credential
1. Click **Add Credential** again
2. Select **HTTP Header Auth**
3. Fill in the following details:
   - **Name**: `CODE_ALCHEMY System`
   - **Header Name**: `Authorization`
   - **Header Value**: `Bearer sk_codealchemy_n8n_2025`
4. Click **Save**

## Method 2: Automated Import via API

### Prerequisites
- N8N must be running
- Basic authentication must be enabled
- The import script must be executable

### Step 1: Run the Automated Import
```bash
# Navigate to your home directory
cd ~

# Run the automated import script
./import_n8n_credentials.sh
```

### Step 2: Verify Import
```bash
# Run the verification script
./verify_n8n_credentials.sh
```

## Method 3: Direct API Import

If you prefer to import credentials directly via the n8n API:

```bash
# Import CODE_ALCHEMY API credentials
curl -X POST http://localhost:5678/api/v1/credentials \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Basic YWRtaW46Y29kZWFsY2hlbXkyMDI1' \
  -d @~/.n8n/credentials/n8n-api-credentials.json

# Import webhook credentials
curl -X POST http://localhost:5678/api/v1/credentials \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Basic YWRtaW46Y29kZWFsY2hlbXkyMDI1' \
  -d @~/.n8n/credentials/n8n-webhook-credentials.json

# Import system credentials
curl -X POST http://localhost:5678/api/v1/credentials \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Basic YWRtaW46Y29kZWFsY2hlbXkyMDI1' \
  -d @~/.n8n/credentials/n8n-system-credentials.json
```

## Verifying Credentials

### Check in N8N Interface
1. Go to **Settings** → **Credentials**
2. Verify that all three credentials are listed:
   - CODE_ALCHEMY API
   - CODE_ALCHEMY Webhook
   - CODE_ALCHEMY System

### Test API Connectivity
Run the verification script to test connectivity:
```bash
~/verify_n8n_credentials.sh
```

This will test:
- N8N process status
- Credentials directory existence
- CODE_ALCHEMY API accessibility
- Webhook endpoint accessibility

## Using Credentials in Workflows

Once imported, you can use these credentials in your n8n workflows:

### HTTP Request Nodes
1. Add an **HTTP Request** node to your workflow
2. In the **Authentication** field, select the appropriate credential:
   - Use **CODE_ALCHEMY API** for API calls
   - Use **CODE_ALCHEMY Webhook** for webhook calls
   - Use **CODE_ALCHEMY System** for system integrations

### Example Configuration
```json
{
  "url": "http://localhost:8000/api/agents/content_analysis/trigger",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpHeaderAuth",
  "credentials": {
    "httpHeaderAuth": {
      "id": "n8n-api-credentials",
      "name": "CODE_ALCHEMY API"
    }
  }
}
```

## Troubleshooting

### Common Issues

#### 1. Credentials Not Appearing
- Ensure you're logged into n8n as an admin user
- Check that the credentials were saved successfully
- Verify the credential type matches (HTTP Header Auth)

#### 2. Authentication Errors
- Verify the API key is correct: `sk_codealchemy_n8n_2025`
- Check that the CODE_ALCHEMY API is running on port 8000
- Ensure the webhook endpoints are accessible

#### 3. Import Failures
- Check that n8n is running and accessible
- Verify the API endpoint is correct
- Check the n8n logs for error messages

### Logs and Debugging
- N8N logs: `~/.n8n/n8n.log`
- N8N error logs: `~/.n8n/n8n-error.log`
- Check the n8n web interface for detailed error messages

## Security Notes

- The API key `sk_codealchemy_n8n_2025` is for development/testing purposes
- In production, use environment variables for sensitive credentials
- Regularly rotate API keys
- Monitor API usage and access logs

## Next Steps

After setting up credentials:

1. **Import Workflows**: Import the workflow templates from `data/n8n/templates/`
2. **Test Integration**: Run the integration test script
3. **Configure Webhooks**: Set up webhook endpoints in your workflows
4. **Monitor Execution**: Check workflow execution logs and results

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the n8n logs
3. Verify the CODE_ALCHEMY API status
4. Run the verification scripts
5. Check the workflow templates for proper credential references

---

**Last Updated**: January 28, 2025  
**Version**: 1.0  
**Compatibility**: N8N 1.0+, CODE_ALCHEMY Professional 2025
