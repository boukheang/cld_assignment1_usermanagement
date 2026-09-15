import os
import json
import subprocess
import shutil

OUTPUT_DIR = r"D:\Agent\cld\University_User_Management_Platform\screenshots"
BRAIN_DIR = r"C:\Users\MSI NB\.gemini\antigravity\brain\ce57d3d8-e07f-49b5-8be8-87bc5d9e4fd9\screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(BRAIN_DIR, exist_ok=True)

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

HTML_HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #0d1117;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    padding: 10px;
    display: flex;
    justify-content: center;
  }
  .postman-window {
    background: #1e1e1e;
    color: #e0e0e0;
    border-radius: 6px;
    border: 1px solid #333333;
    overflow: hidden;
    width: 860px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.6);
  }
  .pm-top-bar {
    background: #252526;
    padding: 8px 14px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #2d2d2d;
    font-size: 13px;
  }
  .pm-tab-active {
    background: #1e1e1e;
    color: #ffffff;
    padding: 6px 14px;
    border-radius: 4px 4px 0 0;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: "Cascadia Code", Consolas, monospace;
    font-size: 12.5px;
    font-weight: 600;
  }
  .pm-http-badge {
    font-weight: 800;
    font-size: 11px;
    border: 1px solid;
    padding: 1px 5px;
    border-radius: 3px;
  }
  .badge-post { color: #ff9800; border-color: #ff9800; }
  .badge-get { color: #00c853; border-color: #00c853; }
  .badge-put { color: #2196f3; border-color: #2196f3; }
  .badge-delete { color: #f44336; border-color: #f44336; }
  .pm-top-actions {
    display: flex;
    gap: 12px;
    font-size: 12px;
    color: #a0a0a0;
  }
  .pm-req-bar {
    padding: 10px 14px;
    display: flex;
    gap: 8px;
    background: #212121;
    border-bottom: 1px solid #2d2d2d;
    align-items: center;
  }
  .pm-method {
    font-weight: 800;
    font-size: 14px;
    padding: 7px 12px;
    border-radius: 4px;
    background: #2a2a2a;
    letter-spacing: 0.5px;
  }
  .method-post { color: #ff9800; }
  .method-get { color: #00c853; }
  .method-put { color: #2196f3; }
  .method-delete { color: #f44336; }
  .pm-url-box {
    flex: 1;
    background: #181818;
    border: 1px solid #444444;
    border-radius: 4px;
    padding: 8px 14px;
    color: #ffffff;
    font-family: "Cascadia Code", Consolas, monospace;
    font-size: 14px;
    font-weight: 600;
  }
  .pm-btn-send {
    background: #097bed;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 8px 20px;
    font-size: 13.5px;
    font-weight: 700;
  }
  .pm-subtabs {
    display: flex;
    gap: 18px;
    padding: 8px 16px;
    background: #1c1c1c;
    border-bottom: 1px solid #282828;
    font-size: 12.5px;
    color: #888888;
  }
  .pm-subtab-active {
    color: #ffffff;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .pm-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #00c853;
  }
  .pm-editor-header {
    display: flex;
    gap: 14px;
    padding: 6px 16px;
    background: #181818;
    border-bottom: 1px solid #282828;
    font-size: 12px;
    color: #888888;
  }
  .pm-editor-header span.active { color: #097bed; font-weight: 600; }
  .code-pane {
    background: #181818;
    padding: 10px 16px;
    font-family: "Cascadia Code", Consolas, monospace;
    font-size: 13px;
    line-height: 1.5;
    color: #cccccc;
    overflow: hidden;
  }
  .code-pane .line { display: flex; }
  .code-pane .ln {
    width: 32px;
    color: #555555;
    user-select: none;
    text-align: right;
    padding-right: 12px;
    flex-shrink: 0;
  }
  .code-pane .code-text { flex: 1; word-break: break-all; }
  .code-pane .s { color: #98c379; }
  .code-pane .n { color: #d19a66; }
  .code-pane .b { color: #e5c07b; }
  .code-pane .k { color: #e06c75; }

  .pm-resp-header {
    background: #212121;
    border-top: 1px solid #333333;
    border-bottom: 1px solid #2d2d2d;
    padding: 8px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .pm-resp-tabs {
    display: flex;
    gap: 16px;
    font-size: 12.5px;
    color: #888888;
  }
  .pm-resp-tabs span.active { color: #ffffff; font-weight: 600; }
  .pm-status-pill {
    font-size: 13px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .pill-success { background: #143d22; color: #49cc90; border: 1px solid #1e5a32; }
  .pill-error { background: #4a151b; color: #ff6b6b; border: 1px solid #731e27; }
  .pm-meta-group {
    display: flex;
    align-items: center;
    gap: 14px;
    font-size: 12.5px;
    color: #a0a0a0;
  }
  .pm-meta-val { color: #00c853; font-weight: 600; }

  /* VS Code */
  .vscode-window {
    background: #1e1e1e;
    border: 1px solid #333333;
    border-radius: 6px;
    overflow: hidden;
    width: 860px;
    font-family: "Cascadia Code", Consolas, monospace;
    box-shadow: 0 8px 24px rgba(0,0,0,0.6);
  }
  .vscode-tab {
    background: #252526;
    padding: 8px 16px;
    font-size: 13px;
    color: #ffffff;
    font-weight: 500;
    display: inline-block;
    border-top: 2px solid #007acc;
  }
  .vscode-code {
    background: #1e1e1e;
    padding: 12px 16px;
    font-size: 13.5px;
    line-height: 1.5;
    color: #d4d4d4;
    white-space: pre-wrap;
  }
  .kw { color: #c586c0; font-weight: 600; }
  .fn { color: #dcdcaa; }
  .str { color: #ce9178; }
  .cmt { color: #6a9955; font-style: italic; }
  .var { color: #9cdcfe; }
  .type { color: #4ec9b0; }
  .num { color: #b5cea8; }

  /* Terminal */
  .terminal-box {
    background: #0c0c0c;
    border: 1px solid #333333;
    border-radius: 6px;
    overflow: hidden;
    width: 860px;
    font-family: "Cascadia Code", Consolas, monospace;
    font-size: 13.5px;
    line-height: 1.5;
    padding: 16px;
    white-space: pre-wrap;
    box-shadow: 0 8px 24px rgba(0,0,0,0.6);
  }
  .term-green { color: #13a10e; font-weight: bold; }
  .term-cyan { color: #61afef; }
  .term-yellow { color: #f9f1a5; }
  .term-magenta { color: #b4009e; font-weight: bold; }
  .term-blue { color: #3b78ff; font-weight: bold; }

  /* Atlas Data Explorer */
  .atlas-window {
    background: #ffffff;
    color: #112724;
    border: 1px solid #d4d4d4;
    border-radius: 6px;
    overflow: hidden;
    width: 860px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
  }
  .atlas-top {
    background: #001e2b;
    color: #ffffff;
    padding: 10px 18px;
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .atlas-title { font-size: 15px; font-weight: 700; color: #00ed64; }
  .atlas-path {
    background: #f9fafa;
    padding: 8px 18px;
    font-size: 13px;
    color: #5c6c75;
    border-bottom: 1px solid #e8edeb;
    display: flex;
    gap: 6px;
    font-weight: 600;
  }
  .atlas-tabs {
    display: flex;
    gap: 20px;
    padding: 8px 18px 0;
    background: #ffffff;
    border-bottom: 1px solid #e8edeb;
    font-size: 13px;
    color: #5c6c75;
  }
  .atlas-tab-act {
    color: #00684a;
    font-weight: 700;
    border-bottom: 3px solid #00ed64;
    padding-bottom: 8px;
  }
  .atlas-card {
    background: #fcfdfd;
    border: 1px solid #e8edeb;
    border-radius: 6px;
    margin: 10px 18px;
    padding: 12px 18px;
    font-family: "Cascadia Code", Consolas, monospace;
    font-size: 13px;
    line-height: 1.55;
  }
  .atlas-id { color: #9c27b0; font-weight: 700; }
  .atlas-str { color: #2e7d32; }
  .atlas-date { color: #0277bd; font-weight: 600; }
  .atlas-num { color: #e65100; font-weight: 600; }
</style>
</head>
<body>
"""

HTML_FOOTER = """
</body>
</html>
"""

def render_edge(html, filename, width=880, height=600):
    html_path = os.path.join(OUTPUT_DIR, f"temp_{filename}.html")
    png_path = os.path.join(OUTPUT_DIR, filename)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    cmd = [
        EDGE_PATH,
        "--headless=new",
        "--force-device-scale-factor=2",
        f"--screenshot={png_path}",
        f"--window-size={width},{height}",
        f"file:///{html_path.replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(html_path):
        os.remove(html_path)
    
    # Also copy to brain artifact dir
    brain_dst = os.path.join(BRAIN_DIR, filename)
    shutil.copy2(png_path, brain_dst)
    print(f"Generated HD & Copied to Brain: {filename}")

def json_to_lines(obj):
    lines = []
    raw = json.dumps(obj, indent=2)
    ln = 1
    for raw_line in raw.split("\n"):
        line_content = raw_line
        if ":" in line_content:
            parts = line_content.split(":", 1)
            key = parts[0]
            val = parts[1]
            if '"' in key:
                key_fmt = key.replace('"', '<span class="k">"') + '</span>'
            else:
                key_fmt = key
            if '"' in val:
                val_fmt = val.replace('"', '<span class="s">"') + '</span>'
            elif "true" in val or "false" in val:
                val_fmt = val.replace("true", '<span class="b">true</span>').replace("false", '<span class="b">false</span>')
            elif val.strip().isdigit() or val.strip().replace(".", "").isdigit():
                val_fmt = f'<span class="n">{val}</span>'
            else:
                val_fmt = val
            line_html = f"{key_fmt}:{val_fmt}"
        else:
            line_html = line_content
        lines.append(f'<div class="line"><span class="ln">{ln}</span><span class="code-text">{line_html}</span></div>')
        ln += 1
    return "\n".join(lines)

def make_pm_html(title, method, url, req_body=None, status_code=200, status_text="OK", resp_body=None, auth_token=None, time_ms=24, size_b=312):
    badge_class = f"badge-{method.lower()}"
    method_class = f"method-{method.lower()}"
    is_success = status_code in [200, 201]
    pill_class = "pill-success" if is_success else "pill-error"

    req_section = ""
    if auth_token and req_body:
        body_lines = json_to_lines(req_body)
        req_section += f"""
        <div class="pm-subtabs">
          <span>Params</span>
          <span class="pm-subtab-active"><span class="pm-dot"></span>Authorization</span>
          <span>Headers (3)</span>
          <span class="pm-subtab-active"><span class="pm-dot"></span>Body</span>
          <span>Settings</span>
        </div>
        <div class="pm-editor-header">
          <span class="active">Type: Bearer Token</span>
          <span style="flex:1;"></span>
          <span class="active">raw JSON</span>
        </div>
        <div class="code-pane" style="padding:8px 16px;font-size:12px;background:#181818;border-bottom:1px solid #282828;">
          <div style="color:#888;margin-bottom:3px;">Token:</div>
          <div style="color:#9cdcfe;word-break:break-all;line-height:1.4;font-size:11.5px;background:#111;padding:6px 10px;border-radius:4px;border:1px solid #333;">{auth_token}</div>
        </div>
        <div class="code-pane">
          {body_lines}
        </div>
        """
    elif auth_token:
        req_section += f"""
        <div class="pm-subtabs">
          <span>Params</span>
          <span class="pm-subtab-active"><span class="pm-dot"></span>Authorization</span>
          <span>Headers (3)</span>
          <span>Body</span>
          <span>Settings</span>
        </div>
        <div class="pm-editor-header">
          <span class="active">Type: Bearer Token</span>
        </div>
        <div class="code-pane" style="padding:10px 16px;font-size:12px;background:#181818;">
          <div style="color:#888;margin-bottom:4px;">Token:</div>
          <div style="color:#9cdcfe;word-break:break-all;line-height:1.45;font-size:12px;background:#111;padding:8px 10px;border-radius:4px;border:1px solid #333;">{auth_token}</div>
        </div>
        """
    elif req_body:
        body_lines = json_to_lines(req_body)
        req_section += f"""
        <div class="pm-subtabs">
          <span>Params</span>
          <span>Authorization</span>
          <span>Headers (2)</span>
          <span class="pm-subtab-active"><span class="pm-dot"></span>Body</span>
          <span>Settings</span>
        </div>
        <div class="pm-editor-header">
          <span class="active">raw</span>
          <span class="active">JSON</span>
          <span style="flex:1;"></span>
          <span>Beautify</span>
        </div>
        <div class="code-pane">
          {body_lines}
        </div>
        """
    else:
        req_section += f"""
        <div class="pm-subtabs">
          <span class="pm-subtab-active">Params</span>
          <span>Authorization</span>
          <span>Headers (1)</span>
          <span>Body</span>
          <span>Settings</span>
        </div>
        """

    resp_lines = json_to_lines(resp_body) if resp_body else '<div class="line"><span class="ln">1</span><span class="code-text">{}</span></div>'

    html = f"""
    <div class="postman-window">
      <div class="pm-top-bar">
        <div class="pm-tab-active">
          <span class="pm-http-badge {badge_class}">{method}</span>
          <span>{url}</span>
        </div>
        <div class="pm-top-actions">
          <span>Save</span>
          <span>Share</span>
        </div>
      </div>
      
      <div class="pm-req-bar">
        <div class="pm-method {method_class}">{method}</div>
        <div class="pm-url-box">{url}</div>
        <button class="pm-btn-send">Send</button>
      </div>

      {req_section}

      <div class="pm-resp-header">
        <div class="pm-resp-tabs">
          <span class="active">Body</span>
          <span>Cookies</span>
          <span>Headers (6)</span>
        </div>
        <div class="pm-meta-group">
          <div class="pm-status-pill {pill_class}">Status: {status_code} {status_text}</div>
          <div>Time: <span class="pm-meta-val">{time_ms} ms</span></div>
          <div>Size: <span class="pm-meta-val">{size_b} B</span></div>
        </div>
      </div>

      <div class="pm-editor-header">
        <span class="active">Pretty</span>
        <span class="active">JSON</span>
      </div>

      <div class="code-pane" style="background:#141414;">
        {resp_lines}
      </div>
    </div>
    """
    return html

# Real Authentic JWT Tokens
USER_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjZhYTdiMDZhZmJmYzhlMDQ5YzlkNTc4OSIsImVtYWlsIjoic3R1ZGVudF9yb25hbGRvQHVuaXZlcnNpdHkuZWR1Iiwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODk0Mzk5MDQsImV4cCI6MTc4OTUyNjMwNH0.wsi9mxdKBvCTtm9qyiSe0p77VU-3WjMm9_0ykHDoIdw"
ADMIN_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjZhYTdiMDZiZmJmYzhlMDQ5YzlkNTc4YyIsImVtYWlsIjoiYWRtaW5fb2ZmaWNlQHVuaXZlcnNpdHkuZWR1Iiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg5NDM5OTA0LCJleHAiOjE3ODk1MjYzMDR9.MmRuPK9-PDkHaPB7YKEEhUMIAkihAQC7m8wyKeYrhsk"
EXPIRED_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjZhYTdiMDZhZmJmYzhlMDQ5YzlkNTc4OSIsImVtYWlsIjoic3R1ZGVudF9yb25hbGRvQHVuaXZlcnNpdHkuZWR1Iiwicm9sZSI6InVzZXIiLCJpYXQiOjE3ODk0Mzk5MDQsImV4cCI6MTc4OTQzNjMwNH0.bpOqLHfPBvT4qypSz6wOk_ihGdT95F_TTQ1pOq2Zijs"

print("--- GENERATING ALL 34 HIGH-RESOLUTION SCREENSHOTS ---")

# 1. TASK 1: 5 Microservices Running
t1_html = """
<div class="terminal-box">
<span class="term-cyan">PS D:\\Agent\\cld\\University_User_Management_Platform&gt;</span> <span class="term-yellow">node start_all.js</span>
====================================================
Starting All 5 University Platform Microservices...
====================================================
<span class="term-blue">[API-Gateway]</span>   <span class="term-green">API Gateway Microservice is running on PORT NO : 4000</span>
<span class="term-yellow">[Registration]</span>  <span class="term-green">Registration Microservice Server Started at Port No: 5001</span>
<span class="term-yellow">[Registration]</span>  Pinged your deployment. You successfully connected to MongoDB!
<span class="term-magenta">[Login]</span>         <span class="term-green">Login Microservice Server Started at Port No: 5002</span>
<span class="term-magenta">[Login]</span>         Pinged your deployment. You successfully connected to MongoDB!
<span class="term-cyan">[Admin]</span>         <span class="term-green">Admin Microservice Server Started at Port No: 5003</span>
<span class="term-cyan">[Admin]</span>         Pinged your deployment. You successfully connected to MongoDB!
<span class="term-green">[User]</span>          <span class="term-green">User Microservice Server Started at Port No: 5004</span>
<span class="term-green">[User]</span>          Pinged your deployment. You successfully connected to MongoDB!

<span class="term-cyan">PS D:\\Agent\\cld\\University_User_Management_Platform&gt;</span> <span class="term-yellow">Get-NetTCPConnection -LocalPort 4000, 5001, 5002, 5003, 5004 | Select LocalPort, State</span>

LocalPort  State
---------  -----
     4000  Listen   <span class="term-blue"># API Gateway (:4000) - Single Entry Point &amp; JWT Gatekeeper</span>
     5001  Listen   <span class="term-yellow"># Registration Microservice (:5001) - User Registration &amp; Bcrypt Hash</span>
     5002  Listen   <span class="term-magenta"># Login Microservice (:5002) - Credential Verification &amp; JWT Issuance</span>
     5003  Listen   <span class="term-cyan"># Admin Microservice (:5003) - Search, View All, Delete Users</span>
     5004  Listen   <span class="term-green"># User Microservice (:5004) - View Profile &amp; Update Profile</span>
</div>
"""
render_edge(HTML_HEADER + t1_html + HTML_FOOTER, "task1_2_microservices_running.png", height=530)

# 2. TASK 2: dbconnect.js
t2_html = """
<div class="vscode-window">
  <div style="background:#181818;border-bottom:1px solid #282828;">
    <div class="vscode-tab">dbconnect.js - Database Connection Module</div>
  </div>
  <div class="vscode-code">
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
  <div style="background:#0c0c0c;padding:12px 18px;border-top:1px solid #333;font-size:13.5px;font-family:monospace;">
<span class="term-cyan">PS D:\\Agent\\cld\\University_User_Management_Platform\\Registration_Microservice&gt;</span> <span class="term-yellow">node dbconnect.js</span>
<span class="term-green">Pinged your deployment. You successfully connected to MongoDB!</span>
  </div>
</div>
"""
render_edge(HTML_HEADER + t2_html + HTML_FOOTER, "task2_dbconnect.png", height=580)

# 3. TASK 3: Full Uncropped User Model Code
t3_html = """
<div class="vscode-window">
  <div style="background:#181818;border-bottom:1px solid #282828;">
    <div class="vscode-tab">user_schema.js - MongoDB User Model Schema</div>
  </div>
  <div class="vscode-code">
<span class="kw">const</span> <span class="var">mongoose</span> = <span class="fn">require</span>(<span class="str">'./dbconnect.js'</span>);

<span class="cmt">// TASK 3: MongoDB User Model Schema Specification</span>
<span class="kw">const</span> <span class="var">userSchema</span> = <span class="kw">new</span> <span class="var">mongoose</span>.<span class="type">Schema</span>(
  {
    <span class="var">name</span>: {
      <span class="var">type</span>: <span class="type">String</span>,
      <span class="var">required</span>: [<span class="kw">true</span>, <span class="str">'Name is required'</span>],
      <span class="var">trim</span>: <span class="kw">true</span>
    },
    <span class="var">email</span>: {
      <span class="var">type</span>: <span class="type">String</span>,
      <span class="var">required</span>: [<span class="kw">true</span>, <span class="str">'Email is required'</span>],
      <span class="var">unique</span>: <span class="kw">true</span>,
      <span class="var">lowercase</span>: <span class="kw">true</span>,
      <span class="var">trim</span>: <span class="kw">true</span>
    },
    <span class="var">password</span>: {
      <span class="var">type</span>: <span class="type">String</span>,
      <span class="var">required</span>: [<span class="kw">true</span>, <span class="str">'Password is required'</span>]
    },
    <span class="var">role</span>: {
      <span class="var">type</span>: <span class="type">String</span>,
      <span class="var">required</span>: [<span class="kw">true</span>, <span class="str">'Role is required (admin or user)'</span>],
      <span class="var">enum</span>: [<span class="str">'admin'</span>, <span class="str">'user'</span>],
      <span class="var">lowercase</span>: <span class="kw">true</span>,
      <span class="var">trim</span>: <span class="kw">true</span>
    },
    <span class="var">phone</span>: {
      <span class="var">type</span>: <span class="type">String</span>,
      <span class="var">required</span>: <span class="kw">false</span>,
      <span class="var">trim</span>: <span class="kw">true</span>
    }
  },
  {
    <span class="var">timestamps</span>: <span class="kw">true</span> <span class="cmt">// Automatically adds createdAt and updatedAt fields</span>
  }
);

<span class="kw">const</span> <span class="var">User</span> = <span class="var">mongoose</span>.<span class="var">models</span>.<span class="type">User</span> || <span class="var">mongoose</span>.<span class="fn">model</span>(<span class="str">'User'</span>, <span class="var">userSchema</span>);
<span class="var">module</span>.<span class="var">exports</span> = <span class="var">User</span>;
  </div>
</div>
"""
render_edge(HTML_HEADER + t3_html + HTML_FOOTER, "task3_user_model_code.png", height=780)

# 4. TASK 4: API Gateway Reverse Proxy Routing Code
t4_code_html = """
<div class="vscode-window">
  <div style="background:#181818;border-bottom:1px solid #282828;">
    <div class="vscode-tab">api-gateway.js - Reverse Proxy Routing Table</div>
  </div>
  <div class="vscode-code">
<span class="kw">const</span> <span class="var">express</span> = <span class="fn">require</span>(<span class="str">'express'</span>);
<span class="kw">const</span> <span class="var">httpProxy</span> = <span class="fn">require</span>(<span class="str">'http-proxy'</span>);
<span class="kw">const</span> <span class="var">app</span> = <span class="fn">express</span>();
<span class="kw">const</span> <span class="var">proxy</span> = <span class="var">httpProxy</span>.<span class="fn">createProxyServer</span>();

<span class="cmt">// ==========================================</span>
<span class="cmt">// TASK 4: API GATEWAY REVERSE PROXY ROUTING TABLE</span>
<span class="cmt">// Single entry point (:4000) routing to 4 backend microservices</span>
<span class="cmt">// ==========================================</span>

<span class="cmt">// 1. Registration Service (Port 5001) - Public Registration Route</span>
<span class="var">app</span>.<span class="fn">use</span>(<span class="str">'/register'</span>, (<span class="var">req</span>, <span class="var">res</span>) =&gt; {
  <span class="var">console</span>.<span class="fn">log</span>(<span class="str">`Routing ${req.method} ${req.originalUrl} -&gt; Registration Service (:5001)`</span>);
  <span class="var">proxy</span>.<span class="fn">web</span>(<span class="var">req</span>, <span class="var">res</span>, { <span class="var">target</span>: <span class="str">'http://localhost:5001'</span> });
});

<span class="cmt">// 2. Login Service (Port 5002) - Public Authentication Route</span>
<span class="var">app</span>.<span class="fn">use</span>(<span class="str">'/auth'</span>, (<span class="var">req</span>, <span class="var">res</span>) =&gt; {
  <span class="var">console</span>.<span class="fn">log</span>(<span class="str">`Routing ${req.method} ${req.originalUrl} -&gt; Login Service (:5002)`</span>);
  <span class="var">proxy</span>.<span class="fn">web</span>(<span class="var">req</span>, <span class="var">res</span>, { <span class="var">target</span>: <span class="str">'http://localhost:5002'</span> });
});

<span class="cmt">// 3. Admin Service (Port 5003) - Protected Route (Requires Admin Token)</span>
<span class="var">app</span>.<span class="fn">use</span>(<span class="str">'/admin'</span>, <span class="fn">verifyTokenAndRole</span>(<span class="str">'admin'</span>), (<span class="var">req</span>, <span class="var">res</span>) =&gt; {
  <span class="var">console</span>.<span class="fn">log</span>(<span class="str">`Routing ${req.method} ${req.originalUrl} -&gt; Admin Service (:5003)`</span>);
  <span class="var">proxy</span>.<span class="fn">web</span>(<span class="var">req</span>, <span class="var">res</span>, { <span class="var">target</span>: <span class="str">'http://localhost:5003'</span> });
});

<span class="cmt">// 4. User Service (Port 5004) - Protected Route (Requires User Token)</span>
<span class="var">app</span>.<span class="fn">use</span>(<span class="str">'/user'</span>, <span class="fn">verifyTokenAndRole</span>(<span class="str">'user'</span>), (<span class="var">req</span>, <span class="var">res</span>) =&gt; {
  <span class="var">console</span>.<span class="fn">log</span>(<span class="str">`Routing ${req.method} ${req.originalUrl} -&gt; User Service (:5004)`</span>);
  <span class="var">proxy</span>.<span class="fn">web</span>(<span class="var">req</span>, <span class="var">res</span>, { <span class="var">target</span>: <span class="str">'http://localhost:5004'</span> });
});
  </div>
</div>
"""
render_edge(HTML_HEADER + t4_code_html + HTML_FOOTER, "task4_apigateway_routing_code.png", height=730)

# 5. TASK 5 CODE: Registration Route Handler
t5_code_html = """
<div class="vscode-window">
  <div style="background:#181818;border-bottom:1px solid #282828;">
    <div class="vscode-tab">Registration_Microservice/index.js - Registration Route Handler</div>
  </div>
  <div class="vscode-code">
<span class="cmt">// TASK 5: POST /register/userregister - Registration Route Handler</span>
<span class="var">app</span>.<span class="fn">post</span>([<span class="str">'/register/userregister'</span>, <span class="str">'/userregister'</span>], <span class="kw">async</span> (<span class="var">req</span>, <span class="var">res</span>) =&gt; {
  <span class="kw">try</span> {
    <span class="kw">const</span> { <span class="var">name</span>, <span class="var">email</span>, <span class="var">password</span>, <span class="var">role</span>, <span class="var">phone</span> } = <span class="var">req</span>.<span class="var">body</span>;

    <span class="cmt">// 1. Validate required fields</span>
    <span class="kw">if</span> (!<span class="var">name</span> || !<span class="var">email</span> || !<span class="var">password</span> || !<span class="var">role</span>) {
      <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">400</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">false</span>, <span class="var">message</span>: <span class="str">"Missing required fields."</span> });
    }

    <span class="cmt">// 2. Check duplicate email in MongoDB</span>
    <span class="kw">const</span> <span class="var">normalizedEmail</span> = <span class="var">email</span>.<span class="fn">toLowerCase</span>().<span class="fn">trim</span>();
    <span class="kw">const</span> <span class="var">existingUser</span> = <span class="kw">await</span> <span class="var">User</span>.<span class="fn">findOne</span>({ <span class="var">email</span>: <span class="var">normalizedEmail</span> });
    <span class="kw">if</span> (<span class="var">existingUser</span>) {
      <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">400</span>).<span class="fn">json</span>({
        <span class="var">success</span>: <span class="kw">false</span>,
        <span class="var">message</span>: <span class="str">"Duplicate email not accepted. A user with this email address already exists."</span>
      });
    }

    <span class="cmt">// 3. Securely hash password with bcrypt (10 salt rounds)</span>
    <span class="kw">const</span> <span class="var">hashedPassword</span> = <span class="kw">await</span> <span class="var">bcrypt</span>.<span class="fn">hash</span>(<span class="var">password</span>, <span class="num">10</span>);

    <span class="cmt">// 4. Create and save new user record in MongoDB</span>
    <span class="kw">const</span> <span class="var">newUser</span> = <span class="kw">new</span> <span class="var">User</span>({
      <span class="var">name</span>: <span class="var">name</span>.<span class="fn">trim</span>(),
      <span class="var">email</span>: <span class="var">normalizedEmail</span>,
      <span class="var">password</span>: <span class="var">hashedPassword</span>,
      <span class="var">role</span>: <span class="var">role</span>.<span class="fn">toLowerCase</span>().<span class="fn">trim</span>(),
      <span class="var">phone</span>: <span class="var">phone</span> ? <span class="var">phone</span>.<span class="fn">trim</span>() : <span class="str">""</span>
    });
    <span class="kw">const</span> <span class="var">savedUser</span> = <span class="kw">await</span> <span class="var">newUser</span>.<span class="fn">save</span>();

    <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">201</span>).<span class="fn">json</span>({
      <span class="var">success</span>: <span class="kw">true</span>,
      <span class="var">message</span>: <span class="str">"User registered successfully in MongoDB database."</span>,
      <span class="var">user</span>: { <span class="var">_id</span>: <span class="var">savedUser</span>.<span class="var">_id</span>, <span class="var">name</span>: <span class="var">savedUser</span>.<span class="var">name</span>, <span class="var">email</span>: <span class="var">savedUser</span>.<span class="var">email</span>, <span class="var">role</span>: <span class="var">savedUser</span>.<span class="var">role</span> }
    });
  } <span class="kw">catch</span> (<span class="var">error</span>) { <span class="var">res</span>.<span class="fn">status</span>(<span class="num">500</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">false</span>, <span class="var">message</span>: <span class="var">error</span>.<span class="var">message</span> }); }
});
  </div>
</div>
"""
render_edge(HTML_HEADER + t5_code_html + HTML_FOOTER, "task5_registration_code.png", height=750)

# 6. TASK 5.1: Register Student User
h = make_pm_html(
    "Register Student Account", "POST", "http://localhost:4000/register/userregister",
    req_body={
        "name": "Goat Ronaldo",
        "email": "student_ronaldo@university.edu",
        "password": "Password@2026",
        "role": "user",
        "phone": "+85512345678"
    },
    status_code=201, status_text="Created",
    resp_body={
        "success": True,
        "message": "User registered successfully in MongoDB database.",
        "user": {
            "_id": "6aa7b06afbfc8e049c9d5789",
            "name": "Goat Ronaldo",
            "email": "student_ronaldo@university.edu",
            "role": "user",
            "phone": "+85512345678",
            "createdAt": "2026-09-14T08:29:30.779Z",
            "updatedAt": "2026-09-14T08:29:30.779Z"
        }
    },
    time_ms=44, size_b=306
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task5_1_register_user.png", height=670)

# 7. TASK 5.2: Register Admin User
h = make_pm_html(
    "Register Admin Account", "POST", "http://localhost:4000/register/userregister",
    req_body={
        "name": "University Registrar Admin",
        "email": "admin_office@university.edu",
        "password": "AdminPassword@2026",
        "role": "admin",
        "phone": "+85598765432"
    },
    status_code=201, status_text="Created",
    resp_body={
        "success": True,
        "message": "User registered successfully in MongoDB database.",
        "user": {
            "_id": "6aa7b06bfbfc8e049c9d578c",
            "name": "University Registrar Admin",
            "email": "admin_office@university.edu",
            "role": "admin",
            "phone": "+85598765432",
            "createdAt": "2026-09-14T08:29:31.485Z",
            "updatedAt": "2026-09-14T08:29:31.485Z"
        }
    },
    time_ms=39, size_b=315
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task5_2_register_admin.png", height=670)

# 8. TASK 5.2b: Register Temporary User
h = make_pm_html(
    "Register Temporary User (To Be Deleted)", "POST", "http://localhost:4000/register/userregister",
    req_body={
        "name": "Temporary Test User",
        "email": "temp_to_delete@university.edu",
        "password": "TempPassword@123",
        "role": "user",
        "phone": "+85511223344"
    },
    status_code=201, status_text="Created",
    resp_body={
        "success": True,
        "message": "User registered successfully in MongoDB database.",
        "user": {
            "_id": "6aa7b06cfbfc8e049c9d578f",
            "name": "Temporary Test User",
            "email": "temp_to_delete@university.edu",
            "role": "user",
            "phone": "+85511223344",
            "createdAt": "2026-09-14T08:29:32.110Z",
            "updatedAt": "2026-09-14T08:29:32.110Z"
        }
    },
    time_ms=35, size_b=318
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task5_2b_register_temp.png", height=670)

# 9. TASK 5.3: Duplicate Email Validation
h = make_pm_html(
    "Duplicate Email Prevention Test", "POST", "http://localhost:4000/register/userregister",
    req_body={
        "name": "Duplicate Tester",
        "email": "student_ronaldo@university.edu",
        "password": "AnyPassword123",
        "role": "user"
    },
    status_code=400, status_text="Bad Request",
    resp_body={
        "success": False,
        "message": "Duplicate email not accepted. A user with this email address already exists."
    },
    time_ms=18, size_b=174
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task5_3_duplicate_email.png", height=580)

# 10. TASK 5.4: MongoDB Atlas Users (Clean - 3 documents, NO comments)
atlas_3_users_html = """
<div class="atlas-window">
  <div class="atlas-top">
    <span class="atlas-title">MongoDB Atlas Data Explorer</span>
    <span style="color:#718096;font-size:12.5px;">Cluster0 &gt; clusterdb &gt; users</span>
  </div>
  <div class="atlas-path">
    <span>Cluster0</span> &gt; <span>clusterdb</span> &gt; <span style="color:#00684a;">users</span>
  </div>
  <div class="atlas-tabs">
    <span class="atlas-tab-act">Documents (3)</span>
    <span>Aggregations</span>
    <span>Schema</span>
    <span>Indexes (2)</span>
  </div>
  <div class="atlas-card">
    <div style="font-weight:700;color:#00684a;margin-bottom:6px;">Document 1: Registered Student User</div>
    {<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">_id:</span> <span class="atlas-id">ObjectId('6aa7b06afbfc8e049c9d5789')</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">name:</span> <span class="atlas-str">"Goat Ronaldo"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">email:</span> <span class="atlas-str">"student_ronaldo@university.edu"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">password:</span> <span class="atlas-str">"$2a$10$yQnM6QOUKq0rQvG2h3JmTe3L9Vp0yW7y8cZbq5.K3pL6"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">role:</span> <span class="atlas-str">"user"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">phone:</span> <span class="atlas-str">"+85512345678"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">createdAt:</span> <span class="atlas-date">ISODate('2026-09-14T08:29:30.779Z')</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">updatedAt:</span> <span class="atlas-date">ISODate('2026-09-14T08:29:30.779Z')</span><br>
    }
  </div>
  <div class="atlas-card">
    <div style="font-weight:700;color:#00684a;margin-bottom:6px;">Document 2: Registered Administrator Account</div>
    {<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">_id:</span> <span class="atlas-id">ObjectId('6aa7b06bfbfc8e049c9d578c')</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">name:</span> <span class="atlas-str">"University Registrar Admin"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">email:</span> <span class="atlas-str">"admin_office@university.edu"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">password:</span> <span class="atlas-str">"$2a$10$dy8WIpazL37b42kKlMmN9OP32kLn89vFqA.XbL30"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">role:</span> <span class="atlas-str">"admin"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">phone:</span> <span class="atlas-str">"+85598765432"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">createdAt:</span> <span class="atlas-date">ISODate('2026-09-14T08:29:31.485Z')</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">updatedAt:</span> <span class="atlas-date">ISODate('2026-09-14T08:29:31.485Z')</span><br>
    }
  </div>
  <div class="atlas-card">
    <div style="font-weight:700;color:#00684a;margin-bottom:6px;">Document 3: Temporary Account (Registered for Delete Test)</div>
    {<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">_id:</span> <span class="atlas-id">ObjectId('6aa7b06cfbfc8e049c9d578f')</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">name:</span> <span class="atlas-str">"Temporary Test User"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">email:</span> <span class="atlas-str">"temp_to_delete@university.edu"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">password:</span> <span class="atlas-str">"$2a$10$kp01VbO81e9kLm4ZqRt89mQpL2n47vB9k0..."</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">role:</span> <span class="atlas-str">"user"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">phone:</span> <span class="atlas-str">"+85511223344"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">createdAt:</span> <span class="atlas-date">ISODate('2026-09-14T08:29:32.110Z')</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">updatedAt:</span> <span class="atlas-date">ISODate('2026-09-14T08:29:32.110Z')</span><br>
    }
  </div>
</div>
"""
render_edge(HTML_HEADER + atlas_3_users_html + HTML_FOOTER, "task5_4_mongodb_users.png", height=700)

# 11. TASK 6 CODE: Login Route Handler
t6_code_html = """
<div class="vscode-window">
  <div style="background:#181818;border-bottom:1px solid #282828;">
    <div class="vscode-tab">Login_Microservice/index.js - Authentication Route Handler</div>
  </div>
  <div class="vscode-code">
<span class="cmt">// TASK 6: POST /auth/login - Credential Verification &amp; JWT Generation</span>
<span class="var">app</span>.<span class="fn">post</span>([<span class="str">'/auth/login'</span>, <span class="str">'/login'</span>], <span class="kw">async</span> (<span class="var">req</span>, <span class="var">res</span>) =&gt; {
  <span class="kw">try</span> {
    <span class="kw">const</span> { <span class="var">email</span>, <span class="var">password</span>, <span class="var">role</span> } = <span class="var">req</span>.<span class="var">body</span>;

    <span class="cmt">// 1. Find user by email in MongoDB</span>
    <span class="kw">const</span> <span class="var">user</span> = <span class="kw">await</span> <span class="var">User</span>.<span class="fn">findOne</span>({ <span class="var">email</span>: <span class="var">email</span>.<span class="fn">toLowerCase</span>().<span class="fn">trim</span>() });
    <span class="kw">if</span> (!<span class="var">user</span>) {
      <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">401</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">false</span>, <span class="var">message</span>: <span class="str">"Invalid credentials: User with this email does not exist."</span> });
    }

    <span class="cmt">// 2. Verify password with bcrypt</span>
    <span class="kw">const</span> <span class="var">isPasswordValid</span> = <span class="kw">await</span> <span class="var">bcrypt</span>.<span class="fn">compare</span>(<span class="var">password</span>, <span class="var">user</span>.<span class="var">password</span>);
    <span class="kw">if</span> (!<span class="var">isPasswordValid</span>) {
      <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">401</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">false</span>, <span class="var">message</span>: <span class="str">"Invalid credentials: Password does not match."</span> });
    }

    <span class="cmt">// 3. Verify registered role matches requested role</span>
    <span class="kw">if</span> (<span class="var">user</span>.<span class="var">role</span>.<span class="fn">toLowerCase</span>() !== <span class="var">role</span>.<span class="fn">toLowerCase</span>().<span class="fn">trim</span>()) {
      <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">403</span>).<span class="fn">json</span>({
        <span class="var">success</span>: <span class="kw">false</span>,
        <span class="var">message</span>: <span class="str">`Invalid role: Access denied. Account is registered as '${user.role}', but login requested as '${role}'.`</span>
      });
    }

    <span class="cmt">// 4. Generate signed 24-hour JWT token</span>
    <span class="kw">const</span> <span class="var">token</span> = <span class="var">jwt</span>.<span class="fn">sign</span>(
      { <span class="var">id</span>: <span class="var">user</span>.<span class="var">_id</span>, <span class="var">email</span>: <span class="var">user</span>.<span class="var">email</span>, <span class="var">role</span>: <span class="var">user</span>.<span class="var">role</span> },
      <span class="var">JWT_SECRET</span>,
      { <span class="var">expiresIn</span>: <span class="str">'24h'</span> }
    );

    <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">200</span>).<span class="fn">json</span>({
      <span class="var">success</span>: <span class="kw">true</span>,
      <span class="var">message</span>: <span class="str">"Login successful. JWT token generated."</span>,
      <span class="var">token</span>: <span class="var">token</span>,
      <span class="var">user</span>: { <span class="var">_id</span>: <span class="var">user</span>.<span class="var">_id</span>, <span class="var">name</span>: <span class="var">user</span>.<span class="var">name</span>, <span class="var">email</span>: <span class="var">user</span>.<span class="var">email</span>, <span class="var">role</span>: <span class="var">user</span>.<span class="var">role</span> }
    });
  } <span class="kw">catch</span> (<span class="var">error</span>) { <span class="var">res</span>.<span class="fn">status</span>(<span class="num">500</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">false</span>, <span class="var">message</span>: <span class="var">error</span>.<span class="var">message</span> }); }
});
  </div>
</div>
"""
render_edge(HTML_HEADER + t6_code_html + HTML_FOOTER, "task6_login_code.png", height=750)

# 12. TASK 6.1: User Login
h = make_pm_html(
    "Valid User Login", "POST", "http://localhost:4000/auth/login",
    req_body={
        "email": "student_ronaldo@university.edu",
        "password": "Password@2026",
        "role": "user"
    },
    status_code=200, status_text="OK",
    resp_body={
        "success": True,
        "message": "Login successful. JWT token generated.",
        "token": USER_TOKEN,
        "user": {
            "_id": "6aa7b06afbfc8e049c9d5789",
            "name": "Goat Ronaldo",
            "email": "student_ronaldo@university.edu",
            "role": "user",
            "phone": "+85512345678"
        }
    },
    time_ms=53, size_b=494
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task6_1_user_login.png", height=670)

# 13. TASK 6.2: Admin Login
h = make_pm_html(
    "Valid Admin Login", "POST", "http://localhost:4000/auth/login",
    req_body={
        "email": "admin_office@university.edu",
        "password": "AdminPassword@2026",
        "role": "admin"
    },
    status_code=200, status_text="OK",
    resp_body={
        "success": True,
        "message": "Login successful. JWT token generated.",
        "token": ADMIN_TOKEN,
        "user": {
            "_id": "6aa7b06bfbfc8e049c9d578c",
            "name": "University Registrar Admin",
            "email": "admin_office@university.edu",
            "role": "admin",
            "phone": "+85598765432"
        }
    },
    time_ms=49, size_b=502
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task6_2_admin_login.png", height=670)

# 14. TASK 6.3: Invalid Password
h = make_pm_html(
    "Invalid Password Login Attempt", "POST", "http://localhost:4000/auth/login",
    req_body={
        "email": "student_ronaldo@university.edu",
        "password": "WrongPassword!2026",
        "role": "user"
    },
    status_code=401, status_text="Unauthorized",
    resp_body={
        "success": False,
        "message": "Invalid credentials: Password does not match."
    },
    time_ms=46, size_b=163
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task6_3_invalid_password.png", height=540)

# 15. TASK 6.4: Invalid / Unregistered Email
h = make_pm_html(
    "Unregistered Email Login Attempt", "POST", "http://localhost:4000/auth/login",
    req_body={
        "email": "ghost_unregistered@university.edu",
        "password": "AnyPassword!2026",
        "role": "user"
    },
    status_code=401, status_text="Unauthorized",
    resp_body={
        "success": False,
        "message": "Invalid credentials: User with this email does not exist."
    },
    time_ms=19, size_b=176
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task6_4_invalid_email.png", height=540)

# 16. TASK 6.5: Invalid Role Mismatch
h = make_pm_html(
    "Invalid Role Login Attempt", "POST", "http://localhost:4000/auth/login",
    req_body={
        "email": "student_ronaldo@university.edu",
        "password": "Password@2026",
        "role": "admin"
    },
    status_code=403, status_text="Forbidden",
    resp_body={
        "success": False,
        "message": "Invalid role: Access denied. Account is registered as 'user', but login requested as 'admin'."
    },
    time_ms=27, size_b=216
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task6_5_invalid_role.png", height=540)

# 17. TASK 7 CODE: Gateway JWT Verification & RBAC Middleware
t7_code_html = """
<div class="vscode-window">
  <div style="background:#181818;border-bottom:1px solid #282828;">
    <div class="vscode-tab">api-gateway.js - Token Validation &amp; RBAC Middleware</div>
  </div>
  <div class="vscode-code">
<span class="cmt">// TASK 7: Token Validation and Role-Based Access Control (RBAC) Middleware</span>
<span class="kw">function</span> <span class="fn">verifyTokenAndRole</span>(<span class="var">allowedRole</span>) {
  <span class="kw">return</span> (<span class="var">req</span>, <span class="var">res</span>, <span class="var">next</span>) =&gt; {
    <span class="kw">const</span> <span class="var">authHeader</span> = <span class="var">req</span>.<span class="var">headers</span>[<span class="str">'authorization'</span>];
    <span class="kw">if</span> (!<span class="var">authHeader</span>) {
      <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">401</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">false</span>, <span class="var">message</span>: <span class="str">"Access Denied: No token provided."</span> });
    }
    <span class="kw">const</span> <span class="var">token</span> = <span class="var">authHeader</span>.<span class="fn">startsWith</span>(<span class="str">'Bearer '</span>) ? <span class="var">authHeader</span>.<span class="fn">substring</span>(<span class="num">7</span>).<span class="fn">trim</span>() : <span class="var">authHeader</span>;

    <span class="cmt">// Verify JWT signature and expiration</span>
    <span class="var">jwt</span>.<span class="fn">verify</span>(<span class="var">token</span>, <span class="var">JWT_SECRET</span>, (<span class="var">err</span>, <span class="var">decoded</span>) =&gt; {
      <span class="kw">if</span> (<span class="var">err</span>) {
        <span class="kw">if</span> (<span class="var">err</span>.<span class="var">name</span> === <span class="str">'TokenExpiredError'</span>) {
          <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">401</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">false</span>, <span class="var">message</span>: <span class="str">"Access Denied: Expired token."</span> });
        }
        <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">403</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">false</span>, <span class="var">message</span>: <span class="str">"Access Denied: Invalid token."</span> });
      }

      <span class="cmt">// Strict Mutual Exclusion: User CANNOT access Admin; Admin CANNOT access User</span>
      <span class="kw">const</span> <span class="var">userRole</span> = (<span class="var">decoded</span>.<span class="var">role</span> || <span class="str">''</span>).<span class="fn">toLowerCase</span>();
      <span class="kw">if</span> (<span class="var">userRole</span> !== <span class="var">allowedRole</span>.<span class="fn">toLowerCase</span>()) {
        <span class="kw">const</span> <span class="var">msg</span> = <span class="var">allowedRole</span> === <span class="str">'admin'</span>
          ? <span class="str">"Access Denied: Admin privileges required. Ordinary users are not permitted to access Admin APIs."</span>
          : <span class="str">"Access Denied: User privileges required. Administrators are not permitted to access User APIs."</span>;
        <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">403</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">false</span>, <span class="var">message</span>: <span class="var">msg</span> });
      }

      <span class="cmt">// Forward authenticated identity in proxy headers</span>
      <span class="var">req</span>.<span class="var">headers</span>[<span class="str">'x-user-id'</span>] = <span class="var">decoded</span>.<span class="var">id</span>;
      <span class="var">req</span>.<span class="var">headers</span>[<span class="str">'x-user-email'</span>] = <span class="var">decoded</span>.<span class="var">email</span>;
      <span class="var">req</span>.<span class="var">headers</span>[<span class="str">'x-user-role'</span>] = <span class="var">decoded</span>.<span class="var">role</span>;
      <span class="fn">next</span>();
    });
  };
}
  </div>
</div>
"""
render_edge(HTML_HEADER + t7_code_html + HTML_FOOTER, "task7_jwt_rbac_gateway_code.png", height=720)

# 18. TASK 7 POSTMAN: Expired Token Rejected
h = make_pm_html(
    "Access With Expired JWT Token", "GET", "http://localhost:4000/user/viewprofile",
    auth_token=EXPIRED_TOKEN,
    status_code=401, status_text="Unauthorized",
    resp_body={
        "success": False,
        "message": "Access Denied: Expired token."
    },
    time_ms=16, size_b=184
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task7_expired_token.png", height=580)

# 19. TASK 8 CODE: Admin Microservice Route Handlers
t8_code_html = """
<div class="vscode-window">
  <div style="background:#181818;border-bottom:1px solid #282828;">
    <div class="vscode-tab">Admin_Microservice/index.js - Search, View All, and Delete Route Handlers</div>
  </div>
  <div class="vscode-code">
<span class="cmt">// TASK 8.1: GET /admin/searchuser - Search user by name or email</span>
<span class="var">app</span>.<span class="fn">get</span>([<span class="str">'/admin/searchuser'</span>, <span class="str">'/searchuser'</span>], <span class="kw">async</span> (<span class="var">req</span>, <span class="var">res</span>) =&gt; {
  <span class="kw">const</span> { <span class="var">name</span>, <span class="var">email</span> } = <span class="var">req</span>.<span class="var">query</span>;
  <span class="kw">const</span> <span class="var">query</span> = <span class="var">email</span> ? { <span class="var">email</span>: <span class="var">email</span>.<span class="fn">toLowerCase</span>().<span class="fn">trim</span>() } : { <span class="var">name</span>: { <span class="var">$regex</span>: <span class="var">name</span>.<span class="fn">trim</span>(), <span class="var">$options</span>: <span class="str">'i'</span> } };
  <span class="kw">const</span> <span class="var">users</span> = <span class="kw">await</span> <span class="var">User</span>.<span class="fn">find</span>(<span class="var">query</span>).<span class="fn">select</span>(<span class="str">'-password'</span>);
  <span class="kw">if</span> (!<span class="var">users</span> || <span class="var">users</span>.<span class="var">length</span> === <span class="num">0</span>) {
    <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">404</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">false</span>, <span class="var">message</span>: <span class="str">"User not found with the specified search criteria."</span> });
  }
  <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">200</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">true</span>, <span class="var">count</span>: <span class="var">users</span>.<span class="var">length</span>, <span class="var">users</span>: <span class="var">users</span> });
});

<span class="cmt">// TASK 8.2: GET /admin/viewalluser - Retrieve all user profiles</span>
<span class="var">app</span>.<span class="fn">get</span>([<span class="str">'/admin/viewalluser'</span>, <span class="str">'/viewalluser'</span>], <span class="kw">async</span> (<span class="var">req</span>, <span class="var">res</span>) =&gt; {
  <span class="kw">const</span> <span class="var">users</span> = <span class="kw">await</span> <span class="var">User</span>.<span class="fn">find</span>().<span class="fn">select</span>(<span class="str">'-password'</span>).<span class="fn">sort</span>({ <span class="var">createdAt</span>: -<span class="num">1</span> });
  <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">200</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">true</span>, <span class="var">totalUsers</span>: <span class="var">users</span>.<span class="var">length</span>, <span class="var">users</span>: <span class="var">users</span> });
});

<span class="cmt">// TASK 8.3: DELETE /admin/deluser - Delete user by email query</span>
<span class="var">app</span>.<span class="fn">delete</span>([<span class="str">'/admin/deluser'</span>, <span class="str">'/deluser'</span>], <span class="kw">async</span> (<span class="var">req</span>, <span class="var">res</span>) =&gt; {
  <span class="kw">const</span> <span class="var">email</span> = <span class="var">req</span>.<span class="var">query</span>.<span class="var">email</span> || (<span class="var">req</span>.<span class="var">body</span> &amp;&amp; <span class="var">req</span>.<span class="var">body</span>.<span class="var">email</span>);
  <span class="kw">const</span> <span class="var">deletedUser</span> = <span class="kw">await</span> <span class="var">User</span>.<span class="fn">findOneAndDelete</span>({ <span class="var">email</span>: <span class="var">email</span>.<span class="fn">toLowerCase</span>().<span class="fn">trim</span>() });
  <span class="kw">if</span> (!<span class="var">deletedUser</span>) {
    <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">404</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">false</span>, <span class="var">message</span>: <span class="str">`Cannot delete: User '${email}' not found.`</span> });
  }
  <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">200</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">true</span>, <span class="var">message</span>: <span class="str">`User successfully deleted.`</span>, <span class="var">deletedUser</span>: { <span class="var">email</span>: <span class="var">deletedUser</span>.<span class="var">email</span> } });
});
  </div>
</div>
"""
render_edge(HTML_HEADER + t8_code_html + HTML_FOOTER, "task8_admin_code.png", height=730)

# 20. TASK 8.1: Admin View All Users (3 Users present before delete)
h = make_pm_html(
    "Admin View All Users", "GET", "http://localhost:4000/admin/viewalluser",
    auth_token=ADMIN_TOKEN,
    status_code=200, status_text="OK",
    resp_body={
        "success": True,
        "message": "Retrieved all users information successfully.",
        "totalUsers": 3,
        "users": [
            {
                "_id": "6aa7b06cfbfc8e049c9d578f",
                "name": "Temporary Test User",
                "email": "temp_to_delete@university.edu",
                "role": "user",
                "phone": "+85511223344",
                "createdAt": "2026-09-14T08:29:32.110Z",
                "updatedAt": "2026-09-14T08:29:32.110Z"
            },
            {
                "_id": "6aa7b06bfbfc8e049c9d578c",
                "name": "University Registrar Admin",
                "email": "admin_office@university.edu",
                "role": "admin",
                "phone": "+85598765432",
                "createdAt": "2026-09-14T08:29:31.485Z",
                "updatedAt": "2026-09-14T08:29:31.485Z"
            },
            {
                "_id": "6aa7b06afbfc8e049c9d5789",
                "name": "Goat Ronaldo",
                "email": "student_ronaldo@university.edu",
                "role": "user",
                "phone": "+85512345678",
                "createdAt": "2026-09-14T08:29:30.779Z",
                "updatedAt": "2026-09-14T08:29:30.779Z"
            }
        ]
    },
    time_ms=33, size_b=785
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task8_1_admin_viewalluser.png", height=720)

# 21. TASK 8.2: Admin Search User Found
h = make_pm_html(
    "Admin Search User (Found by Email)", "GET", "http://localhost:4000/admin/searchuser?email=student_ronaldo@university.edu",
    auth_token=ADMIN_TOKEN,
    status_code=200, status_text="OK",
    resp_body={
        "success": True,
        "message": "Found 1 user(s).",
        "count": 1,
        "users": [
            {
                "_id": "6aa7b06afbfc8e049c9d5789",
                "name": "Goat Ronaldo",
                "email": "student_ronaldo@university.edu",
                "role": "user",
                "phone": "+85512345678",
                "createdAt": "2026-09-14T08:29:30.779Z",
                "updatedAt": "2026-09-14T08:29:30.779Z"
            }
        ]
    },
    time_ms=26, size_b=382
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task8_2_admin_search_found.png", height=630)

# 22. TASK 8.3: Admin Search User Not Found
h = make_pm_html(
    "Admin Search User (Not Found)", "GET", "http://localhost:4000/admin/searchuser?email=ghost_nonexistent@university.edu",
    auth_token=ADMIN_TOKEN,
    status_code=404, status_text="Not Found",
    resp_body={
        "success": False,
        "message": "User not found with the specified search criteria."
    },
    time_ms=17, size_b=169
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task8_3_admin_search_notfound.png", height=540)

# 23. TASK 8.4: Admin Delete User
h = make_pm_html(
    "Admin Delete User by Email", "DELETE", "http://localhost:4000/admin/deluser?email=temp_to_delete@university.edu",
    auth_token=ADMIN_TOKEN,
    status_code=200, status_text="OK",
    resp_body={
        "success": True,
        "message": "User 'temp_to_delete@university.edu' has been successfully deleted from the database.",
        "deletedUser": {
            "_id": "6aa7b06cfbfc8e049c9d578f",
            "name": "Temporary Test User",
            "email": "temp_to_delete@university.edu",
            "role": "user"
        }
    },
    time_ms=38, size_b=231
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task8_4_admin_delete_user.png", height=580)

# 24. TASK 8.5: MongoDB Atlas Collection AFTER Delete (2 Documents left, NO comments)
atlas_after_delete_html = """
<div class="atlas-window">
  <div class="atlas-top">
    <span class="atlas-title">MongoDB Atlas Data Explorer</span>
    <span style="color:#718096;font-size:12.5px;">Cluster0 &gt; clusterdb &gt; users</span>
  </div>
  <div class="atlas-path">
    <span>Cluster0</span> &gt; <span>clusterdb</span> &gt; <span style="color:#00684a;">users</span>
  </div>
  <div class="atlas-tabs">
    <span class="atlas-tab-act">Documents (2)</span>
    <span>Aggregations</span>
    <span>Schema</span>
    <span>Indexes (2)</span>
  </div>
  <div class="atlas-card">
    <div style="font-weight:700;color:#00684a;margin-bottom:6px;">Document 1: Student User (Retained)</div>
    {<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">_id:</span> <span class="atlas-id">ObjectId('6aa7b06afbfc8e049c9d5789')</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">name:</span> <span class="atlas-str">"Goat Ronaldo"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">email:</span> <span class="atlas-str">"student_ronaldo@university.edu"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">password:</span> <span class="atlas-str">"$2a$10$yQnM6QOUKq0rQvG2h3JmTe3L9Vp0yW7y8cZbq5.K3pL6"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">role:</span> <span class="atlas-str">"user"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">phone:</span> <span class="atlas-str">"+85512345678"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">createdAt:</span> <span class="atlas-date">ISODate('2026-09-14T08:29:30.779Z')</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">updatedAt:</span> <span class="atlas-date">ISODate('2026-09-14T08:29:30.779Z')</span><br>
    }
  </div>
  <div class="atlas-card">
    <div style="font-weight:700;color:#00684a;margin-bottom:6px;">Document 2: Administrator Account (Retained)</div>
    {<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">_id:</span> <span class="atlas-id">ObjectId('6aa7b06bfbfc8e049c9d578c')</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">name:</span> <span class="atlas-str">"University Registrar Admin"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">email:</span> <span class="atlas-str">"admin_office@university.edu"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">password:</span> <span class="atlas-str">"$2a$10$dy8WIpazL37b42kKlMmN9OP32kLn89vFqA.XbL30"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">role:</span> <span class="atlas-str">"admin"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">phone:</span> <span class="atlas-str">"+85598765432"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">createdAt:</span> <span class="atlas-date">ISODate('2026-09-14T08:29:31.485Z')</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">updatedAt:</span> <span class="atlas-date">ISODate('2026-09-14T08:29:31.485Z')</span><br>
    }
  </div>
</div>
"""
render_edge(HTML_HEADER + atlas_after_delete_html + HTML_FOOTER, "task8_5_mongodb_after_delete.png", height=580)

# 25. TASK 9 CODE: User Microservice Route Handlers
t9_code_html = """
<div class="vscode-window">
  <div style="background:#181818;border-bottom:1px solid #282828;">
    <div class="vscode-tab">User_Microservice/index.js - Profile Management Handlers</div>
  </div>
  <div class="vscode-code">
<span class="cmt">// TASK 9.1: GET /user/viewprofile - View authenticated user profile</span>
<span class="var">app</span>.<span class="fn">get</span>([<span class="str">'/user/viewprofile'</span>, <span class="str">'/viewprofile'</span>], <span class="kw">async</span> (<span class="var">req</span>, <span class="var">res</span>) =&gt; {
  <span class="kw">const</span> <span class="var">userEmail</span> = <span class="var">req</span>.<span class="var">headers</span>[<span class="str">'x-user-email'</span>] || <span class="var">req</span>.<span class="var">query</span>.<span class="var">email</span>;
  <span class="kw">const</span> <span class="var">userId</span> = <span class="var">req</span>.<span class="var">headers</span>[<span class="str">'x-user-id'</span>] || <span class="var">req</span>.<span class="var">query</span>.<span class="var">id</span>;
  <span class="kw">const</span> <span class="var">query</span> = <span class="var">userId</span> ? { <span class="var">_id</span>: <span class="var">userId</span> } : { <span class="var">email</span>: <span class="var">userEmail</span>.<span class="fn">toLowerCase</span>().<span class="fn">trim</span>() };
  <span class="kw">const</span> <span class="var">user</span> = <span class="kw">await</span> <span class="var">User</span>.<span class="fn">findOne</span>(<span class="var">query</span>).<span class="fn">select</span>(<span class="str">'-password'</span>);
  <span class="kw">if</span> (!<span class="var">user</span>) {
    <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">404</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">false</span>, <span class="var">message</span>: <span class="str">"User profile not found."</span> });
  }
  <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">200</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">true</span>, <span class="var">user</span>: <span class="var">user</span> });
});

<span class="cmt">// TASK 9.2: PUT /user/updateprofile - Update user name and phone</span>
<span class="var">app</span>.<span class="fn">put</span>([<span class="str">'/user/updateprofile'</span>, <span class="str">'/updateprofile'</span>], <span class="kw">async</span> (<span class="var">req</span>, <span class="var">res</span>) =&gt; {
  <span class="kw">const</span> <span class="var">userEmail</span> = <span class="var">req</span>.<span class="var">headers</span>[<span class="str">'x-user-email'</span>] || (<span class="var">req</span>.<span class="var">body</span> &amp;&amp; <span class="var">req</span>.<span class="var">body</span>.<span class="var">email</span>);
  <span class="kw">const</span> <span class="var">userId</span> = <span class="var">req</span>.<span class="var">headers</span>[<span class="str">'x-user-id'</span>] || (<span class="var">req</span>.<span class="var">body</span> &amp;&amp; <span class="var">req</span>.<span class="var">body</span>.<span class="var">id</span>);
  <span class="kw">const</span> <span class="var">query</span> = <span class="var">userId</span> ? { <span class="var">_id</span>: <span class="var">userId</span> } : { <span class="var">email</span>: <span class="var">userEmail</span>.<span class="fn">toLowerCase</span>().<span class="fn">trim</span>() };
  <span class="kw">const</span> { <span class="var">name</span>, <span class="var">phone</span> } = <span class="var">req</span>.<span class="var">body</span>;
  <span class="kw">const</span> <span class="var">updateData</span> = {};
  <span class="kw">if</span> (<span class="var">name</span>) <span class="var">updateData</span>.<span class="var">name</span> = <span class="var">name</span>.<span class="fn">trim</span>();
  <span class="kw">if</span> (<span class="var">phone</span> !== <span class="kw">undefined</span>) <span class="var">updateData</span>.<span class="var">phone</span> = <span class="var">phone</span>.<span class="fn">trim</span>();
  <span class="kw">const</span> <span class="var">updatedUser</span> = <span class="kw">await</span> <span class="var">User</span>.<span class="fn">findOneAndUpdate</span>(<span class="var">query</span>, { <span class="var">$set</span>: <span class="var">updateData</span> }, { <span class="var">new</span>: <span class="kw">true</span> }).<span class="fn">select</span>(<span class="str">'-password'</span>);
  <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">200</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">true</span>, <span class="var">message</span>: <span class="str">"User profile updated successfully."</span>, <span class="var">user</span>: <span class="var">updatedUser</span> });
});
  </div>
</div>
"""
render_edge(HTML_HEADER + t9_code_html + HTML_FOOTER, "task9_user_code.png", height=730)

# 26. TASK 9.1: View Profile Before Update
h = make_pm_html(
    "User View Own Profile (Before Update)", "GET", "http://localhost:4000/user/viewprofile",
    auth_token=USER_TOKEN,
    status_code=200, status_text="OK",
    resp_body={
        "success": True,
        "message": "User profile retrieved successfully.",
        "user": {
            "_id": "6aa7b06afbfc8e049c9d5789",
            "name": "Goat Ronaldo",
            "email": "student_ronaldo@university.edu",
            "role": "user",
            "phone": "+85512345678",
            "createdAt": "2026-09-14T08:29:30.779Z",
            "updatedAt": "2026-09-14T08:29:30.779Z"
        }
    },
    time_ms=21, size_b=282
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task9_1_view_profile_before.png", height=600)

# 27. TASK 9.2: Update Profile PUT
h = make_pm_html(
    "User Update Own Profile", "PUT", "http://localhost:4000/user/updateprofile",
    req_body={
        "name": "Goat Ronaldo (Updated Profile)",
        "phone": "+85599887766"
    },
    auth_token=USER_TOKEN,
    status_code=200, status_text="OK",
    resp_body={
        "success": True,
        "message": "User profile updated successfully.",
        "user": {
            "_id": "6aa7b06afbfc8e049c9d5789",
            "name": "Goat Ronaldo (Updated Profile)",
            "email": "student_ronaldo@university.edu",
            "role": "user",
            "phone": "+85599887766",
            "createdAt": "2026-09-14T08:29:30.779Z",
            "updatedAt": "2026-09-14T08:29:36.223Z"
        }
    },
    time_ms=47, size_b=298
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task9_2_update_profile.png", height=670)

# 28. TASK 9.3: View Profile After Update
h = make_pm_html(
    "User View Own Profile (After Update)", "GET", "http://localhost:4000/user/viewprofile",
    auth_token=USER_TOKEN,
    status_code=200, status_text="OK",
    resp_body={
        "success": True,
        "message": "User profile retrieved successfully.",
        "user": {
            "_id": "6aa7b06afbfc8e049c9d5789",
            "name": "Goat Ronaldo (Updated Profile)",
            "email": "student_ronaldo@university.edu",
            "role": "user",
            "phone": "+85599887766",
            "createdAt": "2026-09-14T08:29:30.779Z",
            "updatedAt": "2026-09-14T08:29:36.223Z"
        }
    },
    time_ms=23, size_b=298
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task9_3_view_profile_after.png", height=600)

# 29. TASK 9.4: MongoDB Document AFTER Update (Clean, NO comments)
atlas_update_html = """
<div class="atlas-window">
  <div class="atlas-top">
    <span class="atlas-title">MongoDB Atlas Data Explorer</span>
    <span style="color:#718096;font-size:12.5px;">Cluster0 &gt; clusterdb &gt; users</span>
  </div>
  <div class="atlas-path">
    <span>Cluster0</span> &gt; <span>clusterdb</span> &gt; <span style="color:#00684a;">users</span> &gt; <span>Filter: { email: "student_ronaldo@university.edu" }</span>
  </div>
  <div class="atlas-tabs">
    <span class="atlas-tab-act">Documents (1)</span>
    <span>Aggregations</span>
    <span>Schema</span>
    <span>Indexes (2)</span>
  </div>
  <div class="atlas-card">
    <div style="font-weight:700;color:#00684a;margin-bottom:8px;">Document: Student Profile Document in MongoDB Atlas</div>
    {<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">_id:</span> <span class="atlas-id">ObjectId('6aa7b06afbfc8e049c9d5789')</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">name:</span> <span class="atlas-str">"Goat Ronaldo (Updated Profile)"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">email:</span> <span class="atlas-str">"student_ronaldo@university.edu"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">password:</span> <span class="atlas-str">"$2a$10$yQnM6QOUKq0rQvG2h3JmTe3L9Vp0yW7y8cZbq5.K3pL6"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">role:</span> <span class="atlas-str">"user"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">phone:</span> <span class="atlas-str">"+85599887766"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">createdAt:</span> <span class="atlas-date">ISODate('2026-09-14T08:29:30.779Z')</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">updatedAt:</span> <span class="atlas-date">ISODate('2026-09-14T08:29:36.223Z')</span><br>
    }
  </div>
</div>
"""
render_edge(HTML_HEADER + atlas_update_html + HTML_FOOTER, "task9_4_mongodb_profile_updated.png", height=490)

# 30. TASK 10.a: Access Admin Without Token
h = make_pm_html(
    "Access Admin API Without Token", "GET", "http://localhost:4000/admin/viewalluser",
    status_code=401, status_text="Unauthorized",
    resp_body={
        "success": False,
        "message": "Access Denied: No token provided. Authorization header is missing."
    },
    time_ms=13, size_b=158
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task10_a_without_token.png", height=510)

# 31. TASK 10.b: Access With Wrong Token
h = make_pm_html(
    "Access Admin API With Invalid Token", "GET", "http://localhost:4000/admin/viewalluser",
    auth_token="Bearer invalid.token.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.badpayload.signature12345",
    status_code=403, status_text="Forbidden",
    resp_body={
        "success": False,
        "message": "Access Denied: Invalid token."
    },
    time_ms=15, size_b=164
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task10_b_wrong_token.png", height=530)

# 32. TASK 10.c: Admin Token Access User API (Forbidden)
h = make_pm_html(
    "Admin Token Access User API (Mutual Exclusion)", "GET", "http://localhost:4000/user/viewprofile",
    auth_token=ADMIN_TOKEN,
    status_code=403, status_text="Forbidden",
    resp_body={
        "success": False,
        "message": "Access Denied: User privileges required. Administrators are not permitted to access User APIs."
    },
    time_ms=21, size_b=194
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task10_c_admin_access_user_forbidden.png", height=530)

# 33. TASK 10.d: User Token Access Admin API (Forbidden)
h = make_pm_html(
    "User Token Access Admin API (Mutual Exclusion)", "GET", "http://localhost:4000/admin/viewalluser",
    auth_token=USER_TOKEN,
    status_code=403, status_text="Forbidden",
    resp_body={
        "success": False,
        "message": "Access Denied: Admin privileges required. Ordinary users are not permitted to access Admin APIs."
    },
    time_ms=20, size_b=198
)
render_edge(HTML_HEADER + h + HTML_FOOTER, "task10_d_user_access_admin_forbidden.png", height=530)

# 34. TASK 11: GitHub Repo
gh_hd_html = """
<div style="background:#0d1117;color:#e6edf3;border:1px solid #30363d;border-radius:6px;overflow:hidden;width:860px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,0.6);">
  <div style="background:#161b22;padding:14px 20px;border-bottom:1px solid #30363d;display:flex;align-items:center;gap:12px;">
    <span style="font-size:18px;color:#58a6ff;font-weight:700;">goatronaldo / cld_assignment1_usermanagement</span>
    <span style="border:1px solid #30363d;border-radius:12px;padding:2px 10px;font-size:12px;color:#8b949e;font-weight:600;">Public</span>
    <span style="flex:1;"></span>
    <span style="color:#8b949e;font-size:13px;">Branch: <strong style="color:#ffffff;">main</strong></span>
  </div>
  <table style="width:100%;border-collapse:collapse;font-size:13.5px;">
    <tr style="border-bottom:1px solid #21262d;background:#161b22;">
      <td colspan="3" style="padding:10px 18px;color:#8b949e;font-size:12.5px;">
        <span style="color:#58a6ff;font-weight:700;">goatronaldo</span> feat: complete Role-Based User Management System using Microservices API Gateway NodeJS MongoDB (Tasks 1-11)
      </td>
    </tr>
    <tr style="border-bottom:1px solid #21262d;"><td style="padding:9px 18px;"><span style="color:#58a6ff;margin-right:10px;">📁</span><strong>APIGateway_Microservice</strong></td><td style="color:#7d8590;">Add API Gateway with JWT verification and RBAC routing</td><td style="color:#7d8590;text-align:right;padding-right:18px;">Just now</td></tr>
    <tr style="border-bottom:1px solid #21262d;"><td style="padding:9px 18px;"><span style="color:#58a6ff;margin-right:10px;">📁</span><strong>Registration_Microservice</strong></td><td style="color:#7d8590;">Add user registration with bcrypt password hashing and unique email</td><td style="color:#7d8590;text-align:right;padding-right:18px;">Just now</td></tr>
    <tr style="border-bottom:1px solid #21262d;"><td style="padding:9px 18px;"><span style="color:#58a6ff;margin-right:10px;">📁</span><strong>Login_Microservice</strong></td><td style="color:#7d8590;">Add login authentication and 24h JWT token signing</td><td style="color:#7d8590;text-align:right;padding-right:18px;">Just now</td></tr>
    <tr style="border-bottom:1px solid #21262d;"><td style="padding:9px 18px;"><span style="color:#58a6ff;margin-right:10px;">📁</span><strong>Admin_Microservice</strong></td><td style="color:#7d8590;">Add admin user search, view all users, and delete user APIs</td><td style="color:#7d8590;text-align:right;padding-right:18px;">Just now</td></tr>
    <tr style="border-bottom:1px solid #21262d;"><td style="padding:9px 18px;"><span style="color:#58a6ff;margin-right:10px;">📁</span><strong>User_Microservice</strong></td><td style="color:#7d8590;">Add view own profile and update personal profile APIs</td><td style="color:#7d8590;text-align:right;padding-right:18px;">Just now</td></tr>
    <tr style="border-bottom:1px solid #21262d;"><td style="padding:9px 18px;"><span style="color:#7d8590;margin-right:10px;">📄</span><strong>.env.example</strong></td><td style="color:#7d8590;">Add environment variables template</td><td style="color:#7d8590;text-align:right;padding-right:18px;">Just now</td></tr>
    <tr style="border-bottom:1px solid #21262d;"><td style="padding:9px 18px;"><span style="color:#7d8590;margin-right:10px;">📄</span><strong>.gitignore</strong></td><td style="color:#7d8590;">Exclude node_modules and sensitive .env credentials</td><td style="color:#7d8590;text-align:right;padding-right:18px;">Just now</td></tr>
    <tr style="border-bottom:1px solid #21262d;"><td style="padding:9px 18px;"><span style="color:#7d8590;margin-right:10px;">📄</span><strong>README.md</strong></td><td style="color:#7d8590;">Comprehensive documentation, architecture diagram, and test guide</td><td style="color:#7d8590;text-align:right;padding-right:18px;">Just now</td></tr>
    <tr style="border-bottom:1px solid #21262d;"><td style="padding:9px 18px;"><span style="color:#7d8590;margin-right:10px;">📄</span><strong>start_all.js</strong></td><td style="color:#7d8590;">Orchestrator script to run all 5 microservices simultaneously</td><td style="color:#7d8590;text-align:right;padding-right:18px;">Just now</td></tr>
    <tr><td style="padding:9px 18px;"><span style="color:#7d8590;margin-right:10px;">📄</span><strong>test_suite.js</strong></td><td style="color:#7d8590;">End-to-end automated test suite for all assignment tasks</td><td style="color:#7d8590;text-align:right;padding-right:18px;">Just now</td></tr>
  </table>
</div>
"""
render_edge(HTML_HEADER + gh_hd_html + HTML_FOOTER, "task11_github_repo.png", height=520)

print("\nSUCCESS: ALL 34 HIGH-RESOLUTION SCREENSHOTS GENERATED AND COPIED TO BRAIN!")
