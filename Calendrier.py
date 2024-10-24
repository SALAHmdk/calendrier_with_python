import tkinter as tk
from tkinter import messagebox
import calendar
import datetime
import holidays

# Application pour afficher le calendrier avec les jours fériés
class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar Viewer")
        self.ro_holidays = holidays.FR()  # Ici, on peut changer selon le pays

        # Créer un cadre de contrôle pour l'année et le mois
        control_frame = tk.Frame(root)
        control_frame.pack(pady=10)

        tk.Label(control_frame, text="Year:").grid(row=0, column=0, padx=5)
        self.year_entry = tk.Entry(control_frame, width=6)
        self.year_entry.insert(0, str(datetime.datetime.now().year))  # Année actuelle par défaut
        self.year_entry.grid(row=0, column=1, padx=5)

        tk.Label(control_frame, text="Month:").grid(row=0, column=2, padx=5)
        self.month_entry = tk.Entry(control_frame, width=3)
        self.month_entry.insert(0, str(datetime.datetime.now().month))  # Mois actuel par défaut
        self.month_entry.grid(row=0, column=3, padx=5)

        tk.Button(control_frame, text="Show", command=self.update_calendar).grid(row=0, column=4, padx=5)

        # Créer un cadre pour afficher le calendrier
        self.calendar_frame = tk.Frame(root)
        self.calendar_frame.pack(pady=20)
        self.days_of_week = ["M", "T", "W", "T", "F", "S", "S"]

        self.update_calendar()

    def update_calendar(self):
        # Supprimer le calendrier précédent
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        try:
            year = int(self.year_entry.get())
            month = int(self.month_entry.get())
            if not (1 <= month <= 12):
                raise ValueError("Mois invalide.")
        except ValueError:
            messagebox.showerror("Erreur", "L'année et le mois doivent être des entiers valides.")
            return

        # Générer le calendrier pour le mois spécifié
        cal = calendar.Calendar(firstweekday=0)  # Le lundi est le premier jour de la semaine
        month_days = cal.monthdayscalendar(year, month)

        # Afficher l'entête avec les jours de la semaine
        for idx, day in enumerate(self.days_of_week):
            lbl = tk.Label(self.calendar_frame, text=day, font=("Arial", 10, "bold"), relief="solid", width=4)
            lbl.grid(row=0, column=idx, padx=2, pady=2)

        # Afficher les jours du mois avec les week-ends et jours fériés colorés
        for row_idx, week in enumerate(month_days):
            for col_idx, day in enumerate(week):
                if day == 0:  # Pas de jour (en dehors du mois)
                    text = ""
                    bg_color = "white"
                    fg_color = "black"  # Ajouter cette ligne pour toujours avoir une couleur de texte
                else:
                    text = str(day)
                    # Colorier les week-ends et les jours fériés
                    bg_color = "white"
                    fg_color = "black"  # Toujours initialiser la couleur du texte
                    if col_idx >= 5:  # Week-end
                        bg_color = "#d1f7c4"  # Vert clair pour les week-ends
                    if datetime.date(year, month, day) in self.ro_holidays:  # Jours fériés
                        bg_color = "#f79a7d"  # Rouge pour les jours fériés
                        fg_color = "red"

                lbl = tk.Label(self.calendar_frame, text=text, bg=bg_color, fg=fg_color, relief="solid", width=4, height=2)
                lbl.grid(row=row_idx+1, column=col_idx, padx=2, pady=2)

        # Mettre à jour le titre de la fenêtre
        self.root.title(f"Calendar - {calendar.month_name[month]} {year}")

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
