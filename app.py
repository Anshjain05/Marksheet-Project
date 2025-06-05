import streamlit as st
import bcrypt
import pandas as pd
from fpdf import FPDF
import os
import base64
from PyPDF2 import PdfMerger
import csv
from io import BytesIO
import tempfile

# ------------------------------
# Utility Functions
# ------------------------------

def merge_pdfs(pdf_paths):
    """Merge multiple PDF files into a single in-memory PDF."""
    merger = PdfMerger()
    for path in pdf_paths:
        merger.append(path)
    merged_pdf_io = BytesIO()
    merger.write(merged_pdf_io)
    merger.close()
    merged_pdf_io.seek(0)  # Reset pointer to start
    return merged_pdf_io

def show_pdf(file_path):
    """Display a PDF file in Streamlit using an iframe."""
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="900" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# ------------------------------
# User Storage & Authentication
# ------------------------------

def load_users():
    if os.path.exists("users.csv"):
        with open("users.csv", mode="r") as f:
            reader = csv.DictReader(f)
            return {row["username"]: row["password"] for row in reader}
    return {}

def save_user(username, hashed_password):
    file_exists = os.path.exists("users.csv")
    with open("users.csv", mode="a", newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["username", "password"])
        writer.writerow([username, hashed_password.decode()])

def check_password():
    users = load_users()

    def password_entered():
        username = st.session_state["username"]
        password = st.session_state["password"]
        if username in users and bcrypt.checkpw(password.encode(), users[username].encode()):
            st.session_state["authentication_status"] = True
            st.session_state["name"] = username
        else:
            st.session_state["authentication_status"] = False
            st.session_state["name"] = None

    if "authentication_status" not in st.session_state:
        st.session_state["authentication_status"] = None
        st.session_state["name"] = None

    if st.session_state["authentication_status"]:
        return True
    elif st.session_state["authentication_status"] is False:
        st.error("Incorrect username or password")
        return False
    else:
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False

# ------------------------------
# Account Creation UI
# ------------------------------

def create_account():
    with st.expander("🆕 Create a New Account"):
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        confirm_pass = st.text_input("Confirm Password", type="password")
        if st.button("Create Account"):
            if new_pass != confirm_pass:
                st.error("Passwords do not match.")
                return
            users = load_users()
            if new_user in users:
                st.error("Username already exists.")
            else:
                hashed = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt())
                save_user(new_user, hashed)
                st.success("Account created! You can now log in.")

# ------------------------------
# Grade Calculation Logic
# ------------------------------

def calculate_grade(mark):
    if mark >= 90:
        return "A+"
    elif mark >= 80:
        return "A"
    elif mark >= 70:
        return "B+"
    elif mark >= 60:
        return "B"
    elif mark >= 50:
        return "C"
    elif mark >= 40:
        return "D"
    else:
        return "F"

# ------------------------------
# PDF Generation Class
# ------------------------------

class MarksheetPDF(FPDF):
    def header(self):
        if hasattr(self, "school_logo_path") and self.school_logo_path:
            self.image(self.school_logo_path, 10, 8, 25)
        self.set_font("Arial", "B", 16)
        if hasattr(self, "school_name") and self.school_name:
            self.cell(0, 10, self.school_name, ln=True, align="C")
        self.set_font("Arial", "I", 12)
        if hasattr(self, "school_address") and self.school_address:
            self.cell(0, 8, self.school_address, ln=True, align="C")
        if hasattr(self, "session_year") and self.session_year:
            self.cell(0, 10, f"Academic Session: {self.session_year}", ln=True, align="C")
        self.ln(10)

    def student_info(self, roll, name, father, mother, class_name):
        self.set_font("Arial", "", 12)
        self.cell(90, 8, f"Name of Student: {name}", ln=False)
        self.cell(0, 8, f"Roll No.: {roll}", ln=True)
        self.cell(90, 8, f"Father's Name: {father}", ln=False)
        self.cell(0, 8, f"Mother's Name: {mother}", ln=True)
        self.cell(0, 8, f"Class: {class_name}", ln=True)
        self.ln(5)

    def marks_table(self, subjects):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(200, 220, 255)
        self.cell(80, 10, "Subject", border=1, fill=True)
        self.cell(40, 10, "Marks Obtained", border=1, fill=True)
        self.cell(40, 10, "Grade", border=1, ln=True, fill=True)

        self.set_font("Arial", "", 11)
        total_marks = 0
        for subj, (mark, grade) in subjects.items():
            total_marks += mark
            self.cell(80, 8, subj, border=1)
            self.cell(40, 8, f"{mark}", border=1, align="C")
            self.cell(40, 8, grade, border=1, align="C", ln=True)

        self.set_font("Arial", "B", 12)
        self.cell(80, 10, "Total", border=1)
        self.cell(40, 10, f"{total_marks}", border=1, align="C")
        self.cell(40, 10, "", border=1, ln=True)

    # def remarks_section(self, remarks=""):
    #     self.ln(8)
    #     self.set_font("Arial", "I", 11)
    #     self.multi_cell(0, 10, f"Remarks: {remarks if remarks else 'N/A'}")
    #     self.ln(5)

    def footer(self):
        self.set_y(-35)
        self.set_font("Arial", "", 10)
        self.cell(0, 10, f"Signature of Principal: ____________________", ln=True, align="R")
        self.ln(5)
        self.cell(0, 10, f"( {self.principal_name} )", ln=True, align="R")

    def create_marksheet(self, roll, name, father, mother, subjects, class_name, school_name, session_year, principal_name, remarks="", school_logo_path=None, school_address=""):
        self.school_name = school_name
        self.session_year = session_year
        self.principal_name = principal_name
        self.school_logo_path = school_logo_path
        self.school_address = school_address

        self.add_page()
        self.student_info(roll, name, father, mother, class_name)
        self.marks_table(subjects)
        #self.remarks_section(remarks)

