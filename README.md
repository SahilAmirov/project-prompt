<div align="center">
  <img src="https://raw.githubusercontent.com/SahilAmirov/project-prompt/refs/heads/main/fav.ico" alt="Project Logo" width="120" height="120">
  <h1 align="center">Project Context Scraper</h1>
  <p align="center">
    Quickly generate a clean, consolidated context file from your entire project to get better help from Large Language Models (LLMs) like GPT-4 and Claude.
    <br />
    <br />
    <a href="https://github.com/SahilAmirov/project-prompt/issues">Report a Bug</a>
    ·
    <a href="https://github.com/SahilAmirov/project-prompt/issues">Request a Feature</a>
  </p>

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.6+-blue.svg" alt="Python Version">
    <a href="https://github.com/SahilAmirov/project-prompt/blob/main/LICENSE.txt"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
    <a href="https://github.com/SahilAmirov/project-prompt/stargazers"><img src="https://img.shields.io/github/stars/SahilAmirov/project-prompt" alt="GitHub Stars"></a>
  </p>
</div>

---

## 📋 About The Project

Struggling to provide complete context to AI models like **GPT-4** or **Claude** about your codebase? Pasting files one-by-one is tedious, and you often hit token limits or include irrelevant "noise" like `node_modules` or `bin` folders.

**Project Context Scraper** is the solution. This simple GUI tool scans your entire project, intelligently filters out everything you don't need, and generates a single, clean `.txt` file. This file contains your directory structure and all essential source code, perfectly formatted to be used as a prompt.

Just copy, paste, and ask your question. Get better, more accurate help from your AI assistant in seconds.

### ✨ Key Features

*   **Simple & Intuitive GUI:** Built with Python's native `tkinter` library for a lightweight experience.
*   **Intelligent 3-Category Filtering:** Automatically categorizes files to:
    1.  **Include Full Content:** Essential source code (`.cs`, `.py`, `.js`, `.html`, etc.).
    2.  **Show Path Only:** Files where location matters but content doesn't (`.db`, `.sln`, `.png`).
    3.  **Ignore Completely:** Useless "noise" like `bin/`, `obj/`, `.git/`, and library folders.
*   **Highly Customizable:** Easily edit the `CONFIGURATION` section in the script to add your own rules.
*   **Clean & Comprehensive Output:** Generates a single `.txt` file with the project name, a clean directory tree, and all relevant file contents, clearly separated.
*   **One-Click Actions:** After generating, instantly **Save to File** or **Copy to Clipboard**.
*   **Standalone Executable:** Build a single `.exe` file with PyInstaller to run anywhere on Windows, no Python installation required.

---

## 🚀 Getting Started

Follow these simple steps to get the application running.

### Prerequisites

You need Python 3.6 or higher installed on your system.
*   [Download Python](https://www.python.org/downloads/)

### Installation & Running

1.  Clone the repository:
    ```sh
    git clone https://github.com/SahilAmirov/project-prompt.git
    ```
2.  Navigate to the project directory:
    ```sh
    cd project-prompt
    ```
3.  Run the application:
    ```sh
    python project_scanner.py
    ```

---

## 🛠️ Building the Executable (Optional)

Create a standalone `.exe` file that can be run on any Windows machine.

1.  Install PyInstaller:
    ```sh
    pip install pyinstaller
    ```
2.  Run the build command from the project directory (make sure `fav.ico` is present):
    ```bash
    pyinstaller --onefile --windowed --icon="fav.ico" --add-data "fav.ico;." project_scanner.py
    ```
    *   `--onefile`: Bundles everything into a single executable.
    *   `--windowed`: Prevents the console window from appearing on run.
    *   `--icon="fav.ico"`: Sets the icon for the `.exe` file itself.
    *   `--add-data "fav.ico;."`: **Crucially**, this embeds the icon file inside the `.exe` so the application window can use it at runtime.

3.  Your `project_scanner.exe` will be in the new `dist` folder.

---

## 📖 Usage

1.  **Launch the App:** Run `project_scanner.py` or the built `project_scanner.exe`.
2.  **Select Folder:** Click **"Browse..."** or paste the full path to your project's root directory.
3.  **Generate:** The **"Generate Summary"** button will activate. Click it.
4.  **Wait:** The status bar will show the progress of the scan.
5.  **Choose Action:**
    *   **Save to File:** Saves the summary as `[ProjectName]_summary.txt`. If run from the `.exe`, it will be inside a `project-prompts` folder.
    *   **Copy to Clipboard:** Copies the entire summary text, ready to be pasted.
6.  **Start Over:** Click **"Start Over"** to scan a new project.

---

## ⚙️ Customization

The core strength of this tool is its filter lists. You can easily customize them by editing the `CONFIGURATION` block at the top of `project_scanner.py`:

*   **`CAT3_...` lists:** Add any directory, file, extension, or pattern you want to **completely ignore**.
*   **`CAT2_...` lists:** Add file types where the **path is important** but the content is not.
*   Everything else is automatically treated as **Category 1** (full content included).

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE.txt` for more information.

---

## 📧 Contact

Sahil Amirov - [@SahilAmirov](https://github.com/SahilAmirov)

Project Link: [https://github.com/SahilAmirov/project-prompt](https://github.com/SahilAmirov/project-prompt)
