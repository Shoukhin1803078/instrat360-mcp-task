# web_server/main.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import os
from typing import Optional
import httpx

# Import for LangChain - FIXED IMPORT
try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("Warning: LangChain not available. Only mock mode will work.")

app = FastAPI(title="INSTRAT360 Chatbot")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# ============================================
# MCP SERVER DATA (Mock Mode)
# ============================================

COMPANY_INFO = {
    "name": "INSTRAT360",
    "tagline": "Unified Agentic AI Platform Built for Strategic Value Creation",
    "overview": "INSTRAT360 is a market-leading agentic AI strategy platform that integrates real-time AI reasoning, data logic, and dynamic strategy execution.",
    "mission": "To empower organizations with adaptable, actionable, and aligned strategies powered by agentic AI."
}

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
# MCP TOOL FUNCTIONS
# ============================================

def get_company_overview():
    """MCP Tool: Get company overview"""
    return COMPANY_INFO

def get_employee_details(name: str):
    """MCP Tool: Get employee details"""
    if name not in EMPLOYEES:
        return {"error": f"Employee '{name}' not found", "available": list(EMPLOYEES.keys())}
    return {"name": name, **EMPLOYEES[name]}

def list_all_employees():
    """MCP Tool: List all employees"""
    result = []
    for name, info in EMPLOYEES.items():
        result.append({"name": name, "role": info["role"], "department": info["department"]})
    return {"employees": result, "total": len(result)}

def get_project_details(project_name: str):
    """MCP Tool: Get project details"""
    if project_name not in PROJECTS:
        return {"error": f"Project '{project_name}' not found", "available": list(PROJECTS.keys())}
    return {"project": project_name, **PROJECTS[project_name]}

def find_expert(skill: str):
    """MCP Tool: Find expert by skill"""
    matches = []
    for name, info in EMPLOYEES.items():
        if any(skill.lower() in exp.lower() for exp in info["expertise"]):
            matches.append({"name": name, "role": info["role"], "expertise": info["expertise"]})
    
    if not matches:
        return {"message": f"No expert found for '{skill}'", "experts": []}
    return {"skill": skill, "experts": matches}

# ============================================
# TOOL DISPATCHER
# ============================================

AVAILABLE_TOOLS = {
    "get_company_overview": get_company_overview,
    "get_employee_details": get_employee_details,
    "list_all_employees": list_all_employees,
    "get_project_details": get_project_details,
    "find_expert": find_expert
}

def call_mcp_tool(tool_name: str, **kwargs):
    """Call an MCP tool by name"""
    if tool_name not in AVAILABLE_TOOLS:
        return {"error": f"Tool '{tool_name}' not found"}
    
    tool_func = AVAILABLE_TOOLS[tool_name]
    try:
        return tool_func(**kwargs)
    except Exception as e:
        return {"error": str(e)}

# ============================================
# AI LOGIC
# ============================================

def detect_intent_and_call_tool(user_message: str):
    """Detect user intent and call appropriate MCP tool"""
    msg_lower = user_message.lower()
    
    # Company overview detection
    if any(word in msg_lower for word in ["company", "overview", "about instrat", "what is"]):
        return call_mcp_tool("get_company_overview")
    
    # Employee list detection
    if any(word in msg_lower for word in ["employees", "team", "staff", "who works", "list people"]):
        return call_mcp_tool("list_all_employees")
    
    # Specific employee detection
    for emp_name in EMPLOYEES.keys():
        if emp_name.lower() in msg_lower:
            return call_mcp_tool("get_employee_details", name=emp_name)
    
    # Project detection
    if any(word in msg_lower for word in ["project", "projects"]):
        for proj_name in PROJECTS.keys():
            if any(word in msg_lower for word in proj_name.lower().split()):
                return call_mcp_tool("get_project_details", project_name=proj_name)
        # Return all projects if no specific project mentioned
        return {"projects": PROJECTS}
    
    # Expert finding detection
    if any(word in msg_lower for word in ["expert", "who knows", "specialist"]):
        for skill in ["strategy", "ai", "consulting", "architecture", "design"]:
            if skill in msg_lower:
                return call_mcp_tool("find_expert", skill=skill)
    
    return None

def format_tool_response(data):
    """Format tool response for LLM"""
    if isinstance(data, dict):
        if "error" in data:
            return f"Error: {data['error']}"
        return str(data)
    return str(data)

# ============================================
# API MODELS
# ============================================

class ChatRequest(BaseModel):
    message: str
    mode: str = "mock"  # "openai" or "mock"
    api_key: Optional[str] = None

# ============================================
# API ENDPOINTS
# ============================================

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page"""
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/chat")
async def chat(request: ChatRequest):
    """Main chat endpoint - handles both mock and OpenAI modes"""
    user_message = request.message
    mode = request.mode
    
    # Step 1: Check if we need to call MCP tools
    tool_result = detect_intent_and_call_tool(user_message)
    
    # Step 2: Prepare context for LLM
    system_context = """You are an AI assistant for INSTRAT360, an agentic AI strategy platform.

You have access to these MCP tools:
- get_company_overview: Get company information
- list_all_employees: Get list of employees
- get_employee_details: Get specific employee info
- get_project_details: Get project information
- find_expert: Find expert by skill

When you receive tool results, provide a natural, conversational response based on that data.
Keep responses clear, friendly, and informative."""
    
    if tool_result:
        system_context += f"\n\nTool Result: {format_tool_response(tool_result)}"
    
    # Step 3: Generate response
    try:
        if mode == "openai" and request.api_key and LANGCHAIN_AVAILABLE:
            # Use OpenAI - Simple approach with tool results injected
            llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                api_key=request.api_key,
                temperature=0.7
            )
            
            # If we detected a tool should be called, include the result
            if tool_result:
                enhanced_context = f"""{system_context}

The user asked: "{user_message}"

I've already retrieved this information from our MCP tools:
{format_tool_response(tool_result)}

Please provide a natural, friendly response based on this data. Format it nicely and be conversational."""
                
                messages = [
                    SystemMessage(content=enhanced_context),
                    HumanMessage(content="Please provide a response based on the tool data above.")
                ]
            else:
                messages = [
                    SystemMessage(content=system_context),
                    HumanMessage(content=user_message)
                ]
            
            response = llm.invoke(messages)
            ai_response = response.content
            
        else:
            # Mock mode - simple rule-based responses
            if tool_result:
                if "employees" in str(tool_result):
                    ai_response = f"Here's the information about our team:\n{format_tool_response(tool_result)}"
                elif "name" in str(tool_result) and "INSTRAT360" in str(tool_result):
                    ai_response = f"Let me tell you about INSTRAT360:\n\n{COMPANY_INFO['overview']}\n\nOur mission: {COMPANY_INFO['mission']}"
                elif "project" in str(tool_result):
                    ai_response = f"Here's the project information:\n{format_tool_response(tool_result)}"
                elif "expert" in str(tool_result):
                    ai_response = f"I found these experts:\n{format_tool_response(tool_result)}"
                else:
                    ai_response = f"Here's what I found:\n{format_tool_response(tool_result)}"
            else:
                ai_response = "I'm the INSTRAT360 assistant! I can help you with:\n- Company overview\n- Employee information\n- Project details\n- Finding experts\n\nWhat would you like to know?"
        
        return JSONResponse(content={
            "response": ai_response,
            "tool_called": tool_result is not None,
            "tool_result": tool_result,
            "mode": mode
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "INSTRAT360 Chatbot"}

# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting INSTRAT360 Chatbot Server...")
    print("📍 Open browser: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)