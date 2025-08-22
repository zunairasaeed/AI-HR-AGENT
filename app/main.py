
                           
                           #                  pipeline works now



# from pathlib import Path
# from dotenv import load_dotenv
# import os
# import shutil
# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import JSONResponse



# # ===== Load ENV =====
# PROJECT_ROOT = Path(__file__).resolve().parent.parent
# load_dotenv(dotenv_path=PROJECT_ROOT / ".env")
# print("✅ ENV LOADED:", os.getenv("AZURE_OPENAI_API_KEY")[:8])

# # ===== Setup App =====
# app = FastAPI()

# # === Setup Upload Directories ===
# RESUME_DIR = PROJECT_ROOT / "data" / "resumes"
# JD_DIR = PROJECT_ROOT / "data" / "jds"
# RESUME_DIR.mkdir(parents=True, exist_ok=True)
# JD_DIR.mkdir(parents=True, exist_ok=True)


# @app.post("/upload")
# async def upload_and_process(
#     resume: UploadFile = File(...),
#     jd: UploadFile = File(...)
# ):
#     try:
#         # ===== Check File Extensions =====
#         for file in [resume, jd]:
#             ext = file.filename.split(".")[-1].lower()
#             if ext not in ["pdf", "docx"]:
#                 return JSONResponse(
#                     status_code=400,
#                     content={"error": f"❌ {file.filename}: Only PDF or DOCX allowed."}
#                 )

#         # ===== Save Resume =====
#         resume_path = RESUME_DIR / resume.filename
#         with open(resume_path, "wb") as buffer:
#             shutil.copyfileobj(resume.file, buffer)

#         # ===== Save JD =====
#         jd_path = JD_DIR / jd.filename
#         with open(jd_path, "wb") as buffer:
#             shutil.copyfileobj(jd.file, buffer)

#         # ===== Run Pipeline =====
#         from app.raw_parser import run_raw_parsing_debug
#         from llm.parser import run_llm_parsing
#         from llm.jd_parser import run_job_parsing
#         from llm.matcher import run_matching
#         from llm.jobs_ranking import run_job_ranking_by_candidate
#         from llm.rank_candidates_by_job import run_candidate_ranking_by_job
#         from llm.parsered_template import run_template_extractor
#         from llm.tailoredcv import tailor_all

#         print(f"\n📄 STEP 1: Raw parsing for {resume.filename}")
#         run_raw_parsing_debug()

#         print(f"🧠 STEP 2: LLM resume parsing for {resume.filename}")
#         run_llm_parsing()

#         print(f"📃 STEP 3: Job description parsing for {jd.filename}")
#         run_job_parsing()

#         print(f"🔍 STEP 4: Matching for {resume.filename}")
#         run_matching()

#         print(f"📊 STEP 5: Ranking jobs for candidate {resume.filename}")
#         run_job_ranking_by_candidate()

#         print("📊 STEP 6: Ranking candidates by job")
#         run_candidate_ranking_by_job()

#         print(f"📝 STEP 7: Generating template context for {resume.filename}")
#         run_template_extractor()

#         print(f"🎯 STEP 8: Tailoring final CV for {resume.filename}")
#         tailor_all()

#         base_name = resume.filename.rsplit(".", 1)[0]
#         tailored_output = f"data/json/llm_tailored_cv/{base_name}__<job>__tailored.docx"

#         return JSONResponse(
#             status_code=200,
#             content={
#                 "message": "✅ Full pipeline executed successfully.",
#                 "tailored_cv_path": tailored_output,
#                 "resume_saved": str(resume_path),
#                 "jd_saved": str(jd_path)
#             }
#         )

#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"error": f"❌ Pipeline error: {str(e)}"}
#         )
                            #####  results [doest ave zip folder nd poin for taikoredcvs]


# from pathlib import Path
# from dotenv import load_dotenv
# import os
# import shutil
# import json
# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import JSONResponse, FileResponse
# from fpdf import FPDF  # For converting JSON rankings into PDF

