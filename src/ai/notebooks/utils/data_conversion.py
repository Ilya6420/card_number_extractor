import os
import glob
import json
import cv2


def prepare_detection_dataset(annotation_dir="../data/synthetic_data/detection/full_annotation", 
                              output_file="../data/synthetic_data/detection/paddle_ocr_det_annotations.txt", 
                              image_dir="../data/synthetic_data/detection/images"):
    """
    Convert JSON annotations to PaddleOCR detection format.
    
    Args:
        annotation_dir (str): Directory containing annotation JSON files
        output_file (str): Path to output annotation file
        image_dir (str): Directory containing the card images
    """
    # Function to convert bbox to 4-point format (clockwise from top-left)
    def bbox_to_points(bbox):
        x1, y1, x2, y2 = bbox
        return [
            [x1, y1],  # top-left
            [x2, y1],  # top-right
            [x2, y2],  # bottom-right
            [x1, y2],  # bottom-left
        ]
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Open output file
    with open(output_file, 'w') as out_file:
        # Find all annotation JSON files
        annotation_files = glob.glob(os.path.join(annotation_dir, "*_annotations.json"))
        print(f"Found {len(annotation_files)} annotation files")
        
        for annotation_file in annotation_files:
            # Determine the corresponding image file
            base_name = os.path.basename(annotation_file).replace("_annotations.json", "")
            image_file_name = f"{base_name}_full.png"
            image_path = os.path.join(image_dir, image_file_name)
            
            # Skip if image doesn't exist
            if not os.path.exists(image_path):
                print(f"Warning: Image file {image_path} not found, skipping")
                continue
            
            # Load annotation data
            with open(annotation_file, 'r') as f:
                annotation = json.load(f)
            
            # Parse all the fields into the PaddleOCR format
            annotations_list = []
            
            # Add card number annotation (currently only processing the card number)
            annotations_list.append({
                "transcription": annotation["number"]["text"],
                "points": bbox_to_points(annotation["number"]["bbox"])
            })
            
            # Generate and write line to output file
            relative_image_path = f'images/{image_file_name}'
            output_line = f'{relative_image_path}\t{json.dumps(annotations_list)}'
            out_file.write(output_line + '\n')
    
    print(f"Processed annotations written to {output_file}")


def prepare_recognition_dataset(detection_annotations_path="../data/synthetic_data/detection/paddle_ocr_det_annotations.txt", 
                                output_dir="../data/synthetic_data/recognition", 
                                output_annotations_path="../data/synthetic_data/recognition/paddle_ocr_req_annotations.txt"):
    """
    Prepare a recognition dataset from detection annotations by cropping card number regions.
    
    Args:
        detection_annotations_path (str): Path to the detection annotations file
        output_dir (str): Directory to save cropped images
        output_annotations_path (str): Path to save recognition annotations
    """
    # Create output directories
    images_dir = os.path.join(output_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    # Read annotations
    with open(detection_annotations_path, 'r') as f:
        annotations = f.readlines()

    # Process each annotation
    train_annotations = []
    processed_count = 0
    
    for idx, line in enumerate(annotations, 1):
        # Parse the line
        parts = line.strip().split('\t')
        if len(parts) != 2:
            continue
            
        img_path = parts[0]
        detection_img_path = os.path.join(os.path.dirname(detection_annotations_path), img_path)
        annotation = json.loads(parts[1])[0]
        
        # Read the image
        img = cv2.imread(detection_img_path)
        if img is None:
            print(f"Could not read image: {detection_img_path}")
            continue
        
        # Get coordinates
        points = annotation['points']
        x1, y1 = points[0]
        x2, y2 = points[1]
        x3, y3 = points[2]
        x4, y4 = points[3]
        
        # Get the transcription
        transcription = annotation['transcription']
        
        # Ensure it's a 16-digit number
        if len(transcription) != 16 or not transcription.isdigit():
            continue
        
        # Crop the region
        cropped = img[int(y1):int(y3), int(x1):int(x2)]
        
        # Save cropped image
        output_img_name = f'seq_{idx:03d}.jpg'
        output_img_path = os.path.join(images_dir, output_img_name)
        cv2.imwrite(output_img_path, cropped)
        
        # Add to training annotations
        train_annotations.append(f"images/{output_img_name}\t{transcription}\n")
        processed_count += 1

    # Save training annotations
    with open(output_annotations_path, 'w', encoding='utf-8') as f:
        f.writelines(train_annotations)

    print(f"Processed {processed_count} images")
    return processed_count
