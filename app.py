import streamlit as st
import requests
import os
from dotenv import load_dotenv
import time
# ── Environment variables load karo ──────────────────────────────────────────
load_dotenv()

API_KEY  = os.getenv("CRM_API_KEY")
BASE_URL = os.getenv("CRM_BASE_URL")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type":  "application/json"
}

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales CRM Assistant",
    page_icon="🏢",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 6px 18px;
        font-weight: 500;
    }
    .success-box {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 8px;
        padding: 12px 16px;
        color: #166534;
        font-size: 14px;
    }
    .error-box {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 8px;
        padding: 12px 16px;
        color: #991b1b;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 8])
with col1:
    st.markdown("## 🏢")
with col2:
    st.markdown("## Sales CRM Assistant")
    st.caption("Powered by FastMCP + HubSpot")

# Server status check
if API_KEY and BASE_URL:
    st.success("🟢 Server ready — credentials loaded", icon=None)
else:
    st.error("🔴 .env file mein CRM_API_KEY ya CRM_BASE_URL missing hai!")

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_search, tab_note, tab_tools = st.tabs(["🔍 Search Lead", "📝 Log Note", "⚙️ Tools"])


# ── Tab 1: Search Lead ────────────────────────────────────────────────────────
with tab_search:
    st.markdown("**`search_lead(email: str)`** — HubSpot contacts/search")
    st.markdown("")

    email = st.text_input(
        "Contact email address",
        placeholder="contact@company.com",
        key="search_email"
    )

    if st.button("🔍 Search CRM", type="primary", key="btn_search"):
        if not email or "@" not in email:
            st.error("Valid email address enter karo.")
        else:
            with st.spinner(f'"{email}" search ho raha hai HubSpot mein...'):
                try:
                    url     = f"{BASE_URL}/objects/contacts/search"
                    payload = {
                        "filterGroups": [{
                            "filters": [{
                                "propertyName": "email",
                                "operator":     "EQ",
                                "value":        email
                            }]
                        }]
                    }
                    response = requests.post(url, json=payload, headers=HEADERS)

                    if response.status_code == 200:
                        data = response.json()
                        if data.get("results"):
                            st.success("✅ Lead mil gaya!")
                            st.json(data["results"])
                        else:
                            st.warning("⚠️ Is email se koi lead nahi mila.")
                    else:
                        st.error(f"❌ Error: {response.text}")

                except Exception as e:
                    st.error(f"❌ CRM se connect nahi ho saka: {str(e)}")

    # Code reference
    with st.expander("📄 server.py reference dekho"):
        st.code("""
# server.py → search_lead()
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
        """, language="python")


# ── Tab 2: Log Note ───────────────────────────────────────────────────────────
with tab_note:
    st.markdown("**`log_sales_note(contact_id, note_content)`** — HubSpot objects/notes")
    st.markdown("")

    contact_id   = st.text_input("Contact ID", placeholder="e.g. 12345678", key="note_cid")
    note_content = st.text_area(
        "Meeting summary / sales note",
        placeholder="Called the lead, discussed pricing. Follow-up scheduled for Monday...",
        height=120,
        key="note_content"
    )

    if st.button("📝 Log Note to CRM", type="primary", key="btn_note"):
        if not contact_id:
            st.error("Contact ID khali nahi hona chahiye.")
        elif not note_content:
            st.error("Note content khali nahi hona chahiye.")
        else:
            with st.spinner(f"Contact {contact_id} ke liye note log ho raha hai..."):
                try:
                    url     = f"{BASE_URL}/objects/notes"
                    payload = {
                        "properties": {
                            "hs_note_body":  note_content,
                            "hs_timestamp":  int(time.time() * 1000)
                        },
                        "associations": [{
                            "to":    {"id": contact_id},
                            "types": [{
                                "associationCategory": "HUBSPOT_DEFINED",
                                "associationTypeId":   202
                            }]
                        }]
                    }
                    response = requests.post(url, json=payload, headers=HEADERS)

                    if response.status_code == 201:
                        st.success(f"✅ Note successfully logged for contact ID {contact_id}!")
                        st.json(response.json())
                    else:
                        st.error(f"❌ Note log nahi hua: {response.text}")

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    with st.expander("📄 server.py reference dekho"):
        st.code("""
# server.py → log_sales_note()
url = f"{BASE_URL}/objects/notes"
payload = {
    "properties": {
        "hs_note_body": note_content,
        "hs_timestamp": "now"
    },
    "associations": [{
        "to": {"id": contact_id},
        "types": [{
            "associationCategory": "HUBSPOT_DEFINED",
            "associationTypeId": 202
        }]
    }]
}
response = requests.post(url, json=payload, headers=HEADERS)
        """, language="python")


# ── Tab 3: Tools Info ─────────────────────────────────────────────────────────
with tab_tools:
    st.markdown("#### Registered MCP Tools")

    col_a, col_b = st.columns(2)
    with col_a:
        st.info("**🔍 search_lead**\n\nFind contact by email in HubSpot CRM")
    with col_b:
        st.info("**📋 log_sales_note**\n\nLog meeting summary to a CRM contact")

    st.markdown("#### Server Configuration")
    st.table({
        "Property":  ["Framework", "CRM",      "Auth",              "Tools registered", "Entry point"],
        "Value":     ["FastMCP",   "HubSpot",  "Bearer token (.env)", "2",              "mcp.run()"]
    })