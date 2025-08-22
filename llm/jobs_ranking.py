

import os
import json
from app.llm_utils import call_gpt


RESULTS_DIR = os.getenv("LLM_RESULTS_DIR", "data/json/llm_results")
OUTPUT_DIR = os.getenv("RANK_BY_CANDIDATE_DIR", "data/json/llm_ranking_by_candidates/by_candidate")
os.makedirs(OUTPUT_DIR, exist_ok=True)
SESSION_LOCK_PATH = os.getenv('SESSION_LOCK_PATH', os.path.join('data', 'session_lock.json'))

def generate_llm_summary(candidate_name, job_title, score, qualified):
    if os.getenv('SKIP_LLM_SUMMARY', '1') == '1':
        return "(ranking summary skipped)"
    system_prompt = "You are an expert assistant helping HR rank candidates."
    user_prompt = f"""
Candidate: {candidate_name}
Job Role: {job_title}
Score: {score}
Qualified: {"Yes" if qualified else "No"}

Explain in 3-4 lines why this candidate ranked where they did for this job. Mention if their score was high or low, and any specific strength or gap if known.
"""
    return call_gpt(system_prompt, user_prompt) or "No summary available."

def _load_session_resumes_filter():
    try:
        if os.path.exists(SESSION_LOCK_PATH):
            with open(SESSION_LOCK_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f) or {}
            # Map llm_normalized <candidate>.json → results <candidate>__matches.json
            normalized = set(data.get('resumes', []))
            return set([f.replace('.json', '__matches.json') for f in normalized]) if normalized else None
    except Exception:
        pass
    return None

"""
Note: Ranking now only runs when run_job_ranking_by_candidate() is called, not on import.
This avoids accidental batch processing and keeps strict session scoping.
"""


def run_job_ranking_by_candidate():
    filter_set = _load_session_resumes_filter()
    for filename in os.listdir(RESULTS_DIR):
        if not filename.endswith("__matches.json"):
            continue
        if filter_set is not None and filename not in filter_set:
            continue

        with open(os.path.join(RESULTS_DIR, filename), "r", encoding="utf-8") as f:
            data = json.load(f)

        candidate = {
            "name": data.get("candidate_name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "linkedin": data.get("linkedin"),
        }

        ranked_jobs = data.get("matched_jobs", [])
        ranked_jobs.sort(key=lambda x: x["final_percentage"], reverse=True)

        for i, job in enumerate(ranked_jobs, start=1):
            job["rank"] = i
            job["llm_ranking_summary"] = generate_llm_summary(
                candidate["name"], job["job_role"], job["final_percentage"], job["qualified"]
            )

        result = {
            "candidate": candidate,
            "ranked_jobs": ranked_jobs
        }

        out_path = os.path.join(OUTPUT_DIR, filename.replace("__matches.json", "__ranked_jobs.json"))
        with open(out_path, "w", encoding="utf-8") as out:
            json.dump(result, out, indent=4)

        print(f"✅ Ranked: {filename}")

# 🔥 Optional for standalone CLI use
if __name__ == "__main__":
    run_job_ranking_by_candidate()
