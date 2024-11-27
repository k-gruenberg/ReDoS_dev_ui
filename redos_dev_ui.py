import tkinter as tk
import re
import timeit
import matplotlib.pyplot as plt
import sys

xs = []
ys = []

displayed_image = None  # has to be global due to garbage collection


# ToDo: add option for timeout
# ToDo: allow to choose regex engine
# ToDo: syntax highlighting / check regex for validity on typing, if invalid, show in red
# ToDo: What if user changes regex? => Don't allow user to change regex unless cleared.
# ToDo: show group matches
# ToDo: make plotted dots green on match and red on mismatch!


def main():
    def time_regex_on_input(regex, input) -> float:
        # Compile pattern (with flags as specified by the user):
        flags = 0
        if FLAG_ASCII.get():
            flags = flags | re.ASCII
        if FLAG_IGNORECASE.get():
            flags = flags | re.IGNORECASE
        if FLAG_MULTILINE.get():
            flags = flags | re.MULTILINE
        if FLAG_DOTALL.get():
            flags = flags | re.DOTALL
        print(f"Flags: {flags}")
        regex_pattern = re.compile(regex, flags=flags)

        # Time the compiled regex on the sample input given by the user:
        print(f"Function chosen: {function_chosen.get()}")
        if function_chosen.get() == "search()":
            # re.search() is the Python equivalent for JavaScript's RegExp.prototype.test().
            t = timeit.Timer(lambda: regex_pattern.search(input))
        elif function_chosen.get() == "match()":
            # re.match() only matches the *beginning* of strings!
            t = timeit.Timer(lambda: regex_pattern.match(input))
        elif function_chosen.get() == "fullmatch()":
            t = timeit.Timer(lambda: regex_pattern.fullmatch(input))
        else:
            print(f"Unknown function chosen: {function_chosen.get()}")
            sys.exit(1)
        iterations: int = int(text_field_iterations.get("1.0", tk.END))
        return (1_000_000_000 * t.timeit(number=iterations)) / iterations  # return result in nanoseconds per iteration

    def plot():
        global xs
        global ys
        global displayed_image

        plt.title(f"Regex: {text_field_regex.get('1.0', tk.END).rstrip('\r\n')}")
        plt.xlabel("Input length")
        plt.ylabel("Time [ns]")
        plt.scatter(xs, ys)

        destination = "tmp.png"
        plt.savefig(destination)
        plt.close('all')

        displayed_image = tk.PhotoImage(file=destination)
        image_label.config(image=displayed_image)

    def add_to_plot():
        global xs
        global ys
        regex = text_field_regex.get("1.0", tk.END).rstrip("\r\n")
        input = text_field_input.get("1.0", tk.END).rstrip("\r\n")
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

    # Frame to hold the regex Label, Text:
    frame_regex = tk.Frame(root)
    frame_regex.pack(padx=5, pady=5)

    label_regex = tk.Label(frame_regex, text="Regex: ", width=10)
    label_regex.pack(side=tk.LEFT)

    text_field_regex = tk.Text(frame_regex, height=1, width=150, padx=5, pady=5)
    text_field_regex.pack(side=tk.LEFT)

    # Frame to hold the regex options:
    frame_regex_options = tk.Frame(root)
    frame_regex_options.pack(padx=5, pady=5)

    # Regex Flags/Checkbuttons:
    FLAG_ASCII = tk.BooleanVar()
    FLAG_IGNORECASE = tk.BooleanVar()
    FLAG_MULTILINE = tk.BooleanVar()
    FLAG_DOTALL = tk.BooleanVar()
    checkbutton_ASCII = tk.Checkbutton(frame_regex_options, text="ASCII (?a)", variable=FLAG_ASCII)
    checkbutton_IGNORECASE = tk.Checkbutton(frame_regex_options, text="IGNORECASE (?i)", variable=FLAG_IGNORECASE)
    checkbutton_MULTILINE = tk.Checkbutton(frame_regex_options, text="MULTILINE (?m)", variable=FLAG_MULTILINE)
    checkbutton_DOTALL = tk.Checkbutton(frame_regex_options, text="DOTALL (?s)", variable=FLAG_DOTALL)
    checkbutton_ASCII.pack(side=tk.LEFT)
    checkbutton_IGNORECASE.pack(side=tk.LEFT)
    checkbutton_MULTILINE.pack(side=tk.LEFT)
    checkbutton_DOTALL.pack(side=tk.LEFT)
    
    # Regex Function/OptionMenu:
    label_function = tk.Label(frame_regex_options, text="Function: ", width=10)
    label_function.pack(side=tk.LEFT)
    function_choices = ['search()', 'match()', 'fullmatch()']
    function_chosen = tk.StringVar(root)
    function_chosen.set('search()')
    options_menu_function = tk.OptionMenu(frame_regex_options, function_chosen, *function_choices)
    options_menu_function.pack(side=tk.LEFT)

    # Frame to hold the input Label and Text:
    frame_input = tk.Frame(root)
    frame_input.pack(padx=5, pady=5)

    label_input = tk.Label(frame_input, text="Input: ", width=10)
    label_input.pack(side=tk.LEFT)

    text_field_input = tk.Text(frame_input, height=1, width=150, padx=5, pady=5)
    text_field_input.pack(side=tk.LEFT)

    # Frame to hold the "Add to Plot" and "Clear Plot" buttons:
    frame_buttons = tk.Frame(root)
    frame_buttons.pack(pady=5)

    button_add_to_plot = tk.Button(frame_buttons, text="Add to Plot", command=add_to_plot)
    button_add_to_plot.pack(side=tk.LEFT, padx=5)

    label_iterations = tk.Label(frame_buttons, text="Iterations: ", width=10)
    label_iterations.pack(side=tk.LEFT)

    text_field_iterations = tk.Text(frame_buttons, height=1, width=15, padx=5, pady=5)
    text_field_iterations.pack(side=tk.LEFT)
    text_field_iterations.delete(1.0, tk.END)
    text_field_iterations.insert(tk.END, "1_000_000")

    button_clear_plot = tk.Button(frame_buttons, text="Clear Plot", command=clear_plot)
    button_clear_plot.pack(side=tk.LEFT, padx=5)

    # The plot/image is displayed in a Label:
    image_label = tk.Label(root)
    image_label.pack(pady=5)

    # Start the Tkinter event loop:
    root.mainloop()


if __name__ == "__main__":
    main()
