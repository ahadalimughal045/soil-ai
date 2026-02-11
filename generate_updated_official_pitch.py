from fpdf import FPDF
import datetime

class UpdatedPitchPDF(FPDF):
    def header(self):
        # We'll handle headers per slide type
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Soil AI Analyzer | Precision Agriculture | Page {self.page_no()}', 0, 0, 'C')

def create_updated_pitch():
    pdf = UpdatedPitchPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Colors
    primary_color = (0, 255, 136) # Neon green
    bg_color = (10, 10, 12) # Dark bg
    text_white = (255, 255, 255)
    
    # 1. Title Slide
    pdf.add_page()
    pdf.set_fill_color(*bg_color)
    pdf.rect(0, 0, 210, 297, 'F')
    
    pdf.set_font("Arial", 'B', 32)
    pdf.set_text_color(*primary_color)
    pdf.ln(60)
    pdf.cell(0, 20, "Soil-AI Analyzer", ln=True, align='C')
    
    pdf.set_font("Arial", '', 16)
    pdf.set_text_color(*text_white)
    pdf.multi_cell(0, 10, "Advanced AI-Powered Soil Diagnostics\nand Precision Crop Advisory System", align='C')
    
    pdf.ln(20)
    pdf.set_font("Arial", 'I', 12)
    pdf.cell(0, 10, "Smart Farming for a Sustainable Green Revolution", ln=True, align='C')

    # 2. Idea Behind (The "What Ifs")
    pdf.add_page()
    pdf.set_fill_color(*bg_color)
    pdf.rect(0, 0, 210, 297, 'F')
    
    pdf.ln(40)
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(*primary_color)
    pdf.cell(0, 15, "The Vision Behind Soil AI", ln=True, align='L')
    
    pdf.set_font("Arial", 'I', 14)
    pdf.set_text_color(*text_white)
    pdf.ln(10)
    quote = [
        "What if a small farmer didn't have to gamble their season because they didn't know their soil?",
        "What if soil testing wasn't slow, expensive, or restricted by geography?",
        "Soil AI turns these 'What Ifs' into 'What Is' by democratizing complex agricultural data."
    ]
    for line in quote:
        pdf.multi_cell(0, 10, line)
        pdf.ln(5)

    # 3. Problems
    pdf.add_page()
    pdf.set_fill_color(*bg_color)
    pdf.rect(0, 0, 210, 297, 'F')
    
    pdf.ln(20)
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(*primary_color)
    pdf.cell(0, 15, "Critical Agricultural Pain Points", ln=True)
    
    pdf.ln(10)
    problems = [
        ("Farming by Guesswork", "Crops chosen without data lead to 40% yield loss and resource waste."),
        ("Zero Rural Access", "Remote farming hubs lack soil laboratories and expensive consultations."),
        ("The 'Time Gap'", "Traditional lab reports take 2-3 weeks; Soil AI takes 5 seconds."),
        ("Financial Barrier", "Testing costs are too high for 90% of smallholder farmers.")
    ]
    for title, desc in problems:
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(*primary_color)
        pdf.cell(0, 10, f"- {title}", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.set_text_color(*text_white)
        pdf.multi_cell(0, 7, desc)
        pdf.ln(5)

    # 4. Solutions (Updated with new features)
    pdf.add_page()
    pdf.set_fill_color(*bg_color)
    pdf.rect(0, 0, 210, 297, 'F')
    
    pdf.ln(20)
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(*primary_color)
    pdf.cell(0, 15, "The Intelligence Solution", ln=True)
    
    solutions = [
        ("Nano-Scale Classification", "Instant soil ID from a single photo using state-of-the-art YOLO models."),
        ("Precision Advisory", "Dynamic crop recommendations, fertilizer schedules, and seasonal planning."),
        ("Longitudinal Health Records", "Cloud-stored history for smarter long-term soil management."),
        ("Interoperable Ecosystem", "Premium API support for B2B agricultural integrations and smart-tractors.")
    ]
    for title, desc in solutions:
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(*primary_color)
        pdf.cell(0, 10, f"> {title}", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.set_text_color(*text_white)
        pdf.multi_cell(0, 7, desc)
        pdf.ln(5)

    # 5. Demo / Proof (Updated Stats)
    pdf.add_page()
    pdf.set_fill_color(*bg_color)
    pdf.rect(0, 0, 210, 297, 'F')
    
    pdf.ln(20)
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(*primary_color)
    pdf.cell(0, 15, "Validation and Performance", ln=True)
    
    pdf.set_font("Arial", '', 14)
    pdf.set_text_color(*text_white)
    pdf.ln(10)
    proof_text = (
        "We have evolved from a prototype to a precision engine.\n\n"
        "- Accuracy: 94.2% Verified across diverse soil textures.\n"
        "- Dataset: Trained on 10,000+ high-fidelity soil samples.\n"
        "- Speed: Real-time analysis in under 5 seconds using optimized edge models.\n"
        "- Trust: Validated with real-world pilot tests and diverse geography."
    )
    pdf.multi_cell(0, 10, proof_text)

    # 6. Business Model (Updated with Plans)
    pdf.add_page()
    pdf.set_fill_color(*bg_color)
    pdf.rect(0, 0, 210, 297, 'F')
    
    pdf.ln(20)
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(*primary_color)
    pdf.cell(0, 15, "SaaS Ecosystem & Business Model", ln=True)
    
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(*text_white)
    pdf.ln(5)
    pdf.multi_cell(0, 8, "Operating as a B2B2C Hybrid Platform targeting the $22B Global AgTech Market.")
    
    plans = [
        ("Basic", "Free access for small farmers for essential diagnostics."),
        ("Professional", "Tiered subscription for high-value crops and historical tracking."),
        ("Enterprise / API", "B2B partnerships for Agri-input suppliers and Smart Irrigation firms.")
    ]
    for p_name, p_desc in plans:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 13)
        pdf.set_text_color(*primary_color)
        pdf.cell(0, 10, f"Plan: {p_name}", ln=True)
        pdf.set_font("Arial", '', 11)
        pdf.set_text_color(*text_white)
        pdf.multi_cell(0, 6, p_desc)

    # 7. Closing & Team
    pdf.add_page()
    pdf.set_fill_color(*bg_color)
    pdf.rect(0, 0, 210, 297, 'F')
    
    pdf.ln(30)
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(*primary_color)
    pdf.cell(0, 15, "Meet the Core Team", ln=True, align='C')
    
    teams = [
        "Tooba Rani - Software Developer",
        "Ahad Ali Mughal - Lead AI / ML Engineer",
        "Azka Fatima - Team Coordinator",
        "Aysia Parween - Software Developer"
    ]
    pdf.ln(10)
    pdf.set_font("Arial", '', 14)
    pdf.set_text_color(*text_white)
    for member in teams:
        pdf.cell(0, 10, member, ln=True, align='C')
        
    pdf.ln(30)
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(*primary_color)
    pdf.cell(0, 15, "Join the Revolution.", ln=True, align='C')
    
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(*text_white)
    pdf.cell(0, 10, "Contact: +92 3182110366 | ahad.ai@outlook.com", ln=True, align='C')

    pdf.output("Soil_AI_OFFICIAL_Pitch_UPDATED.pdf")
    print("Updated Official PDF generated.")

if __name__ == "__main__":
    create_updated_pitch()
