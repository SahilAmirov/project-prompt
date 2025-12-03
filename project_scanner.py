import os
import sys
import json
import tkinter as tk
from tkinter import filedialog, messagebox

# --- CONSTANTS & DEFAULTS ---
SETTINGS_FILENAME = "settings.json"

# Default configuration serves as a fallback and strictly mimics the JSON structure
DEFAULT_CONFIG = {
    "ignore_dirs": [
        ".git", ".idea", ".vscode", "venv", "env", "node_modules", 
        "__pycache__", "bin", "obj", "build", "dist", "target", ".vs"
    ],
    "ignore_filenames": [
        ".gitignore", ".gitattributes", "package-lock.json", "yarn.lock"
    ],
    "ignore_extensions": [
        ".dll", ".exe", ".pdb", ".db", ".log", ".tmp", ".zip", ".rar", 
        ".pyc", ".class", ".o", ".so", ".a", ".lib", 
        ".png", ".jpg", ".jpeg", ".gif", ".ico", ".mp4"
    ],
    "ignore_patterns": [
        ".min.js", ".min.css", ".Designer.cs", ".g.cs"
    ],
    "path_only_extensions": [
        ".sln", ".svg", ".lock"
    ],
    "path_only_filenames": [
        "LICENSE", "README.md"
    ]
}

# --- CONFIGURATION MANAGER ---

