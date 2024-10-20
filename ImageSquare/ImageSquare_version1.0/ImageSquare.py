# ImageSquare
# version 1.0
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
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
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

def square_image(file_path):
    global current_image
    img = Image.open(file_path)
    width, height = img.size
    img_data = np.array(img)
    new_img_data = np.zeros_like(img_data)  # 创建一个与原图同样大小的数组

    while True:
        try:
            block_size = int(block_size_entry.get())
            break  # 如果转换成功，跳出循环
        except ValueError:
            messagebox.showerror("错误", "请输入有效的正整数！")
            return

     # 设置进度条的最大值
    progress_bar['maximum'] = (width // block_size) * (height // block_size)  # 计算块数
    progress_bar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            # 计算当前块的右下角
            block_end_i = min(i + block_size, height)
            block_end_j = min(j + block_size, width)

            # 获取当前块的代表值，这里选择左上角作为代表值
            representative_value = img_data[i, j]

            # 将当前块内所有像素设置为代表值
            for x in range(i, block_end_i):
                for y in range(j, block_end_j):
                    new_img_data[x, y] = representative_value

            # 更新进度条
            progress_bar['value'] += 1
            root.update_idletasks()  # 刷新界面

    # 显示处理后的图像
    if file_path.lower().endswith('.png'):
        output_path = "Square_Image.png"
        output_style = "PNG"
    else:
        output_path = "Square_Image.jpg"
        output_style = "JPEG"
    new_image = Image.fromarray(new_img_data)
    new_image.save(output_path, output_style, quality=95)
    show_processed_image(new_image)
    current_image = new_image  # 实际存储图像对象
    file_path = output_path  # 更新文件路径

    progress_bar.place_forget()  # 隐藏进度条


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
    square_image(file_path)

def save_current_image():
    global current_image
    if current_image is None:
        messagebox.showwarning("警告", "当前没有图片可保存!")
        return
    try:
        save_path = filedialog.asksaveasfilename(defaultextension=".png",  # 默认扩展为PNG
                                                   filetypes=[
                                                       ("JPEG files", "*.jpg;*.jpeg"),
                                                       ("PNG files", "*.png")
                                                   ])
        if save_path:
            # 根据用户选择的扩展名决定保存的格式
            if save_path.lower().endswith('.png'):
                current_image.save(save_path, format='PNG')  # 如果是PNG,保留透明度
            else:
                # 如果是JPEG,则转换为RGB以移除透明度
                rgb_image = current_image.convert("RGB")
                rgb_image.save(save_path, format='JPEG')  # 保存为JPEG格式
            messagebox.showinfo("成功", "图片已成功保存!")
    except Exception as e:
        messagebox.showerror("错误", f"保存图片时出错: {e}")


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
block_size_label = tk.Label(left_frame, text="输入倍数", bg="#2d3748", fg="#ffffff", font=font_song)
block_size_label.pack(pady=10)

block_size_entry = tk.Entry(left_frame, font=font_song, show='*',width= 9)  # show='*' 隐藏输入字符
block_size_entry.pack(pady=10)

encrypt_button = tk.Button(left_frame, text=" 劣  化 ", command=imagemixer, font=font_song)
encrypt_button.pack(pady=10)

save_button = tk.Button(left_frame, text="保存图片", command=save_current_image, font=font_song)
save_button.pack(pady=10)

# 图像展示标签
image_label = tk.Label(right_frame)

# 创建进度条
progress_bar = ttk.Progressbar(right_frame, orient='horizontal', length=300, mode='determinate')

# 运行主循环
root.mainloop()
