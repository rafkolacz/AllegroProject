import tkinter as tk
from tkinter import messagebox
from alleproduct import AllegroAPI
import time

class MainWindow(tk.Frame):
    itemCounter = 0
    items = []

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.nazwa_label = tk.Label(self, text="Lista przedmiotow::")
        self.nazwa_label.pack(fill=tk.X, side=tk.LEFT)
        self.txt = tk.Text(self, height=5, width=50)
        self.txt.pack()

        self.add_btn = tk.Button(self, text="Dodaj nowy przedmiot", command=self.add_item)
        self.add_btn.pack(fill=tk.X)
        self.szukaj_btn = tk.Button(self, text="Szukaj", command=self.szukaj)
        self.szukaj_btn.pack(fill=tk.X)

    def add_item(self):
        if self.itemCounter < 5:
            t = tk.Toplevel(self)
            t.wm_title("Adding item #%s" % self.itemCounter)

            nazwa_label = tk.Label(t, text="Nazwa:")
            nazwa_txt = tk.Entry(t, width=10)
            nazwa_label.grid(column=0, row=0, sticky=tk.W)
            nazwa_txt.grid(column=1, row=0)

            sztuk_label = tk.Label(t, text="Ilosc sztuk:")
            sztuk_txt = tk.Entry(t, width=10)
            sztuk_txt.insert(0, '0')
            sztuk_label.grid(column=0, row=1, sticky=tk.W)
            sztuk_txt.grid(column=1, row=1)

            min_cena_label = tk.Label(t, text="Cena minimalna:")
            min_cena_txt = tk.Entry(t, width=10)
            min_cena_txt.insert(0, '0')
            min_cena_label.grid(column=0, row=2, sticky=tk.W)
            min_cena_txt.grid(column=1, row=2)

            max_cena_label = tk.Label(t, text="Cena maksymalna:")
            max_cena_txt = tk.Entry(t, width=10)
            max_cena_txt.insert(0, '9999')
            max_cena_label.grid(column=0, row=3, sticky=tk.W)
            max_cena_txt.grid(column=1, row=3)

            rep_label = tk.Label(t, text="Minimalna reputacja:")
            rep_txt = tk.Entry(t, width=10)
            rep_txt.insert(0, '0')
            rep_label.grid(column=0, row=4, sticky=tk.W)
            rep_txt.grid(column=1, row=4)

            oceny_label = tk.Label(t, text="Minimalna liczba ocen:")
            oceny_txt = tk.Entry(t, width=10)
            oceny_txt.insert(0, '0')
            oceny_label.grid(column=0, row=5, sticky=tk.W)
            oceny_txt.grid(column=1, row=5)

            def add():
                if nazwa_txt.get():
                    try:
                        self.items.append(
                            [nazwa_txt.get(), int(sztuk_txt.get()), float(min_cena_txt.get()),
                             float(max_cena_txt.get()),
                             float(rep_txt.get()), float(oceny_txt.get())])
                        self.txt.insert(tk.END,
                                        "Przedmiot " + str(
                                            self.itemCounter + 1) + ": [" + nazwa_txt.get() + "," + sztuk_txt.get() + "," + min_cena_txt.get() + "," + max_cena_txt.get() + "," + rep_txt.get() + "," + oceny_txt.get() + "]" + "\n")
                        self.itemCounter += 1
                        t.destroy()
                    except ValueError:
                        messagebox.showerror("Error", "Zly format danych")
                        t.destroy()
                        self.add_item()

                else:
                    messagebox.showerror("Error", "Wpisz nazwe prouktu")
                    self.add_item()

            addBtn = tk.Button(t, text="Dodaj", command=add)
            addBtn.grid(row=6)
        else:
            messagebox.showerror("Error", "Maksymalna ilosc produktu osiagnieta")

    def szukaj(self):
        if self.items:
            t = tk.Toplevel(self)
            t.wm_title("Search Result")
            set1_label = tk.Label(t, text="Zestaw 1:")
            set1_label.grid(column=0, row=1)
            set1_text = tk.Text(t, height=5, width=150)
            set1_text.grid(column=1, row=1)
            set2_label = tk.Label(t, text="Zestaw 2:")
            set2_label.grid(column=0, row=2)
            set2_text = tk.Text(t, height=5, width=150)
            set2_text.grid(column=1, row=2)
            set3_label = tk.Label(t, text="Zestaw 3:")
            set3_label.grid(column=0, row=3)
            set3_text = tk.Text(t, height=5, width=150)
            set3_text.grid(column=1, row=3)

            a = AllegroAPI(self.items)
            a.search()

            for index in range(len(a.set1)):
                set1_text.insert(tk.END, str(index + 1) + ". " + str(a.set1[index][1]) + " Cena: " + str(
                    a.set1[index][0]) + " https://allegro.pl/oferta/" + str(a.set1[index][4]) + "\n")
            for index in range(len(a.set2)):
                set2_text.insert(tk.END, str(index + 1) + ". " + str(a.set2[index][1]) + " Cena: " + str(
                    a.set2[index][0]) + " https://allegro.pl/oferta/" + str(a.set2[index][4]) + "\n")
            for index in range(len(a.set3)):
                set3_text.insert(tk.END, str(index + 1) + ". " + str(a.set3[index][1]) + " Cena: " + str(
                    a.set3[index][0]) + " https://allegro.pl/oferta/" + str(a.set3[index][4]) + "\n")

            self.items = []
            self.itemCounter = 0
            self.txt.delete('1.0', tk.END)
        else:
            messagebox.showerror("Error", "Nie dodales zadnych przedmiotow!")


root = tk.Tk()
window = MainWindow(root)
window.pack(side="top", fill="both", expand=True)
root.title("AllegroProject")
root.mainloop()
