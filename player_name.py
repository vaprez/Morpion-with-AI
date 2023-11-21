import tkinter as tk
from tkinter import messagebox


class GameSetupUI:
    def __init__(self, callback):
        self.callback = callback
        self.root = tk.Tk()
        self.root.title("Choix du Mode de Jeu")
        self.root.configure(bg='#bdc3c7')  # Couleur de fond (gris)
        self.mode_var = tk.IntVar()
        self.mode_var.set(1)

        mode_label = tk.Label(self.root, text="Choisissez le mode de jeu:", font=(
            "Helvetica", 16), bg='#bdc3c7', fg='white')
        mode_label.grid(row=0, column=0, columnspan=2,
                        padx=10, pady=(10, 0), sticky="w")

        player_vs_player = tk.Radiobutton(self.root, text="Joueur contre Joueur", variable=self.mode_var,
                                          value=1, command=self.toggle_entries, font=("Helvetica", 12), bg='#bdc3c7', fg='white')
        player_vs_player.grid(row=1, column=0, columnspan=2,
                              padx=10, pady=5, sticky="w")

        player_vs_computer = tk.Radiobutton(self.root, text="Joueur contre Ordinateur", variable=self.mode_var,
                                            value=2, command=self.toggle_entries, font=("Helvetica", 12), bg='#bdc3c7', fg='white')
        player_vs_computer.grid(
            row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.player1_label = tk.Label(self.root, text="Nom du Joueur 1:", font=(
            "Helvetica", 12), bg='#bdc3c7', fg='white')
        self.player1_entry = tk.Entry(self.root, font=("Helvetica", 12))

        self.player2_label = tk.Label(self.root, text="Nom du Joueur 2:", font=(
            "Helvetica", 12), bg='#bdc3c7', fg='white')
        self.player2_entry = tk.Entry(self.root, font=("Helvetica", 12))

        self.player_label = tk.Label(self.root, text="Nom du Joueur:", font=(
            "Helvetica", 12), bg='#bdc3c7', fg='white')
        self.player_entry = tk.Entry(self.root, font=("Helvetica", 12))

        start_button = tk.Button(self.root, text="Commencer", command=self.start_game, font=(
            "Helvetica", 12), bg='#95a5a6', fg='white')
        start_button.grid(row=5, column=0, columnspan=2,
                          padx=10, pady=(20, 10), sticky="w")

        # Centrage horizontal du bouton "Commencer"
        self.root.update_idletasks()
        width = self.root.winfo_width()
        start_button.grid_configure(
            ipadx=(width - start_button.winfo_reqwidth()) // 2)

    def toggle_entries(self):
        mode = self.mode_var.get()

        if mode == 1:
            self.player1_label.grid(
                row=3, column=0, padx=10, pady=(10, 0), sticky="w")
            self.player1_entry.grid(
                row=3, column=1, padx=10, pady=(10, 0), sticky="w")

            self.player2_label.grid(
                row=4, column=0, padx=10, pady=(10, 0), sticky="w")
            self.player2_entry.grid(
                row=4, column=1, padx=10, pady=(10, 0), sticky="w")

            self.player_label.grid_forget()
            self.player_entry.grid_forget()

        else:
            self.player_label.grid(
                row=3, column=0, padx=10, pady=(10, 0), sticky="w")
            self.player_entry.grid(
                row=3, column=1, padx=10, pady=(10, 0), sticky="w")

            self.player1_label.grid_forget()
            self.player1_entry.grid_forget()
            self.player2_label.grid_forget()
            self.player2_entry.grid_forget()

    def start_game(self):
        mode = self.mode_var.get()

        if mode == 1:
            player1_name = self.player1_entry.get()
            player2_name = self.player2_entry.get()
            messagebox.showinfo(
                "Info", f"Mode: Joueur contre Joueur\nJoueur 1: {player1_name}\nJoueur 2: {player2_name}")
        else:
            player_name = self.player_entry.get()
            messagebox.showinfo(
                "Info", f"Mode: Joueur contre Ordinateur\nJoueur: {player_name}")
        self.root.destroy()  # Ferme la fenêtre après le click sur "Commencer"
        self.callback()
        return player1_name, player2_name

    def run(self):
        self.root.mainloop()
