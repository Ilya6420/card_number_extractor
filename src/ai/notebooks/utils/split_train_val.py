import random
from pathlib import Path


def split_train_val(annotation_file, train_ratio=0.8, seed=42):
    """
    Split the dataset into training and validation sets.
    
    Args:
        annotation_file (str): Path to the annotation file
        train_ratio (float): Ratio of data to use for training (default: 0.8)
        seed (int): Random seed for reproducibility (default: 42)
    """
    # Set random seed for reproducibility
    random.seed(seed)
    
    # Read all lines from the annotation file
    with open(annotation_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Shuffle the lines
    random.shuffle(lines)
    
    # Calculate split point
    split_idx = int(len(lines) * train_ratio)
    train_lines = lines[:split_idx]
    val_lines = lines[split_idx:]
    
    # Create output directory if it doesn't exist
    output_dir = Path(annotation_file).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write train annotations
    train_file = output_dir / 'train_annotations.txt'
    with open(train_file, 'w', encoding='utf-8') as f:
        f.writelines(train_lines)
    
    # Write validation annotations
    val_file = output_dir / 'val_annotations.txt'
    with open(val_file, 'w', encoding='utf-8') as f:
        f.writelines(val_lines)
    
    print(f"Total samples: {len(lines)}")
    print(f"Training samples: {len(train_lines)}")
    print(f"Validation samples: {len(val_lines)}")
    print(f"Train annotations saved to: {train_file}")
    print(f"Validation annotations saved to: {val_file}")

if __name__ == "__main__":
    # Path to the annotation file
    annotation_file = "paddle_ocr_det_annotations.txt"
    
    # Split the data
    split_train_val(annotation_file)
