import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

SCREENSHOTS_DIR = r"D:\Agent\cld\University_User_Management_Platform\screenshots"
DOCX_OUT_ROOT = r"D:\Agent\cld\Role_Based_User_Management_Submission.docx"
DOCX_OUT_PROJ = r"D:\Agent\cld\University_User_Management_Platform\Role_Based_User_Management_Submission.docx"

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
    p_student.paragraph_format.space_after = Pt(12)
    r3 = p_student.add_run("Try Boukheang\n")
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
    
    # Light blue background fill
    shading = parse_xml(r'<w:shd {} w:fill="F0F4F8"/>'.format(nsdecls('w')))
    cell._tc.get_or_add_tcPr().append(shading)
    
    # Left thick border
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

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_run_font(r, "Calibri", 11.5, bold=True, color_rgb=(0, 102, 153))

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
    "communicating through an API Gateway with MongoDB Atlas persistence. Features two user classes: User (students/staff managing own profile) "
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

doc.add_paragraph().paragraph_format.space_after = Pt(10)

# TASK 1 & 2
add_heading_1("Task 1 & Task 2: 5 Microservices Setup & Database Connection Verification")
add_body_p(
    "Created 5 independent microservices (API Gateway, Registration, Login, Admin, and User services). "
    "Configured reusable dbconnect.js in all data-handling microservices establishing stable connection to MongoDB Atlas "
    "with connection pooling, ping health check verification, and environment variable configuration.",
    bold_lead="Implementation Overview:"
)
add_image_with_caption(
    "task1_2_microservices_running.png",
    "Figure 1: PowerShell Orchestrator - All 5 Microservices running simultaneously on ports 4000, 5001, 5002, 5003, and 5004 with MongoDB Atlas connected."
)

# TASK 3
add_heading_1("Task 3: MongoDB User Model Implementation (user_schema.js)")
add_body_p(
    "Designed and implemented the Mongoose User Model matching the exact schema requirements. "
    "Fields include _id (ObjectId), name, email (unique index, lowercase), password (bcrypt hashed), "
    "role (enum: 'admin', 'user'), phone, and automatic timestamps (createdAt, updatedAt).",
    bold_lead="Schema Specification:"
)
add_image_with_caption(
    "task3_user_model_code.png",
    "Figure 2: VS Code Editor - Mongoose User Model Schema (user_schema.js) with required fields, validation, and timestamps."
)

# TASK 4 & 7
add_heading_1("Task 4 & Task 7: API Gateway Microservice & JWT Role-Based Routing Guards")
add_body_p(
    "The API Gateway acts as the single entry point for all client requests. Implements http-proxy reverse routing "
    "and strict JWT token verification middleware. Requests lacking a token or containing invalid/expired tokens are rejected. "
    "Crucially, role-based authorization enforces that ordinary users are blocked from Admin APIs (403 Forbidden) "
    "and administrators are blocked from User APIs (403 Forbidden).",
    bold_lead="Gateway & Security Architecture:"
)
add_image_with_caption(
    "task4_7_apigateway_code.png",
    "Figure 3: VS Code Editor - API Gateway source code (api-gateway.js) displaying JWT verification, role guard middleware, and microservice reverse proxy routes."
)

# TASK 5
add_heading_1("Task 5: Registration Microservice API & Database Verification")
add_body_p(
    "Registration API endpoint POST /register/userregister routed through API Gateway to Port 5001. "
    "Validates input, enforces unique email constraint, securely hashes passwords using bcrypt (10 rounds), "
    "and saves documents into MongoDB Atlas.",
    bold_lead="Registration Functionality:"
)
add_heading_2("5.1: Student User Registration (Role: user)")
add_image_with_caption(
    "task5_1_register_user.png",
    "Figure 4: Postman - POST http://localhost:4000/register/userregister registering student account (Status 201 Created)."
)
add_heading_2("5.2: Administrator Account Registration (Role: admin)")
add_image_with_caption(
    "task5_2_register_admin.png",
    "Figure 5: Postman - POST http://localhost:4000/register/userregister registering administrative account (Status 201 Created)."
)
add_heading_2("5.3: Duplicate Email Prevention Test")
add_image_with_caption(
    "task5_3_duplicate_email.png",
    "Figure 6: Postman - Re-registering with existing email rejected with Status 400 Bad Request ('Duplicate email not accepted')."
)
add_heading_2("5.4: MongoDB Atlas Database Verification")
add_image_with_caption(
    "task5_4_mongodb_users.png",
    "Figure 7: MongoDB Compass / Atlas Data View - Registered users stored in clusterdb.users showing bcrypt password hashes."
)

# TASK 6
add_heading_1("Task 6: Login Microservice API & JWT Token Issuance")
add_body_p(
    "Login API endpoint POST /auth/login routed through API Gateway to Port 5002. "
    "Validates email, password (via bcrypt.compare), and requested role against MongoDB. "
    "Upon successful validation, issues a signed JWT containing user ID, email, and role valid for 24 hours.",
    bold_lead="Authentication Workflow:"
)
add_heading_2("6.1: Valid Student Login (Returns JWT)")
add_image_with_caption(
    "task6_1_user_login.png",
    "Figure 8: Postman - POST http://localhost:4000/auth/login for user returning 200 OK and signed JWT token."
)
add_heading_2("6.2: Valid Administrator Login (Returns JWT)")
add_image_with_caption(
    "task6_2_admin_login.png",
    "Figure 9: Postman - POST http://localhost:4000/auth/login for admin returning 200 OK and signed JWT token."
)
add_heading_2("6.3: Login Attempt with Incorrect Password")
add_image_with_caption(
    "task6_3_invalid_password.png",
    "Figure 10: Postman - Incorrect password rejected with Status 401 Unauthorized ('Password does not match')."
)
add_heading_2("6.4: Login Attempt with Role Mismatch")
add_image_with_caption(
    "task6_4_invalid_role.png",
    "Figure 11: Postman - Student account attempting admin login rejected with Status 403 Forbidden ('Role mismatch')."
)

