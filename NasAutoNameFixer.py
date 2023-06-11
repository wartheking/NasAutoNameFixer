import os
import re
import glob
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def rename_files(folder_path, show_name, season, folder_entry, name_entry, season_entry):
    # 获取文件列表
    file_list = os.listdir(folder_path)

    sorted_file_list = []
    for file_name in file_list:
        # 从文件名的末尾开始向前查找数字作为集数
        episode_match = re.search(r"\D(\d+)\D*$", file_name[::-1])
        if episode_match:
            episode = int(episode_match.group(1)[::-1])
            # 将文件名中的数字提取出来作为集数，将季数转换为英文形式
            season_prefix = "S" + season.zfill(2)
            new_file_name = "{}{}E{}".format(show_name, season_prefix, episode)
            sorted_file_list.append((file_name, episode, new_file_name))

    # 输出排序后的文件列表，并重命名文件
    for file_name, _, new_file_name in sorted(sorted_file_list, key=lambda x: x[1]):
        old_path = os.path.join(folder_path, file_name)
        extension = os.path.splitext(file_name)[1]  # 获取原始文件的后缀
        new_path = os.path.join(folder_path, new_file_name + extension)
        print("Renaming:", old_path, "to", new_path)
        # 执行文件重命名操作
        os.rename(old_path, new_path)

    messagebox.showinfo("处理完成", "文件重命名完成！")
    
    # 清空输入框内容
    folder_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    season_entry.delete(0, tk.END)

def select_folder():
    def handle_select_folder():
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_entry.delete(0, tk.END)
            folder_entry.insert(tk.END, folder_path)
            
            # 提取文件夹名称作为默认电视剧名称，并去掉"中文版"
            show_name = os.path.basename(folder_path)
            show_name = show_name.replace("中文版", "")
            name_entry.delete(0, tk.END)
            name_entry.insert(tk.END, show_name)

    def handle_rename_files():
        folder_path = folder_entry.get()
        show_name = name_entry.get()
        season = season_entry.get()
        if folder_path and show_name and season:
            rename_files(folder_path, show_name, season, folder_entry, name_entry, season_entry)
        else:
            messagebox.showwarning("输入错误", "请填写完整的信息！")

    root = tk.Tk()
    root.title("文件重命名工具")

    folder_label = tk.Label(root, text="选择文件夹：")
    folder_label.pack()

    folder_entry = tk.Entry(root, width=50)
    folder_entry.pack()

    select_button = tk.Button(root, text="选择", command=handle_select_folder)
    select_button.pack()

    name_label = tk.Label(root, text="电视剧名称：")
    name_label.pack()

    name_entry = tk.Entry(root, width=50)
    name_entry.pack()

    season_label = tk.Label(root, text="第几季：")
    season_label.pack()
    
    season_entry = tk.Entry(root, width=50)
    season_entry.pack()
    
    rename_button = tk.Button(root, text="开始重命名", command=handle_rename_files)
    rename_button.pack()
    
    root.mainloop()

select_folder()
