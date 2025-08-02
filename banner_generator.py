#!/usr/bin/env python3
"""
Ultimate PyPI Banner Generator
Professional banner creation with multiple styles and batch generation
"""

import os
import sys
import argparse
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import math
import time

# Configuration
LOGO_PATH = "pypi_logo.png"
OUTPUT_DIR = "output"
FONT_BOLD = "DejaVuSans-Bold.ttf"
FONT_REGULAR = "DejaVuSans.ttf"

# Fixed banner dimensions
IMG_WIDTH = 1200
IMG_HEIGHT = 630
PADDING = 80

# Enhanced theme collection with consistent color schemes
ALL_THEMES = {
    '1': {
        'name': 'professional_light',
        'description': 'Clean white background - Corporate style',
        'type': 'professional',
        'bg': '#ffffff',
        'card': '#f8fafc',
        'primary': '#1e293b',
        'secondary': '#64748b',
        'accent': '#3b82f6',
        'border': '#e2e8f0'
    },
    '2': {
        'name': 'professional_dark',
        'description': 'Dark slate background - Modern tech style',
        'type': 'professional',
        'bg': '#0f172a',
        'card': '#1e293b',
        'primary': '#f1f5f9',
        'secondary': '#cbd5e1',
        'accent': '#60a5fa',
        'border': '#334155'
    },
    '3': {
        'name': 'minimal_clean',
        'description': 'Ultra-minimal white - Very clean',
        'type': 'minimal',
        'bg': '#ffffff',
        'primary': '#1f2937',
        'secondary': '#6b7280',
        'accent': '#10b981',
        'card': '#f9fafb',
        'border': '#e5e7eb'
    },
    '4': {
        'name': 'minimal_dark',
        'description': 'Ultra-minimal dark - Sophisticated',
        'type': 'minimal',
        'bg': '#111827',
        'primary': '#f9fafb',
        'secondary': '#d1d5db',
        'accent': '#60a5fa',
        'card': '#1f2937',
        'border': '#374151'
    },
    '5': {
        'name': 'gradient_blue',
        'description': 'Blue gradient background - Dynamic',
        'type': 'gradient',
        'bg_start': '#667eea',
        'bg_end': '#764ba2',
        'primary': '#ffffff',
        'secondary': '#f1f5f9',
        'accent': '#60a5fa',
        'card': '#1e293b',
        'border': '#334155'
    },
    '6': {
        'name': 'gradient_purple',
        'description': 'Purple gradient background - Creative',
        'type': 'gradient',
        'bg_start': '#a8edea',
        'bg_end': '#fed6e3',
        'primary': '#1f2937',
        'secondary': '#374151',
        'accent': '#8b5cf6',
        'card': '#f3f4f6',
        'border': '#d1d5db'
    },
    '7': {
        'name': 'gradient_sunset',
        'description': 'Sunset gradient background - Warm',
        'type': 'gradient',
        'bg_start': '#fa709a',
        'bg_end': '#fee140',
        'primary': '#ffffff',
        'secondary': '#fef7ff',
        'accent': '#f59e0b',
        'card': '#1f2937',
        'border': '#374151'
    },
    '8': {
        'name': 'gradient_ocean',
        'description': 'Ocean gradient background - Cool',
        'type': 'gradient',
        'bg_start': '#4facfe',
        'bg_end': '#00f2fe',
        'primary': '#ffffff',
        'secondary': '#f0fdfa',
        'accent': '#06b6d4',
        'card': '#134e4a',
        'border': '#0f766e'
    },
    '9': {
        'name': 'modern_glassmorphism',
        'description': 'Glassmorphism effect with blur - Trendy',
        'type': 'glassmorphism',
        'bg': '#0f172a',
        'primary': '#ffffff',
        'secondary': '#cbd5e1',
        'accent': '#06d6a0',
        'card': '#1e293b',
        'border': '#334155'
    },
    '10': {
        'name': 'neon_cyber',
        'description': 'Neon cyberpunk style - Electric',
        'type': 'neon',
        'bg': '#0a0a0a',
        'primary': '#00ff41',
        'secondary': '#39ff14',
        'accent': '#ff0080',
        'card': '#1a1a1a',
        'border': '#00ff41'
    },
    '11': {
        'name': 'material_design',
        'description': 'Material Design inspired - Google style',
        'type': 'material',
        'bg': '#fafafa',
        'primary': '#212121',
        'secondary': '#757575',
        'accent': '#2196f3',
        'card': '#ffffff',
        'border': '#e0e0e0'
    },
    '12': {
        'name': 'retro_synthwave',
        'description': 'Retro synthwave aesthetic - 80s vibes',
        'type': 'synthwave',
        'bg_start': '#ff006e',
        'bg_end': '#8338ec',
        'primary': '#ffffff',
        'secondary': '#ffeedd',
        'accent': '#ffbe0b',
        'card': '#3a0ca3',
        'border': '#7209b7'
    }
}

