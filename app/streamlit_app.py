
### the code running perfectly ti the pipeline

# import streamlit as st
# import requests
# import time

# st.set_page_config(page_title="HR Agent", layout="centered")
# st.title("🧠 HR Agent Dashboard")

# # 1. Upload Section
# st.header("📤 Upload Resume & JD")

# resume = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"], key="resume")
# jd = st.file_uploader("Upload Job Description (PDF or DOCX)", type=["pdf", "docx"], key="jd")

# if 'stage' not in st.session_state:
#     st.session_state.stage = 0

# def show_progress(stage):
#     steps = ["Uploading", "Running AI Pipeline", "Fetching Results", "Complete"]
#     for idx, step in enumerate(steps):
#         icon = "🔄" if stage == idx else "✅" if stage > idx else "⬜"
#         st.markdown(f"{icon} {step}")

# # 2. Pipeline Progress
# st.header("🔄 Pipeline Progress")
# show_progress(st.session_state.stage)

# # 3. Run Matching
# if st.button("🚀 Run Matching Pipeline"):
#     if not resume or not jd:
#         st.warning("Please upload both a resume and a JD.")
#     else:
#         try:
#             st.session_state.stage = 0
#             show_progress(st.session_state.stage)

#             with st.spinner("Uploading..."):
#                 files = {
#                     "resume": (resume.name, resume, resume.type),
#                     "jd": (jd.name, jd, jd.type)
#                 }
#                 upload_res = requests.post("http://localhost:8000/upload", files=files)

#             if upload_res.status_code != 200:
#                 st.error("❌ Upload failed.")
#             else:
#                 st.session_state.stage = 1
#                 show_progress(st.session_state.stage)
#                 time.sleep(2)

#                 st.session_state.stage = 2
#                 show_progress(st.session_state.stage)
#                 results_res = requests.get("http://localhost:8000/results")

#                 if results_res.status_code == 200:
#                     st.session_state.stage = 3
#                     show_progress(st.session_state.stage)
#                     results = results_res.json()

#                     # 4. Resume / JD Text Preview
#                     st.header("📄 Preview Uploaded Files (Text Extract)")
#                     if "text_resume" in upload_res.json():
#                         st.subheader("Resume Content")
#                         st.text(upload_res.json().get("text_resume"))
#                     if "text_jd" in upload_res.json():
#                         st.subheader("JD Content")
#                         st.text(upload_res.json().get("text_jd"))

#                     # 5. Matching Results Table
#                     st.header("📈 Matching Results")

#                     # Filters
#                     st.subheader("🔍 Filters")
#                     job_roles = list(set([job['job_title'] for job in results]))
#                     selected_roles = st.multiselect("Filter by Job Role", job_roles, default=job_roles)
#                     min_score = st.slider("Minimum Score (%)", 0, 100, 50)

#                     filtered = [job for job in results if job['job_title'] in selected_roles and job['score'] >= min_score]

#                     if filtered:
#                         st.table(filtered)
#                     else:
#                         st.warning("No matches based on filters.")

#                     # 6. Tailored CV Download
#                     st.header("📥 Download Tailored CV")
#                     st.markdown("[⬇️ Click here to download tailored CV](http://localhost:8000/download-cv)")
#                 else:
#                     st.error("❌ Failed to fetch results.")
#         except Exception as e:
#             st.error(f"Something went wrong: {e}")


##before i fuck up
# import streamlit as st
# import requests
# import time

# FASTAPI_BASE_URL = "http://localhost:8000"  # Change if different

# st.set_page_config(page_title="HR Agent", layout="centered")
# st.title("🧠 HR Agent Dashboard")

# # 1. Upload Section
# st.header("📤 Upload Resume & JD")

# resume = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"], key="resume")
# jd = st.file_uploader("Upload Job Description (PDF or DOCX)", type=["pdf", "docx"], key="jd")

