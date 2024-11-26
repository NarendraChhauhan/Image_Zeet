import cv2
import numpy as np
from tensorflow.keras.applications import mobilenet_v2
from tensorflow.keras.preprocessing import image as tf_image

def analyze_image(image_path):
    details = {}

    # Load and process image
    img = cv2.imread(image_path)
    if img is None:
        return {"error": "Unable to read the image"}

    img_resized = cv2.resize(img, (224, 224))

    # Object Detection using MobileNetV2
    mobilenet_model = mobilenet_v2.MobileNetV2(weights='imagenet')
    img_array = tf_image.img_to_array(img_resized)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = mobilenet_v2.preprocess_input(img_array)
    predictions = mobilenet_model.predict(img_array)
    decoded_predictions = mobilenet_v2.decode_predictions(predictions, top=3)

    object_details = [{"object": pred[1], "confidence": float(pred[2])} for pred in decoded_predictions[0]]
    details["objects_detected"] = object_details

    # Face Detection with Haar Cascades
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    details["faces_detected"] = len(faces)

    return details
# import torch
# from PIL import Image
# from typing import Any

# class ImageSegmenter:
#     def __init__(self, paths: list[str], show_image_var: bool = False):
#         self.model = self._initialize_model()
#         print('Initialized Model')
#         self.paths = paths
#         self.show_image_var = show_image_var

#     def __call__(self):
#         self.run()

#     def __str__(self) -> str:
#         return 'ImageSegmenter'
    
#     def __repr__(self):
#         return """ImageSegmenter(
#         self.model,
#         self.paths,
#         self.show_image_var
#         )"""

#     def _initialize_model(self, repo_or_dir: str = 'ultralytics/yolov5', model_name: str = 'yolov5s') -> Any:
#         model = torch.hub.load(repo_or_dir, model_name, pretrained=True)
#         return model

#     def open_image(self, image_path: str) -> Image:
#         return Image.open(image_path)
    
#     def open_images(self) -> list[Any]:
#         images = []
#         for path in self.paths:
#             images.append(self.open_image(path))
#         return images
    
#     def save_image(self, results: Any) -> None:
#         results.save()

#     def show_image(self, results: Any):
#         if self.show_image_var:
#             results.show()
    
#     def get_results(self, images: list[Any]) -> Any:
#         results = self.model(images)
#         return results
    
#     def run(self):
#         images = self.open_images()
#         results = self.get_results(images=images)
#         results.print()
#         self.save_image(results=results)
#         self.show_image(results=results)

# if __name__ == '__main__':
#     images = ["./main/gettyimages-1345111398-612x612 (1).jpg"]

#     image_seg = ImageSegmenter(paths=images, show_image_var=False)

#     image_seg.run()

