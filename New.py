from ultralytics import YOLO
from huggingface_hub import hf_hub_download
from matplotlib import pyplot as plt

# Load model
model_path = hf_hub_download(local_dir=".",
                             repo_id="armvectores/yolov8n_handwritten_text_detection",
                             filename="best.pt")
model = YOLO(model_path)

# Your custom image path (ensure double backslashes or raw string for Windows paths)
image_path = r"C:\Project1\MYPROJ\photo.jpg"

# Run prediction
results = model.predict(source=image_path,
                        conf=0.5,
                        save=True,
                        show=False,
                        show_labels=False,
                        show_conf=False)

# Print detected boxes and classes
for result in results:
    boxes = result.boxes
    for box in boxes:
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        xyxy = box.xyxy[0].tolist()
        print(f"Class ID: {cls_id}, Confidence: {conf:.2f}, Box: {xyxy}")

# (Optional) Visualize result if saved
plt.figure(figsize=(15, 10))
plt.imshow(plt.imread('C:\Project1\MYPROJ\photo.jpg'))  # Adjust path if needed
plt.axis('off')
plt.show()