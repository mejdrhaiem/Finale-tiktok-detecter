import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import queue
from datetime import datetime
import os
import shutil
import csv

from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent
from detector import extract_phone_and_suite
from storage import save_phone, TXT_FILE, CSV_FILE
from config import USERNAME, PROXY

# PDF
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet


class TikTokLiveGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Live Monitor - Détection de Numéros")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1a1a1a")

        # Variables
        self.client = None
        self.client_thread = None
        self.is_running = False
        self.was_connected = False
        self.username_var = tk.StringVar(value=USERNAME)
        self.status_var = tk.StringVar(value="⏸️ Arrêté")
        self.comments_count = 0
        self.phones_count = 0

        self.message_queue = queue.Queue()
        self.check_queue()
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#1a1a1a', foreground='#ffffff')
        style.configure('Status.TLabel', font=('Arial', 12), background='#1a1a1a', foreground='#00ff00')

        main_frame = tk.Frame(self.root, bg="#1a1a1a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header
        header_frame = tk.Frame(main_frame, bg="#2a2a2a", relief=tk.RAISED, bd=2)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(header_frame, text="🔴 TikTok Live Monitor",
                 font=('Arial', 18, 'bold'), bg="#2a2a2a", fg="#ff0055").pack(pady=10)

        # Contrôles
        control_frame = tk.Frame(main_frame, bg="#2a2a2a", relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 10))

        username_frame = tk.Frame(control_frame, bg="#2a2a2a")
        username_frame.pack(side=tk.LEFT, padx=10, pady=10)
        tk.Label(username_frame, text="Username TikTok:",
                 font=('Arial', 10), bg="#2a2a2a", fg="#ffffff").pack(side=tk.LEFT, padx=5)
        tk.Entry(username_frame, textvariable=self.username_var, width=20, font=('Arial', 10)).pack(side=tk.LEFT, padx=5)

        button_frame = tk.Frame(control_frame, bg="#2a2a2a")
        button_frame.pack(side=tk.LEFT, padx=20, pady=10)
        self.start_button = tk.Button(button_frame, text="▶️ Démarrer",
                                      command=self.start_client, bg="#00aa00",
                                      fg="white", font=('Arial', 10, 'bold'),
                                      width=12, height=2)
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.stop_button = tk.Button(button_frame, text="⏹️ Arrêter",
                                     command=self.stop_client, bg="#aa0000",
                                     fg="white", font=('Arial', 10, 'bold'),
                                     width=12, height=2, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        self.download_button = tk.Button(button_frame, text="💾 Télécharger",
                                         command=self.download_files, bg="#0066cc",
                                         fg="white", font=('Arial', 10, 'bold'),
                                         width=12, height=2)
        self.download_button.pack(side=tk.LEFT, padx=5)

        status_frame = tk.Frame(control_frame, bg="#2a2a2a")
        status_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        tk.Label(status_frame, text="Statut:",
                 font=('Arial', 10), bg="#2a2a2a", fg="#ffffff").pack(side=tk.LEFT, padx=5)
        self.status_label = tk.Label(status_frame, textvariable=self.status_var,
                                    font=('Arial', 10, 'bold'), bg="#2a2a2a", fg="#00ff00")
        self.status_label.pack(side=tk.LEFT, padx=5)

        # Stats
        stats_frame = tk.Frame(main_frame, bg="#2a2a2a", relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        self.comments_label = tk.Label(stats_frame, text="💬 Commentaires: 0",
                                       font=('Arial', 11), bg="#2a2a2a", fg="#ffffff")
        self.comments_label.pack(side=tk.LEFT, padx=20, pady=10)
        self.phones_label = tk.Label(stats_frame, text="📞 Numéros détectés: 0",
                                     font=('Arial', 11), bg="#2a2a2a", fg="#00ff00")
        self.phones_label.pack(side=tk.LEFT, padx=20, pady=10)

        # Contenu
        content_frame = tk.Frame(main_frame, bg="#1a1a1a")
        content_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(content_frame, bg="#2a2a2a", relief=tk.RAISED, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        tk.Label(left_frame, text="💬 Commentaires en temps réel",
                 font=('Arial', 12, 'bold'), bg="#2a2a2a", fg="#ffffff").pack(pady=5)
        self.comments_text = scrolledtext.ScrolledText(left_frame,
                                                       height=20, width=50,
                                                       bg="#1a1a1a", fg="#ffffff",
                                                       font=('Consolas', 9),
                                                       wrap=tk.WORD)
        self.comments_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        right_frame = tk.Frame(content_frame, bg="#2a2a2a", relief=tk.RAISED, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        tk.Label(right_frame, text="📞 Numéros de téléphone détectés",
                 font=('Arial', 12, 'bold'), bg="#2a2a2a", fg="#00ff00").pack(pady=5)
        self.phones_text = scrolledtext.ScrolledText(right_frame,
                                                     height=20, width=50,
                                                     bg="#1a1a1a", fg="#00ff00",
                                                     font=('Consolas', 9),
                                                     wrap=tk.WORD)
        self.phones_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # --- Gestion queue ---
    def check_queue(self):
        try:
            while True:
                msg_type, data = self.message_queue.get_nowait()
                if msg_type == "comment":
                    self.add_comment(data['user'], data['text'])
                elif msg_type == "phone":
                    self.add_phone(data['phone'], data['suite'], data['user'])
                elif msg_type == "status":
                    self.status_var.set(data)
                elif msg_type == "error":
                    self.add_error(data)
                elif msg_type == "live_ended":
                    self.handle_live_ended()
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_queue)

    def add_comment(self, user, text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.comments_text.insert(tk.END, f"[{timestamp}] {user}: {text}\n")
        self.comments_text.see(tk.END)
        self.comments_count += 1
        self.comments_label.config(text=f"💬 Commentaires: {self.comments_count}")

    def add_phone(self, phone, suite, user):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.phones_text.insert(tk.END, f"[{timestamp}] 📞 {phone}\n")
        self.phones_text.insert(tk.END, f"    👤 {user}\n")
        if suite.strip():
            self.phones_text.insert(tk.END, f"    📝 {suite}\n")
        self.phones_text.insert(tk.END, f"{'-'*50}\n")
        self.phones_text.see(tk.END)
        self.phones_count += 1
        self.phones_label.config(text=f"📞 Numéros détectés: {self.phones_count}")

    def add_error(self, error_msg):
        self.comments_text.insert(tk.END, f"⚠️ ERREUR: {error_msg}\n", "error")
        self.comments_text.see(tk.END)
        self.comments_text.tag_config("error", foreground="#ff0000")

    # --- TikTok Client ---
    def create_client(self):
        username = self.username_var.get().strip()
        if not username:
            messagebox.showerror("Erreur", "Veuillez entrer un username TikTok")
            return None

        client_config = {"unique_id": username}
        if PROXY:
            client_config["proxy"] = PROXY
        client = TikTokLiveClient(**client_config)

        @client.on(CommentEvent)
        async def on_comment(event: CommentEvent):
            try:
                text = event.comment
                user = event.user.nick_name  # corrigé nick_name
                self.message_queue.put(("comment", {"user": user, "text": text}))
                results = extract_phone_and_suite(text)
                for phone, suite in results:
                    if save_phone(phone, suite, user):
                        self.message_queue.put(("phone", {"phone": phone, "suite": suite, "user": user}))
            except Exception as e:
                self.message_queue.put(("error", str(e)))

        return client

    def run_client(self):
        try:
            self.message_queue.put(("status", "🟢 Connexion en cours..."))
            self.client = self.create_client()
            if not self.client:
                self.is_running = False
                self.message_queue.put(("status", "⏸️ Arrêté"))
                return
            self.message_queue.put(("status", "🟢 Connecté - En attente du LIVE..."))
            self.was_connected = True
            self.client.run()
        except Exception as e:
            self.message_queue.put(("error", str(e)))
            self.is_running = False
            self.root.after(0, self.update_buttons)

    def start_client(self):
        if self.is_running: return
        self.is_running = True
        self.was_connected = False
        self.update_buttons()
        self.client_thread = threading.Thread(target=self.run_client, daemon=True)
        self.client_thread.start()

    def stop_client(self):
        if not self.is_running: return
        self.is_running = False
        self.was_connected = False
        self.message_queue.put(("status", "⏸️ Arrêt en cours..."))
        if self.client:
            try:
                self.client.stop()
            except:
                pass
        self.message_queue.put(("status", "⏸️ Arrêté"))
        self.update_buttons()

    def handle_live_ended(self):
        self.is_running = False
        self.update_buttons()
        self.message_queue.put(("status", "🔴 Live terminé"))
        self.root.after(500, self.ask_download_after_live)

    def ask_download_after_live(self):
        if messagebox.askyesno("Live terminé",
                               f"Le live est terminé.\n\n"
                               f"💬 Commentaires reçus: {self.comments_count}\n"
                               f"📞 Numéros détectés: {self.phones_count}\n\n"
                               f"Voulez-vous télécharger les fichiers des commentaires extraits ?"):
            self.download_files()

    # --- Export fichiers ---
    def download_files(self):
        try:
            if not os.path.exists(CSV_FILE) and not os.path.exists(TXT_FILE):
                messagebox.showwarning("Aucun fichier",
                                       "Aucun fichier de commentaires trouvé.\n"
                                       "Les fichiers seront créés lors de la détection de numéros.")
                return
            dest_folder = filedialog.askdirectory(title="Choisir le dossier de destination pour les fichiers")
            if not dest_folder: return

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            username = self.username_var.get().strip() or "tiktok"
            folder_name = f"tiktok_live_{username}_{timestamp}"
            dest_path = os.path.join(dest_folder, folder_name)
            os.makedirs(dest_path, exist_ok=True)

            files_copied = []

            if os.path.exists(CSV_FILE):
                csv_dest = os.path.join(dest_path, "phones.csv")
                shutil.copy2(CSV_FILE, csv_dest)
                files_copied.append("phones.csv")
                # Générer PDF depuis CSV
                pdf_file = os.path.join(dest_path, "phones.pdf")
                self.create_pdf_from_csv(CSV_FILE, pdf_file)
                files_copied.append("phones.pdf")

            if os.path.exists(TXT_FILE):
                txt_dest = os.path.join(dest_path, "phones.txt")
                shutil.copy2(TXT_FILE, txt_dest)
                files_copied.append("phones.txt")

            if files_copied:
                messagebox.showinfo("Téléchargement réussi",
                                    f"Fichiers téléchargés avec succès !\n\n"
                                    f"📁 Dossier: {dest_path}\n\n"
                                    f"Fichiers copiés:\n" + "\n".join(f"  • {f}" for f in files_copied))
            else:
                messagebox.showwarning("Aucun fichier", "Aucun fichier à télécharger.")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du téléchargement:\n{str(e)}")

    def create_pdf_from_csv(self, csv_file, pdf_file):
        if not os.path.exists(csv_file):
            return
        doc = SimpleDocTemplate(pdf_file, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        title = Paragraph("📞 Numéros de téléphone détectés", styles['Heading1'])
        elements.append(title)
        elements.append(Spacer(1, 12))

        data = [["Numéro", "Suite / Note", "Utilisateur"]]
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)

        table = Table(data, colWidths=[120, 250, 120])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#b0b0b0")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 8),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#e0e0e0")),
            ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ]))
        elements.append(table)
        doc.build(elements)

    def update_buttons(self):
        if self.is_running:
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
        else:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = TikTokLiveGUI(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (app.stop_client(), root.destroy()))
    root.mainloop()


if __name__ == "__main__":
    main()
