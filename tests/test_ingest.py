from exam_gen.ingest import chunk_text, parse_pdf
import os


def test_parse_pdf(tmp_path):
    pdf_path = tmp_path / 'sample.pdf'
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.cell(200, 10, txt='Terraform uses HCL', ln=1)
    pdf.output(str(pdf_path))
    text = parse_pdf(str(pdf_path))
    assert 'Terraform' in text
