import tkinter as tk
from tkinter import filedialog , Menu , Text , PanedWindow , simpledialog,colorchooser


class Text_area(Text):
    def __init__(self , master , **kw):
        super().__init__(master , **kw)
        self.filename = ""
        self.text_size = 0
        self.text_family = "Arial"
        self.text_size = "12"
        self.text_color = "black"
        self.is_bold = False
        self.cnt_size = 0
        self.cnt_color = 0
        self.color_b = "white"
        self.colors = {}
        self.sizes = {}
        self.color_all = []

class TextEditor:
    def __init__(self , master):
        self.master = master
        self.master.title("多文本编辑器")
        self.master.geometry("800x800")
        # 创建一个 PanedWindow
        self.paned_window = PanedWindow(master , orient = tk.HORIZONTAL)
        self.paned_window.pack(fill = tk.BOTH , expand = True)
        self.file_name = {}
        # 菜单
        self.menu = Menu(master , tearoff = 0)
        master.config(menu = self.menu)

        self.file_menu = Menu(self.menu , tearoff = 0)
        self.menu.add_cascade(label = "文件" , menu = self.file_menu)
        self.file_menu.add_command(label = "打开" , command = self.open_file)
        self.file_menu.add_command(label = "撤销", command = self.undo)
        self.file_menu.add_command(label = "关闭" , command = self.quit)
        self.file_menu.add_command(label = "新建" , command = self.new_file)
        self.file_menu.add_command(label = "另存为" , command = self.save_as)
        self.file_menu.add_command(label = "保存" , command = self.save)

        self.editor_menu = Menu(self.menu , tearoff = 0)
        self.menu.add_cascade(label = "编辑" , menu = self.editor_menu)
        self.editor_menu.add_command(label = "复制" , command = self.copy)
        self.editor_menu.add_command(label = "黏贴" , command = self.paste)
        self.editor_menu.add_command(label = "剪切" , command = self.cut)
        self.editor_menu.add_command(label = "替换" , command = self.replace_text)
        self.editor_menu.add_command(label = "查找" , command = self.find_text)

        self.text_menu = Menu(self.menu , tearoff = 0)
        self.menu.add_cascade(label = "文字" , menu = self.text_menu)
        self.text_menu.add_command(label = "改变字号" , command = self.change_font)
        self.text_menu.add_command(label = "加粗" , command = self.change_bold)
        self.text_menu.add_command(label = "颜色" , command = self.change_color)
        self.text_menu.add_command(label = "背景颜色" , command = self.change_color_background)
        
        self.geshi_menu = Menu(self.menu , tearoff = 0)
        self.menu.add_cascade(label = "格式" , menu = self.geshi_menu)
        self.geshi_menu.add_command(label = "居中" , command = lambda:self.set_alignment("center"))
        self.geshi_menu.add_command(label = "左对齐" , command = lambda:self.set_alignment("left"))
        self.geshi_menu.add_command(label = "右对齐" , command = lambda:self.set_alignment("right"))

        self.paiban_menu = Menu(self.menu , tearoff = 0)
        self.menu.add_cascade(label = "排版" , menu = self.paiban_menu)
        self.paiban_menu.add_command(label = "水平" , command = self.shuiping)
        self.paiban_menu.add_command(label = "垂直" , command = self.chuizhi)
        self.paiban_menu.add_command(label = "堆叠" , command = self.duidie)
        # 存储所有文本框
        self.text_boxes = []
        self.current_text_box = None  # 当前活动的文本框
        self.new_file()
        self.is_drag = False
        self.drag_x = 0
        self.drag_y = 0
        self.master_x = 0
        self.master_y = 0
        self.drag_index = 0
        self.pailie = True

    def shuiping(self):
        self.paned_window.config(orient=tk.HORIZONTAL)
        self.pailie = True
        self.flash()

    def chuizhi(self):
        self.paned_window.config(orient=tk.VERTICAL)
        self.pailie = True
        self.flash()

    def duidie(self):
        self.pailie = 0

    #实现一个改变字体颜色的函数
    def change_color(self):
        self.current_text_box.cnt_color += 1
        self.current_text_box.text_color = colorchooser.askcolor()[1]
        self.current_text_box.tag_add(f"color{self.current_text_box.cnt_color}","1.0",self.current_text_box.index("end-1c"))
        self.current_text_box.tag_config(f"color{self.current_text_box.cnt_color}",foreground = self.current_text_box.text_color)
        self.current_text_box.colors[f"color{self.current_text_box.cnt_color}"] = self.current_text_box.text_color
        self.current_text_box.config(fg = self.current_text_box.text_color)
        # for i in range(1,self.current_text_box.cnt_color+1):
        #     print(self.current_text_box.text_color)
        #     self.current_text_box.tag_config(f"color{i}" , foreground = self.current_text_box.text_color)

    def change_color1(self):
        global cnt_color
        new_color = colorchooser.askcolor()[1]
        self.current_text_box.cnt_color = self.current_text_box.cnt_color+1
        self.current_text_box.tag_add(f"color{self.current_text_box.cnt_color}","sel.first","sel.last")
        self.current_text_box.colors[f"color{self.current_text_box.cnt_color}"] = new_color
        self.current_text_box.tag_config(f"color{self.current_text_box.cnt_color}",foreground = new_color)
    
    def change_bold(self):
        self.current_text_box.is_bold = not self.current_text_box.is_bold
        self.current_text_box.config(font = (self.current_text_box.text_family , self.current_text_box.text_size , "bold" if self.current_text_box.is_bold else "normal"))
    
    def change_font12(self):
        print("12")
        new_size = simpledialog.askinteger("调整字号" , "请输入字号大小:" , initialvalue = self.current_text_box.text_size)
        if new_size:
            self.current_text_box.cnt_size = self.current_text_box.cnt_size + 1
            self.current_text_box.tag_add(f"large_font{self.current_text_box.cnt_size}" , "sel.first" , "sel.last")
            self.current_text_box.size = new_size
            print(new_size)
            self.current_text_box.sizes[f"large_font{self.current_text_box.cnt_size}"] = new_size
            self.current_text_box.tag_configure(f"large_font{self.current_text_box.cnt_size}" ,
                                    font = (self.current_text_box.text_family , new_size , "bold" if self.current_text_box.is_bold else "normal")) 
            
    def change_color_background(self):
        self.current_text_box.color_b = colorchooser.askcolor()[1]
        self.current_text_box.config(bg = self.current_text_box.color_b)
        
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
        self.text_boxes.remove(self.current_text_box.master)
        self.current_text_box.master.destroy()

    def on_press(self,event):
        event.widget.master.winfo_children()[1].focus_set()
        self.current_text_box = event.widget.master.winfo_children()[1]

        self.drag_index = self.text_boxes.index(event.widget.master)
        self.master.lift()
        self.is_drag = True
        self.drag_x = event.x_root
        self.drag_y = event.y_root
        self.master_x = event.widget.master.winfo_x()
        self.master_y = event.widget.master.winfo_y()
        # self.text_boxes[0],self.text_boxes[1] = self.text_boxes[1],self.text_boxes[0]
        # self.flash()

    def flash(self):
        for i in self.paned_window.winfo_children():
            i.pack_forget()
        for i in self.text_boxes:
            i.pack(fill = "both" , side = tk.TOP)
            self.paned_window.add(i)

    def drag(self,event):
        # print(self)
        if self.is_drag:
            event.widget.master.lift()
            delta_x = event.x_root - self.drag_x
            delta_y = event.y_root - self.drag_y
            print(self.master_x)
            event.widget.master.place(x = delta_x+self.master_x,y = self.master_y+delta_y)

    def release(self,event):
        for index , value in enumerate(self.text_boxes):
            if value.winfo_x()<=event.x_root and value.winfo_x()+value.winfo_width()>=event.x_root and not self.drag_index == index:
                self.text_boxes[index],self.text_boxes[self.drag_index] = self.text_boxes[self.drag_index],self.text_boxes[index]

        if self.pailie:
            self.flash()

    def save(self):
        if self.current_text_box.filename:
            with open(self.current_text_box.filename , "w",encoding='utf-8') as file:
                file.write(self.current_text_box.get(1.0 , "end"))
            self.save_tags(self.current_text_box.filename)
        else:
            self.save_as()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension = ".txt" ,
                                               filetypes = [("Text Files" , "*.txt") ,
                                                            ("All Files" , "*.*")])
        if file_path:
            # 创建一个新的文本框
            frame = tk.Frame(self.master)
            frame2 = tk.Frame(frame,bg = "#999999")
            label = tk.Label(frame2 , text = "",bg = "#999999")
            label.pack()
            frame2.bind("<Button-1>" , self.on_press)
            frame2.bind("<B1-Motion>",self.drag)
            frame2.bind("<ButtonRelease-1>" , self.release)
            
            frame2.pack(fill = "both" , side = tk.TOP)
            text_box = Text_area(frame , wrap = tk.WORD, bd=1 , relief="solid", font = ( "Arial",12),undo = True)
            text_box.bind("<Button-3>",self.text_command)
            text_box.pack(fill = "y",expand = True)
            self.paned_window.add(frame)
            self.text_boxes.append(frame)
            # 读取文件内容
            with open(file_path , 'r' , encoding = 'utf-8') as file:
                text_box.insert(tk.END , file.read())

            # 设置文本框的标题
            text_box.filename = file_path
            label.config(text = file_path)

            # 绑定焦点事件
            text_box.bind("<FocusIn>" , self.set_current_text_box)
            text_box.bind("<FocusOut>" , self.set_focus_out)
            # 设置焦点到新创建的文本框
            text_box.focus_set()
            text_box.pack(fill = "both" , expand = True)
            self.current_text_box = text_box  # 更新当前活动的文本框
            self.load_tags(self.current_text_box.filename)

    def new_file(self):
        frame = tk.Frame(self.master,)
        frame2 = tk.Frame(frame,bg = "#999999")
        label = tk.Label(frame2 , text = "",bg = "#999999")
        label.pack()
        frame2.bind("<Button-1>", self.on_press )
        frame2.bind("<B1-Motion>" , self.drag )
        frame2.bind("<ButtonRelease-1>", self.release)
        frame2.pack(fill = "x")
        print(frame2.master)
        text_box = Text_area(frame , wrap = tk.WORD, bd=1 , relief="solid", font = ( "Arial",12),undo = True)
        text_box.bind("<FocusIn>" , self.set_current_text_box)
        text_box.bind("<FocusOut>" , self.set_focus_out)
        text_box.bind("<Button-3>",self.text_command)
        text_box.focus_set()
        text_box.pack(expand = True , fill = "both")
        frame.pack(fill = "both" , side = tk.TOP)
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
        except:
            return

    def cut(self):
        self.current_text_box.event_generate("<<Cut>>")

    def paste(self):
        self.current_text_box.event_generate("<<Paste>>")

    def set_current_text_box(self , event):
        event.widget.master.lift()
        print(event.widget)
        event.widget.master.winfo_children()[0].config(bg = "#555555")
        event.widget.master.winfo_children()[0].winfo_children()[0].config(bg = "#555555")
        self.current_text_box = event.widget  # 更新当前活动的文本框

    def set_focus_out(self , event):
        event.widget.master.winfo_children()[0].config(bg = "#999999")
        event.widget.master.winfo_children()[0].winfo_children()[0].config(bg = "#999999")

    def save_as(self):
        file = filedialog.asksaveasfile(mode = "w" , defaultextension = ".txt" ,
                                        filetypes = [("All Files" , "*.*") , ("Text Documents" , "*.txt")])
        if file:
            self.current_text_box.filename = file.name
            self.current_text_box.master.winfo_children()[0].winfo_children()[0].config(text = file.name)
            file.close()
            with open(file.name , "w",encoding='utf-8') as file:
                file.write(self.current_text_box.get(1.0 , "end"))
            self.save_tags(self.current_text_box.filename)

    def change_font(self):

        new_size = simpledialog.askinteger("调整字号" , "请输入字号大小:" ,
                                           initialvalue = self.current_text_box.text_size)
        if new_size:
            self.current_text_box.text_size = new_size
            self.current_text_box.config(font = (self.current_text_box , self.current_text_box.text_size ,
                                                 "bold" if self.current_text_box.is_bold else "normal"))
        self.current_text_box.cnt_size = self.current_text_box.cnt_size + 1
        self.current_text_box.tag_add(f"large_font{self.current_text_box.cnt_size}" , "1.0" , self.current_text_box.index("end-1c"))
        self.current_text_box.sizes[f"large_font{self.current_text_box.cnt_size}"] = new_size
        self.current_text_box.tag_configure(f"large_font{self.current_text_box.cnt_size}" ,
                                            font = (self.current_text_box.text_family , new_size , "bold" if self.current_text_box.is_bold else "normal"))      

    def set_alignment(self , alignment):
        self.current_text_box.tag_configure("alignment" , justify = alignment)
        self.current_text_box.tag_add("alignment" , "1.0" , "end")
        
    def text_command(self,event):
        event.widget.focus_set()
        text_menu = tk.Menu(self.master, tearoff=0)
        text_menu.add_command(label="改变字号", command=self.change_font12)
        text_menu.add_command(label="调整颜色",command=self.change_color1)
        text_menu.add_command(label="背景颜色",command=self.change_color_background)
        text_menu.add_command(label="复制", command=self.copy)
        text_menu.add_command(label = "黏贴" ,command=self.paste )
        text_menu.add_command(label = "剪切" ,command=self.cut )
        text_menu.post(event.x_root, event.y_root)

    def save_tags(self, filename):

            all_tags = self.current_text_box.tag_names()
            with open(filename + '_tags', 'w', encoding='utf-8') as f:
                for tag in all_tags:
                    if tag == "sel":
                        attributes_dict = {
                            "name" : "sel",
                            "text_size": self.current_text_box.text_size,
                            "text_family": self.current_text_box.text_family,
                            "is_bold": self.current_text_box.is_bold,
                            "color_b": self.current_text_box.color_b,
                            "color_f": self.current_text_box.text_color,
                            "cnt_size": self.current_text_box.cnt_size,
                            "cnt_color": self.current_text_box.cnt_color
                        }

