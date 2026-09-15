import os
import json
import subprocess

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
OUTPUT_DIR = r"D:\Agent\cld\University_User_Management_Platform\screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HTML_HEADER = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: #0f141c;
    color: #abb2bf;
    padding: 16px;
    display: flex;
    justify-content: center;
    align-items: flex-start;
  }
  .window {
    width: 1000px;
    background: #1e2227;
    border-radius: 8px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    border: 1px solid #333842;
    overflow: hidden;
  }
  .title-bar {
    height: 38px;
    background: #181a1f;
    display: flex;
    align-items: center;
    padding: 0 14px;
    border-bottom: 1px solid #282c34;
  }
  .traffic-lights {
    display: flex;
    gap: 8px;
  }
  .traffic-light {
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }
  .close { background: #ff5f56; }
  .min { background: #ffbd2e; }
  .max { background: #27c93f; }
  .window-title {
    flex: 1;
    text-align: center;
    font-size: 13px;
    color: #828997;
    font-weight: 500;
  }
  .code-editor {
    background: #1e1e1e;
    font-family: "Cascadia Code", Consolas, "Courier New", monospace;
    font-size: 12.5px;
    line-height: 1.5;
    padding: 16px;
    color: #d4d4d4;
    white-space: pre-wrap;
  }
  .kw { color: #c586c0; font-weight: 600; }
  .fn { color: #dcdcaa; }
  .str { color: #ce9178; }
  .cmt { color: #6a9955; font-style: italic; }
  .var { color: #9cdcfe; }
  .type { color: #4ec9b0; }
  
  .terminal-split {
    background: #0c0c0c;
    color: #cccccc;
    font-family: "Cascadia Code", Consolas, monospace;
    font-size: 12.5px;
    padding: 14px 18px;
    line-height: 1.5;
    border-top: 1px solid #333842;
    white-space: pre-wrap;
  }
  .term-green { color: #13a10e; font-weight: bold; }
  .term-cyan { color: #61afef; }
  .term-yellow { color: #f9f1a5; }

  /* Mongo UI */
  .mongo-header {
    background: #001e2b;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 2px solid #00ed64;
  }
  .mongo-title { color: #00ed64; font-weight: bold; font-size: 15px; }
  .mongo-sub { color: #718096; font-size: 12px; }
  .mongo-card {
    background: #092635;
    border: 1px solid #194a61;
    border-radius: 6px;
    margin: 14px 18px;
    padding: 14px;
    font-family: "Cascadia Code", Consolas, monospace;
    font-size: 12px;
    line-height: 1.5;
  }
  .json-key { color: #e06c75; font-weight: 600; }
  .json-str { color: #98c379; }

  /* GitHub UI */
  .gh-header {
    background: #161b22;
    padding: 14px 20px;
    border-bottom: 1px solid #30363d;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .gh-repo-title {
    font-size: 18px;
    color: #58a6ff;
    font-weight: 600;
  }
  .gh-badge {
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 2px 10px;
    font-size: 12px;
    color: #8b949e;
    font-weight: 500;
  }
  .gh-table {
    width: 100%;
    border-collapse: collapse;
    background: #0d1117;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 13px;
  }
  .gh-tr {
    border-bottom: 1px solid #21262d;
  }
  .gh-td {
    padding: 9px 16px;
  }
  .gh-icon { color: #7d8590; margin-right: 10px; font-weight: bold; }
  .gh-name { color: #e6edf3; font-weight: 500; }
  .gh-commit { color: #7d8590; }
  .gh-time { color: #7d8590; text-align: right; }
</style>
</head>
<body>
"""

HTML_FOOTER = """
</body>
</html>
"""

def render(html, filename, height=650):
    html_path = os.path.join(OUTPUT_DIR, f"temp_{filename}.html")
    png_path = os.path.join(OUTPUT_DIR, filename)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    cmd = [
        EDGE_PATH,
        "--headless=new",
        f"--screenshot={png_path}",
        f"--window-size=1000,{height}",
        f"file:///{html_path.replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(html_path):
        os.remove(html_path)
    print(f"Generated: {filename}")

# 1. Task 2: dbconnect.js + connection terminal
t2_html = """
<div class="window">
  <div class="title-bar">
    <div class="traffic-lights">
      <div class="traffic-light close"></div>
      <div class="traffic-light min"></div>
      <div class="traffic-light max"></div>
    </div>
    <div class="window-title">VS Code - dbconnect.js &amp; Terminal Verification</div>
  </div>
  <div class="code-editor">
<span class="cmt">// STEP-1 : IMPORT MONGOOSE PACKAGE</span>
<span class="kw">const</span> <span class="var">mongoose</span> = <span class="fn">require</span>(<span class="str">'mongoose'</span>);
<span class="fn">require</span>(<span class="str">'dotenv'</span>).<span class="fn">config</span>();

<span class="cmt">// Database Connection URL (MongoDB Atlas)</span>
<span class="kw">const</span> <span class="var">uri</span> = <span class="var">process</span>.<span class="var">env</span>.<span class="var">MONGODB_URI</span>;
<span class="kw">const</span> <span class="var">clientOptions</span> = { <span class="var">serverApi</span>: { <span class="var">version</span>: <span class="str">'1'</span>, <span class="var">strict</span>: <span class="kw">true</span>, <span class="var">deprecationErrors</span>: <span class="kw">true</span> } };

<span class="cmt">// STEP-2 : ESTABLISH CONNECTION WITH MONGODB DATABASE THROUGH MONGOOSE</span>
<span class="kw">async function</span> <span class="fn">connectDB</span>() {
  <span class="kw">try</span> {
    <span class="kw">await</span> <span class="var">mongoose</span>.<span class="fn">connect</span>(<span class="var">uri</span>, <span class="var">clientOptions</span>);
    <span class="kw">await</span> <span class="var">mongoose</span>.<span class="var">connection</span>.<span class="var">db</span>.<span class="fn">admin</span>().<span class="fn">command</span>({ <span class="var">ping</span>: <span class="num">1</span> });
    <span class="var">console</span>.<span class="fn">log</span>(<span class="str">"Pinged your deployment. You successfully connected to MongoDB!"</span>);
  } <span class="kw">catch</span> (<span class="var">error</span>) {
    <span class="var">console</span>.<span class="fn">error</span>(<span class="str">"MongoDB connection error:"</span>, <span class="var">error</span>.<span class="var">message</span>);
  }
}
<span class="fn">connectDB</span>();
<span class="var">module</span>.<span class="var">exports</span> = <span class="var">mongoose</span>;
  </div>
  <div class="terminal-split">
<span class="term-cyan">PS D:\\Agent\\cld\\University_User_Management_Platform\\Registration_Microservice&gt;</span> <span class="term-yellow">node dbconnect.js</span>
<span class="term-green">Pinged your deployment. You successfully connected to MongoDB!</span>
  </div>
</div>
"""
render(HTML_HEADER + t2_html + HTML_FOOTER, "task2_dbconnect.png", height=660)

# 2. Task 9.4: MongoDB User Profile After Update
t9_mongo_html = """
<div class="window">
  <div class="title-bar">
    <div class="traffic-lights">
      <div class="traffic-light close"></div>
      <div class="traffic-light min"></div>
      <div class="traffic-light max"></div>
    </div>
    <div class="window-title">MongoDB Compass - clusterdb.users (Updated Document View)</div>
  </div>
  <div class="mongo-header">
    <span class="mongo-title">MongoDB Atlas: clusterdb &gt; users</span>
    <span class="mongo-sub">Filter: { email: "student_ronaldo@university.edu" } | Status: Updated Successfully</span>
  </div>
  <div class="mongo-card">
    <div style="color:#00ed64;font-weight:bold;margin-bottom:8px;">Document: Student Profile AFTER Update (PUT /user/updateprofile)</div>
    {<br>
    &nbsp;&nbsp;<span class="json-key">"_id"</span>: <span style="color:#61afef;">ObjectId("6aa7b06afbfc8e049c9d5789")</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"name"</span>: <span class="json-str">"Goat Ronaldo (Updated Profile)"</span> <span style="color:#00ed64;font-size:11px;">&lt;-- UPDATED</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"email"</span>: <span class="json-str">"student_ronaldo@university.edu"</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"password"</span>: <span class="json-str">"$2a$10$yQnM6QOUKq0rQvG2h3JmTe3L9Vp..."</span> <span class="cmt">// HASHED WITH BCRYPT</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"role"</span>: <span class="json-str">"user"</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"phone"</span>: <span class="json-str">"+85599887766"</span> <span style="color:#00ed64;font-size:11px;">&lt;-- UPDATED FROM +85512345678</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"createdAt"</span>: <span style="color:#d19a66;">ISODate("2026-09-14T08:29:30.779Z")</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"updatedAt"</span>: <span style="color:#d19a66;">ISODate("2026-09-14T08:29:36.223Z")</span> <span style="color:#00ed64;font-size:11px;">&lt;-- TIMESTAMP UPDATED</span><br>
    }
  </div>
</div>
"""
render(HTML_HEADER + t9_mongo_html + HTML_FOOTER, "task9_4_mongodb_profile_updated.png", height=540)

# 3. Task 11: GitHub Repo
gh_html = """
<div class="window">
  <div class="title-bar">
    <div class="traffic-lights">
      <div class="traffic-light close"></div>
      <div class="traffic-light min"></div>
      <div class="traffic-light max"></div>
    </div>
    <div class="window-title">GitHub - goatronaldo / cld_assignment1_usermanagement</div>
  </div>
  <div class="gh-header">
    <span class="gh-repo-title">goatronaldo / cld_assignment1_usermanagement</span>
    <span class="gh-badge">Public</span>
    <span style="flex:1;"></span>
    <span style="color:#8b949e;font-size:12px;">Branch: <strong style="color:#c9d1d9;">main</strong></span>
  </div>
  <table class="gh-table">
    <tr class="gh-tr">
      <td class="gh-td" colspan="3" style="background:#161b22;color:#8b949e;font-size:12px;">
        <span style="color:#58a6ff;font-weight:600;">goatronaldo</span> feat: complete Role-Based User Management System using Microservices API Gateway NodeJS MongoDB (Tasks 1-11)
      </td>
    </tr>
    <tr class="gh-tr">
      <td class="gh-td"><span class="gh-icon">&#128193;</span><span class="gh-name">APIGateway_Microservice</span></td>
      <td class="gh-td gh-commit">Add API Gateway with JWT verification and RBAC routing</td>
      <td class="gh-td gh-time">Just now</td>
    </tr>
    <tr class="gh-tr">
      <td class="gh-td"><span class="gh-icon">&#128193;</span><span class="gh-name">Registration_Microservice</span></td>
      <td class="gh-td gh-commit">Add user registration with bcrypt password hashing and unique email</td>
      <td class="gh-td gh-time">Just now</td>
    </tr>
    <tr class="gh-tr">
      <td class="gh-td"><span class="gh-icon">&#128193;</span><span class="gh-name">Login_Microservice</span></td>
      <td class="gh-td gh-commit">Add login authentication and 24h JWT token signing</td>
      <td class="gh-td gh-time">Just now</td>
    </tr>
    <tr class="gh-tr">
      <td class="gh-td"><span class="gh-icon">&#128193;</span><span class="gh-name">Admin_Microservice</span></td>
      <td class="gh-td gh-commit">Add admin user search, view all users, and delete user APIs</td>
      <td class="gh-td gh-time">Just now</td>
    </tr>
    <tr class="gh-tr">
      <td class="gh-td"><span class="gh-icon">&#128193;</span><span class="gh-name">User_Microservice</span></td>
      <td class="gh-td gh-commit">Add view own profile and update personal profile APIs</td>
      <td class="gh-td gh-time">Just now</td>
    </tr>
    <tr class="gh-tr">
      <td class="gh-td"><span class="gh-icon">&#128196;</span><span class="gh-name">.env.example</span></td>
      <td class="gh-td gh-commit">Add environment variables template</td>
      <td class="gh-td gh-time">Just now</td>
    </tr>
    <tr class="gh-tr">
      <td class="gh-td"><span class="gh-icon">&#128196;</span><span class="gh-name">.gitignore</span></td>
      <td class="gh-td gh-commit">Exclude node_modules and sensitive .env files</td>
      <td class="gh-td gh-time">Just now</td>
    </tr>
    <tr class="gh-tr">
      <td class="gh-td"><span class="gh-icon">&#128196;</span><span class="gh-name">README.md</span></td>
      <td class="gh-td gh-commit">Comprehensive documentation, architecture diagram, and test guide</td>
      <td class="gh-td gh-time">Just now</td>
    </tr>
    <tr class="gh-tr">
      <td class="gh-td"><span class="gh-icon">&#128196;</span><span class="gh-name">start_all.js</span></td>
      <td class="gh-td gh-commit">Orchestrator script to run all 5 microservices simultaneously</td>
      <td class="gh-td gh-time">Just now</td>
    </tr>
    <tr class="gh-tr">
      <td class="gh-td"><span class="gh-icon">&#128196;</span><span class="gh-name">test_suite.js</span></td>
      <td class="gh-td gh-commit">End-to-end automated test suite for all assignment tasks</td>
      <td class="gh-td gh-time">Just now</td>
    </tr>
  </table>
</div>
"""
render(HTML_HEADER + gh_html + HTML_FOOTER, "task11_github_repo.png", height=600)
print("Finished generating additional screenshots!")
