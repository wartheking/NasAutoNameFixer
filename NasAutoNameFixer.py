import os
import re
import glob
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

def rename_files(folder_path, show_name, season, resolution, year, folder_entry, name_entry, season_entry, resolution_combo, year_combo):
    # 获取文件列表
    file_list = os.listdir(folder_path)
    if year != "":
        year = "." + str(year)
    if resolution != "":
        if resolution == "4k":
            resolution = "2160p"
        elif resolution == "2k":
            resolution = "1440p"
        resolution = "." + resolution
    sorted_file_list = []

    #伪AI，往前找，找到数字不一样的那个，默认是集数
    forLoopCount = 0
    while True:
        successGetEpisodeMatchStart = True
        episodeDic = {}
        for file_name in file_list:
            filepureName = os.path.splitext(file_name)[0]
            print(filepureName)
            episode_match = re.search(r"\d+", filepureName)
            for i in range(forLoopCount):
                episode_match = re.search(r"\d+", filepureName[episode_match.end():])
            if episode_match:
                episode = int(episode_match.group(0))
                print(episode)
                if episodeDic.__contains__(episode):
                    episodeDic[episode] += 1
                else:
                    episodeDic[episode] = 1
            else:
                messagebox.showinfo("处理失败", "电视剧存在有相同集数！")
                # 清空输入框内容
                folder_entry.delete(0, tk.END)
                name_entry.delete(0, tk.END)
                season_entry.delete(0, tk.END)
                resolution_combo.set("")  # 清空分辨率下拉框选择
                year_combo.set("")  # 清空年份下拉框选择
                return
        for ed in episodeDic:
            if episodeDic[ed] > 1:
                print(ed)
                print(False)
                successGetEpisodeMatchStart = False
        if successGetEpisodeMatchStart:
            break
        else:
            forLoopCount += 1
            print(forLoopCount)

    for file_name in file_list:
        filepureName = os.path.splitext(file_name)[0]
        # 从文件名的末尾开始向前查找数字作为集数
        episode_match = re.search(r"\d+", filepureName)
        for i in range(forLoopCount):
            episode_match = re.search(r"\d+", filepureName[episode_match.end():])
        if episode_match:
            episode = int(episode_match.group(0))
            print(episode)
            # 将文件名中的数字提取出来作为集数，将季数转换为英文形式
            season_prefix = "S" + season.zfill(2)
            
            new_file_name = "{}.{}E{}{}{}".format(show_name, season_prefix, episode, year, resolution)
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
    resolution_combo.set("")  # 清空分辨率下拉框选择
    year_combo.set("")  # 清空年份下拉框选择

def select_folder():
    def handle_select_folder():
        folder_path = filedialog.askdirectory()
        if folder_path:
            folder_entry.delete(0, tk.END)
            folder_entry.insert(tk.END, folder_path)
            
            
            show_name = os.path.basename(folder_path)
            

            haveResolution = False
            haveYears = False
            # 根据文件夹名称或文件名自动填充年份和分辨率下拉框
            resolutions = ["2160p", "1440p", "1080p", "720p", "480p"]
            for resolution in resolutions:
                if resolution in show_name:
                    haveResolution = True
                    resolution_combo.set(resolution)
                    break
            years = list(range(1900, 2031))
            for year in years:
                if str(year) in show_name:
                    haveYears = True
                    year_combo.set(year)
                    break
            
            if not haveResolution:
                for root,folders,files in os.walk(folder_path):
                    for f in files:
                        for resolution in resolutions:
                            if resolution in f:
                                haveResolution = True
                                resolution_combo.set(resolution)
                                break
                        if haveResolution:
                            break
                    if haveResolution:
                        break

            if not haveYears:
                for root,folders,files in os.walk(folder_path):
                    for f in files:
                        for year in years:
                            if str(year) in f:
                                haveYears = True
                                year_combo.set(year)
                                break
                        if haveYears:
                            break
                    if haveYears:
                        break
                    
            # 提取文件夹名称作为默认电视剧名称，并去掉"中文版"
            show_name = show_name.replace("中文版", "")
            show_name = re.sub(r'\d+|\.', '', show_name)
            name_entry.delete(0, tk.END)
            name_entry.insert(tk.END, show_name)


    def handle_rename_files():
        folder_path = folder_entry.get()
        show_name = name_entry.get()
        season = season_entry.get()
        resolution = resolution_combo.get()
        year = year_combo.get()
        if folder_path and show_name and season and show_name != "必填" and season != "必填":
            rename_files(folder_path, show_name, season, resolution, year, folder_entry, name_entry, season_entry, resolution_combo, year_combo)
        else:
            messagebox.showwarning("输入错误", "请填写完整的信息！")

            
    def name_entry_on_focus_in(event):
        if name_entry.get() == "必填":
            name_entry.delete(0, tk.END)

    def name_entry_on_focus_out(event):
        if name_entry.get() == "":
            name_entry.insert(tk.END, "必填")

    def season_entry_on_focus_in(event):
        if season_entry.get() == "必填":
            season_entry.delete(0, tk.END)

    def season_entry_on_focus_out(event):
        if season_entry.get() == "":
            season_entry.insert(tk.END, "必填")

    def validate_entry(text):
        # 检查输入的文本是否包含数字和小数点
        if any(char.isdigit() or char == '.' for char in text):
            return False
        return True


    root = tk.Tk()
    validate_cmd = root.register(validate_entry)
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
    name_entry.insert(tk.END, "必填")  # 添加占位提示词
    name_entry.bind("<FocusIn>", name_entry_on_focus_in)
    name_entry.bind("<FocusOut>", name_entry_on_focus_out)
    name_entry.pack()

    season_label = tk.Label(root, text="第几季：")
    season_label.pack()

    season_entry = tk.Entry(root, width=50)
    season_entry.insert(tk.END, "必填")  # 添加占位提示词
    season_entry.bind("<FocusIn>", season_entry_on_focus_in)
    season_entry.bind("<FocusOut>", season_entry_on_focus_out)
    season_entry.pack()

    resolution_label = tk.Label(root, text="分辨率：")
    resolution_label.pack()

    resolution_combo = ttk.Combobox(root, values=["4k", "2k", "1080p", "960p", "720p", "480p"])
    resolution_combo.pack()

    year_label = tk.Label(root, text="年份：")
    year_label.pack()

    year_combo = ttk.Combobox(root, values=list(range(1900, 2031)))
    year_combo.pack()

    rename_button = tk.Button(root, text="开始重命名", command=handle_rename_files)
    rename_button.pack()

    root.mainloop()

select_folder()