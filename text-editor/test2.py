import tkinter as tk
from tkinter import ttk
from tkinter import filedialog,simpledialog,messagebox,colorchooser

text_size = 12
text_size2 = 12
text_color = "#000000"
text_color_b = "#ffffff"
text_family = "Arial"
text_color2 = "#000000"
text_color_b2 = "#ffffff"
text_family2 = "Arial"
is_bold = False
is_bold2 = False
cnt_size = 0
cnt_size2 = 0
root = tk.Tk()
filename = ""
filename2 = ""

    # Simply set the theme
root.tk.call("source", "azure.tcl")
root.tk.call("set_theme", "light")

frame = tk.Frame(root,bg = "white")
frame2 = tk.Frame(root,bg = "white")

frame.pack(fill = "x",expand = False,anchor = "nw")
scroll = ttk.Scrollbar()
text_area = tk.Text(root , wrap = "word",undo = True)
scroll = tk.Scrollbar(text_area)
text_area2 = tk.Text(root , wrap = "word",undo = True)
scroll2 = tk.Scrollbar(text_area2)

scroll.pack(side = tk.RIGHT,fill = tk.Y)
scroll2.pack(side = tk.RIGHT,fill = tk.Y)

def save_as(text_area):
    global filename
    file = filedialog.asksaveasfile(mode = "w" , defaultextension = ".txt" ,
                                    filetypes = [("All Files" , "*.*") , ("Text Documents" , "*.txt")])
    if file:
        filename = file.name
        file.write(text_area.get(1.0 , "end"))
        file.close()

def save_as2(text_area):
    global filename2
    file = filedialog.asksaveasfile(mode = "w" , defaultextension = ".txt" ,
                                    filetypes = [("All Files" , "*.*") , ("Text Documents" , "*.txt")])
    if file:
        filename2 = file.name
        file.write(text_area.get(1.0 , "end"))
        file.close()

def save_file(text_area):
        if filename:
            with open(filename, "w") as file:
                file.write(text_area.get(1.0, "end"))
        else:
            save_as(text_area)


def save_file2(text_area):
    if filename2:
        with open(filename2 , "w") as file:
            file.write(text_area.get(1.0 , "end"))
    else:
        save_as(text_area)


def open_file(text_area):
    global  filename
    file = filedialog.askopenfile(defaultextension = ".txt" ,
                                  filetypes = [("All Files" , "*.*") , ("Text Documents" , "*.txt")])
    if file:
        text_area.delete(1.0 , "end")
        for line in file:
            text_area.insert("end" , line)
        filename = file.name
        file.close()

def open_file2(text_area):
    global  filename2
    file = filedialog.askopenfile(defaultextension = ".txt" ,
                                  filetypes = [("All Files" , "*.*") , ("Text Documents" , "*.txt")])
    if file:
        text_area.delete(1.0 , "end")
        for line in file:
            text_area.insert("end" , line)
        filename2 = file.name
        file.close()

def new_file(text_area):
    global filename
    text_area.delete(1.0, "end")
    filename = None

def new_file2(text_area):
    global filename2
    text_area.delete(1.0, "end")
    filename2 = None

def undo(text_area):
    text_area.edit_undo()

def undo2(text_area):
    text_area.edit_undo()

def copy(text_area):
    try:
        # 获取选中的文本
        selected_text = text_area.get("sel.first" , "sel.last")
        # 清空剪贴板
        root.clipboard_clear()
        # 将选中的文本添加到剪贴板
        root.clipboard_append(selected_text)
        print("1")
    except:
        return

def cut(text_area):
    text_area.event_generate("<<Cut>>")

def paste(text_area):
    text_area.event_generate("<<Paste>>")

def find_text(text_area):
    search_text = simpledialog.askstring("查找", "输入查找内容:")
    if search_text:
        text_area.tag_remove("highlight", "1.0", "end")  # 移除旧的高亮
        start_pos = "1.0"
        while True:
            start_pos = text_area.search(search_text, start_pos, stopindex="end")
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(search_text)}c"
            text_area.tag_add("highlight", start_pos, end_pos)
            text_area.see(start_pos)
            start_pos = end_pos
        text_area.tag_config("highlight", background="yellow", foreground="black")

# 替换功能
def replace_text(text_area):
    search_text = simpledialog.askstring("查找", "输入查找内容:")
    replace_text = simpledialog.askstring("替换", "输入替换内容:")
    if search_text and replace_text is not None:
        start_pos = "1.0"
        while True:
            start_pos = text_area.search(search_text, start_pos, stopindex="end")
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(search_text)}c"
            text_area.delete(start_pos, end_pos)
            text_area.insert(start_pos, replace_text)
            start_pos = f"{start_pos}+{len(replace_text)}c"


