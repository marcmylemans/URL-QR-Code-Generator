import argparse
import importlib
import subprocess
from datetime import datetime

# Check and install required modules
required_modules = ['qrcode[pil]', 'requests', 'importlib', 'os']
for module in required_modules:
    try:
        importlib.import_module(module)
    except ImportError:
        print(f"The '{module}' module is not installed. Installing it now...")
        subprocess.run(['pip', 'install', module])

# Now import the required modules
import qrcode
import requests
import csv
import os
from io import BytesIO

def generate_qr_code(url, output_directory):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f'qrcode_{url.replace("://", "_").replace("/", "_").replace("?", "_").replace(":", "_").replace(".", "_")}_{timestamp}.png'
    output_file = os.path.join(output_directory, filename)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    img.save(output_file)
    print(f"QR code for {url} generated and saved to {output_file}")

def process_urls_from_csv(csv_file, output_directory):
    with open(csv_file, 'r') as csv_input:
        reader = csv.DictReader(csv_input)
        for row in reader:
            url = row.get('url', '').strip()
            if url:
                generate_qr_code(url, output_directory)

def main():
    input_source = input("Enter a URL or the location of a CSV file: ")

    if input_source.endswith('.csv') and os.path.isfile(input_source):
        input_type = 'csv'
    elif '://' in input_source:
        input_type = 'url'
    else:
        print("Error: Invalid input. Please provide either a single URL or the location of a CSV file.")
        return

    output_directory = input("Enter the output directory for QR code images (default: qrcodes): ") or 'qrcodes'

    if input_type == 'url':
        generate_qr_code(input_source, output_directory)
    elif input_type == 'csv':
        process_urls_from_csv(input_source, output_directory)

if __name__ == "__main__":
    main()
