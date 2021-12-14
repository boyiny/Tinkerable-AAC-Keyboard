import tkinter as tk
from tkinter import ttk
from tkinter.constants import DISABLED

class View(tk.Tk):

    PAD = 10
    MAX_BUTTON_PER_ROW = 4

    button_captions = [
        'C', '+/-', '%', '/',
        7, 8, 9, '*',
        4, 5, 6, '-',
        1, 2, 3, '+',
        0, '.', '='
    ]

    def __init__(self, controller):
        super().__init__()
        self.title("Calculator")
        self.controller = controller
        self.value_var = tk.StringVar()

        self._make_main_frame()
        self._make_entry()
        self._make_buttons()
    
    def main(self):
        self.mainloop()

    def _make_main_frame(self):
        self.main_frm = ttk.Frame(self)
        self.main_frm.pack(padx=self.PAD, pady=self.PAD)

    def _make_entry(self):
        ent = ttk.Entry(
            self.main_frm, justify='right', textvariable=self.value_var,
            state=DISABLED)
        ent.pack(fill='x')

    def _make_buttons(self):
        outer_frm = ttk.Frame(self.main_frm)
        outer_frm.pack()

        frm = ttk.Frame(outer_frm)
        frm.pack()

        buttons_in_row = 0

        for caption in self.button_captions:
            if buttons_in_row == self.MAX_BUTTON_PER_ROW:
                frm = ttk.Frame(outer_frm)
                frm.pack()
                buttons_in_row = 0

            btn = ttk.Button(frm, text=caption, command=(lambda button=caption: self.controller.on_button_click(button)))
            btn.pack(side='left')

            buttons_in_row += 1
