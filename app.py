from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import PyPDF2
import re
from fpdf import FPDF

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'

# Create folders if they don't exist
for folder in [app.config['UPLOAD_FOLDER'], app.config['RESULT_FOLDER']]:
    if not os.path.exists(folder): os.makedirs(folder)

# --- PDF Generation Logic ---
class ScoutPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Final Talent Scout Report', 0, 1, 'C')
        self.ln(5)

def process_scout_logic(input_path):
    # (Your existing parsing logic here to extract ranks and names)
    # This example uses the data seen in your uploaded report [cite: 1, 3, 8]
    sorted_data = [
        {"rank": 1, "name": "ANJALI", "why": "Expert in Kubernetes/Docker", "improve": "Soft skills", "email": "anjali@email.com"},
        {"rank": 6, "name": "RAHUL", "why": "Good communication", "improve": "Technical depth", "email": "rahul@email.com"}
    ]

    pdf = ScoutPDF()
    
    # Page 1: Rankings Table [cite: 1]
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Executive Summary", 0, 1)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(40, 10, "Rank", 1)
    pdf.cell(100, 10, "Candidate Name", 1, 1)
    pdf.set_font("Arial", '', 12)
    for item in sorted_data:
        pdf.cell(40, 10, f"#{item['rank']}", 1)
        pdf.cell(100, 10, item['name'], 1, 1)

    # Page 2: Details [cite: 3-12]
    pdf.add_page()
    for item in sorted_data:
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, f"RANK #{item['rank']} | {item['name']}", 0, 1)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 7, "Why this Rank:", 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, item['why'])
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 7, "Areas for Improvement:", 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, item['improve'])
        pdf.ln(10)

    # Page 3: Student Info [cite: 15-17]
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "STUDENT CONTACT INFORMATION", 0, 1, 'C')
    pdf.set_font("Arial", '', 10)
    for item in sorted_data:
        pdf.cell(0, 8, f"Name: {item['name']} | Email: {item['email']}", 0, 1)

    out_p = os.path.join(app.config['RESULT_FOLDER'], "Scout_Final_Report.pdf")
    pdf.output(out_p)
    return out_p

# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/<role>')
def login(role):
    return render_template('login.html', role=role)

@app.route('/auth', methods=['POST'])
def auth():
    role = request.form.get('role')
    if role == 'recruiter':
        return redirect(url_for('recruiter_dashboard'))
    return redirect(url_for('student_upload'))

@app.route('/student_upload')
def student_upload():
    return render_template('upload.html')

# FIX: Allow POST method and redirect to waiting
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], "raw_report.pdf"))
            # After saving, go to the waiting page
            return redirect(url_for('waiting'))
    return "No file uploaded", 400

@app.route('/waiting')
def waiting():
    return render_template('waiting.html')

@app.route('/recruiter_dashboard')
def recruiter_dashboard():
    ready = os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], "raw_report.pdf"))
    return render_template('recruiter_action.html', file_ready=ready)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    input_p = os.path.join(app.config['UPLOAD_FOLDER'], "raw_report.pdf")
    if os.path.exists(input_p):
        result_pdf = process_scout_logic(input_p)
        return send_file(result_pdf, as_attachment=True)
    return "No report found.", 404

if __name__ == '__main__':
    app.run(debug=True)