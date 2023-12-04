import argparse
import os
import qrcode

def check_installation(module_name):
    try:
        __import__(module_name)
    except ImportError:
        print(f"Installing {module_name}...")
        import subprocess
        subprocess.call(["pip", "install", module_name])
        print(f"{module_name} installed successfully.")

def generate_wifi_qrcode(ssid, password, output_path):
    check_installation("qrcode")

    wifi_data = f"WIFI:T:WPA;S:{ssid};P:{password};;"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(wifi_data)
    qr.make(fit=True)
    
    # Determine the output filename including the SSID
    filename = f"wifi_qrcode_{ssid}.png"
    output_file = os.path.join(output_path, filename)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_file)
    
    print(f"Wi-Fi QR code for SSID {ssid} generated successfully and saved at: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate QR code for Wi-Fi credentials")

    ssid = input("Enter Wi-Fi SSID: ")
    password = input("Enter Wi-Fi password (press Enter for no password): ")
    output_path = input("Enter the path to save the QR code (press Enter for current directory): ") or "."

    generate_wifi_qrcode(ssid, password, output_path)
