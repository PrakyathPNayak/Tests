import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import nbtlib
from pathlib import Path

class MinecraftLevelEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Level.dat Editor")
        self.root.geometry("900x700")
        self.root.configure(bg="#f0f0f0")
        
        self.level_file = None
        self.level_data = None
        self.edited_values = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        file_frame = ttk.LabelFrame(main_frame, text="Level File Selection", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(file_frame, textvariable=self.path_var, width=60)
        path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.pack(side=tk.LEFT, padx=5)
        
        load_btn = ttk.Button(file_frame, text="Load", command=self.load_level_data)
        load_btn.pack(side=tk.LEFT, padx=5)
        
        search_frame = ttk.Frame(main_frame, padding="5")
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.filter_tree)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        tab_control = ttk.Notebook(main_frame)
        tab_control.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tree_tab = ttk.Frame(tab_control)
        tab_control.add(tree_tab, text="Tree View")
        
        tree_frame = ttk.Frame(tree_tab)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        
        self.tree = ttk.Treeview(tree_frame, 
                                 columns=("Type", "Value"), 
                                 show="tree headings",
                                 yscrollcommand=tree_scroll_y.set,
                                 xscrollcommand=tree_scroll_x.set)
        
        self.tree.heading("#0", text="Path")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Value", text="Value")
        
        self.tree.column("#0", width=300, minwidth=200)
        self.tree.column("Type", width=100, minwidth=80)
        self.tree.column("Value", width=300, minwidth=200)
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        
        settings_tab = ttk.Frame(tab_control)
        tab_control.add(settings_tab, text="Common Settings")
        
        settings_frame = ttk.LabelFrame(settings_tab, text="World Settings", padding="10")
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        row = 0
        self.setting_vars = {}
        
        # Common settings to be displayed, I may need to change this to a more dynamic way of getting the settings
        # but for now, this is a good start
        common_settings = [
            ("Game Mode", "Data.GameType", "int"),
            ("Allow Cheats", "Data.allowCommands", "bool"),
            ("Difficulty", "Data.Difficulty", "int"),
            ("Hardcore Mode", "Data.hardcore", "bool"),
            ("World Name", "Data.LevelName", "str"),
            ("Seed", "Data.WorldGenSettings.seed", "long"),
            ("Time of Day", "Data.DayTime", "long"),
            ("Weather", "Data.raining", "bool"),
            ("Thunder", "Data.thundering", "bool"),
            ("Spawn X", "Data.SpawnX", "int"),
            ("Spawn Y", "Data.SpawnY", "int"),
            ("Spawn Z", "Data.SpawnZ", "int"),
            ("Game Rules", "Data.GameRules", "compound")
        ]
        
        for label_text, path, data_type in common_settings:
            ttk.Label(settings_frame, text=f"{label_text}:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=3)
            
            var = tk.StringVar()
            self.setting_vars[path] = var
            
            if data_type == "bool":
                widget = ttk.Combobox(settings_frame, textvariable=var, values=["True", "False"], width=20)
            elif data_type == "int":
                if "Difficulty" in path or "GameType" in path:
                    if "Difficulty" in path:
                        widget = ttk.Combobox(settings_frame, textvariable=var, 
                                           values=["0 (Peaceful)", "1 (Easy)", "2 (Normal)", "3 (Hard)"], width=20)
                    else:  
                        widget = ttk.Combobox(settings_frame, textvariable=var, 
                                           values=["0 (Survival)", "1 (Creative)", "2 (Adventure)", "3 (Spectator)"], width=20)
                else:
                    widget = ttk.Entry(settings_frame, textvariable=var, width=20)
            else:
                widget = ttk.Entry(settings_frame, textvariable=var, width=40)
                
            widget.grid(row=row, column=1, sticky=tk.W, padx=5, pady=3)
            row += 1
        
        gamerules_frame = ttk.LabelFrame(settings_tab, text="Game Rules", padding="10")
        gamerules_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.gamerules_vars = {}
        self.gamerules_widgets = {}
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        save_btn = ttk.Button(button_frame, text="Save Changes", command=self.save_changes)
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        reload_btn = ttk.Button(button_frame, text="Reload", command=self.load_level_data)
        reload_btn.pack(side=tk.RIGHT, padx=5)
        
    def browse_file(self):
        initial_dir = None
        # Check for Minecraft directory based on OS, TODO: test on Mac and windows

        # TODO: Let the user choose a default directory for the level.dat file in the settings
        if os.name == 'nt':  # Windows 
            mc_dir = os.path.join(os.getenv('APPDATA'), '.minecraft', 'saves')
            if os.path.exists(mc_dir):
                initial_dir = mc_dir
        else:  # Linux/Mac
            home = os.path.expanduser("~")
            mc_dir_linux = os.path.join(home, '.minecraft', 'saves')
            mc_dir_mac = os.path.join(home, 'Library', 'Application Support', 'minecraft', 'saves')
            
            if os.path.exists(mc_dir_linux):
                initial_dir = mc_dir_linux
            elif os.path.exists(mc_dir_mac):
                initial_dir = mc_dir_mac
                
        filename = filedialog.askdirectory(title="Select Minecraft World Folder", initialdir=initial_dir)
        
        if filename:
            level_path = os.path.join(filename, "level.dat")
            if os.path.exists(level_path):
                self.path_var.set(level_path)
            else:
                messagebox.showerror("Error", f"No level.dat found in {filename}")
    
    def load_level_data(self):
        path = self.path_var.get()
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", "Please select a valid level.dat file")
            return
        
        try:
            self.level_file = nbtlib.load(path)
            self.level_data = self.level_file
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            self.populate_tree("", self.level_data) # just feeds the data file tree data intot the treeview
            
            self.populate_common_settings()
            
            messagebox.showinfo("Success", "Level.dat loaded successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load level.dat: {str(e)}")
    
    def populate_tree(self, parent, nbt_data, path=""):
        if isinstance(nbt_data, dict):
            for key, value in nbt_data.items():
                new_path = f"{path}.{key}" if path else key
                node_id = self.tree.insert(parent, tk.END, text=key, values=("Compound", ""))
                self.populate_tree(node_id, value, new_path)
        elif isinstance(nbt_data, list):
            for i, item in enumerate(nbt_data):
                new_path = f"{path}[{i}]"
                node_id = self.tree.insert(parent, tk.END, text=f"[{i}]", values=("List", ""))
                self.populate_tree(node_id, item, new_path)
        else:
            # It's a primitive value, hence just insert it
            value_type = type(nbt_data).__name__
            self.tree.insert(parent, tk.END, text=path.split(".")[-1], values=(value_type, str(nbt_data)))

    def get_nbt_value(self, path):
        """Get a value from the NBT data using a path string like 'Data.GameType'"""
        parts = path.split(".")
        current = self.level_data
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
                
        return current
    
    def set_nbt_value(self, path, value):
        """Set a value in the NBT data using a path string"""
        parts = path.split(".")
        current = self.level_data
        
        # Navigate to the parent of the target
        for part in parts[:-1]:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False
        
        # Set the value on the parent
        if isinstance(current, dict) and parts[-1] in current:
            # Apparently, the type of the value is stored in the last element of the parts
            target_type = type(current[parts[-1]])
            
            # Convert the value to the correct type, TODO: add more types and test
            # I may be in deep water if this goes wrong
            try:
                if target_type == bool:
                    if value.lower() in ["true", "1", "yes"]:
                        typed_value = True
                    else:
                        typed_value = False
                elif target_type == int:
                    # Handle the case where we have "0 (Survival)" format
                    if " (" in value:
                        typed_value = int(value.split(" ")[0])
                    else:
                        typed_value = int(value)
                elif target_type == float:
                    typed_value = float(value)
                elif target_type == str:
                    typed_value = str(value)
                else:
                    # For complex types, we don't change them through this method
                    # TODO: maybe check out better ways to handle this
                    messagebox.showerror("Type Error", f"Cannot set value of type {target_type.__name__} directly")
                    return False
                
                current[parts[-1]] = typed_value
                return True
            
            except (ValueError, TypeError):
                messagebox.showerror("Type Error", f"Cannot convert '{value}' to {target_type.__name__}")
                return False
        
        return False
    
    def populate_common_settings(self):
        """Populate the common settings tab with values from the NBT data"""
        # Populate regular settings
        for path, var in self.setting_vars.items():
            value = self.get_nbt_value(path)
            
            if value is not None:
                # Format special values
                if path == "Data.GameType":
                    game_modes = ["0 (Survival)", "1 (Creative)", "2 (Adventure)", "3 (Spectator)"]
                    if 0 <= value <= 3:
                        var.set(game_modes[value])
                    else:
                        var.set(str(value))
                elif path == "Data.Difficulty":
                    difficulties = ["0 (Peaceful)", "1 (Easy)", "2 (Normal)", "3 (Hard)"]
                    if 0 <= value <= 3:
                        var.set(difficulties[value])
                    else:
                        var.set(str(value))
                else:
                    var.set(str(value))
        
        gamerules = self.get_nbt_value("Data.GameRules")
        if gamerules:
            for widget in self.gamerules_widgets.values():
                widget.destroy()
            
            self.gamerules_vars = {}
            self.gamerules_widgets = {}
            
            parent_frame = next((w for w in self.root.winfo_children() 
                               if isinstance(w, ttk.Frame) and w.winfo_children() 
                               and "Game Rules" in [c['text'] for c in w.winfo_children() 
                                                if hasattr(c, 'cget') and 'text' in c.keys()]), None)
            
            if parent_frame:
                gamerules_frame = [c for c in parent_frame.winfo_children() 
                                  if hasattr(c, 'cget') and 'text' in c.keys() and c['text'] == "Game Rules"][0]
                
                row, col = 0, 0
                for key, value in sorted(gamerules.items()):
                    var = tk.StringVar(value=str(value))
                    self.gamerules_vars[key] = var
                    
                    label = ttk.Label(gamerules_frame, text=key)
                    label.grid(row=row, column=col*2, sticky=tk.W, padx=5, pady=3)
                    
                    if value.lower() in ['true', 'false']:
                        widget = ttk.Combobox(gamerules_frame, textvariable=var, values=["true", "false"], width=10)
                    else:
                        widget = ttk.Entry(gamerules_frame, textvariable=var, width=10)
                    
                    widget.grid(row=row, column=col*2+1, sticky=tk.W, padx=5, pady=3)
                    
                    self.gamerules_widgets[key] = widget
                    
                    # Arrange in 2 columns TODO: this feels like it could be improved
                    col += 1
                    if col >= 2:
                        col = 0
                        row += 1
    
    def on_tree_double_click(self, event):
        """Handle double-clicking on a tree item"""
        item = self.tree.selection()[0]
        item_path = self.get_tree_path(item)
        item_type = self.tree.item(item)["values"][0]
        
        if item_type not in ["Compound", "List"]:
            current_value = self.tree.item(item)["values"][1]
            new_value = tk.simpledialog.askstring("Edit Value", f"Edit value for {item_path}", initialvalue=current_value)
            
            if new_value is not None:
                self.tree.item(item, values=(item_type, new_value))
                
                # Store the edited value for saving later
                self.edited_values[item_path] = new_value
    
    def get_tree_path(self, item):
        """Get the full path of a tree item"""
        path_parts = []
        
        while item:
            text = self.tree.item(item)["text"]
            if text:
                path_parts.insert(0, text)
            item = self.tree.parent(item)
        
        return ".".join(path_parts)
    
    def filter_tree(self, *args):
        """Filter the tree view based on search text"""
        search_text = self.search_var.get().lower()
        
        # First, show all items
        self._show_all_tree_items()
        
        if search_text:
            # Then hide non-matching items, seems a bit backwards but it works
            self._filter_tree_item("", search_text)
    
    def _show_all_tree_items(self):
        """Show all items in the tree"""
        def _show_children(item):
            children = self.tree.get_children(item)
            for child in children:
                self.tree.item(child, open=True)
                _show_children(child)
        
        _show_children("")
    
    def _filter_tree_item(self, item, search_text):
        """Recursively filter tree items"""
        # Process all children first
        children = self.tree.get_children(item)
        visible_children = False
        
        for child in children:
            # If any child is visible, this item should be visible too
            if self._filter_tree_item(child, search_text):
                visible_children = True
        
        # If this is the root, we're done
        if item == "":
            return True
        
        # Check if this item matches the search
        item_text = self.tree.item(item)["text"].lower()
        item_value = str(self.tree.item(item)["values"][1]).lower()
        
        matches = search_text in item_text or search_text in item_value
        
        # Show this item if it matches or has visible children
        if matches or visible_children:
            return True
        else:
            self.tree.detach(item)  # Hide this item
            return False
    
    def save_changes(self):
        """Save changes back to the level.dat file"""
        if not self.level_file:
            messagebox.showerror("Error", "No level.dat file loaded")
            return
        
        # Apply changes from settings tab
        for path, var in self.setting_vars.items():
            value = var.get()
            if value:
                self.set_nbt_value(path, value)
        
        # Apply changes from game rules
        gamerules = self.get_nbt_value("Data.GameRules")
        if gamerules:
            for key, var in self.gamerules_vars.items():
                gamerules[key] = var.get()
        
        # Apply changes from tree view edits
        for path, value in self.edited_values.items():
            self.set_nbt_value(path, value)
        
        # Backup the original file, was told this was good practice. Credits: Nikhil R.
        path = self.path_var.get()
        backup_path = f"{path}.backup"
        
        if not os.path.exists(backup_path):
            import shutil
            shutil.copy2(path, backup_path)
        
        try:
            self.level_file.save()
            messagebox.showinfo("Success", f"Changes saved. Backup created at {backup_path}")
            
            # Clear edited values
            self.edited_values = {}
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save changes: {str(e)}")


if __name__ == "__main__":
    # Check if nbtlib is installed, remove later
    try:
        import nbtlib
    except ImportError:
        print("The nbtlib package is required. Installing...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "nbtlib"])
        
        # Not sure if this is the best way to do this, but it works for now
        import nbtlib
    
    root = tk.Tk()
    app = MinecraftLevelEditor(root)
    root.mainloop()
