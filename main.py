""" Script for OCR of Text from PDFs and images """

import os
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "pytesseract/tesseract.exe"

def process_pdf(pdf_file, input_docs, extracted_txt):
    images = convert_from_path(pdf_file)
    extracted_text = ""

    for i, image in enumerate(images):
        image_path = os.path.join(input_docs, f"{i+1}.jpg")
        image.save(image_path)
        text = pytesseract.image_to_string(image)
        extracted_text += f"Text from page {i+1}:\n{text}\n\n"
        os.remove(image_path)

    with open(extracted_txt, 'w', encoding='utf-8') as file:
        file.write(extracted_text)

def process_image(image_path, extracted_txt):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    with open(extracted_txt, 'w', encoding='utf-8') as file:
        file.write(text)

def process_files_in_directory(INPUT_DIRECTORY, OUTPUT_DIRECTORY):
    for filename in os.listdir(INPUT_DIRECTORY):
        file_path = os.path.join(INPUT_DIRECTORY, filename)
        base_name, file_extension = os.path.splitext(filename)

        if file_extension.lower() == ".pdf":
            pdf_folder = os.path.join(OUTPUT_DIRECTORY, "PDF's text")
            os.makedirs(pdf_folder, exist_ok=True)
            extracted_txt = os.path.join(pdf_folder, f"{base_name}.txt")
            process_pdf(file_path, pdf_folder, extracted_txt)

        elif file_extension.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            image_folder = os.path.join(OUTPUT_DIRECTORY, "Photo's text")
            os.makedirs(image_folder, exist_ok=True)
            extracted_txt = os.path.join(image_folder, f"{base_name}.txt")
            process_image(file_path, extracted_txt)

if __name__ == "__main__":
    INPUT_DIRECTORY = "input_documents"
    OUTPUT_DIRECTORY = "extracted_text"
    process_files_in_directory(INPUT_DIRECTORY, OUTPUT_DIRECTORY)