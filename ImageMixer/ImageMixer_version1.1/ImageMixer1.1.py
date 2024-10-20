# ImageMixer
# version 1.1
# author: beijiu
# date: 2024/10/20

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import numpy as np
import tkinter.font as tkFont


# 声明全局变量
file_path = None
current_image = None  # 用于保存当前显示的图片

def select_file():
    global file_path, current_image
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg")])
    if file_path:
        label.config(text=file_path)
        load_image(file_path)

def load_image(file_path):
    global current_image
    img = Image.open(file_path)
    current_image = img  # 更新当前图片
    img_width, img_height = img.size
    max_width, max_height = 500, 500
    scale = min(max_width / img_width, max_height / img_height)
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)
    img = img.resize((new_width, new_height), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk
    image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def gilbert2d(width, height):
    coordinates = []
    if width >= height:
        generate2d(0, 0, width, 0, 0, height, coordinates)
    else:
        generate2d(0, 0, 0, height, width, 0, coordinates)
    return coordinates

def generate2d(x, y, ax, ay, bx, by, coordinates):
    w = abs(ax + ay)
    h = abs(bx + by)
    dax = 1 if ax > 0 else -1 if ax < 0 else 0
    day = 1 if ay > 0 else -1 if ay < 0 else 0
    dbx = 1 if bx > 0 else -1 if bx < 0 else 0
    dby = 1 if by > 0 else -1 if by < 0 else 0

    if h == 1:
        for i in range(w):
            coordinates.append((x, y))
            x += dax
            y += day
        return

    if w == 1:
        for i in range(h):
            coordinates.append((x, y))
            x += dbx
            y += dby
        return

    ax2 = ax // 2
    ay2 = ay // 2
    bx2 = bx // 2
    by2 = by // 2

    w2 = abs(ax2 + ay2)
    h2 = abs(bx2 + by2)

    if 2 * w > 3 * h:
        if w2 % 2 and w > 2:
            ax2 += dax
            ay2 += day

        generate2d(x, y, ax2, ay2, bx, by, coordinates)
        generate2d(x + ax2, y + ay2, ax - ax2, ay - ay2, bx, by, coordinates)

    else:
        if h2 % 2 and h > 2:
            bx2 += dbx
            by2 += dby

        generate2d(x, y, bx2, by2, ax2, ay2, coordinates)
        generate2d(x + bx2, y + by2, ax, ay, bx - bx2, by - by2, coordinates)
        generate2d(x + (ax - dax) + (bx2 - dbx), y + (ay - day) + (by2 - dby), -bx2, -by2, -(ax - ax2), -(ay - ay2), coordinates)


def process_image(image_path, is_encrypt=True):
    global file_path
    global current_image
    img = Image.open(image_path)
    width, height = img.size
    img_data = np.array(img)

    # 生成Gilbert曲线坐标
    curve = gilbert2d(width, height)
    offset = int((5 ** 0.5 - 1) / 2 * width * height)
    new_img_data = np.zeros_like(img_data)

    # 设置进度条的最大值
    progress_bar['maximum'] = width * height  # 第一次处理的最大值
    progress_bar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    key = key_entry.get()  # 获取用户输入的密钥
    if key != '':
        key = sum(bytearray(key.encode()))  # 将字符串密钥转换为一个整数
        key = key % (width * height)  # 确保密钥在坐标范围内
    
    # 按块处理图像 - 第一次加载进度条
    block_size = 200  # 定义每次处理的像素块大小
    for i in range(0, width * height, block_size):
        for j in range(block_size):
            if i + j >= width * height:
                break  # 避免越界
            old_pos = curve[i + j]

            if is_encrypt:
                if key != '':
                    offset ^= key
                new_pos = curve[(i + j + offset) % (width * height)]
                new_img_data[new_pos[1], new_pos[0]] = img_data[old_pos[1], old_pos[0]]
            else:
                if key != '':
                    offset ^= key
                new_pos = curve[(i + j + offset) % (width * height)]
                new_img_data[old_pos[1], old_pos[0]] = img_data[new_pos[1], new_pos[0]]

        # 更新进度条
        progress_bar['value'] = i + block_size
        root.update_idletasks()  # 刷新界面

    # 显示处理后的图像
    output_path = "encrypted_image.jpg" if is_encrypt else "decrypted_image.jpg"
    new_image = Image.fromarray(new_img_data)
    new_image.save(output_path, "JPEG", quality=95)
    show_processed_image(new_image)
    current_image = new_image  # 实际存储图像对象
    file_path = output_path  # 更新文件路径

    progress_bar.place_forget()  # 隐藏进度条

    
def encrypt_image(image_path):
    process_image(image_path, is_encrypt=True)

def decrypt_image(image_path):
    process_image(image_path, is_encrypt=False)

def show_processed_image(img):
    global current_image
    img_width, img_height = img.size
    max_width, max_height = 500, 500
    scale = min(max_width / img_width, max_height / img_height)
    new_width = int(img_width * scale)
    new_height = int(img_height * scale)
    img = img.resize((new_width, new_height), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk
    image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def imagemixer():
    global file_path
    if file_path is None:
        messagebox.showwarning("警告", "请先选择一张图片!")
        return
    encrypt_image(file_path)

def imagedecryptor():
    global file_path
    if file_path is None:
        messagebox.showwarning("警告", "请先选择一张图片!")
        return
    decrypt_image(file_path)

def save_current_image():
    global current_image
    if current_image is None:
        messagebox.showwarning("警告", "当前没有图片可保存!")
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".jpg", 
                                               filetypes=[("JPEG files", "*.jpg;*.jpeg")])
    if save_path:
        current_image.save(save_path)  # 从current_image保存
        messagebox.showinfo("成功", "图片已成功保存!")

# 创建主窗口
root = tk.Tk()
root.geometry("800x500+200+200")
root.title("图片混淆|ImageMixer")
root.configure(background="#1e293b")

# 创建一个分栏窗口
paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashwidth=5)
paned_window.pack(fill=tk.BOTH, expand=True)

