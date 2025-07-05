# report_generator.py
import csv
from datetime import datetime
from fpdf import FPDF
import statistics

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Data Analysis Report', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1)
        self.ln(4)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, body)
        self.ln()

    def add_table(self, headers, data):
        self.set_font('Arial', 'B', 10)
        col_width = self.w / (len(headers) + 1)
        
        # Headers
        for header in headers:
            self.cell(col_width, 7, header, border=1)
        self.ln()
        
        # Data
        self.set_font('Arial', '', 10)
        for row in data:
            for item in row:
                self.cell(col_width, 6, str(item), border=1)
            self.ln()

def read_data(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def analyze_data(data):
    if not data:
        return {}
    
    numeric_fields = []
    for field in data[0].keys():
        try:
            float(data[0][field])
            numeric_fields.append(field)
        except ValueError:
            pass
    
    analysis = {}
    for field in numeric_fields:
        values = [float(row[field]) for row in data]
        analysis[field] = {
            'count': len(values),
            'mean': statistics.mean(values),
            'median': statistics.median(values),
            'stdev': statistics.stdev(values) if len(values) > 1 else 0,
            'min': min(values),
            'max': max(values)
        }
    
    return analysis

def generate_report(input_file, output_file):
    # Read and analyze data
    data = read_data(input_file)
    analysis = analyze_data(data)
    
    # Create PDF
    pdf = PDFReport()
    pdf.add_page()
    
    # Report title
    pdf.chapter_title(f'Data Analysis Report: {input_file}')
    
    # Data summary
    pdf.chapter_body(f"The dataset contains {len(data)} records with {len(data[0]) if data else 0} fields each.")
    
    # Show sample data
    pdf.chapter_title('Sample Data (First 5 Rows)')
    sample_data = [list(data[0].keys())]  # Headers
    sample_data += [list(row.values()) for row in data[:5]]  # First 5 rows
    pdf.add_table(headers=[], data=sample_data)
    
    # Analysis results
    if analysis:
        pdf.chapter_title('Statistical Analysis')
        for field, stats in analysis.items():
            pdf.chapter_body(
                f"Field: {field}\n"
                f"- Count: {stats['count']}\n"
                f"- Mean: {stats['mean']:.2f}\n"
                f"- Median: {stats['median']:.2f}\n"
                f"- Standard Deviation: {stats['stdev']:.2f}\n"
                f"- Range: {stats['min']:.2f} to {stats['max']:.2f}\n"
            )
    else:
        pdf.chapter_body("No numeric fields found for statistical analysis.")
    
    # Save PDF
    pdf.output(output_file)
    print(f"Report generated successfully: {output_file}")

if __name__ == "__main__":
    # Example usage
    input_csv = "sales_data.csv"  # Replace with your file
    output_pdf = "analysis_report.pdf"
    
    # Create sample data file if it doesn't exist
    try:
        with open(input_csv, 'r') as f:
            pass
    except FileNotFoundError:
        print(f"Creating sample {input_csv} file...")
        with open(input_csv, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['Date', 'Product', 'Units', 'Revenue'])
            writer.writeheader()
            writer.writerows([
                {'Date': '2023-01-01', 'Product': 'A', 'Units': '10', 'Revenue': '1000'},
                {'Date': '2023-01-02', 'Product': 'B', 'Units': '15', 'Revenue': '1800'},
                {'Date': '2023-01-03', 'Product': 'A', 'Units': '8', 'Revenue': '800'},
                {'Date': '2023-01-04', 'Product': 'C', 'Units': '20', 'Revenue': '3000'},
                {'Date': '2023-01-05', 'Product': 'B', 'Units': '12', 'Revenue': '1440'},
                {'Date': '2023-01-06', 'Product': 'A', 'Units': '5', 'Revenue': '500'},
            ])
    
    generate_report(input_csv, output_pdf)