def change_font(text_area):
    global text_size,cnt_size
    new_size = simpledialog.askinteger("调整字号" , "请输入字号大小:" , initialvalue = text_size)
    if new_size:
        text_size = new_size
        text_area.config(font = (text_family , text_size , "bold" if is_bold else "normal"))
    for i in range(cnt_size+1,cnt_size):
        text_area.tag_configure(f"large_font{cnt_size}" ,
                                font = (text_family , text_size , "bold" if is_bold else "normal"))


def change_font2(text_area):
    print("wadaw")
    global text_size2,cnt_size2
    print(cnt_size2)
    new_size = simpledialog.askinteger("调整字号" , "请输入字号大小:" , initialvalue = text_size2)
    if new_size:
        text_size2 = new_size
        text_area.config(font = (text_family2 , text_size2 , "bold" if is_bold2 else "normal"))
    for i in range(1,cnt_size2+1):
        text_area.tag_configure(f"large_font{cnt_size2}" ,
                                font = (text_family2 , text_size2 , "bold" if is_bold2 else "normal"))

def change_font1(text_area):
    global cnt_size
    new_size = simpledialog.askinteger("调整字号" , "请输入字号大小:" , initialvalue = text_size)
    if new_size:
        cnt_size = cnt_size + 1
        text_area.tag_add(f"large_font{cnt_size}" , "sel.first" , "sel.last")
        text_area.tag_configure(f"large_font{cnt_size}" ,
                                font = (text_family , new_size , "bold" if is_bold else "normal"))

def change_font12(text_area):
    global cnt_size2
    new_size = simpledialog.askinteger("调整字号" , "请输入字号大小:" , initialvalue = text_size2)
    if new_size:
        cnt_size2 = cnt_size2 + 1
        text_area.tag_add(f"large_font{cnt_size2}" , "sel.first" , "sel.last")
        text_area.tag_configure(f"large_font{cnt_size2}" ,
                                font = (text_family2 , new_size , "bold" if is_bold2 else "normal"))


def change_bold(text_area):
    global is_bold,cnt_bold
    is_bold = not is_bold
    text_area.config(font = (text_family , text_size , "bold" if is_bold else "normal"))

def change_bold2(text_area):
    global is_bold2,cnt_bold2
    is_bold2 = not is_bold2
    text_area.config(font = (text_family2 , text_size2 , "bold" if is_bold2 else "normal"))

cnt_color = 0
cnt_color2 = 0
def change_color(text_area):
    global text_color
    text_color = colorchooser.askcolor()[1]
    text_area.config(fg = text_color)
    for i in range(1,cnt_color+1):
        text_area.tag_config(f"color{cnt_color}",foreground = text_color)

def change_color2(text_area):
    print("awdaw")
    global text_color2
    text_color2 = colorchooser.askcolor()[1]
    text_area.config(fg = text_color2)
    for i in range(1,cnt_color2+1):
        text_area.tag_config(f"color{cnt_color2}",foreground = text_color2)


def change_color1(text_area):
    global cnt_color
    new_color = colorchooser.askcolor()[1]
    cnt_color = cnt_color+1
    text_area.tag_add(f"color{cnt_color}","sel.first","sel.last")
    text_area.tag_config(f"color{cnt_color}",foreground = new_color)

def change_color12(text_area):
    global cnt_color2
    new_color = colorchooser.askcolor()[1]
    cnt_color2 = cnt_color2+1
    text_area.tag_add(f"color{cnt_color2}","sel.first","sel.last")
    text_area.tag_config(f"color{cnt_color2}",foreground = new_color)

def change_color_background(text_area):
    global text_color_b
    text_color_b = colorchooser.askcolor()[1]
    text_area.config(bg = text_color_b)

def change_color_background2(text_area):
    global text_color_b2
    text_color_b2 = colorchooser.askcolor()[1]
    text_area.config(bg = text_color_b2)

def set_alignment(text_area, alignment):

    text_area.tag_configure("alignment", justify=alignment)
    text_area.tag_add("alignment", "1.0", "end")

#menubutton1
menu1 = tk.Menu()
menu1.add_command(label = "新建",command = lambda :new_file(text_area))
menu1.add_command(label="另存为",command = lambda :save_as(text_area))
menu1.add_command(label="保存",command = lambda :save_file(text_area))
menu1.add_command(label="打开文件",command = lambda :open_file(text_area))
menu1.add_command(label="退出",command = lambda :root.destroy())

menu12 = tk.Menu()
menu12.add_command(label = "新建",command = lambda :new_file2(text_area2))
menu12.add_command(label="另存为",command = lambda :save_as2(text_area2))
menu12.add_command(label="保存",command = lambda :save_file2(text_area2))
menu12.add_command(label="打开文件",command = lambda :open_file2(text_area2))
menu12.add_command(label="退出",command = lambda :root.destroy())

#menubutton2
menu2 = tk.Menu()
menu2.add_command(label="撤销",command = lambda :text_area.edit_undo())
menu2.add_command(label="复制",command = lambda :copy(text_area))
menu2.add_command(label="黏贴",command = lambda :paste(text_area))
menu2.add_command(label="剪切",command = lambda :cut(text_area))
menu2.add_command(label="查找", command=lambda:find_text(text_area))
menu2.add_command(label="替换", command=lambda:replace_text(text_area))

