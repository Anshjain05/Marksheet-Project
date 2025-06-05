**"School Marksheet Generator (Streamlit App)"**.

---

```markdown
# 🏫 School Marksheet Generator

A user-friendly web application built with **Streamlit** that allows teachers or administrators to upload an Excel file and automatically generate personalized **PDF marksheets** for students — complete with subject-wise grades, school branding, and principal signature.

---

## 📌 Features

- 🔐 **Secure Login & User Authentication**
  - Simple username/password protection with bcrypt hashing.
  - User-specific sessions maintained securely via Streamlit session state.

- 📁 **Excel-Based Mark Upload**
  - Upload student data in Excel format.
  - Dynamic detection of subject columns.
  - Automatic grade calculation for each subject.

- 🖨️ **Auto-Generated Marksheet PDFs**
  - Generates individual PDFs for each student.
  - Includes student's name, roll number, parent details, marks, and grades.
  - Includes school logo, name, address, session, and principal signature.
  - Merges all PDFs into a downloadable single file.

- 📝 **Customizable School Details**
  - School name, address, class, session year, principal name and logo are saved per user session.

- 📤 **Downloadable Merged PDF**
  - Download all generated marksheets as one consolidated file.
  - Preview marksheets directly within the browser.

---

## 🚀 Live Demo

> Coming soon... (you can deploy this on [Streamlit Cloud](https://streamlit.io/cloud) or a private server)

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **Streamlit** - for frontend UI
- **pandas** - for data handling
- **FPDF** - for PDF generation
- **PyPDF2** - for merging PDFs
- **bcrypt** - for secure password hashing

---

## 📁 Project Structure

```

📦 School-Marksheet-Generator
├── 📄 app.py                 # Main Streamlit app
├── 📄 users.csv              # Stores registered users and their hashed passwords
├── 📁 generated\_marksheets   # Output folder for generated PDFs
├── 📄 requirements.txt       # Required Python packages
└── 📄 README.md              # You're here!

````

---

## 🧾 Excel Format Example

Your uploaded Excel file **must contain** these mandatory columns:

| Roll No. | Name of the student | Father's Name | Mother's Name | Math | Science | ... |
|----------|---------------------|----------------|----------------|------|---------|-----|

- The script dynamically detects the remaining columns as subjects.
- It calculates grades for each subject based on marks.

---

## 📊 Grading Scheme

| Marks Range | Grade |
|-------------|-------|
| 90 - 100    | A+    |
| 80 - 89     | A     |
| 70 - 79     | B+    |
| 60 - 69     | B     |
| 50 - 59     | C     |
| 40 - 49     | D     |
| Below 40    | F     |

---

## 🧪 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/school-marksheet-generator.git
cd school-marksheet-generator
````

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
streamlit run app.py
```

The app will launch in your browser at `http://localhost:8501`.

---

## 📦 Requirements

The `requirements.txt` file should contain:

```
streamlit
bcrypt
pandas
fpdf
PyPDF2
openpyxl
```

To generate it, run:

```bash
pip freeze > requirements.txt
```

---

## ✅ To-Do / Future Enhancements

* Add student photos to the marksheet.
* Email individual PDFs to students/parents.
* Include bar charts or visual grade summary.
* Admin dashboard for managing users and reports.
* Export data to CSV/Excel post-grading.

---

## 🔒 Security Note

* Passwords are hashed using **bcrypt** and stored in `users.csv`.
* Do not expose the `users.csv` file in public repositories if sensitive data is stored.

---

## 📄 License

This project is open-source and available under the **MIT License**.

---

## 🙌 Contributing

Pull requests are welcome! If you find bugs or want to suggest features, feel free to open an issue or submit a PR.

---

## 👨‍💻 Author

Developed by \[Ansh Jain]
📧 Contact: \[[anshjainsdw@gmail.com](mailto:anshjainsdw@gmail.com)]
📎 GitHub: [github.com/Anshjain05](https://github.com/Anshjain05)

---

```

Let me know if you'd like me to include screenshots or a badge section (e.g., Streamlit app status, Python version, etc.) or tailor it to your GitHub username!
```
