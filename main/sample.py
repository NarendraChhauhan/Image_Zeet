import torch
from PIL import Image
from typing import Any

class ImageSegmenter:
    def __init__(self, paths: list[str], show_image_var: bool = False):
        self.model = self._initialize_model()
        print('Initialized Model')
        self.paths = paths
        self.show_image_var = show_image_var

    def __call__(self):
        self.run()

    def __str__(self) -> str:
        return 'ImageSegmenter'
    
    def __repr__(self):
        return """ImageSegmenter(
        self.model,
        self.paths,
        self.show_image_var
        )"""

    def _initialize_model(self, repo_or_dir: str = 'ultralytics/yolov5', model_name: str = 'yolov5s') -> Any:
        model = torch.hub.load(repo_or_dir, model_name, pretrained=True)
        return model

    def open_image(self, image_path: str) -> Image:
        return Image.open(image_path)
    
    def open_images(self) -> list[Any]:
        images = []
        for path in self.paths:
            images.append(self.open_image(path))
        return images
    
    def save_image(self, results: Any) -> None:
        results.save()

    def show_image(self, results: Any):
        if self.show_image_var:
            results.show()
    
    def get_results(self, images: list[Any]) -> Any:
        results = self.model(images)
        return results
    
    def run(self):
        images = self.open_images()
        results = self.get_results(images=images)
        results.print()
        self.save_image(results=results)
        self.show_image(results=results)


if __name__ == '__main__':
    images = ["./main/gettyimages-1345111398-612x612 (1).jpg"]

    image_seg = ImageSegmenter(paths=images, show_image_var=False)

    image_seg.run()