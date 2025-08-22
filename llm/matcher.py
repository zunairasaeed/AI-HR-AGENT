
####################workig fne below code have only checks to know which step of matchin we are at 

# import os
# import json
# import re
# from app.llm_utils import call_gpt

# # === CONFIGURATION ===
# RESUMES_DIR = "data/json/llm_normalized"
# JOBS_FILE = "data/jobs/parsed_jd"
# RESULTS_DIR = "data/json/llm_results"
# os.makedirs(RESULTS_DIR, exist_ok=True)

# CATEGORY_WEIGHTS = {
#     "must_have": 5,
#     "nice_to_have": 3,
#     "bonus": 2
# }

# QUALIFICATION_PERCENTAGE = 75

# def normalize_text(text):
#     return re.sub(r'\s+', ' ', text.lower().strip())

# def get_match_context(resume_data):
#     context = []
#     context += resume_data.get("skills", [])
#     context += resume_data.get("keywords", [])
#     context += resume_data.get("certificates", [])
#     context += re.findall(r'\b\w+\b', resume_data.get("raw_text", "").lower())
#     return list(set([normalize_text(word) for word in context if len(word) > 1]))

# def match_keywords(context_words, keywords):
#     return list(set([kw for kw in keywords if normalize_text(kw) in context_words]))

# def call_llm_summary(resume_data, job_role, job_keywords):
#     system_prompt = "You are a helpful assistant that analyzes resumes for job relevance."
#     user_prompt = f"""
# You are given the following candidate resume:

# Name: {resume_data.get('name')}
# Skills: {resume_data.get('skills')}
# Certificates: {resume_data.get('certificates')}
# Experience: {resume_data.get('experience')}
# Projects: {resume_data.get('projects')}
# Keywords: {resume_data.get('keywords')}

# Match this candidate to the job role: "{job_role}".

# The job requires:
# - Must-have: {job_keywords.get("must_have", [])}
# - Nice-to-have: {job_keywords.get("nice_to_have", [])}
# - Bonus/Tools: {job_keywords.get("bonus", [])}
# - Responsibilities: {job_keywords.get("responsibilities", [])}
# - Requirements: {job_keywords.get("requirements", [])}
# - Description: {job_keywords.get("description", "")}

# Return a short reasoning (3-4 lines) on whether this candidate is a good fit or not.
# """
#     response = call_gpt(system_prompt, user_prompt)
#     return response or "LLM could not generate summary."

# def collect_max_scores(jobs_data):
#     max_scores = {role: 0 for role in jobs_data}
#     for resume_file in os.listdir(RESUMES_DIR):
#         if not resume_file.endswith(".json"):
#             continue
#         with open(os.path.join(RESUMES_DIR, resume_file), 'r', encoding='utf-8') as f:
#             resume_data = json.load(f)
#         context_words = get_match_context(resume_data)
#         for role, job in jobs_data.items():
#             score = sum(len(match_keywords(context_words, job.get(cat, []))) * CATEGORY_WEIGHTS[cat]
#                         for cat in ["must_have", "nice_to_have"])
#             if score > max_scores[role]:
#                 max_scores[role] = score
#     return max_scores

# def process_resume(file_name, jobs_data, job_max_scores):
#     resume_path = os.path.join(RESUMES_DIR, file_name)
#     with open(resume_path, 'r', encoding='utf-8') as f:
#         resume_data = json.load(f)

#     context_words = get_match_context(resume_data)
#     result_path = os.path.join(RESULTS_DIR, file_name.replace(".json", "__matches.json"))

#     # Load existing result if exists
#     if os.path.exists(result_path):
#         with open(result_path, "r", encoding="utf-8") as f:
#             existing_result = json.load(f)
#         matched_jobs = {job["job_role"]: job for job in existing_result.get("matched_jobs", [])}
#     else:
#         matched_jobs = {}

#     # 🔄 ✅ UPDATED MATCHING LOGIC: Always match every job and record the result, even if empty
#     for role, job in jobs_data.items():
#         matched_summary = {}
#         total_score = 0
#         bonus_score = 0

#         for category in ["must_have", "nice_to_have", "bonus"]:
#             items = job.get(category, [])
#             matched = match_keywords(context_words, items)
#             score = len(matched) * CATEGORY_WEIGHTS[category]

#             if category != "bonus":
#                 total_score += score
#             else:
#                 bonus_score = score

#             matched_summary[category] = {
#                 "matched": matched,
#                 "score": score
#             }

