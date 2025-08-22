# # pipeline_runner.py

# def run_full_pipeline(resume_filename, jd_filename):
#     """
#     Run the full resume + JD pipeline safely.
#     If any step fails, log the error and continue with the next one.
#     """
#     results = {}

#     try:
#         from app.raw_parser import run_raw_parsing_debug
#         from llm.parser import run_llm_parsing
#         from llm.jd_parser import run_job_parsing
#         from llm.matcher import run_matching
#         from llm.jobs_ranking import run_job_ranking_by_candidate
#         from llm.rank_candidates_by_job import run_candidate_ranking_by_job
#         from llm.parsered_template import run_template_extractor
#         from llm.tailoredcv import tailor_all
#     except ImportError as e:
#         return {"error": f"❌ Import failure: {e}"}

#     # STEP 1
#     try:
#         print(f"\n📄 STEP 1: Raw parsing for {resume_filename}")
#         run_raw_parsing_debug()
#         results["raw_parsing"] = "success"
#     except Exception as e:
#         results["raw_parsing"] = f"failed: {e}"

#     # STEP 2
#     try:
#         print(f"🧠 STEP 2: LLM resume parsing for {resume_filename}")
#         run_llm_parsing()
#         results["llm_parsing"] = "success"
#     except Exception as e:
#         results["llm_parsing"] = f"failed: {e}"

#     # STEP 3
#     try:
#         print(f"📃 STEP 3: Job description parsing for {jd_filename}")
#         run_job_parsing()
#         results["job_parsing"] = "success"
#     except Exception as e:
#         results["job_parsing"] = f"failed: {e}"

#     # STEP 4
#     try:
#         print(f"🔍 STEP 4: Matching for {resume_filename}")
#         run_matching()
#         results["matching"] = "success"
#     except Exception as e:
#         results["matching"] = f"failed: {e}"

#     # STEP 5
#     try:
#         print(f"📊 STEP 5: Ranking jobs for candidate {resume_filename}")
#         run_job_ranking_by_candidate()
#         results["job_ranking"] = "success"
#     except Exception as e:
#         results["job_ranking"] = f"failed: {e}"

#     # STEP 6
#     try:
#         print("📊 STEP 6: Ranking candidates by job")
#         run_candidate_ranking_by_job()
#         results["candidate_ranking"] = "success"
#     except Exception as e:
#         results["candidate_ranking"] = f"failed: {e}"

#     # STEP 7
#     try:
#         print(f"📝 STEP 7: Generating template context for {resume_filename}")
#         run_template_extractor()
#         results["template_extractor"] = "success"
#     except Exception as e:
#         results["template_extractor"] = f"failed: {e}"

#     # STEP 8
#     try:
#         print(f"🎯 STEP 8: Tailoring final CV for {resume_filename}")
#         tailor_all()
#         results["tailored_cv"] = "success"
#     except Exception as e:
#         results["tailored_cv"] = f"failed: {e}"

#     return results



# pipeline_runner.py
from pathlib import Path
import os
import shutil
import json

# === Where this file lives ===
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # repo root (AI-HR-AGENT)

# ---------- Directory map helpers ----------
def build_dirmap(data_root: Path) -> dict:
    """
    data_root:
      - batch mode: <repo>/data
      - user mode : <repo>/data/user_mode
    """
    return {
        # uploads
        "RESUME_DIR":            data_root / "resumes",
        "RAW_JD_DIR":            data_root / "jobs" / "raw_jd",
        "PARSED_JD_DIR":         data_root / "jobs" / "parsed_jd",
        "COMBINED_JD_DIR":       data_root / "jobs" / "parsed_jd" / "combined",

        # resume processing
        "RAW_DATA_DIR":          data_root / "json" / "raw_data",
        "LLM_NORMALIZED_DIR":    data_root / "json" / "llm_normalized",

        # matching + ranking
        "LLM_RESULTS_DIR":       data_root / "json" / "llm_results",
        "RANK_BY_JOB_DIR":       data_root / "json" / "rank_candidates_by_job",

        # tailoring
        "TAILORED_JSON_DIR":     data_root / "json" / "llm_tailored_cv",
        "TAILORED_DOCX_DIR":     data_root / "json" / "tailored_cv_docx",
    }

