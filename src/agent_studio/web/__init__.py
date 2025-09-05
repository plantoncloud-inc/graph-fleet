"""Agent Studio Web Interface Module

This module contains the web interface components for the Agent Studio platform,
including HTML templates, static assets, and web-specific utilities.

The web interface provides:
- Agent browsing and discovery
- Template configuration and customization
- Deployment management
- Integration with the Agent Studio API
- Planton Cloud credential management UI

Components:
- HTML templates for all major pages (dashboard, agents, templates, deployments)
- CSS styles with responsive design and cloud provider theming
- JavaScript functionality for API integration and UI interactions
- Static asset management and serving
"""

from pathlib import Path
from typing import Dict, Any, Optional
import os

# Web interface paths
WEB_ROOT = Path(__file__).parent
TEMPLATES_DIR = WEB_ROOT / "templates"
STATIC_DIR = WEB_ROOT / "static"
CSS_DIR = STATIC_DIR / "css"
JS_DIR = STATIC_DIR / "js"
IMAGES_DIR = STATIC_DIR / "images"

def get_web_config() -> Dict[str, Any]:
    """Get web interface configuration
    
    Returns:
        Dictionary with web interface configuration
    """
    return {
        "templates_dir": str(TEMPLATES_DIR),
        "static_dir": str(STATIC_DIR),
        "css_dir": str(CSS_DIR),
        "js_dir": str(JS_DIR),
        "images_dir": str(IMAGES_DIR),
        "static_url_path": "/static",
        "template_engine": "jinja2",
        "auto_reload": True,
        "debug": os.getenv("AGENT_STUDIO_DEBUG", "false").lower() == "true"
    }

def get_available_templates() -> list[str]:
    """Get list of available HTML templates
    
    Returns:
        List of template names (without .html extension)
    """
    if not TEMPLATES_DIR.exists():
        return []
    
    templates = []
    for template_file in TEMPLATES_DIR.glob("*.html"):
        if template_file.name != "base.html":  # Exclude base template
            templates.append(template_file.stem)
    
    return sorted(templates)

def get_static_assets() -> Dict[str, list[str]]:
    """Get list of available static assets by type
    
    Returns:
        Dictionary mapping asset types to lists of asset files
    """
    assets = {
        "css": [],
        "js": [],
        "images": []
    }
    
    # CSS files
    if CSS_DIR.exists():
        assets["css"] = [f.name for f in CSS_DIR.glob("*.css")]
    
    # JavaScript files
    if JS_DIR.exists():
        assets["js"] = [f.name for f in JS_DIR.glob("*.js")]
    
    # Image files
    if IMAGES_DIR.exists():
        assets["images"] = [f.name for f in IMAGES_DIR.glob("*") 
                           if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico']]
    
    return assets

def validate_web_structure() -> Dict[str, Any]:
    """Validate web interface directory structure and files
    
    Returns:
        Dictionary with validation results
    """
    validation = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "structure": {}
    }
    
    # Check required directories
    required_dirs = [TEMPLATES_DIR, STATIC_DIR, CSS_DIR, JS_DIR]
    for directory in required_dirs:
        if directory.exists():
            validation["structure"][directory.name] = "exists"
        else:
            validation["valid"] = False
            validation["errors"].append(f"Missing directory: {directory}")
            validation["structure"][directory.name] = "missing"
    
    # Check required templates
    required_templates = ["base.html", "dashboard.html", "agents.html", "templates.html", "create_agent.html", "deployments.html"]
    for template in required_templates:
        template_path = TEMPLATES_DIR / template
        if template_path.exists():
            validation["structure"][f"template_{template}"] = "exists"
        else:
            validation["valid"] = False
            validation["errors"].append(f"Missing template: {template}")
            validation["structure"][f"template_{template}"] = "missing"
    
    # Check required static assets
    required_assets = {
        "css/agent-studio.css": CSS_DIR / "agent-studio.css",
        "js/agent-studio.js": JS_DIR / "agent-studio.js"
    }
    
    for asset_name, asset_path in required_assets.items():
        if asset_path.exists():
            validation["structure"][f"asset_{asset_name}"] = "exists"
        else:
            validation["valid"] = False
            validation["errors"].append(f"Missing asset: {asset_name}")
            validation["structure"][f"asset_{asset_name}"] = "missing"
    
    return validation