#         max_score = job_max_scores.get(role, 1)
#         match_percentage = (total_score / max_score * 100) if max_score > 0 else 0
#         match_percentage += bonus_score
#         qualified = match_percentage >= QUALIFICATION_PERCENTAGE

#         llm_summary = call_llm_summary(resume_data, role, job)

#         matched_jobs[role] = {
#             "job_role": role,
#             "matched": matched_summary,
#             "total_score": total_score,
#             "bonus_score": bonus_score,
#             "max_score_among_candidates": max_score,
#             "final_percentage": round(match_percentage, 2),
#             "qualified": qualified,
#             "llm_summary": llm_summary
#         }

#     result = {
#         "resume_file": file_name,
#         "candidate_name": resume_data.get("name", "Unknown"),
#         "email": resume_data.get("email", ""),
#         "phone": resume_data.get("phone", ""),
#         "linkedin": resume_data.get("linkedin", ""),
#         "matched_jobs": list(matched_jobs.values())
#     }

#     with open(result_path, "w", encoding="utf-8") as out:
#         json.dump(result, out, indent=4)


# def run_matching():
#     jobs_data = {}

#     # 🔁 Load each parsed JD file
#     for file in os.listdir(JOBS_FILE):
#         if file.endswith(".json"):
#             filepath = os.path.join(JOBS_FILE, file)
#             with open(filepath, "r", encoding="utf-8") as f:
#                 jd_content = json.load(f)

#                 # ✅ Case 1: Multi-job post in a file under "jobs" key
#                 if isinstance(jd_content, dict) and "jobs" in jd_content:
#                     for job in jd_content["jobs"]:
#                         job_title = job.get("job_title")
#                         if job_title:
#                             jobs_data[job_title] = {
#                                 "must_have": job.get("must_have_skills", []),
#                                 "nice_to_have": job.get("nice_to_have_skills", []),
#                                 "bonus": job.get("tools", []),
#                                 "responsibilities": job.get("responsibilities", []),
#                                 "requirements": job.get("requirements", []),
#                                 "description": job.get("description", "")
#                             }

#                 # ✅ Case 2: List of job dicts
#                 elif isinstance(jd_content, list):
#                     for job in jd_content:
#                         job_title = job.get("job_title")
#                         if job_title:
#                             jobs_data[job_title] = {
#                                 "must_have": job.get("must_have_skills", []),
#                                 "nice_to_have": job.get("nice_to_have_skills", []),
#                                 "bonus": job.get("tools", []),
#                                 "responsibilities": job.get("responsibilities", []),
#                                 "requirements": job.get("requirements", []),
#                                 "description": job.get("description", "")
#                             }

#                 # ✅ Case 3: Single job dict
#                 elif isinstance(jd_content, dict) and "job_title" in jd_content:
#                     job_title = jd_content.get("job_title", file.replace(".json", ""))
#                     jobs_data[job_title] = {
#                         "must_have": jd_content.get("must_have_skills", []),
#                         "nice_to_have": jd_content.get("nice_to_have_skills", []),
#                         "bonus": jd_content.get("tools", []),
#                         "responsibilities": jd_content.get("responsibilities", []),
#                         "requirements": jd_content.get("requirements", []),
#                         "description": jd_content.get("description", "")
#                     }

#                 # ✅ Case 4: Custom dict format with job titles as keys
#                 elif isinstance(jd_content, dict):
#                     for job_title, job in jd_content.items():
#                         jobs_data[job_title] = {
#                             "must_have": job.get("must_have", []),
#                             "nice_to_have": job.get("nice_to_have", []),
#                             "bonus": job.get("bonus", []),
#                             "responsibilities": job.get("responsibilities", []),
#                             "requirements": job.get("requirements", []),
#                             "description": job.get("description", "")
#                         }

#     # ✅ Compute max scores
#     job_max_scores = collect_max_scores(jobs_data)

#     # ✅ Match each resume
#     for resume_file in os.listdir(RESUMES_DIR):
#         if resume_file.endswith(".json"):
#             process_resume(resume_file, jobs_data, job_max_scores)

# # 🔥 Optional for standalone execution
# if __name__ == "__main__":
#     run_matching()







import os
import json
import re
from app.llm_utils import call_gpt

# === CONFIGURATION ===
RESUMES_DIR = os.getenv("LLM_NORMALIZED_DIR", "data/json/llm_normalized")
JOBS_FILE = os.getenv("COMBINED_JD_DIR", "data/jobs/parsed_jd/combined")
RESULTS_DIR = os.getenv("LLM_RESULTS_DIR", "data/json/llm_results")
SESSION_LOCK_PATH = os.getenv('SESSION_LOCK_PATH', os.path.join('data', 'session_lock.json'))
os.makedirs(RESULTS_DIR, exist_ok=True)

