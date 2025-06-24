# Chat Bot

A simple chat bot project supporting both Python and Node.js environments.

## Features

- Python and Node.js support
- Ignores compiled files, environment files, and data/model files
- Ready for local development

## Setup

### Python

1. Create a virtual environment:
   ```
   python -m venv venv
   ```
2. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Node.js

1. Install dependencies:
   ```
   npm install
   ```

## Usage

- Run the Python bot:
  ```
  python main.py
  ```
- Run the Node.js bot:
  ```
  node index.js
  ```

## Project Structure

- `__pycache__/`, `*.pyc`, `*.pkl`: Python cache and model files (ignored)
- `*.h5`, `*.csv`: Model/data files (ignored)
- `node_modules/`: Node.js dependencies (ignored)
- `.env`, `venv/`: Environment files and folders (ignored)

## License

MIT License
