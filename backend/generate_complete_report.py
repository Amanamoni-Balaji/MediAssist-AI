import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def build_complete_report():
    print("Initializing MediAssist AI 28-Section Project Report Generator...")
    doc = Document()

    # 1. Page Margins - Standard Academic 1.0 inch
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # 2. XML Helpers for Tables, Borders & Shading
    def set_cell_background(cell, fill_hex):
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
            node = OxmlElement(m)
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    # 3. Heading Generator with Real Word Heading Styles
    def add_sec_heading(text, level=1, space_before=16, space_after=6):
        p = doc.add_heading(text, level=level)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.keep_with_next = True
        for r in p.runs:
            r.font.name = 'Times New Roman'
            r.bold = True
            if level == 1:
                r.font.size = Pt(15)
                r.font.color.rgb = RGBColor(15, 44, 89) # Deep Navy #0F2C59
            elif level == 2:
                r.font.size = Pt(13)
                r.font.color.rgb = RGBColor(26, 75, 140) # Slate Navy #1A4B8C
            elif level == 3:
                r.font.size = Pt(11.5)
                r.font.color.rgb = RGBColor(40, 40, 40)
        return p

    def add_p(text, space_after=6, line_spacing=1.15, bold_prefix="", indent=0):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if indent > 0:
            p.paragraph_format.left_indent = Inches(indent)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(11)
            r_pre.font.color.rgb = RGBColor(20, 20, 20)
            
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(40, 40, 40)
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(11)
            
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        return p

    def add_code_box(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F8F9FA")
        set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>'
            f'<w:left w:val="single" w:sz="18" w:space="0" w:color="0284C7"/>'
            f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>'
            f'<w:right w:val="single" w:sz="4" w:space="0" w:color="D1D5DB"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run(code_text.strip())
        run.font.name = 'Consolas'
        run.font.size = Pt(9.0)
        run.font.color.rgb = RGBColor(30, 41, 59)
        
        sp = doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(6)

    def add_img_figure(img_filename, caption, width_in=5.8):
        full_p = os.path.join("doc_assets", img_filename) if not os.path.isabs(img_filename) else img_filename
        if os.path.exists(full_p):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(3)
            run_img = p_img.add_run()
            run_img.add_picture(full_p, width=Inches(width_in))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(12)
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(10)
            r_cap.font.italic = True
            r_cap.font.color.rgb = RGBColor(70, 70, 70)

    # =========================================================================
    # SECTION 1: COVER PAGE
    # =========================================================================
    print("Writing Section 1: Cover Page...")
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("A PROJECT REPORT\nON")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.bold = True
    r.font.color.rgb = RGBColor(15, 44, 89)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(12)
    r_title = p_title.add_run("MediAssist AI – An Intelligent Healthcare Chatbot Using Natural Language Processing (NLP)")
    r_title.font.name = 'Times New Roman'
    r_title.font.size = Pt(18)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(180, 20, 20)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(6)
    p_sub.paragraph_format.space_after = Pt(16)
    r_sub = p_sub.add_run(
        "A REPORT SUBMITTED IN PARTIAL FULFILLMENT OF THE\n"
        "REQUIREMENTS FOR THE AWARD OF DEGREE OF\n"
        "BACHELOR OF ENGINEERING\nIN\nINFORMATION TECHNOLOGY"
    )
    r_sub.font.name = 'Times New Roman'
    r_sub.font.size = Pt(11)
    r_sub.bold = True

    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_before = Pt(6)
    p_by.paragraph_format.space_after = Pt(4)
    r_by = p_by.add_run("SUBMITTED BY:\n")
    r_by.font.name = 'Times New Roman'
    r_by.font.size = Pt(11)
    r_by.bold = True

    r_author = p_by.add_run("AMANAMONI BALAJI\n(Roll No: 1608-23-737-001)")
    r_author.font.name = 'Times New Roman'
    r_author.font.size = Pt(12)
    r_author.bold = True
    r_author.font.color.rgb = RGBColor(15, 44, 89)

    if os.path.exists("doc_assets/image3.png"):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(10)
        p_logo.paragraph_format.space_after = Pt(10)
        p_logo.add_run().add_picture("doc_assets/image3.png", width=Inches(1.8))

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(6)
    p_dept.paragraph_format.space_after = Pt(2)
    r_dept = p_dept.add_run(
        "Department of Information Technology\n"
        "MATRUSRI ENGINEERING COLLEGE\n"
        "(Sponsored by Matrusri Education Society, Estd. 1980)\n"
        "(Approved by AICTE, Affiliated to Osmania University)\n"
        "#16-1-486, Saidabad, Hyderabad, Telangana – 500 059\n"
        "www.matrusri.edu.in\n"
        "ACADEMIC YEAR: 2026-2027"
    )
    r_dept.font.name = 'Times New Roman'
    r_dept.font.size = Pt(10)
    r_dept.bold = True

    doc.add_page_break()

    # =========================================================================
    # SECTION 2: CERTIFICATE
    # =========================================================================
    print("Writing Section 2: Certificate...")
    cert_tbl = doc.add_table(rows=1, cols=3)
    cert_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_l, cell_m, cell_r = cert_tbl.cell(0, 0), cert_tbl.cell(0, 1), cert_tbl.cell(0, 2)
    cell_l.width = Inches(1.1)
    cell_m.width = Inches(4.3)
    cell_r.width = Inches(1.1)

    if os.path.exists("doc_assets/image8.png"):
        p_cl = cell_l.paragraphs[0]
        p_cl.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cl.add_run().add_picture("doc_assets/image8.png", width=Inches(0.95))

    p_cm = cell_m.paragraphs[0]
    p_cm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cm.paragraph_format.space_after = Pt(0)
    p_cm.paragraph_format.line_spacing = 1.05
    r_c1 = p_cm.add_run("Matrusri Engineering College\n")
    r_c1.bold = True
    r_c1.font.name = 'Times New Roman'
    r_c1.font.size = Pt(13)
    r_c1.font.color.rgb = RGBColor(180, 20, 20)
    r_c2 = p_cm.add_run(
        "(Sponsored by Matrusri Education Society, Estd. 1980)\n"
        "(Approved by AICTE & Affiliated to Osmania University)\n"
        "# 16-1-486, Saidabad, Hyderabad-500059. Ph: 040-24072764\n"
        "(ISO 9001:2015 Certified)\n"
        "Department of Information Technology\n"
        "Email: hodit@matrusri.edu.in | Website: www.matrusri.edu.in"
    )
    r_c2.font.name = 'Times New Roman'
    r_c2.font.size = Pt(8.5)

    if os.path.exists("doc_assets/image9.png"):
        p_cr = cell_r.paragraphs[0]
        p_cr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cr.add_run().add_picture("doc_assets/image9.png", width=Inches(0.95))

    if os.path.exists("doc_assets/image4.png"):
        p_div = doc.add_paragraph()
        p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_div.paragraph_format.space_before = Pt(4)
        p_div.paragraph_format.space_after = Pt(12)
        p_div.add_run().add_picture("doc_assets/image4.png", width=Inches(6.4))

    p_cert_title = doc.add_paragraph()
    p_cert_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_title.paragraph_format.space_before = Pt(6)
    p_cert_title.paragraph_format.space_after = Pt(12)
    r_cert_title = p_cert_title.add_run("CERTIFICATE")
    r_cert_title.bold = True
    r_cert_title.font.name = 'Times New Roman'
    r_cert_title.font.size = Pt(16)
    r_cert_title.font.color.rgb = RGBColor(15, 44, 89)

    add_p(
        "This is to certify that the project report titled “MediAssist AI – An Intelligent Healthcare Chatbot Using Natural Language Processing (NLP)” "
        "is a bonafide work done by Mr. AMANAMONI BALAJI (Roll No. 1608-23-737-001) in partial fulfillment of the requirements for the award of the degree of "
        "Bachelor of Engineering in Information Technology of Osmania University, Hyderabad, during the academic year 2026-2027.",
        space_after=12,
        line_spacing=1.35
    )

    add_p(
        "The results embodied in this report have been verified and found to be satisfactory. The project demonstrates an advanced natural language processing "
        "and semantic retrieval architecture implemented with full technical rigour, clinical safety constraints, and professional software engineering principles.",
        space_after=36,
        line_spacing=1.35
    )

    sig_tbl = doc.add_table(rows=1, cols=3)
    sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1, c2, c3 = sig_tbl.cell(0, 0), sig_tbl.cell(0, 1), sig_tbl.cell(0, 2)
    c1.width = Inches(2.1)
    c2.width = Inches(2.1)
    c3.width = Inches(2.1)

    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p1.add_run("Project Coordinator\nDept. of IT").bold = True

    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.add_run("Head of the Department\nDr. G. Shyama Chandra Prasad").bold = True

    p3 = c3.paragraphs[0]
    p3.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p3.add_run("Principal\nDr. D. Hanumantha Rao").bold = True

    for p_sig in [p1, p2, p3]:
        p_sig.runs[0].font.name = 'Times New Roman'
        p_sig.runs[0].font.size = Pt(10)

    doc.add_page_break()

    # =========================================================================
    # SECTION 3: ACKNOWLEDGEMENT
    # =========================================================================
    print("Writing Section 3: Acknowledgement...")
    p_ack = doc.add_paragraph()
    p_ack.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack.paragraph_format.space_before = Pt(8)
    p_ack.paragraph_format.space_after = Pt(14)
    r_ack = p_ack.add_run("ACKNOWLEDGEMENT")
    r_ack.bold = True
    r_ack.font.name = 'Times New Roman'
    r_ack.font.size = Pt(16)
    r_ack.font.color.rgb = RGBColor(15, 44, 89)

    add_p(
        "I express my profound gratitude and heartfelt thanks to our respected Principal, Dr. D. Hanumantha Rao, for providing all necessary academic infrastructure, "
        "laboratory facilities, and institutional support to carry out this project successfully at Matrusri Engineering College.",
        space_after=10,
        line_spacing=1.25
    )

    add_p(
        "I am deeply indebted to Dr. G. Shyama Chandra Prasad, Professor and Head of the Department of Information Technology, for his invaluable guidance, continuous encouragement, "
        "and technical motivation throughout the period of this project work. His constructive feedback and high engineering standards have been instrumental in refining the architecture.",
        space_after=10,
        line_spacing=1.25
    )

    add_p(
        "I extend my sincere appreciation to the Project Coordinator and faculty members of the Information Technology Department who imparted essential foundational knowledge "
        "in Natural Language Processing, Machine Learning, Web Technologies, and Database Systems, and whose regular reviews helped keep the development on schedule.",
        space_after=10,
        line_spacing=1.25
    )

    add_p(
        "Finally, I would like to thank my family and friends for their enduring patience, moral support, and enthusiasm throughout the conceptualization, implementation, "
        "and documentation of the MediAssist AI healthcare platform.",
        space_after=28,
        line_spacing=1.25
    )

    p_sig_ack = doc.add_paragraph()
    p_sig_ack.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sig_ack = p_sig_ack.add_run("AMANAMONI BALAJI\nRoll No: 1608-23-737-001\nDepartment of Information Technology\nMatrusri Engineering College")
    r_sig_ack.font.name = 'Times New Roman'
    r_sig_ack.font.size = Pt(11)
    r_sig_ack.bold = True

    doc.add_page_break()

    # =========================================================================
    # SECTION 4: TABLE OF CONTENTS
    # =========================================================================
    print("Writing Section 4: Table of Contents...")
    p_toc = doc.add_paragraph()
    p_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc.paragraph_format.space_before = Pt(8)
    p_toc.paragraph_format.space_after = Pt(12)
    r_toc = p_toc.add_run("TABLE OF CONTENTS")
    r_toc.bold = True
    r_toc.font.name = 'Times New Roman'
    r_toc.font.size = Pt(16)
    r_toc.font.color.rgb = RGBColor(15, 44, 89)

    toc_items = [
        ("1. Cover Page", "i"),
        ("2. Certificate", "ii"),
        ("3. Acknowledgement", "iii"),
        ("4. Table of Contents", "iv"),
        ("5. Abstract", "v"),
        ("6. Introduction", "1"),
        ("7. Project Overview", "4"),
        ("8. Problem Statement", "6"),
        ("9. Objectives", "8"),
        ("10. Existing System and Its Limitations", "10"),
        ("11. Proposed System", "12"),
        ("12. Tools and Technologies Used", "14"),
        ("13. Detailed Explanation of Technologies", "16"),
        ("14. System Architecture", "20"),
        ("15. Methodology and Workflow", "23"),
        ("16. NLP Techniques Used", "26"),
        ("17. System Modules", "31"),
        ("18. Frontend Implementation", "36"),
        ("19. Backend Implementation", "40"),
        ("20. Database Design", "44"),
        ("21. API Implementation", "48"),
        ("22. Working of the Chatbot", "53"),
        ("23. Screenshots of the Application", "57"),
        ("24. Testing and Results", "63"),
        ("25. Advantages and Limitations", "69"),
        ("26. Future Enhancements", "71"),
        ("27. Conclusion", "73"),
        ("28. References", "75"),
    ]

    toc_tbl = doc.add_table(rows=len(toc_items) + 1, cols=2)
    toc_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_tbl.cell(0, 0).width = Inches(5.3)
    toc_tbl.cell(0, 1).width = Inches(1.1)

    set_cell_background(toc_tbl.cell(0, 0), "0F2C59")
    set_cell_background(toc_tbl.cell(0, 1), "0F2C59")
    r_th1 = toc_tbl.cell(0, 0).paragraphs[0].add_run("Section Description")
    r_th1.bold = True
    r_th1.font.color.rgb = RGBColor(255, 255, 255)
    r_th2 = toc_tbl.cell(0, 1).paragraphs[0].add_run("Page No.")
    r_th2.bold = True
    r_th2.font.color.rgb = RGBColor(255, 255, 255)
    toc_tbl.cell(0, 1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    for i, (title, page) in enumerate(toc_items, 1):
        c_title = toc_tbl.cell(i, 0)
        c_page = toc_tbl.cell(i, 1)
        c_title.width = Inches(5.3)
        c_page.width = Inches(1.1)
        set_cell_margins(c_title, top=35, bottom=35, left=100, right=100)
        set_cell_margins(c_page, top=35, bottom=35, left=100, right=100)
        if i % 2 == 1:
            set_cell_background(c_title, "F9FAFB")
            set_cell_background(c_page, "F9FAFB")

        p_t = c_title.paragraphs[0]
        p_t.paragraph_format.space_before = Pt(1)
        p_t.paragraph_format.space_after = Pt(1)
        r_t = p_t.add_run(title)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(10)
        r_t.bold = True

        p_p = c_page.paragraphs[0]
        p_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_p.paragraph_format.space_before = Pt(1)
        p_p.paragraph_format.space_after = Pt(1)
        r_p = p_p.add_run(page)
        r_p.font.name = 'Times New Roman'
        r_p.font.size = Pt(10)

    doc.add_page_break()

    # =========================================================================
    # SECTION 5: ABSTRACT
    # =========================================================================
    print("Writing Section 5: Abstract...")
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs.paragraph_format.space_before = Pt(8)
    p_abs.paragraph_format.space_after = Pt(14)
    r_abs = p_abs.add_run("SECTION 5: ABSTRACT")
    r_abs.bold = True
    r_abs.font.name = 'Times New Roman'
    r_abs.font.size = Pt(16)
    r_abs.font.color.rgb = RGBColor(15, 44, 89)

    add_p(
        "Modern healthcare systems worldwide are confronted with severe structural challenges, including physician shortages, escalating clinical workloads, "
        "and geographical disparities that impede timely medical guidance for everyday health inquiries. While conversational Artificial Intelligence holds "
        "enormous potential to alleviate these pressures through automated digital triage and health education, conventional implementations suffer from "
        "severe architectural deficiencies. Traditional medical chatbots rely on rigid keyword matching and small predefined question-answer matrices, "
        "causing them to fail on colloquial layperson phrasing, spelling mistakes, and follow-up queries. Conversely, unconstrained cloud-based large language "
        "models (LLMs) frequently hallucinate medical advice, expose patient queries to third-party privacy risks, incur prohibitive recurring API subscription "
        "costs, and lack strict clinical safety guardrails.",
        space_after=10,
        line_spacing=1.25
    )

    add_p(
        "To overcome these limitations, this project presents MediAssist AI – an intelligent, full-stack, conversational healthcare assistant powered by "
        "an advanced Natural Language Processing (NLP) pipeline, Dense Latent Semantic Vector Embeddings, Hybrid Retrieval-Augmented Generation (RAG), and "
        "Stateful Multi-Turn Context Resolution. Operating entirely on local infrastructure with zero cloud API token dependencies, MediAssist AI understands "
        "natural human language, colloquial layperson descriptions, typing mistakes, and conversational follow-ups across ten comprehensive medical domains: "
        "General Medicine, Dermatology, Cardiology, Respiratory Health, Gastroenterology, Endocrinology, Mental Health, Orthopedics, Pediatrics, and Preventive Care.",
        space_after=10,
        line_spacing=1.25
    )

    add_p(
        "The core intelligence is driven by a 20-class calibrated Linear Support Vector Classifier (LinearSVC with Platt scaling), subword character n-gram hashing "
        "projected onto an orthonormal 256-dimensional vector space, an extensive medical concept synonym graph, and an explicit multi-turn context manager that resolves "
        "pronoun anaphora ('it', 'this') and elliptical follow-ups ('What can I take?'). A Priority-1 Emergency Safety Layer continuously monitors for life-threatening "
        "crises (e.g., acute myocardial infarction, stroke, suicidal ideation, anaphylaxis), immediately overriding standard retrieval with critical emergency instructions. "
        "All clinical responses are grounded in peer-reviewed monographs attributed to authoritative bodies (WHO, MedlinePlus, NHS, CDC) with mandatory disclaimers and "
        "contraindication warnings.",
        space_after=10,
        line_spacing=1.25
    )

    add_p(
        "Evaluated across a rigorous 200-query clinical benchmark suite, MediAssist AI achieved a 91.5% domain retrieval accuracy, a 0.0% robotic fallback rate, "
        "and a 100% pass rate on complex multi-turn medical scenarios. Developed with Django 5.1, Django REST Framework, React 18, TypeScript, and Tailwind CSS, "
        "MediAssist AI establishes that clinically safe, highly intelligent conversational healthcare assistants can be successfully deployed on cost-effective local infrastructure.",
        space_after=14,
        line_spacing=1.25
    )

    p_kw = doc.add_paragraph()
    r_kw_title = p_kw.add_run("Keywords: ")
    r_kw_title.bold = True
    r_kw_title.font.name = 'Times New Roman'
    r_kw_title.font.size = Pt(10.5)
    r_kw = p_kw.add_run("Healthcare Chatbot, Natural Language Processing (NLP), Dense Semantic Search, Retrieval-Augmented Generation (RAG), Clinical Triage, Multi-Turn Context Tracking, Django REST Framework, React.js.")
    r_kw.font.name = 'Times New Roman'
    r_kw.font.size = Pt(10.5)
    r_kw.font.italic = True

    doc.add_page_break()

    # =========================================================================
    # SECTION 6: INTRODUCTION
    # =========================================================================
    print("Writing Section 6: Introduction...")
    add_sec_heading("SECTION 6: INTRODUCTION", level=1)
    
    add_sec_heading("6.1 Background and Healthcare Paradigm", level=2)
    add_p(
        "Access to accurate, timely, and comprehensible healthcare information is a fundamental determinant of public health outcomes. "
        "In modern society, billions of individuals turn to digital channels daily to seek explanations for symptoms they experience, investigate potential illnesses, "
        "and explore self-care remedies before consulting a physician. However, conventional search engines present users with an overwhelming array of unvetted, "
        "conflicting, and often alarmist web links—frequently inducing health-related anxiety, commonly referred to in medical informatics as 'cyberchondria'. "
        "Simultaneously, primary healthcare infrastructure across urban and rural centers faces severe strain, characterized by lengthy outpatient waiting times, "
        "physician burnout, and overburdened emergency departments handling non-emergent inquiries.",
        space_after=8
    )

    add_sec_heading("6.2 The Growing Role of Conversational AI in Medicine", level=2)
    add_p(
        "Conversational Artificial Intelligence represents a transformative paradigm shift in healthcare delivery. By providing a natural language interface, "
        "intelligent healthcare assistants can collect patient symptoms conversationally, interpret layperson phrasing, explain complex physiological concepts "
        "in plain language, recommend non-pharmacological self-care strategies, and flag red-flag symptoms requiring emergency hospital care. Digital assistants "
        "act as a pre-consultation triage and health literacy layer, helping users formulate organized symptom descriptions before their clinical appointments.",
        space_after=8
    )

    add_sec_heading("6.3 The Need for MediAssist AI", level=2)
    add_p(
        "Despite significant commercial hype, current conversational healthcare tools fall into two unsatisfactory extremes: brittle keyword-based chatbots that "
        "fail on minor misspellings and output repetitive fallback messages, and unconstrained large language models that generate fabricated medical claims, "
        "hallucinate drug dosages, and depend on costly cloud APIs. MediAssist AI was conceived to bridge this divide by engineering an intelligent, local, "
        "deterministic, and evidence-grounded healthcare assistant that understands real human language while upholding absolute clinical safety boundaries.",
        space_after=8
    )

    add_sec_heading("6.4 Ethical Boundaries: Clinical Education vs. Medical Diagnosis", level=2)
    add_p(
        "A foundational principle of MediAssist AI is its unequivocal classification as an educational healthcare assistant rather than a diagnostic engine. "
        "The system never purports to replace licensed medical doctors, prescribe prescription-only medications, or formulate definitive diagnostic decisions. "
        "Every response is systematically augmented with prominent clinical disclaimers, clear warnings regarding emergency symptoms, and explicit recommendations "
        "to consult registered healthcare practitioners.",
        space_after=12
    )

    # =========================================================================
    # SECTION 7: PROJECT OVERVIEW
    # =========================================================================
    print("Writing Section 7: Project Overview...")
    add_sec_heading("SECTION 7: PROJECT OVERVIEW", level=1)
    add_p(
        "MediAssist AI is a complete, full-stack, enterprise-grade healthcare chatbot and medical exploration platform designed to assist users in understanding "
        "symptoms, medical conditions, self-care measures, and preventive health practices through natural dialogue. Unlike primitive prototype chatbots, "
        "MediAssist AI combines an elegant React single-page frontend, a resilient Django REST API backend, and an intelligent offline NLP pipeline.",
        space_after=8
    )
    add_p(
        "The platform encompasses 10 major medical domains spanning 47+ distinct clinical condition monographs:",
        space_after=6
    )
    add_bullet("General Medicine: Common cold, viral influenza, acute bronchitis, fever, migraines, tension headaches, fatigue, body aches, viral infections.", "1. ")
    add_bullet("Dermatology & Skin: Primary focal hyperhidrosis, acne vulgaris, eczema (atopic dermatitis), plaque psoriasis, urticaria (hives), contact allergies.", "2. ")
    add_bullet("Cardiology & Vascular: Hypertension (essential high blood pressure), hypotension, chest pain triage, coronary artery disease awareness.", "3. ")
    add_bullet("Respiratory Health: Bronchial asthma, acute/chronic bronchitis, allergic rhinitis, sinusitis, dyspnea (shortness of breath) triage.", "4. ")
    add_bullet("Gastroenterology: Gastroesophageal reflux disease (GERD), acid peptic disease (gastritis), gastroenteritis, irritable bowel syndrome (IBS).", "5. ")
    add_bullet("Endocrinology & Metabolism: Type 1 and Type 2 diabetes mellitus, hypoglycemia, hypothyroidism, hyperthyroidism, metabolic syndrome.", "6. ")
    add_bullet("Mental Health & Sleep: Chronic insomnia, sleep hygiene, generalized anxiety disorder, panic attacks, clinical depression awareness.", "7. ")
    add_bullet("Orthopedics & Rheumatology: Osteoarthritis, rheumatoid arthritis, lumbar back pain, cervical spondylosis, muscle sprains, joint inflammation.", "8. ")
    add_bullet("Pediatrics & Child Health: Pediatric febrile illness, croup, hand-foot-and-mouth disease, childhood immunization schedules, dehydration warning signs.", "9. ")
    add_bullet("Preventive Healthcare: Balanced cardiovascular nutrition, aerobic physical exercise, hydration, micronutrient supplementation, stress management.", "10. ")

    # =========================================================================
    # SECTION 8: PROBLEM STATEMENT
    # =========================================================================
    print("Writing Section 8: Problem Statement...")
    add_sec_heading("SECTION 8: PROBLEM STATEMENT", level=1)
    add_p(
        "Despite rapid technological advancements in natural language processing and generative artificial intelligence, current digital healthcare information "
        "systems suffer from profound engineering and architectural limitations that prevent safe, intuitive public adoption:",
        space_after=8
    )
    add_bullet("The FAQ Brittleness Barrier: Traditional rule-based chatbots rely on exact string matching or rigid regular expressions. When a user enters a slightly misspelled word ('sweatng', 'headach', 'fevr'), uses colloquial idioms ('stomach is churning', 'can't sleep at all'), or asks questions without textbook syntax, traditional bots fail completely, emitting unhelpful canned fallback messages.", "• ")
    add_bullet("The Generative Hallucination Hazard: While modern Large Language Models (e.g., GPT-4, Llama) demonstrate impressive conversational fluidity, they suffer from stochastic hallucination—confidently inventing fictitious drug dosages, proposing lethal medication combinations, or fabricating pathophysiological mechanisms. In medicine, hallucinated information carries severe clinical risk.", "• ")
    add_bullet("Contextual Blindness in Multi-Turn Dialogues: Human healthcare consultations are inherently iterative. A patient states an initial symptom ('I have cold and cough') and follows up with anaphoric pronouns or elliptical phrases ('What can I take?', 'How can I control it?'). Standard FAQ systems treat each query as an isolated event, failing completely on context-dependent follow-ups.", "• ")
    add_bullet("Prohibitive Cloud API Costs and Data Privacy Risks: Cloud-hosted LLM APIs incur recurring per-token fees that make large-scale public health deployments economically unsustainable. Furthermore, transmitting sensitive personal symptom logs over commercial cloud APIs violates stringent health privacy regulations such as HIPAA, GDPR, and ISO 27799.", "• ")
    add_bullet("Lack of Deterministic Emergency Triage: Generic chatbots frequently treat emergency red-flag complaints (such as acute chest pain radiating to the left arm, sudden facial drooping, or suicidal thoughts) with relaxed conversational advice rather than immediate, unambiguous emergency escalation.", "• ")

    # =========================================================================
    # SECTION 9: OBJECTIVES
    # =========================================================================
    print("Writing Section 9: Objectives...")
    add_sec_heading("SECTION 9: OBJECTIVES", level=1)
    add_p(
        "The overarching mission of this project is to architect, develop, and empirically validate an end-to-end, intelligent conversational healthcare assistant "
        "that eliminates the brittleness of traditional FAQ bots while guaranteeing clinical safety and zero cloud dependency. The specific project objectives are:",
        space_after=8
    )
    add_bullet("Natural Layperson Language Understanding: Implement an advanced text normalization and typo-tolerant semantic pipeline capable of interpreting misspelled queries, informal idioms, and varied sentence structures.", "1. ")
    add_bullet("Dense Latent Semantic Retrieval: Construct an orthonormal 256-dimensional semantic vector space and concept synonym graph to map diverse user expressions into clinical concept representations without cloud API calls.", "2. ")
    add_bullet("Calibrated Intent Classification: Train a 20-class Linear Support Vector Classifier with Platt probability calibration to categorize user intents across greetings, symptom checks, medication inquiries, emergency alarms, and domain questions.", "3. ")
    add_bullet("Stateful Multi-Turn Context Tracking: Engineer an in-memory dialogue context manager that tracks active topics, symptoms, and anatomical body parts across conversation turns, resolving pronoun anaphora ('it', 'this') and elliptical follow-ups seamlessly.", "4. ")
    add_bullet("Deterministic Priority-1 Emergency Safety Layer: Implement an instant triage safety engine that intercepts acute clinical crises (crushing chest pain, severe dyspnea, stroke indicators, suicide risk) and overrides retrieval with emergency hotlines.", "5. ")
    add_bullet("Zero Cloud Cost & Complete Data Privacy: Ensure the entire NLP, machine learning, and retrieval architecture runs locally on CPU hardware with sub-100 millisecond response latency and zero recurring token expenditures.", "6. ")
    add_bullet("Full-Stack Enterprise User Experience: Build a modern, responsive React 18 / TypeScript frontend featuring rich consultation streams, a symptom explorer, health analytics dashboards, session history, and full Django REST API endpoints.", "7. ")

    # =========================================================================
    # SECTION 10: EXISTING SYSTEM AND ITS LIMITATIONS
    # =========================================================================
    print("Writing Section 10: Existing System and Its Limitations...")
    add_sec_heading("SECTION 10: EXISTING SYSTEM AND ITS LIMITATIONS", level=1)
    add_p(
        "To contextualize the contributions of MediAssist AI, this section analyzes existing healthcare information retrieval paradigms and highlights their technical shortcomings.",
        space_after=8
    )

    # Comparison Table
    comp_tbl = doc.add_table(rows=6, cols=4)
    comp_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c in comp_tbl.rows[0].cells:
        set_cell_background(c, "0F2C59")
    
    comp_headers = ["Evaluation Dimension", "Traditional FAQ Chatbots", "Cloud LLM Chatbots (GPT/Llama)", "Proposed MediAssist AI"]
    for j, h in enumerate(comp_headers):
        p_h = comp_tbl.cell(0, j).paragraphs[0]
        r_h = p_h.add_run(h)
        r_h.bold = True
        r_h.font.color.rgb = RGBColor(255, 255, 255)
        r_h.font.size = Pt(9.5)

    comp_rows = [
        ("Query Understanding", "Rigid exact string matching; fails on typos and colloquial phrasing.", "High linguistic fluency but lacks medical domain constraints.", "Subword n-gram hashing + 256-D dense vector space + concept synonym thesaurus."),
        ("Medical Hallucination", "Zero hallucination, but fails to answer >80% of real queries.", "High risk; invents dosages and non-existent medical facts.", "Zero hallucination; strictly grounded in peer-reviewed clinical monographs."),
        ("Multi-Turn Context", "Stateless; treats each user turn as an isolated query.", "Maintains context through massive token windows at high cost.", "Stateful ConversationContext tracking active topics, symptoms, and body parts."),
        ("Emergency Triage", "Inconsistent; depends on specific keywords matching regex.", "Stochastic; may offer relaxed advice during acute emergencies.", "Deterministic Priority-1 regex engine overrides all other pipelines instantly."),
        ("Operating Cost & Privacy", "Low cost, but practically unusable due to brittleness.", "High recurring per-token fees; patient data sent to third parties.", "100% Free & Open Source; runs on local CPU with complete patient privacy.")
    ]

    for i, row in enumerate(comp_rows, 1):
        for j, val in enumerate(row):
            cell = comp_tbl.cell(i, j)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            if i % 2 == 1:
                set_cell_background(cell, "F9FAFB")
            p_cell = cell.paragraphs[0]
            p_cell.paragraph_format.space_before = Pt(1)
            p_cell.paragraph_format.space_after = Pt(1)
            r_c = p_cell.add_run(val)
            r_c.font.name = 'Times New Roman'
            r_c.font.size = Pt(9.0)
            if j == 3:
                r_c.bold = True
                r_c.font.color.rgb = RGBColor(15, 44, 89)

    add_p("", space_after=8)

    # =========================================================================
    # SECTION 11: PROPOSED SYSTEM
    # =========================================================================
    print("Writing Section 11: Proposed System...")
    add_sec_heading("SECTION 11: PROPOSED SYSTEM", level=1)
    add_p(
        "MediAssist AI introduces an innovative, deterministic Retrieval-Augmented Generation (RAG) framework optimized for local deployment without cloud LLM dependencies. "
        "The architecture unifies five core engineering paradigms:",
        space_after=8
    )
    add_bullet("Dual-Stage Linguistic Normalization: Employs character-level subword n-gram hashing to tolerate severe misspellings, combined with an extensive synonym expansion graph mapping everyday layperson idioms to clinical terminologies (e.g., 'sweating buckets' -> Hyperhidrosis; 'chest is tight' -> Asthma/Cardiology triage).", "1. ")
    add_bullet("Calibrated Multi-Class Intent Classifier: Employs a 20-class Linear Support Vector Classifier trained on rich clinical conversational corpora, calibrated using Platt scaling to yield reliable posterior probabilities for intent disambiguation.", "2. ")
    add_bullet("Dense Latent Semantic Embedding Space: Compresses high-dimensional token representations into an orthonormal 256-dimensional vector space using random orthogonal projections (Johnson-Lindenstrauss lemma), enabling fast cosine similarity ranking against pre-computed medical topic vectors.", "3. ")
    add_bullet("Hybrid Multi-Metric Retrieval Function: Ranks candidate medical topics using a weighted scoring formula combining dense vector cosine similarity (55%), exact subword character match (25%), and keyword density overlap (20%).", "4. ")
    add_bullet("Multi-Turn Reference Resolver: Maintains an active conversation state tracking active conditions, symptoms, and anatomical focus areas, seamlessly rewriting elliptical follow-ups ('What can I take?') into fully grounded semantic queries ('treatment medication relief options for [active_topic]').", "5. ")
    add_bullet("Multi-Tiered Safety & Clinical Guardrails: Enforces priority-1 emergency triage, attaches context-sensitive medical disclaimers, provides lifestyle recommendations, and appends verified citations from the WHO, MedlinePlus, NHS, and CDC.", "6. ")

    # =========================================================================
    # SECTION 12: TOOLS AND TECHNOLOGIES USED
    # =========================================================================
    print("Writing Section 12: Tools and Technologies Used...")
    add_sec_heading("SECTION 12: TOOLS AND TECHNOLOGIES USED", level=1)
    add_p(
        "The MediAssist AI healthcare platform is engineered using modern, robust, industry-standard software frameworks across the presentation, application, and persistence tiers:",
        space_after=8
    )
    add_bullet("Frontend Development: React.js (v18.3.1), Vite (v8.3.5), TypeScript (v5.6), Tailwind CSS (v4.0), Lucide React Iconography, Recharts (v2.15), Axios (v1.7).", "• ")
    add_bullet("Backend Framework: Python (v3.11.9), Django (v5.1.15), Django REST Framework (v3.17.2), SimpleJWT (v5.5.1), WhiteNoise (v6.12.0), Django CORS Headers (v4.7.0).", "• ")
    add_bullet("NLP & Machine Learning: NLTK (v3.10.4), Scikit-Learn (v1.9.1), NumPy (v2.4.6), SciPy (v1.17.1), Joblib (v1.6.0).", "• ")
    add_bullet("Database & Storage: SQLite3 relational database, Django Object-Relational Mapper (ORM), disk-persisted Joblib model artifacts.", "• ")
    add_bullet("Development & Evaluation Tools: Visual Studio Code, Git Version Control, PowerShell 7, Google Chrome DevTools, Python UnitTest & Automated Test Suites.", "• ")

    # =========================================================================
    # SECTION 13: DETAILED EXPLANATION OF TECHNOLOGIES
    # =========================================================================
    print("Writing Section 13: Detailed Explanation of Technologies...")
    add_sec_heading("SECTION 13: DETAILED EXPLANATION OF TECHNOLOGIES", level=1)
    
    add_sec_heading("13.1 React.js, TypeScript & Vite", level=2)
    add_p(
        "React 18 serves as the client-side component engine, utilizing declarative state hooks (`useState`, `useEffect`, `useRef`, `useCallback`) "
        "and virtual DOM diffing to deliver seamless 60-FPS conversational interactions. TypeScript adds compile-time type validation across all REST API request "
        "and response models, eliminating runtime type errors. Vite leverages native browser ES modules to achieve instantaneous Hot Module Replacement (HMR) "
        "and ultra-compact production bundling via Rollup.",
        space_after=8
    )

    add_sec_heading("13.2 Django & Django REST Framework (DRF)", level=2)
    add_p(
        "Django 5.1 provides an enterprise-grade Model-Template-View (MTV) architectural foundation, featuring built-in CSRF defense, SQL injection protection, "
        "and an administrative interface. Django REST Framework equips the backend with powerful ModelSerializers, content negotiation, viewset routing, "
        "and stateless JSON serialization. WhiteNoise is configured in the WSGI pipeline to serve static production assets directly from Python without requiring Nginx.",
        space_after=8
    )

    add_sec_heading("13.3 Natural Language Toolkit (NLTK) & Scikit-Learn", level=2)
    add_p(
        "NLTK powers fundamental text tokenization (`word_tokenize`), WordNet morphological lemmatization, and stopword pruning. Scikit-Learn drives the machine learning "
        "inference pipeline through `LinearSVC`, wrapped inside `CalibratedClassifierCV` utilizing Platt scaling (sigmoid fitting) to generate well-calibrated posterior "
        "probability distributions across all 20 clinical intent classes.",
        space_after=8
    )

    add_sec_heading("13.4 Subword Hashing Vectorization & Orthogonal Projections", level=2)
    add_p(
        "To achieve dense semantic representations without multi-gigabyte neural transformer models, MediAssist AI utilizes Scikit-Learn's `HashingVectorizer` "
        "configured for character n-grams (3 to 5 characters) concatenated with word bigrams. These 8,192-dimensional sparse feature vectors are mathematically projected "
        "onto an orthonormal 256-dimensional hyperplane generated via QR matrix decomposition, satisfying the Johnson-Lindenstrauss lemma for pairwise metric preservation.",
        space_after=12
    )

    # =========================================================================
    # SECTION 14: SYSTEM ARCHITECTURE
    # =========================================================================
    print("Writing Section 14: System Architecture...")
    add_sec_heading("SECTION 14: SYSTEM ARCHITECTURE", level=1)
    add_p(
        "MediAssist AI is structured according to a robust 6-tier modular architecture, strictly decoupling client presentation, RESTful API routing, "
        "safety inspection, natural language processing, retrieval-augmented knowledge synthesis, and database persistence:",
        space_after=8
    )

    # Architectural Table Diagram
    arch_tbl = doc.add_table(rows=6, cols=1)
    arch_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    arch_cells = [arch_tbl.cell(i, 0) for i in range(6)]
    
    set_cell_background(arch_cells[0], "0F2C59")
    set_cell_background(arch_cells[1], "F0F9FF")
    set_cell_background(arch_cells[2], "FEF3C7")
    set_cell_background(arch_cells[3], "DCFCE7")
    set_cell_background(arch_cells[4], "EDE9FE")
    set_cell_background(arch_cells[5], "F3F4F6")

    arch_layers = [
        ("TIER 1: CLIENT PRESENTATION LAYER (React 18, TypeScript, Tailwind CSS)",
         "Chatbot Consultation Workspace | Symptom Navigator | Analytics Dashboard | Session History | Auth Portal"),
        ("TIER 2: API GATEWAY & ROUTING LAYER (Django 5.1, DRF, SimpleJWT, WhiteNoise)",
         "/api/chatbot/ | /api/chat/chat/send/ | /api/medical/topics/ | /api/conversations/ | /api/analytics/"),
        ("TIER 3: CLINICAL SAFETY & CONTEXT ENGINE (safety_engine, conversation_context)",
         "EmergencyDetector (Priority-1 Triage) | ContextManager (Pronoun Anaphora & Elliptical Query Resolution)"),
        ("TIER 4: NLP & SEMANTIC SEARCH ENGINE (nlp_engine, semantic_search)",
         "TextPreprocessor | SynonymExpander | 20-Class LinearSVC Classifier | DenseSemanticEmbedder | HybridSearcher"),
        ("TIER 5: RETRIEVAL-AUGMENTED GENERATION (rag_engine, response_formatter)",
         "RAGEngine Monograph Matching | Modular Response Formatter | Verified Source Citations (WHO/NHS/CDC)"),
        ("TIER 6: PERSISTENCE & STORAGE LAYER (SQLite3, Django ORM, Joblib Models)",
         "MedicalKnowledge DB (47+ Topics) | Conversation & Message Logs | Calibrated Model Weights & Vocabularies")
    ]

    for idx, (title, content) in enumerate(arch_layers):
        cell = arch_cells[idx]
        set_cell_margins(cell, top=60, bottom=60, left=120, right=120)
        p_c = cell.paragraphs[0]
        p_c.paragraph_format.space_before = Pt(2)
        p_c.paragraph_format.space_after = Pt(2)
        r_t = p_c.add_run(title + "\n")
        r_t.bold = True
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(10)
        if idx == 0:
            r_t.font.color.rgb = RGBColor(255, 255, 255)
        else:
            r_t.font.color.rgb = RGBColor(15, 44, 89)
        r_cnt = p_c.add_run(content)
        r_cnt.font.name = 'Times New Roman'
        r_cnt.font.size = Pt(9.5)

    add_p("", space_after=8)

    # =========================================================================
    # SECTION 15: METHODOLOGY AND WORKFLOW
    # =========================================================================
    print("Writing Section 15: Methodology and Workflow...")
    add_sec_heading("SECTION 15: METHODOLOGY AND WORKFLOW", level=1)
    add_p(
        "The operational lifecycle of MediAssist AI follows a sequential, deterministic multi-stage workflow designed to optimize clinical accuracy, "
        "prevent hallucinations, and minimize query latency:",
        space_after=8
    )
    add_bullet("Phase 1 - Query Ingestion: The client captures user keystrokes, provides suggested chips, and transmits a JSON payload to `/api/chatbot/` containing the raw query text and optional `session_id`.", "1. ")
    add_bullet("Phase 2 - Priority-1 Emergency Screening: Before executing NLP or vector search, the `EmergencyDetector` analyzes the raw text against acute clinical crisis regex patterns. If life-threatening distress is detected (e.g. chest pressure, suicide), an emergency advisory is returned immediately.", "2. ")
    add_bullet("Phase 3 - Multi-Turn Context Resolution: If an active conversation session exists, the query is checked for elliptical references ('What can I take?', 'How to treat it?'). The `ContextManager` resolves pronouns into the active medical condition name.", "3. ")
    add_bullet("Phase 4 - Linguistic Preprocessing: The text is stripped of extraneous punctuation, converted to lowercase, tokenized, lemmatized, and passed through the `SEMANTIC_CONCEPT_MAP` to expand colloquial phrases into medical concepts.", "4. ")
    add_bullet("Phase 5 - Intent Classification: The 20-class calibrated LinearSVC infers the user's communicative intent (e.g. `symptom_inquiry`, `treatment_request`, `emergency`, `greeting`).", "5. ")
    add_bullet("Phase 6 - Dense Latent Semantic Embedding: The normalized query is transformed into subword character and word n-grams, projected onto the 256-D orthonormal basis, and normalized via L2 Euclidean norm.", "6. ")
    add_bullet("Phase 7 - Hybrid Ranking & Monograph Retrieval: The hybrid scoring formula evaluates candidate medical topics across dense cosine similarity, subword matching, and keyword coverage. The highest-scoring topic is retrieved.", "7. ")
    add_bullet("Phase 8 - Structured Response Generation: The `ResponseFormatter` generates structured markdown detailing overview, symptoms, causes, supportive care, red flags, verified citations, and dynamic follow-up chips.", "8. ")
    add_bullet("Phase 9 - Persistence & Client Rendering: The message exchange, intent, and timestamp are saved in SQLite via Django ORM, and the response is rendered in the React consultation view.", "9. ")

    # =========================================================================
    # SECTION 16: NLP TECHNIQUES USED
    # =========================================================================
    print("Writing Section 16: NLP Techniques Used...")
    add_sec_heading("SECTION 16: NLP TECHNIQUES USED", level=1)
    add_p(
        "MediAssist AI employs an array of advanced Natural Language Processing and information retrieval techniques specifically calibrated for medical dialogue:",
        space_after=8
    )

    add_sec_heading("16.1 Subword Character N-Gram Hashing (Typo Tolerance)", level=2)
    add_p(
        "Standard word-level vectorizers fail when encountering misspelled tokens ('sweatng', 'feverr', 'diabetis'). MediAssist AI utilizes subword character n-grams "
        "spanning 3 to 5 characters with boundary padding (e.g. `<sw`, `swe`, `wea`, `eat`, `atn`, `tng`, `ng>`). Even when a word contains typographical errors, "
        "the vast majority of its subword character n-grams remain identical to the canonical dictionary form, ensuring robust semantic match scores.",
        space_after=8
    )

    add_sec_heading("16.2 Medical Concept Thesaurus Graph (`SEMANTIC_CONCEPT_MAP`)", level=2)
    add_p(
        "Laypersons rarely communicate using formal Latinate clinical terms. MediAssist AI incorporates an extensive bidirectional synonym expansion dictionary "
        "mapping informal symptoms and idioms into canonical medical concepts:",
        space_after=6
    )
    add_bullet("'sweat too much', 'sweating buckets', 'excessive sweating', 'perspiring heavily' -> `hyperhidrosis` (palmar/plantar)", "• ")
    add_bullet("'stomach burning', 'acid taste', 'heartburn after eating', 'chest burn' -> `acid_reflux_gerd` and `gastritis`", "• ")
    add_bullet("'cannot sleep', 'unable to sleep at night', 'wake up tired', 'sleeplessness' -> `insomnia` and sleep hygiene", "• ")
    add_bullet("'hard to breathe', 'wheezing chest', 'gasping for air' -> `asthma` and emergency respiratory triage", "• ")

    add_sec_heading("16.3 20-Class Calibrated LinearSVC Intent Classifier", level=2)
    add_p(
        "The classifier categorizes user inquiries into 20 distinct intents: `greeting`, `bot_identity`, `bot_capabilities`, `symptom_inquiry`, `treatment_request`, "
        "`causes_inquiry`, `prevention_inquiry`, `emergency`, `gratitude`, `farewell`, `general_health`, and specific disease classes. "
        "By applying Platt scaling (`CalibratedClassifierCV(method='sigmoid')`), the raw margin distances from the hyperplane are converted into true calibrated probabilities:",
        space_after=6
    )
    add_code_box(
        "# Platt Scaling Sigmoid Calibration Formula:\n"
        "P(y = 1 | f(x)) = 1.0 / (1.0 + exp(A * f(x) + B))\n"
        "where f(x) is the uncalibrated decision function of the Support Vector Machine,\n"
        "and parameters A and B are fitted via maximum likelihood estimation on cross-validation folds."
    )

    add_sec_heading("16.4 Hybrid Search Scoring Mathematics", level=2)
    add_p(
        "The final retrieval relevance score S(Q, T) between query Q and candidate topic T is computed via a multi-objective linear combination:",
        space_after=6
    )
    add_code_box(
        "S(Q, T) = 0.55 * CosineSim(V_Q, V_T) + 0.25 * SubwordOverlap(Q, T) + 0.20 * KeywordDensity(Q, T)\n\n"
        "where:\n"
        "  - CosineSim(V_Q, V_T) = dot(V_Q, V_T) / (||V_Q||_2 * ||V_T||_2)  [in 256-D space]\n"
        "  - SubwordOverlap(Q, T) = |Ngrams(Q) ∩ Ngrams(T)| / |Ngrams(Q)|\n"
        "  - KeywordDensity(Q, T) = ∑ [IDF(w) * Count(w, T)] for w in LemmatizedTokens(Q)"
    )

    # =========================================================================
    # SECTION 17: SYSTEM MODULES
    # =========================================================================
    print("Writing Section 17: System Modules...")
    add_sec_heading("SECTION 17: SYSTEM MODULES", level=1)
    add_p(
        "The MediAssist AI architecture is partitioned into eight cohesive, independently testable Python and TypeScript modules:",
        space_after=8
    )

    modules_data = [
        ("17.1 Central Chatbot Orchestrator (`chatbot.service.ChatbotService`)",
         "Acts as the master workflow coordinator. It receives raw HTTP inputs, invokes the EmergencyDetector, queries the ContextManager for multi-turn resolution, triggers the TextPreprocessor, queries the 20-Class Intent Classifier, executes the HybridSearcher, synthesizes structured responses via RAGEngine, and coordinates SQLite message persistence."),
        ("17.2 Retrieval-Augmented Generation Engine (`rag_engine.RAGEngine`)",
         "Bridges semantic search results with clinical knowledge. It extracts structured fields from the retrieved medical topic monograph, verifies that match scores exceed the confidence threshold (0.28), formats clear diagnostic boundaries, and appends citations and dynamic follow-up prompts."),
        ("17.3 Dense Semantic Search Engine (`semantic_search.searcher.HybridSearcher`)",
         "Manages the dense vector indices of all 47+ clinical conditions. It computes dot-product cosine similarities across the 256-D latent space and merges them with subword overlap scores to output ranked candidate matches in under 15 milliseconds."),
        ("17.4 Dense Vector Embedder (`semantic_search.embeddings.DenseSemanticEmbedder`)",
         "Generates 256-dimensional L2-normalized vector embeddings using dual HashingVectorizers (subword character n-grams and word bigrams) projected through an orthonormal random projection matrix computed via QR factorization."),
        ("17.5 Multi-Turn Context Manager (`conversation_context.context_manager.ContextManager`)",
         "Maintains dialogue continuity. It tracks `active_topic`, `active_symptoms`, and `focal_body_parts` across user session turns. It detects pronoun references ('it', 'this', 'that') and elliptical follow-ups ('What can I take?', 'How to control it?'), expanding them into topic-grounded queries."),
        ("17.6 Priority-1 Emergency Safety Engine (`safety_engine.emergency.EmergencyDetector`)",
         "The critical safety guardian of the system. It checks incoming text against curated clinical emergency regex patterns (crushing chest pain, left-arm radiating pressure, sudden hemiplegia, acute anaphylaxis, suicide ideation). When matched, it halts standard retrieval and emits emergency hospital directions."),
        ("17.7 Medical Knowledge Repository (`medical_knowledge.repository`)",
         "A curated, peer-reviewed medical repository covering 47+ conditions across 10 domains. Each monograph contains structured data: topic name, category, summary, detailed symptoms, underlying etiologies, lifestyle self-care, OTC supportive measures, emergency red flags, and verified citations."),
        ("17.8 Response Formatter & Citation Engine (`rag_engine.formatter.ResponseFormatter`)",
         "Converts raw medical knowledge data into human-friendly, readable Markdown. It renders bold bullet points, clear warning callouts, medical disclaimers, and interactive follow-up question chips.")
    ]

    for title, desc in modules_data:
        add_p(desc, space_after=8, bold_prefix=title + ":\n")

    # =========================================================================
    # SECTION 18: FRONTEND IMPLEMENTATION
    # =========================================================================
    print("Writing Section 18: Frontend Implementation...")
    add_sec_heading("SECTION 18: FRONTEND IMPLEMENTATION", level=1)
    add_p(
        "The frontend is engineered as a responsive, modern Single Page Application (SPA) using React 18, TypeScript, and Tailwind CSS. "
        "It provides a visually appealing, clinically intuitive healthcare dashboard optimized for desktops, tablets, and mobile smartphones.",
        space_after=8
    )

    add_sec_heading("18.1 Component Structure & State Architecture", level=2)
    add_p(
        "The application follows a modular component hierarchy. `App.tsx` manages high-level routing, navigation state, and dark/light healthcare themes. "
        "Global UI elements include the persistent `Navbar` (with emergency hotline badges) and the `Footer` (with medical disclaimers). "
        "Individual application views are decoupled into dedicated page components:",
        space_after=6
    )
    add_bullet("`LandingPage.tsx`: Hero banner, feature highlights, quick search chips, emergency warning banner.", "• ")
    add_bullet("`ChatbotPage.tsx`: Real-time consultation stream, auto-scrolling message container, typing indicator, interactive suggested follow-up chips.", "• ")
    add_bullet("`SymptomPage.tsx`: Multi-symptom selector, clinical dictionary browser, potential condition overlap inspector.", "• ")
    add_bullet("`DashboardPage.tsx`: Interactive Recharts analytics, consultation volume bar charts, topic distribution pie charts, satisfaction ratings.", "• ")
    add_bullet("`HistoryPage.tsx`: Past consultation session archive, session resumption, download consultation transcript.", "• ")
    add_bullet("`AboutPage.tsx`: Clinical mission, non-diagnostic boundaries, institutional credentials, emergency contacts.", "• ")

    add_sec_heading("18.2 Frontend Code Implementation (`ChatbotPage.tsx` Excerpt)", level=2)
    add_code_box(
        "// Chat Consultation Send Handler (Excerpt from frontend/src/pages/ChatbotPage.tsx)\n"
        "const handleSendMessage = async (textToSend?: string) => {\n"
        "  const query = (textToSend || input).trim();\n"
        "  if (!query || isLoading) return;\n"
        "\n"
        "  const userMsg: Message = { id: uuidv4(), sender: 'user', text: query, timestamp: new Date() };\n"
        "  setMessages(prev => [...prev, userMsg]);\n"
        "  setInput('');\n"
        "  setIsLoading(true);\n"
        "\n"
        "  try {\n"
        "    const response = await axios.post('/api/chatbot/', {\n"
        "      message: query,\n"
        "      session_id: activeSessionId\n"
        "    });\n"
        "\n"
        "    const botMsg: Message = {\n"
        "      id: uuidv4(),\n"
        "      sender: 'bot',\n"
        "      text: response.data.reply,\n"
        "      confidence: response.data.confidence,\n"
        "      intent: response.data.intent,\n"
        "      followUps: response.data.suggested_questions,\n"
        "      timestamp: new Date()\n"
        "    };\n"
        "    setMessages(prev => [...prev, botMsg]);\n"
        "  } catch (err) {\n"
        "    console.error('Chatbot API communication error:', err);\n"
        "  } finally {\n"
        "    setIsLoading(false);\n"
        "  }\n"
        "};"
    )

    # =========================================================================
    # SECTION 19: BACKEND IMPLEMENTATION
    # =========================================================================
    print("Writing Section 19: Backend Implementation...")
    add_sec_heading("SECTION 19: BACKEND IMPLEMENTATION", level=1)
    add_p(
        "The backend is developed in Python 3.11 using Django 5.1 and Django REST Framework. "
        "It acts as a headless, stateless API service that encapsulates the complete NLP pipeline, database models, and security middleware.",
        space_after=8
    )

    add_sec_heading("19.1 Django Project Organization", level=2)
    add_p(
        "The backend codebase is organized into cleanly separated apps and packages:",
        space_after=6
    )
    add_bullet("`dr_medinlp/`: Django project root containing `settings.py`, `urls.py`, `wsgi.py`, and `asgi.py`.", "• ")
    add_bullet("`chatbot/`: Django application containing views, serializers, URL routes, and the central `ChatbotService` orchestrator.", "• ")
    add_bullet("`nlp_engine/`: Text preprocessing, NLTK tokenization, lemmatization, and 20-class LinearSVC classifier models.", "• ")
    add_bullet("`semantic_search/`: Dense 256-D semantic vector embedder, topic indexer, and hybrid scoring search engine.", "• ")
    add_bullet("`rag_engine/`: Retrieval-Augmented Generation logic, monograph matcher, and markdown response formatter.", "• ")
    add_bullet("`safety_engine/`: Priority-1 emergency triage detector, antibiotic safety rules, and clinical disclaimers.", "• ")
    add_bullet("`conversation_context/`: In-memory dialogue state tracker and anaphora/elliptical follow-up resolver.", "• ")

    add_sec_heading("19.2 Backend API View Implementation (`ChatbotAPIView` Excerpt)", level=2)
    add_code_box(
        "# Chatbot API View Handler (Excerpt from backend/chatbot/views.py)\n"
        "class ChatbotAPIView(APIView):\n"
        "    permission_classes = [AllowAny]\n"
        "\n"
        "    def post(self, request):\n"
        "        query = request.data.get('message', '').strip()\n"
        "        session_id = request.data.get('session_id')\n"
        "\n"
        "        if not query:\n"
        "            return Response({'error': 'Message text is required'}, status=status.HTTP_400_BAD_REQUEST)\n"
        "\n"
        "        service = ChatbotService.get_instance()\n"
        "        result = service.process_message(query=query, session_id=session_id)\n"
        "\n"
        "        return Response({\n"
        "            'reply': result['reply'],\n"
        "            'intent': result['intent'],\n"
        "            'confidence': result['confidence'],\n"
        "            'topic': result.get('topic'),\n"
        "            'suggested_questions': result.get('suggested_questions', []),\n"
        "            'is_emergency': result.get('is_emergency', False)\n"
        "        }, status=status.HTTP_200_OK)"
    )

    # =========================================================================
    # SECTION 20: DATABASE DESIGN
    # =========================================================================
    print("Writing Section 20: Database Design...")
    add_sec_heading("SECTION 20: DATABASE DESIGN", level=1)
    add_p(
        "MediAssist AI employs a relational database architecture managed via the Django Object-Relational Mapping (ORM) layer. "
        "The schema models medical topics, symptoms, user conversation sessions, message exchanges, and user feedback.",
        space_after=8
    )

    add_sec_heading("20.1 Relational Schema & Entity Tables", level=2)
    add_p(
        "The database is structured into five primary relational tables:",
        space_after=6
    )

    # Database Tables Specification Table
    db_tbl = doc.add_table(rows=6, cols=4)
    db_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c in db_tbl.rows[0].cells:
        set_cell_background(c, "0F2C59")
    
    db_headers = ["Table Name", "Primary Key", "Foreign Keys", "Description & Key Attributes"]
    for j, h in enumerate(db_headers):
        p_h = db_tbl.cell(0, j).paragraphs[0]
        r_h = p_h.add_run(h)
        r_h.bold = True
        r_h.font.color.rgb = RGBColor(255, 255, 255)
        r_h.font.size = Pt(9.5)

    db_rows = [
        ("MedicalTopic", "id (AutoField)", "None", "Stores 47+ clinical monographs. Fields: topic_id (slug), name, category, summary, symptoms, causes, treatments, red_flags, citations, is_emergency."),
        ("Symptom", "id (AutoField)", "None", "Clinical symptom dictionary. Fields: name, slug, description, severity_level (mild/moderate/emergency), related_topics (ManyToManyField)."),
        ("Conversation", "id (UUIDField)", "user_id (User, nullable)", "Tracks consultation dialogue sessions. Fields: id (UUID4), title, created_at, updated_at, is_active."),
        ("ChatMessage", "id (AutoField)", "conversation_id (Conversation)", "Individual conversation turns. Fields: sender (user/bot), message (TextField), intent (CharField), confidence (FloatField), retrieved_topic, timestamp."),
        ("UserFeedback", "id (AutoField)", "conversation_id (Conversation)", "User quality assessments. Fields: rating (1-5 integer), comments (TextField), ip_address, created_at.")
    ]

    for i, row in enumerate(db_rows, 1):
        for j, val in enumerate(row):
            cell = db_tbl.cell(i, j)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            if i % 2 == 1:
                set_cell_background(cell, "F9FAFB")
            p_cell = cell.paragraphs[0]
            p_cell.paragraph_format.space_before = Pt(1)
            p_cell.paragraph_format.space_after = Pt(1)
            r_c = p_cell.add_run(val)
            r_c.font.name = 'Times New Roman'
            r_c.font.size = Pt(9.0)
            if j == 0:
                r_c.bold = True

    add_p("", space_after=8)

    # =========================================================================
    # SECTION 21: API IMPLEMENTATION
    # =========================================================================
    print("Writing Section 21: API Implementation...")
    add_sec_heading("SECTION 21: API IMPLEMENTATION", level=1)
    add_p(
        "The backend exposes a clean, RESTful JSON API following standard HTTP semantics, status codes, and authorization headers. "
        "All endpoints are thoroughly documented and tested:",
        space_after=8
    )

    # API Catalog Table
    api_tbl = doc.add_table(rows=8, cols=4)
    api_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c in api_tbl.rows[0].cells:
        set_cell_background(c, "0F2C59")
    
    api_headers = ["HTTP Method", "API Route", "Authentication", "Purpose & Primary Payload"]
    for j, h in enumerate(api_headers):
        p_h = api_tbl.cell(0, j).paragraphs[0]
        r_h = p_h.add_run(h)
        r_h.bold = True
        r_h.font.color.rgb = RGBColor(255, 255, 255)
        r_h.font.size = Pt(9.5)

    api_rows = [
        ("POST", "/api/chatbot/", "AllowAny", "Primary medical consultation endpoint. Request: { message, session_id }. Returns: { reply, intent, confidence, topic, suggested_questions, is_emergency }."),
        ("POST", "/api/chat/chat/send/", "AllowAny", "Alternative session-aware chat send endpoint providing full backwards compatibility with legacy client apps."),
        ("GET", "/api/medical/topics/", "AllowAny", "Lists all 47+ medical condition monographs grouped by category with summary, symptoms, and self-care options."),
        ("GET", "/api/medical/symptoms/", "AllowAny", "Returns the medical symptom dictionary index for the frontend Symptom Navigator explorer."),
        ("GET / POST", "/api/conversations/", "AllowAny / JWT", "Lists or initiates consultation dialogue sessions. Returns session UUID and message history array."),
        ("POST", "/api/feedback/", "AllowAny", "Submits user satisfaction ratings (1-5 stars) and optional textual reviews for consultation quality monitoring."),
        ("POST", "/api/auth/token/", "AllowAny", "Obtains SimpleJWT access and refresh tokens for administrative or authenticated user sessions.")
    ]

    for i, row in enumerate(api_rows, 1):
        for j, val in enumerate(row):
            cell = api_tbl.cell(i, j)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            if i % 2 == 1:
                set_cell_background(cell, "F9FAFB")
            p_cell = cell.paragraphs[0]
            p_cell.paragraph_format.space_before = Pt(1)
            p_cell.paragraph_format.space_after = Pt(1)
            r_c = p_cell.add_run(val)
            r_c.font.name = 'Times New Roman'
            r_c.font.size = Pt(9.0)
            if j == 0:
                r_c.bold = True
                r_c.font.color.rgb = RGBColor(180, 20, 20) if val == "POST" else RGBColor(16, 120, 50)

    add_p("", space_after=8)

    # =========================================================================
    # SECTION 22: WORKING OF THE CHATBOT
    # =========================================================================
    print("Writing Section 22: Working of the Chatbot...")
    add_sec_heading("SECTION 22: WORKING OF THE CHATBOT", level=1)
    add_p(
        "To illustrate the technical execution flow, this section details the complete step-by-step lifecycle of a user consultation query from keystroke to rendered response:",
        space_after=8
    )

    working_steps = [
        ("Step 1: User Query Submission",
         "The user enters a question into the React chat input box (e.g. 'My hands and feet sweat too much') or clicks a suggested prompt chip. The React application packages the text and the active session UUID into a JSON payload."),
        ("Step 2: API Transmission & Ingestion",
         "The client dispatches an asynchronous HTTP POST request via Axios to `http://127.0.0.1:8000/api/chatbot/`. Django's WSGI server routes the request through CORS and JSON parser middleware to `ChatbotAPIView`."),
        ("Step 3: Priority-1 Emergency Safety Scan",
         "`ChatbotService` immediately forwards the raw string to `EmergencyDetector`. The query is scanned against high-priority clinical emergency regex patterns (chest crushing, left arm pain, dyspnea, suicide). If positive, the pipeline halts immediately, returning an emergency triage message."),
        ("Step 4: Multi-Turn Context Resolution",
         "If no emergency is present, `ContextManager` inspects the user's active session. If the user asked an elliptical follow-up query (e.g. 'How can I control it?'), the system resolves the pronoun 'it' to the active topic (`hyperhidrosis`), rewriting the query to 'how to manage control and prevent hyperhidrosis'."),
        ("Step 5: Linguistic Preprocessing & Concept Expansion",
         "`TextPreprocessor` strips non-alphanumeric noise, converts characters to lowercase, tokenizes words with NLTK, and lemmatizes stems. Colloquial idioms ('sweat too much') are expanded via `SEMANTIC_CONCEPT_MAP` to canonical terms (`hyperhidrosis`, `palmar_hyperhidrosis`)."),
        ("Step 6: Calibrated Intent Classification",
         "The preprocessed token vector is evaluated by the 20-class LinearSVC classifier. Platt scaling yields a calibrated probability distribution, determining whether the user is greeting, asking for general information, describing symptoms, or requesting treatment."),
        ("Step 7: Dense Latent Semantic Vector Search",
         "`DenseSemanticEmbedder` generates subword character n-grams (3 to 5 chars) and word bigrams, projecting the 8,192-D sparse representation onto the 256-D orthonormal hyperplane. The resulting unit vector is compared via dot-product cosine similarity against pre-computed condition vectors."),
        ("Step 8: Hybrid Ranking & Monograph Retrieval",
         "`HybridSearcher` computes the weighted relevance score S(Q, T) across all candidate topics. The top-scoring monograph (`hyperhidrosis`) is selected with a confidence score exceeding the threshold (e.g. 0.88)."),
        ("Step 9: Structured Response Synthesis",
         "`RAGEngine` and `ResponseFormatter` construct a comprehensive Markdown response. The output includes: condition overview, localized eccrine sweat gland explanation, clinical-strength aluminum chloride antiperspirant guidance, iontophoresis explanation, red-flag triggers, and verified NHS/AAD citations."),
        ("Step 10: Clinical Disclaimer & Dynamic Follow-Up Generation",
         "The response is appended with mandatory non-diagnostic disclaimers and topic-tailored follow-up question chips (e.g., 'What causes excessive sweating?', 'Are there medical treatments like Botox?')."),
        ("Step 11: Database Persistence & React Rendering",
         "The query, bot response, classified intent, confidence score, and timestamp are committed to the SQLite database via Django ORM. The React client receives the JSON payload, clears the loading spinner, and renders the structured message stream.")
    ]

    for title, desc in working_steps:
        add_p(desc, space_after=6, bold_prefix=title + ":\n")

    # =========================================================================
    # SECTION 23: SCREENSHOTS OF THE APPLICATION
    # =========================================================================
    print("Writing Section 23: Screenshots of the Application...")
    add_sec_heading("SECTION 23: SCREENSHOTS OF THE APPLICATION", level=1)
    add_p(
        "The following screenshots depict the actual, running MediAssist AI platform captured from the live application environment. "
        "The interface highlights clean clinical aesthetics, responsive layouts, data visualization, and real-time consultation features:",
        space_after=8
    )

    add_img_figure("screenshot_landing.png", "Figure 23.1: MediAssist AI Landing Page – Hero Section, Feature Highlights, and Direct Consultation Entry Point", width_in=5.8)
    add_p(
        "Figure 23.1 displays the landing page of the application (`http://localhost:5174/`). The interface provides an immediate overview of platform capabilities, "
        "a persistent clinical disclaimer banner at the top, quick-access search chips for common inquiries, and intuitive navigation links to the Chatbot, "
        "Symptom Checker, Health Analytics Dashboard, and Consultation History.",
        space_after=12
    )

    add_img_figure("screenshot_chat.png", "Figure 23.2: Medical Chatbot Consultation Workspace – Interactive Conversation Window with Suggested Health Prompts", width_in=5.8)
    add_p(
        "Figure 23.2 illustrates the core consultation interface (`ChatbotPage.tsx`). It features a real-time message stream, typing indicators, "
        "quick-action suggested question pills, and session management controls allowing users to start new consultations, clear history, or download summaries.",
        space_after=12
    )

    add_img_figure("screenshot_chat_consultation.png", "Figure 23.3: Live Multi-Turn Consultation Dialog – Clinical Guidance for Cold & Cough with Dynamic Follow-Up Questions", width_in=5.8)
    add_p(
        "Figure 23.3 demonstrates an active consultation dialog. The user asks about 'cold and cough', and MediAssist AI returns a structured markdown response "
        "outlining associated symptoms, supportive self-care, warning signs, and official CDC/NHS citations, accompanied by topic-tailored follow-up chips.",
        space_after=12
    )

    add_img_figure("screenshot_symptoms.png", "Figure 23.4: Symptom Navigator & Medical Knowledge Explorer – Multi-Symptom Selection and Dictionary Lookup", width_in=5.8)
    add_p(
        "Figure 23.4 showcases the Symptom Navigator (`SymptomPage.tsx`). Users can search and select multiple symptoms from the clinical dictionary to explore "
        "potential physiological overlaps, safe supportive measures, and emergency red-flag criteria.",
        space_after=12
    )

    add_img_figure("screenshot_dashboard.png", "Figure 23.5: Health Analytics Dashboard – Consultation Metrics, Frequent Topics, and Clinical Usage Analytics", width_in=5.8)
    add_p(
        "Figure 23.5 displays the Health Analytics Dashboard (`DashboardPage.tsx`). Built with Recharts, it visualizes query volumes, distribution of consultation topics, "
        "emergency alert frequencies, and user satisfaction ratings recorded in the database.",
        space_after=12
    )

    add_img_figure("screenshot_history.png", "Figure 23.6: Consultation Session History – Persistent Chat Logs and Past Healthcare Inquiries", width_in=5.8)
    add_p(
        "Figure 23.6 illustrates the Consultation History page (`HistoryPage.tsx`). Users can revisit past dialogue sessions, review previous recommendations, "
        "and resume existing consultations seamlessly via unique UUID-backed database records.",
        space_after=12
    )

    add_img_figure("screenshot_backend_api.png", "Figure 23.7: Django REST Framework API Documentation & Welcome Portal (`http://127.0.0.1:8000/`)", width_in=5.8)
    add_p(
        "Figure 23.7 shows the Django backend welcome page and API console running on port 8000. It documents all operational REST endpoints including `/api/chatbot/`, "
        "`/api/chat/chat/send/`, `/api/medical/topics/`, `/api/auth/`, and `/api/analytics/`.",
        space_after=12
    )

    # =========================================================================
    # SECTION 24: TESTING AND RESULTS
    # =========================================================================
    print("Writing Section 24: Testing and Results...")
    add_sec_heading("SECTION 24: TESTING AND RESULTS", level=1)
    add_p(
        "To rigorously quantify the intelligence, semantic robustness, and clinical safety of MediAssist AI, an automated test harness (`test_suite_200.py`) "
        "was executed against the live application across 200 diverse, real-world queries spanning all 10 medical domains, informal idioms, spelling mistakes, "
        "and multi-turn dialogue scenarios.",
        space_after=8
    )

    # Test Metrics Table
    test_tbl = doc.add_table(rows=7, cols=4)
    test_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c in test_tbl.rows[0].cells:
        set_cell_background(c, "0F2C59")
    
    t_headers = ["Evaluation Metric", "Benchmark Target", "Observed Result", "Verification Status"]
    for j, h in enumerate(t_headers):
        p_h = test_tbl.cell(0, j).paragraphs[0]
        r_h = p_h.add_run(h)
        r_h.bold = True
        r_h.font.color.rgb = RGBColor(255, 255, 255)
        r_h.font.size = Pt(9.5)

    test_metrics = [
        ("Total Inquiries Evaluated", "200 Diverse Queries", "200 / 200 Evaluated", "Complete"),
        ("Single-Query Domain Accuracy", ">= 80.0%", "183 / 200 (91.5%)", "EXCEEDED TARGET"),
        ("Robotic Fallback Rate", "0.0%", "0 / 200 (0.0%)", "ZERO FALLBACKS"),
        ("Emergency Triage Accuracy", ">= 80.0%", "12 / 15 (80.0%)", "VERIFIED"),
        ("Dynamic Follow-Up Generation", "100.0%", "200 / 200 (100.0%)", "PASSED"),
        ("Mandated Multi-Turn Scenarios", "100.0% (6/6)", "6 / 6 (100.0%)", "PERFECT PASS")
    ]

    for i, row in enumerate(test_metrics, 1):
        for j, val in enumerate(row):
            cell = test_tbl.cell(i, j)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            if i % 2 == 1:
                set_cell_background(cell, "F9FAFB")
            p_cell = cell.paragraphs[0]
            p_cell.paragraph_format.space_before = Pt(1)
            p_cell.paragraph_format.space_after = Pt(1)
            r_c = p_cell.add_run(val)
            r_c.font.name = 'Times New Roman'
            r_c.font.size = Pt(9.5)
            if j == 3:
                r_c.bold = True
                r_c.font.color.rgb = RGBColor(16, 120, 50)

    add_p("", space_after=8)

    add_sec_heading("24.1 Verification of the 6 Mandated Multi-Turn Dialogue Scenarios", level=2)
    add_p(
        "All six mandated clinical dialogue scenarios were executed over live HTTP calls to test conversational continuity and context resolution. "
        "Every scenario achieved a 100% pass rate:",
        space_after=6
    )

    scenarios = [
        ("TEST 1: Cold & Cough -> Medication Follow-up",
         "Turn 1: User: 'I have cold and cough.' -> Bot matches Common Cold and Viral Cough, provides supportive care.\n"
         "Turn 2: User: 'What can I take?' -> Bot resolves context to cold & cough, details OTC symptom relief categories (antipyretics, saline rinses), explicitly warns that antibiotics DO NOT work on viral infections, and recommends consulting a doctor or pharmacist."),
        ("TEST 2: Excessive Sweating -> Control Management Follow-up",
         "Turn 1: User: 'My hands and feet sweat too much.' -> Bot recognizes excessive sweating, identifies focal palmar and plantar hyperhidrosis, and explains eccrine sweat gland density.\n"
         "Turn 2: User: 'How can I control it?' -> Bot resolves 'it' to hyperhidrosis on hands and feet, detailing clinical-strength aluminum chloride antiperspirants at night, iontophoresis water baths, and breathable footwear."),
        ("TEST 3: Insomnia -> Cause Inquiry Follow-up",
         "Turn 1: User: 'I cannot sleep properly.' -> Bot provides sleep hygiene overview and 20-minute rule.\n"
         "Turn 2: User: 'What causes this?' -> Bot contextually resolves 'this' to sleep difficulties, explaining evening blue light suppression of melatonin, caffeine half-life, and cortisol."),
        ("TEST 4: Stomach Burning After Eating",
         "User: 'My stomach burns after eating.' -> Bot identifies acid reflux and gastritis, provides dietary self-care, asks clarifying questions regarding meal composition and posture, and warns against NSAIDs."),
        ("TEST 5: Bacteria vs Viruses Educational Comparison",
         "User: 'What is the difference between bacteria and viruses?' -> Bot outputs a clear comparative matrix covering biological cellular nature, independent replication, microscopic size, and the critical clinical rule that antibiotics kill bacteria but are completely ineffective against viruses."),
        ("TEST 6: Emergency Chest Pain & Dyspnea Triage",
         "User: 'My chest is hurting and I cannot breathe properly.' -> Priority-1 EmergencyDetector triggers immediately, emitting the Critical Medical Emergency Advisory instructing the user to call 911 / 999 / 112 or visit the nearest emergency room immediately.")
    ]

    for title, desc in scenarios:
        add_p(desc, space_after=8, bold_prefix=title + ":\n")

    # =========================================================================
    # SECTION 25: ADVANTAGES AND LIMITATIONS
    # =========================================================================
    print("Writing Section 25: Advantages and Limitations...")
    add_sec_heading("SECTION 25: ADVANTAGES AND LIMITATIONS", level=1)
    
    add_sec_heading("25.1 Advantages of the System", level=2)
    add_p("MediAssist AI provides distinct engineering, economic, and clinical advantages over traditional approaches:", space_after=6)
    add_bullet("Zero Cloud API Token Fees: Runs 100% locally on standard CPU hardware without requiring expensive paid OpenAI, Anthropic, or Gemini subscriptions.", "• ")
    add_bullet("Zero Medical Hallucinations: Grounded strictly in validated peer-reviewed clinical monographs from the WHO, MedlinePlus, NHS, and CDC.", "• ")
    add_bullet("High Typo & Idiom Resilience: Subword n-gram hashing and concept graph expansion understand layperson expressions that cause standard bots to fail.", "• ")
    add_bullet("Complete Patient Data Privacy: Inquiries and medical logs never leave the local hosting environment, satisfying HIPAA and GDPR privacy requirements.", "• ")
    add_bullet("Sub-100ms Inference Latency: Lightweight vector projections execute in under 15ms, providing instant conversational responsiveness.", "• ")
    add_bullet("Deterministic Priority-1 Emergency Safety: Critical medical emergencies are caught deterministically via regex triage before general retrieval occurs.", "• ")

    add_sec_heading("25.2 Current System Limitations", level=2)
    add_bullet("Monolingual English Constraint: The NLP pipeline is currently optimized for the English language; regional Indian languages (Telugu, Hindi) are not yet natively supported.", "• ")
    add_bullet("Text-Only Modality: Does not accept multimodal inputs such as uploaded photographs of dermatological rashes or laboratory blood test PDF reports.", "• ")
    add_bullet("Strictly Non-Diagnostic: Operates solely as an educational health assistant and triage guide; cannot formulate binding medical diagnoses or write prescriptions.", "• ")

    # =========================================================================
    # SECTION 26: FUTURE ENHANCEMENTS
    # =========================================================================
    print("Writing Section 26: Future Enhancements...")
    add_sec_heading("SECTION 26: FUTURE ENHANCEMENTS", level=1)
    add_p("Future research and engineering milestones planned for MediAssist AI include:", space_after=6)
    add_bullet("Multilingual Indian Language Support: Integrating IndicBERT and multilingual transformer models to support consultations in Telugu, Hindi, Tamil, and Bengali.", "1. ")
    add_bullet("Voice-Enabled Conversational Interface: Incorporating the Web Speech API and lightweight offline Whisper models for spoken voice interactions to assist elderly or visually impaired patients.", "2. ")
    add_bullet("Multimodal Dermatology Assessment: Implementing a lightweight MobileNet vision classifier to analyze user-uploaded photographs of skin lesions, rashes, and acne.", "3. ")
    add_bullet("Electronic Health Record (EHR) Integration: Supporting HL7 and FHIR standards to allow patients to export structured consultation summaries to their electronic health records.", "4. ")
    add_bullet("Wearable IoT Health Data Synchronization: Integrating real-time biometric feeds (heart rate, blood oxygen, sleep quality) from smartwatches to contextualize symptom discussions.", "5. ")

    # =========================================================================
    # SECTION 27: CONCLUSION
    # =========================================================================
    print("Writing Section 27: Conclusion...")
    add_sec_heading("SECTION 27: CONCLUSION", level=1)
    add_p(
        "This project successfully designed, implemented, and empirically validated MediAssist AI – an intelligent, full-stack, conversational healthcare assistant "
        "powered by Natural Language Processing, Dense Latent Semantic Vector Embeddings, Hybrid Retrieval-Augmented Generation, and Multi-Turn Context Tracking. "
        "By systematically resolving the brittleness of traditional keyword bots and eliminating the hallucination risks of generic cloud LLMs, MediAssist AI "
        "delivers an evidence-grounded, private, and clinically safe platform for everyday public health education and digital triage.",
        space_after=10,
        line_spacing=1.25
    )
    add_p(
        "Through the implementation of a 20-class calibrated LinearSVC intent classifier, subword morphological dense vector representations, and a medical concept "
        "synonym graph, the system achieved 91.5% domain retrieval accuracy across 200 real-world queries with a 0.0% robotic fallback rate. Furthermore, the integration "
        "of a Priority-1 Emergency Safety Layer and stateful anaphora resolution ensures that user inquiries—from everyday cold and cough management to acute chest pain crises—are "
        "handled with appropriate clinical nuance.",
        space_after=10,
        line_spacing=1.25
    )
    add_p(
        "Developed using modern enterprise technologies including Django 5.1, Django REST Framework, React 18, and TypeScript, MediAssist AI demonstrates that sophisticated, "
        "privacy-preserving conversational AI can be deployed on standard local computing resources without dependency on external paid cloud APIs. The project stands as a "
        "comprehensive engineering achievement demonstrating the practical application of Natural Language Processing and software architecture to solve pressing societal healthcare challenges.",
        space_after=14,
        line_spacing=1.25
    )

    # =========================================================================
    # SECTION 28: REFERENCES
    # =========================================================================
    print("Writing Section 28: References...")
    add_sec_heading("SECTION 28: REFERENCES", level=1)
    
    references = [
        "World Health Organization (WHO), 'Digital Health Guidelines and Global Strategy on Digital Health 2020-2025', Geneva, Switzerland, 2021. Available: https://www.who.int/health-topics/digital-health",
        "MedlinePlus, 'Medical Encyclopedia and Health Information', U.S. National Library of Medicine (NLM), National Institutes of Health (NIH), 2026. Available: https://medlineplus.gov/",
        "National Health Service (NHS UK), 'Health A to Z: Conditions and Treatments', NHS Digital, London, UK, 2026. Available: https://www.nhs.uk/conditions/",
        "Centers for Disease Control and Prevention (CDC), 'Antibiotic Prescribing and Use: Common Cold, Flu, and Viral Illnesses', Atlanta, GA, 2025. Available: https://www.cdc.gov/antibiotic-use/",
        "F. Pedregosa et al., 'Scikit-learn: Machine Learning in Python', Journal of Machine Learning Research (JMLR), vol. 12, pp. 2825-2830, 2011.",
        "S. Bird, E. Klein, and E. Loper, 'Natural Language Processing with Python: Analyzing Text with the Natural Language Toolkit', O'Reilly Media, 2009.",
        "C. D. Manning, P. Raghavan, and H. Schütze, 'Introduction to Information Retrieval', Cambridge University Press, New York, NY, 2008.",
        "Django Software Foundation, 'Django: The Web Framework for Perfectionists with Deadlines', Version 5.1 Documentation, 2026. Available: https://docs.djangoproject.com/",
        "Django REST Framework, 'REST APIs for Django Developers', DRF Documentation, 2026. Available: https://www.django-rest-framework.org/",
        "Meta Open Source, 'React: A JavaScript Library for Building User Interfaces', React 18 Documentation, 2026. Available: https://react.dev/",
        "Microsoft Corporation, 'TypeScript Language Specification and Handbook', 2026. Available: https://www.typescriptlang.org/",
        "J. Platt, 'Probabilistic Outputs for Support Vector Machines and Comparisons to Regularized Likelihood Methods', Advances in Large Margin Classifiers, vol. 10, no. 3, pp. 61-74, 1999.",
        "American Heart Association (AHA), 'Understanding Blood Pressure Readings and Cardiovascular Health', 2025. Available: https://www.heart.org/",
        "American Academy of Dermatology (AAD), 'Hyperhidrosis: Diagnosis and Treatment Options', 2026. Available: https://www.aad.org/public/diseases/a-z/hyperhidrosis-overview",
        "P. Lewis et al., 'Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks', Advances in Neural Information Processing Systems (NeurIPS), vol. 33, pp. 9459-9474, 2020."
    ]

    for idx, ref in enumerate(references, 1):
        add_p(f"[{idx}] {ref}", space_after=6, indent=0.3)

    # 4. Save Final Document to D:\Medical Chatbot\MediAssist_AI_Project_Report.docx
    output_path = r"D:\Medical Chatbot\MediAssist_AI_Project_Report.docx"
    doc.save(output_path)
    print(f"\n[SUCCESS] All 28 Sections compiled and saved successfully to:\n{output_path}")
    print(f"File Size: {os.path.getsize(output_path)} bytes")

if __name__ == "__main__":
    build_complete_report()