CATEGORY_WEIGHTS = {
    "must_have": 5,
    "nice_to_have": 3,
    "bonus": 2
}

QUALIFICATION_PERCENTAGE = 75

def normalize_text(text):
    return re.sub(r'\s+', ' ', text.lower().strip())

def get_match_context(resume_data):
    context = []
    context += resume_data.get("skills", [])
    context += resume_data.get("keywords", [])
    context += resume_data.get("certificates", [])
    context += re.findall(r'\b\w+\b', resume_data.get("raw_text", "").lower())
    return list(set([normalize_text(word) for word in context if len(word) > 1]))

def match_keywords(context_words, keywords):
    return list(set([kw for kw in keywords if normalize_text(kw) in context_words]))

def call_llm_summary(resume_data, job_role, job_keywords):
    # Allow skipping for speed
    if os.getenv('SKIP_LLM_SUMMARY', '1') == '1':
        return "(summary skipped)"
    system_prompt = "You are a helpful assistant that analyzes resumes for job relevance."
    user_prompt = f"""
You are given the following candidate resume:

Name: {resume_data.get('name')}
Skills: {resume_data.get('skills')}
Certificates: {resume_data.get('certificates')}
Experience: {resume_data.get('experience')}
Projects: {resume_data.get('projects')}
Keywords: {resume_data.get('keywords')}

Match this candidate to the job role: "{job_role}".

The job requires:
- Must-have: {job_keywords.get("must_have", [])}
- Nice-to-have: {job_keywords.get("nice_to_have", [])}
- Bonus/Tools: {job_keywords.get("bonus", [])}
- Responsibilities: {job_keywords.get("responsibilities", [])}
- Requirements: {job_keywords.get("requirements", [])}
- Description: {job_keywords.get("description", "")}

Return a short reasoning (3-4 lines) on whether this candidate is a good fit or not.
"""
    response = call_gpt(system_prompt, user_prompt)
    return response or "LLM could not generate summary."

def _load_session_resumes_filter():
    try:
        if os.path.exists(SESSION_LOCK_PATH):
            with open(SESSION_LOCK_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f) or {}
            return set(data.get('resumes', []))
    except Exception:
        pass
    return None

def collect_max_scores(jobs_data):
    max_scores = {role: 0 for role in jobs_data}
    filter_set = _load_session_resumes_filter()
    for resume_file in os.listdir(RESUMES_DIR):
        if not resume_file.endswith(".json"):
            continue
        if filter_set is not None and resume_file not in filter_set:
            continue
        with open(os.path.join(RESUMES_DIR, resume_file), 'r', encoding='utf-8') as f:
            resume_data = json.load(f)
        context_words = get_match_context(resume_data)
        for role, job in jobs_data.items():
            score = sum(len(match_keywords(context_words, job.get(cat, []))) * CATEGORY_WEIGHTS[cat]
                        for cat in ["must_have", "nice_to_have"])
            if score > max_scores[role]:
                max_scores[role] = score
    return max_scores

def process_resume(file_name, jobs_data, job_max_scores):
    resume_path = os.path.join(RESUMES_DIR, file_name)
    with open(resume_path, 'r', encoding='utf-8') as f:
        resume_data = json.load(f)

    print(f"\n🟢 Processing resume: {file_name} (Candidate: {resume_data.get('name', 'Unknown')})")

    context_words = get_match_context(resume_data)
    result_path = os.path.join(RESULTS_DIR, file_name.replace(".json", "__matches.json"))

    # Always start fresh for current session
    matched_jobs = {}

    # 🔄 ✅ UPDATED MATCHING LOGIC: Always match every job and record the result, even if empty
    for role, job in jobs_data.items():
        print(f"   🔎 Matching candidate '{resume_data.get('name', 'Unknown')}' → Job: {role}")

        matched_summary = {}
        total_score = 0
        bonus_score = 0

        for category in ["must_have", "nice_to_have", "bonus"]:
            items = job.get(category, [])
            matched = match_keywords(context_words, items)
            score = len(matched) * CATEGORY_WEIGHTS[category]

            if category != "bonus":
                total_score += score
            else:
                bonus_score = score

            matched_summary[category] = {
                "matched": matched,
                "score": score
            }

        max_score = job_max_scores.get(role, 1)
        match_percentage = (total_score / max_score * 100) if max_score > 0 else 0
        match_percentage += bonus_score
        qualified = match_percentage >= QUALIFICATION_PERCENTAGE

        llm_summary = call_llm_summary(resume_data, role, job)

        matched_jobs[role] = {
            "job_role": role,
            "matched": matched_summary,
            "total_score": total_score,
            "bonus_score": bonus_score,
            "max_score_among_candidates": max_score,
            "final_percentage": round(match_percentage, 2),
            "qualified": qualified,
            "llm_summary": llm_summary
        }

    result = {
        "resume_file": file_name,
        "candidate_name": resume_data.get("name", "Unknown"),
        "email": resume_data.get("email", ""),
        "phone": resume_data.get("phone", ""),
        "linkedin": resume_data.get("linkedin", ""),
        "matched_jobs": list(matched_jobs.values())
    }

    with open(result_path, "w", encoding="utf-8") as out:
        json.dump(result, out, indent=4)

    print(f"✅ Finished matching for: {file_name} (results saved → {result_path})")


