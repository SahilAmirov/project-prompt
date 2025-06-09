import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage

# --- CONFIGURATION (Final) ---

# CATEGORY 3: IGNORE COMPLETELY (Neither in tree nor in content)
# ===============================================================
CAT3_IGNORE_DIRS = {
    '.git', '.idea', 'venv', 'env', '.env', 'node_modules', '__pycache__',
    '.github', '.vs', 'bin', 'obj', 'Properties',
}
CAT3_IGNORE_FILENAMES = {
    '.gitignore', '.gitattributes', 'libman.json',
}
CAT3_IGNORE_EXTENSIONS = {
    '.dll', '.exe', '.pdb', '.cache', '.suo', '.user', '.sln.dotsettings',
    '.log', '.tmp', '.bak', '.zip', '.rar', '.7z', '.gz', '.br', '.vsidx',
    '.pyc', '.pyd', '.o', '.so', '.a', '.lib', '.class', '.bin', '.map',
    '.db-shm', '.db-wal',
}
CAT3_IGNORE_PATTERNS = {
    '.min.js', '.min.css',
    '.Designer.cs', '.g.cs', '.g.props', '.g.targets', '.resources.dll',
    'ModelSnapshot.cs', '.csproj.user', 'project.assets.json',
    'project.nuget.cache', 'launchSettings.json',
}
CAT3_IGNORE_PATHS = {
    os.path.join('wwwroot', 'lib'),
    os.path.join('wwwroot', 'vendor'),
}

# CATEGORY 2: PATH ONLY (Show in tree, but skip content)
# ===============================================================
CAT2_PATH_ONLY_EXTENSIONS = {
    '.sln', '.db', '.sqlite', '.sqlite3', '.svg', '.ico', '.png', '.jpg',
    'LICENSE', 'LICENSE.txt' # Common license files
}

# --- CORE LOGIC (Completely Revised) ---

def get_file_category(relative_path):
    """Determines the category of a file or directory based on the rules."""
    normalized_path = os.path.normpath(relative_path)
    filename = os.path.basename(normalized_path)
    
    # HACK FIX for wwwroot/lib exclusion
    if 'wwwroot' in normalized_path and 'lib' in normalized_path.split(os.sep):
        return 3
    
    # Category 3 (Ignore Completely) has the highest priority
    if normalized_path in CAT3_IGNORE_PATHS: return 3
    for excluded_path in CAT3_IGNORE_PATHS:
        if normalized_path.startswith(excluded_path + os.sep):
            return 3

    # Skip any hidden folders (e.g., .templates, .git)
    for part in normalized_path.split(os.sep):
        if part.startswith('.') and part != '.':
            return 3
            
    for dir_part in normalized_path.split(os.sep):
        if dir_part in CAT3_IGNORE_DIRS:
            return 3

    if filename in CAT3_IGNORE_FILENAMES: return 3
            
    _ , ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext in CAT3_IGNORE_EXTENSIONS: return 3
    for pattern in CAT3_IGNORE_PATTERNS:
        if filename.endswith(pattern):
            return 3

    # Category 2 (Path Only)
    if ext in CAT2_PATH_ONLY_EXTENSIONS: return 2
    if filename in CAT2_PATH_ONLY_EXTENSIONS: return 2
    
    return 1 # Category 1 (Path & Content)

def create_directory_tree(start_path):
    """Creates a clean string representation of the project's directory tree."""
    tree_lines = []
    for root, dirs, files in os.walk(start_path, topdown=True):
        relative_root = os.path.relpath(root, start=start_path)
        if relative_root == ".": relative_root = ""
        
        # **THE CRITICAL FIX**: If the current directory path itself is excluded,
        # tell os.walk to not go into its subdirectories and skip the rest of the loop.
        if get_file_category(relative_root) == 3:
            dirs[:] = []
            continue

        # Filter subdirectories before os.walk visits them
        dirs[:] = [d for d in dirs if get_file_category(os.path.join(relative_root, d)) != 3]
        
        level = relative_root.count(os.sep) if relative_root else 0
        indent = ' ' * 4 * level
        if relative_root:
            tree_lines.append(f"{indent}├── {os.path.basename(root)}/")
        
        sub_indent = ' ' * 4 * (level + 1)
        filtered_files = sorted([f for f in files if get_file_category(os.path.join(relative_root, f)) != 3])
        for f in filtered_files:
            tree_lines.append(f"{sub_indent}├── {f}")
            
    return "\n".join(tree_lines)

