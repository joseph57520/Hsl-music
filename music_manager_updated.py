
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# Chemins des dossiers de catégories
categories = {
    "Rap / Hip-Hop": "rap_hiphop.html",
    "Jazz / Swing": "jazz_swing.html",
    "Billy Hassli": "billy_hassli.html",
}
music_folder = "music"

# Fonction pour mettre à jour le fichier HTML
def update_html(category_file, new_name):
    try:
        category_path = os.path.join(os.getcwd(), category_file)
        # Lire le contenu actuel du fichier HTML
        with open(category_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Ajouter une nouvelle entrée pour la musique
        music_section_start = "<section class=\"content\">"
        music_section_end = "</section>"
        start_index = html_content.find(music_section_start) + len(music_section_start)
        end_index = html_content.find(music_section_end)

        # Ajouter la nouvelle musique sans effacer les précédentes
        existing_entries = html_content[start_index:end_index].strip()
        new_entry = f"""
        <div class=\"music-card\">
            <h3>{os.path.splitext(new_name)[0]}</h3>
            <audio controls>
                <source src=\"music/{new_name}\" type=\"audio/mp3\">
                Votre navigateur ne supporte pas l'élément audio.
            </audio>
        </div>
        """
        updated_entries = existing_entries + "\n" + new_entry if existing_entries else new_entry
        new_html_content = (
            html_content[:start_index] + "\n" + updated_entries + "\n" + html_content[end_index:]
        )

        # Écrire le nouveau contenu dans le fichier HTML
        with open(category_path, "w", encoding="utf-8") as f:
            f.write(new_html_content)

        messagebox.showinfo("Succès", f"La musique a été ajoutée à la catégorie {category_file}.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

# Fonction principale pour renommer et déplacer la musique
def process_music(category):
    if not selected_file_path:
        messagebox.showwarning("Attention", "Veuillez sélectionner un fichier MP3.")
        return

    new_name = new_name_entry.get().strip()
    if not new_name:
        messagebox.showwarning("Attention", "Veuillez entrer un nouveau nom pour la musique.")
        return

    # Vérifier l'extension
    if not new_name.endswith(".mp3"):
        new_name += ".mp3"

    dest_path = os.path.join(music_folder, new_name)
    try:
        # Vérifier si le fichier existe déjà
        if not os.path.exists(dest_path):
            shutil.copy(selected_file_path, dest_path)
        else:
            messagebox.showinfo("Info", "Le fichier existe déjà, il ne sera pas copié.")

        # Mettre à jour le fichier HTML correspondant
        update_html(categories[category], new_name)

        messagebox.showinfo("Succès", f"Musique ajoutée à la catégorie {category}.")
        root.destroy()  # Fermer l'application
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

# Fonction pour sélectionner un fichier
def select_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename(
        title="Choisir un fichier MP3",
        filetypes=[("Fichiers MP3", "*.mp3")]
    )
    if selected_file_path:
        file_label.config(text=f"Fichier sélectionné : {os.path.basename(selected_file_path)}")

# Interface graphique
root = tk.Tk()
root.title("Gestionnaire de Musiques")
root.geometry("500x400")

selected_file_path = None

tk.Label(root, text="Ajouter une musique", font=("Arial", 16)).pack(pady=10)

# Bouton pour sélectionner un fichier
tk.Button(root, text="Choisir un fichier", command=select_file, width=20).pack(pady=10)
file_label = tk.Label(root, text="Aucun fichier sélectionné", fg="gray")
file_label.pack(pady=5)

# Champ pour entrer le nouveau nom
tk.Label(root, text="Entrez un nouveau nom :", font=("Arial", 12)).pack(pady=10)
new_name_entry = tk.Entry(root, width=40)
new_name_entry.pack(pady=5)

# Boutons pour sélectionner la catégorie
tk.Label(root, text="Choisissez une catégorie :", font=("Arial", 12)).pack(pady=10)
for category in categories.keys():
    tk.Button(root, text=category, command=lambda c=category: process_music(c), width=20).pack(pady=5)

root.mainloop()
