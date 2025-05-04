import os
import random
import json
from typing import List, Tuple
from faker import Faker
from PIL import Image, ImageDraw, ImageFont


class CreditCardGenerator:
    def __init__(self, 
                 background_dir: str = "../backgrounds",
                 text_fonts_dir: str = "../fonts",
                 output_dir: str = "../data/synthetic_data/detection",
                 random_seed: int = 42):
        """Initialize the generator with paths to required assets"""
        self.background_dir = background_dir
        self.text_fonts_dir = text_fonts_dir
        self.output_dir = output_dir
        
        # Set seeds for reproducibility
        random.seed(random_seed)
        self.faker = Faker()
        self.faker.seed_instance(random_seed)
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "full_annotation"), exist_ok=True)
        
        # Load available fonts
        self.text_fonts = self._load_fonts(text_fonts_dir)
        
        # Standard card size
        self.card_size = (850, 540)
        
    def _load_fonts(self, font_dir: str) -> List[str]:
        """Load all .ttf fonts from directory"""
        return [os.path.join(font_dir, f) for f in os.listdir(font_dir) 
                if f.endswith('.ttf')]
    
    def _generate_mock_data(self) -> dict:
        """Generate random card data"""
        return {
            'number': f"{random.randint(1000,9999)} {random.randint(1000,9999)} "
                     f"{random.randint(1000,9999)} {random.randint(1000,9999)}",
            'valid': f"{random.randint(1,12):02d}/{random.randint(23,30)}",
            'name': self.faker.name().upper(),
            'bank': self.faker.company().upper() + " BANK"
        }
    
    def draw_text_with_shadow(self, 
                            draw: ImageDraw,
                            position: Tuple[int, int],
                            text: str,
                            font: ImageFont,
                            text_color: str = "white",
                            shadow_color: str = "black",
                            offset: int = 2) -> None:
        """Draw text with shadow effect"""
        x, y = position
        # Draw shadow
        draw.text((x + offset, y + offset), text, font=font, fill=shadow_color)
        # Draw text
        draw.text((x, y), text, font=font, fill=text_color)

    def calculate_text_bbox(self,
                          draw: ImageDraw,
                          position: Tuple[int, int],
                          text: str,
                          font: ImageFont,
                          bbox_margin: int = 10) -> dict:
        """Calculate text bounding box without drawing it and return bbox coordinates"""
        # Get bounding box
        left, top, right, bottom = draw.textbbox(position, text, font=font)
        
        # Add margin
        enlarged_bbox = (
            left - bbox_margin,
            top - bbox_margin,
            right + bbox_margin,
            bottom + bbox_margin
        )
        
        # Draw text with shadow
        self.draw_text_with_shadow(draw, position, text, font)
        
        return {
            'text': text,
            'bbox': list(enlarged_bbox),
            'position': list(position)
        }

    def generate_card(self, 
                     background_path: str,
                     card_font_size: int = 50,
                     save: bool = True,
                     show: bool = False) -> Tuple[Image.Image, dict]:
        """Generate a single credit card with annotations"""
        # Load and resize background
        card = self._prepare_background(background_path)
        
        # Create two copies for visualization
        card_groups = card.copy()
        card_full = card.copy()
        
        # Setup drawing
        draw_groups = ImageDraw.Draw(card_groups)
        draw_full = ImageDraw.Draw(card_full)
        
        # Random font for this card
        base_font = random.choice(self.text_fonts)
        
        # Generate random card data
        card_data = self._generate_mock_data()
        
        # Draw all elements and collect annotations
        annotations = {}
        
        # Draw bank name
        annotations['bank'] = self._draw_bank_name(
            draw_groups, draw_full, card_data['bank'], base_font, card_font_size
        )
        
        # Draw card number
        number_annotations = self._draw_card_number(
            draw_groups, draw_full, card_data['number'], base_font, card_font_size
        )
        annotations['number_parts'] = number_annotations['parts']
        annotations['number'] = number_annotations['full']
        
        # Draw expiration date
        annotations['valid'] = self._draw_expiration_date(
            draw_groups, draw_full, card_data['valid'], base_font, card_font_size
        )
        
        # Draw cardholder name
        annotations['name'] = self._draw_cardholder_name(
            draw_groups, draw_full, card_data['name'], base_font, card_font_size
        )
        
        if save:
            self._save_card_files(card_groups, card_full, annotations)
        
        if show:
            card_full.show()
            
        return card_groups, annotations
    
    def _prepare_background(self, background_path: str) -> Image.Image:
        """Load and prepare the card background"""
        card = Image.open(background_path).convert("RGB")
        return card.resize(self.card_size)
    
    def _draw_bank_name(self, draw_groups, draw_full, bank_name, base_font, card_font_size):
        """Draw bank name on both card versions and return annotations"""
        bank_font_size = card_font_size - 10
        bank_font = ImageFont.truetype(base_font, bank_font_size)
        
        # Position bank name in top left, top right, or top middle
        card_width = self.card_size[0]
        position_type = random.choice(['left', 'middle', 'right'])
        
        if position_type == 'left':
            bank_name_position = (50, 20)
        elif position_type == 'middle':
            # Calculate middle position based on card width
            bank_name_position = (card_width // 2 // 2, 20)
        else:  # right
            bank_name_position = (card_width - 400, 20)
        
        # Draw bank name on both images without bounding boxes
        bank_annotation = self.calculate_text_bbox(draw_groups, bank_name_position, 
                                                 bank_name, bank_font)
        self.draw_text_with_shadow(draw_full, bank_name_position, bank_name, bank_font)
        
        return bank_annotation
    
    def _draw_card_number(self, draw_groups, draw_full, card_number, base_font, card_font_size):
        """Draw card number on both card versions and return annotations"""
        number_font_size = card_font_size - 10
        number_font = ImageFont.truetype(base_font, number_font_size)
        
        # Draw card number with even spacing
        number_groups = card_number.split()
        x = 50  # Starting x position
        y = 300  # Fixed y position
        spacing = random.randint(120, 180)  # Random space between number groups
        
        # Store individual number part bboxes
        number_parts = []
                
        # Draw each number group and collect bboxes on first image (grouped)
        for i, group in enumerate(number_groups):
            position = (x + i * spacing, y)
            bbox_info = self.calculate_text_bbox(draw_groups, position, group, number_font)
            number_parts.append(bbox_info)
        
        # Get the bounding box coordinates for the full number
        first_bbox = number_parts[0]['bbox']
        last_bbox = number_parts[-1]['bbox']
        full_number_bbox = [
            first_bbox[0],  # leftmost x
            first_bbox[1],  # topmost y
            last_bbox[2],   # rightmost x
            last_bbox[3]    # bottom y
        ]
        
        # Draw the full number on the second image with the same positioning as the groups
        # Draw the text with shadow for each digit group at the same positions
        for i, group in enumerate(number_groups):
            position = (x + i * spacing, y)
            self.draw_text_with_shadow(draw_full, position, group, number_font)
        
        # Store the full number annotation
        full_number = {
            'text': card_number.replace(' ', ''),  # Store without spaces
            'bbox': full_number_bbox,
            'position': [x, y]
        }
        
        return {
            'parts': number_parts,
            'full': full_number
        }
    
    def _draw_expiration_date(self, draw_groups, draw_full, valid_date, base_font, card_font_size):
        """Draw expiration date on both card versions and return annotations"""
        valid_font_size = card_font_size - 30
        valid_font = ImageFont.truetype(base_font, valid_font_size)
        
        date_font_size = card_font_size - 30
        date_font = ImageFont.truetype(base_font, date_font_size)
        
        valid_position = (50, 380)
        thru_position = (50, 400)
        date_position = (120, 390)
        
        # Draw on both images
        for draw in [draw_groups, draw_full]:
            # Draw VALID text
            self.draw_text_with_shadow(draw, valid_position, "VALID", valid_font)
            # Draw THRU text
            self.draw_text_with_shadow(draw, thru_position, "THRU", valid_font)
        
        # Draw date with bbox on both images
        date_annotation = self.calculate_text_bbox(draw_groups, date_position, valid_date, date_font)
        self.draw_text_with_shadow(draw_full, date_position, valid_date, date_font)
        
        return date_annotation
    
    def _draw_cardholder_name(self, draw_groups, draw_full, name, base_font, card_font_size):
        """Draw cardholder name on both card versions and return annotations"""
        name_font_size = card_font_size - 10
        name_font = ImageFont.truetype(base_font, name_font_size)
        
        name_position = (50, 470)
        
        # Draw name with bbox on both images
        name_annotation = self.calculate_text_bbox(draw_groups, name_position, name, name_font)
        self.draw_text_with_shadow(draw_full, name_position, name, name_font)
        
        return name_annotation
    
    def _save_card_files(self, card_groups, card_full, annotations):
        """Save card images and annotations to files"""
        # Generate random filename base
        file_base = f"card_{random.randint(1000,9999)}"
        
        # Save images
        #card_groups.save(os.path.join(self.output_dir, f"{file_base}_groups.png"))
        card_full.save(os.path.join(self.output_dir, "images", f"{file_base}_full.png"))
        
        # Save annotations
        annotations_filename = f"{file_base}_annotations.json"
        with open(os.path.join(self.output_dir, "full_annotation", annotations_filename), 'w') as f:
            json.dump(annotations, f, indent=4)
