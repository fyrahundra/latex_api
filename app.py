import os
import zipfile
import uuid
import subprocess
from flask import Flask, request, send_file, send_from_directory

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB


def pick_tex_file(work_dir: str):
    tex_candidates = []
    for root, _, files in os.walk(work_dir):
        for name in files:
            if name.endswith(".tex"):
                tex_candidates.append(os.path.join(root, name))

    if not tex_candidates:
        return None, []

    preferred_names = {"garb.tex"}
    tex_candidates.sort(
        key=lambda p: (
            os.path.basename(p) not in preferred_names,
            len(os.path.relpath(p, work_dir)),
            p,
        )
    )
    return tex_candidates[0], tex_candidates


def run_command(cmd, cwd):
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120
        )
        return result.stdout.decode(errors="ignore"), result.stderr.decode(errors="ignore")
    except subprocess.TimeoutExpired:
        return "", "Command timed out"


def patch_optional_font_packages(work_dir: str):
    """Make uploaded style files resilient when optional font packages are missing."""
    patched_files = []
    for root, _, files in os.walk(work_dir):
        for name in files:
            if not name.endswith(".sty"):
                continue

            path = os.path.join(root, name)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except OSError:
                continue

            old = "\\usepackage{tgpagella}"
            if old not in content:
                continue

            replacement = (
                "% Auto-fallback for environments where tgpagella is unavailable\n"
                "\\IfFileExists{tgpagella.sty}{\\usepackage{tgpagella}}{\\usepackage{mathpazo}}"
            )
            new_content = content.replace(old, replacement)
            if new_content == content:
                continue

            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                patched_files.append(path)
            except OSError:
                continue

    return patched_files


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/compile", methods=["POST"])
def compile_zip():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]
    job_id = str(uuid.uuid4())
    work_dir = f"/tmp/{job_id}"
    os.makedirs(work_dir, exist_ok=True)

    zip_path = os.path.join(work_dir, "input.zip")
    file.save(zip_path)

    print(f"Saved uploaded file to: {zip_path}")

    # ---- Extract ZIP safely ----
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            print("ZIP contains:", zip_ref.namelist())
            for member in zip_ref.namelist():
                member_path = os.path.join(work_dir, member)
                if os.path.commonpath([work_dir, os.path.abspath(member_path)]) != work_dir:
                    return f"Invalid ZIP entry: {member}", 400
            zip_ref.extractall(work_dir)
    except zipfile.BadZipFile:
        return "Invalid ZIP file", 400

    # ---- Debug extracted files ----
    print("\n--- EXTRACTED FILES ---")
    for root, _, files in os.walk(work_dir):
        for f in files:
            print(os.path.relpath(os.path.join(root, f), work_dir))
    print("--- END EXTRACT ---\n")

    patched = patch_optional_font_packages(work_dir)
    if patched:
        print("Patched optional package fallback in:")
        for p in patched:
            print(" -", p)

    # ---- Find TEX ----
    tex_file, tex_candidates = pick_tex_file(work_dir)
    if not tex_file:
        return "No .tex file found", 400

    tex_dir = os.path.dirname(tex_file)
    tex_name = os.path.basename(tex_file)

    print("Using TEX file:", tex_file)

    # ---- Run latexmk (handles EVERYTHING) ----
    cmd = [
        "latexmk",
        "-pdf",
        "-interaction=nonstopmode",
        "-file-line-error",
        tex_name
    ]

    stdout, stderr = run_command(cmd, tex_dir)

    print("\n--- LATEXMK STDOUT ---\n", stdout)
    print("\n--- LATEXMK STDERR ---\n", stderr)

    # ---- Debug: list files after compile ----
    print("\n--- FILES AFTER COMPILATION ---")
    for root, _, files in os.walk(tex_dir):
        for f in files:
            print(os.path.join(root, f))
    print("--- END FILES ---\n")

    # ---- Return the PDF generated from the selected TEX file ----
    expected_pdf = os.path.splitext(tex_name)[0] + ".pdf"
    pdf_path = os.path.join(tex_dir, expected_pdf)

    if not os.path.exists(pdf_path):
        return (
            "Compilation failed (no PDF found)\n\n"
            f"STDOUT:\n{stdout}\n\nSTDERR:\n{stderr}"
        ), 400

    print(f"Returning PDF: {pdf_path}")
    return send_file(pdf_path, mimetype="application/pdf")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)