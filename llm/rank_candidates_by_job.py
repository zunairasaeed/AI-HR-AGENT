#before changinng everyhtng works fine  output in json 
# import os
# import json
# from app.llm_utils import call_gpt

# RESULTS_DIR = "data/json/llm_results"
# OUTPUT_FILE = "data/json/rank_candidates_by_job/job_rankings.json"

# job_rankings = {}

# def generate_llm_summary(candidate_name, job_role, percent, qualified):
#     system_prompt = "You are an assistant evaluating job candidates."
#     user_prompt = f"""
# Candidate: {candidate_name}
# Job Role: {job_role}
# Score %: {percent}
# Qualified: {"Yes" if qualified else "No"}

# Summarize why this candidate is ranked as such for the job. Use 2-3 lines, mention if they met the criteria well or lacked some important skills.
# """
#     return call_gpt(system_prompt, user_prompt) or "Summary unavailable."



# def run_candidate_ranking_by_job():
#     job_rankings = {}

#     for filename in os.listdir(RESULTS_DIR):
#         if not filename.endswith("__matches.json"):
#             continue

#         with open(os.path.join(RESULTS_DIR, filename), "r", encoding="utf-8") as f:
#             data = json.load(f)

#         candidate_name = data.get("candidate_name")
#         email = data.get("email", "")
#         phone = data.get("phone", "")
#         linkedin = data.get("linkedin", "")

#         for job in data.get("matched_jobs", []):
#             job_role = job["job_role"]
#             score = job["total_score"]
#             bonus = job["bonus_score"]
#             percent = job["final_percentage"]
#             qualified = job["qualified"]

#             entry = {
#                 "candidate_name": candidate_name,
#                 "email": email,
#                 "phone": phone,
#                 "linkedin": linkedin,
#                 "total_score": score,
#                 "bonus_score": bonus,
#                 "final_percentage": percent,
#                 "qualified": qualified,
#                 "llm_ranking_summary": generate_llm_summary(candidate_name, job_role, percent, qualified)
#             }

#             job_rankings.setdefault(job_role, []).append(entry)

#     # Sort and rank
#     for job, candidates in job_rankings.items():
#         candidates.sort(key=lambda x: x["final_percentage"], reverse=True)
#         for i, c in enumerate(candidates, start=1):
#             c["rank"] = i

#     # Save output
#     os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
#     with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
#         json.dump(job_rankings, out, indent=4)

#     print(f"🎯 Job rankings saved to {OUTPUT_FILE}")


# # 🔥 Optional CLI
# if __name__ == "__main__":
#     run_candidate_ranking_by_job()



#added pdf fucnionalty somewhat satisfied witht he pdf file  


import os
import json
from app.llm_utils import call_gpt
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

RESULTS_DIR = os.getenv("LLM_RESULTS_DIR", "data/json/llm_results")
OUTPUT_FILE = os.getenv("RANK_BY_JOB_JSON", "data/json/rank_candidates_by_job/job_rankings.json")
OUTPUT_PDF = os.getenv("RANK_BY_JOB_PDF", "data/json/rank_candidates_by_job/job_rankings.pdf")
SESSION_LOCK_PATH = os.getenv('SESSION_LOCK_PATH', os.path.join('data', 'session_lock.json'))

job_rankings = {}

def generate_llm_summary(candidate_name, job_role, percent, qualified):
    if os.getenv('SKIP_LLM_SUMMARY', '1') == '1':
        return "(ranking summary skipped)"
    system_prompt = "You are an assistant evaluating job candidates."
    user_prompt = f"""
Candidate: {candidate_name}
Job Role: {job_role}
Score %: {percent}
Qualified: {"Yes" if qualified else "No"}

Summarize why this candidate is ranked as such for the job. Use 2-3 lines, mention if they met the criteria well or lacked some important skills.
"""
    return call_gpt(system_prompt, user_prompt) or "Summary unavailable."


