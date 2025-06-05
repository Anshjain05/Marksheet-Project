**"School Marksheet Generator (Streamlit App)"**.

Here is a **ready-to-paste `README.md`** file including only the **necessary Python dependencies** for your **School Marksheet Generator** project based on the code you provided.

---

````markdown
# 🏫 School Marksheet Generator

A secure, user-authenticated Streamlit web app to generate personalized student marksheets from Excel files and export them as individual or merged PDF documents. Designed for schools or educational institutions to automate result generation efficiently.

---

## 🚀 Features

- ✅ **User Authentication** (login/signup with password hashing)
- 📤 Upload Excel with student marks
- 📝 Automatically compute grades
- 🖨️ Generate professional marksheets in PDF format
- 🧾 Merge all PDFs for easy download
- 🖼️ School logo, principal signature, and academic session info
- 🧠 Saves permanent school/class details per user session

---

## 📦 Requirements

Install dependencies using the `requirements.txt` below:

```txt
streamlit==1.44.1
bcrypt==4.3.0
pandas==2.2.3
fpdf==1.7.2
PyPDF2==3.0.1
openpyxl==3.1.5
````

To install:

```bash
pip install -r requirements.txt
```

---

## 📁 Folder Structure

```bash
project/
│
├── app.py                  # Main Streamlit application file
├── users.csv               # Stores user credentials (generated at runtime)
├── generated_marksheets/   # Stores generated PDF files
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```

---

## 🧪 Excel File Format

The Excel file should contain the following columns:

| Roll No. | Name of the student | Father's Name | Mother's Name | Subject 1 | Subject 2 | ... |
| -------- | ------------------- | ------------- | ------------- | --------- | --------- | --- |

**Note:** Subject names can be dynamic. Grades will be auto-calculated for each subject.

---

## 🛠️ How to Use

1. **Run the App**

```bash
streamlit run app.py
```

2. **Create an Account** or Login

3. **Fill Permanent Details** (School info, logo, principal name)

4. **Upload Excel File** with student marks

5. **Click "Generate Marksheets"**

6. **Preview and Download Merged PDF**

---

## 🔐 Security Notes

* Passwords are hashed using `bcrypt` and stored in `users.csv`.
* Make sure `users.csv` is secured or use a proper database in production.

---

## 📃 License

MIT License

---

## 🙌 Acknowledgments

Developed with ❤️ using [Streamlit](https://streamlit.io/), [FPDF](https://pyfpdf.github.io/), and [PyPDF2](https://pypi.org/project/PyPDF2/).

```