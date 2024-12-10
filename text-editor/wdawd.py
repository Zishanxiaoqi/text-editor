import tkinter as tk
from tkinter import filedialog, Menu, Text, PanedWindow , simpledialog

class Text_area(tk.Text):
    def __init__(self , master, **kw):
        super().__init__(master , **kw)
        self.filename = ""
        self.text_size = 0
        self.text_family = "Arial"
        self.text_size = "12"
        self.is_bold = False
        self.cnt_size = 0
        self.cnt_color = 0
class TextEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("多文本编辑器")
        self.master.geometry("800x800")
        # 创建一个 PanedWindow
        self.paned_window = PanedWindow(master, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        self.file_name = {}
        # 菜单
        self.menu = Menu(master , tearoff = 0)
        master.config(menu=self.menu)

        self.file_menu = Menu(self.menu,tearoff = 0)
        self.menu.add_cascade(label = "文件" , menu = self.file_menu)
        self.file_menu.add_command(label = "打开" , command = self.open_file)
        self.file_menu.add_command(label = "关闭" , command = self.quit)
        self.file_menu.add_command(label = "新建" , command = self.new_file)
        self.file_menu.add_command(label = "另存为" , command = self.save_as)
        self.file_menu.add_command(label = "保存" , command = self.save_as)


        self.editor_menu = Menu(self.menu , tearoff = 0)
        self.menu.add_cascade(label="编辑", menu=self.editor_menu)
        self.editor_menu.add_command(label = "复制" , command = self.copy)
        self.editor_menu.add_command(label = "黏贴" , command = self.paste)
        self.editor_menu.add_command(label = "剪切" , command = self.cut)
        self.editor_menu.add_command(label = "替换" , command = self.replace_text)
        self.editor_menu.add_command(label = "查找" , command = self.find_text)

        self.text_menu = Menu(self.menu , tearoff = 0)
        self.menu.add_cascade (label = "文字" , menu = self.text_menu)
        self.text_menu.add_command(label = "改变字号" , command = self.change_font)

        self.geshi_menu = Menu(self.menu , tearoff = 0)
        self.menu.add_cascade(label = "格式" , menu = self.geshi_menu)
        self.geshi_menu.add_command(label = "居中" , command =lambda :self.set_alignment("center"))
        self.geshi_menu.add_command(label = "左对齐" , command = lambda:self.set_alignment("left"))
        self.geshi_menu.add_command(label = "右对齐" , command = lambda:self.set_alignment("right"))
        # 存储所有文本框
        self.text_boxes = []
        self.current_text_box = None  # 当前活动的文本框
        self.new_file()

    # def save_file(text_area):
    #     if filename:
    #         with open(filename , "w") as file:
    #             file.write(text_area.get(1.0 , "end"))
    #     else:
    #         save_as(text_area)

    def find_text(self):
        search_text = simpledialog.askstring("查找" , "输入查找内容:")
        if search_text:
            self.current_text_box.tag_remove("highlight" , "1.0" , "end")  # 移除旧的高亮
            start_pos = "1.0"
            while True:
                start_pos = self.current_text_box.search(search_text , start_pos , stopindex = "end")
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_text)}c"
                self.current_text_box.tag_add("highlight" , start_pos , end_pos)
                self.current_text_box.see(start_pos)
                start_pos = end_pos
            self.current_text_box.tag_config("highlight" , background = "yellow" , foreground = "black")

    def quit(self):
        self.current_text_box.master.destroy()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt"),
                                                           ("All Files", "*.*")])
        if file_path:
            # 创建一个新的文本框
            frame = tk.Frame(self.master)
            label = tk.Label(frame , text = "")
            label.pack(fill = "y" , side = tk.TOP)

            text_box = Text_area(frame, wrap=tk.WORD)
            self.paned_window.add(frame)
            self.text_boxes.append(frame)
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                text_box.insert(tk.END, file.read())

            # 设置文本框的标题
            text_box.filename = file_path
            label.config(text = file_path)

            # 绑定焦点事件
            text_box.bind("<FocusIn>", self.set_current_text_box)
            # 设置焦点到新创建的文本框
            text_box.focus_set()
            text_box.pack(fill = "both",expand = True)
            self.current_text_box = text_box  # 更新当前活动的文本框

    def new_file(self):
        frame = tk.Frame(self.master)
        label = tk.Label(frame,text = "")
        label.pack(fill = "y",side = tk.TOP)
        text_box = Text_area(frame , wrap = tk.WORD)
        text_box.bind("<FocusIn>" , self.set_current_text_box)
        text_box.focus_set()
        text_box.pack(expand = True,fill = "both")
        self.paned_window.add(frame)
        self.text_boxes.append(frame)

    def replace_text(self):
        search_text = simpledialog.askstring("查找" , "输入查找内容:")
        replace_text = simpledialog.askstring("替换" , "输入替换内容:")
        if search_text and replace_text is not None:
            start_pos = "1.0"
            while True:
                start_pos = self.current_text_box.search(search_text , start_pos , stopindex = "end")
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(search_text)}c"
                self.current_text_box.delete(start_pos , end_pos)
                self.current_text_box.insert(start_pos , replace_text)
                start_pos = f"{start_pos}+{len(replace_text)}c"

    def undo(self):
        self.current_text_box.edit_undo()

    def copy(self):
        try:
            # 获取选中的文本
            selected_text = self.current_text_box.get("sel.first" , "sel.last")
            # 清空剪贴板
            root.clipboard_clear()
            # 将选中的文本添加到剪贴板
            root.clipboard_append(selected_text)
            print("1")
        except:
            return

    def cut(self):
        self.current_text_box.event_generate("<<Cut>>")

    def paste(self):
        self.current_text_box.event_generate("<<Paste>>")
                
    def set_current_text_box(self, event):
        self.current_text_box = event.widget  # 更新当前活动的文本框
        print(event.widget.get)

    def save_as(self):
        file = filedialog.asksaveasfile(mode = "w" , defaultextension = ".txt" ,
                                        filetypes = [("All Files" , "*.*") , ("Text Documents" , "*.txt")])
        if file:
            self.current_text_box.filename = file.name
            self.current_text_box.master.winfo_children()[0].config(text = self.current_text_box.filename)
            file.write(self.current_text_box.get(1.0 , "end"))
            file.close()

    def change_font(self):

        new_size = simpledialog.askinteger("调整字号" , "请输入字号大小:" , initialvalue = self.current_text_box.text_size)
        if new_size:
            self.current_text_box.text_size = new_size
            self.current_text_box.config(font = (self.current_text_box , self.current_text_box.text_size , "bold" if self.current_text_box.is_bold else "normal"))

        for i in range(self.current_text_box.cnt_size + 1 , self.current_text_box.cnt_size):
            self.current_text_box.tag_configure(f"large_font{self.current_text_box.cnt_size}" ,
                                    font = (self.current_text_box.text_family , self.current_text_box.text_size , "bold" if self.current_text_box.is_bold else "normal"))

    def set_alignment(self , alignment):
        self.current_text_box.tag_configure("alignment" , justify = alignment)
        self.current_text_box.tag_add("alignment" , "1.0" , "end")

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
