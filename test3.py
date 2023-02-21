import tkinter
import pygame
import random

# initialize pygame mixer for music
pygame.mixer.init()

# set the size of the window and the font for the labels
WINDOW_SIZE = 800
FONT_SIZE = 20

# create a list of random numbers to sort
numbers = [random.randint(1, 100) for _ in range(20)]

# create the main window and set the title
window = tkinter.Tk()
window.title("Selection Sort Algorithm")

# create a canvas to display the numbers
canvas = tkinter.Canvas(window, width=WINDOW_SIZE, height=WINDOW_SIZE//2)
canvas.pack()

# create a label to display the instructions
instruction_label = tkinter.Label(window, text="Click the button to sort the numbers!")
instruction_label.config(font=("Courier", FONT_SIZE))
instruction_label.pack()

# create a label to display the current step of the algorithm
step_label = tkinter.Label(window, text="")
step_label.config(font=("Courier", FONT_SIZE))
step_label.pack()

# create a button to start the sorting
button = tkinter.Button(window, text="Sort", command=lambda: start_sorting(numbers))
button.pack()

# create a function to start the sorting
def start_sorting(numbers):
    # play music while sorting
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play()

    for i in range(len(numbers)):
        min_index = i
        # select the minimum element in the unsorted part of the list
        for j in range(i+1, len(numbers)):
            if numbers[j] < numbers[min_index]:
                min_index = j

        # swap the minimum element with the first unsorted element
        numbers[i], numbers[min_index] = numbers[min_index], numbers[i]

        # update the canvas and the step label after each swap
        display_numbers(numbers)
        step_label.config(text=f"Step {i+1}: Swapped {numbers[i]} and {numbers[min_index]}")
        window.update()

        # wait for a short period of time to create an animation effect
        pygame.time.wait(50)

    # stop the music after sorting
    pygame.mixer.music.stop()

# create a function to display the numbers in the canvas
def display_numbers(numbers):
    canvas.delete("all")
    bar_width = WINDOW_SIZE // len(numbers)
    for i in range(len(numbers)):
        bar_height = numbers[i] * (WINDOW_SIZE//2) // 100
        x1 = i * bar_width
        y1 = WINDOW_SIZE//2 - bar_height
        x2 = (i+1) * bar_width
        y2 = WINDOW_SIZE//2
        canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
        canvas.create_text((x1+x2)//2, y1-10, text=str(numbers[i]), font=("Courier", FONT_SIZE))

# display the GUI
display_numbers(numbers)
window.mainloop()
