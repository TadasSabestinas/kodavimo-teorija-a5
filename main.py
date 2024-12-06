from encoder import Encoder
from channel import Channel
from decoder import Decoder
import tkinter as tk
from tkinter import messagebox, simpledialog


def retrieve_error_positions(sent, received):
    #nustato klaidu pozicijas tarp siusto ir gauto vektoriaus.
    #Parametrai:
    #sent - siustas pranešimas (vektorius).
    #received - gautas pranesimas (vektorius).
    positions = []
    for i in range(len(sent)):
        if sent[i] != received[i]:
            positions.append(i)
    return positions


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("A5 App")  
        self.geometry("300x400") 

        self.m = None 
        self.pe = None  
        self.input_message = None  
        self.encoded_message = None  
        self.sent_message = None  
        self.error_positions = None 
        self.decoded_message = None 

        #Sukuriami aplikacijos puslapiai (klases HomePage, InputMessagePage, ResultPage).
        self.frames = {}
        for Page in (HomePage, InputMessagePage, ResultPage):
            page_name = Page.__name__
            frame = Page(parent=self, controller=self)  #sukuriamas kiekvienas puslapis.
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")  #puslapiai isdestomi vienas ant kito.

        self.show_frame("HomePage")  #pradinis puslapis nustatomas kaip HomePage.

    def show_frame(self, page_name):
        #rodo pasirinkta puslapi pagal jo pavadinima.
        frame = self.frames[page_name]
        frame.tkraise()  #puslapis iskeliamas i prieki.


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        #inicializuoja HomePage puslapi.
        #Parametrai:
        #parent - tevinis langas.
        #controller - pagrindines programos valdiklis.
        super().__init__(parent)
        self.controller = controller

        #Vartotojo ivedimo laukai ir mygtukai
        tk.Label(self, text="Įveskite parametrus:", font=("Arial", 16)).pack(pady=10)
        tk.Label(self, text="m (natūralus skaičius):").pack()
        self.m_entry = tk.Entry(self)  #laukas parametru m ivedimui.
        self.m_entry.pack()

        tk.Label(self, text="Klaidos tikimybė p (0 ≤ p ≤ 1):").pack()
        self.pe_entry = tk.Entry(self)  #laukas klaidos tikimybei ivesti.
        self.pe_entry.pack()

        tk.Button(self, text="Toliau", command=self.validate_inputs).pack(pady=20)

    def validate_inputs(self):
        #patikrina, ar vartotojo ivesti parametrai yra teisingi.
        #jei ivestys netinkamos, rodomas klaidos pranesimas.
        try:
            m = int(self.m_entry.get())  # Gaunamas m parametras.
            pe = float(self.pe_entry.get())  # Gaunama klaidos tikimybe
            if m <= 0 or pe < 0 or pe > 1:
                raise ValueError  # Klaida, jei reiksmes ne tinkamo diapazono.
            self.controller.m = m  # Issaugoma m reikšmė.
            self.controller.pe = pe  # Issaugoma klaidos tikimybe.
            self.controller.show_frame("InputMessagePage")  #pereinama i kita psl
        except ValueError:
            messagebox.showerror("Klaida", "Įveskite tinkamas reikšmes: m > 0, 0 ≤ p ≤ 1.") 


class InputMessagePage(tk.Frame):
    def __init__(self, parent, controller):
        #inicializuojamas InputMessagePage psl.
        super().__init__(parent)
        self.controller = controller

        #Vartotojo ivedimo laukai ir mygtukai
        tk.Label(self, text="Įveskite pranešimą:", font=("Arial", 16)).pack(pady=10)
        self.message_entry = tk.Entry(self, width=50) 
        self.message_entry.pack()

        tk.Button(self, text="Užkoduoti", command=self.encode_message).pack(pady=10) 
        self.encoded_label = tk.Label(self, text="")  # zinutes uzkodavimo rez laukas
        self.encoded_label.pack()

        tk.Button(self, text="Siųsti", command=self.send_message).pack(pady=10)

    def encode_message(self):
        #uzkoduoja vartotojo ivesta pranesima.
        message = self.message_entry.get()
        if len(message) != self.controller.m + 1 or not all(c in "01" for c in message):
            # Patikrina, ar žinutė yra tinkamo ilgio ir sudaryta iš dvejetainių reikšmių.
            messagebox.showerror("Klaida", f"Žinutė turi būti {self.controller.m + 1} bitų ilgio dvejetainė eilutė.")
            return

        decoder = Decoder()
        self.controller.input_message = decoder.string_to_int_array(message)  # Konvertuojama į sveikųjų skaičių masyvą
        encoder = Encoder()
        self.controller.encoded_message = encoder.encode(self.controller.input_message, self.controller.m)  #uzkoduojama
        self.encoded_label.config(text=f"Užkoduota žinutė: {self.controller.encoded_message}")  #parodom uzkoduota rez

    def send_message(self):
        #siunciam uzkoduota pranesima per kanala
        if not self.controller.encoded_message:
            messagebox.showerror("Klaida", "Pirma reikia užkoduoti žinutę.")  #patikrinam ar zinute uzkoduota
            return

        channel = Channel(self.controller.pe)
        self.controller.sent_message = channel.send(self.controller.encoded_message)  #siunciam kanalu zinute
        self.controller.error_positions = retrieve_error_positions(self.controller.encoded_message, self.controller.sent_message)  #nustatom klaidu pozicijas
        self.controller.frames["ResultPage"].update_labels()
        self.controller.show_frame("ResultPage")  # pereinam i rezultatu psl


