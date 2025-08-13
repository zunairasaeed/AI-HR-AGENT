# from pathlib import Path
# from dotenv import load_dotenv
# import os

# # 🔥 Load env before anything else
# PROJECT_ROOT = Path(__file__).resolve().parent.parent
# load_dotenv(dotenv_path=PROJECT_ROOT / ".env")
# print("✅ ENV LOADED:", os.getenv("AZURE_OPENAI_API_KEY")[:8])



# from fastapi import FastAPI, UploadFile, File
# from fastapi.responses import JSONResponse
# from pathlib import Path
# import shutil
# import os

# # ✅ Load .env from the absolute path (so it always works)
# from dotenv import load_dotenv
# PROJECT_ROOT = Path(__file__).resolve().parent.parent
# ENV_PATH = PROJECT_ROOT / ".env"
# load_dotenv(dotenv_path=ENV_PATH)

# app = FastAPI()

# # === Setup Upload Directory ===
# UPLOAD_DIR = PROJECT_ROOT / "data" / "resumes"
# UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# @app.post("/upload")
# async def upload_and_process(file: UploadFile = File(...)):
#     filename = file.filename
#     ext = filename.split(".")[-1].lower()

#     if ext not in ["pdf", "docx"]:
#         return JSONResponse(status_code=400, content={"error": "❌ Only PDF or DOCX allowed."})

#     # ✅ Save uploaded file
#     file_path = UPLOAD_DIR / filename
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     try:
#         # ✅ STEP-BY-STEP PIPELINE CALLS
#         from app.raw_parser import run_raw_parsing_debug
#         from llm.parser import run_llm_parsing
#         from llm.jd_parser import run_job_parsing
#         from llm.matcher import run_matching
#         from llm.jobs_ranking import run_job_ranking_by_candidate
#         from llm.rank_candidates_by_job import run_candidate_ranking_by_job
#         from llm.parsered_template import run_template_extractor
#         from llm.tailoredcv import tailor_all

#         print(f"\n📄 STEP 1: Raw parsing for {filename}")
#         run_raw_parsing_debug()

#         print(f"🧠 STEP 2: LLM resume parsing for {filename}")
#         run_llm_parsing()

#         print("📃 STEP 3: Job description parsing")
#         run_job_parsing()
 
#         print(f"🔍 STEP 4: Matching for {filename}")
#         run_matching()

#         print(f"📊 STEP 5: Ranking jobs for candidate {filename}")
#         run_job_ranking_by_candidate()

#         print("📊 STEP 6: Ranking candidates by job")
#         run_candidate_ranking_by_job()

#         print(f"📝 STEP 7: Generating template context for {filename}")
#         run_template_extractor()

#         print(f"🎯 STEP 8: Tailoring final CV for {filename}")
#         tailor_all()

#         base_name = filename.rsplit(".", 1)[0]
#         tailored_output = f"data/json/llm_tailored_cv/{base_name}__<job>__tailored.docx"

#         return JSONResponse(
#             status_code=200,
#             content={
#                 "message": "✅ Full pipeline executed successfully.",
#                 "tailored_cv_path": tailored_output
#             }
#         )

#     except Exception as e:
#         return JSONResponse(
#             status_code=500,
#             content={"error": f"❌ Pipeline error: {str(e)}"})

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
 #####                       results


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
# testing phase


## testings

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


# # ===== List Tailored CVs (optional) =====
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

from pathlib import Path
from dotenv import load_dotenv
import os
import shutil
import json
import zipfile
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fpdf import FPDF

# ===== Load ENV =====
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")
print("✅ ENV LOADED:", os.getenv("AZURE_OPENAI_API_KEY")[:8])

# ===== Setup App =====
app = FastAPI()

# === Setup Upload Directories ===
RESUME_DIR = PROJECT_ROOT / "data" / "resumes"
JD_DIR = PROJECT_ROOT / "data" / "jds"
RESUME_DIR.mkdir(parents=True, exist_ok=True)
JD_DIR.mkdir(parents=True, exist_ok=True)