# ------------------------------
# Streamlit App Main
# ------------------------------

st.set_page_config(page_title="School Marksheet Generator", layout="centered")
st.title("🏫 School Marksheet Generator")

# Authenticate user
if not check_password():
    create_account()  # Show registration below login
    st.stop()

# Get logged-in username
username = st.session_state["name"]
st.sidebar.success(f"Welcome {username} 👋")

# Logout button
st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authentication_status": False, "name": None}))

# Persistent permanent details memory in session
if "permanent_details" not in st.session_state:
    st.session_state["permanent_details"] = {}

if not st.session_state["permanent_details"]:
    # Sidebar input for permanent details
    st.sidebar.header("Enter Permanent Details")
    class_name = st.sidebar.text_input("Class (e.g., 10th, 12th)")
    school_name = st.sidebar.text_input("School Name")
    school_address = st.sidebar.text_input("School Address")
    principal_name = st.sidebar.text_input("Principal Name")
    session_year = st.sidebar.text_input("Session (e.g., 2024-2025)")
    school_logo_file = st.sidebar.file_uploader("Upload School Logo (PNG/JPG)", type=["png", "jpg", "jpeg"])

    if school_logo_file is not None:
        temp_logo_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        temp_logo_file.write(school_logo_file.read())
        temp_logo_file.close()
        logo_path = temp_logo_file.name
    else:
        logo_path = None

    if st.sidebar.button("Save Details"):
        if class_name and school_name and school_address and principal_name and session_year:
            st.session_state["permanent_details"] = {
                "class_name": class_name,
                "school_name": school_name,
                "school_address": school_address,
                "principal_name": principal_name,
                "session_year": session_year,
                "logo_path": logo_path
            }
            st.sidebar.success("Details saved! They will be remembered next time you login.")
        else:
            st.sidebar.error("Please fill all fields.")
else:
    # Show saved details with option to edit
    details = st.session_state["permanent_details"]
    st.sidebar.header("Permanent Details")
    st.sidebar.write(f"**Class:** {details['class_name']}")
    st.sidebar.write(f"**School Name:** {details['school_name']}")
    st.sidebar.write(f"**School Address:** {details['school_address']}")
    st.sidebar.write(f"**Principal Name:** {details['principal_name']}")
    st.sidebar.write(f"**Session:** {details['session_year']}")
    if st.sidebar.button("Edit Details"):
        # Remove temporary logo file if exists when editing
        if details.get("logo_path") and os.path.exists(details["logo_path"]):
            os.remove(details["logo_path"])
        st.session_state["permanent_details"] = {}

# File uploader for marksheet data Excel
uploaded_file = st.file_uploader("📥 Upload Excel File (Use provided format)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ File uploaded successfully!")

    # Required columns validation
    required_cols = ['Roll No.', 'Name of the student', "Father's Name", "Mother's Name"]
    for col in required_cols:
        if col not in df.columns:
            st.error(f"Missing required column: {col}")
            st.stop()

    # Check for empty required fields
    if df[required_cols].isnull().any().any():
        st.error("Some required fields are empty. Please fill all mandatory columns.")
        st.stop()

    # Identify subjects dynamically
    subject_cols = [c for c in df.columns if c not in required_cols]

    if not subject_cols:
        st.error("No subjects found in the uploaded file.")
        st.stop()

    # Calculate grades for each subject column dynamically
    for subject in subject_cols:
        df[f"{subject} Grade"] = df[subject].apply(calculate_grade)

    # Prepare to generate marksheets
    if st.button("📄 Generate Marksheets"):
        if not st.session_state.get("permanent_details"):
            st.error("Please enter permanent details in the sidebar first.")
            st.stop()

        details = st.session_state["permanent_details"]
        logo_path = details.get("logo_path")

        output_dir = "generated_marksheets"
        os.makedirs(output_dir, exist_ok=True)
        pdf_paths = []

        for _, row in df.iterrows():
            roll = row['Roll No.']
            student = row['Name of the student']
            father = row["Father's Name"]
            mother = row["Mother's Name"]
            subjects = {}

            for subj in subject_cols:
                mark = int(row[subj])
                grade = row[f"{subj} Grade"]
                subjects[subj] = (mark, grade)

            pdf = MarksheetPDF()
            pdf.create_marksheet(
                roll, student, father, mother, subjects,
                details["class_name"], details["school_name"],
                details["session_year"], details["principal_name"],
                school_logo_path=logo_path,
                school_address=details["school_address"]
            )
            file_path = os.path.join(output_dir, f"{roll}_{student.replace(' ', '_')}.pdf")
            pdf.output(file_path)
            pdf_paths.append(file_path)

        st.success("🎉 Marksheets generated successfully!")

        # Merge PDFs and show one preview
        merged_pdf_io = merge_pdfs(pdf_paths)

        merged_preview_path = os.path.join(output_dir, "merged_preview.pdf")
        with open(merged_preview_path, "wb") as f:
            f.write(merged_pdf_io.read())
        merged_pdf_io.seek(0)

        st.download_button(
            label="📥 Download All Marksheets (Merged PDF)",
            data=merged_pdf_io,
            file_name="All_Marksheets.pdf",
            mime="application/pdf"
        )

        st.write("### Preview: All Marksheets Merged")
        show_pdf(merged_preview_path)

        # Cleanup temporary logo file after generation
        if logo_path and os.path.exists(logo_path):
            os.remove(logo_path)

else:
    st.info("Please upload an Excel file containing marksheet data.")
