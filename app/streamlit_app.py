
import streamlit as st
import requests
import time
import os

# ========= CONFIG =========
# Read backend URL from env first; try secrets only if present; fallback to local
FASTAPI_BASE_URL = os.environ.get("FASTAPI_BASE_URL")
if not FASTAPI_BASE_URL:
    try:
        FASTAPI_BASE_URL = st.secrets["FASTAPI_BASE_URL"]
    except Exception:
        FASTAPI_BASE_URL = "http://127.0.0.1:8000"

# Default timeout; adjustable in UI
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", "600"))  # seconds

# ========= PAGE SETTINGS =========
st.set_page_config(page_title="HR Agent Dashboard", layout="wide")
st.title("🧠 HR Agent Dashboard")

# ========= UPLOAD SECTION =========
st.header("📤 Upload Resumes, JDs, and Optional Template")

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    resumes = st.file_uploader(
        "Upload up to 5 Resumes (PDF or DOCX)", type=["pdf", "docx"], key="resumes", accept_multiple_files=True
    )
    
    jds = st.file_uploader(
        "Upload up to 2 Job Descriptions (PDF or DOCX) - optional",
        type=["pdf", "docx"], key="jds", accept_multiple_files=True
    )

with col2:
    use_default_template = st.checkbox(
        "Use default template (recommended if you don't have a template)", value=True
    )
    template_file = None
    if not use_default_template:
        template_file = st.file_uploader(
            "Optional resume template (DOCX/PDF)", type=["docx", "pdf"], key="template_file"
        )

if "stage" not in st.session_state:
    st.session_state.stage = 0

# ========= UTILS =========
def show_progress(stage: int):
    steps = ["Uploading", "Running AI Pipeline", "Fetching Results", "Complete"]
    for idx, step in enumerate(steps):
        icon = "🔄" if stage == idx else "✅" if stage > idx else "⬜"
        st.markdown(f"{icon} {step}")

