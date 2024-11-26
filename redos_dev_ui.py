import tkinter as tk
import re
import timeit
import matplotlib.pyplot as plt

xs = []
ys = []

displayed_image = None  # has to be global due to garbage collection


# ToDo: add option for timeout
# ToDo: allow to choose regex engine
# ToDo: syntax highlighting / check regex for validity on typing, if invalid, show in red
# ToDo: What if user changes regex? => Don't allow user to change regex unless cleared.
# ToDo: add flags
# ToDo: allow to choose between search() and match
# ToDo: show group matches
# ToDo: make plotted dots green on match and red on mismatch!


def main():
    def time_regex_on_input(regex, input) -> float:
        regex_pattern = re.compile(regex)
        t = timeit.Timer(lambda: regex_pattern.search(input))
        # re.search() is the Python equivalent for JavaScript's RegExp.prototype.test().
        # re.match() only matches the *beginning* of strings!
        return t.timeit(number=1_000_000)

    def plot():
        global xs
        global ys
        global displayed_image

        plt.title(f"Regex: {text_field_regex.get('1.0', tk.END)}")
        plt.xlabel("Input length")
        plt.ylabel("Time")
        plt.scatter(xs, ys)

        destination = "tmp.png"
        plt.savefig(destination)
        plt.close('all')

        displayed_image = tk.PhotoImage(file=destination)
        image_label.config(image=displayed_image)

    def add_to_plot():
        global xs
        global ys
        regex = text_field_regex.get("1.0", tk.END)
        input = text_field_input.get("1.0", tk.END)
        x = len(input)
        y = time_regex_on_input(regex=regex, input=input)
        xs.append(x)
        ys.append(y)
        plot()

    def clear_plot():
        global xs
        global ys
        xs = []
        ys = []
        plot()

    root = tk.Tk()
    root.title("ReDos Development UI")
    root.state("zoomed")

    # Frame to hold the regex Label and Text:
    frame_regex = tk.Frame(root)
    frame_regex.pack(padx=5, pady=5)

    label_regex = tk.Label(frame_regex, text="Regex: ", width=10)
    label_regex.pack(side=tk.LEFT)

    text_field_regex = tk.Text(frame_regex, height=1, width=150, padx=5, pady=5)
    text_field_regex.pack(side=tk.LEFT)

    # Frame to hold the input Label and Text:
    frame_input = tk.Frame(root)
    frame_input.pack()

    label_input = tk.Label(frame_input, text="Input: ", width=10)
    label_input.pack(side=tk.LEFT)

    text_field_input = tk.Text(frame_input, height=1, width=150, padx=5, pady=5)
    text_field_input.pack(side=tk.LEFT)

    # Frame to hold the "Add to Plot" and "Clear Plot" buttons:
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    button_add_to_plot = tk.Button(button_frame, text="Add to Plot", command=add_to_plot)
    button_add_to_plot.pack(side=tk.LEFT, padx=5)

    button_clear_plot = tk.Button(button_frame, text="Clear Plot", command=clear_plot)
    button_clear_plot.pack(side=tk.LEFT, padx=5)

    # The plot/image is displayed in a Label:
    image_label = tk.Label(root)
    image_label.pack(pady=5)

    # Start the Tkinter event loop:
    root.mainloop()


if __name__ == "__main__":
    main()