def generate_project_summary(project_path, status_update_callback):
    """Scans the project using the 3-category system and returns a summary string."""
    all_contents = []
    
    status_update_callback("Generating clean directory structure...")
    try:
        tree = create_directory_tree(project_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create directory tree: {e}")
        return None

    status_update_callback("Scanning files and reading relevant content...")
    
    file_count = 0
    for root, dirs, files in os.walk(project_path, topdown=True):
        relative_root = os.path.relpath(root, start=project_path)
        if relative_root == ".": relative_root = ""
        
        # **THE CRITICAL FIX**: Also applied here to prevent processing files
        # in an excluded directory path.
        if get_file_category(relative_root) == 3:
            dirs[:] = []
            continue

        # Filter subdirectories before os.walk visits them
        dirs[:] = [d for d in dirs if get_file_category(os.path.join(relative_root, d)) != 3]

        for file in sorted(files):
            relative_path = os.path.join(relative_root, file)
            category = get_file_category(relative_path)

            if category == 3: continue

            file_count += 1
            status_update_callback(f"Processing file {file_count}: {relative_path.replace(os.sep, '/')}")
            
            if category == 1:
                file_path = os.path.join(root, file)
                content_header = f"--- FILE: {relative_path.replace(os.sep, '/')} ---\n\n"
                file_content = ""
                try:
                    with open(file_path, 'rb') as f_check:
                        chunk = f_check.read(1024)
                        if b'\x00' in chunk:
                            file_content = "!!! SKIPPED: File appears to be binary. !!!"
                        else:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                file_content = f.read()
                except Exception as e:
                    file_content = f"!!! ERROR: Could not read file. Reason: {e} !!!"
                all_contents.append(content_header + file_content)
            
    status_update_callback("Finalizing summary...")
    
    project_name = os.path.basename(project_path.rstrip('/\\'))
    final_output = f"PROJECT NAME: {project_name}\n"
    final_output += "=" * 80 + "\n\n"
    final_output += "DIRECTORY STRUCTURE:\n"
    final_output += "-" * 80 + "\n"
    final_output += f"{project_name}/\n{tree}\n"
    final_output += "\n" + "=" * 80 + "\n\n"
    final_output += "FILE CONTENTS:\n"
    final_output += "-" * 80 + "\n\n"
    final_output += "\n\n".join(all_contents)
    
    return final_output

# --- GUI CLASS (No changes needed) ---
class ProjectScannerApp:
    def __init__(self, master):
        self.master = master
        master.title("Project Scanner (by SahilAmirov)")
        master.geometry("550x300")
        self.project_path = tk.StringVar()
        self.summary_text = None
        self.output_path = None
        input_frame = tk.Frame(master)
        input_frame.pack(pady=10, padx=10, fill=tk.X)
        self.label = tk.Label(input_frame, text="Select or paste the project folder path:")
        self.label.pack(anchor=tk.W)
        self.path_entry = tk.Entry(input_frame, textvariable=self.project_path, width=70)
        self.path_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=2)
        self.path_entry.bind("<KeyRelease>", self.validate_path_entry)
        self.browse_button = tk.Button(input_frame, text="Browse...", command=self.select_folder)
        self.browse_button.pack(side=tk.RIGHT, padx=(5, 0))
        self.action_frame = tk.Frame(master)
        self.action_frame.pack(pady=20)
        self.start_button = tk.Button(self.action_frame, text="Generate Summary", command=self.process_project, state='disabled', font=('Helvetica', 10, 'bold'))
        self.start_button.pack()
        self.save_button = tk.Button(self.action_frame, text="Save to File", command=self.save_summary_to_file)
        self.copy_button = tk.Button(self.action_frame, text="Copy to Clipboard", command=self.copy_summary_to_clipboard)
        self.reset_button = tk.Button(master, text="Start Over", command=self.reset_ui)
        self.status_label = tk.Label(master, text="Ready. Using final filtering logic.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def select_folder(self):
        folder_selected = filedialog.askdirectory(initialdir=os.getcwd())
        if folder_selected:
            self.project_path.set(folder_selected)
            self.validate_path_entry()

    def validate_path_entry(self, event=None):
        path = self.project_path.get()
        if path and os.path.isdir(path):
            self.start_button.config(state='normal')
            self.status_label.config(text=f"Valid path: {path}")
        else:
            self.start_button.config(state='disabled')
            self.status_label.config(text="Please enter a valid directory path.")

    def process_project(self):
        path = self.project_path.get()
        if not path or not os.path.isdir(path):
            messagebox.showwarning("Invalid Path", "Please select a valid directory.")
            return
        self.toggle_controls(active=False)
        self.master.update()
        try:
            self.summary_text = generate_project_summary(path, self.update_status)
            if self.summary_text:
                self.setup_post_generation_ui(path)
                self.update_status(f"Summary generated successfully. {self.summary_stats} Choose an action.")
            else:
                self.reset_ui()
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
            self.reset_ui()

    def setup_post_generation_ui(self, project_path):
        self.start_button.pack_forget()
        self.browse_button.config(state='disabled')
        self.path_entry.config(state='readonly')
        self.save_button.pack(side=tk.LEFT, padx=5)
        self.copy_button.pack(side=tk.LEFT, padx=5)
        self.reset_button.pack(side=tk.BOTTOM, pady=10)
        project_name = os.path.basename(project_path.rstrip('/\\'))
        output_filename = f"{project_name}_summary.txt"
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
            output_dir = os.path.join(base_dir, 'project-prompts')
            os.makedirs(output_dir, exist_ok=True)
        else:
            try:
                # __file__ is not defined in all contexts (e.g. some interactive interpreters)
                script_path = os.path.abspath(__file__)
                output_dir = os.path.dirname(script_path)
            except NameError:
                 output_dir = os.getcwd() # Fallback to current working directory
        self.output_path = os.path.join(output_dir, output_filename)
        self.summary_stats = f"({len(self.summary_text.splitlines())} lines, {len(self.summary_text)} chars)"


    def save_summary_to_file(self):
        if not self.summary_text or not self.output_path:
            messagebox.showerror("Error", "No summary content to save.")
            return
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                f.write(self.summary_text)
            messagebox.showinfo("Success", f"Project summary saved!\n\nLocation:\n{self.output_path}")
            self.update_status(f"Project summary saved! {self.summary_stats}")

        except Exception as e:
            messagebox.showerror("Save Error", f"Could not write to file: {e}")

    def copy_summary_to_clipboard(self):
        if not self.summary_text:
            messagebox.showerror("Error", "No summary content to copy.")
            return
        self.master.clipboard_clear()
        self.master.clipboard_append(self.summary_text)
        self.update_status(f"Summary copied to clipboard! {self.summary_stats}")
        messagebox.showinfo("Copied!", "The project summary has been copied to your clipboard.")

    def reset_ui(self):
        self.summary_text = None
        self.summary_stats = ""
        self.output_path = None
        self.project_path.set("")
        self.toggle_controls(active=True)
        self.start_button.config(state='disabled')
        self.save_button.pack_forget()
        self.copy_button.pack_forget()
        self.reset_button.pack_forget()
        self.start_button.pack()
        self.update_status("Ready. Using final filtering logic.")

    def toggle_controls(self, active):
        state = 'normal' if active else 'disabled'
        self.path_entry.config(state='normal' if active else 'readonly')
        self.browse_button.config(state=state)
        self.start_button.config(state=state if self.project_path.get() else 'disabled')
        if not active:
             self.start_button.config(state='disabled')

    def update_status(self, message):
        self.status_label.config(text=message)
        self.master.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    icon_path = os.path.join(base_path, 'fav.ico')
    root.iconbitmap(icon_path)

    app = ProjectScannerApp(root)
    root.mainloop()