# # ===== Load ENV =====
# PROJECT_ROOT = Path(__file__).resolve().parent.parent
# load_dotenv(dotenv_path=PROJECT_ROOT / ".env")
# print("✅ ENV LOADED:", os.getenv("AZURE_OPENAI_API_KEY")[:8])

# # ===== Setup App =====
# app = FastAPI()

# # === Setup Upload Directories ===
# RESUME_DIR = PROJECT_ROOT / "data" / "resumes"
# JD_DIR = PROJECT_ROOT / "data" / "jds"
# RESUME_DIR.mkdir(parents=True, exist_ok=True)
# JD_DIR.mkdir(parents=True, exist_ok=True)

# TAILORED_CV_DIR = PROJECT_ROOT / "data" / "json" / "tailored_cv_docx"
# JOB_RANKINGS_DIR = PROJECT_ROOT / "data" / "json" / "rank_candidates_by_job"
# TAILORED_CV_DIR.mkdir(parents=True, exist_ok=True)
# JOB_RANKINGS_DIR.mkdir(parents=True, exist_ok=True)


# @app.post("/upload")
# async def upload_and_process(
#     resume: UploadFile = File(...),
#     jd: UploadFile = File(...)
# ):
#     try:
#         # ===== Check File Extensions =====
#         for file in [resume, jd]:
#             ext = file.filename.split(".")[-1].lower()
#             if ext not in ["pdf", "docx"]:
#                 return JSONResponse(
#                     status_code=400,
#                     content={"error": f"❌ {file.filename}: Only PDF or DOCX allowed."}
#                 )

#         # ===== Save Resume =====
#         resume_path = RESUME_DIR / resume.filename
#         with open(resume_path, "wb") as buffer:
#             shutil.copyfileobj(resume.file, buffer)

#         # ===== Save JD =====
#         jd_path = JD_DIR / jd.filename
#         with open(jd_path, "wb") as buffer:
#             shutil.copyfileobj(jd.file, buffer)

#         # ===== Run Pipeline =====
#         from app.raw_parser import run_raw_parsing_debug
#         from llm.parser import run_llm_parsing
#         from llm.jd_parser import run_job_parsing
#         from llm.matcher import run_matching
#         from llm.jobs_ranking import run_job_ranking_by_candidate
#         from llm.rank_candidates_by_job import run_candidate_ranking_by_job
#         from llm.parsered_template import run_template_extractor
#         from llm.tailoredcv import tailor_all

#         print(f"\n📄 STEP 1: Raw parsing for {resume.filename}")
#         run_raw_parsing_debug()

#         print(f"🧠 STEP 2: LLM resume parsing for {resume.filename}")
#         run_llm_parsing()

#         print(f"📃 STEP 3: Job description parsing for {jd.filename}")
#         run_job_parsing()

#         print(f"🔍 STEP 4: Matching for {resume.filename}")
#         run_matching()

#         print(f"📊 STEP 5: Ranking jobs for candidate {resume.filename}")
#         run_job_ranking_by_candidate()

#         print("📊 STEP 6: Ranking candidates by job")
#         run_candidate_ranking_by_job()

#         print(f"📝 STEP 7: Generating template context for {resume.filename}")
#         run_template_extractor()

#         print(f"🎯 STEP 8: Tailoring final CV for {resume.filename}")
#         tailor_all()

#         base_name = resume.filename.rsplit(".", 1)[0]
#         tailored_output = f"data/json/tailored_cv_docx/{base_name}__<job>__tailored.docx"

#         return JSONResponse(
#             status_code=200,
#             content={
#                 "message": "✅ Full pipeline executed successfully.",
#                 "tailored_cv_path": tailored_output,
#                 "resume_saved": str(resume_path),
#                 "jd_saved": str(jd_path)
#             }
#         )

#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"error": f"❌ Pipeline error: {str(e)}"}
#         )


# # ===== New Route: List Tailored CVs =====
# @app.get("/tailored_cvs")
# def list_tailored_cvs():
#     files = sorted(TAILORED_CV_DIR.glob("*.docx"))
#     return {"tailored_cvs": [str(file) for file in files]}


