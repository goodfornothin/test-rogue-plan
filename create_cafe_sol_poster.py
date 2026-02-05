#!/usr/bin/env python3
"""
Cafe Sol Salsa & Bachata Night Poster Generator
Creates an eye-catching social media poster for Facebook groups
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os

# Poster dimensions (Facebook recommended: 1200x630 for links, 1080x1080 for square posts)
# Using 1080x1350 for Instagram/Facebook portrait (4:5 ratio - great for feeds)
WIDTH = 1080
HEIGHT = 1350

# Colors - vibrant party theme
PINK = (233, 69, 96)  # #e94560
DARK_BG = (18, 18, 35)  # #121223
WHITE = (255, 255, 255)
GOLD = (255, 215, 100)
LIGHT_PINK = (255, 150, 170)

def create_poster():
    # Create base image with gradient background
    img = Image.new('RGB', (WIDTH, HEIGHT), DARK_BG)
    draw = ImageDraw.Draw(img)
    
    # Create gradient background (dark to slightly lighter)
    for y in range(HEIGHT):
        r = int(18 + (y / HEIGHT) * 15)
        g = int(18 + (y / HEIGHT) * 10)
        b = int(35 + (y / HEIGHT) * 20)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    
    # Load and place the party image
    script_dir = os.path.dirname(__file__)
    img_path = os.path.join(script_dir, 'images', 'RogueParty.jpg')
    
    if os.path.exists(img_path):
        party_img = Image.open(img_path)
        # Resize to fit width, crop to show upper portion (where faces are)
        aspect = party_img.width / party_img.height
        new_width = WIDTH - 60  # margins
        new_height = int(new_width / aspect)
        party_img = party_img.resize((new_width, new_height), Image.LANCZOS)
        
        # Crop to show upper 60% (where the dancers are)
        crop_height = min(450, new_height)
        crop_top = int(new_height * 0.15)  # Start 15% from top
        party_img = party_img.crop((0, crop_top, new_width, crop_top + crop_height))
        
        # Add slight vignette/border effect
        party_img = party_img.convert('RGB')
        
        # Round corners effect
        mask = Image.new('L', party_img.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), party_img.size], radius=20, fill=255)
        
        # Create rounded image
        rounded_party = Image.new('RGB', party_img.size, DARK_BG)
        rounded_party.paste(party_img, mask=mask)
        
        # Paste onto main image
        img.paste(rounded_party, (30, 200))
        img_bottom = 200 + crop_height
    else:
        img_bottom = 200
    
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts (fall back to default if not available)
    try:
        # macOS fonts
        font_bold = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 72)
        font_big = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 56)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 40)
        font_regular = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 32)
        font_small = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
    except:
        font_bold = ImageFont.load_default()
        font_big = font_bold
        font_medium = font_bold
        font_regular = font_bold
        font_small = font_bold
    
    # Top banner - "SALSA & BACHATA NIGHT"
    y_pos = 40
    
    # Draw decorative top line
    draw.rectangle([(100, y_pos), (WIDTH - 100, y_pos + 4)], fill=PINK)
    y_pos += 20
    
    # Main title
    title1 = "SALSA & BACHATA"
    bbox = draw.textbbox((0, 0), title1, font=font_bold)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) // 2, y_pos), title1, font=font_bold, fill=PINK)
    y_pos += 75
    
    title2 = "NIGHT!"
    bbox = draw.textbbox((0, 0), title2, font=font_bold)
    text_width = bbox[2] - bbox[0]
    # Add glow effect
    for offset in range(3, 0, -1):
        alpha = 100 - offset * 30
        glow_color = (255, 100, 130)
        draw.text(((WIDTH - text_width) // 2 + offset, y_pos + offset), title2, font=font_bold, fill=glow_color)
    draw.text(((WIDTH - text_width) // 2, y_pos), title2, font=font_bold, fill=WHITE)
    
    # Below image - Event details
    y_pos = img_bottom + 30
    
    # Date banner with background
    draw.rounded_rectangle([(50, y_pos), (WIDTH - 50, y_pos + 70)], radius=10, fill=PINK)
    date_text = "📅 TUESDAY 17 FEBRUARY 2026"
    bbox = draw.textbbox((0, 0), date_text, font=font_medium)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) // 2, y_pos + 15), date_text, font=font_medium, fill=WHITE)
    y_pos += 90
    
    # Venue
    venue_text = "📍 CAFE SOL LONDON"
    bbox = draw.textbbox((0, 0), venue_text, font=font_big)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) // 2, y_pos), venue_text, font=font_big, fill=GOLD)
    y_pos += 60
    
    address_text = "56 Clapham High Street, SW4 7UL"
    bbox = draw.textbbox((0, 0), address_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) // 2, y_pos), address_text, font=font_small, fill=(180, 180, 180))
    y_pos += 50
    
    # Schedule box
    draw.rounded_rectangle([(80, y_pos), (WIDTH - 80, y_pos + 180)], radius=15, fill=(30, 30, 55), outline=PINK, width=2)
    
    schedule_y = y_pos + 20
    
    # Class info
    class_text = "🎓 BACHATA CLASS"
    bbox = draw.textbbox((0, 0), class_text, font=font_medium)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) // 2, schedule_y), class_text, font=font_medium, fill=LIGHT_PINK)
    schedule_y += 45
    
    time_text = "7:30pm - 8:30pm  •  Only £10"
    bbox = draw.textbbox((0, 0), time_text, font=font_regular)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) // 2, schedule_y), time_text, font=font_regular, fill=WHITE)
    schedule_y += 50
    
    # Social info
    social_text = "💃 FREE SOCIAL DANCING"
    bbox = draw.textbbox((0, 0), social_text, font=font_medium)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) // 2, schedule_y), social_text, font=font_medium, fill=GOLD)
    schedule_y += 45
    
    free_text = "8:30pm till late  •  FREE ENTRY!"
    bbox = draw.textbbox((0, 0), free_text, font=font_regular)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) // 2, schedule_y), free_text, font=font_regular, fill=WHITE)
    
    y_pos += 200
    
    # Fun taglines
    tagline1 = "✨ Beginners welcome! No partner needed ✨"
    bbox = draw.textbbox((0, 0), tagline1, font=font_small)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) // 2, y_pos), tagline1, font=font_small, fill=LIGHT_PINK)
    y_pos += 35
    
    tagline2 = "Meet new people • Great music • Fun vibes"
    bbox = draw.textbbox((0, 0), tagline2, font=font_small)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) // 2, y_pos), tagline2, font=font_small, fill=(150, 150, 150))
    y_pos += 50
    
    # Book now banner
    draw.rounded_rectangle([(150, y_pos), (WIDTH - 150, y_pos + 55)], radius=27, fill=PINK)
    book_text = "BOOK NOW!"
    bbox = draw.textbbox((0, 0), book_text, font=font_medium)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) // 2, y_pos + 8), book_text, font=font_medium, fill=WHITE)
    y_pos += 70
    
    # Contact info
    contact_text = "📱 @roguebachata  •  WhatsApp: 07596 031416"
    bbox = draw.textbbox((0, 0), contact_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    draw.text(((WIDTH - text_width) // 2, y_pos), contact_text, font=font_small, fill=(140, 140, 140))
    
    # Bottom decorative line
    draw.rectangle([(100, HEIGHT - 30), (WIDTH - 100, HEIGHT - 26)], fill=PINK)
    
    # Save as PNG
    output_path = os.path.join(script_dir, 'CafeSol_Feb17_Poster.png')
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ Poster saved to: {output_path}")
    
    return output_path

if __name__ == "__main__":
    create_poster()
