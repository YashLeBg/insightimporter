import json
from pymongo import MongoClient
import tkinter as tk
from tkinter import Tk, filedialog, messagebox, ttk

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connexion MongoDB")
        self.root.geometry("600x400")
        
        # Variables pour stocker les informations de connexion
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.cluster = tk.StringVar(value="insight.gnhnexe.mongodb.net")
        self.database = tk.StringVar(value="insight")
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Connexion à MongoDB Atlas", font=('Helvetica', 14, 'bold'))
        title_label.pack(pady=(0, 20))
        
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X)
        
        ttk.Label(form_frame, text="Nom d'utilisateur:").pack(anchor=tk.W)
        ttk.Entry(form_frame, textvariable=self.username, width=40).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Mot de passe:").pack(anchor=tk.W)
        ttk.Entry(form_frame, textvariable=self.password, show="*", width=40).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Cluster MongoDB:").pack(anchor=tk.W)
        ttk.Entry(form_frame, textvariable=self.cluster, width=40).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(form_frame, text="Base de données:").pack(anchor=tk.W)
        ttk.Entry(form_frame, textvariable=self.database, width=40).pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(main_frame, text="Se connecter", command=self.connect).pack(pady=20)
        
    def connect(self):
        username = self.username.get()
        password = self.password.get()
        cluster = self.cluster.get()
        database = self.database.get()
        
        if not all([username, password, cluster, database]):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return
            
        uri = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority"
        
        try:
            client = MongoClient(uri)
            db = client[database]
            db.list_collection_names()
            
            self.root.destroy()
            app = App(uri, database)
            app.root.mainloop()
            
        except Exception as e:
            messagebox.showerror("Erreur de connexion", f"Impossible de se connecter à MongoDB:\n{str(e)}")

class App:
    def __init__(self, uri, database):
        self.root = tk.Tk()
        self.root.title("Importation modeles InsightMaker vers MongoDB")
        self.root.geometry("600x400")
        
        self.client = MongoClient(uri)
        self.db = self.client[database]
        self.models_collection = self.db["models"]
        self.elements_collection = self.db["elements"]
    
        self.selected_files = []
        
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(main_frame, text="Sélectionner des fichiers...", command=self.select_files).pack(pady=5)
        
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.files_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.files_listbox.yview)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Supprimer sélection", command=self.remove_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Tout supprimer", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Importer", command=self.validate).pack(side=tk.RIGHT, padx=5)
        
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Choisir des fichiers JSON",
            filetypes=[("Fichiers JSON", "*.json")]
        )
        if files:
            for file in files:
                if file not in self.selected_files:
                    self.selected_files.append(file)
                    self.files_listbox.insert(tk.END, file)
    
    def remove_selected(self):
        selection = self.files_listbox.curselection()
        for index in reversed(selection):
            self.files_listbox.delete(index)
            self.selected_files.pop(index)
    
    def clear_all(self):
        self.files_listbox.delete(0, tk.END)
        self.selected_files.clear()
    
    def validate(self):
        if not self.selected_files:
            messagebox.showwarning("Aucun fichier", "Veuillez sélectionner au moins un fichier JSON.")
            return
        
        total_files = len(self.selected_files)
        processed_files = 0
        errors = []
        
        for file_path in self.selected_files:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                
                model_data = {
                    "name": data.get("name"),
                    "engine": data.get("engine"),
                    "algorithm": data["simulation"].get("algorithm"),
                    "time_start": data["simulation"].get("time_start"),
                    "time_length": data["simulation"].get("time_length"),
                    "time_step": data["simulation"].get("time_step"),
                    "time_units": data["simulation"].get("time_units"),
                }
                model_result = self.models_collection.insert_one(model_data)
                model_id = model_result.inserted_id
                
                for el in data.get("elements", []):
                    if el.get("type") != "LINK":
                        element_data = {
                            "model_id": model_id,
                            "type": el.get("type"),
                            "name": el.get("name"),
                            "description": el.get("description", ""),
                            "value": el.get("behavior", {}).get("value", ""),
                            "units": el.get("behavior", {}).get("units", ""),
                        }
                        self.elements_collection.insert_one(element_data)
                
                processed_files += 1
                
            except Exception as e:
                errors.append(f"Erreur avec le fichier {file_path}: {str(e)}")
        
        if errors:
            error_message = "\n".join(errors)
            messagebox.showerror("Erreurs", f"Des erreurs sont survenues:\n{error_message}")
        else:
            messagebox.showinfo("Succès", f"Tous les fichiers ({processed_files}/{total_files}) ont été importés avec succès.")

if __name__ == "__main__":
    login = LoginWindow()
    login.root.mainloop()
