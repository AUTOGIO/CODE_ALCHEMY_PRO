#!/usr/bin/env python3
"""
CODE_ALCHEMY Professional - Example 2: Document Processing & Analysis
Real-world scenario: Processing and analyzing business documents
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.agents.file_organization.agent import create_file_organization_agent
from src.integrations.github_integration import create_github_integration


def document_processing_project():
    """Real document processing and analysis workflow"""
    
    print("📄 CODE_ALCHEMY Professional - Document Processing Project")
    print("=" * 60)
    
    # Step 1: Initialize components
    print("\n📋 Step 1: Initializing System Components")
    file_agent = create_file_organization_agent()
    github = create_github_integration()
    
    # Step 2: Create sample business documents
    print("\n📁 Step 2: Creating Sample Business Documents")
    project_dir = Path("examples/document_processing_project")
    project_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample business documents
    sample_documents = {
        "financial_report_2024.txt": """
Q4 2024 Financial Report
Company: TechCorp Solutions
Date: December 31, 2024

REVENUE SUMMARY:
- Q1: $2.5M
- Q2: $3.1M
- Q3: $3.8M
- Q4: $4.2M
Total Annual Revenue: $13.6M

EXPENSES:
- Personnel: $8.2M (60%)
- Infrastructure: $2.7M (20%)
- Marketing: $1.4M (10%)
- R&D: $1.3M (10%)
Total Expenses: $13.6M

PROFIT MARGIN: 15%
NET PROFIT: $2.04M

KEY METRICS:
- Customer Acquisition Cost: $150
- Customer Lifetime Value: $2,400
- Monthly Recurring Revenue: $1.1M
- Churn Rate: 2.3%

RECOMMENDATIONS:
1. Increase R&D investment by 20%
2. Optimize customer acquisition channels
3. Implement cost reduction strategies
4. Expand to new markets
""",
        "customer_feedback.json": """
{
  "survey_results": {
    "total_responses": 1250,
    "satisfaction_scores": {
      "product_quality": 4.2,
      "customer_service": 4.5,
      "ease_of_use": 4.1,
      "value_for_money": 3.9,
      "overall_satisfaction": 4.2
    },
    "top_complaints": [
      "Slow response times",
      "Complex interface",
      "High pricing",
      "Limited features",
      "Poor documentation"
    ],
    "top_praises": [
      "Reliable service",
      "Helpful support team",
      "Good value",
      "Easy integration",
      "Regular updates"
    ],
    "improvement_suggestions": [
      "Faster loading times",
      "Simpler user interface",
      "Better documentation",
      "More customization options",
      "Lower pricing tiers"
    ]
  }
}
""",
        "market_analysis.md": """
# Market Analysis Report 2024

## Executive Summary
The software-as-a-service (SaaS) market continues to experience strong growth, with our target segment showing 25% year-over-year expansion.

## Market Size
- Total Addressable Market: $45B
- Serviceable Addressable Market: $12B
- Serviceable Obtainable Market: $2.4B

## Competitive Landscape
### Primary Competitors:
1. **TechGiant Inc.** - 35% market share
   - Strengths: Brand recognition, extensive features
   - Weaknesses: High cost, complex interface

2. **StartupXYZ** - 15% market share
   - Strengths: Modern interface, competitive pricing
   - Weaknesses: Limited features, small team

3. **EnterpriseSoft** - 20% market share
   - Strengths: Enterprise features, security
   - Weaknesses: Expensive, slow innovation

## Growth Opportunities
1. **Emerging Markets**: 40% growth potential
2. **SMB Segment**: 30% growth potential
3. **Mobile Solutions**: 50% growth potential
4. **AI Integration**: 60% growth potential

## Recommendations
1. Focus on SMB market segment
2. Develop mobile-first solutions
3. Integrate AI capabilities
4. Expand to emerging markets
5. Improve customer experience
""",
        "employee_survey.csv": """
Department,Employee_ID,Job_Satisfaction,Work_Life_Balance,Compensation,Benefits,Management,Overall_Rating
Engineering,EMP001,4.2,3.8,4.0,4.5,4.1,4.1
Engineering,EMP002,4.5,4.0,3.9,4.3,4.2,4.2
Sales,EMP003,4.1,3.5,4.3,4.0,3.8,4.0
Sales,EMP004,3.9,3.2,4.1,3.8,3.6,3.7
Marketing,EMP005,4.3,4.2,3.8,4.1,4.0,4.1
Marketing,EMP006,4.0,4.1,3.7,4.2,3.9,4.0
HR,EMP007,4.4,4.3,3.9,4.4,4.3,4.3
HR,EMP008,4.2,4.0,3.8,4.2,4.1,4.0
Finance,EMP009,3.8,3.5,4.2,4.0,3.7,3.8
Finance,EMP010,4.0,3.9,4.1,4.1,3.9,4.0
""",
        "project_timeline.yaml": """