# TASK 8
add_heading_1("Task 8: Admin Microservice APIs")
add_body_p(
    "Admin Microservice (Port 5003) provides administrative user management capabilities. "
    "Access is strictly protected by the API Gateway requiring valid Administrator JWT tokens.",
    bold_lead="Admin Capabilities:"
)
add_heading_2("8.1: View All Users Information")
add_image_with_caption(
    "task8_1_admin_viewalluser.png",
    "Figure 12: Postman - GET http://localhost:4000/admin/viewalluser with Admin Token returning all registered users (Status 200 OK)."
)
add_heading_2("8.2: Search User by Query Parameter (Found vs Not Found)")
add_image_with_caption(
    "task8_2_admin_search_found.png",
    "Figure 13: Postman - GET http://localhost:4000/admin/searchuser?email=... returning matching user document (Status 200 OK)."
)
add_image_with_caption(
    "task8_3_admin_search_notfound.png",
    "Figure 14: Postman - GET http://localhost:4000/admin/searchuser?email=ghost... returning Status 404 Not Found."
)
add_heading_2("8.3: Delete User by Email ID")
add_image_with_caption(
    "task8_4_admin_delete_user.png",
    "Figure 15: Postman - DELETE http://localhost:4000/admin/deluser?email=... successfully deleting user (Status 200 OK)."
)

# TASK 9
add_heading_1("Task 9: User Microservice APIs")
add_body_p(
    "User Microservice (Port 5004) enables students/staff to view and update their own profiles. "
    "The API Gateway authenticates the User token and injects the verified identity headers.",
    bold_lead="User Profile Operations:"
)
add_heading_2("9.1: View Own Profile (Before Update)")
add_image_with_caption(
    "task9_1_view_profile_before.png",
    "Figure 16: Postman - GET http://localhost:4000/user/viewprofile retrieving original user profile (Status 200 OK)."
)
add_heading_2("9.2: Update Profile (PUT /user/updateprofile)")
add_image_with_caption(
    "task9_2_update_profile.png",
    "Figure 17: Postman - PUT http://localhost:4000/user/updateprofile updating user name and phone (Status 200 OK)."
)
add_heading_2("9.3: View Own Profile (After Update)")
add_image_with_caption(
    "task9_3_view_profile_after.png",
    "Figure 18: Postman - GET http://localhost:4000/user/viewprofile confirming updated profile values in MongoDB (Status 200 OK)."
)

# TASK 10
add_heading_1("Task 10: Security & Gatekeeper Tests (Postman With Clear URL & Output)")
add_body_p(
    "Demonstration of the four mandatory security gatekeeper test cases proving comprehensive protection at the API Gateway:",
    bold_lead="Access Control Verification:"
)
add_heading_2("10.a: Access Protected API Without Token")
add_image_with_caption(
    "task10_a_without_token.png",
    "Figure 19: Postman - GET /admin/viewalluser without Authorization header rejected with Status 401 Unauthorized."
)
add_heading_2("10.b: Access Protected API With Wrong / Malformed Token")
add_image_with_caption(
    "task10_b_wrong_token.png",
    "Figure 20: Postman - Access with invalid token rejected with Status 403 Forbidden ('Invalid token')."
)
add_heading_2("10.c: Admin Token Attempting to Access User API (Forbidden)")
add_image_with_caption(
    "task10_c_admin_access_user_forbidden.png",
    "Figure 21: Postman - Admin token attempting GET /user/viewprofile rejected with Status 403 Forbidden ('Admins cannot access User APIs')."
)
add_heading_2("10.d: User Token Attempting to Access Admin API (Forbidden)")
add_image_with_caption(
    "task10_d_user_access_admin_forbidden.png",
    "Figure 22: Postman - User token attempting GET /admin/viewalluser rejected with Status 403 Forbidden ('Users cannot access Admin APIs')."
)

# TASK 11
add_heading_1("Task 11: GitHub Repository & Deployment Details")
add_body_p(
    "The complete codebase including all 5 microservices, schemas, environment configurations, and orchestration scripts "
    "is version-controlled and pushed to the public GitHub repository:",
    bold_lead="Repository Details:"
)

p_link = doc.add_paragraph()
r_link_label = p_link.add_run("Public GitHub Repository URL: ")
set_run_font(r_link_label, "Calibri", 11, bold=True, color_rgb=(0, 51, 102))
r_url = p_link.add_run("https://github.com/boukheang/cld_assignment1_usermanagement.git")
set_run_font(r_url, "Calibri", 11, bold=True, color_rgb=(0, 102, 204))

# Save docx files
doc.save(DOCX_OUT_ROOT)
doc.save(DOCX_OUT_PROJ)
print(f"Saved DOCX successfully to: {DOCX_OUT_ROOT}")
print(f"Saved DOCX copy to: {DOCX_OUT_PROJ}")