# # ===== New Route: Download Tailored CV =====
# @app.get("/download_tailored_cv/{filename}")
# def download_tailored_cv(filename: str):
#     file_path = TAILORED_CV_DIR / filename
#     if not file_path.exists():
#         return JSONResponse({"error": "File not found"}, status_code=404)
#     return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename=filename)


# # ===== New Route: Convert Rankings JSON → PDF and Download =====
# @app.get("/download_rankings_pdf")
# def download_rankings_pdf():
#     files = sorted(JOB_RANKINGS_DIR.glob("*.json"))
#     if not files:
#         return JSONResponse({"error": "No rankings found"}, status_code=404)

#     pdf = FPDF()
#     pdf.set_font("Arial", size=12)

#     for file in files:
#         pdf.add_page()
#         pdf.cell(200, 10, f"Rankings: {file.name}", ln=True)
#         try:
#             with open(file, "r", encoding="utf-8") as f:
#                 data = json.load(f)
#                 pdf.multi_cell(0, 10, json.dumps(data, indent=2))
#         except Exception as e:
#             pdf.multi_cell(0, 10, f"Error reading {file.name}: {e}")

#     output_path = PROJECT_ROOT / "data" / "json" / "rankings_combined.pdf"
#     pdf.output(str(output_path))
#     return FileResponse(output_path, media_type="application/pdf", filename="rankings_combined.pdf")


############       now have xip folder tailored cv #####


# from pathlib import Path
# from dotenv import load_dotenv
# import os
# import shutil
# import json
# import zipfile
# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import JSONResponse, FileResponse
# from fpdf import FPDF

# # ===== Load ENV =====
# PROJECT_ROOT = Path(__file__).resolve().parent.parent
# load_dotenv(dotenv_path=PROJECT_ROOT / ".env")
# print("✅ ENV LOADED:", os.getenv("AZURE_OPENAI_API_KEY")[:8])

# # ===== Setup App =====
# app = FastAPI()

# # === Setup Upload Directories ===
# RESUME_DIR = PROJECT_ROOT / "data" / "resumes"
# JD_DIR = PROJECT_ROOT / "data" / "jds"
# RESUME_DIR.mkdir(parents=True, exist_ok=True)
# JD_DIR.mkdir(parents=True, exist_ok=True)

# TAILORED_CV_DIR = PROJECT_ROOT / "data" / "json" / "tailored_cv_docx"
# JOB_RANKINGS_DIR = PROJECT_ROOT / "data" / "json" / "rank_candidates_by_job"
# TAILORED_CV_DIR.mkdir(parents=True, exist_ok=True)
# JOB_RANKINGS_DIR.mkdir(parents=True, exist_ok=True)

# @app.post("/upload")
# async def upload_and_process(
#     resume: UploadFile = File(...),
#     jd: UploadFile = File(...)
# ):
#     try:
#         # ===== Check File Extensions =====
#         for file in [resume, jd]:
#             ext = file.filename.split(".")[-1].lower()
#             if ext not in ["pdf", "docx"]:
#                 return JSONResponse(
#                     status_code=400,
#                     content={"error": f"❌ {file.filename}: Only PDF or DOCX allowed."}
#                 )

#         # ===== Save Resume =====
#         resume_path = RESUME_DIR / resume.filename
#         with open(resume_path, "wb") as buffer:
#             shutil.copyfileobj(resume.file, buffer)

#         # ===== Save JD =====
#         jd_path = JD_DIR / jd.filename
#         with open(jd_path, "wb") as buffer:
#             shutil.copyfileobj(jd.file, buffer)

#         # ===== Run Pipeline =====
#         # Import your pipeline functions here; adjust as per your project structure
#         from app.raw_parser import run_raw_parsing_debug
#         from llm.parser import run_llm_parsing
#         from llm.jd_parser import run_job_parsing
#         from llm.matcher import run_matching
#         from llm.jobs_ranking import run_job_ranking_by_candidate
#         from llm.rank_candidates_by_job import run_candidate_ranking_by_job
#         from llm.parsered_template import run_template_extractor
#         from llm.tailoredcv import tailor_all

