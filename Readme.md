# 🚀 AI-Powered Custom HubSpot CRM MCP Server

A custom Python-based **Model Context Protocol (MCP)** server that seamlessly integrates enterprise HubSpot CRM with the **Claude Desktop** application. This project enables sales teams and developers to interact with CRM data conversationally using natural language directly inside their AI workspace.

---

## 🌟 Key Features
- **Model Context Protocol (MCP):** Built using the official MCP Python SDK to expose secure custom tools for AI models.
- **HubSpot API Integration:** Powered by a HubSpot Private App ("Stout-Juice") utilizing Personal Access Tokens (PAT) for secure data retrieval.
- **Natural Language CRM Queries:** Fetch contacts, search leads, and query client history simply by chatting with Claude.
- **Seamless Local Architecture:** Runs locally via a Python virtual environment and connects directly to Claude Desktop background processes.

---

## 🛠️ Tech Stack
- **Language:** Python
- **Protocol:** Model Context Protocol (MCP) SDK
- **API & Auth:** HubSpot Private App API, Personal Access Token (PAT)
- **Environment:** VS Code, Postman (API Testing), Claude Desktop

---

## 📁 Project Structure
```text
sales-crm-mcp project/
├── venv/                   # Python Virtual Environment
├── .env                    # Environment variables (API Keys - Git ignored)
├── server.py               # Main MCP server script handling HubSpot API
├── requirements.txt        # Project dependencies
└── README.md               # Project 


⚙️ Installation & Setup
Clone the Repository:

Clone the Repository:

git clone [https://github.com/techbased708-crypto/hubspot-mcp-server.git](https://github.com/techbased708-crypto/hubspot-mcp-server.git)
cd sales-crm-mcp-project

Set up Virtual Environment:
python -m venv venv
source venv/Scripts/activate  # On Windows

Install Dependencies:
pip install -r requirements.txt

Configure Environment Variables:
Create a .env file in the root directory and add your HubSpot credentials:

CRM_API_KEY=your_hubspot_pat_here
CRM_BASE_URL=[https://api.hubapi.com](https://api.hubapi.com)

Configure Claude Desktop:
Add your server path to your Claude configuration file (%APPDATA%\Claude\claude_desktop_config.json):

{
  "mcpServers": {
    "sales-crm-mcp": {
      "command": "C:\\Users\\your-username\\Desktop\\sales-crm-mcp project\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\your-username\\Desktop\\sales-crm-mcp project\\server.py"
      ]
    }
  }
}

💡 Usage
Open Claude Desktop and start querying your CRM data naturally:

"Find contacts in my HubSpot CRM"
"Search for lead details in HubSpot"