# if 'stage' not in st.session_state:
#     st.session_state.stage = 0

# def show_progress(stage):
#     steps = ["Uploading", "Running AI Pipeline", "Fetching Results", "Complete"]
#     for idx, step in enumerate(steps):
#         icon = "🔄" if stage == idx else "✅" if stage > idx else "⬜"
#         st.markdown(f"{icon} {step}")

# def download_file_from_fastapi(endpoint, filename):
#     """Downloads a file from FastAPI and returns bytes + filename."""
#     response = requests.get(f"{FASTAPI_BASE_URL}{endpoint}")
#     if response.status_code == 200:
#         return response.content, filename
#     else:
#         st.error(f"❌ Failed to fetch file from {endpoint}")
#         return None, None

# # 2. Pipeline Progress
# st.header("🔄 Pipeline Progress")
# show_progress(st.session_state.stage)

# # 3. Run Matching
# if st.button("🚀 Run Matching Pipeline"):
#     if not resume or not jd:
#         st.warning("Please upload both a resume and a JD.")
#     else:
#         try:
#             st.session_state.stage = 0
#             show_progress(st.session_state.stage)

#             with st.spinner("Uploading..."):
#                 files = {
#                     "resume": (resume.name, resume, resume.type),
#                     "jd": (jd.name, jd, jd.type)
#                 }
#                 upload_res = requests.post(f"{FASTAPI_BASE_URL}/upload", files=files)

#             if upload_res.status_code != 200:
#                 st.error("❌ Upload failed.")
#             else:
#                 st.session_state.stage = 1
#                 show_progress(st.session_state.stage)
#                 time.sleep(2)

#                 st.session_state.stage = 2
#                 show_progress(st.session_state.stage)
#                 results_res = requests.get(f"{FASTAPI_BASE_URL}/results")

#                 if results_res.status_code == 200:
#                     st.session_state.stage = 3
#                     show_progress(st.session_state.stage)
#                     results = results_res.json()

#                     # 4. Resume / JD Text Preview
#                     st.header("📄 Preview Uploaded Files (Text Extract)")
#                     if "text_resume" in upload_res.json():
#                         st.subheader("Resume Content")
#                         st.text(upload_res.json().get("text_resume"))
#                     if "text_jd" in upload_res.json():
#                         st.subheader("JD Content")
#                         st.text(upload_res.json().get("text_jd"))

#                     # 5. Matching Results Table
#                     st.header("📈 Matching Results")

#                     # Filters
#                     st.subheader("🔍 Filters")
#                     job_roles = list(set([job['job_title'] for job in results]))
#                     selected_roles = st.multiselect("Filter by Job Role", job_roles, default=job_roles)
#                     min_score = st.slider("Minimum Score (%)", 0, 100, 50)

#                     filtered = [job for job in results if job['job_title'] in selected_roles and job['score'] >= min_score]

#                     if filtered:
#                         st.table(filtered)
#                     else:
#                         st.warning("No matches based on filters.")

#                     # 6. Results Download Section
#                     st.header("📥 Download Results")

#                     # Download Rankings PDF
#                     pdf_bytes, pdf_filename = download_file_from_fastapi("/download/rankings-pdf", "job_rankings.pdf")
#                     if pdf_bytes:
#                         st.download_button(
#                             label="⬇️ Download Rankings PDF",
#                             data=pdf_bytes,
#                             file_name=pdf_filename,
#                             mime="application/pdf"
#                         )

#                     # Download Tailored CV DOCX
#                     docx_bytes, docx_filename = download_file_from_fastapi("/download/tailored-cv-docx", "tailored_cv.docx")
#                     if docx_bytes:
#                         st.download_button(
#                             label="⬇️ Download Tailored CV (DOCX)",
#                             data=docx_bytes,
#                             file_name=docx_filename,
#                             mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#                         )

#                 else:
#                     st.error("❌ Failed to fetch results.")
#         except Exception as e:
#             st.error(f"Something went wrong: {e}")



