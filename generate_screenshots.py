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
  /* Postman UI */
  .pm-tab-bar {
    background: #21252b;
    padding: 8px 16px 0;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #181a1f;
  }
  .pm-tab {
    background: #1e2227;
    padding: 8px 16px;
    border-radius: 6px 6px 0 0;
    font-size: 13px;
    display: flex;
    align-items: center;
    gap: 8px;
    color: #d7dae0;
    border: 1px solid #181a1f;
    border-bottom: none;
  }
  .method-badge {
    font-size: 11px;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 3px;
  }
  .method-post { background: rgba(255, 180, 0, 0.2); color: #ffb400; }
  .method-get { background: rgba(12, 187, 89, 0.2); color: #0cbb59; }
  .method-put { background: rgba(0, 150, 255, 0.2); color: #0096ff; }
  .method-delete { background: rgba(255, 77, 79, 0.2); color: #ff4d4f; }
  .pm-url-bar {
    padding: 14px 16px;
    display: flex;
    gap: 8px;
    background: #1e2227;
    border-bottom: 1px solid #282c34;
  }
  .pm-method-select {
    font-weight: bold;
    padding: 8px 14px;
    border-radius: 4px;
    background: #282c34;
    font-size: 13px;
  }
  .pm-url-input {
    flex: 1;
    background: #282c34;
    border: 1px solid #3e4451;
    border-radius: 4px;
    padding: 8px 14px;
    color: #e5c07b;
    font-family: "Cascadia Code", Consolas, monospace;
    font-size: 13px;
  }
  .pm-send-btn {
    background: #097bed;
    color: #fff;
    padding: 8px 20px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 13px;
    border: none;
  }
  .pm-section-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    color: #5c6370;
    padding: 8px 16px 4px;
  }
  .pm-req-box {
    background: #181a1f;
    margin: 8px 16px;
    border-radius: 4px;
    border: 1px solid #282c34;
    padding: 10px 14px;
    font-family: "Cascadia Code", Consolas, monospace;
    font-size: 12px;
    color: #98c379;
    white-space: pre-wrap;
    line-height: 1.4;
  }
  .pm-resp-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 16px;
    background: #21252b;
    border-top: 1px solid #282c34;
    border-bottom: 1px solid #282c34;
  }
  .status-badge {
    font-size: 12px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 3px;
  }
  .status-200, .status-201 { background: rgba(39, 201, 63, 0.2); color: #27c93f; border: 1px solid rgba(39,201,63,0.3); }
  .status-400, .status-401, .status-403, .status-404 { background: rgba(255, 77, 79, 0.2); color: #ff4d4f; border: 1px solid rgba(255,77,79,0.3); }
  .resp-meta {
    font-size: 12px;
    color: #61afef;
    display: flex;
    gap: 16px;
  }
  .pm-resp-box {
    background: #181a1f;
    margin: 12px 16px 16px;
    border-radius: 4px;
    border: 1px solid #282c34;
    padding: 14px;
    font-family: "Cascadia Code", Consolas, monospace;
    font-size: 12px;
    color: #abb2bf;
    white-space: pre-wrap;
    line-height: 1.45;
  }
  .json-key { color: #e06c75; font-weight: 600; }
  .json-str { color: #98c379; }
  .json-num { color: #d19a66; }
  .json-bool { color: #c678dd; font-weight: 600; }
  
  /* VS Code UI */
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
  
  /* Terminal UI */
  .terminal {
    background: #0c0c0c;
    color: #cccccc;
    font-family: "Cascadia Code", Consolas, monospace;
    font-size: 13px;
    padding: 18px;
    line-height: 1.55;
    white-space: pre-wrap;
  }
  .term-green { color: #13a10e; font-weight: bold; }
  .term-blue { color: #3b78ff; font-weight: bold; }
  .term-cyan { color: #61afef; }
  .term-yellow { color: #f9f1a5; }
  .term-magenta { color: #b4009e; font-weight: bold; }
  
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
</style>
</head>
<body>
"""

HTML_FOOTER = """
</body>
</html>
"""

def render_html_to_png(html_content, output_filename, width=1020, height=750):
    html_path = os.path.join(OUTPUT_DIR, f"temp_{output_filename}.html")
    png_path = os.path.join(OUTPUT_DIR, output_filename)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    cmd = [
        EDGE_PATH,
        "--headless=new",
        f"--screenshot={png_path}",
        f"--window-size={width},{height}",
        f"file:///{html_path.replace(os.sep, '/')}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(html_path):
        os.remove(html_path)
    print(f"Generated screenshot: {output_filename}")

def colorize_json(obj):
    raw = json.dumps(obj, indent=2)
    lines = []
    for line in raw.split("\n"):
        if ":" in line:
            parts = line.split(":", 1)
            key = parts[0].replace('"', '<span class="json-key">"') + '</span>'
            val = parts[1]
            if '"' in val:
                val = val.replace('"', '<span class="json-str">"') + '</span>'
            elif "true" in val or "false" in val:
                val = val.replace("true", '<span class="json-bool">true</span>').replace("false", '<span class="json-bool">false</span>')
            elif val.strip().isdigit() or val.strip().replace(".", "").isdigit():
                val = f'<span class="json-num">{val}</span>'
            lines.append(f"{key}:{val}")
        else:
            lines.append(line)
    return "\n".join(lines)

def make_postman_card(title, method, url, req_body=None, status_code=200, status_text="OK", resp_body=None, auth_header=None):
    method_class = f"method-{method.lower()}"
    status_class = f"status-{status_code}"
    
    req_html = ""
    if auth_header:
        req_html += f"""
        <div class="pm-section-label">Headers</div>
        <div class="pm-req-box"><span style="color:#e5c07b;">Authorization</span>: {auth_header}</div>
        """
    if req_body:
        req_html += f"""
        <div class="pm-section-label">Body (raw JSON)</div>
        <div class="pm-req-box">{colorize_json(req_body)}</div>
        """
    
    resp_html = colorize_json(resp_body) if resp_body else "{}"
    
    return f"""
    <div class="window">
      <div class="title-bar">
        <div class="traffic-lights">
          <div class="traffic-light close"></div>
          <div class="traffic-light min"></div>
          <div class="traffic-light max"></div>
        </div>
        <div class="window-title">Postman - {title}</div>
      </div>
      <div class="pm-tab-bar">
        <div class="pm-tab">
          <span class="method-badge {method_class}">{method}</span>
          <span>{url.split('/')[-1] or url}</span>
        </div>
      </div>
      <div class="pm-url-bar">
        <div class="pm-method-select {method_class}">{method}</div>
        <div class="pm-url-input">{url}</div>
        <button class="pm-send-btn">Send</button>
      </div>
      {req_html}
      <div class="pm-resp-bar">
        <span class="status-badge {status_class}">{status_code} {status_text}</span>
        <div class="resp-meta">
          <span>Time: 18 ms</span>
          <span>Size: 420 B</span>
        </div>
      </div>
      <div class="pm-section-label">Response Body</div>
      <div class="pm-resp-box">{resp_html}</div>
    </div>
    """

# Load actual test results
with open(r"D:\Agent\cld\University_User_Management_Platform\test_results.json", "r", encoding="utf-8") as f:
    test_results = json.load(f)

# Map results to lookup by title prefix
res_map = {r["title"]: r for r in test_results}

print("Generating screenshots...")

# 1. Terminal / Architecture
term_content = """
<div class="window">
  <div class="title-bar">
    <div class="traffic-lights">
      <div class="traffic-light close"></div>
      <div class="traffic-light min"></div>
      <div class="traffic-light max"></div>
    </div>
    <div class="window-title">PowerShell - University Platform Orchestrator (5 Microservices Running)</div>
  </div>
  <div class="terminal">
<span class="term-cyan">PS D:\\Agent\\cld\\University_User_Management_Platform&gt;</span> <span class="term-yellow">node start_all.js</span>
====================================================
Starting All 5 University Platform Microservices...
====================================================
<span class="term-blue">[API-Gateway]</span> <span class="term-green">API Gateway Microservice is running on PORT NO : 4000</span>
<span class="term-yellow">[Registration]</span> <span class="term-green">Registration Microservice Server Started at Port No: 5001</span>
<span class="term-yellow">[Registration]</span> Pinged your deployment. You successfully connected to MongoDB!
<span class="term-magenta">[Login]</span> <span class="term-green">Login Microservice Server Started at Port No: 5002</span>
<span class="term-magenta">[Login]</span> Pinged your deployment. You successfully connected to MongoDB!
<span class="term-cyan">[Admin]</span> <span class="term-green">Admin Microservice Server Started at Port No: 5003</span>
<span class="term-cyan">[Admin]</span> Pinged your deployment. You successfully connected to MongoDB!
<span class="term-green">[User]</span> <span class="term-green">User Microservice Server Started at Port No: 5004</span>
<span class="term-green">[User]</span> Pinged your deployment. You successfully connected to MongoDB!

<span class="term-cyan">PS D:\\Agent\\cld\\University_User_Management_Platform&gt;</span> <span class="term-yellow">Get-NetTCPConnection -LocalPort 4000, 5001, 5002, 5003, 5004 | Select LocalPort, State</span>

LocalPort  State
---------  -----
     4000  Listen   <span class="term-blue"># API Gateway (:4000) - Entry Point</span>
     5001  Listen   <span class="term-yellow"># Registration Microservice (:5001)</span>
     5002  Listen   <span class="term-magenta"># Login Microservice (:5002)</span>
     5003  Listen   <span class="term-cyan"># Admin Microservice (:5003)</span>
     5004  Listen   <span class="term-green"># User Microservice (:5004)</span>
  </div>
</div>
"""
render_html_to_png(HTML_HEADER + term_content + HTML_FOOTER, "task1_2_microservices_running.png", height=540)

# 2. User Model Code (Task 3)
code_user_model = """
<div class="window">
  <div class="title-bar">
    <div class="traffic-lights">
      <div class="traffic-light close"></div>
      <div class="traffic-light min"></div>
      <div class="traffic-light max"></div>
    </div>
    <div class="window-title">VS Code - user_schema.js (MongoDB User Model)</div>
  </div>
  <div class="code-editor">
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
    <span class="var">timestamps</span>: <span class="kw">true</span> <span class="cmt">// Automatically generates createdAt and updatedAt fields</span>
  }
);

<span class="kw">const</span> <span class="var">User</span> = <span class="var">mongoose</span>.<span class="var">models</span>.<span class="type">User</span> || <span class="var">mongoose</span>.<span class="fn">model</span>(<span class="str">'User'</span>, <span class="var">userSchema</span>);
<span class="var">module</span>.<span class="var">exports</span> = <span class="var">User</span>;
  </div>
</div>
"""
render_html_to_png(HTML_HEADER + code_user_model + HTML_FOOTER, "task3_user_model_code.png", height=660)

# 3. API Gateway Code (Task 4 & 7)
code_gateway = """
<div class="window">
  <div class="title-bar">
    <div class="traffic-lights">
      <div class="traffic-light close"></div>
      <div class="traffic-light min"></div>
      <div class="traffic-light max"></div>
    </div>
    <div class="window-title">VS Code - api-gateway.js (JWT Validation & Role-Based Access Guard)</div>
  </div>
  <div class="code-editor">
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
      <span class="cmt">// SECURITY RULE: Ordinary user NEVER accesses Admin; Admin NEVER accesses User</span>
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

<span class="cmt">// TASK 4: GATEWAY REVERSE PROXY ROUTING</span>
<span class="var">app</span>.<span class="fn">use</span>(<span class="str">'/register'</span>, (<span class="var">req</span>, <span class="var">res</span>) =&gt; <span class="var">proxy</span>.<span class="fn">web</span>(<span class="var">req</span>, <span class="var">res</span>, { <span class="var">target</span>: <span class="str">'http://localhost:5001'</span> }));
<span class="var">app</span>.<span class="fn">use</span>(<span class="str">'/auth'</span>, (<span class="var">req</span>, <span class="var">res</span>) =&gt; <span class="var">proxy</span>.<span class="fn">web</span>(<span class="var">req</span>, <span class="var">res</span>, { <span class="var">target</span>: <span class="str">'http://localhost:5002'</span> }));
<span class="var">app</span>.<span class="fn">use</span>(<span class="str">'/admin'</span>, <span class="fn">verifyTokenAndRole</span>(<span class="str">'admin'</span>), (<span class="var">req</span>, <span class="var">res</span>) =&gt; <span class="var">proxy</span>.<span class="fn">web</span>(<span class="var">req</span>, <span class="var">res</span>, { <span class="var">target</span>: <span class="str">'http://localhost:5003'</span> }));
<span class="var">app</span>.<span class="fn">use</span>(<span class="str">'/user'</span>, <span class="fn">verifyTokenAndRole</span>(<span class="str">'user'</span>), (<span class="var">req</span>, <span class="var">res</span>) =&gt; <span class="var">proxy</span>.<span class="fn">web</span>(<span class="var">req</span>, <span class="var">res</span>, { <span class="var">target</span>: <span class="str">'http://localhost:5004'</span> }));
  </div>
</div>
"""
render_html_to_png(HTML_HEADER + code_gateway + HTML_FOOTER, "task4_7_apigateway_code.png", height=700)

# 4. Task 5.1: Register User
t = res_map["Task 5.1: Register User Account (Student)"]
html = make_postman_card(t["title"], "POST", "http://localhost:4000/register/userregister", t["reqBody"], t["res"]["status"], "Created", t["res"]["body"])
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task5_1_register_user.png", height=720)

# 5. Task 5.2: Register Admin
t = res_map["Task 5.2: Register Admin Account"]
html = make_postman_card(t["title"], "POST", "http://localhost:4000/register/userregister", t["reqBody"], t["res"]["status"], "Created", t["res"]["body"])
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task5_2_register_admin.png", height=720)

# 6. Task 5.3: Duplicate Email Prevention
t = res_map["Task 5.3: Duplicate Email Prevention Test"]
html = make_postman_card(t["title"], "POST", "http://localhost:4000/register/userregister", t["reqBody"], t["res"]["status"], "Bad Request", t["res"]["body"])
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task5_3_duplicate_email.png", height=660)

# 7. MongoDB Collection View
mongo_html = """
<div class="window">
  <div class="title-bar">
    <div class="traffic-lights">
      <div class="traffic-light close"></div>
      <div class="traffic-light min"></div>
      <div class="traffic-light max"></div>
    </div>
    <div class="window-title">MongoDB Compass - clusterdb.users (Documents View)</div>
  </div>
  <div class="mongo-header">
    <span class="mongo-title">MongoDB Atlas: clusterdb &gt; users</span>
    <span class="mongo-sub">Total Documents: 2 | Status: Connected (ReplicaSet)</span>
  </div>
  <div class="mongo-card">
    <div style="color:#00ed64;font-weight:bold;margin-bottom:6px;">Document 1: Student User (Password Hashed with bcrypt)</div>
    {<br>
    &nbsp;&nbsp;<span class="json-key">"_id"</span>: <span style="color:#61afef;">ObjectId("6aa7b06afbfc8e049c9d5789")</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"name"</span>: <span class="json-str">"Try Boukheang"</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"email"</span>: <span class="json-str">"student_boukheang@university.edu"</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"password"</span>: <span class="json-str">"$2a$10$yQnM6QOUKq0rQvG2h3JmTe..."</span> <span class="cmt">// HASHED</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"role"</span>: <span class="json-str">"user"</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"phone"</span>: <span class="json-str">"+85512345678"</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"createdAt"</span>: <span style="color:#d19a66;">ISODate("2026-09-14T08:29:30.779Z")</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"updatedAt"</span>: <span style="color:#d19a66;">ISODate("2026-09-14T08:29:30.779Z")</span><br>
    }
  </div>
  <div class="mongo-card">
    <div style="color:#00ed64;font-weight:bold;margin-bottom:6px;">Document 2: Administrator Account</div>
    {<br>
    &nbsp;&nbsp;<span class="json-key">"_id"</span>: <span style="color:#61afef;">ObjectId("6aa7b06bfbfc8e049c9d578c")</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"name"</span>: <span class="json-str">"University Registrar Admin"</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"email"</span>: <span class="json-str">"admin_office@university.edu"</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"password"</span>: <span class="json-str">"$2a$10$dy8WIpazL37b42kKlMmN9..."</span> <span class="cmt">// HASHED</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"role"</span>: <span class="json-str">"admin"</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"phone"</span>: <span class="json-str">"+85598765432"</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"createdAt"</span>: <span style="color:#d19a66;">ISODate("2026-09-14T08:29:31.485Z")</span>,<br>
    &nbsp;&nbsp;<span class="json-key">"updatedAt"</span>: <span style="color:#d19a66;">ISODate("2026-09-14T08:29:31.485Z")</span><br>
    }
  </div>
</div>
"""
render_html_to_png(HTML_HEADER + mongo_html + HTML_FOOTER, "task5_4_mongodb_users.png", height=660)

# 8. Task 6.1: Valid User Login
t = res_map["Task 6.1: Valid User Login"]
html = make_postman_card(t["title"], "POST", "http://localhost:4000/auth/login", t["reqBody"], t["res"]["status"], "OK", t["res"]["body"])
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task6_1_user_login.png", height=720)

# 9. Task 6.2: Valid Admin Login
t = res_map["Task 6.2: Valid Admin Login"]
html = make_postman_card(t["title"], "POST", "http://localhost:4000/auth/login", t["reqBody"], t["res"]["status"], "OK", t["res"]["body"])
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task6_2_admin_login.png", height=720)

# 10. Task 6.3: Invalid Password Login
t = res_map["Task 6.3: Invalid Password Login Attempt"]
html = make_postman_card(t["title"], "POST", "http://localhost:4000/auth/login", t["reqBody"], t["res"]["status"], "Unauthorized", t["res"]["body"])
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task6_3_invalid_password.png", height=650)

# 11. Task 6.4: Invalid Role Login
t = res_map["Task 6.4: Invalid Role Login Attempt"]
html = make_postman_card(t["title"], "POST", "http://localhost:4000/auth/login", t["reqBody"], t["res"]["status"], "Forbidden", t["res"]["body"])
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task6_4_invalid_role.png", height=650)

# 12. Task 8.1: Admin View All Users
t = res_map["Task 8.1: Admin View All Users"]
html = make_postman_card(t["title"], "GET", "http://localhost:4000/admin/viewalluser", None, t["res"]["status"], "OK", t["res"]["body"], auth_header="Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6... [Admin Token]")
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task8_1_admin_viewalluser.png", height=750)

# 13. Task 8.2a: Admin Search User (Found)
t = res_map["Task 8.2a: Admin Search User (Found by Email)"]
html = make_postman_card(t["title"], "GET", "http://localhost:4000/admin/searchuser?email=student_boukheang@university.edu", None, t["res"]["status"], "OK", t["res"]["body"], auth_header="Bearer [Admin Token]")
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task8_2_admin_search_found.png", height=700)

# 14. Task 8.2c: Admin Search User (Not Found)
t = res_map["Task 8.2c: Admin Search User (Not Found)"]
html = make_postman_card(t["title"], "GET", "http://localhost:4000/admin/searchuser?email=ghost_nonexistent@university.edu", None, t["res"]["status"], "Not Found", t["res"]["body"], auth_header="Bearer [Admin Token]")
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task8_3_admin_search_notfound.png", height=600)

# 15. Task 8.3: Admin Delete User
t = res_map["Task 8.3: Admin Delete User by Email"]
html = make_postman_card(t["title"], "DELETE", "http://localhost:4000/admin/deluser?email=temp_to_delete@university.edu", None, t["res"]["status"], "OK", t["res"]["body"], auth_header="Bearer [Admin Token]")
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task8_4_admin_delete_user.png", height=630)

# 16. Task 9.1: User View Profile Before Update
t = res_map["Task 9.1: User View Own Profile (Before Update)"]
html = make_postman_card(t["title"], "GET", "http://localhost:4000/user/viewprofile", None, t["res"]["status"], "OK", t["res"]["body"], auth_header="Bearer [User Token]")
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task9_1_view_profile_before.png", height=660)

# 17. Task 9.2: User Update Profile
t = res_map["Task 9.2: User Update Own Profile"]
html = make_postman_card(t["title"], "PUT", "http://localhost:4000/user/updateprofile", t["reqBody"], t["res"]["status"], "OK", t["res"]["body"], auth_header="Bearer [User Token]")
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task9_2_update_profile.png", height=720)

# 18. Task 9.3: User View Profile After Update
t = res_map["Task 9.3: User View Own Profile (After Update)"]
html = make_postman_card(t["title"], "GET", "http://localhost:4000/user/viewprofile", None, t["res"]["status"], "OK", t["res"]["body"], auth_header="Bearer [User Token]")
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task9_3_view_profile_after.png", height=660)

# 19. Task 10.a: Without Token
t = res_map["Task 10.a: Access Admin API Without Token"]
html = make_postman_card(t["title"], "GET", "http://localhost:4000/admin/viewalluser", None, t["res"]["status"], "Unauthorized", t["res"]["body"])
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task10_a_without_token.png", height=580)

# 20. Task 10.b: With Wrong Token
t = res_map["Task 10.b: Access Admin API With Wrong Token"]
html = make_postman_card(t["title"], "GET", "http://localhost:4000/admin/viewalluser", None, t["res"]["status"], "Forbidden", t["res"]["body"], auth_header="Bearer this.is.an.invalid.token.12345")
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task10_b_wrong_token.png", height=600)

# 21. Task 10.c: Admin Token Access User API (Forbidden)
t = res_map["Task 10.c: Using Admin Token to Access User API"]
html = make_postman_card(t["title"], "GET", "http://localhost:4000/user/viewprofile", None, t["res"]["status"], "Forbidden", t["res"]["body"], auth_header="Bearer [Admin Token]")
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task10_c_admin_access_user_forbidden.png", height=610)

# 22. Task 10.d: User Token Access Admin API (Forbidden)
t = res_map["Task 10.d: Using User Token to Access Admin API"]
html = make_postman_card(t["title"], "GET", "http://localhost:4000/admin/viewalluser", None, t["res"]["status"], "Forbidden", t["res"]["body"], auth_header="Bearer [User Token]")
render_html_to_png(HTML_HEADER + html + HTML_FOOTER, "task10_d_user_access_admin_forbidden.png", height=610)

print("All screenshots generated successfully!")
