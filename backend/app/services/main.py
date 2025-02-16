from pathlib import Path
from services.normalizer.normalizer import Normalizer
from services.ocr.ocr import OCR
from services.swudb.swudb import SWUDB


def main():
    # n = Normalizer(f"{Path(__file__).parent}/tcg_scanner/normalizer/cloud-rider.png")
    # n = Normalizer(f"{Path(__file__).parent}/tcg_scanner/normalizer/nala.webp")
    n = Normalizer(f"{Path(__file__).parent}/tcg_scanner/normalizer/photo.jpeg")
    # n = Normalizer(f"{Path(__file__).parent}/tcg_scanner/normalizer/iso.png")
    # n = Normalizer()
    # n.display()

    # ocr = OCR(n)
    # ocr.detect_all_text()
    
    # print(f"Detected text: {ocr.detect_all_text()}")

    # results = ocr.detect_text_in_regions()
    # ocr.draw_regions("output_with_boxes.jpg", show_plot=True)
    # print(
    #     "########################################## OCR ##########################################"
    # )
    # print(results)
    # print(
    #     "#########################################################################################"
    # )
    n.detect_rectangles(kernel=(3,3))

    swudb = SWUDB()

    # print(swudb.get_card(results["set"], int(results["number"].split("/")[0])))


if __name__ == "__main__":
    main()
