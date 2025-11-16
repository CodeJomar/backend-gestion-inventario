from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageTemplate, Frame
from reportlab.lib.units import inch
from datetime import datetime


def generar_pdf_movimiento(movimiento, producto):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.4*inch,
        leftMargin=0.4*inch,
        topMargin=0.5*inch,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Heading1"],
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#333333"),
        alignment=1,
        spaceBefore=0,
        spaceAfter=0,
        fontName="Helvetica-Bold",
    )

    section_title_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontSize=12,
        leading=14,
        textColor=colors.HexColor("#1a959f"),
        spaceBefore=12,
        spaceAfter=6,
        fontName="Helvetica-Bold",
        leftIndent=30,
    )

    label_style = ParagraphStyle(
        "LabelStyle",
        parent=styles["Normal"],
        fontSize=10,
        leading=12,
        textColor=colors.HexColor("#333333"),
        fontName="Helvetica-Bold",
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontSize=10,
        leading=12,
        textColor=colors.HexColor("#555555"),
    )

    elements = []

    elements.append(Spacer(1, 0.5*inch))

    header_data = [[
        Paragraph("", styles["Normal"]),
        Paragraph("DETALLE - MOV", title_style),
        Paragraph("", styles["Normal"]),
    ]]
    
    header_t = Table(header_data, colWidths=[2*inch, 4*inch, 2*inch])
    header_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#1a959f")),
        ("BACKGROUND", (1, 0), (1, 0), colors.white),
        ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#1a959f")),
        ("ALIGN", (1, 0), (1, 0), "CENTER"),  # changed from RIGHT to CENTER
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0, colors.white),
        ("ROWHEIGHT", (0, 0), (-1, -1), 50),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(header_t)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Factura a:", section_title_style))
    elements.append(Spacer(1, 12))

    fecha_completa = movimiento.get("created_at", "N/A")
    fecha_str = "N/A"
    hora_str = "N/A"
    
    if fecha_completa and fecha_completa != "N/A":
        try:
            fecha_obj = datetime.fromisoformat(str(fecha_completa).replace('Z', '+00:00'))
            fecha_str = fecha_obj.strftime("%d/%m/%Y")
            hora_str = fecha_obj.strftime("%H:%M:%S")
        except:
            fecha_str = str(fecha_completa)

    factura_data = [
        [
            Paragraph(f"<b>Nombre</b><br/>{movimiento.get('created_by', 'Desconocido')}", normal_style),
            Paragraph(f"<b>ID Movimiento</b><br/>{movimiento.get('id', 'N/A')}", normal_style),
        ],
        [
            Paragraph(f"<b>Motivo</b><br/>{movimiento.get('motivo', 'N/A')}", normal_style),
            Paragraph(f"<b>Tipo de Movimiento</b><br/>{movimiento.get('tipo_movimiento', 'N/A')}", normal_style),
        ],
        [
            Paragraph(f"<b>Fecha</b><br/>{fecha_str}", normal_style),
            Paragraph(f"<b>Hora</b><br/>{hora_str}", normal_style),
        ],
    ]

    factura_t = Table(factura_data, colWidths=[3.25*inch, 3.25*inch])
    factura_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 0, colors.white),
        ("GRID", (0, 0), (-1, -1), 0, colors.white),
        ("LEFTPADDING", (0, 0), (-1, -1), 30),
        ("RIGHTPADDING", (0, 0), (-1, -1), 15),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(factura_t)
    elements.append(Spacer(1, 20))

    separator = Table([["" * 80]], colWidths=[6.5*inch])
    separator.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (0, 0), 1, colors.HexColor("#d0d0d0")),
    ]))
    elements.append(separator)
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Detalle de Producto:", section_title_style))
    elements.append(Spacer(1, 12))

    monto_total = float(producto.get("precio", 0)) * movimiento.get("cantidad", 0)

    producto_data = [
        [Paragraph("Producto", label_style), Paragraph(producto.get("nombre", "N/A"), normal_style)],
        [Paragraph("Marca", label_style), Paragraph(producto.get("marca", "N/A"), normal_style)],
        [Paragraph("Categoría", label_style), Paragraph(producto.get("categoria", "N/A"), normal_style)],
        [Paragraph("Precio Unitario", label_style), Paragraph(f"S/ {float(producto.get('precio', 0)):.2f}", normal_style)],
        [Paragraph("Cantidad", label_style), Paragraph(str(movimiento.get("cantidad", 0)), normal_style)],
    ]

    producto_t = Table(producto_data, colWidths=[2.2*inch, 4.3*inch])
    producto_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f5f5f5")),
        ("BACKGROUND", (1, 0), (1, -1), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#d0d0d0")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e5e5e5")),
        ("ROWHEIGHT", (0, 0), (-1, -1), 24),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    elements.append(producto_t)
    elements.append(Spacer(1, 16))

    total_data = [
        [
            Paragraph("", normal_style),  # columna vacía
            Paragraph(f"<b>Total</b>", ParagraphStyle("TotalLabel", parent=label_style, textColor=colors.white)),
            Paragraph(f"<b>S/ {monto_total:.2f}</b>", ParagraphStyle("TotalValue", parent=label_style, textColor=colors.white)),
        ]
    ]
    
    total_t = Table(total_data, colWidths=[2*inch, 1.5*inch, 2*inch])
    total_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), colors.white),
        ("BACKGROUND", (1, 0), (-1, 0), colors.HexColor("#1a959f")),
        ("VALIGN", (1, 0), (-1, 0), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "LEFT"),
        ("ALIGN", (2, 0), (2, 0), "RIGHT"),
        ("BOX", (1, 0), (-1, 0), 0, colors.HexColor("#1a959f")),
        ("ROWHEIGHT", (1, 0), (-1, 0), 28),
        ("LEFTPADDING", (1, 0), (1, 0), 16),
        ("RIGHTPADDING", (2, 0), (2, 0), 16),
    ]))
    elements.append(total_t)

    elements.append(Spacer(1, 30))

    footer = Paragraph(
        "<i>Este documento fue generado automáticamente por el Sistema de Gestión de Inventario: HogarElectric.</i>",
        ParagraphStyle("Footer", fontSize=8, textColor=colors.HexColor("#a8a8a8"), alignment=1)
    )
    elements.append(footer)

    doc.build(elements)
    buffer.seek(0)
    return buffer
