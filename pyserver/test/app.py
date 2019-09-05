import tkinter.filedialog as tkFiledDialog
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from trans_interior import TransInterior


class MainWindow(object):
    def __init__(self):
        root = tk.Tk()
        root.geometry('400x400')
        self.frame1 = tk.Frame(root)
        self.frame1.pack(side=TOP)
        self.frame_img = tk.Frame(root)
        self.frame_img.pack(side=TOP)

        self.trans_goods = TransInterior()
        self.imgs = {}
        self.label_button = []

        self.fType = [("画像ファイル", "*.jpg"), ("画像ファイル", "*.png")]
        self.file_name = None
        self.img = None

        # loader
        self.load_button = tk.Button(self.frame1, text="load file", command=self.load_file)
        self.load_button.grid(row=0, column=4)

        self.trans_button = tk.Button(self.frame1, text="translation", command=self.print_right_image)
        self.trans_button.grid(row=0, column=5)

        root.mainloop()

    def callback(self, event):
        print(event.x)
        print(event.y)

    def destroy_child(self, frame):
        children = frame.winfo_children()
        for child in children:
            child.destroy()

    def print_left_image(self):
        self.img = Image.open(self.file_name)
        h, w = self.img.size
        self.destroy_child(self.frame_img)
        canvas = tk.Canvas(self.frame_img, width=h, height=w)
        canvas.place(x=100, y=350)
        self.imgs[0] = ImageTk.PhotoImage(self.img)
        canvas.create_image(3, 3, image=self.imgs[0], anchor=tk.NW)
        canvas.grid(row=0, column=0)
        canvas.bind("<1>", self.print_right_image)
        self.print_center_image()

    def print_center_image(self):
        self.img_tr = self.trans_goods.segmentation(self.img)
        h, w = self.img.size
        img_tr = self.img_tr.resize((h, w), Image.NEAREST)
        canvas = tk.Canvas(self.frame_img, width=h, height=w)
        canvas.place(x=300, y=350)
        self.imgs[1] = ImageTk.PhotoImage(img_tr)
        canvas.create_image(3, 3, image=self.imgs[1], anchor=tk.NW)
        canvas.grid(row=0, column=1)

    def print_right_image(self, event):
        if self.file_name is None:
            return
        # img_tr = self.trans_goods.segmentation(self.img)
        h, w = self.img.size

        img_tr = self.img_tr.resize((h, w), Image.NEAREST)
        img_trans = self.trans_goods.change_material(self.img, event.x, event.y, img_tr)

        canvas = tk.Canvas(self.frame_img, width=h, height=w)
        canvas.place(x=300, y=350)
        self.imgs[2] = ImageTk.PhotoImage(img_trans)
        canvas.create_image(3, 3, image=self.imgs[2], anchor=tk.NW)
        canvas.grid(row=0, column=2)

    def load_file(self):
        self.imgs.clear()
        self.file_name = tkFiledDialog.askopenfilename(filetype=self.fType)
        self.print_left_image()


if __name__ == "__main__":
    MainWindow()