def download_file_from_fastapi(endpoint: str, filename: str):
    """GET a file from FastAPI and return bytes for Streamlit's download_button."""
    url = f"{FASTAPI_BASE_URL}{endpoint}"
    try:
        r = requests.get(url, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            return r.content, filename
        else:
            # Try to show JSON error if backend sent one
            try:
                err = r.json().get("error", r.text)
            except Exception:
                err = r.text
            st.error(f"❌ Failed to fetch from {endpoint}: {err}")
            return None, None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Network error fetching {endpoint}: {e}")
        return None, None

def try_upload_to_backend(resumes, jds, template_file, use_default_template: bool):
    """Try plural field names first (new API), then fallback to singular (old API)."""
    # Build plural multipart
    plural_multipart = []
    for r in resumes:
        plural_multipart.append((
            "resumes",
            (r.name, r.getvalue(), r.type or "application/octet-stream")
        ))
    if jds:
        for j in jds:
            plural_multipart.append((
                "jds",
                (j.name, j.getvalue(), j.type or "application/octet-stream")
            ))
    if (not use_default_template) and template_file is not None:
        plural_multipart.append((
            "template_file",
            (
                template_file.name,
                template_file.getvalue(),
                template_file.type or "application/octet-stream",
            ),
        ))

    # Try plural API first
    try:
        url = f"{FASTAPI_BASE_URL}/upload?use_default_template={str(use_default_template).lower()}"
        r = requests.post(url, files=plural_multipart, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            return r.json(), None
        else:
            error_msg = f"Plural API failed: {r.status_code} - {r.text}"
    except Exception as e:
        error_msg = f"Plural API error: {e}"

    # Fallback to singular API (old format)
    try:
        singular_multipart = []
        if resumes:
            singular_multipart.append((
                "resume",
                (resumes[0].name, resumes[0].getvalue(), resumes[0].type or "application/octet-stream")
            ))
        if jds:
            singular_multipart.append((
                "jd",
                (jds[0].name, jds[0].getvalue(), jds[0].type or "application/octet-stream")
            ))
        
        url = f"{FASTAPI_BASE_URL}/upload"
        r = requests.post(url, files=singular_multipart, timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            return r.json(), None
        else:
            return None, f"Singular API also failed: {r.status_code} - {r.text}"
    except Exception as e:
        return None, f"Singular API error: {e}"

# ========= MAIN UPLOAD LOGIC =========
if st.button("🚀 Start Processing", type="primary"):
    if not resumes:
        st.error("❌ Please upload at least one resume.")
    else:
        st.session_state.stage = 0
        show_progress(0)
        
        with st.spinner("📤 Uploading files..."):
            result, error = try_upload_to_backend(resumes, jds, template_file, use_default_template)
            
            if error:
                st.error(f"❌ Upload failed: {error}")
                st.session_state.stage = 0
            else:
                st.session_state.stage = 1
                show_progress(1)
                
                # Show pipeline results
                if "pipeline_result" in result:
                    st.success("✅ Pipeline completed successfully!")
                    
                    # Display pipeline results in a clean format
                    pipeline_result = result["pipeline_result"]
                    st.subheader("📊 Pipeline Results")
                    
                    # Create a nice display of results
                    result_cols = st.columns(2)
                    with result_cols[0]:
                        st.metric("Resumes Processed", len(result.get("resumes_saved", [])))
                        st.metric("JDs Processed", len(result.get("jds_saved", [])) if result.get("jds_saved") != "No JDs uploaded" else 0)
                    
                    with result_cols[1]:
                        successful_steps = sum(1 for step, status in pipeline_result.items() if status == "success")
                        total_steps = len(pipeline_result)
                        st.metric("Steps Completed", f"{successful_steps}/{total_steps}")
                        st.metric("Session Isolated", "✅ Yes" if result.get("session_isolated", False) else "❌ No")
                    
                    # Show detailed step results
                    st.subheader("🔍 Step Details")
                    for step, status in pipeline_result.items():
                        icon = "✅" if status == "success" else "❌" if status == "failed" else "⚠️"
                        st.write(f"{icon} {step.replace('_', ' ').title()}: {status}")
                    
                    st.session_state.stage = 2
                    show_progress(2)
                    
                    # Show download options
                    st.session_state.stage = 3
                    show_progress(3)
                    
                    st.subheader("📥 Download Results")
                    
                    # Download buttons in columns
                    download_col1, download_col2 = st.columns(2)
                    
                    with download_col1:
                        if st.button("📄 Download Tailored CVs (ZIP)", type="secondary"):
                            content, filename = download_file_from_fastapi("/download/tailored-cv-docx", "tailored_cvs.zip")
                            if content:
                                st.download_button(
                                    label="💾 Save Tailored CVs ZIP",
                                    data=content,
                                    file_name=filename,
                                    mime="application/zip"
                                )
                    
                    with download_col2:
                        if st.button("📊 Download Rankings PDF", type="secondary"):
                            content, filename = download_file_from_fastapi("/download/rankings-pdf", "job_rankings.pdf")
                            if content:
                                st.download_button(
                                    label="💾 Save Rankings PDF",
                                    data=content,
                                    file_name=filename,
                                    mime="application/pdf"
                                )
                    
                    # List tailored CVs
                    st.subheader("📋 Generated Tailored CVs")
                    try:
                        cv_response = requests.get(f"{FASTAPI_BASE_URL}/tailored_cvs", timeout=30)
                        if cv_response.status_code == 200:
                            cv_data = cv_response.json()
                            if cv_data.get("tailored_cvs"):
                                for cv in cv_data["tailored_cvs"]:
                                    st.write(f"📄 {cv}")
                            else:
                                st.info("No tailored CVs found for this session.")
                        else:
                            st.warning("Could not fetch tailored CV list.")
                    except Exception as e:
                        st.warning(f"Could not fetch tailored CV list: {e}")
                else:
                    st.success("✅ Upload successful!")
                    st.json(result)

# ========= FOOTER =========
st.markdown("---")
st.markdown("*AI HR Agent - Automated Resume Processing and Job Matching*")