class UltimateBannerGenerator:
    def __init__(self):
        self.fonts = self._load_fonts()
        
    def _load_fonts(self):
        """Load fonts with fallback"""
        fonts = {}
        sizes = {
            'title': 48,
            'version': 20,
            'desc': 22,
            'badge': 16,
            'cmd': 28,
            'url': 18
        }
        
        for name, size in sizes.items():
            try:
                font_file = FONT_BOLD if name in ['title', 'version', 'cmd'] else FONT_REGULAR
                fonts[name] = ImageFont.truetype(font_file, size)
            except:
                fonts[name] = ImageFont.load_default()
        
        return fonts
    
    def _create_gradient_background(self, width, height, color_start, color_end):
        """Create gradient background"""
        img = Image.new('RGB', (width, height))
        
        # Convert hex to RGB
        start_rgb = tuple(int(color_start[i:i+2], 16) for i in (1, 3, 5))
        end_rgb = tuple(int(color_end[i:i+2], 16) for i in (1, 3, 5))
        
        for y in range(height):
            ratio = y / height
            color = tuple(
                int(start_rgb[i] * (1 - ratio) + end_rgb[i] * ratio)
                for i in range(3)
            )
            draw = ImageDraw.Draw(img)
            draw.line([(0, y), (width, y)], fill=color)
        
        return img
    
    def _create_glassmorphism_background(self, width, height, theme):
        """Create glassmorphism effect background"""
        img = Image.new('RGB', (width, height), theme['bg'])
        draw = ImageDraw.Draw(img)
        
        # Add some geometric shapes for depth
        for i in range(5):
            x = int(width * (0.2 + i * 0.15))
            y = int(height * (0.1 + i * 0.2))
            size = 150 + i * 50
            color = tuple(int(theme['accent'][j:j+2], 16) for j in (1, 3, 5))
            color = (*color, 30)  # Semi-transparent
            
            # Create overlay for blur effect
            overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            overlay_draw = ImageDraw.Draw(overlay)
            overlay_draw.ellipse([x, y, x + size, y + size], fill=color)
            
            img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        return img
    
    def _create_neon_background(self, width, height, theme):
        """Create neon cyberpunk background"""
        img = Image.new('RGB', (width, height), theme['bg'])
        draw = ImageDraw.Draw(img)
        
        # Add grid lines for cyberpunk effect
        grid_spacing = 50
        grid_color = tuple(int(theme['primary'][i:i+2], 16) for i in (1, 3, 5))
        
        for x in range(0, width, grid_spacing):
            draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
        
        for y in range(0, height, grid_spacing):
            draw.line([(0, y), (width, y)], fill=grid_color, width=1)
        
        return img
    
    def _draw_rounded_rect(self, draw, bbox, radius, fill=None, outline=None):
        """Draw rounded rectangle"""
        x1, y1, x2, y2 = bbox
        
        if radius <= 0:
            draw.rectangle(bbox, fill=fill, outline=outline)
            return
            
        # Main rectangles
        draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill, outline=outline)
        draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill, outline=outline)
        
        # Corners
        draw.pieslice([x1, y1, x1 + radius*2, y1 + radius*2], 180, 270, fill=fill, outline=outline)
        draw.pieslice([x2 - radius*2, y1, x2, y1 + radius*2], 270, 360, fill=fill, outline=outline)
        draw.pieslice([x1, y2 - radius*2, x1 + radius*2, y2], 90, 180, fill=fill, outline=outline)
        draw.pieslice([x2 - radius*2, y2 - radius*2, x2, y2], 0, 90, fill=fill, outline=outline)
    
    def _wrap_text(self, text, font, max_width, draw):
        """Wrap text to fit width"""
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = f"{current_line}{word} ".strip()
            if draw.textlength(test_line, font=font) <= max_width:
                current_line = f"{current_line}{word} "
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = f"{word} "
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines
    
    def generate_banner(self, package_data, theme):
        """Generate banner with specified theme"""
        
        # Create background based on theme type
        if theme['type'] in ['gradient', 'synthwave']:
            img = self._create_gradient_background(IMG_WIDTH, IMG_HEIGHT, 
                                                 theme['bg_start'], theme['bg_end'])
        elif theme['type'] == 'glassmorphism':
            img = self._create_glassmorphism_background(IMG_WIDTH, IMG_HEIGHT, theme)
        elif theme['type'] == 'neon':
            img = self._create_neon_background(IMG_WIDTH, IMG_HEIGHT, theme)
        else:
            img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT), theme['bg'])
        
        draw = ImageDraw.Draw(img)
        
        # Content area (leave space for logo if it exists)
        logo_space = 140 if os.path.exists(LOGO_PATH) else 0
        content_width = IMG_WIDTH - 2 * PADDING - logo_space
        
        y = PADDING + 20
        
        # Package name
        package_name = package_data['name']
        text_color = theme['primary']
        draw.text((PADDING, y), package_name, 
                 font=self.fonts['title'], fill=text_color)
        y += self.fonts['title'].getbbox(package_name)[3] + 25
        
        # Version badge
        version = package_data.get('version', '')
        if version:
            version_text = f"v{version}"
            version_width = draw.textlength(version_text, self.fonts['version']) + 16
            version_height = 28
            
            self._draw_rounded_rect(draw, 
                [PADDING, y, PADDING + version_width, y + version_height],
                14, fill=theme['accent'])
            
            draw.text((PADDING + 8, y + 4), version_text, 
                     font=self.fonts['version'], fill='white')
            y += version_height + 30
        
        # Description
        summary = package_data.get('summary', '')
        if summary:
            lines = self._wrap_text(summary, self.fonts['desc'], content_width, draw)
            secondary_color = theme['secondary']
            for line in lines:
                draw.text((PADDING, y), line, 
                         font=self.fonts['desc'], fill=secondary_color)
                y += self.fonts['desc'].getbbox(line)[3] + 6
            y += 25
        
        # Python requirement badge
        requires_python = package_data.get('requires_python', '')
        if requires_python:
            req_text = f"Python {requires_python}+"
            req_width = draw.textlength(req_text, self.fonts['badge']) + 12
            req_height = 24
            
            badge_color = theme.get('border', theme['accent'])
            self._draw_rounded_rect(draw,
                [PADDING, y, PADDING + req_width, y + req_height],
                4, fill=badge_color)
            
            draw.text((PADDING + 6, y + 3), req_text,
                     font=self.fonts['badge'], fill='white')
            y += req_height + 35
        
        # Installation command
        cmd_text = f"pip install {package_name}"
        cmd_height = 50
        cmd_padding = 20
        
        # Terminal card
        card_color = theme['card']
        self._draw_rounded_rect(draw,
            [PADDING, y, PADDING + content_width, y + cmd_height],
            8, fill=card_color)
        
        # Add border for better visibility
        if theme['type'] not in ['gradient', 'synthwave']:
            border_color = theme['border']
            self._draw_rounded_rect(draw,
                [PADDING, y, PADDING + content_width, y + cmd_height],
                8, fill=None, outline=border_color)
        
        draw.text((PADDING + cmd_padding, y + 12), f"$ {cmd_text}",
                 font=self.fonts['cmd'], fill=text_color)
        y += cmd_height + 30
        
        # Project URL
        project_url = package_data.get('project_url', '')
        if project_url:
            clean_url = project_url.replace('https://', '').replace('http://', '')
            secondary_color = theme['secondary']
            draw.text((PADDING, y), clean_url,
                     font=self.fonts['url'], fill=secondary_color)
        
        # Logo (auto-include if exists, no asking)
        if os.path.exists(LOGO_PATH):
            try:
                logo = Image.open(LOGO_PATH).convert("RGBA")
                logo_size = 100
                logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
                
                logo_x = IMG_WIDTH - logo_size - PADDING
                logo_y = PADDING + 20
                
                # Logo background
                bg_padding = 15
                logo_bg_color = theme['card']
                self._draw_rounded_rect(draw,
                    [logo_x - bg_padding, logo_y - bg_padding,
                     logo_x + logo_size + bg_padding, logo_y + logo_size + bg_padding],
                    8, fill=logo_bg_color)
                
                img.paste(logo, (logo_x, logo_y), logo)
            except Exception as e:
                print(f"Logo error: {e}")
        
        # Accent line at top
        draw.rectangle([0, 0, IMG_WIDTH, 4], fill=theme['accent'])
        
        return img
    
    def show_welcome(self):
        """Show enhanced welcome message"""
        print("🎨" + "="*60 + "🎨")
        print("           ULTIMATE PYPI BANNER GENERATOR v2.0")
        print("    Professional • Minimal • Gradient • Modern Themes")
        print("       Single • Multiple • Batch • Category Generation")
        print("🎨" + "="*60 + "🎨")
        print()
        print("✨ NEW FEATURES:")
        print("   • 12 Professional Themes (4 new styles added)")
        print("   • Batch Generation (Multiple themes at once)")
        print("   • Category Selection (Generate by theme type)")
        print("   • Enhanced Visual Effects (Glassmorphism, Neon, etc.)")
        print("   • No Preview Images (Cleaner output)")
        print()
    
    def get_package_name(self):
        """Get package name from user"""
        print("📦 PACKAGE SELECTION")
        print("-" * 20)
        
        while True:
            package_name = input("Enter PyPI package name: ").strip()
            
            if not package_name:
                print("❌ Package name cannot be empty. Please try again.")
                continue
            
            # Validate package exists on PyPI
            print(f"🔍 Checking '{package_name}' on PyPI...")
            
            try:
                response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    info = data['info']
                    print(f"✅ Found: {info.get('name', package_name)}")
                    print(f"   Version: {info.get('version', 'N/A')}")
                    print(f"   Summary: {info.get('summary', 'No description')[:60]}...")
                    print()
                    
                    confirm = input("📋 Use this package? (y/n): ").strip().lower()
                    if confirm in ['y', 'yes', '']:
                        return package_name
                    else:
                        continue
                else:
                    print(f"❌ Package '{package_name}' not found on PyPI.")
                    retry = input("🔄 Try another name? (y/n): ").strip().lower()
                    if retry not in ['y', 'yes', '']:
                        return None
                    continue
                    
            except requests.RequestException:
                print("❌ Error connecting to PyPI. Check your internet connection.")
                retry = input("🔄 Try again? (y/n): ").strip().lower()
                if retry not in ['y', 'yes', '']:
                    return None
                continue
    
    def get_theme_choice(self):
        """Get theme selection from user with multiple options"""
        print("\n🎨 GENERATION OPTIONS")
        print("-" * 20)
        print()
        print("Choose generation mode:")
        print("A. Single Theme - Generate one specific theme")
        print("B. Multiple Themes - Choose several themes")
        print("C. All Themes - Generate all 12 themes at once")
        print("D. Category - Generate all themes from a category")
        print()
        
        while True:
            mode = input("Select mode (A/B/C/D): ").strip().upper()
            
            if mode == 'A':
                return self._get_single_theme()
            elif mode == 'B':
                return self._get_multiple_themes()
            elif mode == 'C':
                return list(ALL_THEMES.keys())
            elif mode == 'D':
                return self._get_themes_by_category()
            else:
                print("❌ Invalid choice. Please select A, B, C, or D.")
    
    def _get_single_theme(self):
        """Get single theme selection"""
        print("\n🎨 THEME SELECTION")
        print("-" * 17)
        print()
        
        # Group themes by category
        categories = {
            'Professional': ['1', '2'],
            'Minimal': ['3', '4'],
            'Gradient': ['5', '6', '7', '8'],
            'Modern': ['9', '10', '11', '12']
        }
        
        for category, theme_keys in categories.items():
            print(f"📂 {category}:")
            for key in theme_keys:
                theme = ALL_THEMES[key]
                print(f"   {key}. {theme['name'].replace('_', ' ').title()}")
                print(f"      {theme['description']}")
            print()
        
        while True:
            choice = input("Select theme (1-12): ").strip()
            
            if choice in ALL_THEMES:
                selected_theme = ALL_THEMES[choice]
                print(f"✅ Selected: {selected_theme['name'].replace('_', ' ').title()}")
                return [choice]
            else:
                print("❌ Invalid choice. Please select 1-12.")
    
    def _get_multiple_themes(self):
        """Get multiple theme selection"""
        print("\n🎨 MULTIPLE THEME SELECTION")
        print("-" * 27)
        print()
        
        # Show all themes with numbers
        for key, theme in ALL_THEMES.items():
            print(f"{key}. {theme['name'].replace('_', ' ').title()}")
        
        print()
        print("Enter theme numbers separated by commas (e.g., 1,3,5)")
        print("Or enter ranges (e.g., 1-4,7,9-12)")
        
        while True:
            selection = input("Select themes: ").strip()
            
            try:
                selected_keys = []
                
                # Parse comma-separated values and ranges
                parts = selection.split(',')
                for part in parts:
                    part = part.strip()
                    if '-' in part:
                        # Handle range
                        start, end = part.split('-')
                        for i in range(int(start), int(end) + 1):
                            if str(i) in ALL_THEMES:
                                selected_keys.append(str(i))
                    else:
                        # Handle single number
                        if part in ALL_THEMES:
                            selected_keys.append(part)
                
                if selected_keys:
                    selected_keys = list(set(selected_keys))  # Remove duplicates
                    selected_keys.sort(key=int)  # Sort numerically
                    
                    print(f"\n✅ Selected {len(selected_keys)} themes:")
                    for key in selected_keys:
                        theme = ALL_THEMES[key]
                        print(f"   • {theme['name'].replace('_', ' ').title()}")
                    
                    return selected_keys
                else:
                    print("❌ No valid themes selected. Try again.")
                    
            except ValueError:
                print("❌ Invalid format. Use numbers separated by commas or ranges (e.g., 1,3,5 or 1-4).")
    
    def _get_themes_by_category(self):
        """Get themes by category"""
        print("\n📂 CATEGORY SELECTION")
        print("-" * 19)
        print()
        
        categories = {
            '1': {
                'name': 'Professional',
                'themes': ['1', '2'],
                'description': 'Corporate and business styles'
            },
            '2': {
                'name': 'Minimal',
                'themes': ['3', '4'],
                'description': 'Clean and simple designs'
            },
            '3': {
                'name': 'Gradient',
                'themes': ['5', '6', '7', '8'],
                'description': 'Colorful gradient backgrounds'
            },
            '4': {
                'name': 'Modern',
                'themes': ['9', '10', '11', '12'],
                'description': 'Trendy and experimental styles'
            }
        }
        
        for key, category in categories.items():
            print(f"{key}. {category['name']} ({len(category['themes'])} themes)")
            print(f"   {category['description']}")
            print()
        
        while True:
            choice = input("Select category (1-4): ").strip()
            
            if choice in categories:
                selected_category = categories[choice]
                print(f"✅ Selected: {selected_category['name']} category")
                print(f"   Themes: {', '.join(selected_category['themes'])}")
                return selected_category['themes']
            else:
                print("❌ Invalid choice. Please select 1-4.")
    
    def fetch_package_data(self, package_name):
        """Fetch package data from PyPI"""
        try:
            response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
            response.raise_for_status()
            data = response.json()
            return {
                'name': package_name,
                'version': data['info'].get('version', ''),
                'summary': data['info'].get('summary', ''),
                'requires_python': data['info'].get('requires_python', ''),
                'project_url': data['info'].get('project_url', f"https://pypi.org/project/{package_name}/"),
                'author': data['info'].get('author', '')
            }
        except Exception as e:
            print(f"Error fetching package data: {e}")
            return None
    
    def save_banner(self, img, package_name, theme):
        """Save banner without preview generation"""
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{package_name}_{theme['name']}_{timestamp}.png"
        
        # Main banner only
        main_path = os.path.join(OUTPUT_DIR, filename)
        img.save(main_path, quality=95, optimize=True)
        
        return main_path
    
    def generate_multiple_banners(self, package_data, selected_themes):
        """Generate multiple banners at once"""
        generated_files = []
        
        print(f"\n🚀 BATCH GENERATION")
        print("-" * 19)
        print(f"📦 Package: {package_data['name']}")
        print(f"🎨 Themes: {len(selected_themes)} selected")
        print(f"📏 Size: {IMG_WIDTH}x{IMG_HEIGHT}px")
        print()
        
        for i, theme_key in enumerate(selected_themes, 1):
            theme = ALL_THEMES[theme_key]
            print(f"🎨 [{i}/{len(selected_themes)}] Generating {theme['name'].replace('_', ' ').title()}...")
            
            try:
                img = self.generate_banner(package_data, theme)
                file_path = self.save_banner(img, package_data['name'], theme)
                generated_files.append(file_path)
                
                file_size = os.path.getsize(file_path) / 1024
                print(f"   ✅ Saved: {os.path.basename(file_path)} ({file_size:.1f} KB)")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
            
            # Small delay for visual feedback
            time.sleep(0.2)
        
        return generated_files
    
    def run(self):
        """Main interactive flow with enhanced options"""
        try:
            self.show_welcome()
            
            # Get user inputs
            package_name = self.get_package_name()
            if not package_name:
                print("👋 Goodbye!")
                return
            
            selected_themes = self.get_theme_choice()
            
            # Fetch package data
            print(f"\n� FETCHING DATA")
            print("-" * 15)
            print("� Getting package information from PyPI...")
            package_data = self.fetch_package_data(package_name)
            if not package_data:
                print("❌ Failed to fetch package data.")
                return
            print("✅ Package data retrieved successfully!")
            
            # Generate banners
            if len(selected_themes) == 1:
                # Single banner generation
                theme = ALL_THEMES[selected_themes[0]]
                
                print(f"\n🚀 GENERATING BANNER")
                print("-" * 19)
                print(f"📦 Package: {package_name}")
                print(f"🎨 Theme: {theme['name'].replace('_', ' ').title()}")
                print(f"📏 Size: {IMG_WIDTH}x{IMG_HEIGHT}px")
                print()
                
                print("🎨 Creating banner...")
                img = self.generate_banner(package_data, theme)
                
                print("💾 Saving file...")
                output_path = self.save_banner(img, package_name, theme)
                
                file_size = os.path.getsize(output_path) / 1024
                print(f"✅ Banner generated successfully!")
                print(f"📁 File: {output_path} ({file_size:.1f} KB)")
                
            else:
                # Multiple banners generation
                generated_files = self.generate_multiple_banners(package_data, selected_themes)
                
                print(f"\n✅ BATCH GENERATION COMPLETE!")
                print("-" * 30)
                print(f"📊 Generated: {len(generated_files)} banners")
                
                total_size = sum(os.path.getsize(f) for f in generated_files) / 1024
                print(f"📁 Total size: {total_size:.1f} KB")
                print(f"📂 Location: {OUTPUT_DIR}/")
            
            print("\n" + "🎉" + "="*58 + "🎉")
            print("                 GENERATION COMPLETED!")
            print("🎉" + "="*58 + "🎉")
            
            # Ask if user wants to generate another
            print()
            another = input("🔄 Generate more banners? (y/n): ").strip().lower()
            if another in ['y', 'yes']:
                print()
                self.run()  # Recursive call for another banner
            else:
                print("\n✨ Thank you for using the Ultimate PyPI Banner Generator!")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Main entry point with command-line interface"""
    parser = argparse.ArgumentParser(
        description="Ultimate PyPI Banner Generator - Create professional banners for PyPI packages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python banner_generator.py                    # Interactive mode
  python banner_generator.py --package requests # Quick generation for 'requests'
  python banner_generator.py --help            # Show this help message

Interactive mode allows you to:
  • Choose from 12 professional themes
  • Generate single or multiple banners
  • Select themes by category
  • Batch generate all themes at once
        """
    )
    
    parser.add_argument(
        '--package', '-p',
        type=str,
        help='PyPI package name (if not provided, interactive mode will prompt)'
    )
    
    parser.add_argument(
        '--theme', '-t',
        type=str,
        choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
        help='Theme number (1-12). If not provided, interactive mode will show all options'
    )
    
    parser.add_argument(
        '--list-themes', '-l',
        action='store_true',
        help='List all available themes and exit'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=OUTPUT_DIR,
        help=f'Output directory (default: {OUTPUT_DIR})'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='Ultimate PyPI Banner Generator v2.0.0'
    )
    
    args = parser.parse_args()
    
    # List themes and exit
    if args.list_themes:
        print("🎨 Available Themes:")
        print("=" * 50)
        
        categories = {
            'Professional': ['1', '2'],
            'Minimal': ['3', '4'],
            'Gradient': ['5', '6', '7', '8'],
            'Modern': ['9', '10', '11', '12']
        }
        
        for category, theme_keys in categories.items():
            print(f"\n📂 {category}:")
            for key in theme_keys:
                theme = ALL_THEMES[key]
                print(f"   {key}. {theme['name'].replace('_', ' ').title()}")
                print(f"      {theme['description']}")
        
        print(f"\nUsage: python {sys.argv[0]} --package <package_name> --theme <1-12>")
        return
    
    # Update output directory if specified
    if args.output != OUTPUT_DIR:
        # We'll pass this to the generator instead of using global
        output_dir = args.output
    else:
        output_dir = OUTPUT_DIR
    
    # Create generator instance
    generator = UltimateBannerGenerator()
    
    # If both package and theme provided, do quick generation
    if args.package and args.theme:
        print(f"🚀 Quick Generation Mode")
        print(f"📦 Package: {args.package}")
        print(f"🎨 Theme: {ALL_THEMES[args.theme]['name'].replace('_', ' ').title()}")
        
        # Fetch package data
        print("📡 Fetching package data from PyPI...")
        package_data = generator.fetch_package_data(args.package)
        if not package_data:
            print("❌ Failed to fetch package data. Please check the package name.")
            sys.exit(1)
        
        # Generate banner
        theme = ALL_THEMES[args.theme]
        img = generator.generate_banner(package_data, theme)
        output_path = generator.save_banner(img, args.package, theme)
        
        file_size = os.path.getsize(output_path) / 1024
        print(f"✅ Banner generated: {output_path} ({file_size:.1f} KB)")
        return
    
    # If only package provided, interactive theme selection
    if args.package:
        print(f"📦 Package: {args.package}")
        print("🎨 Interactive theme selection...")
        
        # Override the get_package_name method result
        generator._package_name = args.package
        
        # Validate package exists
        print(f"🔍 Checking '{args.package}' on PyPI...")
        package_data = generator.fetch_package_data(args.package)
        if not package_data:
            print("❌ Package not found on PyPI. Please check the package name.")
            sys.exit(1)
        
        print(f"✅ Found: {package_data['name']}")
        print(f"   Version: {package_data.get('version', 'N/A')}")
        
        # Continue with theme selection
        selected_themes = generator.get_theme_choice()
        
        # Generate banners
        if len(selected_themes) == 1:
            theme = ALL_THEMES[selected_themes[0]]
            img = generator.generate_banner(package_data, theme)
            output_path = generator.save_banner(img, args.package, theme)
            
            file_size = os.path.getsize(output_path) / 1024
            print(f"✅ Banner generated: {output_path} ({file_size:.1f} KB)")
        else:
            generated_files = generator.generate_multiple_banners(package_data, selected_themes)
            total_size = sum(os.path.getsize(f) for f in generated_files) / 1024
            print(f"\n✅ Generated {len(generated_files)} banners ({total_size:.1f} KB total)")
        
        return
    
    # Fall back to full interactive mode
    generator.run()

if __name__ == "__main__":
    main()
