#!/usr/bin/env python3
"""
Rogue Bachata A4 Two-Sided Poster Generator
Matches the website style with dark theme and accent colors
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import Color, HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
import os

# Brand Colors from website CSS
COLORS = {
    'primary': HexColor('#1a1a2e'),
    'secondary': HexColor('#16213e'),
    'accent': HexColor('#e94560'),
    'accent_light': HexColor('#ff6b6b'),
    'text': HexColor('#eeeeee'),
    'text_muted': HexColor('#aaaaaa'),
    'bg': HexColor('#0f0f1a'),
    'card_bg': HexColor('#1a1a2e'),
}

# Page dimensions
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 15 * mm

# Contact Information
CONTACT = {
    'website': 'roguebachata.com',
    'instagram': '@roguebachata',
    'whatsapp': '+44 7596 031416',
    'email': 'voice@oscarcastellino.com',
}

# Offerings
OFFERINGS = [
    {
        'name': 'Rogue Bachata Classes',
        'instructors': 'Boadicea & Oscar',
        'description': 'Perfect for beginners and those looking to strengthen their foundation in a fun and friendly atmosphere.',
    },
    {
        'name': 'Rogue Resonance Workshops',
        'instructors': 'Oscar',
        'description': 'Take your dancing to the next level. Explore groundedness, flow, and authentic connection.',
    },
]

# Principles
PRINCIPLES = [
    ('Body, Bond, Beyond', 'Ground in yourself, listen to your partner, expand into the space'),
    ('Legato', 'Your center of gravity travels on a continuous, unbroken path'),
    ('Pause, Presence, Pivot', 'Stop the movement, find each other, then redirect together'),
    ('Bounce and Roll', 'When bodies meet, rebound elastically or redirect'),
    ('Humility', 'Surrender your movement when connection is lost'),
    ('Lazy', 'Relaxed and lazy, yet in time—a paradox of dance'),
]


def draw_gradient_bg(c, width, height):
    """Draw a gradient background from primary to bg color"""
    steps = 100
    for i in range(steps):
        ratio = i / steps
        r = COLORS['bg'].red + (COLORS['primary'].red - COLORS['bg'].red) * ratio * 0.3
        g = COLORS['bg'].green + (COLORS['primary'].green - COLORS['bg'].green) * ratio * 0.3
        b = COLORS['bg'].blue + (COLORS['primary'].blue - COLORS['bg'].blue) * ratio * 0.3
        c.setFillColor(Color(r, g, b))
        y = height * (1 - i / steps)
        c.rect(0, y - height / steps, width, height / steps + 1, fill=True, stroke=False)


def draw_accent_line(c, x, y, width, thickness=2):
    """Draw an accent colored line"""
    c.setStrokeColor(COLORS['accent'])
    c.setLineWidth(thickness)
    c.line(x, y, x + width, y)


def draw_decorative_element(c, x, y, size=20):
    """Draw a decorative diamond shape"""
    c.setFillColor(COLORS['accent'])
    c.saveState()
    c.translate(x, y)
    c.rotate(45)
    c.rect(-size/2, -size/2, size, size, fill=True, stroke=False)
    c.restoreState()


def load_and_draw_image(c, image_path, x, y, width, height, opacity=0.4):
    """Load and draw an image with optional opacity overlay"""
    if os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            c.drawImage(ImageReader(img), x, y, width, height, preserveAspectRatio=True, anchor='c', mask='auto')
            # Draw overlay for opacity effect
            c.setFillColor(Color(COLORS['bg'].red, COLORS['bg'].green, COLORS['bg'].blue, alpha=1-opacity))
            c.rect(x, y, width, height, fill=True, stroke=False)
        except Exception as e:
            print(f"Could not load image {image_path}: {e}")


def create_front_page(c):
    """Create the front page of the poster"""
    width, height = PAGE_WIDTH, PAGE_HEIGHT
    
    # Background
    draw_gradient_bg(c, width, height)
    
    # Try to add background image with overlay
    img_path = os.path.join(os.path.dirname(__file__), 'images', 'RogueResonance.png')
    if os.path.exists(img_path):
        load_and_draw_image(c, img_path, 0, height * 0.4, width, height * 0.6, opacity=0.25)
    
    # Top decorative element
    draw_decorative_element(c, width / 2, height - 30 * mm, 8)
    
    # Main Title - ROGUE
    c.setFillColor(COLORS['text'])
    c.setFont('Helvetica-Bold', 72)
    title = "ROGUE"
    title_width = c.stringWidth(title, 'Helvetica-Bold', 72)
    c.drawString((width - title_width) / 2, height - 70 * mm, title)
    
    # Subtitle - BACHATA
    c.setFillColor(COLORS['accent'])
    c.setFont('Helvetica-Bold', 36)
    subtitle = "BACHATA"
    subtitle_width = c.stringWidth(subtitle, 'Helvetica-Bold', 36)
    c.drawString((width - subtitle_width) / 2, height - 85 * mm, subtitle)
    
    # Tagline
    c.setFillColor(COLORS['text_muted'])
    c.setFont('Helvetica', 14)
    tagline = "Movement  ·  Connection  ·  Freedom"
    tagline_width = c.stringWidth(tagline, 'Helvetica', 14)
    c.drawString((width - tagline_width) / 2, height - 100 * mm, tagline)
    
    # Accent line under tagline
    draw_accent_line(c, width / 2 - 50 * mm, height - 108 * mm, 100 * mm, 1)
    
    # Offerings Section
    y_pos = height - 135 * mm
    
    for offering in OFFERINGS:
        # Card background
        card_height = 45 * mm
        c.setFillColor(Color(0.1, 0.1, 0.15, alpha=0.8))
        c.roundRect(MARGIN, y_pos - card_height, width - 2 * MARGIN, card_height, 8, fill=True, stroke=False)
        
        # Accent bar on left
        c.setFillColor(COLORS['accent'])
        c.rect(MARGIN, y_pos - card_height, 4, card_height, fill=True, stroke=False)
        
        # Offering name
        c.setFillColor(COLORS['text'])
        c.setFont('Helvetica-Bold', 16)
        c.drawString(MARGIN + 12 * mm, y_pos - 12 * mm, offering['name'])
        
        # Instructors
        c.setFillColor(COLORS['accent'])
        c.setFont('Helvetica', 11)
        c.drawString(MARGIN + 12 * mm, y_pos - 20 * mm, f"with {offering['instructors']}")
        
        # Description
        c.setFillColor(COLORS['text_muted'])
        c.setFont('Helvetica', 9)
        # Word wrap the description
        desc = offering['description']
        max_width = width - 2 * MARGIN - 15 * mm
        words = desc.split()
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            if c.stringWidth(test_line, 'Helvetica', 9) < max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        desc_y = y_pos - 28 * mm
        for line in lines[:2]:  # Max 2 lines
            c.drawString(MARGIN + 12 * mm, desc_y, line)
            desc_y -= 12
        
        y_pos -= card_height + 8 * mm
    
    # Bottom Section - Contact Info
    y_pos = 55 * mm
    
    # Website (prominent)
    c.setFillColor(COLORS['accent'])
    c.setFont('Helvetica-Bold', 24)
    website = CONTACT['website']
    website_width = c.stringWidth(website, 'Helvetica-Bold', 24)
    c.drawString((width - website_width) / 2, y_pos, website)
    
    # Contact row
    y_pos -= 18 * mm
    c.setFont('Helvetica', 11)
    c.setFillColor(COLORS['text'])
    
    # Instagram
    insta_text = f"Instagram: {CONTACT['instagram']}"
    c.drawString(MARGIN + 10 * mm, y_pos, insta_text)
    
    # WhatsApp
    wa_text = f"WhatsApp: {CONTACT['whatsapp']}"
    c.drawString(width / 2 + 5 * mm, y_pos, wa_text)
    
    # Bottom decorative line
    draw_accent_line(c, MARGIN, 20 * mm, width - 2 * MARGIN, 2)
    
    # Small tagline at bottom
    c.setFillColor(COLORS['text_muted'])
    c.setFont('Helvetica', 8)
    bottom_text = "Join us on the dance floor"
    bottom_width = c.stringWidth(bottom_text, 'Helvetica', 8)
    c.drawString((width - bottom_width) / 2, 12 * mm, bottom_text)


def create_back_page(c):
    """Create the back page with principles and more info"""
    width, height = PAGE_WIDTH, PAGE_HEIGHT
    
    # Background
    draw_gradient_bg(c, width, height)
    
    # Header
    c.setFillColor(COLORS['accent'])
    c.setFont('Helvetica-Bold', 28)
    header = "The Rogue Principles"
    header_width = c.stringWidth(header, 'Helvetica-Bold', 28)
    c.drawString((width - header_width) / 2, height - 35 * mm, header)
    
    # Subheader
    c.setFillColor(COLORS['text_muted'])
    c.setFont('Helvetica', 11)
    subheader = "Where the performing arts meet the social dance floor"
    subheader_width = c.stringWidth(subheader, 'Helvetica', 11)
    c.drawString((width - subheader_width) / 2, height - 45 * mm, subheader)
    
    # Accent line
    draw_accent_line(c, width / 2 - 40 * mm, height - 52 * mm, 80 * mm, 1)
    
    # Principles Grid (2 columns, 3 rows)
    y_start = height - 70 * mm
    col_width = (width - 2 * MARGIN - 10 * mm) / 2
    row_height = 38 * mm
    
    for i, (name, desc) in enumerate(PRINCIPLES):
        col = i % 2
        row = i // 2
        
        x = MARGIN + col * (col_width + 10 * mm)
        y = y_start - row * row_height
        
        # Card background
        c.setFillColor(Color(0.1, 0.1, 0.15, alpha=0.7))
        c.roundRect(x, y - 32 * mm, col_width, 32 * mm, 6, fill=True, stroke=False)
        
        # Decorative diamond
        draw_decorative_element(c, x + 10 * mm, y - 8 * mm, 4)
        
        # Principle name
        c.setFillColor(COLORS['text'])
        c.setFont('Helvetica-Bold', 11)
        c.drawString(x + 18 * mm, y - 10 * mm, f"Rogue {name}")
        
        # Description with word wrap
        c.setFillColor(COLORS['text_muted'])
        c.setFont('Helvetica', 8)
        words = desc.split()
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            if c.stringWidth(test_line, 'Helvetica', 8) < col_width - 15 * mm:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        desc_y = y - 18 * mm
        for line in lines[:2]:
            c.drawString(x + 8 * mm, desc_y, line)
            desc_y -= 10
    
    # Instructors Section
    y_pos = height - 195 * mm
    
    c.setFillColor(COLORS['accent'])
    c.setFont('Helvetica-Bold', 18)
    inst_header = "Your Instructors"
    inst_width = c.stringWidth(inst_header, 'Helvetica-Bold', 18)
    c.drawString((width - inst_width) / 2, y_pos, inst_header)
    
    y_pos -= 15 * mm
    
    # Oscar
    c.setFillColor(COLORS['text'])
    c.setFont('Helvetica-Bold', 12)
    c.drawString(MARGIN + 5 * mm, y_pos, "Oscar")
    c.setFillColor(COLORS['text_muted'])
    c.setFont('Helvetica', 9)
    oscar_desc = "A performer at the highest levels of theatre with over 20 years on the social dance floor. His Rogue style evolved by bringing stage experience onto the dance floor."
    
    # Word wrap
    words = oscar_desc.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if c.stringWidth(test_line, 'Helvetica', 9) < width - 2 * MARGIN - 10 * mm:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    
    y_pos -= 8 * mm
    for line in lines:
        c.drawString(MARGIN + 5 * mm, y_pos, line)
        y_pos -= 11
    
    y_pos -= 5 * mm
    
    # Boadicea & Oscar
    c.setFillColor(COLORS['text'])
    c.setFont('Helvetica-Bold', 12)
    c.drawString(MARGIN + 5 * mm, y_pos, "Boadicea & Oscar")
    c.setFillColor(COLORS['text_muted'])
    c.setFont('Helvetica', 9)
    bo_desc = "An experienced Bachata couple known for their unique connection and musicality. Their style is much sought after at socials."
    
    words = bo_desc.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if c.stringWidth(test_line, 'Helvetica', 9) < width - 2 * MARGIN - 10 * mm:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    
    y_pos -= 8 * mm
    for line in lines:
        c.drawString(MARGIN + 5 * mm, y_pos, line)
        y_pos -= 11
    
    # Contact Section at bottom
    y_pos = 50 * mm
    
    # Contact header
    c.setFillColor(COLORS['accent'])
    c.setFont('Helvetica-Bold', 14)
    contact_header = "Get in Touch"
    contact_width = c.stringWidth(contact_header, 'Helvetica-Bold', 14)
    c.drawString((width - contact_width) / 2, y_pos, contact_header)
    
    # Contact details in a nice layout
    y_pos -= 12 * mm
    c.setFillColor(COLORS['text'])
    c.setFont('Helvetica', 10)
    
    # Center the contact info
    contact_lines = [
        f"Website: {CONTACT['website']}",
        f"Instagram: {CONTACT['instagram']}",
        f"WhatsApp: {CONTACT['whatsapp']}",
    ]
    
    for line in contact_lines:
        line_width = c.stringWidth(line, 'Helvetica', 10)
        c.drawString((width - line_width) / 2, y_pos, line)
        y_pos -= 8 * mm
    
    # Bottom decorative elements
    draw_accent_line(c, MARGIN, 18 * mm, width - 2 * MARGIN, 2)
    
    draw_decorative_element(c, width / 2, 10 * mm, 5)


def create_poster():
    """Generate the complete two-sided A4 poster PDF"""
    output_path = os.path.join(os.path.dirname(__file__), 'RogueBachata_Poster.pdf')
    
    c = canvas.Canvas(output_path, pagesize=A4)
    
    # Front page
    create_front_page(c)
    c.showPage()
    
    # Back page
    create_back_page(c)
    c.showPage()
    
    c.save()
    print(f"✅ Poster created successfully: {output_path}")
    print(f"   File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    return output_path


if __name__ == '__main__':
    create_poster()
