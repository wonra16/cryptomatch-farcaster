"""
Dynamic Image Generator for Match Results
Creates beautiful, shareable match result images
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import Dict, Tuple
import io
import base64
import random


class MatchImageGenerator:
    """Generates match result images"""
    
    def __init__(self):
        self.width = 1200
        self.height = 630  # Optimal for social media
        self.colors = {
            "high_match": {
                "bg_start": "#FF6B6B",
                "bg_end": "#FF8E53",
                "accent": "#FFD93D",
                "text": "#FFFFFF"
            },
            "medium_match": {
                "bg_start": "#4ECDC4",
                "bg_end": "#556270",
                "accent": "#C7F0DB",
                "text": "#FFFFFF"
            },
            "low_match": {
                "bg_start": "#A8E6CF",
                "bg_end": "#FFD3B6",
                "accent": "#FFAAA5",
                "text": "#2C3E50"
            }
        }
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def create_gradient_background(self, match_level: str) -> Image.Image:
        """Create gradient background"""
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        
        colors = self.colors.get(match_level, self.colors["medium_match"])
        start_color = self.hex_to_rgb(colors["bg_start"])
        end_color = self.hex_to_rgb(colors["bg_end"])
        
        for y in range(self.height):
            ratio = y / self.height
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        return img
    
    def add_glow_effect(self, img: Image.Image) -> Image.Image:
        """Add soft glow effect"""
        return img.filter(ImageFilter.GaussianBlur(radius=2))
    
    def generate_match_image(
        self,
        personality1: Dict,
        personality2: Dict,
        compatibility_score: int,
        match_level: str,
        comedy_text: str
    ) -> str:
        """
        Generate match result image
        Returns base64 encoded image
        """
        # Create base image
        img = self.create_gradient_background(match_level)
        draw = ImageDraw.Draw(img)
        
        # Try to load fonts (fallback to default if not available)
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 48)
            body_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
            small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # Get colors
        colors = self.colors.get(match_level, self.colors["medium_match"])
        text_color = self.hex_to_rgb(colors["text"])
        accent_color = self.hex_to_rgb(colors["accent"])
        
        # Title
        title_text = "💕 CRYPTO MATCH 💕"
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        title_x = (self.width - title_width) // 2
        draw.text((title_x, 50), title_text, fill=text_color, font=title_font)
        
        # Score - BIG and centered
        score_text = f"{compatibility_score}%"
        score_bbox = draw.textbbox((0, 0), score_text, font=title_font)
        score_width = score_bbox[2] - score_bbox[0]
        score_x = (self.width - score_width) // 2
        
        # Draw score with glow effect
        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
            draw.text((score_x + offset[0], 180 + offset[1]), score_text, fill=accent_color, font=title_font)
        draw.text((score_x, 180), score_text, fill=text_color, font=title_font)
        
        # Match level emoji
        level_emoji = {
            "high_match": "🔥 PERFECT MATCH 🔥",
            "medium_match": "💫 GOOD VIBES 💫",
            "low_match": "⚡ OPPOSITES ATTRACT ⚡"
        }
        level_text = level_emoji.get(match_level, "💕 MATCH 💕")
        level_bbox = draw.textbbox((0, 0), level_text, font=subtitle_font)
        level_width = level_bbox[2] - level_bbox[0]
        level_x = (self.width - level_width) // 2
        draw.text((level_x, 280), level_text, fill=text_color, font=subtitle_font)
        
        # Personalities
        p1_text = f"{personality1['emoji']} {personality1['title']}"
        p2_text = f"{personality2['emoji']} {personality2['title']}"
        
        p1_bbox = draw.textbbox((0, 0), p1_text, font=body_font)
        p1_width = p1_bbox[2] - p1_bbox[0]
        p1_x = (self.width - p1_width) // 2
        
        p2_bbox = draw.textbbox((0, 0), p2_text, font=body_font)
        p2_width = p2_bbox[2] - p2_bbox[0]
        p2_x = (self.width - p2_width) // 2
        
        draw.text((p1_x, 380), p1_text, fill=text_color, font=body_font)
        draw.text((self.width // 2 - 30, 420), "💕", fill=accent_color, font=subtitle_font)
        draw.text((p2_x, 460), p2_text, fill=text_color, font=body_font)
        
        # Comedy text (wrapped)
        comedy_wrapped = self._wrap_text(comedy_text, body_font, self.width - 100)
        y_offset = 530
        for line in comedy_wrapped[:2]:  # Max 2 lines
            line_bbox = draw.textbbox((0, 0), line, font=small_font)
            line_width = line_bbox[2] - line_bbox[0]
            line_x = (self.width - line_width) // 2
            draw.text((line_x, y_offset), line, fill=text_color, font=small_font)
            y_offset += 35
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG', optimize=True)
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_base64}"
    
    def _wrap_text(self, text: str, font, max_width: int) -> list:
        """Wrap text to fit within max_width"""
        words = text.split()
        lines = []
        current_line = []
        
        draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            
            if width > max_width:
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines


# Singleton instance
image_generator = MatchImageGenerator()
