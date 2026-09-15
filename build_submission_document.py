import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

SCREENSHOTS_DIR = r"D:\Agent\cld\University_User_Management_Platform\screenshots"
DOCX_OUT_ROOT = r"D:\Agent\cld\Role_Based_User_Management_Submission.docx"
DOCX_OUT_PROJ = r"D:\Agent\cld\University_User_Management_Platform\Role_Based_User_Management_Submission.docx"
PDF_OUT_ROOT = r"D:\Agent\cld\Role_Based_User_Management_Submission.pdf"
PDF_OUT_PROJ = r"D:\Agent\cld\University_User_Management_Platform\Role_Based_User_Management_Submission.pdf"

doc = docx.Document()

# Set page margins to 0.5 inches
for section in doc.sections:
    section.top_margin = Inches(0.5)
    section.bottom_margin = Inches(0.5)
    section.left_margin = Inches(0.5)
    section.right_margin = Inches(0.5)

def set_run_font(run, font_name="Calibri", size_pt=11, bold=False, color_rgb=(0,0,0), italic=False):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)

def add_header_block():
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(0)
    r1 = p.add_run("Fall 2026 Semester\n")
    set_run_font(r1, "Calibri", 12, bold=True, color_rgb=(80, 80, 80))
    
    r2 = p.add_run("CLD 376 Cloud Native Development\n")
    set_run_font(r2, "Calibri", 14, bold=True, color_rgb=(0, 51, 102))

    p_student = doc.add_paragraph()
    p_student.paragraph_format.space_before = Pt(4)
    p_student.paragraph_format.space_after = Pt(10)
    r3 = p_student.add_run("Goat Ronaldo\n")
    set_run_font(r3, "Calibri", 13, bold=True, color_rgb=(0, 0, 0))
    r4 = p_student.add_run("ID: 2024476\n")
    set_run_font(r4, "Calibri", 11, bold=False, color_rgb=(60, 60, 60))

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(14)
    r5 = p_title.add_run("01. Role-Based User Management System Using Microservices API Gateway NodeJS MongoDB")
    set_run_font(r5, "Calibri", 16, bold=True, color_rgb=(0, 70, 140))

