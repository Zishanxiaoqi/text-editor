import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font, colorchooser
import ctypes
import tkinter as tk
from tkinter import *
cnt = 0
def dark_title_bar(window):
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ctypes.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ctypes.c_int(value)
    set_window_attribute(hwnd , rendering_policy , ctypes.byref(value) , ctypes.sizeof(value))
    window.update()

# 创建主应用程序窗口
root = tk.Tk()
dark_title_bar(root)
root.tk.call("source" , "azure.tcl")
root.tk.call("set_theme" , "dark")
root.title("增强文本编辑器")
root.geometry("600x400")

# 设置默认字体
current_font_family = "Arial"
current_font_size = 12
is_bold = False



# 创建Text小部件，用于显示和编辑文本
text_area = tk.Text(root, wrap="word", font=(current_font_family, current_font_size))
text_area.pack(expand=1, fill="both")


# 创建菜单栏
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# 文件菜单的回调函数
def add_tag():
    try:
        global cnt
        text_area.tag_add(f"large_font{cnt}" , "sel.first" , "sel.last")
        cnt = cnt+1
        return True
    except tk.TclError:
        return False

def remove_tag():
    text_area.tag_remove("large_font" , "sel.first" , "sel.last")



def new_file():
    """新建文件，清空文本区域"""
    text_area.delete(1.0, tk.END)
    root.title("未命名 - 文本编辑器")

def open_file():
    """打开现有文件并显示其内容"""
    file_path = filedialog.askopenfilename(
        filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, content)
            root.title(f"{file_path} - 文本编辑器")
        except Exception as e:
            messagebox.showerror("错误", f"无法读取文件: {e}")

def save_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text_area.get(1.0, tk.END))
            root.title(f"{file_path} - 文本编辑器")
        except Exception as e:
            messagebox.showerror("错误", f"无法保存文件: {e}")

# 编辑菜单功能
def find_text():
    """查找文本"""
    search_query = simpledialog.askstring("查找文本", "请输入要查找的内容:")
    if search_query:
        start_pos = text_area.search(search_query, "1.0", tk.END)
        if start_pos:
            end_pos = f"{start_pos}+{len(search_query)}c"
            text_area.tag_add("highlight", start_pos, end_pos)
            text_area.tag_config("highlight", background="yellow", foreground="black")
        else:
            messagebox.showinfo("查找结果", "未找到匹配的内容。")

def change_font():
    """更换字体"""
    global current_font_family
    new_font_family = simpledialog.askstring("更换字体", "请输入字体名称:")
    if new_font_family:
        current_font_family = new_font_family
        text_area.config(font=(current_font_family, current_font_size, "bold" if is_bold else "normal"))

def toggle_bold():
    """加粗文本"""
    global is_bold
    is_bold = not is_bold
    text_area.config(font=(current_font_family, current_font_size, "bold" if is_bold else "normal"))



def change_font_size():
    global cnt
    global current_font_size
    """调整字号"""
    if not add_tag():
        new_size = simpledialog.askinteger("调整字号", "请输入字号大小:", initialvalue=current_font_size)
        if new_size:
            current_font_size = new_size
            text_area.config(font=(current_font_family, current_font_size, "bold" if is_bold else "normal"))
    else:
        new_size = simpledialog.askinteger("调整字号" , "请输入字号大小:" , initialvalue = current_font_size)
        if new_size:
            text_area.tag_add(f"large_font{cnt}" , "sel.first" , "sel.last")
            text_area.tag_configure(f"large_font{cnt}",font = (current_font_family , new_size , "bold" if is_bold else "normal"))


def change_font_color():
    """调整字体颜色"""
    global cnt
    if not add_tag():
        color = colorchooser.askcolor()[1]
        if color:
            text_area.config(fg=color)
    else:
        color = colorchooser.askcolor()[1]
        print(color)
        text_area.tag_add(f"large_font{cnt}" , "sel.first" , "sel.last")
        text_area.tag_config(f"large_font{cnt}" ,foreground = color)


def text_command(event):
    text_menu = tk.Menu(root, tearoff=0)
    text_menu.add_command(label="改变字号", command=change_font_size)
    text_menu.add_command(label="调整颜色",command =change_font_color )
    text_menu.add_command(label="粘贴", )
    # 显示菜单（右键点击位置）
    text_menu.post(event.x_root, event.y_root)

text_area.bind("<Button-3>",text_command)

# 在菜单栏中添加文件菜单
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="文件", menu=file_menu)
file_menu.add_command(label="新建", command=new_file)
file_menu.add_command(label="打开", command=open_file)
file_menu.add_command(label="保存", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="退出", command=root.quit)

# 在菜单栏中添加编辑菜单
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="编辑", menu=edit_menu)
edit_menu.add_command(label="查找", command=find_text)

# 在菜单栏中添加格式菜单
format_menu = tk.Menu(menu_bar, tearoff=0)

menu_bar.add_cascade(label="格式", menu=format_menu)
format_menu.add_command(label="更换字体", command=change_font)
format_menu.add_command(label="加粗", command=toggle_bold)
format_menu.add_command(label="取消加粗", command=toggle_bold)
format_menu.add_command(label="调整字号", command=change_font_size)
format_menu.add_command(label="调整字体颜色", command=change_font_color)

# 运行应用程序主循环
root.mainloop()
