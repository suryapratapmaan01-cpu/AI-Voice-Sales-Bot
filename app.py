import streamlit as st
from supabase import create_client, Client

# --- PAGE LAYOUT & STYLING ---
st.set_page_config(page_title="AI Sales Bot Control Center", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    h1 { color: #4F46E5; }
    .report-box { padding: 15px; border-radius: 8px; border: 1px solid #E5E7EB; background: #FFFFFF; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- CONNECT TO YOUR DATABASE ---
# Replace these strings with your actual Supabase credentials
SUPABASE_URL = "https://anugthjpsyyqxdxeezpf.supabase.co" 
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFudWd0aGpwc3l5cXhkeGVlenBmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5MjU2ODg2MSwiZXhwIjoyMTA4MTQ0ODYxfQ.QYx_88LFw0pNnSQQrnfSZbPgatm3oZVDzrkAyk5FF-0"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- HEADER ---
st.title("💼 AI Voice Sales Agent Dashboard")
st.caption("Live Interactive Voice Stream & Automated CRM Logs")
st.markdown("---")

col_call, col_history = st.columns([1, 1])

# --- LEFT COLUMN: LIVE CHAT AND INTERACTIVE WIDGET ---
with col_call:
    st.subheader("📞 Live Call Control Center")
    st.info("Click 'Start Call' inside the console below to instantly speak with our multilingual sales executive.")

    # Paste your Retell AI Shareable Link inside this iframe to present it beautifully
    retell_shareable_link = "https://agent.retellai.com/orb/agent_245dce37711bd07c83337fbf28?token=b972f5dc0a3c3586a098b09d2615e955"

    st.components.v1.iframe(retell_shareable_link, height=450, scrolling=True)

# --- RIGHT COLUMN: REAL-TIME CALL HISTORY ---
with col_history:
    st.subheader("📊 Historical Logs & AI Evaluations")

    # Fetch the latest call history from your working table
    try:
        response = supabase.table("call_history").select("*").order("created_at", desc=True).execute()
        records = response.data
    except Exception as e:
        records = []

    if not records:
        st.warning("Awaiting first test call logs... Once your Make.com automation runs, the records will appear here instantly!")
    else:
        for record in records:
            with st.container():
                st.markdown(f"""
                <div class="report-box">
                    <h4>🕒 <b>Date:</b> {record.get('created_at', 'N/A')[:16]} | ⏳ <b>Duration:</b> {record.get('duration', '0')}s</h4>
                    <p>🤖 <b>AI Raw Insights:</b> {record.get('summary', 'Processing text transcript...')}</p>
                </div>
                """, unsafe_allow_html=True)
                if record.get('recording_url'):
                    st.audio(record['recording_url'], format="audio/mp3")