# import streamlit as st
# import requests
# import time

# # ====== CONFIG ======
# FASTAPI_BASE_URL = "http://localhost:8000"  # Change if your FastAPI runs on another port

# # ====== PAGE SETTINGS ======
# st.set_page_config(page_title="HR Agent Dashboard", layout="centered")
# st.title("🧠 HR Agent Dashboard")

# # ====== UPLOAD SECTION ======
# st.header("📤 Upload Resume & JD")

# resume = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"], key="resume")
# jd = st.file_uploader("Upload Job Description (PDF or DOCX)", type=["pdf", "docx"], key="jd")

# if "stage" not in st.session_state:
#     st.session_state.stage = 0


# # ====== FUNCTIONS ======
# def show_progress(stage):
#     """Display step-by-step pipeline progress."""
#     steps = ["Uploading", "Running AI Pipeline", "Fetching Results", "Complete"]
#     for idx, step in enumerate(steps):
#         icon = "🔄" if stage == idx else "✅" if stage > idx else "⬜"
#         st.markdown(f"{icon} {step}")


# def download_file_from_fastapi(endpoint, filename):
#     """Fetch file bytes from FastAPI endpoint."""
#     try:
#         response = requests.get(f"{FASTAPI_BASE_URL}{endpoint}")
#         if response.status_code == 200:
#             return response.content, filename
#         else:
#             st.error(f"❌ Failed to fetch file from {endpoint}: {response.json().get('error', 'Unknown error')}")
#             return None, None
#     except requests.exceptions.RequestException as e:
#         st.error(f"❌ Error fetching from {endpoint}: {e}")
#         return None, None


# # ====== PROGRESS SECTION ======
# st.header("🔄 Pipeline Progress")
# show_progress(st.session_state.stage)


# # ====== RUN MATCHING PIPELINE ======
# if st.button("🚀 Run Matching Pipeline"):
#     if not resume or not jd:
#         st.warning("⚠️ Please upload both a resume and a JD before running the pipeline.")
#     else:
#         try:
#             # Step 1: Upload
#             st.session_state.stage = 0
#             show_progress(st.session_state.stage)
#             with st.spinner("📤 Uploading files..."):
#                 files = {
#                     "resume": (resume.name, resume, resume.type),
#                     "jd": (jd.name, jd, jd.type),
#                 }
#                 upload_res = requests.post(f"{FASTAPI_BASE_URL}/upload", files=files)

#             if upload_res.status_code != 200:
#                 st.error("❌ Upload failed. Please check your backend.")
#             else:
#                 # Step 2: Running AI pipeline
#                 st.session_state.stage = 1
#                 show_progress(st.session_state.stage)
#                 time.sleep(2)  # Simulate processing time

#                 # Step 3: Fetch results
#                 st.session_state.stage = 2
#                 show_progress(st.session_state.stage)

#                 # NOTE: You might want to implement an actual /results endpoint in FastAPI that returns matching results JSON
#                 results_res = requests.get(f"{FASTAPI_BASE_URL}/results")  # Assuming you have this endpoint
#                 if results_res.status_code == 200:
#                     st.session_state.stage = 3
#                     show_progress(st.session_state.stage)
#                     results = results_res.json()

#                     # ====== PREVIEW FILE CONTENT ======
#                     st.header("📄 Preview Uploaded Files (Text Extract)")
#                     if "text_resume" in upload_res.json():
#                         st.subheader("Resume Content")
#                         st.text(upload_res.json().get("text_resume", ""))
#                     if "text_jd" in upload_res.json():
#                         st.subheader("Job Description Content")
#                         st.text(upload_res.json().get("text_jd", ""))

