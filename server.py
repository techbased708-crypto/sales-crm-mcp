import os
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

API_KEY = os.getenv("CRM_API_KEY")
BASE_URL = os.getenv("CRM_BASE_URL")

# Initialize FastMCP server
mcp = FastMCP("Sales CRM Assistant")

# Helper headers for API requests
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@mcp.tool()
def search_lead(email: str) -> str:
    """Search for a lead or contact in the CRM by their email address."""
    try:
        # Example endpoint structure (adjust based on your CRM like HubSpot/Salesforce)
        url = f"{BASE_URL}/objects/contacts/search"
        payload = {
            "filterGroups": [{
                "filters": [{
                    "propertyName": "email",
                    "operator": "EQ",
                    "value": email
                }]
            }]
        }
        response = requests.post(url, json=payload, headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("results"):
                return f"Lead Found: {data['results']}"
            return "No lead found with this email."
        else:
            return f"Error searching lead: {response.text}"
    except Exception as e:
        return f"Failed to connect to CRM: {str(e)}"

@mcp.tool()
def log_sales_note(contact_id: str, note_content: str) -> str:
    """Log a meeting summary or sales note to a specific contact in the CRM."""
    try:
        url = f"{BASE_URL}/objects/notes"
        payload = {
            "properties": {
                "hs_note_body": note_content,
                "hs_timestamp": "now"
            },
            "associations": [{
                "to": {"id": contact_id},
                "types": [{"associationCategory": "HUBSPOT_DEFINED", "associationTypeId": 202}]
            }]
        }
        response = requests.post(url, json=payload, headers=HEADERS)
        
        if response.status_code == 201:
            return f"Successfully logged note for contact ID {contact_id}."
        else:
            return f"Failed to log note: {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()