TAILORED_CV_DIR = PROJECT_ROOT / "data" / "json" / "tailored_cv_docx"
JOB_RANKINGS_DIR = PROJECT_ROOT / "data" / "json" / "rank_candidates_by_job"
TAILORED_CV_DIR.mkdir(parents=True, exist_ok=True)
JOB_RANKINGS_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload")
async def upload_and_process(
    resume: UploadFile = File(...),
    jd: UploadFile = File(...)
):
    try:
        # ===== Check File Extensions =====
        for file in [resume, jd]:
            ext = file.filename.split(".")[-1].lower()
            if ext not in ["pdf", "docx"]:
                return JSONResponse(
                    status_code=400,
                    content={"error": f"❌ {file.filename}: Only PDF or DOCX allowed."}
                )

        # ===== Save Resume =====
        resume_path = RESUME_DIR / resume.filename
        with open(resume_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)

        # ===== Save JD =====
        jd_path = JD_DIR / jd.filename
        with open(jd_path, "wb") as buffer:
            shutil.copyfileobj(jd.file, buffer)

        # ===== Run Pipeline =====
        # Import your pipeline functions here; adjust as per your project structure
        from app.raw_parser import run_raw_parsing_debug
        from llm.parser import run_llm_parsing
        from llm.jd_parser import run_job_parsing
        from llm.matcher import run_matching
        from llm.jobs_ranking import run_job_ranking_by_candidate
        from llm.rank_candidates_by_job import run_candidate_ranking_by_job
        from llm.parsered_template import run_template_extractor
        from llm.tailoredcv import tailor_all

        print(f"\n📄 STEP 1: Raw parsing for {resume.filename}")
        run_raw_parsing_debug()

        print(f"🧠 STEP 2: LLM resume parsing for {resume.filename}")
        run_llm_parsing()

        print(f"📃 STEP 3: Job description parsing for {jd.filename}")
        run_job_parsing()

        print(f"🔍 STEP 4: Matching for {resume.filename}")
        run_matching()

        print(f"📊 STEP 5: Ranking jobs for candidate {resume.filename}")
        run_job_ranking_by_candidate()

        print("📊 STEP 6: Ranking candidates by job")
        run_candidate_ranking_by_job()

        print(f"📝 STEP 7: Generating template context for {resume.filename}")
        run_template_extractor()

        print(f"🎯 STEP 8: Tailoring final CV for {resume.filename}")
        tailor_all()

        return JSONResponse(
            status_code=200,
            content={
                "message": "✅ Full pipeline executed successfully.",
                "resume_saved": str(resume_path),
                "jd_saved": str(jd_path)
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"❌ Pipeline error: {str(e)}"}
        )


# ===== List Tailored CVs =====
@app.get("/tailored_cvs")
def list_tailored_cvs():
    files = sorted(TAILORED_CV_DIR.glob("*.docx"))
    return {"tailored_cvs": [file.name for file in files]}  # Return only file names


# ===== Download all Tailored CVs as ZIP =====
@app.get("/download/tailored-cv-docx")
def download_all_tailored_cvs():
    files = sorted(TAILORED_CV_DIR.glob("*.docx"))
    if not files:
        return JSONResponse({"error": "No tailored CVs found"}, status_code=404)

    zip_path = PROJECT_ROOT / "data" / "json" / "tailored_cvs.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in files:
            zipf.write(file, arcname=file.name)

    return FileResponse(zip_path, media_type="application/zip", filename="tailored_cvs.zip")


# ===== Convert Rankings JSON → PDF and serve =====
@app.get("/download/rankings-pdf")
def download_rankings_pdf():
    files = sorted(JOB_RANKINGS_DIR.glob("*.json"))
    if not files:
        return JSONResponse({"error": "No rankings found"}, status_code=404)

    pdf = FPDF()
    pdf.set_font("Arial", size=12)

    for file in files:
        pdf.add_page()
        pdf.cell(200, 10, f"Rankings: {file.name}", ln=True)
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                pdf.multi_cell(0, 10, json.dumps(data, indent=2))
        except Exception as e:
            pdf.multi_cell(0, 10, f"Error reading {file.name}: {e}")

    output_path = PROJECT_ROOT / "data" / "json" / "rankings_combined.pdf"
    pdf.output(str(output_path))
    return FileResponse(output_path, media_type="application/pdf", filename="rankings_combined.pdf")
