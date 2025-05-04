import re

import numpy as np
from paddleocr import PaddleOCR

from core.logging_config import get_logger


logger = get_logger(__name__)


class CardNumberExtractor:
    def __init__(self, threshold: int = 10):
        self.threshold: int = threshold  # Acceptable Y-difference for grouping digits
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')

    def extract_card_number(self, image) -> tuple[str | None, list | None, float | None]:
        """Extract credit card number from image bytes"""

        logger.debug("Running OCR on image")
        if image.mode != 'RGB':
            logger.debug("Converting image to RGB mode")
            image = image.convert('RGB')

        image_np = np.array(image)
        result = self.ocr.ocr(image_np, cls=True)[0]
        print(result)
        logger.info(f"OCR result: {result}")
        # First try to find a complete 16-digit number
        logger.debug("Searching for complete 16-digit card number")
        full_card_number, bbox, confidence = self._find_full_card_number(result)
        if full_card_number:
            logger.info(f"Found complete 16-digit card number: {full_card_number[:4]}****{full_card_number[-4:]}")
            return full_card_number, bbox, confidence

        # If no complete number found, try to assemble from 4-digit groups
        logger.debug("No complete number found, attempting to assemble from 4-digit groups")
        return self._assemble_from_digit_groups(result)

    def _find_full_card_number(self, ocr_result: list) -> tuple[str | None, list | None, float | None]:
        """Look for a complete 16-digit number in the OCR results"""
        for box, (text, conf) in ocr_result:
            # Remove spaces and check if it's a 16-digit number
            cleaned_text = text.replace(" ", "")
            if re.fullmatch(r'\d{16}', cleaned_text):
                logger.debug(f"Detected complete 16-digit card number with confidence: {conf}")
                return cleaned_text, box, conf
        return None, None, None

    def _assemble_from_digit_groups(self, ocr_result: list) -> tuple[str | None, list | None, float | None]:
        """Assemble card number from 4-digit groups"""
        # Extract 4-digit numbers with their vertical positions
        digits_with_y = self._extract_digit_groups(ocr_result)
        logger.debug(f"Found {len(digits_with_y)} 4-digit groups")

        if len(digits_with_y) < 4:
            logger.warning("Not enough 4-digit groups found to form a card number")
            return None, None, None

        # Group digits on the same line and assemble card number
        return self._group_digits_by_position(digits_with_y)

    def _extract_digit_groups(self, ocr_result: list) -> list[tuple[str, float, list, float]]:
        """Extract all 4-digit groups with their vertical center positions"""
        digits_with_y = []
        for box, (text, conf) in ocr_result:
            if re.fullmatch(r'\d{4}', text):
                # Calculate average Y center of bounding box
                y_coords = [point[1] for point in box]
                avg_y = sum(y_coords) / len(y_coords)
                logger.debug(f"Found 4-digit group: {text} at y-position: {avg_y:.2f}")
                digits_with_y.append((text, avg_y, box, conf))
        return digits_with_y

    def _group_digits_by_position(self, digits_with_y: list[tuple[str, float, list, float]]) -> tuple[str | None, list | None, float | None]:
        """Group 4-digit numbers that appear on the same line"""
        used = set()

        for i, (text1, y1, box1, conf1) in enumerate(digits_with_y):
            if i in used:
                continue

            # Build a group with matching Y positions
            group = [(text1, box1, conf1)]
            used.add(i)

            # Find all other digits on the same line
            for j, (text2, y2, box2, conf2) in enumerate(digits_with_y):
                if j != i and j not in used and abs(y1 - y2) <= self.threshold:
                    group.append((text2, box2, conf2))
                    used.add(j)

            if len(group) == 4:
                # Sort left to right by the X of the first corner
                group_sorted = sorted(group, key=lambda x: x[1][0][0])
                card_number = ''.join([g[0] for g in group_sorted])

                # Combine all bounding boxes
                all_points = []
                for _, box, _ in group_sorted:
                    all_points.extend(box)

                # Create a bounding box that encompasses all digit groups
                min_x = min(point[0] for point in all_points)
                min_y = min(point[1] for point in all_points)
                max_x = max(point[0] for point in all_points)
                max_y = max(point[1] for point in all_points)

                combined_bbox = [[min_x, min_y], [max_x, min_y], [max_x, max_y], [min_x, max_y]]

                # Calculate mean confidence
                mean_confidence = sum(g[2] for g in group_sorted) / len(group_sorted)

                logger.info(f"Assembled 16-digit card number: {card_number[:4]}****{card_number[-4:]} with confidence: {mean_confidence:.4f}")
                return card_number, combined_bbox, mean_confidence

        logger.warning("Could not assemble a complete card number from 4-digit groups")
        return None, None, None


# Create a singleton instance
card_number_extractor = CardNumberExtractor()
