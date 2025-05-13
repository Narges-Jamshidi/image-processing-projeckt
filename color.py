import os
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from sklearn.cluster import KMeans

# import matplotlib.pyplot as plt


COLOR_DB_PATH = "color_database"


def load_color_database():
    color_data = {}
    for file in os.listdir(COLOR_DB_PATH):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
            color_name = os.path.splitext(file)[0]
            img_path = os.path.join(COLOR_DB_PATH, file)
            img = Image.open(img_path).resize((50, 50))
            avg_color = np.array(img).reshape(-1, 3).mean(axis=0)
            color_data[color_name] = (avg_color, img_path)
    return color_data


def extract_dominant_colors(image_path, k=4):
    img = Image.open(image_path)
    img = img.resize((200, 200))
    img_np = np.array(img)
    img_np = img_np.reshape(-1, 3)

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(img_np)
    colors = kmeans.cluster_centers_
    return colors.astype(int)


def match_colors(dominant_colors, color_database):
    matched = []
    for color in dominant_colors:
        min_dist = float('inf')
        match_name, match_img = None, None
        for name, (ref_color, img_path) in color_database.items():
            dist = np.linalg.norm(color - ref_color)
            if dist < min_dist:
                min_dist = dist
                match_name = name
                match_img = img_path
        matched.append((match_name, match_img))
    return matched


def process_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return

    for widget in result_frame.winfo_children():
        widget.destroy()

    dominant_colors = extract_dominant_colors(file_path)
    matched_colors = match_colors(dominant_colors, color_database)


    img = Image.open(file_path)
    img = img.resize((200, 200))
    img_tk = ImageTk.PhotoImage(img)
    Label(result_frame, text="Input Image").grid(row=0, column=0, pady=5)
    Label(result_frame, image=img_tk).grid(row=1, column=0, pady=5)
    result_frame.image = img_tk


    Label(result_frame, text="Detected Colors").grid(row=0, column=1, columnspan=4)
    for idx, (name, img_path) in enumerate(matched_colors):
        Label(result_frame, text=name).grid(row=1, column=idx + 1)
        color_img = Image.open(img_path).resize((50, 50))
        color_img_tk = ImageTk.PhotoImage(color_img)
        label = Label(result_frame, image=color_img_tk)
        label.image = color_img_tk
        label.grid(row=2, column=idx + 1, padx=5, pady=5)







root = Tk()
root.title("Color Detector")
root.geometry("800x400")

color_database = load_color_database()

upload_btn = Button(root, text="آپلود عکس", command=process_image, font=("Arial", 14))
upload_btn.pack(pady=20)

result_frame = Frame(root)
result_frame.pack()

root.mainloop()
