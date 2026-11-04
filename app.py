from flask import Flask, request, jsonify
import json
import os
import re

app = Flask(__name__)

SUBMISSIONS_FILE = "submissions.json"

def load_submissions():
    if os.path.exists(SUBMISSIONS_FILE):
        with open(SUBMISSIONS_FILE, "r") as f:
            return json.load(f)
    return []

def save_submissions(submissions):
    with open(SUBMISSIONS_FILE, "w") as f:
        json.dump(submissions, f, indent=2)

def is_valid_url(url):
    pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(pattern.match(url))

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Assignment Submission Portal</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; padding: 20px; background: #f0f4f8; }
        h1 { color: #2c3e50; text-align: center; }
        .form-box { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        input { width: 100%; padding: 10px; margin: 8px 0 16px 0; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
        button { background: #3498db; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; width: 100%; font-size: 16px; }
        button:hover { background: #2980b9; }
        #message { margin-top: 15px; padding: 10px; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        .submissions { background: white; padding: 20px; border-radius: 10px; margin-top: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
        th { background: #3498db; color: white; }
        label { font-weight: bold; color: #555; }
    </style>
</head>
<body>
    <h1>📚 Assignment Submission Portal</h1>
    <div class="form-box">
        <label>Student Name *</label>
        <input type="text" id="name" placeholder="Enter your full name">
        <label>Registration Number *</label>
        <input type="text" id="reg" placeholder="e.g. FA21-BSE-001">
        <label>Assignment Title *</label>
        <input type="text" id="title" placeholder="Enter assignment title">
        <label>Submission URL *</label>
        <input type="text" id="url" placeholder="https://github.com/yourusername/repo">
        <button onclick="submitAssignment()">Submit Assignment</button>
        <div id="message"></div>
    </div>

    <div class="submissions">
        <h2>📋 Submissions</h2>
        <table id="subTable">
            <tr><th>Name</th><th>Reg No</th><th>Title</th><th>URL</th></tr>
        </table>
    </div>

    <script>
        async function submitAssignment() {
            const data = {
                name: document.getElementById("name").value,
                reg_number: document.getElementById("reg").value,
                title: document.getElementById("title").value,
                url: document.getElementById("url").value
            };
            const res = await fetch("/submit", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });
            const result = await res.json();
            const msg = document.getElementById("message");
            msg.textContent = result.message;
            msg.className = result.success ? "success" : "error";
            if (result.success) loadSubmissions();
        }

        async function loadSubmissions() {
            const res = await fetch("/submissions");
            const data = await res.json();
            const table = document.getElementById("subTable");
            table.innerHTML = "<tr><th>Name</th><th>Reg No</th><th>Title</th><th>URL</th></tr>";
            data.forEach(s => {
                table.innerHTML += "<tr><td>" + s.name + "</td><td>" + s.reg_number + "</td><td>" + s.title + "</td><td><a href=" + s.url + " target=_blank>Link</a></td></tr>";
            });
        }
        loadSubmissions();
    </script>
</body>
</html>
'''

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()

    if not data.get("name") or not data["name"].strip():
        return jsonify({"success": False, "message": "Name is required"}), 400

    # DEFECT: registration number validation removed

    if not data.get("title") or not data["title"].strip():
        return jsonify({"success": False, "message": "Assignment title is required"}), 400

    if not data.get("url") or not data["url"].strip():
        return jsonify({"success": False, "message": "Submission URL is required"}), 400

    if not is_valid_url(data["url"]):
        return jsonify({"success": False, "message": "Invalid submission URL"}), 400

    submissions = load_submissions()
    submissions.append({
        "name": data["name"].strip(),
        "reg_number": data.get("reg_number", "").strip(),
        "title": data["title"].strip(),
        "url": data["url"].strip()
    })
    save_submissions(submissions)

    return jsonify({"success": True, "message": "Submission saved successfully!"})

@app.route("/submissions", methods=["GET"])
def get_submissions():
    return jsonify(load_submissions())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