#         print(f"\n📄 STEP 1: Raw parsing for {resume.filename}")
#         run_raw_parsing_debug()

#         print(f"🧠 STEP 2: LLM resume parsing for {resume.filename}")
#         run_llm_parsing()

#         print(f"📃 STEP 3: Job description parsing for {jd.filename}")
#         run_job_parsing()

#         print(f"🔍 STEP 4: Matching for {resume.filename}")
#         run_matching()

#         print(f"📊 STEP 5: Ranking jobs for candidate {resume.filename}")
#         run_job_ranking_by_candidate()

#         print("📊 STEP 6: Ranking candidates by job")
#         run_candidate_ranking_by_job()

#         print(f"📝 STEP 7: Generating template context for {resume.filename}")
#         run_template_extractor()

#         print(f"🎯 STEP 8: Tailoring final CV for {resume.filename}")
#         tailor_all()

#         return JSONResponse(
#             status_code=200,
#             content={
#                 "message": "✅ Full pipeline executed successfully.",
#                 "resume_saved": str(resume_path),
#                 "jd_saved": str(jd_path)
#             }
#         )

#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"error": f"❌ Pipeline error: {str(e)}"}
#         )


# # ===== List Tailored CVs =====
# @app.get("/tailored_cvs")
# def list_tailored_cvs():
#     files = sorted(TAILORED_CV_DIR.glob("*.docx"))
#     return {"tailored_cvs": [file.name for file in files]}  # Return only file names


# # ===== Download all Tailored CVs as ZIP =====
# @app.get("/download/tailored-cv-docx")
# def download_all_tailored_cvs():
#     files = sorted(TAILORED_CV_DIR.glob("*.docx"))
#     if not files:
#         return JSONResponse({"error": "No tailored CVs found"}, status_code=404)

#     zip_path = PROJECT_ROOT / "data" / "json" / "tailored_cvs.zip"
#     with zipfile.ZipFile(zip_path, 'w') as zipf:
#         for file in files:
#             zipf.write(file, arcname=file.name)

#     return FileResponse(zip_path, media_type="application/zip", filename="tailored_cvs.zip")


# # ===== Convert Rankings JSON → PDF and serve =====
# @app.get("/download/rankings-pdf")
# def download_rankings_pdf():
#     files = sorted(JOB_RANKINGS_DIR.glob("*.json"))
#     if not files:
#         return JSONResponse({"error": "No rankings found"}, status_code=404)

#     pdf = FPDF()
#     pdf.set_font("Arial", size=12)

#     for file in files:
#         pdf.add_page()
#         pdf.cell(200, 10, f"Rankings: {file.name}", ln=True)
#         try:
#             with open(file, "r", encoding="utf-8") as f:
#                 data = json.load(f)
#                 pdf.multi_cell(0, 10, json.dumps(data, indent=2))
#         except Exception as e:
#             pdf.multi_cell(0, 10, f"Error reading {file.name}: {e}")

#     output_path = PROJECT_ROOT / "data" / "json" / "rankings_combined.pdf"
#     pdf.output(str(output_path))
#     return FileResponse(output_path, media_type="application/pdf", filename="rankings_combined.pdf")



###### remove hte ranking jsn to pdf onw hting and tehe mutlie inout 
# from pathlib import Path
# from dotenv import load_dotenv
# import os
# import shutil
# import zipfile
# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import JSONResponse, FileResponse

# # ===== Load ENV =====
# PROJECT_ROOT = Path(__file__).resolve().parent.parent
# load_dotenv(dotenv_path=PROJECT_ROOT / ".env")
# print("✅ ENV LOADED:", os.getenv("AZURE_OPENAI_API_KEY")[:8])

# # ===== Setup App =====
# app = FastAPI()

