import os
from imageai.Detection import ObjectDetection

# Model dosyasının yolu
model_path = "static/models/yolov3.pt"

# Model dosyasının varlığını kontrol et
if not os.path.isfile(model_path):
    raise FileNotFoundError(f"Model dosyası bulunamadı: {model_path}")

# Nesne algılayıcıyı ayarla
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(model_path)
detector.loadModel()

def detect_objects(image_path):
    detections = detector.detectObjectsFromImage(
        input_image=image_path,
        output_image_path="static/resimler/output_image.jpg",
        minimum_percentage_probability=15)
    
    categories = {
        'vehicles': ['bicycle', 'car', 'motorbike', 'bus', 'truck'],
        'traffic_signs': ['traffic_light', 'stop_sign', 'parking_meter'],
        'people': ['person'],
        'animals': ['bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe'],
        'plants': ['pottedplant'],
        'kitchen_appliances': ['microwave', 'oven'],
        'travel_items': ['backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports_ball', 'kite', 'surfboard', 'tennis_racket'],
        'furniture': ['chair', 'sofa', 'bed', 'diningtable', 'toilet'],
        'electronics': ['tvmonitor', 'laptop', 'mouse', 'remote', 'keyboard', 'cell_phone'],
        'food_and_drinks': ['bottle', 'wine_glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot_dog', 'pizza', 'donut', 'cake'],
        'library_items': ['book']
    }
    
    scores = {category: 0 for category in categories}

    for detection in detections:
        obj_name = detection["name"]
        for category, items in categories.items():
            if obj_name in items:
                scores[category] += 1

    max_category = max(scores, key=scores.get)
    
    messages = {
        "vehicles": "Burası Taşıtlar ile dolu",
        "traffic_signs": "Trafik işaretleri mevcut",
        "people": "İnsanlar burada",
        "animals": "Hayvanlar ve doğa mükemmel uyum",
        "plants": "Bitkiler burada",
        "kitchen_appliances": "Mutfak aletleri burada",
        "travel_items": "Seyahat eşyaları mevcut",
        "furniture": "Mobilyalar var",
        "electronics": "Elektronik cihazlar burada",
        "food_and_drinks": "Yiyecekler ve içecekler mevcut",
        "library_items": "Kütüphane eşyaları burada"
    }

    return messages.get(max_category, "Ortam belirlenemedi.")
