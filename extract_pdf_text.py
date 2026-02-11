import PyPDF2

def extract_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n--- PAGE BREAK ---\n"
    return text

if __name__ == "__main__":
    try:
        content = extract_text('Soil AI Analyzer pitch deck.pdf')
        with open('old_pitch_text.txt', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Text extracted successfully.")
    except Exception as e:
        print(f"Error: {e}")