# # === Setup Upload Directories ===
# RESUME_DIR = PROJECT_ROOT / "data" / "resumes"
# JD_DIR = PROJECT_ROOT / "data" / "jds"
# RESUME_DIR.mkdir(parents=True, exist_ok=True)
# JD_DIR.mkdir(parents=True, exist_ok=True)

# TAILORED_CV_DIR = PROJECT_ROOT / "data" / "json" / "tailored_cv_docx"
# JOB_RANKINGS_DIR = PROJECT_ROOT / "data" / "json" / "rank_candidates_by_job"
# TAILORED_CV_DIR.mkdir(parents=True, exist_ok=True)
# JOB_RANKINGS_DIR.mkdir(parents=True, exist_ok=True)

# # ===== Upload & Run Pipeline =====
# @app.post("/upload")
# async def upload_and_process(
#     resumes: list[UploadFile] = File(..., description="Upload up to 5 resumes"),
#     jds: list[UploadFile] = File(None, description="Upload up to 2 JDs (optional)")
# ):
#     try:
#         # ==== Validate Counts ====
#         if len(resumes) > 5:
#             return JSONResponse(status_code=400, content={"error": "❌ Max 5 resumes allowed."})
#         if jds and len(jds) > 2:
#             return JSONResponse(status_code=400, content={"error": "❌ Max 2 JDs allowed."})

#         saved_resumes, saved_jds = [], []

#         # ==== Save Resumes ====
#         for resume in resumes:
#             ext = resume.filename.split(".")[-1].lower()
#             if ext not in ["pdf", "docx"]:
#                 return JSONResponse(status_code=400, content={"error": f"❌ {resume.filename}: Only PDF or DOCX allowed."})
#             path = RESUME_DIR / resume.filename
#             with open(path, "wb") as buffer:
#                 shutil.copyfileobj(resume.file, buffer)
#             saved_resumes.append(str(path))

#         # ==== Save JDs (optional) ====
#         if jds:
#             for jd in jds:
#                 ext = jd.filename.split(".")[-1].lower()
#                 if ext not in ["pdf", "docx"]:
#                     return JSONResponse(status_code=400, content={"error": f"❌ {jd.filename}: Only PDF or DOCX allowed."})
#                 path = JD_DIR / jd.filename
#                 with open(path, "wb") as buffer:
#                     shutil.copyfileobj(jd.file, buffer)
#                 saved_jds.append(str(path))

#         # ==== Run Pipeline ====
#         from app.raw_parser import run_raw_parsing_debug
#         from llm.parser import run_llm_parsing
#         from llm.jd_parser import run_job_parsing
#         from llm.matcher import run_matching
#         from llm.jobs_ranking import run_job_ranking_by_candidate
#         from llm.rank_candidates_by_job import run_candidate_ranking_by_job
#         from llm.parsered_template import run_template_extractor
#         from llm.tailoredcv import tailor_all

#         for resume in saved_resumes:
#             print(f"\n📄 STEP 1: Raw parsing for {resume}")
#             run_raw_parsing_debug()

#             print(f"🧠 STEP 2: LLM resume parsing for {resume}")
#             run_llm_parsing()

#             if saved_jds:
#                 print("📃 STEP 3: Job description parsing")
#                 run_job_parsing()

#             print(f"🔍 STEP 4: Matching for {resume}")
#             run_matching()

#             print(f"📊 STEP 5: Ranking jobs for candidate {resume}")
#             run_job_ranking_by_candidate()

#             print(f"📝 STEP 6: Generating template context for {resume}")
#             run_template_extractor()

#             print(f"🎯 STEP 7: Tailoring final CV for {resume}")
#             tailor_all()

#         # === Final Step: Ranking candidates by job (PDF already generated in module) ===
#         print("📊 STEP 8: Ranking candidates by job (PDF)")
#         run_candidate_ranking_by_job()

#         return JSONResponse(
#             status_code=200,
#             content={
#                 "message": "✅ Full pipeline executed successfully.",
#                 "resumes_saved": saved_resumes,
#                 "jds_saved": saved_jds or "No JDs uploaded"
#             }
#         )

