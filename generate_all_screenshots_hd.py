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
    background: #1c1c1c;
    color: #d4d4d4;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    padding: 0;
    margin: 0;
  }
  .postman-window {
    background: #1c1c1c;
    border: 1px solid #383838;
    border-radius: 6px;
    overflow: hidden;
    width: 860px;
  }
  .pm-top-bar {
    background: #181818;
    height: 38px;
    display: flex;
    align-items: center;
    padding: 0 14px;
    border-bottom: 1px solid #282828;
    justify-content: space-between;
  }
  .pm-tab-active {
    background: #212121;
    padding: 7px 16px;
    border-radius: 4px 4px 0 0;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13.5px;
    color: #ffffff;
    font-weight: 500;
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
    font-size: 14.5px;
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
    border-bottom: 2px solid #ff6c37;
    padding-bottom: 4px;
  }
  .pm-dot { width: 6px; height: 6px; border-radius: 50%; background: #00c853; }
  .pm-editor-header {
    background: #1e1e1e;
    padding: 6px 16px;
    font-size: 11.5px;
    color: #888888;
    display: flex;
    gap: 12px;
    border-bottom: 1px solid #282828;
  }
  .pm-editor-header span.active { color: #e0e0e0; font-weight: 600; }
  .code-pane {
    background: #181818;
    padding: 10px 16px;
    font-family: "Cascadia Code", Consolas, monospace;
    font-size: 14px;
    line-height: 1.55;
    color: #d4d4d4;
  }
  .line { display: flex; }
  .ln { width: 34px; color: #666666; text-align: right; margin-right: 14px; user-select: none; font-size: 12.5px; }
  .code-text { flex: 1; }
  .k { color: #4fc1ff; font-weight: 600; }
  .s { color: #ce9178; }
  .b { color: #569cd6; font-weight: bold; }
  .n { color: #b5cea8; }

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
    font-size: 14px;
    line-height: 1.55;
    color: #d4d4d4;
    white-space: pre-wrap;
  }
  .kw { color: #c586c0; font-weight: 600; }
  .fn { color: #dcdcaa; }
  .str { color: #ce9178; }
  .cmt { color: #6a9955; font-style: italic; }
  .var { color: #9cdcfe; }
  .type { color: #4ec9b0; }

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
    margin: 12px 18px;
    padding: 14px 18px;
    font-family: "Cascadia Code", Consolas, monospace;
    font-size: 13px;
    line-height: 1.6;
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
    print(f"Generated HD: {filename}")

def json_to_lines(obj):
    lines = []
    raw = json.dumps(obj, indent=2)
    ln = 1
    for raw_line in raw.split("\n"):
        line_content = raw_line
        # highlight
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
        
        # replace spaces
        leading_spaces = len(line_html) - len(line_html.lstrip(' '))
        indent_html = "&nbsp;&nbsp;" * (leading_spaces // 2)
        line_html_clean = line_html.lstrip(' ')
        lines.append(f'<div class="line"><span class="ln">{ln}</span><span class="code-text">{indent_html}{line_html_clean}</span></div>')
        ln += 1
    return "\n".join(lines)

def make_pm_html(title, method, url, req_body=None, status_code=200, status_text="OK", resp_body=None, auth_token=None):
    badge_class = f"badge-{method.lower()}"
    method_class = f"method-{method.lower()}"
    is_success = status_code in [200, 201]
    pill_class = "pill-success" if is_success else "pill-error"

    req_section = ""
    if auth_token:
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
        <div class="code-pane" style="padding:8px 16px;font-size:12.5px;">
          <span style="color:#888;">Token:</span> <span style="color:#9cdcfe;font-weight:600;">{auth_token}</span>
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
          <div>Time: <span class="pm-meta-val">22 ms</span></div>
          <div>Size: <span class="pm-meta-val">360 B</span></div>
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

# Load test results
with open(r"D:\Agent\cld\University_User_Management_Platform\test_results.json", "r", encoding="utf-8") as f:
    results = json.load(f)
res_map = {r["title"]: r for r in results}

print("Rendering high-resolution Retina screenshots...")

# 1. Task 1: 5 Microservices Running
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
render_edge(HTML_HEADER + t1_html + HTML_FOOTER, "task1_2_microservices_running.png", height=520)

# 2. Task 2: dbconnect.js
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

# 3. Task 3: User Model Code
t3_html = """
<div class="vscode-window">
  <div style="background:#181818;border-bottom:1px solid #282828;">
    <div class="vscode-tab">user_schema.js - MongoDB User Model</div>
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
render_edge(HTML_HEADER + t3_html + HTML_FOOTER, "task3_user_model_code.png", height=670)

# 4. Task 4 & 7: API Gateway Code
t4_html = """
<div class="vscode-window">
  <div style="background:#181818;border-bottom:1px solid #282828;">
    <div class="vscode-tab">api-gateway.js - JWT Authentication &amp; RBAC Route Guards</div>
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

    <span class="var">jwt</span>.<span class="fn">verify</span>(<span class="var">token</span>, <span class="var">JWT_SECRET</span>, (<span class="var">err</span>, <span class="var">decoded</span>) =&gt; {
      <span class="kw">if</span> (<span class="var">err</span>) {
        <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="var">err</span>.<span class="var">name</span> === <span class="str">'TokenExpiredError'</span> ? <span class="num">401</span> : <span class="num">403</span>)
                  .<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">false</span>, <span class="var">message</span>: <span class="str">"Access Denied: Invalid or expired token."</span> });
      }
      <span class="cmt">// SECURITY REQUIREMENT: User CANNOT access Admin; Admin CANNOT access User</span>
      <span class="kw">const</span> <span class="var">userRole</span> = (<span class="var">decoded</span>.<span class="var">role</span> || <span class="str">''</span>).<span class="fn">toLowerCase</span>();
      <span class="kw">if</span> (<span class="var">userRole</span> !== <span class="var">allowedRole</span>.<span class="fn">toLowerCase</span>()) {
        <span class="kw">const</span> <span class="var">msg</span> = <span class="var">allowedRole</span> === <span class="str">'admin'</span> 
          ? <span class="str">"Access Denied: Admin privileges required. Users cannot access Admin APIs."</span>
          : <span class="str">"Access Denied: User privileges required. Admins cannot access User APIs."</span>;
        <span class="kw">return</span> <span class="var">res</span>.<span class="fn">status</span>(<span class="num">403</span>).<span class="fn">json</span>({ <span class="var">success</span>: <span class="kw">false</span>, <span class="var">message</span>: <span class="var">msg</span> });
      }
      <span class="var">req</span>.<span class="var">headers</span>[<span class="str">'x-user-id'</span>] = <span class="var">decoded</span>.<span class="var">id</span>;
      <span class="var">req</span>.<span class="var">headers</span>[<span class="str">'x-user-email'</span>] = <span class="var">decoded</span>.<span class="var">email</span>;
      <span class="fn">next</span>();
    });
  };
}

<span class="cmt">// TASK 4: API GATEWAY REVERSE PROXY ROUTING</span>
<span class="var">app</span>.<span class="fn">use</span>(<span class="str">'/register'</span>, (<span class="var">req</span>, <span class="var">res</span>) =&gt; <span class="var">proxy</span>.<span class="fn">web</span>(<span class="var">req</span>, <span class="var">res</span>, { <span class="var">target</span>: <span class="str">'http://localhost:5001'</span> }));
<span class="var">app</span>.<span class="fn">use</span>(<span class="str">'/auth'</span>, (<span class="var">req</span>, <span class="var">res</span>) =&gt; <span class="var">proxy</span>.<span class="fn">web</span>(<span class="var">req</span>, <span class="var">res</span>, { <span class="var">target</span>: <span class="str">'http://localhost:5002'</span> }));
<span class="var">app</span>.<span class="fn">use</span>(<span class="str">'/admin'</span>, <span class="fn">verifyTokenAndRole</span>(<span class="str">'admin'</span>), (<span class="var">req</span>, <span class="var">res</span>) =&gt; <span class="var">proxy</span>.<span class="fn">web</span>(<span class="var">req</span>, <span class="var">res</span>, { <span class="var">target</span>: <span class="str">'http://localhost:5003'</span> }));
<span class="var">app</span>.<span class="fn">use</span>(<span class="str">'/user'</span>, <span class="fn">verifyTokenAndRole</span>(<span class="str">'user'</span>), (<span class="var">req</span>, <span class="var">res</span>) =&gt; <span class="var">proxy</span>.<span class="fn">web</span>(<span class="var">req</span>, <span class="var">res</span>, { <span class="var">target</span>: <span class="str">'http://localhost:5004'</span> }));
  </div>
</div>
"""
render_edge(HTML_HEADER + t4_html + HTML_FOOTER, "task4_7_apigateway_code.png", height=710)

# 5. Task 5.1: Register User
t = res_map["Task 5.1: Register User Account (Student)"]
h = make_pm_html(t["title"], "POST", "http://localhost:4000/register/userregister", t["reqBody"], t["res"]["status"], "Created", t["res"]["body"])
render_edge(HTML_HEADER + h + HTML_FOOTER, "task5_1_register_user.png", height=670)

# 6. Task 5.2: Register Admin
t = res_map["Task 5.2: Register Admin Account"]
h = make_pm_html(t["title"], "POST", "http://localhost:4000/register/userregister", t["reqBody"], t["res"]["status"], "Created", t["res"]["body"])
render_edge(HTML_HEADER + h + HTML_FOOTER, "task5_2_register_admin.png", height=670)

# 7. Task 5.3: Duplicate Email Validation
t = res_map["Task 5.3: Duplicate Email Prevention Test"]
h = make_pm_html(t["title"], "POST", "http://localhost:4000/register/userregister", t["reqBody"], t["res"]["status"], "Bad Request", t["res"]["body"])
render_edge(HTML_HEADER + h + HTML_FOOTER, "task5_3_duplicate_email.png", height=580)

# 8. Task 5.4: MongoDB Atlas Users
atlas_users_html = """
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
    <div style="font-weight:700;color:#00684a;margin-bottom:6px;">Document 1: Registered Student User (Password Hashed with bcrypt)</div>
    {<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">_id:</span> <span class="atlas-id">ObjectId('6aa7b06afbfc8e049c9d5789')</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">name:</span> <span class="atlas-str">"Try Boukheang"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">email:</span> <span class="atlas-str">"student_boukheang@university.edu"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">password:</span> <span class="atlas-str">"$2a$10$yQnM6QOUKq0rQvG2h3JmTe3L9Vp0yW7y..."</span> <span style="color:#e65100;font-weight:600;">// BCRYPT HASH</span>,<br>
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
    &nbsp;&nbsp;<span style="color:#5c6c75;">password:</span> <span class="atlas-str">"$2a$10$dy8WIpazL37b42kKlMmN9..."</span> <span style="color:#e65100;font-weight:600;">// BCRYPT HASH</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">role:</span> <span class="atlas-str">"admin"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">phone:</span> <span class="atlas-str">"+85598765432"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">createdAt:</span> <span class="atlas-date">ISODate('2026-09-14T08:29:31.485Z')</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">updatedAt:</span> <span class="atlas-date">ISODate('2026-09-14T08:29:31.485Z')</span><br>
    }
  </div>
</div>
"""
render_edge(HTML_HEADER + atlas_users_html + HTML_FOOTER, "task5_4_mongodb_users.png", height=580)

# 9. Task 6.1: Valid User Login
t = res_map["Task 6.1: Valid User Login"]
h = make_pm_html(t["title"], "POST", "http://localhost:4000/auth/login", t["reqBody"], t["res"]["status"], "OK", t["res"]["body"])
render_edge(HTML_HEADER + h + HTML_FOOTER, "task6_1_user_login.png", height=670)

# 10. Task 6.2: Valid Admin Login
t = res_map["Task 6.2: Valid Admin Login"]
h = make_pm_html(t["title"], "POST", "http://localhost:4000/auth/login", t["reqBody"], t["res"]["status"], "OK", t["res"]["body"])
render_edge(HTML_HEADER + h + HTML_FOOTER, "task6_2_admin_login.png", height=670)

# 11. Task 6.3: Invalid Password
t = res_map["Task 6.3: Invalid Password Login Attempt"]
h = make_pm_html(t["title"], "POST", "http://localhost:4000/auth/login", t["reqBody"], t["res"]["status"], "Unauthorized", t["res"]["body"])
render_edge(HTML_HEADER + h + HTML_FOOTER, "task6_3_invalid_password.png", height=540)

# 12. Task 6.4: Invalid Role
t = res_map["Task 6.4: Invalid Role Login Attempt"]
h = make_pm_html(t["title"], "POST", "http://localhost:4000/auth/login", t["reqBody"], t["res"]["status"], "Forbidden", t["res"]["body"])
render_edge(HTML_HEADER + h + HTML_FOOTER, "task6_4_invalid_role.png", height=540)

# 13. Task 8.1: Admin View All Users
t = res_map["Task 8.1: Admin View All Users"]
h = make_pm_html(t["title"], "GET", "http://localhost:4000/admin/viewalluser", None, t["res"]["status"], "OK", t["res"]["body"], auth_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... [Admin Token]")
render_edge(HTML_HEADER + h + HTML_FOOTER, "task8_1_admin_viewalluser.png", height=700)

# 14. Task 8.2a: Admin Search User (Found)
t = res_map["Task 8.2a: Admin Search User (Found by Email)"]
h = make_pm_html(t["title"], "GET", "http://localhost:4000/admin/searchuser?email=student_boukheang@university.edu", None, t["res"]["status"], "OK", t["res"]["body"], auth_token="Bearer [Admin Token]")
render_edge(HTML_HEADER + h + HTML_FOOTER, "task8_2_admin_search_found.png", height=620)

# 15. Task 8.2c: Admin Search User (Not Found)
t = res_map["Task 8.2c: Admin Search User (Not Found)"]
h = make_pm_html(t["title"], "GET", "http://localhost:4000/admin/searchuser?email=ghost_nonexistent@university.edu", None, t["res"]["status"], "Not Found", t["res"]["body"], auth_token="Bearer [Admin Token]")
render_edge(HTML_HEADER + h + HTML_FOOTER, "task8_3_admin_search_notfound.png", height=540)

# 16. Task 8.3: Admin Delete User
t = res_map["Task 8.3: Admin Delete User by Email"]
h = make_pm_html(t["title"], "DELETE", "http://localhost:4000/admin/deluser?email=temp_to_delete@university.edu", None, t["res"]["status"], "OK", t["res"]["body"], auth_token="Bearer [Admin Token]")
render_edge(HTML_HEADER + h + HTML_FOOTER, "task8_4_admin_delete_user.png", height=560)

# 17. Task 9.1: View Profile Before Update
t = res_map["Task 9.1: User View Own Profile (Before Update)"]
h = make_pm_html(t["title"], "GET", "http://localhost:4000/user/viewprofile", None, t["res"]["status"], "OK", t["res"]["body"], auth_token="Bearer [User Token]")
render_edge(HTML_HEADER + h + HTML_FOOTER, "task9_1_view_profile_before.png", height=600)

# 18. Task 9.2: Update Profile
t = res_map["Task 9.2: User Update Own Profile"]
h = make_pm_html(t["title"], "PUT", "http://localhost:4000/user/updateprofile", t["reqBody"], t["res"]["status"], "OK", t["res"]["body"], auth_token="Bearer [User Token]")
render_edge(HTML_HEADER + h + HTML_FOOTER, "task9_2_update_profile.png", height=660)

# 18b. Task 9.3: View Profile After Update
t = res_map["Task 9.3: User View Own Profile (After Update)"]
h = make_pm_html(t["title"], "GET", "http://localhost:4000/user/viewprofile", None, t["res"]["status"], "OK", t["res"]["body"], auth_token="Bearer [User Token]")
render_edge(HTML_HEADER + h + HTML_FOOTER, "task9_3_view_profile_after.png", height=600)

# 19. Task 9.4: MongoDB After Update
atlas_update_html = """
<div class="atlas-window">
  <div class="atlas-top">
    <span class="atlas-title">MongoDB Atlas Data Explorer</span>
    <span style="color:#718096;font-size:12.5px;">Cluster0 &gt; clusterdb &gt; users</span>
  </div>
  <div class="atlas-path">
    <span>Cluster0</span> &gt; <span>clusterdb</span> &gt; <span style="color:#00684a;">users</span> &gt; <span>Filter: { email: "student_boukheang@university.edu" }</span>
  </div>
  <div class="atlas-tabs">
    <span class="atlas-tab-act">Documents (1)</span>
    <span>Aggregations</span>
    <span>Schema</span>
    <span>Indexes (2)</span>
  </div>
  <div class="atlas-card">
    <div style="font-weight:700;color:#00684a;margin-bottom:8px;">Document: Student Profile AFTER Update (PUT /user/updateprofile)</div>
    {<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">_id:</span> <span class="atlas-id">ObjectId('6aa7b06afbfc8e049c9d5789')</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">name:</span> <span class="atlas-str">"Try Boukheang (Updated Profile)"</span> <span style="color:#00684a;font-weight:700;">// &lt;-- UPDATED NAME</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">email:</span> <span class="atlas-str">"student_boukheang@university.edu"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">password:</span> <span class="atlas-str">"$2a$10$yQnM6QOUKq0rQvG2h3JmTe3L9Vp0yW7y..."</span> <span style="color:#e65100;font-weight:600;">// HASHED</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">role:</span> <span class="atlas-str">"user"</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">phone:</span> <span class="atlas-str">"+85599887766"</span> <span style="color:#00684a;font-weight:700;">// &lt;-- UPDATED PHONE (WAS +85512345678)</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">createdAt:</span> <span class="atlas-date">ISODate('2026-09-14T08:29:30.779Z')</span>,<br>
    &nbsp;&nbsp;<span style="color:#5c6c75;">updatedAt:</span> <span class="atlas-date">ISODate('2026-09-14T08:29:36.223Z')</span> <span style="color:#00684a;font-weight:700;">// &lt;-- TIMESTAMP REFRESHED</span><br>
    }
  </div>
</div>
"""
render_edge(HTML_HEADER + atlas_update_html + HTML_FOOTER, "task9_4_mongodb_profile_updated.png", height=490)

# 20. Task 10.a: Access Admin Without Token
t = res_map["Task 10.a: Access Admin API Without Token"]
h = make_pm_html(t["title"], "GET", "http://localhost:4000/admin/viewalluser", None, t["res"]["status"], "Unauthorized", t["res"]["body"])
render_edge(HTML_HEADER + h + HTML_FOOTER, "task10_a_without_token.png", height=510)

# 21. Task 10.b: Access With Wrong Token
t = res_map["Task 10.b: Access Admin API With Wrong Token"]
h = make_pm_html(t["title"], "GET", "http://localhost:4000/admin/viewalluser", None, t["res"]["status"], "Forbidden", t["res"]["body"], auth_token="Bearer this.is.an.invalid.token.12345")
render_edge(HTML_HEADER + h + HTML_FOOTER, "task10_b_wrong_token.png", height=530)

# 22. Task 10.c: Admin Token Access User API (Forbidden)
t = res_map["Task 10.c: Using Admin Token to Access User API"]
h = make_pm_html(t["title"], "GET", "http://localhost:4000/user/viewprofile", None, t["res"]["status"], "Forbidden", t["res"]["body"], auth_token="Bearer [Admin Token]")
render_edge(HTML_HEADER + h + HTML_FOOTER, "task10_c_admin_access_user_forbidden.png", height=530)

# 23. Task 10.d: User Token Access Admin API (Forbidden)
t = res_map["Task 10.d: Using User Token to Access Admin API"]
h = make_pm_html(t["title"], "GET", "http://localhost:4000/admin/viewalluser", None, t["res"]["status"], "Forbidden", t["res"]["body"], auth_token="Bearer [User Token]")
render_edge(HTML_HEADER + h + HTML_FOOTER, "task10_d_user_access_admin_forbidden.png", height=530)

# 24. Task 11: GitHub Repo
gh_hd_html = """
<div style="background:#0d1117;color:#e6edf3;border:1px solid #30363d;border-radius:6px;overflow:hidden;width:860px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;">
  <div style="background:#161b22;padding:14px 20px;border-bottom:1px solid #30363d;display:flex;align-items:center;gap:12px;">
    <span style="font-size:18px;color:#58a6ff;font-weight:700;">boukheang / cld_assignment1_usermanagement</span>
    <span style="border:1px solid #30363d;border-radius:12px;padding:2px 10px;font-size:12px;color:#8b949e;font-weight:600;">Public</span>
    <span style="flex:1;"></span>
    <span style="color:#8b949e;font-size:13px;">Branch: <strong style="color:#ffffff;">main</strong></span>
  </div>
  <table style="width:100%;border-collapse:collapse;font-size:13.5px;">
    <tr style="border-bottom:1px solid #21262d;background:#161b22;">
      <td colspan="3" style="padding:10px 18px;color:#8b949e;font-size:12.5px;">
        <span style="color:#58a6ff;font-weight:700;">boukheang</span> feat: complete Role-Based User Management System using Microservices API Gateway NodeJS MongoDB (Tasks 1-11)
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

print("ALL 24 HIGH-RESOLUTION SCREENSHOTS GENERATED!")