def add_callout_box(text, bold_prefix="Scenario: "):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    cell = table.cell(0, 0)
    cell.width = Inches(7.5)
    
    shading = parse_xml(r'<w:shd {} w:fill="F0F4F8"/>'.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(shading)
    
    borders = parse_xml(r'''
        <w:tcBorders {} >
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="0055A5"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    '''.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r_bold = p.add_run(bold_prefix)
    set_run_font(r_bold, "Calibri", 10.5, bold=True, color_rgb=(0, 51, 102))
    r_body = p.add_run(text)
    set_run_font(r_body, "Calibri", 10.5, bold=False, color_rgb=(40, 40, 40))
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, "Calibri", 13.5, bold=True, color_rgb=(0, 51, 102))

def add_body_p(text, bold_lead=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    if bold_lead:
        r_lead = p.add_run(bold_lead + " ")
        set_run_font(r_lead, "Calibri", 10.5, bold=True, color_rgb=(20, 20, 20))
    r = p.add_run(text)
    set_run_font(r, "Calibri", 10.5, bold=False, color_rgb=(40, 40, 40))
    return p

def add_image_with_caption(filename, caption_text, width_inches=6.8):
    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    if os.path.exists(filepath):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(filepath, width=Inches(width_inches))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(caption_text)
        set_run_font(r_cap, "Calibri", 9.5, italic=True, color_rgb=(80, 80, 80))
    else:
        p_err = doc.add_paragraph()
        r = p_err.add_run(f"[Screenshot {filename} missing]")
        set_run_font(r, "Calibri", 10, bold=True, color_rgb=(200, 0, 0))

# ----------------- BUILD DOCUMENT CONTENT -----------------

add_header_block()

add_callout_box(
    "A university Central Identity and User Management Platform developed as independent microservices "
    "communicating through an API Gateway with MongoDB Atlas persistence. Features two distinct user roles: User (students managing personal profile) "
    "and Admin (administrators managing accounts). Strictly enforces mutual exclusion: Users can NEVER access Admin APIs, "
    "and Admins can NEVER access User APIs.",
    bold_prefix="Real-Life Scenario & System Architecture: "
)

# ARCHITECTURE SUMMARY TABLE
table = doc.add_table(rows=6, cols=4)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Microservice", "Port", "Endpoints", "Role / Responsibilities"]
data = [
    ["API Gateway", "4000", "All routes (/) via reverse proxy", "Single entry point, JWT verification, role-based route guard"],
    ["Registration", "5001", "POST /register/userregister", "Validates input, checks duplicate email, bcrypt password hash, MongoDB store"],
    ["Login (Auth)", "5002", "POST /auth/login", "Validates email/password/role, issues signed 24h JWT token"],
    ["Admin Service", "5003", "GET /admin/searchuser, viewalluser\nDELETE /admin/deluser", "Admin operations: search by name/email, view all users, delete user"],
    ["User Service", "5004", "GET /user/viewprofile\nPUT /user/updateprofile", "User operations: view authenticated profile, update profile details"]
]
for col_idx, text in enumerate(headers):
    cell = table.cell(0, col_idx)
    shading = parse_xml(r'<w:shd {} w:fill="003366"/>'.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(shading)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    set_run_font(r, "Calibri", 10, bold=True, color_rgb=(255, 255, 255))

for row_idx, row_data in enumerate(data, start=1):
    for col_idx, text in enumerate(row_data):
        cell = table.cell(row_idx, col_idx)
        if row_idx % 2 == 1:
            shading = parse_xml(r'<w:shd {} w:fill="F7F9FA"/>'.format(nsdecls('w')))
            cell._tc.get_or_add_tcPr().append(shading)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(text)
        set_run_font(r, "Calibri", 9.5, bold=(col_idx==0), color_rgb=(30, 30, 30))

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# 1. TASK 1
add_heading_1("Task 1 – Five Microservices Running")
add_body_p(
    "All five independent microservices (API Gateway on port 4000, Registration Service on port 5001, "
    "Login Service on port 5002, Admin Service on port 5003, and User Service on port 5004) started and running simultaneously. "
    "TCP port listener verification confirms each process is actively listening on its designated port.",
    bold_lead="Microservices Orchestration:"
)
add_image_with_caption(
    "task1_2_microservices_running.png",
    "Evidence 1: PowerShell Orchestrator - All 5 Microservices running simultaneously on ports 4000, 5001, 5002, 5003, and 5004."
)

# 2. TASK 2
add_heading_1("Task 2 – MongoDB Database Connection")
add_body_p(
    "Mongoose database connection module (dbconnect.js) implemented with connection pooling, retry options, "
    "and deployment ping command. Successful execution confirms active connection to MongoDB Atlas database (clusterdb).",
    bold_lead="Database Connectivity:"
)
add_image_with_caption(
    "task2_dbconnect.png",
    "Evidence 2: VS Code editor showing dbconnect.js and terminal verification showing successful MongoDB Atlas connection."
)

# 3. TASK 3
add_heading_1("Task 3 – MongoDB User Model")
add_body_p(
    "Complete Mongoose User schema (user_schema.js) created according to specification with _id, name, email (unique, lowercase), "
    "password (bcrypt hashed), role (enum: ['admin', 'user']), optional phone number, and automatic timestamps (createdAt, updatedAt).",
    bold_lead="Schema Definition:"
)
add_image_with_caption(
    "task3_user_model_code.png",
    "Evidence 3: VS Code editor - Complete MongoDB User Model Schema (user_schema.js) with required fields, validation, and timestamps."
)

# 4. TASK 4
add_heading_1("Task 4 – API Gateway Routing and Reverse Proxy")
add_body_p(
    "API Gateway (api-gateway.js) implemented as the single client entry point on port 4000 using http-proxy reverse routing. "
    "Routes /register requests to Port 5001, /auth requests to Port 5002, /admin requests to Port 5003, and /user requests to Port 5004.",
    bold_lead="Gateway Routing Architecture:"
)
add_image_with_caption(
    "task4_apigateway_routing_code.png",
    "Evidence 4: VS Code editor - API Gateway reverse proxy routing table (api-gateway.js) routing to ports 5001, 5002, 5003, and 5004."
)

# 5. TASK 5
add_heading_1("Task 5 – User Registration Microservice")
add_body_p(
    "Registration Microservice route handler (POST /register/userregister) performs field validation, verifies that the email is not already "
    "registered in MongoDB Atlas, hashes the plaintext password with bcrypt (10 rounds), and saves the new user document.",
    bold_lead="Registration Logic & Source Code:"
)
add_image_with_caption(
    "task5_registration_code.png",
    "Evidence 5: VS Code editor - Registration Microservice route handler (/register/userregister) with validation, duplicate check, and bcrypt hashing."
)

add_body_p(
    "Client registers a new student user account (Goat Ronaldo) via POST http://localhost:4000/register/userregister through the API Gateway. "
    "Registration service validates input, securely hashes the password with bcrypt, stores the document in MongoDB, and returns Status 201 Created.",
    bold_lead="Student User Registration:"
)
add_image_with_caption(
    "task5_1_register_user.png",
    "Evidence 5b: Postman - POST http://localhost:4000/register/userregister registering student account Goat Ronaldo (Status 201 Created, 44ms)."
)

add_body_p(
    "Administrator account registered via POST http://localhost:4000/register/userregister with role 'admin' for subsequent administrative operations.",
    bold_lead="Admin Account Setup:"
)
add_image_with_caption(
    "task5_2_register_admin.png",
    "Evidence 5c: Postman - POST http://localhost:4000/register/userregister registering administrator account (Status 201 Created, 39ms)."
)

add_body_p(
    "Temporary user registered via POST http://localhost:4000/register/userregister to provide authentic continuity for the upcoming administrative deletion test.",
    bold_lead="Temporary Account Registration (for Deletion Test):"
)
add_image_with_caption(
    "task5_2b_register_temp.png",
    "Evidence 5d: Postman - POST http://localhost:4000/register/userregister registering temporary test user (Status 201 Created, 35ms)."
)

add_body_p(
    "Attempting to register with an email address that already exists in MongoDB is immediately rejected with Status 400 Bad Request "
    "and error message 'Duplicate email not accepted. A user with this email address already exists.'",
    bold_lead="Duplicate Email Prevention:"
)
add_image_with_caption(
    "task5_3_duplicate_email.png",
    "Evidence 6: Postman - Duplicate email rejected with Status 400 Bad Request ('Duplicate email not accepted', 18ms)."
)

add_body_p(
    "MongoDB Atlas collection (clusterdb.users) inspection displaying all 3 registered user documents. "
    "Passwords are never stored in plain text and are securely hashed with bcrypt ($2a$10$...).",
    bold_lead="MongoDB Atlas Persistence Verification:"
)
add_image_with_caption(
    "task5_4_mongodb_users.png",
    "Evidence 7: MongoDB Atlas Data Explorer - Collection view displaying the 3 registered user documents with bcrypt password hashes."
)

# 6. TASK 6
add_heading_1("Task 6 – Login and JWT Authentication Microservice")
add_body_p(
    "Login Microservice route handler (POST /auth/login) checks if the email exists, compares the submitted password against the bcrypt hash, "
    "verifies the role matches the registered account, and generates a 24-hour signed JSON Web Token (JWT).",
    bold_lead="Authentication Logic & Source Code:"
)
add_image_with_caption(
    "task6_login_code.png",
    "Evidence 8: VS Code editor - Login Microservice route handler (/auth/login) verifying credentials and issuing 24-hour signed JWTs."
)

add_body_p(
    "Student user logs in via POST http://localhost:4000/auth/login through the API Gateway. "
    "Login service verifies credentials against MongoDB and returns Status 200 OK along with a signed 24-hour JWT token.",
    bold_lead="Student User Login:"
)
add_image_with_caption(
    "task6_1_user_login.png",
    "Evidence 8b: Postman - POST http://localhost:4000/auth/login returning Status 200 OK and signed user JWT token (53ms)."
)

add_body_p(
    "Administrator logs in via POST http://localhost:4000/auth/login returning Status 200 OK and signed Admin JWT token.",
    bold_lead="Admin Login:"
)
add_image_with_caption(
    "task6_2_admin_login.png",
    "Evidence 8c: Postman - POST http://localhost:4000/auth/login returning Status 200 OK and signed Admin JWT token (49ms)."
)

add_body_p(
    "Login attempt with an incorrect password is rejected with Status 401 Unauthorized ('Invalid credentials: Password does not match').",
    bold_lead="Invalid Password Handling:"
)
add_image_with_caption(
    "task6_3_invalid_password.png",
    "Evidence 9: Postman - Incorrect password rejected with Status 401 Unauthorized ('Password does not match', 46ms)."
)

add_body_p(
    "Login attempt with an unregistered email is rejected with Status 401 Unauthorized ('Invalid credentials: User with this email does not exist').",
    bold_lead="Unregistered Email Handling:"
)
add_image_with_caption(
    "task6_4_invalid_email.png",
    "Evidence 9b: Postman - Unregistered email rejected with Status 401 Unauthorized ('User with this email does not exist', 19ms)."
)

add_body_p(
    "Login attempt where the requested role does not match the account's registered role in MongoDB is rejected with Status 403 Forbidden.",
    bold_lead="Invalid Role Handling:"
)
add_image_with_caption(
    "task6_5_invalid_role.png",
    "Evidence 10: Postman - Student account attempting admin login rejected with Status 403 Forbidden ('Role mismatch', 27ms)."
)

# 7. TASK 7
add_heading_1("Task 7 – JWT Authentication and Role-Based Access Control Middleware")
add_body_p(
    "API Gateway middleware (verifyTokenAndRole) inspects the Authorization header, validates the JWT signature and expiration, "
    "and enforces strict Role-Based Access Control (RBAC). Requests to /admin/* require role === 'admin'; requests to /user/* require role === 'user'.",
    bold_lead="Security Gatekeeper Code:"
)
add_image_with_caption(
    "task7_jwt_rbac_gateway_code.png",
    "Evidence 11: VS Code editor - API Gateway verifyTokenAndRole middleware validating JWT tokens and enforcing strict role separation."
)

add_body_p(
    "Accessing a protected endpoint with an expired JWT token is detected by jwt.verify() and rejected with Status 401 Unauthorized ('Access Denied: Expired token').",
    bold_lead="Expired JWT Token Verification:"
)
add_image_with_caption(
    "task7_expired_token.png",
    "Evidence 11b: Postman - GET http://localhost:4000/user/viewprofile with expired JWT token rejected with Status 401 Unauthorized (16ms)."
)

# 8. TASK 8
add_heading_1("Task 8 – Admin Microservice Operations")
add_body_p(
    "Admin Microservice implements three administrative handlers: searchuser (search by name or email), viewalluser (list all registered users), "
    "and deluser (delete user by email). Passwords are excluded from query outputs for security.",
    bold_lead="Admin Service Source Code:"
)
add_image_with_caption(
    "task8_admin_code.png",
    "Evidence 12: VS Code editor - Admin Microservice route handlers for searchuser, viewalluser, and deluser."
)

add_body_p(
    "Administrator retrieves all registered users via GET http://localhost:4000/admin/viewalluser with Admin Bearer Token. "
    "Admin service returns Status 200 OK with all 3 registered user accounts.",
    bold_lead="Admin View All Users:"
)
add_image_with_caption(
    "task8_1_admin_viewalluser.png",
    "Evidence 13: Postman - GET http://localhost:4000/admin/viewalluser with Admin Bearer Token returning all 3 registered users (Status 200 OK, 33ms)."
)

add_body_p(
    "Administrator searches for a student user by query parameter (GET http://localhost:4000/admin/searchuser?email=...) with Admin Bearer Token. "
    "Admin service queries MongoDB and returns Status 200 OK with the matched user document.",
    bold_lead="Admin Search User Found:"
)
add_image_with_caption(
    "task8_2_admin_search_found.png",
    "Evidence 14: Postman - GET http://localhost:4000/admin/searchuser?email=... returning matching student user document (Status 200 OK, 26ms)."
)

add_body_p(
    "Searching for a non-existent user returns Status 404 Not Found with error message 'User not found with the specified search criteria.'",
    bold_lead="Admin Search User Not Found:"
)
add_image_with_caption(
    "task8_3_admin_search_notfound.png",
    "Evidence 15: Postman - GET http://localhost:4000/admin/searchuser?email=ghost... returning Status 404 Not Found (17ms)."
)

add_body_p(
    "Administrator deletes the temporary user account via DELETE http://localhost:4000/admin/deluser?email=temp_to_delete@university.edu with Admin Bearer Token. "
    "Admin service removes the user document from MongoDB and returns Status 200 OK.",
    bold_lead="Admin Delete User:"
)
add_image_with_caption(
    "task8_4_admin_delete_user.png",
    "Evidence 16: Postman - DELETE http://localhost:4000/admin/deluser?email=temp_to_delete@university.edu successfully deleting user (Status 200 OK, 38ms)."
)

add_body_p(
    "MongoDB Atlas collection inspection immediately following deletion confirming that temp_to_delete was completely removed. "
    "The collection now contains exactly 2 documents (Goat Ronaldo and Admin), verifying complete database deletion.",
    bold_lead="MongoDB Atlas Persistence After Deletion:"
)
add_image_with_caption(
    "task8_5_mongodb_after_delete.png",
    "Evidence 17: MongoDB Atlas Data Explorer - Collection view after deletion showing 2 users remaining (proving temp_to_delete was removed)."
)

# 9. TASK 9
add_heading_1("Task 9 – User Microservice Operations")
add_body_p(
    "User Microservice implements personal profile operations: viewprofile (retrieves authenticated profile) and updateprofile "
    "(modifies user name and phone number). Identity is securely extracted from headers forwarded by the API Gateway.",
    bold_lead="User Service Source Code:"
)
add_image_with_caption(
    "task9_user_code.png",
    "Evidence 18: VS Code editor - User Microservice route handlers for viewprofile and updateprofile."
)

add_body_p(
    "Student views personal profile via GET http://localhost:4000/user/viewprofile using User Bearer Token. "
    "API Gateway passes identity to User Microservice, returning Status 200 OK with initial profile details.",
    bold_lead="View Profile Before Update:"
)
add_image_with_caption(
    "task9_1_view_profile_before.png",
    "Evidence 19: Postman - GET http://localhost:4000/user/viewprofile retrieving original user profile (Status 200 OK, 21ms)."
)

add_body_p(
    "Student updates name and phone number via PUT http://localhost:4000/user/updateprofile using User Bearer Token. "
    "User Microservice updates the document in MongoDB and returns Status 200 OK with updated profile information.",
    bold_lead="Update Profile Details:"
)
add_image_with_caption(
    "task9_2_update_profile.png",
    "Evidence 20: Postman - PUT http://localhost:4000/user/updateprofile updating user name and phone (Status 200 OK, 47ms)."
)

add_body_p(
    "Student retrieves profile again via GET http://localhost:4000/user/viewprofile using User Bearer Token, confirming updated profile details (name and phone) are returned with Status 200 OK.",
    bold_lead="View Profile After Update:"
)
add_image_with_caption(
    "task9_3_view_profile_after.png",
    "Evidence 21: Postman - GET http://localhost:4000/user/viewprofile verifying updated profile data (Status 200 OK, 23ms)."
)

add_body_p(
    "MongoDB Atlas collection inspection confirming the profile was modified in the database: name changed to 'Goat Ronaldo (Updated Profile)', "
    "phone changed to '+85599887766', and updatedAt timestamp automatically refreshed.",
    bold_lead="MongoDB Atlas Document Verification After Update:"
)
add_image_with_caption(
    "task9_4_mongodb_profile_updated.png",
    "Evidence 22: MongoDB Atlas Data Explorer - User profile in clusterdb.users showing updated name, phone, and refreshed timestamp."
)

# 10. TASK 10
add_heading_1("Task 10 – Role-Based Security and Mutual Exclusion Testing")

add_body_p(
    "Client attempts to access protected route GET http://localhost:4000/admin/viewalluser without an Authorization header. "
    "API Gateway intercepts and immediately rejects the request with Status 401 Unauthorized ('Access Denied: No token provided').",
    bold_lead="Security Test 10(a) – Access Admin API Without Token:"
)
add_image_with_caption(
    "task10_a_without_token.png",
    "Evidence 23: Postman - Protected endpoint accessed without Authorization header rejected with Status 401 Unauthorized (13ms)."
)

add_body_p(
    "Client attempts to access protected route using a fabricated or invalid token. "
    "API Gateway verifies token signature, detects invalid token, and rejects with Status 403 Forbidden ('Access Denied: Invalid token').",
    bold_lead="Security Test 10(b) – Access API Using Invalid JWT:"
)
add_image_with_caption(
    "task10_b_wrong_token.png",
    "Evidence 24: Postman - Protected endpoint accessed with invalid JWT rejected with Status 403 Forbidden (15ms)."
)

add_body_p(
    "Client uses an Administrator JWT token to access the User-only endpoint GET http://localhost:4000/user/viewprofile. "
    "API Gateway enforces role mutual exclusion and rejects the request with Status 403 Forbidden ('Access Denied: User privileges required. Administrators are not permitted to access User APIs').",
    bold_lead="Security Test 10(c) – Admin Token Attempting to Access User API:"
)
add_image_with_caption(
    "task10_c_admin_access_user_forbidden.png",
    "Evidence 25: Postman - Administrator token attempting to access User API rejected with Status 403 Forbidden (21ms)."
)

add_body_p(
    "Client uses an Ordinary User (Student) JWT token to access the Administrative endpoint GET http://localhost:4000/admin/viewalluser. "
    "API Gateway enforces role mutual exclusion and rejects the request with Status 403 Forbidden ('Access Denied: Admin privileges required. Ordinary users are not permitted to access Admin APIs').",
    bold_lead="Security Test 10(d) – User Token Attempting to Access Admin API:"
)
add_image_with_caption(
    "task10_d_user_access_admin_forbidden.png",
    "Evidence 26: Postman - Ordinary user token attempting to access Admin API rejected with Status 403 Forbidden (20ms)."
)

# 11. TASK 11
add_heading_1("Task 11 – Public GitHub Repository")
add_body_p(
    "The complete source code including all 5 microservices, schemas, environment templates, and automated test scripts "
    "is published in a public GitHub repository. Sensitive files (.env, node_modules) are properly excluded via .gitignore.",
    bold_lead="Public Repository Link:"
)

p_link = doc.add_paragraph()
r_link_label = p_link.add_run("Public GitHub Repository URL: ")
set_run_font(r_link_label, "Calibri", 11, bold=True, color_rgb=(0, 51, 102))
r_url = p_link.add_run("https://github.com/goatronaldo/cld_assignment1_usermanagement.git")
set_run_font(r_url, "Calibri", 11, bold=True, color_rgb=(0, 102, 204))

add_image_with_caption(
    "task11_github_repo.png",
    "Evidence 27: GitHub Web View - Public repository goatronaldo/cld_assignment1_usermanagement showing the 5 microservices and project files."
)

# Save DOCX files
doc.save(DOCX_OUT_ROOT)
doc.save(DOCX_OUT_PROJ)
print(f"Saved DOCX successfully to: {DOCX_OUT_ROOT}")
print(f"Saved DOCX copy to: {DOCX_OUT_PROJ}")

# Convert to PDF using win32com ExportAsFixedFormat (Full Print Quality, Lossless Images)
try:
    import win32com.client
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    docx_obj = word.Documents.Open(DOCX_OUT_ROOT)
    
    # Export with OptimizeFor=0 (wdExportOptimizeForPrint) to prevent image compression
    docx_obj.ExportAsFixedFormat(
        OutputFileName=PDF_OUT_ROOT,
        ExportFormat=17,       # wdExportFormatPDF
        OpenAfterExport=False,
        OptimizeFor=0,         # wdExportOptimizeForPrint (Preserves full image resolution!)
        CreateBookmarks=1,     # wdExportCreateHeadingBookmarks
        DocStructureTags=True,
        BitmapMissingFonts=True,
        UseISO19005_1=False
    )
    docx_obj.ExportAsFixedFormat(
        OutputFileName=PDF_OUT_PROJ,
        ExportFormat=17,
        OpenAfterExport=False,
        OptimizeFor=0,
        CreateBookmarks=1,
        DocStructureTags=True,
        BitmapMissingFonts=True,
        UseISO19005_1=False
    )
    docx_obj.Close()
    word.Quit()
    print(f"Saved Full Print Quality PDF successfully to: {PDF_OUT_ROOT}")
    print(f"Saved Full Print Quality PDF copy to: {PDF_OUT_PROJ}")
except Exception as e:
    print(f"Word COM conversion note: {e}")