#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": f"❌ Pipeline error: {str(e)}"})


# # ===== List Tailored CVs =====
# @app.get("/tailored_cvs")
# def list_tailored_cvs():
#     files = sorted(TAILORED_CV_DIR.glob("*.docx"))
#     return {"tailored_cvs": [file.name for file in files]}  


# # ===== Download all Tailored CVs as ZIP =====
# @app.get("/download/tailored-cv-docx")
# def download_all_tailored_cvs():
#     files = sorted(TAILORED_CV_DIR.glob("*.docx"))
#     if not files:
#         return JSONResponse({"error": "No tailored CVs found"}, status_code=404)

#     zip_path = PROJECT_ROOT / "data" / "json" / "tailored_cvs.zip"
#     with zipfile.ZipFile(zip_path, 'w') as zipf:
#         for file in files:
#             zipf.write(file, arcname=file.name)

#     return FileResponse(zip_path, media_type="application/zip", filename="tailored_cvs.zip")


# # ===== Download Rankings PDF (generated by module) =====
# @app.get("/download/rankings-pdf")
# def download_rankings_pdf():
#     pdf_files = sorted(JOB_RANKINGS_DIR.glob("*.pdf"))
#     if not pdf_files:
#         return JSONResponse({"error": "No rankings PDF found"}, status_code=404)

#     # Take the latest generated PDF
#     latest_pdf = pdf_files[-1]
#     return FileResponse(latest_pdf, media_type="application/pdf", filename=latest_pdf.name)








from pathlib import Path
from dotenv import load_dotenv
import os
import shutil
import zipfile
import json
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

# ===== Load ENV =====
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")
try:
    _api_key = os.getenv("AZURE_OPENAI_API_KEY")
    print("✅ ENV LOADED:", (_api_key[:8] + "…") if _api_key else "(not set)")
except Exception:
    print("✅ ENV LOADED: (not set)")

# ===== Setup App =====
app = FastAPI(title="AI HR Agent API", version="1.0.0")

# ===== CORS Middleware =====
# Allow requests from Streamlit frontend and local development
origins = [
    "http://localhost:8501",  # Local Streamlit
    "http://127.0.0.1:8501",  # Local Streamlit alternative
    "https://*.streamlit.app",  # Streamlit Cloud
    "https://*.fly.dev",  # Fly.io deployments
    "*"  # Allow all origins for development (remove in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Setup Upload Directories (original project folders) ===
RESUME_DIR = PROJECT_ROOT / "data" / "resumes"
JD_DIR = PROJECT_ROOT / "data" / "jobs" / "raw_jd"  # ensure JDs go where parser expects
RESUME_DIR.mkdir(parents=True, exist_ok=True)
JD_DIR.mkdir(parents=True, exist_ok=True)

SESSION_LOCK_PATH = PROJECT_ROOT / "data" / "session_lock.json"
SESSION_LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)

TAILORED_CV_DIR = PROJECT_ROOT / "data" / "json" / "tailored_cv_docx"
JOB_RANKINGS_DIR = PROJECT_ROOT / "data" / "json" / "rank_candidates_by_job"
TAILORED_CV_DIR.mkdir(parents=True, exist_ok=True)
JOB_RANKINGS_DIR.mkdir(parents=True, exist_ok=True)

def clear_session_lock():
    """Clear the session lock to ensure clean start"""
    try:
        if SESSION_LOCK_PATH.exists():
            SESSION_LOCK_PATH.unlink()
        print("🧹 Session lock cleared")
    except Exception as e:
        print(f"⚠️ Could not clear session lock: {e}")

def create_session_lock(uploaded_resumes, uploaded_jds):
    """Create a new session lock with only current uploads"""
    try:
        lock = {
            "uploaded_resumes": uploaded_resumes,
            "uploaded_jds": uploaded_jds,
            "timestamp": str(Path().cwd())
        }
        with open(SESSION_LOCK_PATH, "w", encoding="utf-8") as f:
            json.dump(lock, f, indent=2, ensure_ascii=False)
        print(f"🔒 Session lock created with {len(uploaded_resumes)} resumes and {len(uploaded_jds)} JDs")
        return True
    except Exception as e:
        print(f"❌ Failed to create session lock: {e}")
        return False

