# persona_engine/job_parser.py
import json
import os

def load_persona_job(input_dir="/app/input"):
    """
    Looks for a file named `persona_job.json` in the input directory.
    Returns: persona (str), job (str)
    """
    filepath = os.path.join(input_dir, "persona_job.json")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError("persona_job.json not found in input directory!")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    persona = data.get("persona", "").strip()
    job = data.get("job_to_be_done", "").strip()

    if not persona or not job:
        raise ValueError("Invalid or incomplete persona_job.json")

    return persona, job
