#!/usr/bin/env python3
"""
CODE_ALCHEMY Professional - Example 4: Security Monitoring & Threat Detection
Real-world scenario: Monitoring system security and detecting potential threats
"""

import os
import sys
import json
import time
import psutil
import requests
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.agents.file_organization.agent import create_file_organization_agent
from src.integrations.github_integration import create_github_integration


def security_monitoring_project():
    """Real security monitoring and threat detection workflow"""
    
    print("🔒 CODE_ALCHEMY Professional - Security Monitoring Project")
    print("=" * 60)
    
    # Step 1: Initialize components
    print("\n📋 Step 1: Initializing Security Components")
    file_agent = create_file_organization_agent()
    github = create_github_integration()
    
    # Step 2: System security baseline
    print("\n🔍 Step 2: Establishing Security Baseline")
    
    # Get system information
    system_info = {
        "hostname": os.uname().nodename,
        "platform": sys.platform,
        "python_version": sys.version,
        "cpu_count": psutil.cpu_count(),
        "memory_total": psutil.virtual_memory().total,
        "disk_usage": psutil.disk_usage('/').percent
    }
    
    print(f"✅ System: {system_info['hostname']} ({system_info['platform']})")
    print(f"💻 CPU: {system_info['cpu_count']} cores")
    print(f"💾 Memory: {system_info['memory_total'] // (1024**3)} GB")
    print(f"💿 Disk: {system_info['disk_usage']}% used")
    
    # Step 3: Security scan simulation
    print("\n🔍 Step 3: Security Vulnerability Scan")
    
    # Simulate security vulnerabilities
    security_scan_results = {
        "vulnerabilities": {
            "high": [
                {
                    "id": "VULN-001",
                    "type": "Outdated Dependencies",
                    "description": "Python packages with known security vulnerabilities",
                    "affected_packages": ["urllib3", "requests"],
                    "severity": "high",
                    "recommendation": "Update to latest versions"
                },
                {
                    "id": "VULN-002",
                    "type": "Weak File Permissions",
                    "description": "Sensitive files with overly permissive access",
                    "affected_files": ["data/documents/", "config/"],
                    "severity": "high",
                    "recommendation": "Restrict file permissions to 600"
                }
            ],
            "medium": [
                {
                    "id": "VULN-003",
                    "type": "Missing SSL Verification",
                    "description": "HTTP requests without SSL certificate verification",
                    "affected_code": ["src/integrations/"],
                    "severity": "medium",
                    "recommendation": "Enable SSL verification for all requests"
                },
                {
                    "id": "VULN-004",
                    "type": "Hardcoded Credentials",
                    "description": "API tokens and credentials in code",
                    "affected_files": ["src/core/config.py"],
                    "severity": "medium",
                    "recommendation": "Use environment variables for all credentials"
                }
            ],
            "low": [
                {
                    "id": "VULN-005",
                    "type": "Debug Mode Enabled",
                    "description": "Debug mode is enabled in production",
                    "affected_config": ["ENVIRONMENT=production", "DEBUG_MODE=true"],
                    "severity": "low",
                    "recommendation": "Disable debug mode in production"
                }
            ]
        },
        "threat_indicators": [
            {
                "type": "Suspicious Network Activity",
                "description": "Multiple failed connection attempts to external APIs",
                "timestamp": datetime.now().isoformat(),
                "severity": "medium"
            },
            {
                "type": "Unusual File Access",
                "description": "Multiple rapid file access patterns in data directory",
                "timestamp": datetime.now().isoformat(),
                "severity": "low"
            },
            {
                "type": "High CPU Usage",
                "description": "Sustained high CPU usage (>80%) for extended periods",
                "timestamp": datetime.now().isoformat(),
                "severity": "medium"
            }
        ],
        "compliance_issues": [
            {
                "type": "Data Privacy",
                "description": "User data not properly encrypted at rest",
                "compliance_standard": "GDPR",
                "severity": "high"
            },
            {
                "type": "Access Control",
                "description": "Missing role-based access control implementation",
                "compliance_standard": "SOC2",
                "severity": "medium"
            },
            {
                "type": "Audit Logging",
                "description": "Insufficient audit logging for security events",
                "compliance_standard": "ISO27001",
                "severity": "medium"
            }
        ]
    }
    
    # Display scan results
    print(f"🚨 High Severity Vulnerabilities: {len(security_scan_results['vulnerabilities']['high'])}")
    print(f"⚠️ Medium Severity Vulnerabilities: {len(security_scan_results['vulnerabilities']['medium'])}")
    print(f"ℹ️ Low Severity Vulnerabilities: {len(security_scan_results['vulnerabilities']['low'])}")
    print(f"🔍 Threat Indicators: {len(security_scan_results['threat_indicators'])}")
    print(f"📋 Compliance Issues: {len(security_scan_results['compliance_issues'])}")
    
    # Step 4: Real-time monitoring simulation
    print("\n📊 Step 4: Real-time Security Monitoring")
    
    # Simulate real-time monitoring data
    monitoring_data = {
        "network_activity": {
            "active_connections": 15,
            "failed_attempts": 3,
            "suspicious_ips": ["192.168.1.100", "10.0.0.50"],
            "data_transfer": "2.3 GB"
        },
        "system_activity": {
            "cpu_usage": psutil.cpu_percent(),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_io": "High",
            "process_count": len(psutil.pids())
        },
        "file_activity": {
            "files_accessed": 45,
            "files_modified": 12,
            "files_created": 8,
            "files_deleted": 2
        },
        "user_activity": {
            "active_sessions": 3,
            "failed_logins": 1,
            "privilege_escalations": 0,
            "suspicious_commands": 0
        }
    }
    
    print("📈 Real-time Monitoring Data:")
    print(f"   Network: {monitoring_data['network_activity']['active_connections']} connections")
    print(f"   System: CPU {monitoring_data['system_activity']['cpu_usage']}%, Memory {monitoring_data['system_activity']['memory_usage']}%")
    print(f"   Files: {monitoring_data['file_activity']['files_accessed']} accessed, {monitoring_data['file_activity']['files_modified']} modified")
    print(f"   Users: {monitoring_data['user_activity']['active_sessions']} sessions, {monitoring_data['user_activity']['failed_logins']} failed logins")
    
    # Step 5: Threat analysis and response
    print("\n🎯 Step 5: Threat Analysis and Response")
    
    threat_analysis = {
        "risk_assessment": {
            "overall_risk_score": 7.2,
            "risk_level": "medium",
            "factors": [
                "High severity vulnerabilities present",
                "Suspicious network activity detected",
                "Compliance issues identified"
            ]
        },
        "immediate_actions": [
            "Update vulnerable dependencies",
            "Restrict file permissions",
            "Enable SSL verification",
            "Implement proper credential management"
        ],
        "long_term_recommendations": [
            "Implement comprehensive security monitoring",
            "Add intrusion detection system",
            "Establish security incident response plan",
            "Conduct regular security audits",
            "Implement data encryption at rest"
        ],
        "compliance_remediation": [
            "Implement data encryption for GDPR compliance",
            "Add role-based access control for SOC2",
            "Enhance audit logging for ISO27001",
            "Establish data retention policies"
        ]
    }
    
    print(f"🎯 Overall Risk Score: {threat_analysis['risk_assessment']['overall_risk_score']}/10")
    print(f"⚠️ Risk Level: {threat_analysis['risk_assessment']['risk_level'].upper()}")
    
    print("\n🚨 Immediate Actions Required:")
    for action in threat_analysis['immediate_actions']:
        print(f"   • {action}")
    
    # Step 6: Generate security report
    print("\n📊 Step 6: Generating Security Report")
    
    project_dir = Path("examples/security_monitoring_project")
    project_dir.mkdir(parents=True, exist_ok=True)
    
    security_report = {
        "project": "Security Monitoring & Threat Detection",
        "timestamp": datetime.now().isoformat(),
        "system_info": system_info,
        "scan_results": security_scan_results,
        "monitoring_data": monitoring_data,
        "threat_analysis": threat_analysis,
        "summary": {
            "total_vulnerabilities": (
                len(security_scan_results['vulnerabilities']['high']) +
                len(security_scan_results['vulnerabilities']['medium']) +
                len(security_scan_results['vulnerabilities']['low'])
            ),
            "high_risk_vulnerabilities": len(security_scan_results['vulnerabilities']['high']),
            "threat_indicators": len(security_scan_results['threat_indicators']),
            "compliance_issues": len(security_scan_results['compliance_issues']),
            "overall_risk_score": threat_analysis['risk_assessment']['overall_risk_score']
        }
    }
    
    # Save security report
    report_file = project_dir / "security_monitoring_report.json"
    with open(report_file, 'w') as f:
        json.dump(security_report, f, indent=2)
    print(f"✅ Security report saved: {report_file}")
    
    # Step 7: Create security alerts
    print("\n🚨 Step 7: Creating Security Alerts")
    
    # Create security alerts based on findings
    alerts = []
    
    for vuln in security_scan_results['vulnerabilities']['high']:
        alerts.append({
            "type": "Vulnerability Alert",
            "severity": "high",
            "title": f"High Severity Vulnerability: {vuln['type']}",
            "description": vuln['description'],
            "recommendation": vuln['recommendation'],
            "timestamp": datetime.now().isoformat()
        })
    
    for threat in security_scan_results['threat_indicators']:
        if threat['severity'] in ['high', 'medium']:
            alerts.append({
                "type": "Threat Alert",
                "severity": threat['severity'],
                "title": f"Security Threat Detected: {threat['type']}",
                "description": threat['description'],
                "recommendation": "Investigate and respond immediately",
                "timestamp": threat['timestamp']
            })
    
    # Save alerts
    alerts_file = project_dir / "security_alerts.json"
    with open(alerts_file, 'w') as f:
        json.dump(alerts, f, indent=2)
    print(f"✅ Security alerts saved: {alerts_file}")
    
    # Step 8: Create GitHub issue for security findings
    print("\n🐙 Step 8: Creating GitHub Security Issue")
    
    github_status = github.test_connection()
    if github_status["success"]:
        issue_body = f"""
## Security Monitoring Results

### System Information:
- Hostname: {system_info['hostname']}
- Platform: {system_info['platform']}
- Risk Score: {threat_analysis['risk_assessment']['overall_risk_score']}/10

### Critical Findings:
1. **High Severity Vulnerabilities**: {len(security_scan_results['vulnerabilities']['high'])}
   - Outdated dependencies with known vulnerabilities
   - Weak file permissions on sensitive directories
   
2. **Threat Indicators**: {len(security_scan_results['threat_indicators'])}
   - Suspicious network activity detected
   - Unusual file access patterns
   - High CPU usage patterns

3. **Compliance Issues**: {len(security_scan_results['compliance_issues'])}
   - Data privacy violations (GDPR)
   - Missing access controls (SOC2)
   - Insufficient audit logging (ISO27001)

### Immediate Actions Required:
1. Update vulnerable dependencies (urllib3, requests)
2. Restrict file permissions to 600
3. Enable SSL verification for all requests
4. Move credentials to environment variables
5. Disable debug mode in production

### Long-term Recommendations:
1. Implement comprehensive security monitoring
2. Add intrusion detection system
3. Establish security incident response plan
4. Conduct regular security audits
5. Implement data encryption at rest

### Compliance Remediation:
1. Implement data encryption for GDPR compliance
2. Add role-based access control for SOC2
3. Enhance audit logging for ISO27001
4. Establish data retention policies
"""
        
        issue_result = github.create_issue(
            repo_name="code-alchemy-examples",
            title="Security Alert: High Severity Vulnerabilities Detected",
            body=issue_body,
            labels=["security", "vulnerability", "urgent", "compliance"]
        )
        
        if issue_result["success"]:
            print(f"✅ Created GitHub security issue: {issue_result['issue']['url']}")
    
    print("\n🎉 Security Monitoring Project Complete!")
    print(f"📁 Project files: {project_dir}")
    print(f"📊 Security report: {report_file}")
    print(f"🚨 Security alerts: {alerts_file}")
    print(f"🔍 Vulnerabilities found: {security_report['summary']['total_vulnerabilities']}")


if __name__ == "__main__":
    security_monitoring_project() 