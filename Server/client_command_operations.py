import requests

# Server URL
SERVER_URL = "http://127.0.0.1:5001"

# Machine ID (Example: Replace with actual client IDs)
MACHINE_ID = "DESKTOP-SA1ONQI"


def get_command(machine_id):
    """Retrieve the current command for a client."""
    try:
        response = requests.get(f"{SERVER_URL}/command/{machine_id}")
        if response.status_code == 200:
            command_data = response.json()
            print(f"Current Command for {machine_id}: {command_data['current_command']}")
        else:
            print(f"Failed to retrieve command. Status Code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error fetching command: {e}")


def set_command(machine_id, command):
    """Set a new command for a client."""
    try:
        payload = {"command": command}
        response = requests.post(f"{SERVER_URL}/command/{machine_id}", json=payload)
        if response.status_code == 200:
            print(f"Successfully set command: {command}")
            print(response.json())
        else:
            print(f"Failed to set command. Status Code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error setting command: {e}")

# Uncomment any operation below to run it:

# Example: Fetch the current command for the machine
#get_command(MACHINE_ID)

# Example: Set a new command for the machine
set_command(MACHINE_ID, "STOP")
#set_command(MACHINE_ID, "RUN")
#set_command(MACHINE_ID, "PAUSE")

# Example: Test updating to a custom command:
# set_command(MACHINE_ID, "CUSTOM_COMMAND")