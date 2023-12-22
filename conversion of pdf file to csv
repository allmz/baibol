import PyPDF2
import pandas as pd
import argparse

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            text = [reader.pages[i].extract_text() for i in range(num_pages)]
        return '\n'.join(text)
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None

def process_text_to_csv(text, csv_path):
    if text:
        lines = text.split('\n')
        rows = [line.split('\t') for line in lines if line] 

        df = pd.DataFrame(rows[1:], columns=rows[0])
        df.to_csv(csv_path, index=False)
    else:
        print("No text to process.")

def main():
    parser = argparse.ArgumentParser(description="Extract text from PDF and convert to CSV")
    parser.add_argument("pdf_path", type=str, help="Path to the PDF file")
    parser.add_argument("csv_path", type=str, help="Path for the output CSV file")

    args = parser.parse_args()

    text = extract_text_from_pdf(args.pdf_path)
    process_text_to_csv(text, args.csv_path)

if __name__ == "__main__":
    main()
