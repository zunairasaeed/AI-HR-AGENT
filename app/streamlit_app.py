
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
st.set_page_config(page_title="HR Agent Dashboard", layout="centered")
st.title("🧠 HR Agent Dashboard")

# ========= SETTINGS (Sidebar) =========
st.sidebar.header("Settings")
FASTAPI_BASE_URL = st.sidebar.text_input("Backend URL", FASTAPI_BASE_URL, help="FastAPI base URL (e.g., http://127.0.0.1:8000 or your Railway URL)")
REQUEST_TIMEOUT = st.sidebar.slider("Request timeout (seconds)", min_value=60, max_value=1200, value=REQUEST_TIMEOUT, step=30)

# ========= UPLOAD SECTION =========
st.header("📤 Upload Resumes, JDs, and Optional Template")

resumes = st.file_uploader(
    "Upload up to 5 Resumes (PDF or DOCX)", type=["pdf", "docx"], key="resumes", accept_multiple_files=True
)
jds = st.file_uploader(
    "Upload up to 2 Job Descriptions (PDF or DOCX) - optional",
    type=["pdf", "docx"], key="jds", accept_multiple_files=True
)

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

    # Attempt new API
    res = requests.post(
        f"{FASTAPI_BASE_URL}/upload",
        params={"use_default_template": str(use_default_template).lower()},
        files=plural_multipart,
        timeout=REQUEST_TIMEOUT,
    )
    if res.status_code != 422:
        return res

    # If backend expects singular fields (old API), retry with first resume/JD
    # Only if error indicates missing 'resume' or 'jd'
    try:
        err = res.json()
        missing_fields = "resume" in str(err) or "jd" in str(err)
    except Exception:
        missing_fields = False
    if not missing_fields:
        return res

    if not resumes or not jds:
        return res  # cannot fallback if one is missing

    singular_multipart = [
        ("resume", (resumes[0].name, resumes[0].getvalue(), resumes[0].type or "application/octet-stream")),
        ("jd", (jds[0].name, jds[0].getvalue(), jds[0].type or "application/octet-stream")),
    ]
    if (not use_default_template) and template_file is not None:
        singular_multipart.append((
            "template_file",
            (
                template_file.name,
                template_file.getvalue(),
                template_file.type or "application/octet-stream",
            ),
        ))

    return requests.post(
        f"{FASTAPI_BASE_URL}/upload",
        params={"use_default_template": str(use_default_template).lower()},
        files=singular_multipart,
        timeout=REQUEST_TIMEOUT,
    )

# ========= PROGRESS SECTION =========
st.header("🔄 Pipeline Progress")
show_progress(st.session_state.stage)

# ========= RUN PIPELINE =========
if st.button("🚀 Run Matching Pipeline"):
    if not resumes:
        st.warning("⚠️ Please upload at least one resume.")
    else:
        try:
            # Step 1: Upload files to FastAPI
            st.session_state.stage = 0
            show_progress(st.session_state.stage)
            with st.spinner("📤 Uploading files..."):
                # IMPORTANT: send bytes using getvalue() and multiple parts per field name
                upload_res = try_upload_to_backend(resumes, jds, template_file, use_default_template)

            if upload_res.status_code != 200:
                # Try to show JSON error if backend sent one
                try:
                    err = upload_res.json().get("error", upload_res.text)
                except Exception:
                    err = upload_res.text
                st.error(f"❌ Upload failed: {err}")
            else:
                # Step 2: Simulate running AI pipeline (replace with actual polling if you have it)
                st.session_state.stage = 1
                show_progress(st.session_state.stage)
                time.sleep(2)  # simulate delay

                # Step 3: Fetch results (if your backend exposes any status/results endpoint, call it here)
                st.session_state.stage = 2
                show_progress(st.session_state.stage)

                # Step 4: Complete
                st.session_state.stage = 3
                show_progress(st.session_state.stage)

                st.success("✅ Pipeline executed successfully!")

                # Show backend message/summary
                try:
                    payload = upload_res.json()
                    if payload:
                        st.json(payload)
                except Exception:
                    pass

                # ========= DOWNLOAD SECTION =========
                st.header("📥 Download Outputs")

                # Download Rankings PDF
                pdf_bytes, pdf_filename = download_file_from_fastapi(
                    "/download/rankings-pdf", "rankings_combined.pdf"
                )
                if pdf_bytes:
                    st.download_button(
                        label="⬇️ Download Rankings PDF",
                        data=pdf_bytes,
                        file_name=pdf_filename,
                        mime="application/pdf",
                    )

                # Download Tailored CVs ZIP
                docx_bytes, docx_filename = download_file_from_fastapi(
                    "/download/tailored-cv-docx", "tailored_cvs.zip"
                )
                if docx_bytes:
                    st.download_button(
                        label="⬇️ Download Tailored CVs ZIP",
                        data=docx_bytes,
                        file_name=docx_filename,
                        mime="application/zip",
                    )

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")

# Optional: quick link to your FastAPI docs so you can verify endpoints manually
st.caption("Need to check the backend? Open your FastAPI docs:")
st.link_button("Open FastAPI Swagger", f"{FASTAPI_BASE_URL}/docs")
