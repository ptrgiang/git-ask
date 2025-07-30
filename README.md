# Git Command Generator

A simple desktop application that helps you find the right Git commands using natural language. 

This tool provides a graphical user interface (GUI) where you can describe a task you want to perform in Git (e.g., "create a new branch called 'feature'"), and it will generate the corresponding command-line instructions.

## Features

- **Natural Language Input:** Describe what you want to do in plain English.
- **Instant Command Generation:** Get the Git commands you need in seconds.
- **Cross-Platform:** Built with Python and Tkinter, it runs on Windows, macOS, and Linux.

## API Usage

This application uses a third-party API from [gitfluence.com](https://www.gitfluence.com/) to process natural language prompts and generate Git commands. You can also use this API directly.

**Endpoint:** `https://www.gitfluence.com/api/generate`

**Method:** `POST`

**Body:**
```json
{
    "prompt": "your natural language query"
}
```

**Example with cURL:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"prompt":"delete the last commit"}' https://www.gitfluence.com/api/generate
```

**Disclaimer:** This is a third-party API. Its availability and functionality are not guaranteed by this project.

## How to Run

1.  **Prerequisites:** Ensure you have Python 3 installed.
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Application:**
    ```bash
    python git_chat_gui.py
    ```

## How to Build the Executable

To create a standalone executable from the script, you can use PyInstaller:

1.  **Install PyInstaller:**
    ```bash
    pip install pyinstaller
    ```
2.  **Build the `.exe`:**
    ```bash
    pyinstaller --onefile --windowed --name GitCommandGenerator git_chat_gui.py
    ```
    The executable will be located in the `dist/` directory.