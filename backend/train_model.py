import os
import shutil
import random
from ultralytics import YOLO

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "temp_data", "Soil types")
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

def prepare_dataset():
    if os.path.exists(DATASET_DIR):
        shutil.rmtree(DATASET_DIR)
    
    os.makedirs(os.path.join(DATASET_DIR, "train"), exist_ok=True)
    os.makedirs(os.path.join(DATASET_DIR, "val"), exist_ok=True)
    
    classes = os.listdir(RAW_DATA_DIR)
    print(f"Detected classes: {classes}")
    
    for cls in classes:
        cls_path = os.path.join(RAW_DATA_DIR, cls)
        if not os.path.isdir(cls_path):
            continue
            
        images = [f for f in os.listdir(cls_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        random.shuffle(images)
        
        split = int(0.8 * len(images))
        train_imgs = images[:split]
        val_imgs = images[split:]
        
        # Create class folders in train/val
        os.makedirs(os.path.join(DATASET_DIR, "train", cls), exist_ok=True)
        os.makedirs(os.path.join(DATASET_DIR, "val", cls), exist_ok=True)
        
        for img in train_imgs:
            shutil.copy(os.path.join(cls_path, img), os.path.join(DATASET_DIR, "train", cls, img))
        for img in val_imgs:
            shutil.copy(os.path.join(cls_path, img), os.path.join(DATASET_DIR, "val", cls, img))
            
    print("Dataset prepared successfully.")

def train():
    print("Starting Advanced AI Model Training (High Intensity)...")
    # Using 's' (Small) instead of 'n' (Nano) for much better feature extraction
    model = YOLO("yolov8s-cls.pt") 
    
    # Advanced Training Parameters
    # imgsz=416: Higher resolution for better texture detection
    # epochs=50: More training cycles
    # patience=10: Early stopping if no improvement for 10 epochs
    # dropout=0.1: Prevent overfitting
    results = model.train(
        data=DATASET_DIR, 
        epochs=50, 
        imgsz=416,
        batch=16,
        patience=10,
        dropout=0.1,
        project=os.path.join(BASE_DIR, "runs"),
        name="soil_classifier_v2"
    )
    
    # Export the best model to a final location
    best_model_path = os.path.join(BASE_DIR, "runs", "soil_classifier_v2", "weights", "best.pt")
    final_model_path = os.path.join(BASE_DIR, "soil_model_v2.pt")
    shutil.copy(best_model_path, final_model_path)
    
    # Update current system to use the new best model
    prod_model_path = os.path.join(BASE_DIR, "soil_model.pt")
    shutil.copy(final_model_path, prod_model_path)
    
    print(f"✅ Enhanced Model trained and saved as {prod_model_path}")

if __name__ == "__main__":
    # Ensure data is fresh
    prepare_dataset()
    train()
