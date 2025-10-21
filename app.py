# requirements: flask, gspread, oauth2client
# pip install flask gspread oauth2client

from flask import Flask, request, render_template_string, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = Flask(__name__)

# --- Configure Google Sheets ---
# 1) Create a Google Service Account and download JSON key file.
# 2) Share your Google Sheet with the service account email (edit access).
SCOPE = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
CREDS_FILE = 'service-account.json'   # place your downloaded key here
SPREADSHEET_NAME = 'ClickLogs'       # create this sheet beforehand

gc = gspread.service_account(filename=CREDS_FILE)
sh = gc.open(SPREADSHEET_NAME)
ws = sh.sheet1

# --- Landing page with consent ---
CONSENT_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>PhinexIntra — Phishing Awareness</title>
  <style>
    :root{
      --bg:#180028; --card:#230040; --accent:#a855f7; --accent2:#c084fc; --muted:#b197d7; --glass:rgba(255,255,255,0.06);
      --max-w:900px;
      font-family: Inter, system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
    }
    body{margin:0;min-height:100vh;background:linear-gradient(180deg,#100020 0%, #1e0038 60%);color:#f3e8ff;display:flex;align-items:center;justify-content:center;padding:40px}
    .wrap{width:100%;max-width:var(--max-w);background:linear-gradient(180deg,rgba(255,255,255,0.02), var(--card));border-radius:14px;box-shadow:0 10px 30px rgba(20,0,40,0.7);padding:28px;}
    header{display:flex;gap:16px;align-items:center}
    .logo{width:56px;height:56px;border-radius:10px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-weight:700;color:#fff;font-size:18px;text-shadow:0 0 5px rgba(0,0,0,0.3)}
    h1{margin:0;font-size:28px;letter-spacing:-0.4px}
    .sub{color:var(--muted);margin-top:6px}
    .hero{display:flex;gap:28px;margin-top:20px;align-items:center}
    .left{flex:1}
    .right{width:320px;background:var(--glass);padding:18px;border-radius:10px;border:1px solid rgba(255,255,255,0.1)}
    .pill{display:inline-block;background:rgba(255,255,255,0.07);padding:6px 10px;border-radius:999px;color:var(--accent2);font-weight:600;margin-bottom:12px}
    p{color:#e9d5ff;line-height:1.5;margin:10px 0}
    .cta{display:flex;gap:10px;margin-top:14px}
    .btn{background:var(--accent);color:#fff;padding:12px 16px;border-radius:10px;border:0;font-weight:700;cursor:pointer;text-decoration:none;transition:0.3s}
    .btn:hover{background:var(--accent2)}
    .btn.secondary{background:transparent;border:1px solid rgba(255,255,255,0.2);color:var(--muted);font-weight:600}
    .btn.secondary:hover{border-color:var(--accent2);color:var(--accent2)}
    .note{font-size:13px;color:var(--muted);margin-top:12px}
    .small-list{margin:10px 0;padding-left:18px;color:var(--muted)}
    footer{margin-top:18px;font-size:13px;color:var(--muted);display:flex;justify-content:space-between;align-items:center}
    @media (max-width:760px){.hero{flex-direction:column}.right{width:100%}}
  </style>
</head>
<body>
  <main class="wrap" role="main">
    <header>
     
      <div>
        <h1>PhinexIntra — <span style="color:var(--accent2)">You have been phished</span></h1>
        <div class="sub">Awareness exercise • Phishing campaign result</div>
      </div>
    </header>

    <section class="hero" aria-labelledby="hero-title">
      <div class="left">
        <span class="pill">Security Awareness Program</span>
        <h2 id="hero-title" style="margin-top:8px">Don't worry — this is a simulated phishing test</h2>
        <p>
          Our awareness campaign detected that this account interacted with a simulated phishing message. This exercise is part of our continuous effort to build a strong security culture and help you recognize real phishing attempts.
        </p>

        <p>
          What happens next: you will be enrolled in a short learning path on our LMS, including a video walkthrough, gamified micro-lessons, and a final quiz to test your knowledge.
        </p>

        <ul class="small-list">
          <li>Watch a short <strong>training video</strong> on the LMS.</li>
          <li>Complete <strong>interactive gamified learning</strong> modules.</li>
          <li>Finish a <strong>quick test</strong> — your progress will be recorded.</li>
        </ul>

        <div class="cta">
          <a class="btn" href="#" id="start-btn">Go to LMS &amp; Start Learning</a>
          <a class="btn secondary" href="#" id="report-btn">Report a Real Phish</a>
        </div>

        <p class="note">Note: This is a safe simulation for awareness purposes. No actual compromise occurred. Completing your LMS module helps strengthen our collective defense.</p>
      </div>

      <aside class="right" aria-label="Summary">
        <strong>Result summary</strong>
        <p style="margin:8px 0 4px 0;color:#e9d5ff"><strong>Status:</strong> Phished (simulated)</p>
        <p style="margin:6px 0 0 0;color:var(--muted)"><strong>Action:</strong> Enrolled in LMS training & final test</p>
        <hr style="border:none;border-top:1px solid rgba(255,255,255,0.1);margin:12px 0">
        <p style="font-size:13px;color:var(--muted)"><strong>Help:</strong> Contact <a href="mailto:security@phinexintra.local" style="color:var(--accent2);text-decoration:none;">support@phinexintra.com</a></p>
      </aside>
    </section>

    <footer>
      <span>PhinexIntra • Security Awareness</span>
      <small>&copy; <span id="year"></span></small>
    </footer>
  </main>

  <script>
    document.getElementById('year').textContent = new Date().getFullYear();
    document.getElementById('start-btn').addEventListener('click', function(e){
      e.preventDefault();
      window.location.href = '/lms/enroll?campaign=phishing-awareness';
    });
    document.getElementById('report-btn').addEventListener('click', function(e){
      e.preventDefault();
      window.location.href = 'mailto:security@phinexintra.local?subject=Report%20Phishing%20Incident';
    });
  </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(CONSENT_HTML)

@app.route('/log', methods=['POST'])
def log():
    # get IP (Flask provides remote_addr) — beware of proxies; adjust if behind reverse proxy
    ip = request.remote_addr or ''
    ua = request.headers.get('User-Agent', '')
    ts = datetime.utcnow().isoformat()
    # Save to Google Sheet
    try:
        ws.append_row([ts, ip, ua])
    except Exception as e:
        print("Sheet append error:", e)
    # redirect or show a success page
    return "<h3>Thanks — your consent recorded. You may now continue.</h3>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