class ConfigManager:
    """Handles loading and saving of the scanning rules."""
    
    def __init__(self):
        self.config = DEFAULT_CONFIG
        self.load_settings()

    def load_settings(self):
        """Loads settings from JSON file or creates it if missing."""
        if not os.path.exists(SETTINGS_FILENAME):
            self._create_default_settings()
        else:
            try:
                with open(SETTINGS_FILENAME, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge loaded config with defaults to ensure all keys exist
                    for key in DEFAULT_CONFIG:
                        if key not in loaded_config:
                            loaded_config[key] = DEFAULT_CONFIG[key]
                    self.config = loaded_config
            except Exception as e:
                print(f"Error loading settings.json: {e}. Using defaults.")
                self.config = DEFAULT_CONFIG

    def _create_default_settings(self):
        """Creates the settings.json file with default values."""
        try:
            with open(SETTINGS_FILENAME, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_CONFIG, f, indent=2)
        except Exception as e:
            print(f"Could not create default settings file: {e}")

    # Helper methods to access sets for O(1) lookups
    @property
    def ignore_dirs(self): return set(self.config.get('ignore_dirs', []))
    @property
    def ignore_files(self): return set(self.config.get('ignore_filenames', []))
    @property
    def ignore_exts(self): return set(self.config.get('ignore_extensions', []))
    @property
    def ignore_patterns(self): return set(self.config.get('ignore_patterns', []))
    @property
    def path_only_exts(self): return set(self.config.get('path_only_extensions', []))
    @property
    def path_only_files(self): return set(self.config.get('path_only_filenames', []))


# Initialize Config globally
files_config = ConfigManager()


# --- CORE LOGIC ---

def get_file_category(relative_path):
    """
    Determines the category of a file or directory.
    Returns:
        3: Ignore Completely
        2: Path Only (Tree view only)
        1: Content (Tree + File Content)
    """
    normalized_path = os.path.normpath(relative_path)
    filename = os.path.basename(normalized_path)
    
    # 1. Check Directories (Highest Priority)
    # Check if any part of the path is in the ignore list
    path_parts = normalized_path.split(os.sep)
    
    # Skip hidden folders (starting with .) except current dir '.'
    for part in path_parts:
        if part.startswith('.') and part != '.' and len(part) > 1:
            # Exception: we might want some .config folders, but usually hidden folders are config/cache
            # For strictness, if it's in the explicit ignore list, it's gone.
            pass 

    # Check explicit directory ignores
    for part in path_parts:
        if part in files_config.ignore_dirs:
            return 3

    # 2. Check Filenames
    if filename in files_config.ignore_files:
        return 3

    # 3. Check Extensions
    _, ext = os.path.splitext(filename)
    ext = ext.lower()
    
    if ext in files_config.ignore_exts:
        return 3

    # 4. Check Patterns (Substring matching)
    for pattern in files_config.ignore_patterns:
        if pattern.lower() in filename.lower():
            return 3

    # 5. Check Category 2 (Path Only)
    if ext in files_config.path_only_exts:
        return 2
    if filename in files_config.path_only_files:
        return 2
        
    # Default to Category 1 (Include Content)
    return 1

def create_directory_tree(start_path):
    """Generates the visual directory tree string."""
    tree_lines = []
    
    for root, dirs, files in os.walk(start_path, topdown=True):
        relative_root = os.path.relpath(root, start=start_path)
        if relative_root == ".": relative_root = ""
        
        # Check if the current directory is excluded
        if relative_root and get_file_category(relative_root) == 3:
            dirs[:] = [] # Stop descending
            continue

        # Filter subdirectories in-place so os.walk doesn't visit them
        dirs[:] = [d for d in dirs if get_file_category(os.path.join(relative_root, d)) != 3]
        
        level = relative_root.count(os.sep) if relative_root else 0
        indent = ' ' * 4 * level
        
        if relative_root:
            tree_lines.append(f"{indent}├── {os.path.basename(root)}/")
        
        sub_indent = ' ' * 4 * (level + 1)
        
        # Filter and sort files
        valid_files = []
        for f in files:
            cat = get_file_category(os.path.join(relative_root, f))
            if cat != 3:
                valid_files.append(f)
        
        for f in sorted(valid_files):
            tree_lines.append(f"{sub_indent}├── {f}")
            
    return "\n".join(tree_lines)

def is_binary_file(file_path):
    """Heuristic to check if a file is binary."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\x00' in chunk
    except Exception:
        return True

def generate_project_summary(project_path, status_callback):
    """Main function to scan project and generate string output."""
    all_contents = []
    
    # Reload config just in case user edited it while app was open
    files_config.load_settings()
    
    status_callback("Generating directory structure...")
    try:
        tree = create_directory_tree(project_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to scan directory: {e}")
        return None

    status_callback("Reading file contents...")
    
    file_count = 0
    
    for root, dirs, files in os.walk(project_path, topdown=True):
        relative_root = os.path.relpath(root, start=project_path)
        if relative_root == ".": relative_root = ""
        
        # Skip excluded directories
        if relative_root and get_file_category(relative_root) == 3:
            dirs[:] = []
            continue

        # Filter subdirectories
        dirs[:] = [d for d in dirs if get_file_category(os.path.join(relative_root, d)) != 3]

        for file in sorted(files):
            relative_path = os.path.join(relative_root, file)
            category = get_file_category(relative_path)

            if category != 1: 
                continue # Skip Ignore (3) and Path Only (2) for content reading

            file_path = os.path.join(root, file)
            file_count += 1
            status_callback(f"Reading: {file}")
            
            header = f"--- FILE: {relative_path.replace(os.sep, '/')} ---\n"
            
            content = ""
            if is_binary_file(file_path):
                content = "[Binary File - Content Skipped]"
            else:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        # Simple check for very large files to prevent freezing
                        if len(content) > 500000: 
                            content = f"[File too large ({len(content)} chars) - Truncated]\n" + content[:5000] + "\n...[Truncated]..."
                except Exception as e:
                    content = f"[Error reading file: {e}]"
            
            all_contents.append(f"{header}\n{content}\n")
            
    status_callback("Finalizing output...")
    
    project_name = os.path.basename(project_path.rstrip(os.sep))
    
    output = []
    output.append(f"PROJECT NAME: {project_name}")
    output.append("=" * 80)
    output.append("DIRECTORY STRUCTURE:")
    output.append("-" * 80)
    output.append(f"{project_name}/")
    output.append(tree)
    output.append("\n" + "=" * 80)
    output.append("FILE CONTENTS:")
    output.append("-" * 80)
    output.append("\n".join(all_contents))
    
    return "\n".join(output)

# --- GUI CLASS ---

class ProjectScannerApp:
    def __init__(self, master):
        self.master = master
        master.title("Project to Prompt (JSON Config)")
        master.geometry("600x350")
        
        # Styles / Fonts
        self.font_bold = ('Segoe UI', 10, 'bold')
        self.font_norm = ('Segoe UI', 9)

        # Variables
        self.project_path = tk.StringVar()
        self.summary_text = None
        self.output_path = None

        # UI Layout
        self.build_ui()
        
        # Initial check
        self.validate_path_entry()

    def build_ui(self):
        # Input Frame
        input_frame = tk.LabelFrame(self.master, text="Project Source", padx=10, pady=10)
        input_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(input_frame, text="Select root folder:", font=self.font_norm).pack(anchor=tk.W)
        
        entry_frame = tk.Frame(input_frame)
        entry_frame.pack(fill=tk.X, pady=5)
        
        self.path_entry = tk.Entry(entry_frame, textvariable=self.project_path, width=60)
        self.path_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        self.path_entry.bind("<KeyRelease>", self.validate_path_entry)
        
        self.browse_button = tk.Button(entry_frame, text="Browse...", command=self.select_folder)
        self.browse_button.pack(side=tk.RIGHT)

        # Config Info
        lbl_config = tk.Label(input_frame, text=f"Config: Loaded from {SETTINGS_FILENAME}", fg="gray", font=("Segoe UI", 8))
        lbl_config.pack(anchor=tk.W)

        # Action Frame
        self.action_frame = tk.Frame(self.master)
        self.action_frame.pack(pady=10)
        
        self.start_button = tk.Button(self.action_frame, text="GENERATE CONTEXT", 
                                      command=self.process_project, 
                                      font=self.font_bold, bg="#e1e1e1", state='disabled')
        self.start_button.pack(pady=5, ipadx=10, ipady=5)

        # Post-Action Buttons (Hidden initially)
        self.post_action_frame = tk.Frame(self.master)
        
        self.save_button = tk.Button(self.post_action_frame, text="Save .txt", command=self.save_to_file, width=15)
        self.copy_button = tk.Button(self.post_action_frame, text="Copy to Clipboard", command=self.copy_to_clipboard, width=15)
        self.reset_button = tk.Button(self.post_action_frame, text="Scan Another", command=self.reset_ui, width=15)
        
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.copy_button.pack(side=tk.LEFT, padx=5)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready.")
        self.status_bar = tk.Label(self.master, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def select_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.project_path.set(path)
            self.validate_path_entry()

    def validate_path_entry(self, event=None):
        path = self.project_path.get()
        if path and os.path.isdir(path):
            self.start_button.config(state='normal', bg="#4CAF50", fg="white")
            self.status_var.set("Valid path selected.")
        else:
            self.start_button.config(state='disabled', bg="#e1e1e1", fg="black")
            self.status_var.set("Please select a valid directory.")

    def process_project(self):
        path = self.project_path.get()
        if not path or not os.path.isdir(path): return
        
        # UI State: Busy
        self.path_entry.config(state='disabled')
        self.browse_button.config(state='disabled')
        self.start_button.pack_forget()
        self.master.update()

        # Run Scan
        self.summary_text = generate_project_summary(path, self.update_status)

        if self.summary_text:
            self.show_results()
        else:
            self.reset_ui()

    def update_status(self, msg):
        self.status_var.set(msg)
        self.master.update()

    def show_results(self):
        stats = f"{len(self.summary_text.splitlines())} lines, {len(self.summary_text)} chars"
        self.status_var.set(f"Done! {stats}")
        self.post_action_frame.pack(pady=10)

    def save_to_file(self):
        if not self.summary_text: return
        project_name = os.path.basename(self.project_path.get().rstrip(os.sep))
        default_name = f"{project_name}_prompt_context.txt"
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.summary_text)
                messagebox.showinfo("Success", f"Saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def copy_to_clipboard(self):
        if not self.summary_text: return
        self.master.clipboard_clear()
        self.master.clipboard_append(self.summary_text)
        messagebox.showinfo("Copied", "Content copied to clipboard!")

    def reset_ui(self):
        self.summary_text = None
        self.post_action_frame.pack_forget()
        self.path_entry.config(state='normal')
        self.browse_button.config(state='normal')
        self.project_path.set("")
        self.start_button.pack(pady=5, ipadx=10, ipady=5)
        self.validate_path_entry()

def resource_path(relative_path):
    """ PyInstaller ile paketlenince dosya yolunu bulmak için gerekli fonksiyon """
    try:
        # PyInstaller temp klasörü yaratır ve yolu _MEIPASS içine atar
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    root = tk.Tk()
    
    # İkon dosyasının yolunu güvenli şekilde al
    icon_file = resource_path("fav.ico")
    
    # Eğer dosya varsa ikonu ayarla
    if os.path.exists(icon_file):
        try:
            root.iconbitmap(icon_file)
        except Exception:
            pass # İkon yüklenemezse program çökmesin, devam etsin

    app = ProjectScannerApp(root)
    root.mainloop()