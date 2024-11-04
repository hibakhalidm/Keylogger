import requests


def set_command(machine_id, command):
    url = f"http://127.0.0.1:5000/command/{machine_id}"
    response = requests.post(url, json={"command": command})
    print(f"Set command response: {response.json()}")


def get_command(machine_id):
    url = f"http://127.0.0.1:5000/command/{machine_id}"
    response = requests.get(url)
    print(f"Current command: {response.json()['current_command']}")


if __name__ == "__main__":
    machine_id = "DESKTOP-4IH3VOH"

    # Set command to STOP
    set_command(machine_id, "STOP")

    # Get the current command
    get_command(machine_id)

    # # Reset command to RUN after some time if needed
    #set_command(machine_id, "RUN")
