# Webhook Receiver Project

## Overview
This project receives GitHub webhook events (push, pull request, merge) from an action-repo, stores them in MongoDB, and displays them in a minimal UI that updates every 15 seconds.

## Setup

### 1. Clone the Repo
```bash
git clone https://github.com/Imdachu/webhook-repo
cd <-webhook-repo-folder>
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start MongoDB
Make sure MongoDB is running locally.

### 4. Run the Flask App
```bash
python run.py
```

### 5. Expose Locally with ngrok
```bash
ngrok http 5000
```
Copy the HTTPS URL.

### 6. Configure GitHub Webhook
- Go to your action-repo on GitHub.
- Settings > Webhooks > Add webhook.
- Payload URL: `https://<your-ngrok-id>.ngrok.io/webhook/receiver`
- Content type: `application/json`
- Events: Push, Pull requests

## Usage

- Visit `http://127.0.0.1:5000/` to see the UI.
- Trigger events in your action-repo (push, PR, merge).
- The UI will update automatically.

## Author
Darshan Rai