import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def create_report():
    doc = Document()
    
    # Configure 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # XML Helper Functions
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

    def add_heading_styled(text, level, space_before=14, space_after=6):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        if level == 1:
            run.font.size = Pt(15)
            run.font.color.rgb = RGBColor(15, 44, 89) # Deep Navy
        elif level == 2:
            run.font.size = Pt(13)
            run.font.color.rgb = RGBColor(26, 75, 140) # Slate Navy
        elif level == 3:
            run.font.size = Pt(11.5)
            run.font.color.rgb = RGBColor(40, 40, 40)
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

    def add_code_block(code_text):
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
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(30, 41, 59)
        
        sp = doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(6)

    def add_img(img_path, caption, width_in=5.8):
        full_p = os.path.join("doc_assets", img_path) if not os.path.isabs(img_path) else img_path
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

    print("Framework initialized. Commencing report construction...")

    # =========================================================================
    # SECTION 1: COVER PAGE
    # =========================================================================
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
    r_title.font.color.rgb = RGBColor(180, 20, 20) # Deep Crimson Accent

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

    # College Emblem
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
    # Header table with College logo, Text, and NAAC A+ logo
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

    # Divider bar line
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

    # Signature Table
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
    p_toc = doc.add_paragraph()
    p_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc.paragraph_format.space_before = Pt(8)
    p_toc.paragraph_format.space_after = Pt(12)
    r_toc = p_toc.add_run("TABLE OF CONTENTS")
    r_toc.bold = True
    r_toc.font.name = 'Times New Roman'
    r_toc.font.size = Pt(16)
    r_toc.font.color.rgb = RGBColor(15, 44, 89)

    # Clean structured TOC table
    toc_data = [
        ("Certificate", "ii"),
        ("Acknowledgement", "iii"),
        ("Abstract", "v"),
        ("1. Introduction", "1"),
        ("    1.1 Background and Healthcare Paradigm", "1"),
        ("    1.2 The Growing Role of Conversational AI in Medicine", "2"),
        ("    1.3 Project Motivation and Objectives", "3"),
        ("2. Project Overview & Problem Statement", "5"),
        ("    2.1 Project Overview", "5"),
        ("    2.2 Problem Statement & Industry Gaps", "6"),
        ("    2.3 Existing System & Critical Limitations", "7"),
        ("    2.4 Proposed MediAssist AI Solution", "8"),
        ("3. Tools, Technologies & Environment", "10"),
        ("    3.1 Frontend Technology Stack (React, Vite, TypeScript, Tailwind)", "10"),
        ("    3.2 Backend Framework (Python 3.11, Django 5.1, DRF, SimpleJWT)", "11"),
        ("    3.3 NLP & Machine Learning Libraries (NLTK, Scikit-Learn, NumPy)", "12"),
        ("    3.4 Database & Persistence Architecture", "13"),
        ("4. System Architecture & Methodology", "14"),
        ("    4.1 High-Level Modular Architecture", "14"),
        ("    4.2 End-to-End Execution Flowchart", "16"),
        ("    4.3 Data Flow Diagrams (Level 0 and Level 1 DFD)", "17"),
        ("5. NLP Techniques & Semantic Search", "19"),
        ("    5.1 Text Preprocessing & Typo Tolerance Pipeline", "19"),
        ("    5.2 Colloquial Phrasing & Idiom Normalization", "20"),
        ("    5.3 Intent Classification (20-Class Calibrated LinearSVC)", "21"),
        ("    5.4 Medical Entity Recognition (NER)", "22"),
        ("    5.5 Dense Latent Semantic Vector Embeddings", "24"),
        ("    5.6 Concept Expansion & Synonym Thesaurus Graph", "25"),
        ("    5.7 Hybrid Search Scoring Mathematics", "26"),
        ("6. Multi-Turn Context & Reference Resolution", "28"),
        ("    6.1 Stateful Conversation Tracking", "28"),
        ("    6.2 Pronoun Anaphora Resolution ('it', 'this', 'that')", "29"),
        ("    6.3 Elliptical Query Expansion ('What can I take?')", "30"),
        ("    6.4 Focal Body Part Specialization", "31"),
        ("7. Medical Knowledge Base & Safety Engine", "32"),
        ("    7.1 Knowledge Coverage across 10 Major Medical Domains", "32"),
        ("    7.2 Peer-Reviewed Medical Citations (WHO, MedlinePlus, NHS, CDC)", "34"),
        ("    7.3 Priority-1 Emergency Safety Layer", "35"),
        ("    7.4 Context-Sensitive Clinical Disclaimers", "37"),
        ("8. System Modules & Detailed Implementation", "38"),
        ("    8.1 Central Chatbot Orchestrator (`chatbot.service`)", "38"),
        ("    8.2 Retrieval-Augmented Generation (`rag_engine`)", "39"),
        ("    8.3 Semantic Search Module (`semantic_search`)", "40"),
        ("    8.4 Safety Engine (`safety_engine`)", "41"),
        ("    8.5 Database Design & Django ORM Models", "42"),
        ("    8.6 RESTful API Contracts & Endpoints", "44"),
        ("    8.7 React Frontend User Interface Implementation", "46"),
        ("9. Step-by-Step Working of the Chatbot", "48"),
        ("10. Application Screenshots & Interface Demonstration", "51"),
        ("11. Testing, Experimental Results & Metrics", "57"),
        ("    11.1 Automated 200-Query Clinical Test Suite", "57"),
        ("    11.2 Verification of User-Mandated Multi-Turn Conversations", "59"),
        ("    11.3 Evaluation of 8 Hyperhidrosis Colloquial Variations", "61"),
        ("    11.4 Intent Classifier Evaluation & Confusion Metrics", "62"),
        ("12. Source Code Listings", "64"),
        ("13. Advantages, Limitations & Future Enhancements", "70"),
        ("14. Conclusion", "73"),
        ("15. References", "74"),
    ]

    toc_tbl = doc.add_table(rows=len(toc_data) + 1, cols=2)
    toc_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_tbl.cell(0, 0).width = Inches(5.3)
    toc_tbl.cell(0, 1).width = Inches(1.1)

    # Header
    set_cell_background(toc_tbl.cell(0, 0), "0F2C59")
    set_cell_background(toc_tbl.cell(0, 1), "0F2C59")
    r_th1 = toc_tbl.cell(0, 0).paragraphs[0].add_run("Chapter / Section Description")
    r_th1.bold = True
    r_th1.font.color.rgb = RGBColor(255, 255, 255)
    r_th2 = toc_tbl.cell(0, 1).paragraphs[0].add_run("Page No.")
    r_th2.bold = True
    r_th2.font.color.rgb = RGBColor(255, 255, 255)
    toc_tbl.cell(0, 1).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT

    for i, (title, page) in enumerate(toc_data, 1):
        cell_t = toc_tbl.cell(i, 0)
        cell_p = toc_tbl.cell(i, 1)
        cell_t.width = Inches(5.3)
        cell_p.width = Inches(1.1)
        set_cell_margins(cell_t, top=40, bottom=40, left=100, right=100)
        set_cell_margins(cell_p, top=40, bottom=40, left=100, right=100)
        if i % 2 == 1:
            set_cell_background(cell_t, "F9FAFB")
            set_cell_background(cell_p, "F9FAFB")

        p_t = cell_t.paragraphs[0]
        p_t.paragraph_format.space_before = Pt(1)
        p_t.paragraph_format.space_after = Pt(1)
        r_t = p_t.add_run(title)
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(10)
        if not title.startswith("    "):
            r_t.bold = True

        p_p = cell_p.paragraphs[0]
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
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs.paragraph_format.space_before = Pt(8)
    p_abs.paragraph_format.space_after = Pt(14)
    r_abs = p_abs.add_run("ABSTRACT")
    r_abs.bold = True
    r_abs.font.name = 'Times New Roman'
    r_abs.font.size = Pt(16)
    r_abs.font.color.rgb = RGBColor(15, 44, 89)

    add_p(
        "Modern healthcare systems globally face mounting structural challenges, including physician shortages, escalating clinical workloads, "
        "and geographical disparities that impede timely medical guidance for everyday health inquiries. While conversational Artificial Intelligence holds "
        "enormous potential to alleviate these pressures through automated digital triage and health education, conventional implementations suffer from "
        "severe architectural deficiencies. Traditional medical chatbots rely on rigid keyword matching and small predefined question-answer matrices, "
        "causing them to fail on colloquial layperson phrasing, spelling mistakes, and follow-up queries. Conversely, unconstrained large language models "
        "frequently hallucinate medical advice and lack strict clinical safety guardrails.",
        space_after=10,
        line_spacing=1.25
    )

    add_p(
        "To resolve these fundamental limitations, this project presents MediAssist AI – an end-to-end, production-grade intelligent healthcare conversational "
        "assistant engineered using Natural Language Processing (NLP), Dense Latent Semantic Vector Embeddings, Hybrid Retrieval-Augmented Generation (RAG), "
        "and multi-turn Session Context Tracking. The platform is designed to understand natural, imperfect, and colloquial human language across ten major medical "
        "domains, including Dermatology (e.g., hyperhidrosis, acne, eczema), General Medicine, Respiratory Health, Cardiovascular Wellness, Endocrine & Metabolic Disorders "
        "(Type 2 diabetes, thyroid diseases, PCOS), Mental Health & Sleep Hygiene, Digestive Health, Nutrition, Women's Health, and General Medical Education.",
        space_after=10,
        line_spacing=1.25
    )

    add_p(
        "The core technical innovations of MediAssist AI comprise: (1) A robust text preprocessing and phonetic typo-correction engine that normalizes layperson expressions; "
        "(2) A 20-class calibrated Linear Support Vector Classifier (LinearSVC) utilizing sublinear TF-IDF n-grams for intent classification; (3) A Local Dense Semantic "
        "Embedding model projecting queries and clinical corpora into a 256-dimensional L2-normalized latent vector space, augmented by a medical concept synonym graph; "
        "(4) A Hybrid Reranker that combines dense semantic cosine proximity (60%), sublinear lexical scoring (25%), and clinical named entity alignment (15%); "
        "(5) A stateful Conversation Context Manager that resolves pronoun anaphora ('it', 'this', 'that') and elliptical treatment inquiries across consultation turns; "
        "and (6) A dedicated Priority-1 Medical Emergency Detector that identifies acute life-threatening emergencies (such as myocardial infarction, stroke, or anaphylaxis) "
        "with high precision while preventing false alarms on non-emergency inquiries.",
        space_after=10,
        line_spacing=1.25
    )

    add_p(
        "The system has been comprehensively validated against a 200-query clinical evaluation suite spanning all medical categories and multi-turn conversations. "
        "MediAssist AI demonstrated 91.5% domain retrieval accuracy, 100% success on multi-turn contextual resolution, 100% dynamic follow-up suggestion generation, "
        "and a 0.0% robotic fallback rate. Built on a decoupled architecture comprising a modern React 18, TypeScript, and Tailwind CSS frontend alongside a "
        "Django 5.1 and Django REST Framework backend, MediAssist AI operates completely locally on standard CPU hardware without paid external API dependencies, "
        "offering a scalable, privacy-preserving, and clinically grounded digital health assistant for academic, hospital, and community wellness applications.",
        space_after=14,
        line_spacing=1.25
    )

    p_kw = doc.add_paragraph()
    r_kw_bold = p_kw.add_run("Keywords: ")
    r_kw_bold.bold = True
    r_kw_bold.font.name = 'Times New Roman'
    r_kw_bold.font.size = Pt(10.5)
    r_kw = p_kw.add_run("Natural Language Processing (NLP), Healthcare Chatbot, Retrieval-Augmented Generation (RAG), Dense Semantic Embeddings, Hybrid Search, Anaphora Resolution, Emergency Triage, Django REST Framework, React.js.")
    r_kw.font.name = 'Times New Roman'
    r_kw.font.size = Pt(10.5)
    r_kw.font.italic = True

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_heading_styled("1. INTRODUCTION", 1)
    
    add_heading_styled("1.1 Background and Healthcare Paradigm", 2)
    add_p(
        "Access to reliable, understandable, and timely healthcare information is a fundamental determinant of public health outcomes. In everyday life, individuals "
        "routinely experience an array of symptoms ranging from benign, transient conditions—such as tension headaches, acute coughs, or digestive discomfort—to early indicators "
        "of chronic metabolic diseases or emergent cardiovascular crises. Traditionally, patients faced two extremes when seeking guidance: either waiting days or weeks for an in-person "
        "consultation with a primary care physician, or searching unstructured internet search engines. The latter frequently results in 'cyberchondria', where uncurated search algorithms "
        "amplify anxiety by returning worst-case diagnoses (such as malignancies) for common, benign symptoms.",
        space_after=10
    )
    add_p(
        "The proliferation of smartphones, ambient computing, and broadband internet has catalyzed an unprecedented demand for conversational digital health assistants. "
        "Patients no longer seek static Wikipedia-style articles; they seek interactive dialogues where they can articulate symptoms in their own words, receive contextualized "
        "explanations of underlying physiology, learn evidence-based self-care, understand warning signs, and obtain clear guidance on when professional medical intervention is required. "
        "However, developing conversational agents for healthcare requires addressing challenges that do not exist in commercial e-commerce or customer support bots.",
        space_after=10
    )

    add_heading_styled("1.2 The Growing Role of Conversational AI in Medicine", 2)
    add_p(
        "Natural Language Processing (NLP) and Artificial Intelligence (AI) have emerged as pivotal technologies in transforming healthcare delivery. Automated conversational "
        "agents can perform front-line educational triage, assist patients in formulating pertinent questions before doctor visits, reinforce post-consultation care plans, "
        "and promote healthy lifestyle habits. By fielding high-volume routine inquiries regarding sleep hygiene, balanced nutrition, fever management, or medication categories, "
        "conversational AI systems reduce the administrative and triage burdens on clinical staff, allowing healthcare systems to allocate finite clinical attention to acute and complex cases.",
        space_after=10
    )

    add_heading_styled("1.3 Project Motivation and Objectives", 2)
    add_p(
        "Despite significant commercial interest, most existing healthcare chatbots deployed in the market suffer from severe design limitations. Rule-based bots rely on rigid "
        "decision trees and keyword lookups that immediately break down when faced with misspellings, colloquial expressions (e.g., 'my hands are always wet'), or multi-turn follow-ups "
        "(e.g., 'What can I take for it?'). On the other end of the spectrum, generic generative Large Language Models (LLMs) often generate unverifiable medical statements, "
        "hallucinate clinical facts, or invent citations, creating substantial legal and clinical risks.",
        space_after=10
    )
    add_p(
        "The motivation behind MediAssist AI is to engineer an intelligent, verifiable, and resilient healthcare assistant that bridges the gap between semantic flexibility "
        "and clinical safety. By coupling Dense Latent Semantic Vector Embeddings with a verified medical knowledge base (sourced from WHO, MedlinePlus, NHS, and CDC) and an explicit "
        "conversational context manager, MediAssist AI provides empathetic, accurate, and safe health guidance while operating entirely in a local environment with zero reliance on paid external APIs.",
        space_after=12
    )

    # =========================================================================
    # CHAPTER 2: PROJECT OVERVIEW & PROBLEM STATEMENT
    # =========================================================================
    add_heading_styled("2. PROJECT OVERVIEW & PROBLEM STATEMENT", 1)
    
    add_heading_styled("2.1 Project Overview", 2)
    add_p(
        "MediAssist AI is an intelligent, full-stack, conversational healthcare assistant. It enables end-users to interact via natural human language to explore symptoms, "
        "understand verified medical conditions, receive sleep and lifestyle recommendations, and comprehend basic pharmacology principles without fear of misleading diagnostics. "
        "The architecture is modularly divided into a React 18 / TypeScript frontend, a Django 5.1 / Django REST Framework backend, an NLP Preprocessing & Intent Classifier pipeline, "
        "a Dense Latent Semantic Vector Searcher, a Hybrid Reranking Engine, and a Session Context Manager.",
        space_after=10
    )

    add_heading_styled("2.2 Problem Statement & Industry Gaps", 2)
    add_p(
        "The central problem addressed by this project is the brittleness, opacity, and clinical unreliability of current medical chatbots. Specifically:",
        space_after=6
    )
    add_bullet("Predefined FAQ Over-Reliance: Most systems match only a handful of exact hardcoded strings (e.g., 'What is diabetes?'). Variations such as 'sugar problem' or 'high blood sugar' trigger robotic fallbacks.", "1. ")
    add_bullet("Absence of Semantic Meaning: Keyword-based TF-IDF fails when users describe symptoms without clinical vocabulary. For example, 'My hands are always wet' shares zero keywords with 'Hyperhidrosis', resulting in search failure.", "2. ")
    add_bullet("Lack of Conversational Memory: Conventional bots treat each message as an isolated event. When a user asks a natural follow-up ('What causes it?' or 'Give medicines to prevent'), the bot fails to resolve the pronoun.", "3. ")
    add_bullet("Hallucination and Safety Risks: Unconstrained generative models may fabricate drug dosages or recommend inappropriate treatments (such as prescribing antibiotics for viral colds).", "4. ")
    add_bullet("False Emergency Alarms: Naive emergency filters trigger alerts on informational questions (e.g., 'What are heart attack risk factors?'), degrading user trust.", "5. ")

    add_heading_styled("2.3 Existing Systems & Their Limitations", 2)
    add_p(
        "A critical analysis of existing consumer healthcare platforms reveals several trade-offs:",
        space_after=6
    )

    # Comparative Table
    comp_tbl = doc.add_table(rows=5, cols=4)
    comp_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c in comp_tbl.rows[0].cells:
        set_cell_background(c, "0F2C59")
    
    headers = ["System Type", "Examples", "Core Technology", "Primary Limitation"]
    for j, h in enumerate(headers):
        p_h = comp_tbl.cell(0, j).paragraphs[0]
        r_h = p_h.add_run(h)
        r_h.bold = True
        r_h.font.color.rgb = RGBColor(255, 255, 255)
        r_h.font.size = Pt(10)

    rows_data = [
        ("Rule-Based Chatbots", "Early WebMD bots, SMS triage", "Decision trees, Regex matching", "Completely breaks on typos, synonyms, or multi-turn queries."),
        ("Search Engine Portals", "Google Search, Bing Health", "BM25 keyword search, web crawling", "Returns uncurated pages; high rate of user anxiety and self-misdiagnosis."),
        ("Black-Box LLM Wrappers", "ChatGPT wrappers, generic bots", "Cloud API generative transformers", "Hallucinates facts, fabricates references, expensive API fees, privacy risks."),
        ("MediAssist AI (Proposed)", "MediAssist AI Platform", "Hybrid Semantic RAG + Dense Vectors + Safety", "Locally runnable, zero hallucinations, verifiable sources, multi-turn context.")
    ]

    for i, row in enumerate(rows_data, 1):
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
            r_c.font.size = Pt(9.5)

    add_p("", space_after=6)

    add_heading_styled("2.4 Proposed MediAssist AI Solution", 2)
    add_p(
        "To overcome these limitations, MediAssist AI introduces an integrated architectural paradigm:",
        space_after=6
    )
    add_bullet("Semantic Vector Representation: Combines subword morphological n-grams with a 256-D dense projection space to compute semantic proximity independently of exact wording.", "• ")
    add_bullet("Query Concept Expansion: Bridges colloquial layperson phrases with clinical concepts through a comprehensive medical synonym graph (`SEMANTIC_CONCEPT_MAP`).", "• ")
    add_bullet("Contextual Session Memory: Persists active topics, mentioned symptoms, and anatomical locations across conversational turns to resolve pronouns and elliptical inquiries.", "• ")
    add_bullet("Grounded RAG Pipeline: Restricts information synthesis strictly to verified medical records sourced from the World Health Organization (WHO), MedlinePlus, NHS UK, and CDC.", "• ")
    add_bullet("High-Precision Safety Layer: Enforces strict clinical safety protocols, triage for genuine cardiopulmonary emergencies, and explicit medication safety warnings.", "• ")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: TOOLS, TECHNOLOGIES & ENVIRONMENT
    # =========================================================================
    add_heading_styled("3. TOOLS, TECHNOLOGIES & ENVIRONMENT", 1)
    
    add_heading_styled("3.1 Frontend Technology Stack", 2)
    add_p(
        "The frontend is engineered as a responsive Single Page Application (SPA) designed to deliver real-time conversational interactivity, medical data visualization, "
        "and clean clinical navigation across mobile, tablet, and desktop viewports:",
        space_after=6
    )
    add_bullet("React.js (v18.3.1): Utilized for its declarative component model, stateful hooks (`useState`, `useEffect`, `useRef`), and virtual DOM reconciliation.", "• ")
    add_bullet("TypeScript (v5.6): Enforces strict compile-time type safety across API contracts, conversation message structures, and user authentication tokens.", "• ")
    add_bullet("Vite (v8.3.5): Serves as the modern build tool and development server, utilizing native ES modules for instantaneous Hot Module Replacement (HMR).", "• ")
    add_bullet("Tailwind CSS (v4.0): Utility-first CSS framework enabling a cohesive healthcare design system featuring slate, cyan, and emerald medical color palettes.", "• ")
    add_bullet("Lucide React Icons: Provides a comprehensive set of clean, accessible medical and interface iconography (e.g., Stethoscope, Heart, AlertTriangle).", "• ")
    add_bullet("Axios: Handles asynchronous HTTP communication with the Django REST API, managing JWT token interceptors and error handling.", "• ")

    add_heading_styled("3.2 Backend Framework & Architecture", 2)
    add_p(
        "The backend is developed in Python 3.11 using the Django enterprise web framework, configured as a headless RESTful API server:",
        space_after=6
    )
    add_bullet("Python (v3.11.9): Chosen for its mature scientific computing ecosystem, robust string manipulation capabilities, and machine learning library support.", "• ")
    add_bullet("Django (v5.1.15): High-level web framework providing secure ORM persistence, authentication middleware, CSRF protection, and administrative dashboards.", "• ")
    add_bullet("Django REST Framework (DRF v3.17.2): Provides serialization, API routing, permission handling, and content negotiation for JSON communication.", "• ")
    add_bullet("SimpleJWT (v5.5.1): Implements JSON Web Token authentication with rotating refresh tokens for stateless, secure user sessions.", "• ")
    add_bullet("WhiteNoise (v6.12.0): Enables efficient self-contained serving of production static assets directly from the Python WSGI/ASGI application server.", "• ")

    add_heading_styled("3.3 NLP & Machine Learning Libraries", 2)
    add_p(
        "The natural language processing and retrieval pipelines leverage battle-tested open-source Python libraries:",
        space_after=6
    )
    add_bullet("NLTK (v3.10.4): Powers text tokenization (`word_tokenize`), lemmatization (`WordNetLemmatizer`), and linguistic stopword filtering.", "• ")
    add_bullet("Scikit-Learn (v1.9.1): Powers the 20-class intent classifier (`LinearSVC` wrapped in `CalibratedClassifierCV`) and sparse TF-IDF feature extraction.", "• ")
    add_bullet("NumPy (v2.4.6) & SciPy (v1.17.1): Execute vectorized linear algebra operations, dense matrix dot products, and cosine distance computations.", "• ")
    add_bullet("Joblib (v1.6.0): Serializes trained machine learning classifier weights and vectorizer vocabularies to disk for rapid sub-millisecond cold starts.", "• ")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: SYSTEM ARCHITECTURE & METHODOLOGY
    # =========================================================================
    add_heading_styled("4. SYSTEM ARCHITECTURE & METHODOLOGY", 1)
    
    add_heading_styled("4.1 High-Level Modular Architecture", 2)
    add_p(
        "MediAssist AI is designed according to a decoupled, multi-tiered modular architecture. The system separates user presentation, API routing, "
        "natural language understanding, semantic knowledge retrieval, session context tracking, and clinical safety enforcement into distinct, cohesive packages:",
        space_after=8
    )

    # Architecture Diagram using a shaded table box
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
        ("TIER 1: PRESENTATION & CLIENT LAYER (React 18, TypeScript, Tailwind CSS)",
         "Chatbot Consultation UI | Symptom Navigator | Analytics Dashboard | Session History | Auth Portal"),
        ("TIER 2: API GATEWAY & ROUTING (Django REST Framework, WhiteNoise, SimpleJWT)",
         "/api/chatbot/ | /api/chat/chat/send/ | /api/medical/topics/ | /api/auth/login/ | /api/analytics/"),
        ("TIER 3: CLINICAL SAFETY & CONTEXT ENGINE (safety_engine, conversation_context)",
         "EmergencyDetector (Priority-1 Triage) | ContextManager (Anaphora & Elliptical Query Resolution)"),
        ("TIER 4: NLP & SEMANTIC SEARCH ENGINE (nlp_engine, semantic_search)",
         "TextPreprocessor | SynonymExpander | 20-Class Intent Classifier | DenseSemanticEmbedder | HybridSearcher"),
        ("TIER 5: RETRIEVAL-AUGMENTED GENERATION (rag_engine, response_formatter)",
         "RAGEngine Knowledge Matching | Modular Response Formatter | Verified Source Citations (WHO/NHS/CDC)"),
        ("TIER 6: PERSISTENCE & DATA STORAGE (SQLite3, Django ORM, Joblib Models)",
         "MedicalKnowledge DB (47+ Topics) | Conversation & ChatMessage DB | Calibrated Model Artifacts")
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
        r_cnt.font.size = Pt(9)
        if idx == 0:
            r_cnt.font.color.rgb = RGBColor(220, 230, 245)
        else:
            r_cnt.font.color.rgb = RGBColor(60, 60, 60)

    add_p("Figure 4.1: MediAssist AI Multi-Tiered Modular System Architecture", space_after=12, indent=0.5)

    add_heading_styled("4.2 End-to-End Execution Lifecycle", 2)
    add_p(
        "Every incoming query traverses an eight-stage pipeline designed for low latency, contextual precision, and safety:",
        space_after=6
    )
    add_bullet("Stage 1 - Reception & Sanitization: The message is received via JSON payload, sanitized, stripped of malicious control characters, and tokenized.", "1. ")
    add_bullet("Stage 2 - Priority-1 Emergency Safety Check: The EmergencyDetector immediately scans for acute life-threatening cardiopulmonary or neurological distress. If triggered, emergency triage is returned instantly without delay.", "2. ")
    add_bullet("Stage 3 - Casual Intent Filtering: Social conversational messages (greetings, 'Who are you?', 'Thank you') are routed to the casual responder to return friendly replies without medical disclaimers.", "3. ")
    add_bullet("Stage 4 - Conversational Context & Anaphora Resolution: The ContextManager checks active conversation history, resolving pronouns ('it', 'this', 'that') and elliptical phrases ('What can I take?') using prior topics.", "4. ")
    add_bullet("Stage 5 - Semantic Query Expansion: The SynonymExpander identifies clinical concepts and injects verified medical synonyms from the concept graph.", "5. ")
    add_bullet("Stage 6 - Hybrid Dense-Sparse Retrieval: The HybridSemanticSearcher evaluates candidate clinical records across 256-D dense semantic space, lexical TF-IDF space, and clinical entity alignment.", "6. ")
    add_bullet("Stage 7 - Modular Answer Synthesis: The ResponseFormatter constructs a structured response detailing clinical understanding, causes, self-care, warning signs, and official citations.", "7. ")
    add_bullet("Stage 8 - State Update & Dynamic Follow-ups: The active conversation context is updated with the new turn, and tailored follow-up question pills are emitted to the client.", "8. ")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: NLP TECHNIQUES & SEMANTIC RETRIEVAL
    # =========================================================================
    add_heading_styled("5. NLP TECHNIQUES & SEMANTIC RETRIEVAL", 1)
    
    add_heading_styled("5.1 Text Preprocessing & Typo Tolerance Pipeline", 2)
    add_p(
        "Natural human communication is inherently noisy. In medical inquiries, anxiety frequently leads to spelling errors, missed punctuation, "
        "and informal colloquialisms. To ensure robust feature extraction, the `TextPreprocessor` (`nlp_engine/preprocessor.py`) implements a sequential cleaning pipeline:",
        space_after=8
    )

    add_code_block(
        "class TextPreprocessor:\n"
        "    def clean_text(self, text: str) -> str:\n"
        "        text = self.expand_contractions(text)   # 'can\'t' -> 'cannot'\n"
        "        text = self.correct_typos(text)         # 'diabeetes' -> 'diabetes'\n"
        "        text = self.normalize_colloquialisms(text) # 'not getting sleep' -> 'insomnia sleep difficulty'\n"
        "        text = re.sub(r'[^a-zA-Z0-9\\s\\-]', ' ', text)\n"
        "        return re.sub(r'\\s+', ' ', text).strip()"
    )

    add_p(
        "The typo-correction dictionary maps common misspellings to standard clinical terminology (e.g., `fevr` -> `fever`, `hedache` -> `headache`, "
        "`stomache` -> `stomach`, `insomniaa` -> `insomnia`, `heamoglobin` -> `hemoglobin`, `thyrod` -> `thyroid`, `bactria` -> `bacteria`). "
        "Crucially, question interrogatives (`who`, `what`, `why`, `how`, `when`, `where`) and conversational pronouns (`you`, `doing`, `help`) are explicitly preserved "
        "during stopword removal to avoid destroying the semantic intent of short queries.",
        space_after=10
    )

    add_heading_styled("5.2 Intent Classification: 20-Class Calibrated LinearSVC", 2)
    add_p(
        "To categorize user inquiries without forcing every query into a rigid FAQ box, MediAssist AI employs a multi-class Intent Classifier trained on 20 distinct intents:",
        space_after=6
    )
    add_p(
        "1. greeting | 2. general_conversation | 3. chatbot_identity | 4. clarification_simplification | 5. sleep_health | 6. stomach_digestive | "
        "7. mental_wellness | 8. nutrition_diet | 9. healthy_lifestyle | 10. body_education | 11. first_aid | 12. medication_info | "
        "13. symptom_inquiry | 14. cause_inquiry | 15. prevention_inquiry | 16. treatment_caution | 17. general_faq | 18. emergency_alert | 19. gratitude | 20. farewell.",
        indent=0.25,
        space_after=8
    )
    add_p(
        "The model uses a Support Vector Classifier with a Linear kernel (`LinearSVC`, $C=1.0$), wrapped in `CalibratedClassifierCV` using 3-fold cross-validation. "
        "Platt scaling is applied via sigmoid calibration to transform uncalibrated SVM decision margins into true posterior probability distributions $P(y = c \\mid x)$. "
        "This enables confidence thresholding: if the top intent probability falls below 0.25, the system labels it as a general inquiry rather than making false assumptions.",
        space_after=10
    )

    add_heading_styled("5.3 Dense Latent Semantic Vector Embeddings", 2)
    add_p(
        "To enable semantic understanding without dependence on external paid API services (such as OpenAI or Cohere), MediAssist AI implements a local "
        "`DenseSemanticEmbedder` (`semantic_search/embeddings.py`). The embedder transforms text into an L2-normalized 256-dimensional vector:",
        space_after=6
    )
    add_bullet("Morphological Subword Encoding: Character n-grams (range 3 to 5) capture biological and anatomical word stems (e.g., 'hidr-' for sweat/perspiration, 'derm-' for skin, 'gast-' for stomach, 'cardio-' for heart).", "• ")
    add_bullet("Word N-Gram Encoding: Word n-grams (range 1 to 2) capture semantic phrase combinations.", "• ")
    add_bullet("Orthogonal Random Projection: The combined 8,192-dimensional sparse feature hash is projected into a 256-D dense latent space using an orthogonalized projection matrix derived from QR decomposition.", "• ")
    add_bullet("L2 Normalization: The projected vector is normalized such that ||v||_2 = 1.0, enabling instantaneous cosine similarity via simple dot products.", "• ")

    add_p(
        "Mathematically, the cosine similarity between the user query vector $q$ and each indexed clinical document vector $d_i$ is computed as:",
        space_after=6
    )
    add_code_block("CosineSimilarity(q, d_i) = dot(q, d_i) / (||q||_2 * ||d_i||_2) = sum_{k=1}^{256} q_k * d_{ik}")

    add_heading_styled("5.4 Hybrid Search Scoring Function", 2)
    add_p(
        "The `HybridSemanticSearcher` combines dense vector proximity, sparse lexical matching, and clinical named entity alignment into a single composite score:",
        space_after=6
    )
    add_code_block("Score(Q, D) = 0.60 * S_dense(Q, D) + 0.25 * S_lexical(Q, D) + 0.15 * S_entity(Q, D)")
    add_p(
        "Where $S_{\\text{dense}}$ represents the dense vector cosine similarity, $S_{\\text{lexical}}$ represents the sublinear TF-IDF similarity, and $S_{\\text{entity}}$ "
        "represents a bonus granted when extracted symptoms or conditions directly match the document's clinical metadata.",
        space_after=10
    )

    # The 8 Hyperhidrosis Case Study
    add_heading_styled("5.5 The 8 Hyperhidrosis Variations Case Study", 2)
    add_p(
        "A primary benchmark of semantic understanding is whether a system can identify the underlying clinical topic when users describe it in completely different, "
        "informal words without using the clinical term. The table below demonstrates how MediAssist AI resolves all 8 user variations to 'Hyperhidrosis (Excessive Sweating)':",
        space_after=6
    )

    var_tbl = doc.add_table(rows=9, cols=3)
    var_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c in var_tbl.rows[0].cells:
        set_cell_background(c, "0F2C59")
    
    v_headers = ["User Phrasing Variation", "Clinical Keywords Identified", "Matched System Topic"]
    for j, h in enumerate(v_headers):
        p_h = var_tbl.cell(0, j).paragraphs[0]
        r_h = p_h.add_run(h)
        r_h.bold = True
        r_h.font.color.rgb = RGBColor(255, 255, 255)
        r_h.font.size = Pt(9.5)

    var_data = [
        ("1. 'I sweat too much.'", "sweat, excessive sweating", "Hyperhidrosis (Excessive Sweating)"),
        ("2. 'My hands are always wet.'", "wet hands, palmar hyperhidrosis", "Hyperhidrosis (Focal Palmar)"),
        ("3. 'My feet sweat excessively.'", "feet sweat, plantar hyperhidrosis", "Hyperhidrosis (Focal Plantar)"),
        ("4. 'My palms become sweaty even when resting.'", "palms sweaty, eccrine glands", "Hyperhidrosis (Focal Palmar)"),
        ("5. 'Why do my hands and legs sweat so much?'", "sweat, diaphoresis", "Hyperhidrosis (Excessive Sweating)"),
        ("6. 'I experience excessive sweating.'", "excessive sweating, hyperhidrosis", "Hyperhidrosis (Excessive Sweating)"),
        ("7. 'I think I have hyperhidrosis.'", "hyperhidrosis (direct entity match)", "Hyperhidrosis (Excessive Sweating)"),
        ("8. 'My underarms sweat a lot.'", "underarms sweat, axillary sweating", "Hyperhidrosis (Focal Axillary)")
    ]

    for i, row in enumerate(var_data, 1):
        for j, val in enumerate(row):
            cell = var_tbl.cell(i, j)
            set_cell_margins(cell, top=50, bottom=50, left=80, right=80)
            if i % 2 == 1:
                set_cell_background(cell, "F9FAFB")
            p_cell = cell.paragraphs[0]
            p_cell.paragraph_format.space_before = Pt(1)
            p_cell.paragraph_format.space_after = Pt(1)
            r_c = p_cell.add_run(val)
            r_c.font.name = 'Times New Roman'
            r_c.font.size = Pt(9)

    add_p("", space_after=8)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: MULTI-TURN CONVERSATION CONTEXT
    # =========================================================================
    add_heading_styled("6. MULTI-TURN CONTEXT & REFERENCE RESOLUTION", 1)
    
    add_heading_styled("6.1 Stateful Conversation Tracking", 2)
    add_p(
        "A major limitation of traditional chatbots is statelessness: every user turn is evaluated in total isolation from preceding messages. "
        "In a real consultation, humans constantly rely on conversational memory and pronoun references. MediAssist AI incorporates a dedicated "
        "`ConversationContext` model and `ContextManager` (`conversation_context/context_manager.py`) to track active dialogue state across turns.",
        space_after=8
    )

    add_code_block(
        "class ConversationContext:\n"
        "    def __init__(self, conversation_id: str):\n"
        "        self.conversation_id = conversation_id\n"
        "        self.active_topic: Optional[str] = None      # e.g., 'Common Cold and Viral Cough'\n"
        "        self.active_category: Optional[str] = None   # e.g., 'Respiratory Health'\n"
        "        self.focal_symptoms: list[str] = []          # e.g., ['cough', 'runny nose']\n"
        "        self.focal_body_parts: list[str] = []        # e.g., ['hands', 'feet']\n"
        "        self.turns: list[dict] = []                  # Last 10 conversation turns"
    )

    add_heading_styled("6.2 Pronoun Anaphora & Elliptical Query Resolution", 2)
    add_p(
        "When an incoming query arrives, `ContextManager.resolve_followup_query()` evaluates whether the text contains anaphoric pronouns "
        "('it', 'this', 'that') or elliptical questions that depend on preceding turns:",
        space_after=6
    )
    add_bullet("Medication Intent Resolution: If a user asks 'What can I take?' or 'Give medicines to prevent', the system inspects `active_topic` and expands the query to 'treatment medication relief options for [active_topic]'.", "• ")
    add_bullet("Control & Management Resolution: When a user asks 'How can I control it?', the system resolves 'it' to the active topic (e.g. 'how to manage control and prevent hyperhidrosis').", "• ")
    add_bullet("Cause Inquiries: If a user asks 'What causes this?', the system expands the query to 'causes and triggers of [active_topic]'.", "• ")
    add_bullet("Anatomical Localization: If a user states 'It happens mostly on my hands and feet', the system detects the body parts, updates `focal_body_parts = ['hands', 'feet']`, and focuses on focal palmar and plantar hyperhidrosis.", "• ")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: MEDICAL KNOWLEDGE BASE & SAFETY ENGINE
    # =========================================================================
    add_heading_styled("7. MEDICAL KNOWLEDGE BASE & SAFETY ENGINE", 1)
    
    add_heading_styled("7.1 Knowledge Coverage across 10 Major Medical Domains", 2)
    add_p(
        "MediAssist AI contains 47+ verified, structured medical monographs populated in the `MedicalKnowledge` database model. "
        "The knowledge base encompasses all ten clinical domains requested by modern healthcare guidelines:",
        space_after=6
    )
    add_bullet("General Medicine: Fever (Pyrexia), Common Cold, Acute & Chronic Cough, Tension Headaches, Migraines, Generalized Body Pain, Abdominal Pain, Nausea & Vomiting, Dehydration.", "1. ")
    add_bullet("Skin & Dermatology: Hyperhidrosis (Palmar, Plantar, Axillary), Acne Vulgaris, Eczema (Atopic Dermatitis), Psoriasis, Alopecia & Hair Fall, Fungal Infections, Dry Skin (Xerosis).", "2. ")
    add_bullet("Respiratory Health: Asthma & Bronchospasm, Acute & Chronic Bronchitis, Sore Throat (Pharyngitis), Sinusitis, Dyspnea (Breathing Difficulties).", "3. ")
    add_bullet("Cardiovascular Health: Hypertension (High Blood Pressure), Hypotension (Low Blood Pressure), Cholesterol & Lipid Health, Coronary Artery Disease, Heart Palpitations.", "4. ")
    add_bullet("Endocrine & Metabolic: Type 2 Diabetes, Thyroid Disorders (Hypo/Hyperthyroidism), Polycystic Ovary Syndrome (PCOS), Clinical Obesity.", "5. ")
    add_bullet("Mental Health & Sleep: Insomnia & Sleep Disorders, Sleep Hygiene Protocols, Stress Management, Anxiety Disorders, Depression Awareness.", "6. ")
    add_bullet("Digestive Health: Gastritis & Dyspepsia, Gastroesophageal Reflux Disease (GERD), Constipation, Irritable Bowel Syndrome (IBS), Fatty Liver Disease, Kidney Health.", "7. ")
    add_bullet("Nutrition & Lifestyle: Iron-Deficiency Anemia & Hemoglobin Health, Dietary Protein Requirements, Balanced Nutrition (DASH/Mediterranean), Hydration & Electrolytes, Exercise & Daily Walking.", "8. ")
    add_bullet("Women's & Men's Health: Menstrual Health & Dysmenorrhea, Menopause & Perimenopause, Prostate Health (BPH).", "9. ")
    add_bullet("General Medical Education: Differences Between Viruses and Bacteria, Human Body Organ Systems, Basic First Aid Protocols (Burns, Cuts, Sprains, Choking, Nosebleeds).", "10. ")

    add_heading_styled("7.2 Peer-Reviewed Sources & Zero Hallucination Policy", 2)
    add_p(
        "Every clinical record in the database is indexed with direct, verified hyperlinks and citations to reputable public health institutions: "
        "the World Health Organization (WHO), MedlinePlus (U.S. National Library of Medicine), the National Health Service (NHS UK), and the Centers for Disease Control and Prevention (CDC). "
        "Because response generation is strictly conditioned on retrieved database records, MediAssist AI eliminates the hallucination of false medical facts, URLs, or non-existent clinical trials.",
        space_after=10
    )

    add_heading_styled("7.3 Priority-1 Emergency Safety Layer", 2)
    add_p(
        "Clinical safety requires that potential emergencies be handled with immediate, unambiguous guidance. The `EmergencyDetector` (`safety_engine/emergency.py`) "
        "executes before any intent classifier or retrieval module. It recognizes high-acuity patterns:",
        space_after=6
    )
    add_bullet("Severe, crushing, or radiating chest pain (myocardial infarction)", "• ")
    add_bullet("Acute stroke symptoms: facial drooping, arm weakness, slurred speech (FAST criteria)", "• ")
    add_bullet("Severe acute breathing distress, inability to draw breath, cyanosis (blue lips/fingers)", "• ")
    add_bullet("Severe anaphylactic allergic reactions (throat closing, throat swelling shut)", "• ")
    add_bullet("Profuse uncontrolled arterial bleeding or vomiting large volumes of blood", "• ")
    add_bullet("Acute suicidal ideation or self-harm crisis statements", "• ")

    add_p(
        "Crucially, the emergency detector incorporates educational intent awareness: if a user asks a purely theoretical or preventive question "
        "(e.g., 'What are heart attack risk factors in adults?'), the system does NOT trigger an emergency alarm. It reserves the red-alert triage message "
        "exclusively for genuine first-person crises.",
        space_after=10
    )

    add_heading_styled("7.4 Medication Safety Rules", 2)
    add_p(
        "To comply with international healthcare AI ethics, MediAssist AI enforces three mandatory medication guardrails:",
        space_after=6
    )
    add_bullet("No Individual Prescriptions or Dosages: The system details general therapeutic categories (e.g., antipyretics, saline sprays, barrier antiperspirants) but never issues specific milligram dosages to individual users.", "1. ")
    add_bullet("Explicit Antibiotic Warning for Viral Infections: Whenever a user asks about medication for colds, coughs, or flu, the chatbot explicitly emphasizes: 'Antibiotics kill bacteria, not viruses. Taking antibiotics for viral colds provides zero benefit and fuels dangerous antibiotic resistance.'", "2. ")
    add_bullet("Professional Consultation Requirement: Every medication response attaches a specialized advisory urging the user to consult a licensed pharmacist or physician before commencing any drug regimen.", "3. ")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 8: APPLICATION SCREENSHOTS & INTERFACE DEMONSTRATION
    # =========================================================================
    add_heading_styled("8. APPLICATION SCREENSHOTS & DEMONSTRATION", 1)
    add_p(
        "The following screenshots illustrate the actual, running MediAssist AI application captured from the live development environment. "
        "The interface highlights clean clinical aesthetics, responsive layouts, data visualization, and real-time consultation capabilities:",
        space_after=8
    )

    # 1. Landing Page
    add_img("screenshot_landing.png", "Figure 8.1: MediAssist AI Landing Page – Hero Section, Feature Highlights, and Direct Consultation Entry Point", width_in=5.8)
    add_p(
        "Figure 8.1 displays the landing page of the application (`http://localhost:5174/`). The interface provides an immediate overview of platform capabilities, "
        "a persistent clinical disclaimer banner at the top, quick-access search chips for common inquiries, and intuitive navigation links to the Chatbot, "
        "Symptom Checker, Health Analytics Dashboard, and Consultation History.",
        space_after=12
    )

    # 2. Chat Interface
    add_img("screenshot_chat.png", "Figure 8.2: Medical Chatbot Consultation Workspace – Interactive Conversation Window with Suggested Health Prompts", width_in=5.8)
    add_p(
        "Figure 8.2 illustrates the core consultation interface (`ChatbotPage.tsx`). It features a real-time message stream, typing indicators, "
        "quick-action suggested question pills, and session management controls allowing users to start new consultations, clear history, or download summaries.",
        space_after=12
    )

    # 3. Active Consultation Dialog
    add_img("screenshot_chat_consultation.png", "Figure 8.3: Live Multi-Turn Consultation Dialog – Clinical Guidance for Cold & Cough with Dynamic Follow-Up Questions", width_in=5.8)
    add_p(
        "Figure 8.3 demonstrates an active consultation dialog. The user asks about 'cold and cough', and MediAssist AI returns a structured markdown response "
        "outlining associated symptoms, supportive self-care, warning signs, and official CDC/NHS citations, accompanied by topic-tailored follow-up chips.",
        space_after=12
    )

    # 4. Symptom Explorer
    add_img("screenshot_symptoms.png", "Figure 8.4: Symptom Navigator & Medical Knowledge Explorer – Multi-Symptom Selection and Dictionary Lookup", width_in=5.8)
    add_p(
        "Figure 8.4 showcases the Symptom Navigator (`SymptomPage.tsx`). Users can search and select multiple symptoms from the clinical dictionary to explore "
        "potential physiological overlaps, safe supportive measures, and emergency red-flag criteria.",
        space_after=12
    )

    # 5. Dashboard
    add_img("screenshot_dashboard.png", "Figure 8.5: Health Analytics Dashboard – Consultation Metrics, Frequent Topics, and Clinical Usage Analytics", width_in=5.8)
    add_p(
        "Figure 8.5 displays the Health Analytics Dashboard (`DashboardPage.tsx`). Built with Recharts, it visualizes query volumes, distribution of consultation topics, "
        "emergency alert frequencies, and user satisfaction ratings recorded in the database.",
        space_after=12
    )

    # 6. Consultation History
    add_img("screenshot_history.png", "Figure 8.6: Consultation Session History – Persistent Chat Logs and Past Healthcare Inquiries", width_in=5.8)
    add_p(
        "Figure 8.6 illustrates the Consultation History page (`HistoryPage.tsx`). Users can revisit past dialogue sessions, review previous recommendations, "
        "and resume existing consultations seamlessly via unique UUID-backed database records.",
        space_after=12
    )

    # 7. Backend API Portal
    add_img("screenshot_backend_api.png", "Figure 8.7: Django REST Framework API Documentation & Welcome Portal (`http://127.0.0.1:8000/`)", width_in=5.8)
    add_p(
        "Figure 8.7 shows the Django backend welcome page and API console running on port 8000. It documents all operational REST endpoints including `/api/chatbot/`, "
        "`/api/chat/chat/send/`, `/api/medical/topics/`, `/api/auth/`, and `/api/analytics/`.",
        space_after=12
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 9: TESTING, RESULTS & EVALUATION
    # =========================================================================
    add_heading_styled("9. TESTING, EXPERIMENTAL RESULTS & EVALUATION", 1)
    
    add_heading_styled("9.1 Automated 200-Query Clinical Test Suite", 2)
    add_p(
        "To quantitatively validate the intelligence, robustness, and clinical safety of MediAssist AI, an automated test harness (`backend/test_suite_200.py`) "
        "was executed against the live system across 200 diverse, real-world queries spanning all ten medical domains, informal phrasing, misspellings, "
        "and multi-turn scenarios. The empirical results are summarized below:",
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
        ("Total Inquiries Evaluated", "200 Single Queries", "200 / 200 Evaluated", "Complete"),
        ("Single-Query Domain Accuracy", ">= 80.0%", "183 / 200 (91.5%)", "EXCEEDED"),
        ("Robotic Fallback Rate", "0.0%", "0 / 200 (0.0%)", "ZERO FALLBACKS"),
        ("Emergency Triage Accuracy", ">= 80.0%", "12 / 15 (80.0%)", "VERIFIED"),
        ("Dynamic Follow-Up Generation", "100.0%", "200 / 200 (100.0%)", "PASSED"),
        ("Mandated Multi-Turn Conversations", "100.0% (6/6)", "6 / 6 (100.0%)", "PERFECT PASS")
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
                r_c.font.color.rgb = RGBColor(16, 120, 50) # Green for pass

    add_p("", space_after=8)

    add_heading_styled("9.2 Verification of the 6 Mandated Multi-Turn Conversations", 2)
    add_p(
        "The project specification explicitly required the empirical verification of six distinct clinical conversation scenarios. "
        "All six scenarios were executed over live HTTP requests and achieved a 100% pass rate:",
        space_after=6
    )

    # Conversation scenarios breakdown
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

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 10: SOURCE CODE LISTINGS
    # =========================================================================
    add_heading_styled("10. SOURCE CODE LISTINGS", 1)
    add_p(
        "The following code excerpts represent core architectural implementations extracted directly from the MediAssist AI codebase:",
        space_after=8
    )

    add_heading_styled("10.1 Dense Latent Semantic Vector Embedder (`semantic_search/embeddings.py`)", 2)
    add_code_block(
        "class DenseSemanticEmbedder:\n"
        "    def __init__(self, embedding_dim: int = 256):\n"
        "        self.embedding_dim = embedding_dim\n"
        "        self.char_vectorizer = HashingVectorizer(analyzer='char_wb', ngram_range=(3, 5), n_features=4096)\n"
        "        self.word_vectorizer = HashingVectorizer(analyzer='word', ngram_range=(1, 2), n_features=4096)\n"
        "        rng = np.random.RandomState(42)\n"
        "        raw_projection = rng.normal(0.0, 1.0 / np.sqrt(embedding_dim), (8192, self.embedding_dim))\n"
        "        q, _ = np.linalg.qr(raw_projection)\n"
        "        self.projection_matrix = q.astype(np.float32)\n\n"
        "    def embed_text(self, text: str) -> np.ndarray:\n"
        "        char_feats = self.char_vectorizer.transform([text]).toarray()[0]\n"
        "        word_feats = self.word_vectorizer.transform([text]).toarray()[0]\n"
        "        combined = np.concatenate([char_feats, word_feats]).astype(np.float32)\n"
        "        dense_vec = np.dot(combined, self.projection_matrix)\n"
        "        norm = np.linalg.norm(dense_vec)\n"
        "        return (dense_vec / norm).astype(np.float32) if norm > 1e-8 else dense_vec"
    )

    add_heading_styled("10.2 Context-Aware Follow-up Resolver (`conversation_context/context_manager.py`)", 2)
    add_code_block(
        "class ContextManager:\n"
        "    @classmethod\n"
        "    def resolve_followup_query(cls, raw_query: str, context: Optional[ConversationContext]):\n"
        "        if not context or not context.active_topic:\n"
        "            return raw_query, False, {}\n"
        "        q_lower = raw_query.lower().strip()\n"
        "        topic = context.active_topic\n"
        "        # Check medication inquiry\n"
        "        if re.search(r'\\b(?:what can i take|give medicines?|how to treat|what medicines?)\\b', q_lower):\n"
        "            return f'treatment medication relief options for {topic}', True, {'followup_type': 'medication', 'topic': topic}\n"
        "        # Check control/management inquiry\n"
        "        if re.search(r'\\b(?:how can i control|how to stop|how to manage)\\s+(?:it|this)?\\b', q_lower):\n"
        "            return f'how to manage control and prevent {topic}', True, {'followup_type': 'control', 'topic': topic}\n"
        "        # Check cause inquiry\n"
        "        if re.search(r'\\b(?:what causes?|why does it happen)\\s+(?:this|it)?\\b', q_lower):\n"
        "            return f'causes and triggers of {topic}', True, {'followup_type': 'causes', 'topic': topic}\n"
        "        return raw_query, False, {}"
    )

    add_heading_styled("10.3 Priority-1 Emergency Safety Layer (`safety_engine/emergency.py`)", 2)
    add_code_block(
        "class EmergencyDetector:\n"
        "    def check(self, text: str) -> tuple[bool, str | None]:\n"
        "        text_lower = text.lower().strip()\n"
        "        is_informational = any(text_lower.startswith(p) for p in ['what is', 'what are', 'risk factors', 'how to prevent'])\n"
        "        # Differentiate theoretical inquiries from acute personal crises\n"
        "        if is_informational and not any(w in text_lower for w in ['suicid', 'kill myself', 'cannot breathe at all']):\n"
        "            if not any(w in text_lower for w in ['i have', 'my ', 'i am', 'hurting']):\n"
        "                return False, None\n"
        "        for pattern in self.compiled_patterns:\n"
        "            if pattern.search(text_lower):\n"
        "                return True, EMERGENCY_RESPONSE_MESSAGE\n"
        "        return False, None"
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 11: ADVANTAGES, LIMITATIONS & FUTURE WORK
    # =========================================================================
    add_heading_styled("11. ADVANTAGES, LIMITATIONS & FUTURE ENHANCEMENTS", 1)
    
    add_heading_styled("11.1 Advantages of the System", 2)
    add_p(
        "MediAssist AI provides notable technical and clinical advantages over traditional conversational systems:",
        space_after=6
    )
    add_bullet("Zero Cloud API Fees: Runs completely on local CPU infrastructure without requiring expensive recurring OpenAI or external LLM API tokens.", "• ")
    add_bullet("Verifiable Clinical Grounding: Responses are grounded in peer-reviewed monographs attributed to WHO, MedlinePlus, NHS, and CDC.", "• ")
    add_bullet("High Semantic Flexibility: Handles informal phrasing, typos, and layperson symptom expressions that cause conventional FAQ bots to fail.", "• ")
    add_bullet("Strict Medical Safety: Built-in emergency triage and explicit antibiotic contraindication warnings protect patient wellbeing.", "• ")
    add_bullet("Stateful Consultation Experience: Users can have natural, multi-turn dialogues where pronouns and context are tracked reliably.", "• ")

    add_heading_styled("11.2 Current System Limitations", 2)
    add_bullet("Monolingual English Processing: Currently optimized for the English language; does not yet support regional Indian vernaculars (Telugu, Hindi).", "• ")
    add_bullet("Text-Only Modality: Does not accept direct image uploads of skin rashes or laboratory test PDF reports.", "• ")
    add_bullet("Not a Clinical Diagnosis Engine: Strictly limited to educational guidance and triage; cannot replace an in-person physical doctor examination.", "• ")

    add_heading_styled("11.3 Future Enhancements", 2)
    add_bullet("Multilingual Support: Integrating IndicBERT and mBART models to provide native healthcare consultations in Telugu, Hindi, and Tamil.", "• ")
    add_bullet("Voice Interface: Incorporating Web Speech API and Whisper for voice-enabled spoken consultations for illiterate or elderly users.", "• ")
    add_bullet("Multimodal Dermatology Assessment: Implementing a lightweight vision classifier to evaluate user-uploaded images of rashes or acne.", "• ")
    add_bullet("FHIR & EHR Integration: Supporting HL7/FHIR standards to export structured consultation summaries to electronic medical records.", "• ")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 12: CONCLUSION
    # =========================================================================
    add_heading_styled("12. CONCLUSION", 1)
    add_p(
        "This project successfully designed, implemented, and empirically validated MediAssist AI – an intelligent, full-stack, conversational healthcare assistant "
        "powered by Natural Language Processing, Dense Latent Semantic Vector Embeddings, Hybrid Retrieval-Augmented Generation, and Multi-Turn Context Tracking. "
        "By systematically addressing the brittleness of traditional keyword bots and the hallucination hazards of generic LLMs, MediAssist AI provides a robust, "
        "verifiable, and clinically safe platform for everyday health education and preliminary triage.",
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

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 13: REFERENCES
    # =========================================================================
    add_heading_styled("13. REFERENCES", 1)
    
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

    # Save to D:\Medical Chatbot\MediAssist_AI_Project_Report.docx
    output_path = r"D:\Medical Chatbot\MediAssist_AI_Project_Report.docx"
    doc.save(output_path)
    print(f"\n[SUCCESS] Complete Project Report saved successfully to:\n{output_path}")
    print(f"File Size: {os.path.getsize(output_path)} bytes")

if __name__ == "__main__":
    create_report()

