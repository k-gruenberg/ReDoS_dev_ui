import tkinter as tk
import re
import timeit
import matplotlib.pyplot as plt
import sys
from typing import Tuple, Callable

xs = []  # scatter point x coordinates
ys = []  # scatter point y coordinates
cs = []  # scatter point colors

displayed_image = None  # has to be global due to garbage collection


# ToDo: add option for timeout
# ToDo: allow to choose regex engine
# ToDo: show group matches


def main():
    def time_regex_on_input(regex: str, input: str) -> Tuple[float, bool]:
        """
        Parameters:
            regex: a string representing an un-compiled regular expression
            input: the sample input string to test

        Returns:
            A tuple, consisting of:
            1. the average number of nanoseconds each iteration took,
            2. a boolean indicating whether the input matched the regex or not.
        """

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
            f: Callable = lambda: regex_pattern.search(input)
        elif function_chosen.get() == "match()":
            # re.match() only matches the *beginning* of strings!
            f: Callable = lambda: regex_pattern.match(input)
        elif function_chosen.get() == "fullmatch()":
            f: Callable = lambda: regex_pattern.fullmatch(input)
        else:
            print(f"Unknown function chosen: {function_chosen.get()}")
            sys.exit(1)
        t = timeit.Timer(f)
        iterations: int = int(text_field_iterations.get("1.0", tk.END))
        avg_time_in_ns: float = (1_000_000_000 * t.timeit(number=iterations)) / iterations  # nanoseconds per iteration
        return avg_time_in_ns, (f() is not None)

    def plot(title=None):
        global xs
        global ys
        global cs
        global displayed_image

        plt.title(f"Regex: {text_field_regex.get('1.0', tk.END).rstrip('\r\n')}" if title is None else title)
        plt.xlabel("Input length")
        plt.ylabel("Time [ns]")
        plt.scatter(xs, ys, c=cs)

        destination = "tmp.png"
        plt.savefig(destination)
        plt.close('all')

        displayed_image = tk.PhotoImage(file=destination)
        image_label.config(image=displayed_image)

    def add_to_plot():
        global xs
        global ys
        global cs

        # Lock regex input text field:
        text_field_regex.configure(state="disabled")

        regex: str = text_field_regex.get("1.0", tk.END).rstrip("\r\n")
        input: str = text_field_input.get("1.0", tk.END).rstrip("\r\n")
        x: int = len(input)
        y, match = time_regex_on_input(regex=regex, input=input)
        xs.append(x)
        ys.append(y)
        cs.append('g' if match else 'r')
        plot()

    def clear_plot():
        global xs
        global ys
        global cs

        # Unlock regex input text field:
        text_field_regex.configure(state="normal")

        # Clear plot:
        xs = []
        ys = []
        cs = []
        plot(title="")

    def on_text_field_regex_change(_event):
        # Check if the regex was actually modified:
        if text_field_regex.edit_modified():
            # 1. Check if the regex is valid, if not color in dark red.
            # 2. Highlight all repetition operators ("+" and "*") in light red.
            try:
                regex: str = text_field_regex.get("1.0", tk.END).rstrip("\r\n")
                re.compile(regex)
                # Regex is valid:
                text_field_regex.tag_delete("invalid")
                # Highlight all repetition operators ("+" and "*")
                text_field_regex.tag_delete("operator")
                text_field_regex.tag_config("operator", foreground="red")
                for i in range(len(regex)):
                    char = regex[i]
                    if char in ["+", "*"]:
                        index = f"1.{i}"
                        text_field_regex.tag_add("operator", index, index + "+1c")
            except re.error:
                # Regex is invalid:
                text_field_regex.tag_config("invalid", foreground="red4")
                text_field_regex.tag_add("invalid", f"1.0", tk.END)

            # Reset the modified flag to ensure the event is triggered again:
            text_field_regex.edit_modified(False)

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
    text_field_regex.bind("<<Modified>>", on_text_field_regex_change)

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