#                     # ====== MATCHING RESULTS ======
#                     st.header("📈 Matching Results")
#                     st.subheader("🔍 Filters")
#                     job_roles = list(set([job.get("job_title", "") for job in results]))
#                     selected_roles = st.multiselect("Filter by Job Role", job_roles, default=job_roles)
#                     min_score = st.slider("Minimum Score (%)", 0, 100, 50)

#                     filtered = [
#                         job for job in results
#                         if job.get("job_title") in selected_roles and job.get("score", 0) >= min_score
#                     ]

#                     if filtered:
#                         st.table(filtered)
#                     else:
#                         st.warning("No matches found for selected filters.")

#                     # ====== DOWNLOAD RESULTS ======
#                     st.header("📥 Download Results")

#                     # Rankings PDF
#                     pdf_bytes, pdf_filename = download_file_from_fastapi(
#                         "/download/rankings-pdf", "rankings_combined.pdf"
#                     )
#                     if pdf_bytes:
#                         st.download_button(
#                             label="⬇️ Download Rankings PDF",
#                             data=pdf_bytes,
#                             file_name=pdf_filename,
#                             mime="application/pdf",
#                         )

#                     # Tailored CVs ZIP
#                     docx_bytes, docx_filename = download_file_from_fastapi(
#                         "/download/tailored-cv-docx", "tailored_cvs.zip"
#                     )
#                     if docx_bytes:
#                         st.download_button(
#                             label="⬇️ Download Tailored CVs ZIP",
#                             data=docx_bytes,
#                             file_name=docx_filename,
#                             mime="application/zip",
#                         )
#                 else:
#                     st.error(f"❌ Failed to fetch results from FastAPI: {results_res.text}")
#         except Exception as e:
#             st.error(f"❌ Something went wrong: {e}")

                                        



                                    #WORKINGGGGGGGGG
# import streamlit as st
# import requests
# import time
# BACKEND_URL = "https://web-production-ffce.up.railway.app"

# # ====== CONFIG ======
# FASTAPI_BASE_URL = "http://localhost:8000"  # Change if your FastAPI runs elsewhere

# # ====== PAGE SETTINGS ======
# st.set_page_config(page_title="HR Agent Dashboard", layout="centered")
# st.title("🧠 HR Agent Dashboard")

# # ====== UPLOAD SECTION ======
# st.header("📤 Upload Resume & Job Description")

# resume = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"], key="resume")
# jd = st.file_uploader("Upload Job Description (PDF or DOCX)", type=["pdf", "docx"], key="jd")

# if "stage" not in st.session_state:
#     st.session_state.stage = 0


# # ====== UTILS ======
# def show_progress(stage):
#     steps = ["Uploading", "Running AI Pipeline", "Fetching Results", "Complete"]
#     for idx, step in enumerate(steps):
#         icon = "🔄" if stage == idx else "✅" if stage > idx else "⬜"
#         st.markdown(f"{icon} {step}")


# def download_file_from_fastapi(endpoint, filename):
#     try:
#         response = requests.get(f"{FASTAPI_BASE_URL}{endpoint}")
#         if response.status_code == 200:
#             return response.content, filename
#         else:
#             st.error(f"❌ Failed to fetch file from {endpoint}: {response.json().get('error', 'Unknown error')}")
#             return None, None
#     except requests.exceptions.RequestException as e:
#         st.error(f"❌ Error fetching from {endpoint}: {e}")
#         return None, None


# # ====== PROGRESS SECTION ======
# st.header("🔄 Pipeline Progress")
# show_progress(st.session_state.stage)


# # ====== RUN PIPELINE ======
# if st.button("🚀 Run Matching Pipeline"):
#     if not resume or not jd:
#         st.warning("⚠️ Please upload both a resume and a job description before running the pipeline.")
#     else:
#         try:
#             # Step 1: Upload files to FastAPI
#             st.session_state.stage = 0
#             show_progress(st.session_state.stage)
#             with st.spinner("📤 Uploading files..."):
#                 files = {
#                     "resume": (resume.name, resume, resume.type),
#                     "jd": (jd.name, jd, jd.type),
#                 }
#                 upload_res = requests.post(f"{FASTAPI_BASE_URL}/upload", files=files)

