from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

def create_geotech_pdf(filename):
    # Setup the document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        spaceAfter=20
    )
    heading_style = styles['Heading2']
    subheading_style = styles['Heading3']
    body_style = styles['Normal']
    body_style.spaceAfter = 10

    # The content we want to add
    story = []

    # --- Document Title ---
    story.append(Paragraph("Geotechnical Engineering Problem Solutions", title_style))
    
    # --- Problem 1 ---
    story.append(Paragraph("Problem 1: Effective Stress Calculation", heading_style))
    
    p1_given = """<b>Given:</b><br/>
    * Surface Sand layer: H = 4.0 m, Unit weight (gamma) = 17 kN/m³<br/>
    * Intermediate Clay layer: H = 3.0 m, Unit weight (gamma) = 19 kN/m³<br/>
    * Bottom Gravel layer: H = 4.0 m, Unit weight (gamma) = 18.5 kN/m³<br/>
    * Water table: At the top of the clay layer (depth z = 4.0 m)<br/>
    * Surcharge load: q = 59 kN/m²<br/>
    * Unit weight of water: gamma_w = 9.81 kN/m³"""
    story.append(Paragraph(p1_given, body_style))

    p1_principle = """<b>Principle of Effective Stress:</b><br/>
    Effective Stress (sigma') = Total Stress (sigma) - Pore Water Pressure (u)<br/><br/>
    <b>The 'Immediately After' Condition (t = 0):</b><br/>
    * <b>Sand and Gravel:</b> Free-draining. Surcharge directly increases effective stress.<br/>
    * <b>Clay:</b> Undrained condition at t=0. Excess pore water pressure equals the surcharge load (59 kN/m²). The change in effective stress is zero."""
    story.append(Paragraph(p1_principle, body_style))

    story.append(Paragraph("Calculations by Depth:", subheading_style))
    
    calc_text = """
    <b>1. At Ground Surface (z = 0.0 m)</b><br/>
    * Total Stress = 59 kN/m² (Surcharge only)<br/>
    * Pore Pressure = 0 kN/m²<br/>
    * Effective Stress = <b>59 kN/m²</b><br/><br/>
    
    <b>2. At Sand-Clay Interface (z = 4.0 m)</b><br/>
    <i>Just above (in Sand):</i><br/>
    * Total Stress = 59 + (4.0 * 17) = 127 kN/m²<br/>
    * Pore Pressure = 0 kN/m²<br/>
    * Effective Stress = <b>127 kN/m²</b><br/>
    <i>Just below (in Clay):</i><br/>
    * Total Stress = 127 kN/m²<br/>
    * Pore Pressure = 0 (static) + 59 (excess) = 59 kN/m²<br/>
    * Effective Stress = 127 - 59 = <b>68 kN/m²</b><br/><br/>

    <b>3. At Clay-Gravel Interface (z = 7.0 m)</b><br/>
    <i>Just above (in Clay):</i><br/>
    * Total Stress = 127 + (3.0 * 19) = 184 kN/m²<br/>
    * Pore Pressure = (3.0 * 9.81) + 59 = 88.43 kN/m²<br/>
    * Effective Stress = 184 - 88.43 = <b>95.57 kN/m²</b><br/>
    <i>Just below (in Gravel):</i><br/>
    * Total Stress = 184 kN/m²<br/>
    * Pore Pressure = 29.43 kN/m² (excess pressure is 0)<br/>
    * Effective Stress = 184 - 29.43 = <b>154.57 kN/m²</b><br/><br/>

    <b>4. At Bottom of Gravel Layer (z = 11.0 m)</b><br/>
    * Total Stress = 184 + (4.0 * 18.5) = 258 kN/m²<br/>
    * Pore Pressure = 7.0 * 9.81 = 68.67 kN/m²<br/>
    * Effective Stress = 258 - 68.67 = <b>189.33 kN/m²</b>
    """
    story.append(Paragraph(calc_text, body_style))
    story.append(Spacer(1, 20)) # Adds visual space between problems

    # --- Problem 2 ---
    story.append(Paragraph("Problem 2: Consolidation Time", heading_style))
    
    p2_given = """<b>Given:</b><br/>
    * Clay layer thickness (H) = 4 m = 400 cm<br/>
    * Permeable top, impervious bottom -> <b>Single Drainage</b><br/>
    * Drainage path (d) = H = 400 cm<br/>
    * Coefficient of consolidation (Cv) = 0.03 cm²/min<br/>
    * Final expected settlement (Sf) = 8 cm"""
    story.append(Paragraph(p2_given, body_style))

    story.append(Paragraph("i. Time for 80% total settlement", subheading_style))
    p2_part1 = """Degree of consolidation (U) = 80%. Because U > 60%, we use the logarithmic formula.<br/>
    * Time Factor (Tv) = 1.781 - 0.933 * log10(100 - 80) = 0.567<br/>
    * Time (t) = (Tv * d²) / Cv<br/>
    * t = (0.567 * 400²) / 0.03 = 3,024,000 minutes<br/>
    * <b>t = 2,100 days</b> (approx. 5.75 years)"""
    story.append(Paragraph(p2_part1, body_style))

    story.append(Paragraph("ii. Time required for a settlement of 4 cm", subheading_style))
    p2_part2 = """Degree of consolidation (U) = St / Sf = 4 / 8 = 0.50 (or 50%).<br/>
    Because U is less than or equal to 60%, we use the parabolic formula.<br/>
    * Time Factor (Tv) = (pi / 4) * (0.50)² = 0.196<br/>
    * Time (t) = (Tv * d²) / Cv<br/>
    * t = (0.196 * 400²) / 0.03 = 1,045,333 minutes<br/>
    * <b>t = 726 days</b> (approx. 2 years)"""
    story.append(Paragraph(p2_part2, body_style))

    # Build the PDF
    doc.build(story)
    print(f"PDF successfully generated: {filename}")

if __name__ == "__main__":
    output_filename = "Geotechnical_Engineering_Solutions.pdf"
    create_geotech_pdf(output_filename)