import tkinter as tk
import tkinter.font as tkFont
from tkinter import colorchooser
from tkinter.filedialog import asksaveasfilename
from PIL import Image, ImageTk
import shutil

from qrcodegenerator import qr_maker, qr_basic, qr_styler

class App:
    def __init__(self, root):
        #setting title
        root.title("QR Code Generator")

        #setting window size
        width=910
        height=580
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2 - 50)
        root.geometry(alignstr)
        root.resizable(width=True, height=True)
        self.frames = {}
        self.mainframe = GeneratorPage(self)
        self.mainframe.pack()
        
class GeneratorPage(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self)
        self.controller = controller
        self.configure(padx=20, pady=20)
        
        self.error_correction = tk.StringVar(self, "H")
        self.version_var = tk.IntVar(value=5)
        self.box_var = tk.IntVar(value=10)
        self.border_var = tk.IntVar(value=4)
        
        self.colormask = tk.IntVar(value=0)
        self.moduledrawer = tk.IntVar(value=0)
        self.embed = tk.BooleanVar(value=False)
        
        self.fill_color = ((0, 0, 0), '#000000')
        self.back_color = ((255, 255, 255), '#ffffff')
        self.other_color = ((0, 0, 255), '#0000ff')
        self.path = "Select Image"

        # self.columnconfigure(0, weight=5)
        # self.columnconfigure(1, weight=1)
        # self.columnconfigure(1, weight=10)
        
        self.label = tk.Label(self, text="QR Code Generator")
        self.label.grid(row=0, column=0, columnspan=2)
        
        self.sample_qr = self.image_loader(qr_basic(qr_maker("QR Code Generator")))
        # print(self.sample_qr)
        self.sample = tk.Label(self, image=self.sample_qr)
        self.sample.grid(row=1, column=0, columnspan=2)
        
        self.sample_label = tk.Label(self, text="Value: QR Code Generator")
        self.sample_label.grid(row=2, column=0, columnspan=2)
        
        self.value = tk.StringVar()
        self.input_box = tk.Entry(self, width=50,
                            textvariable=self.value)
        self.input_box.grid(row=3, column=0, sticky="we")
        
        self.check = tk.IntVar(value=0)
        
        self.input_button = tk.Button(self, text="Enter", width=10, 
                                    command=self.update_sample)
        self.input_button.grid(row=3, column=1, sticky="we")
        
        self.check_menu = tk.Checkbutton(self, text="Extra styling options", pady=5,
                                        variable=self.check)
        self.check_menu.select()
        self.check_menu.grid(row=4, column=0)
        
        self.save_button = tk.Button(self, text="Save", width=10,
                                    command=self.saveqr)
        self.save_button.grid(row=4, column=1, sticky="we")
        
        self.menu_frame = tk.Frame(self, width=485, height=550, pady=35)
        self.menu_frame.grid(row=0, column=2, rowspan=5, sticky="nsew")
        self.menu_frame.grid_propagate(False)
        self.draw_menu()
    
    def update_sample(self):
        qr_value = self.value.get()

        if self.check.get() == 0:
            qr = qr_maker(qr_value)
            temp = qr_basic(qr)
        else:
            qr = qr_maker(qr_value, self.version_var.get(), self.error_correction.get(), 
                            self.box_var.get(), self.border_var.get())
            temp = qr_styler(qr, path=self.path,
                            fill=self.fill_color[0] ,back=self.back_color[0], other=self.other_color[0],
                            colormask=self.colormask.get(), moduledrawer=self.moduledrawer.get(), 
                            embed=self.embed.get())
        
        self.sample_qr = self.image_loader(temp)
        self.sample["image"] = self.sample_qr
        self.sample_label["text"] = "Value: " + qr_value
    
    def image_loader(self, qr_img):
        # img = Image(qr_img)
        size = 400
        
        self.new_img = qr_img.resize((size, size), resample=0)
        tk_img = ImageTk.PhotoImage(self.new_img)
        return tk_img
    
    def saveqr(self):
        path = asksaveasfilename(initialfile = 'Untitled.png',
        defaultextension=".png",filetypes=[("Image file","*.png *.jpeg"),("All Files","*.*")])

        self.new_img.save(path)
    
    def draw_menu(self):
        self.option_title = tk.Label(self.menu_frame, text="Options")
        self.option_title.grid(row=0, column=0, columnspan=3, sticky="n")
        
        
        ec_options = {  "Very High Correction":"H",
                        "High Correction":"Q",
                        "Medium Correction":"M",
                        "Low Correction":"L"}
        for (num, (text, value)) in enumerate(ec_options.items()):
            tk.Radiobutton(self.menu_frame, text=text, value=value,
                            variable=self.error_correction,
                            padx=30
                            ).grid(row=num+1, column=0, sticky="nw")
        
        self.version_label = tk.Label(self.menu_frame, text="QR Code Size: ", padx=30)
        self.version_label.grid(row=1, column=1, sticky="nw")
        
        self.version_size = tk.Spinbox(self.menu_frame, width=3,
                                    from_=1, to=40, increment=1,
                                    textvariable=self.version_var)
        
        self.version_size.grid(row=1, column=2, sticky="nw")
        
        self.box_label = tk.Label(self.menu_frame, text="Box Size: ", padx=30)
        self.box_label.grid(row=2, column=1, sticky="nw")
        
        
        self.box_size = tk.Spinbox(self.menu_frame, width=3,
                                    from_=1, to=40, increment=1,
                                    textvariable=self.box_var)
        
        self.box_size.grid(row=2, column=2, sticky="nw")
        
        self.border_label = tk.Label(self.menu_frame, text="Border Size: ", padx=30)
        self.border_label.grid(row=3, column=1, sticky="nw")
        
        self.border_size = tk.Spinbox(self.menu_frame, width=3, 
                                    from_=4, to=100, increment=1,
                                    textvariable=self.border_var)
        
        self.border_size.grid(row=3, column=2, sticky="nw")
        
        self.colormask_title = tk.Label(self.menu_frame, text="Colormask:", padx=30, pady=5)
        self.colormask_title.grid(row=5, column=0, sticky="nw")
        
        colormask_options = {"SolidFillColorMask":0,
                            "RadialGradiantColorMask":1,
                            "SquareGradiantColorMask":2,
                            "HorizontalGradiantColorMask":3,
                            "VerticalGradiantColorMask":4,
                            "ImageColorMask":5}
        for (num, (text, value)) in enumerate(colormask_options.items()):
            tk.Radiobutton(self.menu_frame, text=text, value=value,
                            variable=self.colormask,
                            padx=30
                            ).grid(row=num+6, column=0, sticky="nw")
            
        self.moduledrawer_title = tk.Label(self.menu_frame, text="Module Drawer:", padx=30, pady=5)
        self.moduledrawer_title.grid(row=5, column=1, columnspan=2, sticky="nw")
        
        moduledrawer_options = {"SquareModuleDrawer":0,
                                "GappedSquareModuleDrawer":1,
                                "CircleModuleDrawer":2,
                                "RoundedModuleDrawer":3,
                                "VerticalBarsDrawer":4,
                                "HorizontalBarsDrawer":5}
        for (num, (text, value)) in enumerate(moduledrawer_options.items()):
            tk.Radiobutton(self.menu_frame, text=text, value=value,
                            variable=self.moduledrawer,
                            padx=30).grid(row=num+6, column=1, columnspan=2, sticky="nw")
        
        self.colormenu = tk.Frame(self.menu_frame, width=485, height=100, padx=30, pady=10)
        self.colormenu.grid(row=12, column=0, columnspan=3)
        self.colormenu.grid_propagate(False)
        
        self.draw_colormenu()
        

    
    def draw_colormenu(self):
        self.fill_color_button = tk.Button(self.colormenu)
        self.fill_color_button.config(bg=self.fill_color[1], width=1, height=1, padx=5, command=self.update_fill_color)
        self.fill_color_button.grid(row=0, column=0, sticky="w")
        
        self.fill_color_label = tk.Label(self.colormenu, text="Fill Colour   ")
        self.fill_color_label.grid(row=0, column=1, sticky="w")
        
        self.back_color_button = tk.Button(self.colormenu)
        self.back_color_button.config(bg=self.back_color[1], width=1, height=1, padx=5, command=self.update_back_color)
        self.back_color_button.grid(row=0, column=2, sticky="w")
        
        self.back_color_label = tk.Label(self.colormenu, text="Background Colour   ")
        self.back_color_label.grid(row=0, column=3, sticky="w")
        
        self.other_color_button = tk.Button(self.colormenu)
        self.other_color_button.config(bg=self.other_color[1], width=1, height=1, padx=5, command=self.update_other_color)
        self.other_color_button.grid(row=0, column=4, sticky="w")
        
        self.other_color_label = tk.Label(self.colormenu, text="Other Colour   ")
        self.other_color_label.grid(row=0, column=5, sticky="w")
        
        self.image_check = tk.Checkbutton(self.colormenu, variable=self.embed)
        self.image_check.grid(row=1, column=0, sticky="w")
        
        self.image_label = tk.Label(self.colormenu, text="Insert Image")
        self.image_label.grid(row=1, column=1, columnspan=3, sticky="w")
        
        self.path_info = tk.StringVar(value=self.path)
        self.image_path = tk.Entry(self.colormenu, textvariable=self.path_info)
        self.image_path.grid(row=2, column=0, columnspan=4, sticky="we")
        
        self.image_browse = tk.Button(self.colormenu, text="Browse")
        self.image_browse.grid(row=2, column=4, columnspan=2, sticky="w")
    
    def update_fill_color(self):
        self.fill_color = colorchooser.askcolor(initialcolor=self.fill_color[1])
        self.fill_color_button.config(bg=self.fill_color[1])

    def update_back_color(self):
        self.back_color = colorchooser.askcolor(initialcolor=self.back_color[1])
        self.back_color_button.config(bg=self.back_color[1])
        
    def update_other_color(self):
        self.other_color = colorchooser.askcolor(initialcolor=self.other_color[1])
        self.other_color_button.config(bg=self.other_color[1])
        print(self.other_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()