#             if upload_res.status_code != 200:
#                 st.error(f"❌ Upload failed: {upload_res.json().get('error', 'Unknown error')}")
#             else:
#                 # Step 2: Simulate running AI pipeline
#                 st.session_state.stage = 1
#                 show_progress(st.session_state.stage)
#                 time.sleep(2)  # simulate delay, replace with actual polling if available

#                 # Step 3: Fetch results (if you have /results endpoint)
#                 st.session_state.stage = 2
#                 show_progress(st.session_state.stage)

#                 # OPTIONAL: Implement results fetching logic here if you have an endpoint

#                 # Step 4: Complete
#                 st.session_state.stage = 3
#                 show_progress(st.session_state.stage)

#                 st.success("✅ Pipeline executed successfully!")

#                 # ====== DOWNLOAD SECTION ======
#                 st.header("📥 Download Outputs")

#                 # Download Rankings PDF
#                 pdf_bytes, pdf_filename = download_file_from_fastapi(
#                     "/download/rankings-pdf", "rankings_combined.pdf"
#                 )
#                 if pdf_bytes:
#                     st.download_button(
#                         label="⬇️ Download Rankings PDF",
#                         data=pdf_bytes,
#                         file_name=pdf_filename,
#                         mime="application/pdf",
#                     )

#                 # Download Tailored CVs ZIP
#                 docx_bytes, docx_filename = download_file_from_fastapi(
#                     "/download/tailored-cv-docx", "tailored_cvs.zip"
#                 )
#                 if docx_bytes:
#                     st.download_button(
#                         label="⬇️ Download Tailored CVs ZIP",
#                         data=docx_bytes,
#                         file_name=docx_filename,
#                         mime="application/zip",
#                     )

#         except Exception as e:
#             st.error(f"❌ Something went wrong: {e}")

import streamlit as st
import requests
import time

# ========= CONFIG =========
# Use your deployed FastAPI on Railway:
FASTAPI_BASE_URL = "https://web-production-ffce.up.railway.app"  # <-- EDITED

REQUEST_TIMEOUT = 60  # seconds (adjust if your pipeline takes longer)

# ========= PAGE SETTINGS =========
st.set_page_config(page_title="HR Agent Dashboard", layout="centered")
st.title("🧠 HR Agent Dashboard")

# ========= UPLOAD SECTION =========
st.header("📤 Upload Resume & Job Description")

resume = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"], key="resume")
jd = st.file_uploader("Upload Job Description (PDF or DOCX)", type=["pdf", "docx"], key="jd")

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

# ========= PROGRESS SECTION =========
st.header("🔄 Pipeline Progress")
show_progress(st.session_state.stage)

# ========= RUN PIPELINE =========
if st.button("🚀 Run Matching Pipeline"):
    if not resume or not jd:
        st.warning("⚠️ Please upload both a resume and a job description before running the pipeline.")
    else:
        try:
            # Step 1: Upload files to FastAPI
            st.session_state.stage = 0
            show_progress(st.session_state.stage)
            with st.spinner("📤 Uploading files..."):
                # IMPORTANT: send bytes using getvalue()
                files = {
                    "resume": (resume.name, resume.getvalue(), resume.type or "application/octet-stream"),
                    "jd": (jd.name, jd.getvalue(), jd.type or "application/octet-stream"),
                }
                upload_res = requests.post(
                    f"{FASTAPI_BASE_URL}/upload",
                    files=files,
                    timeout=REQUEST_TIMEOUT,
                )

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

                # ========= DOWNLOAD SECTION =========
                st.header("📥 Download Outputs")

                # Download Rankings PDF (your backend must implement this endpoint)
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

                # Download Tailored CVs ZIP (your backend must implement this endpoint)
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
