from rembg import remove
import os

def fonksiyon(input_path, output_path):
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Çıktı dizinini oluşturma
        with open(input_path, 'rb') as i:
            input_data = i.read()  # Girdi dosyasını okuma
            output_data = remove(input_data)  # Arka planı kaldırma
            with open(output_path, 'wb') as o:
                o.write(output_data)  # Çıktı dosyasını yazma
    except Exception as e:
        print(f"Error processing image: {e}")
        raise e
