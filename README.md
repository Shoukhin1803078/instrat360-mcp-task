# instrat360-task

# INSTRAT360 MCP Chatbot Project

I create a simple chatbot AI assistant for **INSTRAT360** company with **Model Context Protocol (MCP)** integration . The chatbot can answer questions about INSTRAT360 company using MCP tools for data retrieval.

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
├── requirements.txt          
├── README.md                
├── mcp_server/
│   └── mcp_server.py        # Here I define MCP server with resources, tools, prompts
└── web_server/
    ├── main.py              # FastAPI web server
    └── static/
        └── index.html       # Chat UI (HTML + CSS + JS)
```

## Setup Instructions

### Prerequisites
- requires-python = ">=3.12"
- uv (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Shoukhin1803078/instrat360-mcp-task.git
cd instrat360-mcp-task
```

### Step 2: Create virtual environment and install Dependencies

```bash
uv venv
source .venv/bin/activate (For MAC OS)
uv pip install -r requirements.txt
```

### Step 3: Run the MCP Server 

The MCP server can run independently for testing:

```bash
cd mcp_server
uv run mcp_server.py
```

This will start the FastMCP server on the default port.

### Step 4: Run the Web Server in another terminal
Create a new terminal and then go to web_server directory

```bash
cd web_server
python3 main.py
```


### Step 5: Open the Chatbot

Open browser and go to:

```
http://localhost:8000
```

--- 

# Sample Output
<img width="1710" height="1107" alt="Screenshot 2025-10-20 at 11 20 17 PM" src="https://github.com/user-attachments/assets/c2927dd2-1697-49ef-97dd-6b21b6f6c1a1" />
<img width="1710" height="1107" alt="Screenshot 2025-10-20 at 11 27 47 PM" src="https://github.com/user-attachments/assets/197fbcab-73f0-4e25-b1c0-ce4bcc8fe365" />
<img width="1710" height="1107" alt="Screenshot 2025-10-20 at 10 54 38 PM" src="https://github.com/user-attachments/assets/2de394ff-f6a0-45e0-affe-23a78bc272c0" />
<img width="1710" height="1107" alt="Screenshot 2025-10-20 at 10 56 26 PM" src="https://github.com/user-attachments/assets/b443b9ff-a50b-47e7-bf7f-4136e6129d50" />
<img width="1710" height="1107" alt="Screenshot 2025-10-20 at 10 56 38 PM" src="https://github.com/user-attachments/assets/6344c92d-b10a-4870-9d84-318755c7f892" />
<img width="1710" height="1107" alt="Screenshot 2025-10-20 at 10 56 58 PM" src="https://github.com/user-attachments/assets/b0566cfa-02e0-4383-9d8d-cc81217aaa27" />
<img width="1710" height="1107" alt="Screenshot 2025-10-20 at 11 00 11 PM" src="https://github.com/user-attachments/assets/8d62c404-a0f0-4760-bbe1-533f51f5de09" />
<img width="1710" height="1107" alt="Screenshot 2025-10-20 at 11 00 40 PM" src="https://github.com/user-attachments/assets/1c0cfc21-8450-4d37-8a7b-3f23040e521e" />
<img width="1710" height="1107" alt="Screenshot 2025-10-20 at 11 01 00 PM" src="https://github.com/user-attachments/assets/9b645636-2eb5-4f0b-8f38-98153ac975cb" />
<img width="1710" height="1107" alt="Screenshot 2025-10-20 at 11 01 34 PM" src="https://github.com/user-attachments/assets/60ab8182-7944-48f5-8228-f93883ec69fd" />
<img width="1710" height="1107" alt="Screenshot 2025-10-20 at 11 03 29 PM" src="https://github.com/user-attachments/assets/61e22f4c-ab33-4f56-b5ce-b57b1f4a2583" />
<img width="1710" height="1107" alt="Screenshot 2025-10-20 at 11 03 42 PM" src="https://github.com/user-attachments/assets/7df754a5-e35c-4d2b-bf51-a85fb84c5345" />



---

##  Usage Guide

### Mock Mode (No API Key Required)

1. Select **"Mock Mode"** (default)
2. Type question in the chat input
3. The bot uses rule-based logic to detect intent and call MCP tools
4. Responses are formatted naturally

**Example Questions:**
- "Tell me about INSTRAT360"
- "Who are the employees?"
- "Show me the projects"
- "Find an AI expert"

### OpenAI Mode (Requires API Key)

1. Select **"OpenAI Mode"**
2. Enter OpenAI API key
3. Type question
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
| "What projects exist?" | Project list | Returns all projects |
| "Find an AI expert" | Expert search | `find_expert("AI")` |