def get_web_interface_info() -> Dict[str, Any]:
    """Get comprehensive web interface information
    
    Returns:
        Dictionary with web interface details
    """
    return {
        "config": get_web_config(),
        "templates": get_available_templates(),
        "static_assets": get_static_assets(),
        "validation": validate_web_structure(),
        "features": {
            "responsive_design": True,
            "cloud_provider_theming": True,
            "api_integration": True,
            "real_time_updates": True,
            "authentication_integration": True,
            "multi_tenant_support": True,
            "accessibility_features": True,
            "mobile_optimized": True
        },
        "pages": {
            "dashboard": {
                "path": "/dashboard",
                "template": "dashboard.html",
                "description": "Main dashboard with stats and quick actions"
            },
            "agents": {
                "path": "/agents",
                "template": "agents.html", 
                "description": "Agent browsing and management"
            },
            "templates": {
                "path": "/templates",
                "template": "templates.html",
                "description": "Template browsing and discovery"
            },
            "create_agent": {
                "path": "/create",
                "template": "create_agent.html",
                "description": "Agent creation and configuration"
            },
            "deployments": {
                "path": "/deployments",
                "template": "deployments.html",
                "description": "Deployment management and monitoring"
            }
        },
        "integrations": {
            "agent_studio_api": True,
            "planton_cloud_auth": True,
            "bootstrap_ui": True,
            "fontawesome_icons": True,
            "chartjs_visualization": True
        }
    }

# Template rendering utilities (for FastAPI integration)
def get_template_context(page: str, user: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Get template context for a specific page
    
    Args:
        page: Page name (dashboard, agents, templates, etc.)
        user: Optional user information
        
    Returns:
        Dictionary with template context variables
    """
    base_context = {
        "page": page,
        "user": user or {},
        "config": get_web_config(),
        "static_url": "/static",
        "api_url": "/api"
    }
    
    # Page-specific context
    page_contexts = {
        "dashboard": {
            "title": "Dashboard",
            "show_stats": True,
            "show_quick_actions": True
        },
        "agents": {
            "title": "My Agents",
            "show_filters": True,
            "show_grid_toggle": True
        },
        "templates": {
            "title": "Agent Templates",
            "show_featured": True,
            "show_categories": True
        },
        "create_agent": {
            "title": "Create Agent",
            "show_wizard": True,
            "show_templates": True
        },
        "deployments": {
            "title": "Deployments",
            "show_stats": True,
            "auto_refresh": True
        }
    }
    
    if page in page_contexts:
        base_context.update(page_contexts[page])
    
    return base_context

# Web server integration helpers
def setup_static_routes(app, static_url_path: str = "/static"):
    """Setup static file routes for web framework
    
    Args:
        app: Web application instance (FastAPI, Flask, etc.)
        static_url_path: URL path for static files
    """
    try:
        # FastAPI static files setup
        from fastapi.staticfiles import StaticFiles
        app.mount(static_url_path, StaticFiles(directory=str(STATIC_DIR)), name="static")
        return True
    except ImportError:
        try:
            # Flask static files setup
            app.static_folder = str(STATIC_DIR)
            app.static_url_path = static_url_path
            return True
        except:
            return False

def setup_template_engine(app, templates_dir: Optional[str] = None):
    """Setup template engine for web framework
    
    Args:
        app: Web application instance
        templates_dir: Optional custom templates directory
    """
    template_dir = templates_dir or str(TEMPLATES_DIR)
    
    try:
        # FastAPI Jinja2 templates setup
        from fastapi.templating import Jinja2Templates
        return Jinja2Templates(directory=template_dir)
    except ImportError:
        try:
            # Flask Jinja2 templates setup
            app.template_folder = template_dir
            return app.jinja_env
        except:
            return None

__all__ = [
    "WEB_ROOT",
    "TEMPLATES_DIR", 
    "STATIC_DIR",
    "CSS_DIR",
    "JS_DIR",
    "IMAGES_DIR",
    "get_web_config",
    "get_available_templates",
    "get_static_assets",
    "validate_web_structure",
    "get_web_interface_info",
    "get_template_context",
    "setup_static_routes",
    "setup_template_engine"
]

