# Keylogger Project

## Overview

This project is a **keylogger system** designed to monitor and log activities such as keystrokes, clipboard content, screenshots, and system information, with an option to upload all data securely to a Flask server.

The `system_checker.py` file is a **keylogger script** designed to disguise its purpose under a generic-sounding name. It operates by:
- Logging user input (keystrokes, clipboard, screenshots).
- Encrypting data using the **Fernet encryption algorithm**.
- Uploading encrypted data to a local/remote server for storage.

The project includes tools to:
1. **Run the server.**
2. **Send commands to clients via the server's API.**
3. **Decrypt uploaded files for analysis.**

---

## Features

### Keylogger (Client — `system_checker.py`)
- Captures:
   - **Keystrokes** (e.g., user input and special keys like `ENTER` and `SPACE`).
   - **Clipboard** data changes.
   - **Screenshots** periodically.
   - **System information** (e.g., machine name, IP address).
- Encrypts captured files using the `cryptography` library for secure transmission.
- Automatically uploads encrypted data to the **Flask server**.

### Server (`server.py`)
- Stores files uploaded by various clients organized by their `machine_id`.
- Offers an API to:
   - **Control logging activity** (start, stop, pause, or resume).
   - Manage client-specific commands via HTTP requests.

---

## Installation and Usage

### 1. Setting Up the Server
1. **Clone the repo**:
    ```bash
    git clone <repository_link>
    cd Keylogger
    ```

2. **Install Python dependencies**:
    ```bash
    pip install flask flask-sqlalchemy
    ```

3. **Run the server**:
    ```bash
    python server.py
    ```

4. **Access the Server Features**:
   - **Upload Files:** POST to `/upload`.
   - **Send Commands:** Use `/command/<machine_id>` endpoints (see below).

---

### 2. Running the Keylogger (`system_checker.py`)
1. Edit the `system_checker.py` file, if necessary (e.g., change the server IP and port).
2. Run the script:
    ```bash
    python system_checker.py
    ```
3. The script will:
   - Log user activity into encrypted files.
   - Upload the files to the server for secure storage.

---

### 3. Sending Commands to a Client
The server provides an API to send specific instructions to clients. For example:
- To **stop** data logging:
    ```bash
    curl -X POST -H "Content-Type: application/json" \
         -d '{"command": "STOP"}' \
         http://127.0.0.1:5001/command/<machine_id>
    ```

Commands include:
| Command     | Description                               |
|-------------|-------------------------------------------|
| **RUN**     | Start or continue logging.               |
| **STOP**    | Completely stop logging.                 |
| **PAUSE**   | Pause logging temporarily.               |
| **RESUME**  | Resume paused logging.                   |

---

### 4. Decrypting Files
To analyze logged data, use the provided `Decryption.py` script:
1. Ensure the `upload` folder contains encrypted files.
2. Edit the `upload_folder` path in `Decryption.py` to point to the folder.
3. Run the script:
    ```bash
    python Decryption.py
    ```
4. Decrypted files will be saved with the prefix `d_` (e.g., `d_key_log.txt`).

---

## Disclaimer

**This software is for authorized use only. Deploying it without owner consent is illegal and unethical. Use responsibly.**