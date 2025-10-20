from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import os
from typing import Optional
import httpx


try:
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("Warning: LangChain not available. Only mock mode will work.")

app = FastAPI(title="INSTRAT360 Chatbot")

app.mount("/static", StaticFiles(directory="static"), name="static")


# MCP SERVER DATA (Mock Mode)


COMPANY_INFO = {
    "name": "INSTRAT360",
    "tagline": "Unified Agentic AI Platform Built for Strategic Value Creation",
    "overview": "INSTRAT360 is a market-leading agentic AI strategy platform that integrates real-time AI reasoning, data logic, and dynamic strategy execution.",
    "mission": "To empower organizations with adaptable, actionable, and aligned strategies powered by agentic AI."
}

EMPLOYEES = {
    "Asbjørn Levring": {
        "role": "Founder & CEO ",
        "department": "Operations",
        "expertise": ["Strategic Planning", "Agentic AI", "Operational Efficiency", "AI Integration"]
    },
    "Mahmud Hasan": {
        "role": "CTO & AI Architect",
        "department": "Technology",
        "expertise": ["AI Architecture", "System Design"]
    },
    "Fahim": {
        "role": "Head of AI",
        "department": "AI",
        "expertise": ["Mlops" ,"LLM","Consulting", "AI system Design"]
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


# MCP TOOL FUNCTIONS


def get_company_overview():
    return COMPANY_INFO

def get_employee_details(name: str):
    if name not in EMPLOYEES:
        return {"error": f"Employee '{name}' not found", "available": list(EMPLOYEES.keys())}
    return {"name": name, **EMPLOYEES[name]}

def list_all_employees():
    result = []
    for name, info in EMPLOYEES.items():
        result.append({"name": name, "role": info["role"], "department": info["department"]})
    return {"employees": result, "total": len(result)}

def get_project_details(project_name: str):
    if project_name not in PROJECTS:
        return {"error": f"Project '{project_name}' not found", "available": list(PROJECTS.keys())}
    return {"project": project_name, **PROJECTS[project_name]}

def find_expert(skill: str):
    matches = []
    for name, info in EMPLOYEES.items():
        if any(skill.lower() in exp.lower() for exp in info["expertise"]):
            matches.append({"name": name, "role": info["role"], "expertise": info["expertise"]})
    
    if not matches:
        return {"message": f"No expert found for '{skill}'", "experts": []}
    return {"skill": skill, "experts": matches}


# All TOOL 

AVAILABLE_TOOLS = {
    "get_company_overview": get_company_overview,
    "get_employee_details": get_employee_details,
    "list_all_employees": list_all_employees,
    "get_project_details": get_project_details,
    "find_expert": find_expert
}

def call_mcp_tool(tool_name: str, **kwargs):
   
    if tool_name not in AVAILABLE_TOOLS:
        return {"error": f"Tool '{tool_name}' not found"}
    
    tool_func = AVAILABLE_TOOLS[tool_name]
    try:
        return tool_func(**kwargs)
    except Exception as e:
        return {"error": str(e)}



def format_employee_list(data):
    if "employees" not in data:
        return str(data)
    
    response = f"**Our Team ({data['total']} members)**\n\n"
    for emp in data["employees"]:
        response += f" **{emp['name']}**\n"
        response += f"    *{emp['role']}*\n"
        response += f"    {emp['department']}\n\n"
    
    return response.strip()

def format_employee_details(data):
    if "error" in data:
        return f" {data['error']}"
    
    response = f" **{data['name']}**\n\n"
    response += f"**Role:** {data['role']}\n"
    response += f"**Department:** {data['department']}\n"
    
    if "expertise" in data:
        response += f"**Expertise:**\n"
        for skill in data["expertise"]:
            response += f"  • {skill}\n"
    
    return response.strip()

def format_company_overview(data):
    
    response = f" **{data['name']}**\n\n"
    response += f"*{data['tagline']}*\n\n"
    response += f"**Overview:**\n{data['overview']}\n\n"
    response += f"**Mission:**\n{data['mission']}"
    
    return response

def format_project_details(data):
    if "error" in data:
        return f" {data['error']}"
    
    response = f" **Project: {data['project']}**\n\n"
    response += f"**Owner:** {data['owner']}\n"
    response += f"**Status:** {data['status']}\n"
    response += f"**Progress:** {data['progress']}%\n"
    
    
    filled = int(data['progress'] / 10)
    empty = 10 - filled
    progress_bar = "" * filled + "" * empty
    response += f"\n{data['progress']}%"
    
    return response

def format_all_projects(data):
    if "projects" not in data:
        return str(data)
    
    response = "**Active Projects**\n\n"
    for proj_name, proj_info in data["projects"].items():
        response += f"**{proj_name}**\n"
        response += f"  Owner: {proj_info['owner']}\n"
        response += f"  Status: {proj_info['status']}\n"
        
        filled = int(proj_info['progress'] / 10)
        empty = 10 - filled
        progress_bar = "=" * filled + "=" * empty
        response += f"  Progress:{proj_info['progress']}%\n\n"
    
    return response.strip()

def format_expert_search(data):
    
    if "experts" not in data or len(data["experts"]) == 0:
        return f"No experts found for the specified skill."
    
    response = f"**Experts in {data.get('skill', 'this area')}:**\n\n"
    for expert in data["experts"]:
        response += f" **{expert['name']}**\n"
        response += f"    *{expert['role']}*\n"
        response += f"    Expertise: {', '.join(expert['expertise'])}\n\n"
    
    return response.strip()

def format_tool_response(data, tool_name=None):
    if isinstance(data, dict):
        if "error" in data:
            return f" {data['error']}"
        
        if "employees" in data and isinstance(data["employees"], list):
            return format_employee_list(data)
        
        if "name" in data and "role" in data and "department" in data:
            return format_employee_details(data)
        
        if "name" in data and data.get("name") == "INSTRAT360":
            return format_company_overview(data)
        
        if "project" in data and "owner" in data:
            return format_project_details(data)
       
        if "projects" in data and isinstance(data["projects"], dict):
            return format_all_projects(data)
        
        if "experts" in data:
            return format_expert_search(data)
    
    return str(data)


def detect_intent_and_call_tool(user_message: str):
    
    msg_lower = user_message.lower()
    
    # Company overview detection
    if any(word in msg_lower for word in ["company", "overview", "about instrat360", "what is","instrat360"]):
        return call_mcp_tool("get_company_overview"), "get_company_overview"
    
    # Employee list detection
    if any(word in msg_lower for word in ["employees", "team", "staff", "who works", "list people", "members","team member"]):
        return call_mcp_tool("list_all_employees"), "list_all_employees"
    
    # Specific employee detection
    for emp_name in EMPLOYEES.keys():
        if emp_name.lower() in msg_lower:
            return call_mcp_tool("get_employee_details", name=emp_name), "get_employee_details"
    
    # Project detection
    if any(word in msg_lower for word in ["project", "projects"]):
        for proj_name in PROJECTS.keys():
            if any(word in msg_lower for word in proj_name.lower().split()):
                return call_mcp_tool("get_project_details", project_name=proj_name), "get_project_details"
        # Return all projects if no specific project mentioned
        return {"projects": PROJECTS}, "list_all_projects"
    
 
    if any(word in msg_lower for word in ["expert", "who knows", "specialist"]):
        for skill in ["strategy", "ai", "consulting", "architecture", "design"]:
            if skill in msg_lower:
                return call_mcp_tool("find_expert", skill=skill), "find_expert"
    
    return None, None



class ChatRequest(BaseModel):
    message: str
    mode: str = "mock"  # "openai" or "mock"
    api_key: Optional[str] = None



@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.message
    mode = request.mode
    
   
    tool_result, tool_name = detect_intent_and_call_tool(user_message)
    
   
    system_context = """You are an AI assistant for INSTRAT360, an agentic AI strategy platform.

                        You have access to these MCP tools:
                        - get_company_overview: Get company information
                        - list_all_employees: Get list of employees
                        - get_employee_details: Get specific employee info
                        - get_project_details: Get project information
                        - find_expert: Find expert by skill

                        When you receive tool results, provide a natural, conversational response based on that data.
                        Keep responses clear, friendly, and informative."""
    
    
    try:
        if mode == "openai" and request.api_key and LANGCHAIN_AVAILABLE:
           
            llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                api_key=request.api_key,
                temperature=0.7
            )
            
            if tool_result:
                formatted_data = format_tool_response(tool_result, tool_name)
                enhanced_context = f"""{system_context}

The user asked: "{user_message}"

I've already retrieved this information from our MCP tools:
{formatted_data}

Please provide a natural, friendly response based on this data. The data is already well-formatted, so you can present it directly or add some context."""
                
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
            
            if tool_result:
                ai_response = format_tool_response(tool_result, tool_name)
            else:
                ai_response = "I'm the INSTRAT360 assistant! I can help you with:\n\n• Company overview\n• Employee information\n• Project details\n• Finding experts\n\nWhat would you like to know?"
        
        return JSONResponse(content={
            "response": ai_response,
            "tool_called": tool_result is not None,
            "tool_result": tool_result,
            "mode": mode
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/developer")
async def developer():
    return {"Developer": "Md Al Amin Tokder", "project": "INSTRAT360 Chatbot"}


if __name__ == "__main__":
    import uvicorn
    print("Starting INSTRAT360 Chatbot Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)