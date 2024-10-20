# ImageCompress
# version: 1.0
# author: beijiu
# date: 2024/10/20


import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

# 创建主窗口
root = tk.Tk()
root.geometry("400x300")
root.title("图片压缩工具")

def compress_image():
    # 选择文件
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg")])
    if not file_path:
        return

    # 打开图片
    img = Image.open(file_path)

    # 获取压缩质量
    try:
        quality = int(quality_entry.get())  # 从输入框获取质量值
        if quality < 1 or quality > 100:
            messagebox.showwarning("警告", "质量值必须在1到100之间!")
            return
    except ValueError:
        messagebox.showwarning("警告", "请输入有效的整数质量值!")
        return

    # 选择保存路径
    save_path = filedialog.asksaveasfilename(defaultextension=".jpg", 
                                               filetypes=[("JPEG files", "*.jpg;*.jpeg")])
    if save_path:
        img.save(save_path, "JPEG", quality=quality)  # 保存为JPEG格式，包含质量参数
        messagebox.showinfo("成功", "图片已成功压缩并保存!")

# 创建输入框和按钮
quality_label = tk.Label(root, text="压缩质量（1-100）：")
quality_label.pack()

quality_entry = tk.Entry(root, width=10)
quality_entry.pack()

compress_button = tk.Button(root, text="选择图片并压缩", command=compress_image)
compress_button.pack()

# 运行主循环
root.mainloop()