def ensure_dirs(dirs: dict, clean: bool):
    upload_keys = {"RESUME_DIR", "RAW_JD_DIR"}
    for key, p in dirs.items():
        p.mkdir(parents=True, exist_ok=True)
        if clean and key not in upload_keys:
            # only remove files; keep nested dirs if any
            for child in p.glob("*"):
                try:
                    if child.is_file():
                        child.unlink()
                except Exception:
                    pass

def export_env(dirs: dict):
    """
    Export paths so modules can read them with os.getenv(...)
    """
    for k, v in dirs.items():
        os.environ[k] = str(v)
    # Additional convenience env vars
    # data_root is parent of many paths; here we set user mode dir explicitly
    os.environ['DATA_USER_MODE_DIR'] = str(Path(dirs['RESUME_DIR']).parents[1])
    # Raw file path used by llm/parser
    os.environ['RAW_FILE'] = str(Path(dirs['RAW_DATA_DIR']) / 'raw_data.json')
    # Ranking outputs
    os.environ['RANK_BY_CANDIDATE_DIR'] = str((Path(dirs['LLM_RESULTS_DIR']).parent / 'llm_ranking_by_candidates' / 'by_candidate'))
    os.environ['RANK_BY_JOB_JSON'] = str(Path(dirs['RANK_BY_JOB_DIR']) / 'job_rankings.json')
    os.environ['RANK_BY_JOB_PDF'] = str(Path(dirs['RANK_BY_JOB_DIR']) / 'job_rankings.pdf')
    # Session lock path for session isolation
    os.environ['SESSION_LOCK_PATH'] = str(Path(dirs['RESUME_DIR']).parent / 'session_lock.json')

def ensure_default_template_extracted():
    """Ensure there is at least one extracted template JSON present.
    Writes a minimal default one if none exists to prevent tailoring failures.
    """
    templates_root = Path(__file__).resolve().parents[1] / 'templates' / 'json_extracted_template'
    templates_root.mkdir(parents=True, exist_ok=True)
    has_any = any(
        p.is_file() and p.suffix.lower() == '.json' and p.name.endswith('__extracted_template.json')
        for p in templates_root.glob('*.json')
    )
    if has_any:
        return
    default_sections = {
        "template_name": "Default_Template",
        "sections": {
            "Personal Info": True,
            "Profile / Summary": True,
            "Skills": True,
            "Certifications": True,
            "Functional Skills": True,
            "Business Sector": True,
            "Work Experience": True,
            "Education": True,
            "Project Descriptions": True,
            "Languages": True
        }
    }
    out_path = templates_root / 'Default__extracted_template.json'
    try:
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(default_sections, f, indent=2, ensure_ascii=False)
        print(f"✅ Wrote default extracted template → {out_path}")
    except Exception as e:
        print(f"⚠️ Could not write default template: {e}")

