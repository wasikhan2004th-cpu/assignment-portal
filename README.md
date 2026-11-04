# Assignment Submission Portal - DevOps Lab Mid (CSC418)

## Course Information
- **Course:** DevOps for Cloud Computing (CSC418)
- **Instructor:** Mr. Babar Shazad
- **Student:** Wasi Ahmed Khan
- **Repo:** https://github.com/wasikhan2004th-cpu/assignment-portal

## Run the Application
```bash
pip install flask pytest requests
python app.py
```
Open: http://localhost:5000

## Run Tests
```bash
pip install pytest pytest-json-report
pytest tests/ -v
```

## Start the Report Receiver
```bash
python receiver.py
```
Receiver runs on: http://localhost:5001/report

## Start ngrok Tunnel
```bash
ngrok http 5001
```
Then update RECEIVER_URL secret in GitHub with the ngrok URL.

## CI/CD Pipeline
GitHub Actions runs automatically on every push:
- Runs 3 automated tests
- Builds JSON report
- Sends report to local receiver via ngrok
- Sends email report
- Deploys to GitHub Pages (only on passing tests)

## GitHub Pages (Bonus)
Live URL: https://wasikhan2004th-cpu.github.io/assignment-portal

## Email Report (Bonus)
Test report automatically sent to email after every push.