menu22 = tk.Menu()
menu22.add_command(label="撤销",command = lambda :text_area2.edit_undo())
menu22.add_command(label="复制",command = lambda :copy(text_area2))
menu22.add_command(label="黏贴",command = lambda :paste(text_area2))
menu22.add_command(label="剪切",command = lambda :cut(text_area2))
menu22.add_command(label="查找", command=lambda: find_text(text_area2))
menu22.add_command(label="替换", command=lambda: replace_text(text_area2))

#menubutton3
menu3 = tk.Menu()
menu3.add_command(label="大小",command = lambda :change_font(text_area))
menu3.add_command(label="加粗",command = lambda :change_bold(text_area))
menu3.add_command(label="文字颜色",command = lambda :change_color(text_area))
menu3.add_command(label="背景颜色",command = lambda :change_color_background(text_area))

menu32 = tk.Menu()
menu32.add_command(label="大小",command = lambda :change_font2(text_area2))
menu32.add_command(label="加粗",command = lambda :change_bold2(text_area2))
menu32.add_command(label="文字颜色",command = lambda :change_color2(text_area2))
menu32.add_command(label="背景颜色",command = lambda :change_color_background2(text_area2))

#menubutton4
menu4 = tk.Menu()
menu4.add_command(label="左对齐",command = lambda :set_alignment(text_area,"left"))
menu4.add_command(label="居中对齐",command = lambda :set_alignment(text_area,"center"))
menu4.add_command(label="右对齐",command = lambda :set_alignment(text_area,"right"))

menu42 = tk.Menu()
menu42.add_command(label="左对齐",command = lambda :set_alignment(text_area2,"left"))
menu42.add_command(label="居中对齐",command = lambda :set_alignment(text_area2,"center"))
menu42.add_command(label="右对齐",command = lambda :set_alignment(text_area2,"right"))


menubutton1 = ttk.Menubutton(frame,text="文件", direction="below",menu = menu1)
menubutton2 = ttk.Menubutton(frame,text="编辑", direction="below",menu = menu2)
menubutton3 = ttk.Menubutton(frame,text="文字", direction="below",menu = menu3)
menubutton4 = ttk.Menubutton(frame,text="格式", direction="below",menu = menu4)



menubutton12 = ttk.Menubutton(frame2,text="文件", direction="below",menu = menu12)
menubutton22 = ttk.Menubutton(frame2,text="编辑", direction="below",menu = menu22)
menubutton32 = ttk.Menubutton(frame2,text="文字", direction="below",menu = menu32)
menubutton42 = ttk.Menubutton(frame2,text="格式", direction="below",menu = menu42)


menubutton1.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
menubutton2.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
menubutton3.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
menubutton4.grid(row=0, column=3, padx=5, pady=5, sticky="nw")

menubutton12.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
menubutton22.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
menubutton32.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
menubutton42.grid(row=0, column=3, padx=5, pady=5, sticky="nw")

text_area.pack(fill = "both",expand = True)
frame2.pack(fill = "x",expand = False,anchor = "nw")
text_area2.pack(fill = "both",expand = True)

def text_command(event):
    text_menu = tk.Menu(root, tearoff=0)
    text_menu.add_command(label="改变字号", command = lambda :change_font1(text_area))
    text_menu.add_command(label="调整颜色",command = lambda :change_color1(text_area))
    text_menu.add_command(label = "加粗" , command = lambda:change_bold(text_area))
    text_menu.add_command(label="复制",command = lambda :copy(text_area))
    text_menu.add_command(label = "黏贴" , command = lambda :paste(text_area))
    text_menu.add_command(label = "剪切" , command = lambda :cut(text_area))
    text_menu.post(event.x_root, event.y_root)

def text_command2(event):
    text_menu = tk.Menu(root, tearoff=0)
    text_menu.add_command(label="改变字号", command = lambda :change_font12(text_area2))
    text_menu.add_command(label="调整颜色",command = lambda :change_color12(text_area2))
    text_menu.add_command(label = "加粗" , command = lambda:change_bold2(text_area2))
    text_menu.add_command(label="复制",command = lambda :copy(text_area2))
    text_menu.add_command(label = "黏贴" , command = lambda :paste(text_area2))
    text_menu.add_command(label = "剪切" , command = lambda :cut(text_area2))
    text_menu.post(event.x_root, event.y_root)

text_area.bind("<Button-3>",text_command)
text_area2.bind("<Button-3>",text_command2)


scroll.config(command = text_area.yview)
text_area.config(yscrollcommand = scroll.set)

scroll2.config(command = text_area2.yview)
text_area2.config(yscrollcommand = scroll2.set)

root.title("文本编辑器")
root.geometry("800x800")
root.mainloop()