def _read_json_safely(path: Path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

def _dir_has_files(dir_path: Path, suffix: str) -> bool:
    try:
        return any(p.suffix.lower() == suffix for p in dir_path.iterdir() if p.is_file())
    except Exception:
        return False

def _expect_non_empty_json(path: Path, label: str):
    data = _read_json_safely(path)
    if not data:
        raise RuntimeError(f"{label} missing or empty: {path}")

def _expect_dir_has(dir_path: Path, suffix: str, label: str):
    if not _dir_has_files(dir_path, suffix):
        raise RuntimeError(f"{label} not produced in {dir_path}")

# ---------- Public API ----------
def run_full_pipeline(
    resume_filename: str = "",
    jd_filename: str = "",
    user_mode: bool = False,
    clean_run: bool = True,
    skip_llm_summary: bool = True
):
    """
    Run the full pipeline.
    - user_mode=False -> uses <repo>/data (batch mode, your current behavior)
    - user_mode=True  -> uses <repo>/data/user_mode (keeps user uploads isolated)
    - clean_run=True  -> empties all target folders before running so nothing mixes
    """
    # 1) choose root
    data_root = PROJECT_ROOT / "data"  # stay in original folders always

    # 2) prepare directory map + env
    dirs = build_dirmap(data_root)
    ensure_dirs(dirs, clean=clean_run)
    export_env(dirs)
    # Performance toggle for summary generation in downstream modules
    os.environ['SKIP_LLM_SUMMARY'] = '1' if skip_llm_summary else '0'

    # 3) import and run modules in your existing order
    results = {}
    try:
        from app.raw_parser import run_raw_parsing_debug
        from llm.parser import run_llm_parsing
        from llm.jd_parser import run_job_parsing
        from llm.matcher import run_matching
        from llm.jobs_ranking import run_job_ranking_by_candidate
        from llm.rank_candidates_by_job import run_candidate_ranking_by_job
        from llm.parsered_template import run_template_extractor
        from llm.tailoredcv import tailor_all
    except ImportError as e:
        return {"error": f"❌ Import failure: {e}"}

    # STEP 1
    try:
        print(f"\n📄 STEP 1: Raw parsing for {resume_filename}")
        run_raw_parsing_debug()
        # Verify raw_data.json exists and is a non-empty list
        raw_file = Path(os.environ['RAW_FILE'])
        _expect_non_empty_json(raw_file, "Raw parsed resumes")
        results["raw_parsing"] = "success"
    except Exception as e:
        results["raw_parsing"] = f"failed: {e}"

    # STEP 2
    try:
        print(f"🧠 STEP 2: LLM resume parsing for {resume_filename}")
        run_llm_parsing()
        # Verify normalized resumes directory has json
        _expect_dir_has(Path(os.environ['LLM_NORMALIZED_DIR']), ".json", "Normalized resumes")
        results["llm_parsing"] = "success"
    except Exception as e:
        results["llm_parsing"] = f"failed: {e}"

    # STEP 3
    try:
        if jd_filename and jd_filename.strip():
            print(f"📃 STEP 3: Job description parsing for {jd_filename}")
            run_job_parsing()
            # Verify combined JD all_jobs.json exists
            combined_path = Path(os.environ['COMBINED_JD_DIR']) / 'all_jobs.json'
            _expect_non_empty_json(combined_path, "Combined JDs")
            results["job_parsing"] = "success"
        else:
            print("📃 STEP 3: Skipping JD parsing (no JDs uploaded)")
            results["job_parsing"] = "skipped (no JDs)"
    except Exception as e:
        results["job_parsing"] = f"failed: {e}"

    # STEP 4
    try:
        if jd_filename and jd_filename.strip():
            print(f"🔍 STEP 4: Matching for {resume_filename}")
            run_matching()
            # Verify llm_results has __matches.json
            _expect_dir_has(Path(os.environ['LLM_RESULTS_DIR']), ".json", "Matching results")
            results["matching"] = "success"
        else:
            print("🔍 STEP 4: Skipping matching (no JDs available)")
            results["matching"] = "skipped (no JDs)"
    except Exception as e:
        results["matching"] = f"failed: {e}"

    # STEP 5
    try:
        if jd_filename and jd_filename.strip():
            print(f"📊 STEP 5: Ranking jobs for candidate {resume_filename}")
            run_job_ranking_by_candidate()
            _expect_dir_has(Path(os.environ['RANK_BY_CANDIDATE_DIR']), ".json", "Rank-by-candidate results")
            results["job_ranking"] = "success"
        else:
            print("📊 STEP 5: Skipping job ranking (no JDs available)")
            results["job_ranking"] = "skipped (no JDs)"
    except Exception as e:
        results["job_ranking"] = f"failed: {e}"

    # STEP 6  (this module now produces the PDF; make sure it writes to RANK_BY_JOB_DIR)
    try:
        if jd_filename and jd_filename.strip():
            print("📊 STEP 6: Ranking candidates by job (PDF output)")
            run_candidate_ranking_by_job()
            # JSON always saved; PDF may also be saved
            _expect_non_empty_json(Path(os.environ['RANK_BY_JOB_JSON']), "Rank-by-job JSON")
            results["candidate_ranking"] = "success"
        else:
            print("📊 STEP 6: Skipping candidate ranking (no JDs available)")
            results["candidate_ranking"] = "skipped (no JDs)"
    except Exception as e:
        results["candidate_ranking"] = f"failed: {e}"

    # STEP 7
    try:
        print(f"📝 STEP 7: Generating template context for {resume_filename}")
        run_template_extractor()
        results["template_extractor"] = "success"
    except Exception as e:
        results["template_extractor"] = f"failed: {e}"

    # STEP 8
    try:
        if jd_filename and jd_filename.strip():
            # ensure a default extracted template is present so tailoring never fails
            ensure_default_template_extracted()
            print(f"🎯 STEP 8: Tailoring final CV for {resume_filename}")
            tailor_all()
            results["tailored_cv"] = "success"
        else:
            print("🎯 STEP 8: Skipping CV tailoring (no JDs available)")
            results["tailored_cv"] = "skipped (no JDs)"
    except Exception as e:
        results["tailored_cv"] = f"failed: {e}"

    return results
