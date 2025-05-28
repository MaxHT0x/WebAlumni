# Windsurf Web Alumni Version

This project is a Flask-based web application designed for processing and analyzing alumni data, primarily from Excel files. The application allows users to upload data, which is then cleaned, normalized (e.g., standardizing company names, employment status), and analyzed by the backend. The processed information or generated reports are then made available for download, likely as new Excel files.

## Project Structure

- `app.py`: Main Flask application logic, file uploads, data processing, API endpoints.
- `templates/index.html`: Main UI for file uploads and interaction.
- `uploads/`: Stores uploaded files (ignored by Git).
- `generated_files/`: Stores processed output files (ignored by Git).
- `requirements.txt`: Lists the Python dependencies for the project.
- `.venv/`: Python virtual environment (ignored by Git).

## Setup and Installation

### 1. Download Source Code

Clone the repository to your local machine (once you've pushed it to GitHub):
```bash
git clone <your-repository-url>
cd Windsurf-Web-Alumni-Version
```

Alternatively, you can download the source code as a ZIP file and extract it.

### 2. Create and Activate Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
# Create a virtual environment (e.g., named .venv)
python -m venv .venv

# Activate the virtual environment
# On Windows
.venv\Scripts\activate
# On macOS/Linux
# source .venv/bin/activate
```

### 3. Install Requirements

Install the necessary Python packages using pip and the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Running the Application

Once the setup is complete, you can run the Flask application:

```bash
python app.py
```

The application will typically be available at `http://127.0.0.1:5000/` in your web browser.