# 将字典转换为字符串以便写入文件
                        attributes_str = str(attributes_dict)
                        f.write(attributes_str + '\n')
                        continue
                   
                    # 记录标签名称和配置信息
                    tag_info = {}
                    if tag.startswith("color"):
                        if self.current_text_box.tag_ranges(tag):
                            tag_info["name"] = tag
                            tag_info["color"] = self.current_text_box.colors[tag]
                            print(f"{self.current_text_box.tag_ranges(tag)[1]}"+"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                            tag_info["start"] = f"{self.current_text_box.tag_ranges(tag)[0]}"
                            tag_info["end"] = f"{self.current_text_box.tag_ranges(tag)[1]}"
                            
                    elif tag.startswith("large_font"):
                        if self.current_text_box.tag_ranges(tag):
                            print("large_font")
                            tag_info["name"] = tag
                            tag_info["size"] = self.current_text_box.sizes[tag]
                            tag_info["start"] = f"{self.current_text_box.tag_ranges(tag)[0]}"
                            
                            tag_info["end"] = f"{self.current_text_box.tag_ranges(tag)[1]}"
                        
                    tag_info = str(tag_info)
                    f.write(tag_info + '\n')
            print(f"所有标签及其信息已成功保存到 {filename}_tags")

    def load_tags(self, filename):
            with open(filename + '_tags', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # 将字符串解析为字典
                tag_info = eval(line)  # 使用 eval 解析字符串为字典，注意安全性
                if 'name' in tag_info:
                    tag_name = tag_info['name']
                    # 应用选中的标签
                    if tag_name == "sel":
                        self.current_text_box.text_size = tag_info["text_size"]
                        self.current_text_box.text_family = tag_info["text_family"]
                        self.current_text_box.is_bold = tag_info["is_bold"]
                        self.current_text_box.color_b = tag_info["color_b"]
                        self.current_text_box.text_color = tag_info["color_f"]
                        self.current_text_box.cnt_size = tag_info["cnt_size"]
                        self.current_text_box.cnt_color = tag_info["cnt_color"]
                        self.current_text_box.configure(font=(self.current_text_box.text_family, self.current_text_box.text_size, "bold" if self.current_text_box.is_bold else "normal"),bg=self.current_text_box.color_b,fg=self.current_text_box.text_color)
                    # 对于 color 标签
                    elif tag_name.startswith("color"):
                        print(tag_name)
                        self.current_text_box.colors[tag_name] = tag_info["color"]
                        self.current_text_box.tag_add(tag_name, tag_info["start"], tag_info["end"])
                        self.current_text_box.tag_configure(tag_name , foreground=tag_info["color"])
                    # 对于 large_font 标签
                    elif tag_name.startswith("large_font"):
                        self.current_text_box.sizes[tag_name] = tag_info["size"]
                        # 设置范围
                        self.current_text_box.tag_add(tag_name, tag_info["start"], tag_info["end"])
                        self.current_text_box.tag_configure(tag_name, font=(self.current_text_box.text_family, tag_info["size"], "bold" if self.current_text_box.is_bold else "normal"))
                        
            print(f"所有标签及其信息已成功加载到当前文本框")


if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()