# 创建左侧的框架
left_frame = tk.Frame(paned_window, width=300, bg="#2d3748")
paned_window.add(left_frame)

# 创建右侧的框架
right_frame = tk.Frame(paned_window, width=500, bg="#020617")
paned_window.add(right_frame)

# 设置字体
font_song = tkFont.Font(family="宋体", size=12)

# 创建一个标签来显示选中的文件路径
label = tk.Label(left_frame, text="尚未选择图片", bg="#2d3748", fg="#ffffff", font=font_song)
label.pack(pady=20)

# 创建一个标签用于显示“图片预底”
title_label = tk.Label(right_frame, text="巧妇难为无米之炊,愣着干嘛?上图啊", bg="#020617", fg="#ffffff", font=font_song)
title_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# 创建按钮
select_button = tk.Button(left_frame, text="选择图片", command=select_file, font=font_song)
select_button.pack(pady=10)

# 在左侧框架中添加一个标签和输入框
key_label = tk.Label(left_frame, text="输入密钥：", bg="#2d3748", fg="#ffffff", font=font_song)
key_label.pack(pady=10)

key_entry = tk.Entry(left_frame, font=font_song, show='*',width= 9)  # show='*' 隐藏输入字符
key_entry.pack(pady=10)

encrypt_button = tk.Button(left_frame, text=" 加  密 ", command=imagemixer, font=font_song)
encrypt_button.pack(pady=10)

decrypt_button = tk.Button(left_frame, text=" 解  密 ", command=imagedecryptor, font=font_song)
decrypt_button.pack(pady=10)

save_button = tk.Button(left_frame, text="保存图片", command=save_current_image, font=font_song)
save_button.pack(pady=10)

# 图像展示标签
image_label = tk.Label(right_frame)

# 创建进度条
progress_bar = ttk.Progressbar(right_frame, orient='horizontal', length=300, mode='determinate')

# 运行主循环
root.mainloop()
