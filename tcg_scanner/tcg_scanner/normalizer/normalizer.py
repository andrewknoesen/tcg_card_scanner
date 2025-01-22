from pathlib import Path
from typing import List, Optional
import cv2
from matplotlib import pyplot as plt
import numpy as np


class Normalizer:
    def __init__(
        self,
        image_path: Optional[str] = f"{Path(__file__).parent}/image.png",
        sample_path: Optional[str] = f"{Path(__file__).parent}/samples",
    ):
        self.sample_path = sample_path
        self.set_image(image_path)
        self.height, self.width = self.img.shape[:2]

    def set_image(self, image_path: str):
        # Opening image
        self.img = cv2.imread(image_path)

        # OpenCV opens images as BRG
        # but we want it as RGB and
        # we also need a grayscale
        # version
        self.img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

    def display(self):
        # Creates the environment
        # of the picture and shows it
        plt.subplot(1, 1, 1)
        plt.imshow(self.img_rgb)
        plt.show()

    def order_points(self, pts):
        # Initialize ordered points array
        rect = np.zeros((4, 2), dtype="float32")

        # Get corners by sum and difference
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]  # Top-left
        rect[2] = pts[np.argmax(s)]  # Bottom-right

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]  # Top-right
        rect[3] = pts[np.argmax(diff)]  # Bottom-left

        return rect

    def extract_card(self, box) -> np.ndarray:
        # Get the lengths of the sides of the box
        side1 = np.linalg.norm(box[0] - box[1])
        side2 = np.linalg.norm(box[1] - box[2])

        width = int(max(side1, side2))
        height = int(min(side1, side2))

        src_points = self.order_points(np.float32(box))
        dst_points = np.array(
            [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
            dtype="float32",
        )

        matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        warped = cv2.warpPerspective(self.img, matrix, (width, height))

        # Rotate to make short end on top
        if width > height:
            warped = cv2.rotate(warped, cv2.ROTATE_90_CLOCKWISE)
            width, height = height, width

        # Get all sample masks from directory
        samples_dir = Path(__file__).parent / "samples"
        mask_paths = list(samples_dir.glob("*.png"))

        if not mask_paths:
            return warped

        top_height = int(height * 0.2)  # Use top 20% of card
        normal_total_score = 0
        rotated_total_score = 0

        # Compare with each mask
        for mask_path in mask_paths:
            sample_mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
            if sample_mask is not None:
                # Resize mask to match current card dimensions
                sample_mask = cv2.resize(sample_mask, (width, height))
                sample_mask = sample_mask[:top_height, :]

                # Compare normal orientation
                gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
                top_portion = gray[:top_height, :]
                normal_diff = cv2.absdiff(top_portion, sample_mask)
                normal_total_score += cv2.mean(normal_diff)[0]

                # Compare rotated orientation
                rotated = cv2.rotate(warped, cv2.ROTATE_180)
                rotated_gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
                rotated_top = rotated_gray[:top_height, :]
                rotated_diff = cv2.absdiff(rotated_top, sample_mask)
                rotated_total_score += cv2.mean(rotated_diff)[0]

        # Use orientation with best average match across all masks
        if rotated_total_score < normal_total_score:
            warped = cv2.rotate(warped, cv2.ROTATE_180)

        return warped

    def detect_rectangles(
        self, kernel: tuple[int, int] = (1, 1), show_plot: Optional[bool] = False
    ) -> List[np.ndarray]:
        blur = cv2.GaussianBlur(self.img_gray, (1, 1), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        inverted = thresh

        # Create kernel for morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel)
        morph = cv2.morphologyEx(inverted, cv2.MORPH_CLOSE, kernel)
        morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(
            morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        detected_cards = []  # Reset detected cards list

        for idx, cnt in enumerate(contours):
            if cv2.contourArea(cnt) > 1500:
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.intp(box)

                # Draw contour on original image
                cv2.drawContours(self.img, [box], 0, (0, 255, 0), 2)

                # Extract and flatten card
                card = self.extract_card(box)
                detected_cards.append(card)

                # Save individual card
                cv2.imwrite(f"outputs/card_{idx}.jpg", card)

        cv2.imwrite("rectangles.jpg", self.img)

        if show_plot:
            plt.figure(figsize=(20, 10))
            plt.subplot(1, 2, 1)
            plt.imshow(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
            plt.title("Detected Rectangles")

            # plt.tight_layout()
            plt.show()


if __name__ == "__main__":
    n = Normalizer("./image.png")
    n.display()
