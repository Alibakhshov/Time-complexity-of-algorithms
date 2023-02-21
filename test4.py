import tkinter as tk
from tkinter import filedialog
import pygame
import random
import time

# set the size of the window and the font for the labels
WINDOW_SIZE = 800
FONT_SIZE = 20

class SortGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Selection Sort Algorithm")
        self.master.geometry("800x600")

        # create labels and buttons
        self.label = tk.Label(self.master, text="Enter numbers or select a file to sort:")
        self.label.pack(pady=10)

        self.entry = tk.Entry(self.master, width=50)
        self.entry.pack()

        self.browse_button = tk.Button(self.master, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=10)

        self.sort_button = tk.Button(self.master, text="Sort", command=self.start_sorting)
        self.sort_button.pack(pady=10)

        self.save_button = tk.Button(self.master, text="Save", command=self.save_output)
        self.save_button.pack(pady=10)

        self.step_label = tk.Label(self.master, text="")
        self.step_label.pack(pady=10)

        self.canvas = tk.Canvas(self.master, width=WINDOW_SIZE, height=WINDOW_SIZE//2)
        self.canvas.pack()

        # initialize pygame mixer for music
        pygame.mixer.init()

        # initialize variables
        self.numbers = []
        self.filename = ""

    # function to browse a file and load its contents
    def browse_file(self):
        self.filename = filedialog.askopenfilename()
        with open(self.filename, 'r') as f:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, f.read())

    # function to start the sorting
    def start_sorting(self):
        self.numbers = []
        input_str = self.entry.get()

        # if user has input numbers
        if input_str:
            self.numbers = [int(x) for x in input_str.split()]

        # if user has uploaded a file
        elif self.filename:
            with open(self.filename, 'r') as f:
                input_str = f.read()
                self.numbers = [int(x) for x in input_str.split()]

        # if no numbers have been input or uploaded
        else:
            return

        # play music while sorting
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.play()

        # run selection sort
        for i in range(len(self.numbers)):
            min_index = i
            # select the minimum element in the unsorted part of the list
            for j in range(i+1, len(self.numbers)):
                if self.numbers[j] < self.numbers[min_index]:
                    min_index = j

            # swap the minimum element with the first unsorted element
            self.numbers[i], self.numbers[min_index] = self.numbers[min_index], self.numbers[i]

            # update the canvas and the step label after each swap
            self.display_numbers()
            self.step_label.config(text=f"Step {i+1}: Swapped {self.numbers[i]} and {self.numbers[min_index]}")
            self.master.update()

            # wait for a short period of time to create an animation effect
            time.sleep(0.1)

        # stop the music after sorting
        pygame.mixer.music.stop()

        # display the time complexity of the sort
        self.step_label.config(text=f"Time complexity: O(n^2)")

    # function to display the numbers on the canvas
    def display_numbers(self):
        self.canvas.delete("all")
        width = WINDOW_SIZE // len(self.numbers)
        x = 0
        for i in range(len(self.numbers)):
            height = self.numbers[i] * 5
            self.canvas.create_rectangle(x, 0, x+width, height, fill="blue")
            self.canvas.create_text(x+width/2, height+10, text=str(self.numbers[i]))
            x += width

    # function to save the output to a file
    def save_output(self):
        with filedialog.asksaveasfile(mode="w", defaultextension=".txt") as f:
            f.write(" ".join([str(x) for x in self.numbers]))

    def run(self):
        self.master.mainloop()
root = tk.Tk()
gui = SortGUI(root)
gui.run()