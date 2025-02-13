from typing import Optional
import cv2
import pytesseract
from matplotlib import pyplot as plt
from tcg_scanner.normalizer.normalizer import Normalizer


class OCR:
    def __init__(self, n: Normalizer):
        self.n = n

        self.img = n.img.copy()  # Create a copy to avoid modifying original
        self.gray_scale = n.img_gray

        self.regions_percent = [
            (17, 6, 78, 5),  # Region 1: x=100, y=100, width=200, height=50
            (22, 11, 65, 2.5),  # Region 2: x=100, y=200, width=200, height=50
            (73, 94.5, 5.3, 2.8),
            (86, 94.5, 9, 2.8),
        ]
        self.regions = self.percentage_to_pixels(self.regions_percent)

    def percentage_to_pixels(self, regions_percent):
        """
        Convert percentage regions to pixel coordinates
        regions_percent: List of tuples (x%, y%, w%, h%)
        Returns: List of tuples (x_px, y_px, w_px, h_px)
        """
        pixel_regions = []
        for x_percent, y_percent, w_percent, h_percent in regions_percent:
            # Convert percentages to pixels
            x = int((x_percent / 100.0) * self.n.width)
            y = int((y_percent / 100.0) * self.n.height)
            w = int((w_percent / 100.0) * self.n.width)
            h = int((h_percent / 100.0) * self.n.height)

            pixel_regions.append((x, y, w, h))
        return pixel_regions

    def detect_all_text(self):
        # Convert to grayscale
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to preprocess the image
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Get text data including bounding boxes
        data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)

        return data["text"]

    def detect_text_in_regions(self):
        results = []
        for x, y, w, h in self.regions:
            # Extract region of interest (ROI)
            roi = self.img[y : y + h, x : x + w]
            # Preprocess the ROI
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            # Get text and bounding boxes for this region
            d = pytesseract.image_to_data(roi, output_type=pytesseract.Output.DICT)

            # Combine all valid words in this region into a sentence
            region_text = []
            region_bbox = None

            for i in range(len(d["text"])):
                if int(d["conf"][i]) > 0 and d["text"][i].strip():
                    region_text.append(d["text"][i])

                    # Store the overall bounding box for the region
                    if region_bbox is None:
                        region_bbox = (x, y, w, h)

            # Only append if we found text in this region

            results.append(" ".join(region_text))
        keys = ["title", "subtitle", "set", "number"]
        return dict(zip(keys, results))

    def draw_regions(self, output_path, show_plot: Optional[bool] = False):
        # Draw rectangles for specified regions
        for x, y, w, h in self.regions:
            cv2.rectangle(self.img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Save the image with bounding boxes
        cv2.imwrite(output_path, self.img)

        if show_plot:
            # Convert BGR to RGB for matplotlib display
            rgb_image = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            plt.figure(figsize=(10, 8))
            plt.imshow(rgb_image)
            plt.axis("off")
            plt.show()
