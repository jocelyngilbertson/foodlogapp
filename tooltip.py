import tkinter as tk

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self):
        "Display text in tooltip window"
        self.x, self.y, _, _ = self.widget.bbox("insert")
        self.x += self.widget.winfo_rootx() + 25
        self.y += self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (self.x, self.y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tooltip Test")
        self.entry = tk.Entry(self)
        self.entry.pack(padx=10, pady=10)

        # Create a tooltip for the first Entry widget
        self.tooltip = Tooltip(self.entry, "Enter your text here")

        # Bind focus in and focus out events
        self.entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.entry.bind('<FocusOut>', self.on_entry_focus_out)
        self.entry.bind('<Key>', self.on_entry_key)

        # Create a second Entry widget just we can test losing focus
        # on the first entry widget
        self.entry2 = tk.Entry(self)
        self.entry2.pack(padx=10, pady=10)

    def on_entry_focus_in(self, event):
        if self.entry.get().strip() == "":
            self.tooltip.showtip()

    def on_entry_focus_out(self, event):
        self.tooltip.hidetip()

    def on_entry_key(self, event):
        self.tooltip.hidetip()

    def on_entry_key_up(self, event):
        if self.entry.get().strip() == "":
            self.tooltip.showtip()

    def on_entry_key(self, event):
        self.tooltip.hidetip()
        self.on_entry_key_up(event)

if __name__ == "__main__":
    app = App()
    app.mainloop()
