import tkinter as Tk
import customtkinter as CTk
from PIL import Image
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
import password


class App(CTk.CTk):

    def __init__(self):
        super().__init__()

        self.geometry('460x420')
        self.title('Password generator')
        self.resizable(False, False)

        self.logo = CTk.CTkImage(dark_image=Image.open('password-generator/ui/img.png'), size=(460, 150))
        self.logo_label = CTk.CTkLabel(master=self, text='', image=self.logo)
        self.logo_label.grid(row=0, column=0)

        self.password_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.password_frame.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky='nsew')

        self.entry_password = CTk.CTkEntry(master=self.password_frame, width=300)
        self.entry_password.grid(row=0, column=0, padx=(0, 20))

        self.btn_generate = CTk.CTkButton(master=self.password_frame, text='Generate', width=100,
                                          command=self.set_password)
        self.btn_generate.grid(row=0, column=1)

        self.btn_copy = CTk.CTkButton(master=self.password_frame, text='Copy', width=100,
                                      command=self.copy_password)
        self.btn_copy.grid(row=1, column=1, sticky='n', pady=(5, 0))

        self.entropy = CTk.CTkLabel(master=self.password_frame, text='', width=100, fg_color='transparent')
        self.entropy.grid(row=1, column=0, sticky='e', padx=(0, 20))

        self.strength_of_pass = CTk.CTkLabel(master=self.password_frame, text='', width=100, fg_color='transparent')
        self.strength_of_pass.grid(row=1, column=0, sticky='w', padx=(0, 0))

        self.options_frame = CTk.CTkFrame(master=self)
        self.options_frame.grid(row=2, column=0, padx=(20, 20), pady=(20, 0), sticky='nsew')

        self.password_length_slider = CTk.CTkSlider(master=self.options_frame, from_=0, to=50, number_of_steps=50,
                                                    command=self.slider_events)
        self.password_length_slider.grid(row=1, column=0, columnspan=3, pady=(20, 20), sticky='ew')

        self.password_length_entry = CTk.CTkEntry(master=self.options_frame, width=50)
        self.password_length_entry.grid(row=1, column=3, padx=(20, 10), sticky='we')
        self.password_length_entry.bind('<KeyRelease>', lambda event: self.update_slider(
            self.password_length_slider, self.password_length_entry))

        self.cb_lower_var = Tk.StringVar()
        self.cb_lower = CTk.CTkCheckBox(master=self.options_frame, text='a-z', variable=self.cb_lower_var,
                                        onvalue=ascii_lowercase, offvalue='')
        self.cb_lower.grid(row=2, column=0, padx=10)

        self.cb_upper_var = Tk.StringVar()
        self.cb_upper = CTk.CTkCheckBox(master=self.options_frame, text='A-Z', variable=self.cb_upper_var,
                                        onvalue=ascii_uppercase, offvalue='')
        self.cb_upper.grid(row=2, column=1)

        self.cb_digits_var = Tk.StringVar()
        self.cb_digits = CTk.CTkCheckBox(master=self.options_frame, text='0-9', variable=self.cb_digits_var,
                                         onvalue=digits, offvalue='')
        self.cb_digits.grid(row=2, column=2)

        self.cb_symbols_var = Tk.StringVar()
        self.cb_symbol = CTk.CTkCheckBox(master=self.options_frame, text='@#$%', variable=self.cb_symbols_var,
                                         onvalue=punctuation, offvalue='')
        self.cb_symbol.grid(row=2, column=3)

        self.appearance_mode_options_menu = CTk.CTkOptionMenu(master=self.options_frame,
                                                              values=['Light', 'Dark', 'System'],
                                                              command=self.change_appearance_mode_event)
        self.appearance_mode_options_menu.grid(row=3, column=0, columnspan=4, pady=(10, 10))

        self.appearance_mode_options_menu.set('System')

        self.default_options()

    def default_options(self) -> None:
        self.password_length_slider.set(12)
        self.password_length_entry.insert(0, '12')
        self.cb_lower.select()
        self.cb_upper.select()

    def change_appearance_mode_event(self, new_appearance_mode: str) -> None:
        CTk.set_appearance_mode(new_appearance_mode)

    def copy_password(self) -> None:
        self.clipboard_clear()
        self.clipboard_append(self.entry_password.get())

    def slider_events(self, value: str) -> None:
        self.password_length_entry.delete(0, 'end')
        self.password_length_entry.insert(0, int(value))

    def update_slider(self, slider: CTk.CTkSlider, entry: CTk.CTkEntry) -> None:
        try:
            value = int(entry.get())
        except ValueError:
            value = 0
        slider.set(value)

    def get_characters(self) -> str:
        chars = ''.join(self.cb_digits_var.get() + self.cb_lower_var.get()
                        + self.cb_upper_var.get() + self.cb_symbols_var.get())
        return chars

    def set_password(self) -> None:
        self.entry_password.delete(0, 'end')
        self.entry_password.insert(0, password.new_password(length=int(self.password_length_slider.get()),
                                                            chars=self.get_characters()))
        self.set_entropy()
        self.set_complexity()

    def set_entropy(self) -> str:
        length = int(self.password_length_slider.get())
        char_num = self.get_character_number()

        self.entropy.configure(text=f'Entropy: {password.get_entropy(length, char_num)} bit')

    def get_character_number(self) -> int:
        char_counter = sum([
            10 if self.cb_digits.get() else 0,
            26 if self.cb_lower.get() else 0,
            26 if self.cb_upper.get() else 0,
            32 if self.cb_symbol.get() else 0,
        ])

        return char_counter

    def set_complexity(self) -> None:
        length = int(self.password_length_slider.get())
        char_num = self.get_character_number()

        for complexity in password.PasswordComplexity:
            if password.get_entropy(length, char_num) >= complexity.value:
                self.strength_of_pass.configure(text=f'Strength: {complexity.name}')


if __name__ == '__main__':
    app = App()
    app.mainloop()
