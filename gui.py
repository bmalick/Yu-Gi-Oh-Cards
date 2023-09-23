from tkinter import Tk, Entry, Label, Canvas, PhotoImage, Button, messagebox, font, simpledialog
from tkinter.constants import END
from ygo_deck import YGODeck
from requests.exceptions import HTTPError
import os



class Gui:
    def __init__(self) -> None:
        self.create_window()
        self.create_logo()
        self.create_labels()
        self.create_entries()
        self.create_buttons()
        self.verify_keys()
        
        self.window.mainloop()
    
    def verify_keys(self):
        self.filename = "keys.txt"
        if self.filename not in os.listdir():
            self.create_keys()
        
    def create_keys(self):
        api_key = link = None
        # while not api_key:
        api_key = simpledialog.askstring(title="API Key", prompt="Enter you Notion API Key")
        # while not link:
        link = simpledialog.askstring(title="Database link", prompt="Enter you Notion database link")
        with open(self.filename,"w") as file:
            file.write(api_key+"\n"+link)

    def create_window(self):
        self.window = Tk()
        self.window.title("Yu-Gi-Oh Cards")
        self.window.config(padx=30, pady=30)
    
    def create_logo(self):
        canvas = Canvas(width=300, height=300)
        self.logo = PhotoImage(file="./logo.jpg")
        canvas.create_image(150,150, image=self.logo)
        canvas.grid(column=1, row=0, columnspan=2)


    def create_labels(self):
        self.custom_font = font.Font(family="Segoe UI", size=11)
        self.name_label      = Label(text="Name", font=self.custom_font)
        self.type_label      = Label(text="Type", font=self.custom_font)
        self.atk_label       = Label(text="ATK", font=self.custom_font)
        self.def_label       = Label(text="DEF", font=self.custom_font)
        self.level_label     = Label(text="Level", font=self.custom_font)
        self.race_label      = Label(text="Race", font=self.custom_font)
        self.attribute_label = Label(text="Attribute", font=self.custom_font)
        self.limit_label     = Label(text="Limit", font=self.custom_font)
        
        self.place_labels()
        


    def place_labels(self):
        self.left_labels  = [self.name_label, self.type_label, self.atk_label, self.def_label]
        self.right_labels = [self.level_label, self.race_label, self.attribute_label, self.limit_label]
        
        for i, label in enumerate(self.left_labels):
            label.grid(row=i+1, column=0, pady=10, sticky="w")
            
        for i, label in enumerate(self.right_labels):
            label.grid(row=i+1, column=3, pady=10, sticky="e")


    def create_entries(self):
        self.name_entry      = Entry(width=35, font=self.custom_font)
        self.type_entry      = Entry(width=35, font=self.custom_font)
        self.atk_entry       = Entry(width=35, font=self.custom_font)
        self.def_entry       = Entry(width=35, font=self.custom_font)
        self.level_entry     = Entry(width=35, font=self.custom_font)
        self.race_entry      = Entry(width=35, font=self.custom_font)
        self.attribute_entry = Entry(width=35, font=self.custom_font)
        self.limit_entry     = Entry(width=35, font=self.custom_font)

        self.place_entries()
        self.insert_default_values()


    def place_entries(self):
        self.left_entries  = [self.name_entry, self.type_entry, self.atk_entry, self.def_entry]
        self.right_entries = [self.level_entry, self.race_entry, self.attribute_entry, self.limit_entry]
        
        for i, entry in enumerate(self.left_entries):
            entry.grid(row=i+1, column=1, pady=10, padx=10)
            
        for i, entry in enumerate(self.right_entries):
            entry.grid(row=i+1, column=2, pady=10, padx=10)
            
    def insert_default_values(self):
        self.name_entry.insert(0, "Dark Magician")
        self.limit_entry.insert(0, 1)


    def create_buttons(self):
        btn_font = font.Font(family="Roboto", size=10, weight="bold")
        self.keys_btn = Button(text="Change keys", width=15, font=btn_font, command=self.create_keys, bg="blue", fg="white", highlightthickness=0)
        self.keys_btn.grid(row=5, column=1)
        
        self.fetch_btn = Button(text="Fetch", width=15, font=btn_font, command=self.fetch, bg="green", fg="white", highlightthickness=0)
        self.fetch_btn.grid(row=5, column=2)
        
        
        self.clear_btn = Button(text="Clear", width=15, font=btn_font, command=self.clear, bg="red", fg="white",  highlightthickness=0)
        self.clear_btn.grid(row=5, column=3)
        

    
    def get_entries(self):
        entries = {
            "card_name"      : self.name_entry.get(),
            "card_type"      : self.type_entry.get(),
            "card_atk"       : self.atk_entry.get(),
            "card_def"       : self.def_entry.get(),
            "card_level"     : self.level_entry.get(),
            "card_race"      : self.race_entry.get(),
            "card_attribute" : self.attribute_entry.get().upper(),
            "limit"          : self.limit_entry.get(),
        }
        
        return entries
        

    def clear(self):
        for entry in self.left_entries+self.right_entries:
            entry.delete(0, END)

    def fetch(self):
        
        entries = self.get_entries()
        entries = {key:item if item!="" else None for key,item in entries.items()}
        for key in ["card_atk", "card_def", "card_level", "limit"]:
            try:
                if entries[key] is not None:
                    entries[key] = int(entries[key])
            except ValueError:
                messagebox.showinfo(title="Integers error", message="This occurs because one of the integer entry is not an integer. Please verify the inputs of Atk, Def, Level and Limit")
                self.clear()
                self.limit_entry.insert(0, 1)
                return 
        if entries["limit"] == None:
            entries["limit"] = 1
        
        entries["filename"] = self.filename

        ygo_deck = YGODeck(
            **entries
        )
        try:
            ygo_deck.fetch()
        except HTTPError:
            messagebox.showinfo(title="Http error", message="This occurs because something is wrong with notion key or your database id. If you chande properties name in your notion database this won't work.")


        