def run_matching():
    print("\n🚀 Starting Matching Pipeline...\n")
    jobs_data = {}

    # 🔁 Load each parsed JD file
    for file in os.listdir(JOBS_FILE):
        if file.endswith(".json"):
            filepath = os.path.join(JOBS_FILE, file)
            with open(filepath, "r", encoding="utf-8") as f:
                jd_content = json.load(f)

                # ✅ Case 1: Multi-job post in a file under "jobs" key
                if isinstance(jd_content, dict) and "jobs" in jd_content:
                    for job in jd_content["jobs"]:
                        job_title = job.get("job_title")
                        if job_title:
                            jobs_data[job_title] = {
                                "must_have": job.get("must_have_skills", []),
                                "nice_to_have": job.get("nice_to_have_skills", []),
                                "bonus": job.get("tools", []),
                                "responsibilities": job.get("responsibilities", []),
                                "requirements": job.get("requirements", []),
                                "description": job.get("description", "")
                            }

                # ✅ Case 2: List of job dicts
                elif isinstance(jd_content, list):
                    for job in jd_content:
                        job_title = job.get("job_title")
                        if job_title:
                            jobs_data[job_title] = {
                                "must_have": job.get("must_have_skills", []),
                                "nice_to_have": job.get("nice_to_have_skills", []),
                                "bonus": job.get("tools", []),
                                "responsibilities": job.get("responsibilities", []),
                                "requirements": job.get("requirements", []),
                                "description": job.get("description", "")
                            }

                # ✅ Case 3: Single job dict
                elif isinstance(jd_content, dict) and "job_title" in jd_content:
                    job_title = jd_content.get("job_title", file.replace(".json", ""))
                    jobs_data[job_title] = {
                        "must_have": jd_content.get("must_have_skills", []),
                        "nice_to_have": jd_content.get("nice_to_have_skills", []),
                        "bonus": jd_content.get("tools", []),
                        "responsibilities": jd_content.get("responsibilities", []),
                        "requirements": jd_content.get("requirements", []),
                        "description": jd_content.get("description", "")
                    }

                # ✅ Case 4: Custom dict format with job titles as keys
                elif isinstance(jd_content, dict):
                    for job_title, job in jd_content.items():
                        jobs_data[job_title] = {
                            "must_have": job.get("must_have", []),
                            "nice_to_have": job.get("nice_to_have", []),
                            "bonus": job.get("bonus", []),
                            "responsibilities": job.get("responsibilities", []),
                            "requirements": job.get("requirements", []),
                            "description": job.get("description", "")
                        }

    print(f"📂 Loaded {len(jobs_data)} job roles from JD files.")

    # ✅ Check if we have any jobs to match against
    if not jobs_data:
        print("⚠️ No job descriptions found. Skipping matching step.")
        return

    # ✅ Compute max scores
    job_max_scores = collect_max_scores(jobs_data)
    print("📊 Max scores computed for all jobs.")

    # ✅ Match each resume
    filter_set = _load_session_resumes_filter()
    resumes = [f for f in os.listdir(RESUMES_DIR) if f.endswith('.json') and (filter_set is None or f in filter_set)]
    for resume_file in resumes:
        process_resume(resume_file, jobs_data, job_max_scores)

    print("\n🎉 All matching completed! Results saved in:", RESULTS_DIR)

# 🔥 Optional for standalone execution
if __name__ == "__main__":
    run_matching()




