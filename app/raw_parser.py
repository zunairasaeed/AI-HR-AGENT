
import os
import json
from docx import Document
from pdfminer.high_level import extract_text

# Allow env overrides set by pipeline_runner
RESUME_DIR = os.getenv('RESUME_DIR', 'data/resumes')
RAW_DATA_DIR = os.getenv('RAW_DATA_DIR', 'data/json/raw_data')
OUTPUT_FILE = os.path.join(RAW_DATA_DIR, 'raw_data.json')
SESSION_LOCK_PATH = os.getenv('SESSION_LOCK_PATH', os.path.join('data', 'session_lock.json'))

def extract_text_from_docx(path):
    try:
        doc = Document(path)
        return '\n'.join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"❌ Error reading DOCX file {path}: {e}")
        return ""

def extract_text_from_pdf(path):
    try:
        return extract_text(path)
    except Exception as e:
        print(f"❌ Error reading PDF file {path}: {e}")
        return ""

def extract_raw_data(file_path):
    ext = file_path.split('.')[-1].lower()
    if ext == 'pdf':
        return extract_text_from_pdf(file_path)
    elif ext == 'docx':
        return extract_text_from_docx(file_path)
    else:
        return ""

def _load_session_uploaded_resumes():
    try:
        if os.path.exists(SESSION_LOCK_PATH):
            with open(SESSION_LOCK_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f) or {}
            return set(data.get('uploaded_resumes', []))
    except Exception:
        pass
    return None

def _update_session_uploaded_resumes(single_file):
    try:
        os.makedirs(os.path.dirname(SESSION_LOCK_PATH), exist_ok=True)
        data = {}
        if os.path.exists(SESSION_LOCK_PATH):
            with open(SESSION_LOCK_PATH, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f) or {}
                except json.JSONDecodeError:
                    data = {}
        uploaded = set(data.get('uploaded_resumes', []))
        if single_file:
            uploaded.add(single_file)
        data['uploaded_resumes'] = sorted(uploaded)
        with open(SESSION_LOCK_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Could not update session lock (uploaded_resumes): {e}")

def extract_all_resumes():
    data = []
    filter_set = _load_session_uploaded_resumes()
    for file_name in os.listdir(RESUME_DIR):
        if file_name.endswith(('.pdf', '.docx')):
            if filter_set is not None and file_name not in filter_set:
                continue
            full_path = os.path.join(RESUME_DIR, file_name)
            print(f"📄 Parsing {file_name}...")
            text = extract_raw_data(full_path)
            data.append({
                "filename": file_name,
                "path": full_path,
                "raw_text": text.strip()
            })
    return data

def save_to_json(data, file_name):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# ✅ THIS is the function FastAPI calls now
def run_raw_parsing_debug(single_file=None):
    if single_file:
        file_path = os.path.join(RESUME_DIR, single_file)
        print(f"📄 Raw parsing single file: {single_file}")
        text = extract_raw_data(file_path)
        result = [{
            "filename": single_file,
            "path": file_path,
            "raw_text": text.strip()
        }]
        _update_session_uploaded_resumes(single_file)

    else:
        print("📄 Raw parsing all resumes...")
        result = extract_all_resumes()

    save_to_json(result, OUTPUT_FILE)
    print(f"\n✅ Saved raw data for {len(result)} resume(s) to {OUTPUT_FILE}")

# ✅ Run when executed directly (for testing only)
if __name__ == "__main__":
    run_raw_parsing_debug()


print("✅ raw_parser module loaded from:", __file__)
print("✅ run_raw_parsing_debug exists:", 'run_raw_parsing_debug' in dir())
