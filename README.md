# instrat360-task

# INSTRAT360 MCP Chatbot Project

I create a simple chatbot application that demonstrates **Model Context Protocol (MCP)** integration with AI assistants. The chatbot can answer questions about INSTRAT360 company using MCP tools for data retrieval.

## Features
- **AI Chatbot**:
  - Chat with AI about INSTRAT360 company
  - Automatic MCP tool calling when needed
  - Two modes: Mock (no API key) and OpenAI (with API key)
  - Clean UI (I use HTML,CSS,JS for simplicity)

- **MCP Server** with 3 core capabilities:
  - **Resources**: Company info, employee list, project list
  - **Tools**: 5 callable functions (company overview, employee details, etc.)
  - **Prompts**: 3 pre-defined templates for analysis


## Technology i use:

- **fastmcp**: MCP server framework
- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **langchain**: LLM orchestration
- **langchain-openai**: OpenAI integration
- **httpx**: HTTP client
- **python-dotenv**: Environment variable management



## Project Structure

```
instrat360-mcp-task/
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── mcp_server/
│   └── mcp_server.py        # MCP server with resources, tools, prompts
└── web_server/
    ├── main.py              # FastAPI web server
    └── static/
        └── index.html       # Chat UI (HTML + CSS + JS)
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- uv (Python package manager)

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd instrat360-mcp-task
```

### Step 2: Create virtual environment and install Dependencies

```bash
uv venv
source .venv/bin/activate (For MAC OS)
uv pip install -r requirements.txt
```

### Step 3: Run the MCP Server (Optional - for testing)

The MCP server can run independently for testing:

```bash
cd mcp_server
uv run mcp_server.py
```

This will start the FastMCP server on the default port.

### Step 4: Run the Web Server
Create a new terminal and then go to web_server directory

```bash
cd web_server
python3 main.py
```


### Step 5: Open the Chatbot

Open your browser and go to:

```
http://localhost:8000
```

--- 

## 🎮 Usage Guide

### Mock Mode (No API Key Required)

1. Select **"Mock Mode"** (default)
2. Type your question in the chat input
3. The bot uses rule-based logic to detect intent and call MCP tools
4. Responses are formatted naturally

**Example Questions:**
- "Tell me about INSTRAT360"
- "Who are the employees?"
- "What is Sarah Chen's role?"
- "Show me the projects"
- "Find an AI expert"

### OpenAI Mode (Requires API Key)

1. Select **"OpenAI Mode"**
2. Enter your OpenAI API key
3. Type your question
4. The bot uses GPT-3.5-turbo for natural language understanding
5. MCP tools are automatically called when needed



## 🔧 MCP Capabilities Demonstration

### 1. Resources (Read-only data endpoints)

```python
@mcp.resource("company://info")
def get_company_resource():
    """Returns company information"""
    
@mcp.resource("company://employees")
def get_employees_resource():
    """Returns list of employees"""
    
@mcp.resource("company://projects")
def get_projects_resource():
    """Returns list of projects"""
```

### 2. Tools (Callable functions)

```python
@mcp.tool()
def get_company_overview():
    """Get complete company overview"""
    
@mcp.tool()
def get_employee_details(name: str):
    """Get specific employee information"""
    
@mcp.tool()
def list_all_employees():
    """List all employees with roles"""
    
@mcp.tool()
def get_project_details(project_name: str):
    """Get specific project information"""
    
@mcp.tool()
def find_expert(skill: str):
    """Find employees by expertise area"""
```

### 3. Prompts (Pre-defined templates)

```python
@mcp.prompt()
def company_analysis_prompt():
    """Template for company analysis"""
    
@mcp.prompt()
def employee_expertise_prompt():
    """Template for finding experts"""
    
@mcp.prompt()
def project_status_prompt():
    """Template for project reviews"""
```



## Environment Variables (Optional)

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=""
```





##  How MCP Tools Are Called

The system uses **intent detection** to automatically call the right MCP tool:

| User Query | Detected Intent | MCP Tool Called |
|------------|----------------|-----------------|
| "Tell me about INSTRAT360" | Company info | `get_company_overview()` |
| "Who are the employees?" | Employee list | `list_all_employees()` |
| "Who is Sarah Chen?" | Specific employee | `get_employee_details("Sarah Chen")` |
| "What projects exist?" | Project list | Returns all projects |
| "Find an AI expert" | Expert search | `find_expert("AI")` |