class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        #inicializuojam rez psl
        super().__init__(parent)
        self.controller = controller

        #etiketes rezultatams ir veiksmams
        tk.Label(self, text="Rezultatai:", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Kanalo žinutė:").pack()
        self.sent_label = tk.Label(self, text="(žinutė nepasiekiama)", font=("Arial", 12), fg="blue")
        self.sent_label.pack()

        tk.Label(self, text="Klaidos:").pack()
        self.error_label = tk.Label(self, text="(klaidos nepasiekiamos)", font=("Arial", 12), fg="red")
        self.error_label.pack()

        tk.Label(self, text="Pradinė žinutė:").pack()
        self.input_label = tk.Label(self, text="(pradinė žinutė nepasiekiama)", font=("Arial", 12), fg="green")
        self.input_label.pack()

        tk.Label(self, text="Dekoduota žinutė:").pack()
        self.decoded_label = tk.Label(self, text="(dekoduota žinutė nepasiekiama)", font=("Arial", 12))
        self.decoded_label.pack()

        #mygtukai rezultatu redagavimui ir grizimui i pagr langa
        tk.Button(self, text="Redaguoti", command=self.edit_sent_message).pack(pady=10)
        tk.Button(self, text="Dekoduoti", command=self.decode_message).pack(pady=10)
        tk.Button(self, text="Grįžti į pradinį puslapį", command=lambda: controller.show_frame("HomePage")).pack(pady=10)

    def update_labels(self):
        # Atnaujina rezultatu etiketes, rodancias zinute, klaidas ir dekodavimo rezultatus.
        self.input_label.config(text=f"Pradinė žinutė: {self.controller.input_message}")
        self.sent_label.config(text=f"Kanalo žinutė: {self.controller.sent_message}")
        self.error_label.config(
            text=f"Klaidų skaičius: {len(self.controller.error_positions)}, "
                 f"pozicijos: {self.controller.error_positions}"
        )
        self.decoded_label.config(text="") #nunulinamas dekodavimo rezultatas

    def edit_sent_message(self):
        #leidzia vartotojui rankiniu budu redaguoti kanalo žinute.
        new_message = simpledialog.askstring("Redaguoti žinutę", "Įveskite naują žinutę:")
        if new_message and len(new_message) == len(self.controller.sent_message) and all(c in "01" for c in new_message):
            decoder = Decoder()
            self.controller.sent_message = decoder.string_to_int_array(new_message) 
            self.controller.error_positions = retrieve_error_positions(
                self.controller.encoded_message, self.controller.sent_message
            )  
            self.update_labels()  #atnaujinamos rezultatu etiketes
        else:
            messagebox.showerror("Klaida", "Netinkama žinutė. Įveskite tinkamos ilgio dvejetainę eilutę.")

    def decode_message(self):
        try:
            decoder = Decoder()
            self.controller.decoded_message = decoder.decode(self.controller.sent_message, self.controller.m)  # Dekoduoja.
            self.decoded_label.config(text=f"Rezultatas: {self.controller.decoded_message}")  # Rodo rezultata
        except Exception as e:
            messagebox.showerror("Klaida dekoduojant", f"Įvyko klaida: {str(e)}")  #rodoma klaida jei dekodavimas nepavyksta.


if __name__ == "__main__":
    app = App()  
    app.mainloop()  