def generate_pdf_from_rankings(job_rankings, output_path=OUTPUT_PDF):
    """Generate PDF report from job rankings dictionary"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    for job, candidates in job_rankings.items():
        # Job heading
        story.append(Paragraph(f"<b>Job Role: {job}</b>", styles["Heading1"]))
        story.append(Spacer(1, 12))

        for c in candidates:
            # Candidate rank + basic info
            story.append(Paragraph(
                f"<b>Rank {c['rank']}:</b> {c['candidate_name']} "
                f"({c['final_percentage']}%) - {'Qualified' if c['qualified'] else 'Not Qualified'}",
                styles["Heading3"]
            ))
            story.append(Spacer(1, 6))

            # Personal info table
            personal_table = [
                ["Email:", c.get("email", "")],
                ["Phone:", c.get("phone", "")],
                ["LinkedIn:", c.get("linkedin", "")]
            ]
            pt = Table(personal_table, hAlign="LEFT")
            pt.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(pt)
            story.append(Spacer(1, 10))

            # Scores table
            score_table = [
                ["Total Score", c.get("total_score", 0)],
                ["Bonus Score", c.get("bonus_score", 0)],
                ["Final %", f"{c.get('final_percentage', 0)}%"],
                ["Qualified", "Yes" if c.get("qualified") else "No"]
            ]
            st = Table(score_table, hAlign="LEFT")
            st.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(st)
            story.append(Spacer(1, 10))

            # Matched keywords (if available)
            if "matched" in c:
                matched = c["matched"]
                for category in ["must_have", "nice_to_have", "bonus"]:
                    if category in matched:
                        words = ", ".join(matched[category].get("matched", []))
                        score_val = matched[category].get("score", 0)
                        story.append(Paragraph(
                            f"<b>{category.replace('_', ' ').title()}:</b> {words} "
                            f"(Score: {score_val})",
                            styles["Normal"]
                        ))
                        story.append(Spacer(1, 6))

            # LLM summary
            if c.get("llm_ranking_summary"):
                story.append(Paragraph("<b>Summary:</b>", styles["Heading4"]))
                story.append(Paragraph(c["llm_ranking_summary"], styles["Normal"]))
                story.append(Spacer(1, 15))

        story.append(Spacer(1, 25))

    doc.build(story)
    print(f"📄 PDF report saved to {output_path}")


def _load_session_resumes_filter():
    try:
        if os.path.exists(SESSION_LOCK_PATH):
            with open(SESSION_LOCK_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f) or {}
            normalized = set(data.get('resumes', []))
            return set([f.replace('.json', '__matches.json') for f in normalized]) if normalized else None
    except Exception:
        pass
    return None

def run_candidate_ranking_by_job():
    job_rankings = {}

    filter_set = _load_session_resumes_filter()
    for filename in os.listdir(RESULTS_DIR):
        if not filename.endswith("__matches.json"):
            continue
        if filter_set is not None and filename not in filter_set:
            continue

        with open(os.path.join(RESULTS_DIR, filename), "r", encoding="utf-8") as f:
            data = json.load(f)

        candidate_name = data.get("candidate_name")
        email = data.get("email", "")
        phone = data.get("phone", "")
        linkedin = data.get("linkedin", "")

        for job in data.get("matched_jobs", []):
            job_role = job["job_role"]
            score = job["total_score"]
            bonus = job["bonus_score"]
            percent = job["final_percentage"]
            qualified = job["qualified"]

            entry = {
                "candidate_name": candidate_name,
                "email": email,
                "phone": phone,
                "linkedin": linkedin,
                "total_score": score,
                "bonus_score": bonus,
                "final_percentage": percent,
                "qualified": qualified,
                "llm_ranking_summary": generate_llm_summary(candidate_name, job_role, percent, qualified),
                "matched": job.get("matched", {})  # ✅ keep matched skills for PDF
            }

            job_rankings.setdefault(job_role, []).append(entry)

    # Sort and rank
    for job, candidates in job_rankings.items():
        candidates.sort(key=lambda x: x["final_percentage"], reverse=True)
        for i, c in enumerate(candidates, start=1):
            c["rank"] = i

    # Save JSON
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(job_rankings, out, indent=4)

    print(f"🎯 Job rankings saved to {OUTPUT_FILE}")

    # Save PDF
    generate_pdf_from_rankings(job_rankings)


# 🔥 Optional CLI
if __name__ == "__main__":
    run_candidate_ranking_by_job()
