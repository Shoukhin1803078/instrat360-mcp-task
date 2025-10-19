# mcp_server/mcp_server.py
from fastmcp import FastMCP

# Initialize MCP Server
mcp = FastMCP("INSTRAT360 MCP Server")

# ============================================
# DATA STORE (Resources)
# ============================================

COMPANY_INFO = {
    "name": "INSTRAT360",
    "tagline": "Unified Agentic AI Platform Built for Strategic Value Creation",
    "overview": "INSTRAT360 is a market-leading agentic AI strategy platform that integrates real-time AI reasoning, data logic, and dynamic strategy execution.",
    "mission": "To empower organizations with adaptable, actionable, and aligned strategies powered by agentic AI."
}

# EMPLOYEES = {
#     "Sarah Chen": {
#         "role": "CEO & Chief Strategist",
#         "department": "Executive",
#         "expertise": ["Strategic Planning", "AI Integration"]
#     },
#     "Marcus Johnson": {
#         "role": "CTO & AI Architect",
#         "department": "Technology",
#         "expertise": ["AI Architecture", "System Design"]
#     },
#     "Priya Sharma": {
#         "role": "Head of Strategy Consulting",
#         "department": "Consulting",
#         "expertise": ["Management Consulting", "OKR Design"]
#     }
# }


EMPLOYEES = {
    "Sarah Chen": {
        "role": "CEO & Chief Strategist",
        "department": "Executive",
        "expertise": ["Strategic Planning", "AI Integration"]
    },
    "Marcus Johnson": {
        "role": "CTO & AI Architect",
        "department": "Technology",
        "expertise": ["AI Architecture", "System Design"]
    },
    "Priya Sharma": {
        "role": "Head of Strategy Consulting",
        "department": "Consulting",
        "expertise": ["Management Consulting", "OKR Design"]
    }
}


PROJECTS = {
    "Platform Vision 2025": {
        "owner": "Sarah Chen",
        "status": "In Progress",
        "progress": 65
    },
    "Multi-Agent Framework": {
        "owner": "Marcus Johnson",
        "status": "In Progress",
        "progress": 78
    },
    "Financial Services Vertical": {
        "owner": "Priya Sharma",
        "status": "Active",
        "progress": 42
    }
}

# ============================================
# RESOURCES (Read-only data endpoints)
# ============================================

@mcp.resource("company://info")
def get_company_resource():
    """Resource: Company information"""
    return COMPANY_INFO

@mcp.resource("company://employees")
def get_employees_resource():
    """Resource: List of all employees"""
    return {"employees": list(EMPLOYEES.keys())}

@mcp.resource("company://projects")
def get_projects_resource():
    """Resource: List of all projects"""
    return {"projects": list(PROJECTS.keys())}

# ============================================
# TOOLS (Callable functions)
# ============================================

@mcp.tool()
def get_company_overview():
    """Get complete company overview including name, tagline, mission"""
    return COMPANY_INFO

@mcp.tool()
def get_employee_details(name: str):
    """Get detailed information about a specific employee"""
    if name not in EMPLOYEES:
        return {"error": f"Employee '{name}' not found", "available": list(EMPLOYEES.keys())}
    return {"name": name, **EMPLOYEES[name]}

@mcp.tool()
def list_all_employees():
    """List all employees with their roles"""
    result = []
    for name, info in EMPLOYEES.items():
        result.append({"name": name, "role": info["role"], "department": info["department"]})
    return {"employees": result, "total": len(result)}

@mcp.tool()
def get_project_details(project_name: str):
    """Get detailed information about a specific project"""
    if project_name not in PROJECTS:
        return {"error": f"Project '{project_name}' not found", "available": list(PROJECTS.keys())}
    return {"project": project_name, **PROJECTS[project_name]}

@mcp.tool()
def find_expert(skill: str):
    """Find employees who have expertise in a specific skill"""
    matches = []
    for name, info in EMPLOYEES.items():
        if any(skill.lower() in exp.lower() for exp in info["expertise"]):
            matches.append({"name": name, "role": info["role"], "expertise": info["expertise"]})
    
    if not matches:
        return {"message": f"No expert found for '{skill}'", "experts": []}
    return {"skill": skill, "experts": matches}

# ============================================
# PROMPTS (Pre-defined templates)
# ============================================

@mcp.prompt()
def company_analysis_prompt():
    """Prompt template for company analysis"""
    return """You are analyzing INSTRAT360, an agentic AI strategy platform.

Available information:
- Company overview, mission, and vision
- Employee profiles and expertise areas
- Active projects and their status

Please provide insights on:
1. Company strengths and positioning
2. Team capabilities
3. Project portfolio health"""

@mcp.prompt()
def employee_expertise_prompt():
    """Prompt template for finding the right expert"""
    return """Help find the right INSTRAT360 team member for a specific need.

Consider:
- Employee roles and departments
- Areas of expertise
- Current project involvement

Provide recommendations based on the query."""

@mcp.prompt()
def project_status_prompt():
    """Prompt template for project status review"""
    return """Review INSTRAT360 project status and provide analysis.

Focus on:
- Current progress metrics
- Project ownership
- Status and priorities

Deliver actionable insights."""

# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":
    mcp.run()