# ===== Upload & Run Pipeline =====
@app.post("/upload")
async def upload_and_process(
    resumes: list[UploadFile] = File(..., description="Upload up to 5 resumes"),
    jds: list[UploadFile] = File(None, description="Upload up to 2 JDs (optional)"),
    use_default_template: bool = Query(True, description="Use default template if no custom template provided"),
    template_file: UploadFile | None = File(default=None, description="Optional resume template (DOCX/PDF)")
):
    try:
        # ==== Validate Counts ====
        if len(resumes) > 5:
            return JSONResponse(status_code=400, content={"error": "❌ Max 5 resumes allowed."})
        if jds and len(jds) > 2:
            return JSONResponse(status_code=400, content={"error": "❌ Max 2 JDs allowed."})

        # ==== Clear previous session lock ====
        clear_session_lock()

        saved_resumes, saved_jds = [], []

        # ==== Save Resumes ====
        for resume in resumes:
            ext = resume.filename.split(".")[-1].lower()
            if ext not in ["pdf", "docx"]:
                return JSONResponse(status_code=400, content={"error": f"❌ {resume.filename}: Only PDF or DOCX allowed."})
            path = RESUME_DIR / resume.filename
            with open(path, "wb") as buffer:
                shutil.copyfileobj(resume.file, buffer)
            saved_resumes.append(str(path))

        # ==== Save JDs (optional) ====
        if jds:
            for jd in jds:
                ext = jd.filename.split(".")[-1].lower()
                if ext not in ["pdf", "docx"]:
                    return JSONResponse(status_code=400, content={"error": f"❌ {jd.filename}: Only PDF or DOCX allowed."})
                path = JD_DIR / jd.filename
                with open(path, "wb") as buffer:
                    shutil.copyfileobj(jd.file, buffer)
                saved_jds.append(str(path))

        # ==== Optional: Accept template upload ====
        if template_file and not use_default_template:
            tmpl_ext = template_file.filename.split(".")[-1].lower()
            if tmpl_ext not in ["docx", "pdf"]:
                return JSONResponse(status_code=400, content={"error": f"❌ {template_file.filename}: Only DOCX or PDF allowed for template."})
            # Save into templates folder for extractor to pick up
            templates_dir = PROJECT_ROOT / "templates"
            templates_dir.mkdir(parents=True, exist_ok=True)
            tmpl_path = templates_dir / template_file.filename
            with open(tmpl_path, "wb") as buffer:
                shutil.copyfileobj(template_file.file, buffer)

        # ==== Create session lock with ONLY current uploads ====
        uploaded_resume_names = [os.path.basename(p) for p in saved_resumes]
        uploaded_jd_names = [os.path.basename(p) for p in saved_jds]
        
        if not create_session_lock(uploaded_resume_names, uploaded_jd_names):
            return JSONResponse(status_code=500, content={"error": "❌ Failed to create session lock"})

        # ==== Run Pipeline with session isolation ====
        from app.pipeline_runner import run_full_pipeline

        # Run pipeline once for all resumes (pipeline runner handles multiple resumes internally)
        pipeline_result = run_full_pipeline(
            resume_filename=", ".join(uploaded_resume_names),  # Pass all resume names
            jd_filename=", ".join(uploaded_jd_names) if uploaded_jd_names else "",
            user_mode=False,
            clean_run=True
        )

        return JSONResponse(
            status_code=200,
            content={
                "message": "✅ Full pipeline executed successfully with session isolation.",
                "resumes_saved": uploaded_resume_names,
                "jds_saved": uploaded_jd_names or "No JDs uploaded",
                "session_isolated": True,
                "pipeline_result": pipeline_result
            }
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"❌ Pipeline error: {str(e)}"})


