from fpdf import FPDF

class ScoutPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Talent Scout: Candidate Analysis Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def create_scout_report():
    # Your Candidate Data
    candidates = [
        {"rank": 1, "name": "ANJALI", "why": "Expert in Kubernetes/Docker, B.E in Electronics (80%).", "improve": "Soft skills.", "contact": "anjali@email.com"},
        {"rank": 2, "name": "MONICA", "why": "Proficient in Python and CRM tools; automated sales reporting.", "improve": "Communication and advanced Excel.", "contact": "monica@email.com"},
        {"rank": 3, "name": "LEO", "why": "Strong in Java, C++, and Data Structures. Google HashCode participant.", "improve": "Practical project implementation.", "contact": "leo@email.com"},
        {"rank": 5, "name": "KEVIN", "why": "Experience as a freelance web developer.", "improve": "Corporate workflow experience.", "contact": "kevin@email.com"},
        {"rank": 6, "name": "RAHUL", "why": "Good communication and basic C knowledge.", "improve": "Technical depth and Microsoft Office.", "contact": "rahul@email.com"}
    ]

    # Sort numerically just in case
    candidates = sorted(candidates, key=lambda x: x['rank'])

    pdf = ScoutPDF()

    # --- PAGE 1: RANKINGS TABLE ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Executive Summary: Rankings", 0, 1, 'L')
    pdf.ln(5)
    
    # Table Header
    pdf.set_fill_color(200, 220, 255)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(40, 10, " Rank", 1, 0, 'C', True)
    pdf.cell(150, 10, " Candidate Name", 1, 1, 'L', True)
    
    # Table Rows
    pdf.set_font("Arial", '', 12)
    for c in candidates:
        pdf.cell(40, 10, f"#{c['rank']}", 1, 0, 'C')
        pdf.cell(150, 10, f" {c['name']}", 1, 1, 'L')

    # --- PAGE 2: DETAILS ---
    pdf.add_page()
    for c in candidates:
        # Candidate Header
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(0, 102, 204) # Blue
        pdf.cell(0, 10, f"RANK #{c['rank']} | CANDIDATE: {c['name']}", 0, 1)
        
        # Why this Rank
        pdf.set_font('Arial', 'B', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, "Why this Rank:", 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 5, c['why'])
        
        # Areas for Improvement
        pdf.set_font('Arial', 'B', 10)
        pdf.set_text_color(200, 0, 0) # Red
        pdf.cell(0, 7, "Areas for Improvement:", 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 5, c['improve'])
        
        pdf.ln(5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)

    # --- PAGE 3: STUDENT INFO (AT LAST) ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "STUDENT CONTACT INFORMATION", 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 11)
    for c in candidates:
        pdf.cell(0, 8, f"Candidate: {c['name']} | Contact: {c['contact']}", 0, 1)

    pdf.output("Final_Talent_Scout_Report.pdf")
    print("🚀 Success! Created 'Final_Talent_Scout_Report.pdf'")

if __name__ == "__main__":
    create_scout_report()