project_name: "Product Launch 2024"
start_date: 2024-01-15
end_date: 2024-06-30
budget: $500,000

phases:
  planning:
    duration: 4 weeks
    budget: $50,000
    tasks:
      - market_research
      - requirements_gathering
      - team_formation
      - technology_selection
  
  development:
    duration: 12 weeks
    budget: $300,000
    tasks:
      - frontend_development
      - backend_development
      - database_design
      - api_integration
      - testing
  
  testing:
    duration: 4 weeks
    budget: $75,000
    tasks:
      - unit_testing
      - integration_testing
      - user_acceptance_testing
      - performance_testing
  
  launch:
    duration: 2 weeks
    budget: $75,000
    tasks:
      - marketing_campaign
      - customer_onboarding
      - support_setup
      - monitoring_setup

milestones:
  - date: 2024-02-15
    event: "Requirements Finalized"
  - date: 2024-04-15
    event: "Development Complete"
  - date: 2024-05-15
    event: "Testing Complete"
  - date: 2024-06-15
    event: "Launch Ready"
"""
    }
    
    # Create sample documents
    for filename, content in sample_documents.items():
        file_path = project_dir / filename
        with open(file_path, 'w') as f:
            f.write(content.strip())
        print(f"✅ Created: {file_path}")
    
    # Step 3: Process documents with file organization agent
    print("\n🔧 Step 3: Processing Documents")
    
    # Move documents to data/documents for processing
    for filename in sample_documents.keys():
        source_path = project_dir / filename
        dest_path = Path("data/documents") / filename
        if source_path.exists():
            dest_path.write_text(source_path.read_text())
            print(f"📄 Moved to processing: {filename}")
    
    # Process documents
    processing_result = file_agent.process_documents()
    print(f"✅ Processing complete: {processing_result['files_processed']} files organized")
    
    # Step 4: Analyze document content
    print("\n📊 Step 4: Document Content Analysis")
    
    analysis_results = {
        "financial_report": {
            "type": "financial_document",
            "key_metrics": {
                "total_revenue": "$13.6M",
                "profit_margin": "15%",
                "net_profit": "$2.04M",
                "growth_rate": "68% (Q1 to Q4)"
            },
            "insights": [
                "Strong revenue growth throughout the year",
                "Healthy profit margin maintained",
                "R&D investment at 10% of revenue",
                "Customer metrics show good retention"
            ],
            "recommendations": [
                "Increase R&D investment to 15%",
                "Focus on customer acquisition optimization",
                "Consider market expansion",
                "Implement cost reduction strategies"
            ]
        },
        "customer_feedback": {
            "type": "survey_data",
            "key_metrics": {
                "total_responses": 1250,
                "overall_satisfaction": 4.2,
                "top_issue": "Slow response times",
                "top_strength": "Reliable service"
            },
            "insights": [
                "Strong customer satisfaction (4.2/5)",
                "Customer service is a key strength",
                "Response time is the main concern",
                "Value for money needs improvement"
            ],
            "recommendations": [
                "Improve system performance and response times",
                "Enhance user interface simplicity",
                "Develop better documentation",
                "Consider pricing strategy review"
            ]
        },
        "market_analysis": {
            "type": "market_research",
            "key_metrics": {
                "market_size": "$45B",
                "target_market": "$2.4B",
                "growth_rate": "25% YoY",
                "competitors": 3
            },
            "insights": [
                "Large addressable market opportunity",
                "Strong competitive landscape",
                "Emerging markets show high growth potential",
                "AI integration is key differentiator"
            ],
            "recommendations": [
                "Focus on SMB market segment",
                "Develop mobile-first solutions",
                "Integrate AI capabilities",
                "Expand to emerging markets"
            ]
        },
        "employee_survey": {
            "type": "hr_data",
            "key_metrics": {
                "total_employees": 10,
                "average_satisfaction": 4.0,
                "best_department": "HR (4.3)",
                "improvement_area": "Work-life balance"
            },
            "insights": [
                "Overall positive employee satisfaction",
                "HR department leads in satisfaction",
                "Work-life balance needs improvement",
                "Compensation is generally satisfactory"
            ],
            "recommendations": [
                "Improve work-life balance policies",
                "Enhance management training",
                "Review compensation structure",
                "Strengthen employee benefits"
            ]
        },
        "project_timeline": {
            "type": "project_management",
            "key_metrics": {
                "project_duration": "24 weeks",
                "total_budget": "$500,000",
                "largest_phase": "Development (60%)",
                "critical_path": "Development phase"
            },
            "insights": [
                "Well-structured project timeline",
                "Adequate budget allocation",
                "Development phase is critical",
                "Testing phase properly allocated"
            ],
            "recommendations": [
                "Monitor development phase closely",
                "Ensure adequate testing resources",
                "Prepare marketing campaign early",
                "Set up monitoring systems"
            ]
        }
    }
    
    # Step 5: Generate comprehensive report
    print("\n📈 Step 5: Generating Comprehensive Analysis Report")
    
    comprehensive_report = {
        "project": "Document Processing & Analysis",
        "timestamp": datetime.now().isoformat(),
        "documents_processed": len(sample_documents),
        "analysis_summary": {
            "financial_health": "Strong (15% profit margin)",
            "customer_satisfaction": "Good (4.2/5 rating)",
            "market_position": "Favorable (25% growth)",
            "employee_morale": "Positive (4.0/5 rating)",
            "project_status": "On track (24 weeks)"
        },
        "key_findings": [
            "Company shows strong financial performance with 68% revenue growth",
            "Customer satisfaction is good but response times need improvement",
            "Market opportunity is significant with $2.4B target market",
            "Employee satisfaction is positive with room for work-life balance improvement",
            "Project timeline is well-structured with adequate budget allocation"
        ],
        "strategic_recommendations": [
            "Prioritize system performance improvements to address customer concerns",
            "Increase R&D investment to 15% for competitive advantage",
            "Focus on SMB market segment for growth",
            "Implement work-life balance initiatives for employee retention",
            "Monitor project development phase closely for on-time delivery"
        ],
        "risk_assessment": {
            "high_risk": [
                "Customer churn due to slow response times",
                "Market competition from larger players"
            ],
            "medium_risk": [
                "Employee turnover due to work-life balance",
                "Project delays in development phase"
            ],
            "low_risk": [
                "Financial performance fluctuations",
                "Market growth slowdown"
            ]
        }
    }
    
    # Save comprehensive report
    report_file = project_dir / "comprehensive_analysis_report.json"
    with open(report_file, 'w') as f:
        json.dump(comprehensive_report, f, indent=2)
    print(f"✅ Comprehensive report saved: {report_file}")
    
    # Step 6: Create GitHub issue for findings
    print("\n🐙 Step 6: Creating GitHub Issue for Findings")
    
    github_status = github.test_connection()
    if github_status["success"]:
        issue_body = f"""
