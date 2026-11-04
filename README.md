\# Assignment Submission Portal — DevOps Lab Mid (CSC418)



\## Run the Application

```bash

pip install flask pytest requests

python app.py

```

Open: http://localhost:5000



\## Run Tests

```bash

pip install pytest pytest-json-report

pytest tests/ -v

```



\## Start the Report Receiver

```bash

python receiver.py

```

Receiver runs on: http://localhost:5001/report



\## CI/CD Pipeline

GitHub Actions runs on every push. Set `RECEIVER\_URL` in GitHub Secrets to your ngrok tunnel URL.



\## GitHub Pages (Bonus)

Deployed automatically to GitHub Pages after passing tests on `main` branch.

