import tkinter as tk
from tkinter import filedialog

class NextbotConfigGUI:
    def __init__(self, master):
        self.master = master
        master.title("Nextbot Creation")

        self.name = tk.StringVar()
        self.texture = tk.StringVar()
        self.chase_sound = tk.StringVar()
        self.death_sound = tk.StringVar()
        self.death_texture = tk.StringVar()
        self.chase_speed = tk.DoubleVar()
        self.wonder_speed = tk.DoubleVar()

        tk.Label(master, text="Name: ").grid(row=0, column=0)
        tk.Entry(master, textvariable=self.name).grid(row=0,column=1)

        tk.Label(master, text="Texture:").grid(row=1, column=0)
        tk.Entry(master, textvariable=self.texture).grid(row=1, column=1)
        tk.Button(master, text="Select", command=self.choose_texture_file).grid(row=0, column=2)

        tk.Label(master, text="Chase Sound:").grid(row=2, column=0)
        tk.Entry(master, textvariable=self.chase_sound).grid(row=2, column=1)
        tk.Button(master, text="Select", command=self.choose_chase_sound_file).grid(row=1, column=2)

        tk.Label(master, text="Death Sound:").grid(row=3, column=0)
        tk.Entry(master, textvariable=self.death_sound).grid(row=3, column=1)
        tk.Button(master, text="Select", command=self.choose_death_sound_file).grid(row=2, column=2)

        tk.Label(master, text="Death Texture:").grid(row=4, column=0)
        tk.Entry(master, textvariable=self.death_texture).grid(row=4, column=1)
        tk.Button(master, text="Select", command=self.choose_death_texture_file).grid(row=3, column=2)

        tk.Label(master, text="Chase Speed:").grid(row=5, column=0)
        tk.Entry(master, textvariable=self.chase_speed).grid(row=5, column=1)

        tk.Label(master, text="Wonder Speed:").grid(row=6, column=0)
        tk.Entry(master, textvariable=self.wonder_speed).grid(row=6, column=1)

        tk.Button(master, text="Create Nextbot", command=self.create_nextbot).grid(row=7, column=1)

        tk.Button(master, text="Reset", command=self.reset_inputs).grid(row=7, column=2)

    def choose_texture_file(self):
        file_path = filedialog.askopenfilename()
        self.texture.set(file_path)

    def choose_chase_sound_file(self):
        file_path = filedialog.askopenfilename()
        self.chase_sound.set(file_path)

    def choose_death_sound_file(self):
        file_path = filedialog.askopenfilename()
        self.death_sound.set(file_path)

    def choose_death_texture_file(self):
        file_path = filedialog.askopenfilename()
        self.death_texture.set(file_path)

    def create_nextbot(self):
        # Output the user choices in the desired format and save to a file
        nextbot_config = f"{self.name.get()}=Nextbot(texture='{self.texture.get()}', chase_sound='{self.chase_sound.get()}', death_sound='{self.death_sound.get()}', death_texture='{self.death_texture.get()}', chase_speed={self.chase_speed.get()}, wonder_speed={self.wonder_speed.get()})"
        with open("Nextbots.txt", "a") as f:
            f.write(nextbot_config + "\n")

    def reset_inputs(self):
        self.texture.set("")
        self.chase_sound.set("")
        self.death_sound.set("")
        self.death_texture.set("")
        self.chase_speed.set(0.0)
        self.wonder_speed.set(0.0)


root = tk.Tk()
my_gui = NextbotConfigGUI(root)
root.mainloop()