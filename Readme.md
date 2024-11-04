# Keylogger Project

## Overview

This project provides a **keylogger system** for monitoring activity such as keystrokes, clipboard content, screenshots, and system information. Data is automatically encrypted and uploaded to a server, ensuring secure access and storage. A decryption system is included for authorized users to retrieve and analyze collected data.

---

## Features

### Keylogger (Client):
- Captures keystrokes, clipboard content, screenshots, and system info.
- Automatically uploads encrypted data to the server.

### Server:
- **Encrypted Storage**: All received data is securely encrypted.
- **Organized File Management**: Data categorized by machine ID.
- **Command Management**: Control client machines (e.g., `START`, `STOP`).
- **Decryption Support**: Includes scripts to decrypt and access data.

---

## Installation

### Server Setup:
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   python server.py
   ```

---

## Working with Encrypted Files

### Checking Encrypted Files:
- Uploaded files are located in the configured `UPLOAD_FOLDER`.
- Example folder structure:
  ```
  UPLOAD_FOLDER/
      Machine1/
          encrypted_keylog.txt
          encrypted_clipboard.txt
          encrypted_system_info.txt
          encrypted_screenshot_001.png
  ```

### Decrypting Files:
- Use the following provided scripts in the **cryptography** folder:

1. **decryption.py**:
   - Primary tool for decrypting files.
   - Usage:
     ```bash
     python cryptography/decryption.py -f <path_to_encrypted_file>
     ```

2. **Decryption_l.py** (For Text Files):
   - Alternative decryption script if issues occur.
   - Usage:
     ```bash
     python cryptography/Decryption_l.py -f <path_to_encrypted_text_file>
     ```

---

## Command Management

Control the behavior of the keylogger via the API:

- `GET /command/<machine_id>`: Retrieve machine command (default: `RUN`).
- `POST /command/<machine_id>`: Set a machine command (e.g., `STOP`, `PAUSE`).

---

## Security

- **Encrypted Data**: Ensures secure storage of all information.
- **Restricted Decryption**: Decryption keys and scripts are limited to authorized users.
- Ensure HTTPS for secure data transmission.

---

## Legal Disclaimer

This project is for **authorized use only**. Unauthorized deployment without the owner’s consent is illegal and unethical. Use responsibly.

---

## Future Enhancements

- Automate decryption of all files in bulk.
- Add encrypted communication between client and server.
- Implement a web dashboard for visualizing uploaded data.