## Document Analysis Results

### Documents Analyzed: {len(sample_documents)}
- Financial Report 2024
- Customer Feedback Survey
- Market Analysis Report
- Employee Satisfaction Survey
- Project Timeline

### Key Findings:
1. **Financial Health**: Strong performance with 15% profit margin
2. **Customer Satisfaction**: Good (4.2/5) but response times need improvement
3. **Market Position**: Favorable with $2.4B target market
4. **Employee Morale**: Positive (4.0/5) with work-life balance concerns
5. **Project Status**: On track with 24-week timeline

### Strategic Recommendations:
1. Prioritize system performance improvements
2. Increase R&D investment to 15%
3. Focus on SMB market segment
4. Implement work-life balance initiatives
5. Monitor project development phase closely

### Risk Assessment:
- **High Risk**: Customer churn, market competition
- **Medium Risk**: Employee turnover, project delays
- **Low Risk**: Financial fluctuations, market slowdown
"""
        
        issue_result = github.create_issue(
            repo_name="code-alchemy-examples",
            title="Document Analysis: Business Intelligence Report",
            body=issue_body,
            labels=["analysis", "business-intelligence", "strategic-planning"]
        )
        
        if issue_result["success"]:
            print(f"✅ Created GitHub issue: {issue_result['issue']['url']}")
    
    print("\n🎉 Document Processing Project Complete!")
    print(f"📁 Project files: {project_dir}")
    print(f"📊 Analysis report: {report_file}")
    print(f"📄 Documents processed: {len(sample_documents)}")


if __name__ == "__main__":
    document_processing_project() 