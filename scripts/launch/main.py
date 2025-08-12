#!/usr/bin/env python3
"""
CODE_ALCHEMY_PRO - Main Launch Script
Consolidated entry point for all system components
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

try:
    from core.config import Config
    from web.app import main as dashboard_main
except ImportError:
    # Handle import errors gracefully
    Config = None
    dashboard_main = None


def launch_dashboard():
    """Launch the Streamlit dashboard"""
    print("🚀 Launching CODE_ALCHEMY_PRO Dashboard...")
    dashboard_main()


def launch_n8n_integration():
    """Launch N8N integration services"""
    print("🔗 Launching N8N Integration Services...")
    # Import and launch N8N integration
    try:
        from integrations.n8n_integration import N8NIntegration
        integration = N8NIntegration()
        integration.start()
    except ImportError as e:
        print(f"❌ N8N integration not available: {e}")
        sys.exit(1)


def launch_agent_system():
    """Launch the AI agent system"""
    print("🤖 Launching AI Agent System...")
    try:
        from agents.agent_manager import AgentManager
        manager = AgentManager()
        manager.start_all_agents()
    except ImportError as e:
        print(f"❌ Agent system not available: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="CODE_ALCHEMY_PRO - AI-Powered Desktop Intelligence System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s dashboard          # Launch web dashboard
  %(prog)s n8n               # Launch N8N integration
  %(prog)s agents            # Launch AI agent system
  %(prog)s all               # Launch all components
        """
    )
    
    parser.add_argument(
        "component",
        choices=["dashboard", "n8n", "agents", "all"],
        help="Component to launch"
    )
    
    parser.add_argument(
        "--config",
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config:
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"❌ Configuration file not found: {config_path}")
            sys.exit(1)
        Config.load_from_file(config_path)
    
    # Set debug mode
    if args.debug:
        os.environ["DEBUG"] = "1"
        print("🐛 Debug mode enabled")
    
    # Launch requested component
    try:
        if args.component == "dashboard":
            launch_dashboard()
        elif args.component == "n8n":
            launch_n8n_integration()
        elif args.component == "agents":
            launch_agent_system()
        elif args.component == "all":
                    msg = "🚀 Launching all CODE_ALCHEMY_PRO components..."
        print(msg)
        launch_agent_system()
        launch_n8n_integration()
        launch_dashboard()
    except KeyboardInterrupt:
        print("\n⏹️  Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Error launching {args.component}: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