# ===== List Tailored CVs (only current session) =====
@app.get("/tailored_cvs")
def list_tailored_cvs():
    try:
        # Only show CVs from current session
        if SESSION_LOCK_PATH.exists():
            with open(SESSION_LOCK_PATH, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            current_resumes = session_data.get('uploaded_resumes', [])
            
            # Filter CVs to only those matching current session resumes
            files = []
            for file in sorted(TAILORED_CV_DIR.glob("*.docx")):
                file_name = file.name
                # Check if this CV belongs to any current session resume
                if any(resume_name.split('.')[0].lower() in file_name.lower() for resume_name in current_resumes):
                    files.append(file_name)
            
            return {"tailored_cvs": files, "session_isolated": True}
        else:
            return {"tailored_cvs": [], "session_isolated": False, "message": "No active session"}
    except Exception as e:
        return {"error": f"Failed to list CVs: {e}"}


# ===== Download all Tailored CVs as ZIP (only current session) =====
@app.get("/download/tailored-cv-docx")
def download_all_tailored_cvs():
    try:
        # Only include CVs from current session
        if SESSION_LOCK_PATH.exists():
            with open(SESSION_LOCK_PATH, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            current_resumes = session_data.get('uploaded_resumes', [])
            
            # Filter CVs to only those matching current session resumes
            session_cvs = []
            # Prefer manifest if available (exact file list from last tailoring)
            manifest_path = TAILORED_CV_DIR.parent / "llm_tailored_cv" / "tailored_manifest.json"
            if manifest_path.exists():
                try:
                    with open(manifest_path, "r", encoding="utf-8") as mf:
                        manifest = json.load(mf) or {}
                    for fname in manifest.get("files", []):
                        full = TAILORED_CV_DIR / fname
                        if full.exists():
                            session_cvs.append(full)
                except Exception:
                    session_cvs = []
            # Fallback to candidate slug match
            if not session_cvs:
                candidate_keys = {os.path.splitext(name)[0].lower().replace(' ', '_') for name in current_resumes}
                for file in sorted(TAILORED_CV_DIR.glob("*.docx")):
                    fn = file.name.lower()
                    if any(fn.startswith(key + "__") for key in candidate_keys):
                        session_cvs.append(file)
            
            if not session_cvs:
                return JSONResponse({"error": "No tailored CVs found for current session"}, status_code=404)

            zip_path = PROJECT_ROOT / "data" / "json" / "tailored_cvs.zip"
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file in session_cvs:
                    zipf.write(file, arcname=file.name)

            return FileResponse(zip_path, media_type="application/zip", filename="tailored_cvs.zip")
        else:
            return JSONResponse({"error": "No active session found"}, status_code=404)
    except Exception as e:
        return JSONResponse({"error": f"Failed to create ZIP: {e}"}, status_code=500)


# ===== Download Rankings PDF (only current session) =====
@app.get("/download/rankings-pdf")
def download_rankings_pdf():
    try:
        # Check if rankings exist for current session
        if SESSION_LOCK_PATH.exists():
            pdf_files = sorted(JOB_RANKINGS_DIR.glob("*.pdf"))
            if not pdf_files:
                return JSONResponse({"error": "No rankings PDF found"}, status_code=404)

            # Take the latest generated PDF
            latest_pdf = pdf_files[-1]
            return FileResponse(latest_pdf, media_type="application/pdf", filename=latest_pdf.name)
        else:
            return JSONResponse({"error": "No active session found"}, status_code=404)
    except Exception as e:
        return JSONResponse({"error": f"Failed to download rankings: {e}"}, status_code=500)


# ===== Health Check ====
@app.get("/health")
def health_check():
    return {"status": "healthy", "session_active": SESSION_LOCK_PATH.exists()}


# ===== Clear Session ====
@app.post("/clear-session")
def clear_current_session():
    """Clear the current session and all associated data"""
    try:
        clear_session_lock()
        return {"message": "✅ Session cleared successfully"}
    except Exception as e:
        return {"error": f"❌ Failed to clear session: {e}"}
