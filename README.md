<div align="center">
  <img src="https://raw.githubusercontent.com/SahilAmirov/project-prompt/refs/heads/main/fav.ico" alt="Project Logo" width="120" height="120">
  <h1 align="center">Project to Prompt</h1>
  <p align="center">
    Quickly generate a clean, consolidated context file from your entire project to get better help from Large Language Models (LLMs) like GPT-4, Gemini, Claude, etc.
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

Struggling to provide complete context to AI models like **GPT-4**, **Gemini**, **Claude**, etc about your codebase? Pasting files one-by-one is tedious, and you often hit token limits or include irrelevant "noise" like `node_modules` or `bin` folders.

**Project Context Scraper** is the solution. This simple GUI tool scans your entire project, intelligently filters out everything you don't need, and generates a single, clean `.txt` file. This file contains your directory structure and all essential source code, perfectly formatted to be used as a prompt.

Just copy, paste, and ask your question. Get better, more accurate help from your AI assistant in seconds.

---

## 🚀 Getting Started

There are two ways to use this application: downloading the ready-to-use version or running from the source code.

### Option 1: Download (Recommended)

1.  Go to the **[Releases Page](https://github.com/SahilAmirov/project-prompt/releases)**.
2.  Download the latest `.zip` file (e.g., `Project.Context.Scraper.v1.0.zip`).
3.  Extract the archive to a folder on your computer.
4.  Double-click `Project Scanner.exe` to run. No installation needed!

### Option 2: Run from Source

If you have Python installed and want to run the script directly:

1.  **Prerequisites:** Ensure you have [Python 3.6+](https://www.python.org/downloads/) on your system.
2.  **Clone the repository:**
    ```sh
    git clone https://github.com/SahilAmirov/project-prompt.git
    ```
3.  **Navigate to the directory:**
    ```sh
    cd project-prompt
    ```
4.  **Run the application:**
    ```sh
    python project_scanner.py
    ```

---

## 📖 Usage

1.  **Launch the app** by running `Project Scanner.exe` or the Python script.
2.  **Select Folder:** Click **"Browse..."** or paste the full path to your project's root directory.
3.  **Generate:** The **"Generate Summary"** button will activate. Click it.
4.  **Wait:** The status bar will show the progress of the scan.
5.  **Choose Action:**
    *   **Save to File:** Saves the complete summary as `[ProjectName]_summary.txt`.
    *   **Copy to Clipboard:** Copies the entire summary text, ready to be pasted.
6.  **Start Over:** Click **"Start Over"** to scan a new project.

---

## ✨ Key Features

*   **Simple GUI:** Lightweight and intuitive user experience.
*   **Intelligent 3-Category Filtering:** Automatically categorizes files to include content, show path only, or ignore completely.
*   **Highly Customizable:** Easily edit the script's `CONFIGURATION` section to add your own rules.
*   **Clean & Comprehensive Output:** Generates a single `.txt` file with project name, a clean directory tree, and all relevant file contents.
*   **Portable Executable:** No installation required for the downloaded version.

---

## 🤝 Contributing

Contributions make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

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
