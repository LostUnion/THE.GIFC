import customtkinter
from CTkListbox import *
from tkinter import filedialog as fd
from tkinter import *
import os
from PIL import Image
from pathlib import Path
from threading import Thread
import webbrowser

listt = []
frames = []
running = False

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

class Application(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('GIFC')
        self.geometry('600x600')
        self.resizable(False, False)
        self.put_frames()
    
    def put_frames(self):
        self.add_primary_window = PrimaryWindow(self)
        self.add_secondary_window = SecondaryWindow(self)

class PrimaryWindow(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.image = None
        self.primary_tab = customtkinter.CTkTabview(self.master, width=250, height=580)
        self.primary_tab.place(relx=0.01, rely=0.001)
        self.put_widgets()
        
    def put_widgets(self):
        def delete_file():
            active_switch = SecondaryWindow(parent=app)
            active_switch._s_switch.configure(state="disabled")
            
            self._photo_caption.configure(state="normal")
            self._list_of_images.delete('all')
            self._photo_caption.delete(1.0, 'end')
            self._photo_caption.insert('end', '')
            self._photo_caption.configure(state="disabled")
            listt.clear()
            
            self._label_img = customtkinter.CTkLabel(self.primary_tab, width=240, height=150, text=None, image=None, bg_color="#3B3B3B")
            self._label_img.place(relx=0.019, rely=0.050)
            
        def correct_size(width , height, image):
            if width > 240 or height > 150:
                ratio = min(240 / width, 250 / height)
                return image.resize((int(width * ratio), int(height * ratio)), resample=Image.LANCZOS)
            
        def show_selected_file(event):
            index = self._list_of_images.curselection()
            if index == 0 or index:
                self._photo_caption.configure(state="normal")
                selected_file_index = index
                selected_file = self._list_of_images.get(selected_file_index)
                file_name = os.path.basename(selected_file)
                self._photo_caption.delete(1.0, 'end')
                self._photo_caption.insert('end', f'{file_name}')
                self._photo_caption.configure(state="disabled")
                
                img = Image.open(selected_file)
                img = correct_size(img.size[0], img.size[1], img)
                size = img.size[0], img.size[1]
                self.image = customtkinter.CTkImage(light_image=img, size=size)
                self._label_img.configure(image=self.image)
                self._label_img.image = self.image
                
        def open_file():
            file_names = fd.askopenfilenames(title="Выберите файлы для сохранения")
            count = 0
            for file_name in file_names:
                self._list_of_images.insert(count, file_name)
                listt.append(file_name)
                count += 1
            active_switch = SecondaryWindow(parent=app)
            active_switch._s_switch.configure(state="normal")
                
        self._label_img = customtkinter.CTkLabel(self.primary_tab, width=240, height=150,
                                                 text=None, image=None, bg_color="#3B3B3B")
        self._label_img.place(relx=0.019, rely=0.050)
        
        self._photo_caption = customtkinter.CTkTextbox(self.primary_tab,width=240,
                                                       height=20,bg_color="#3B3B3B")
        self._photo_caption.insert('end', '')
        self._photo_caption.configure(state='disabled')
        self._photo_caption.place(relx=0.019, rely=0.30)
        
        self.settings_font = customtkinter.CTkFont(family='Arial', size=10)
        self._list_of_images = CTkListbox(self.primary_tab, width=212, height=310,
                                          font=self.settings_font,hover_color="#0FCAFD",
                                          hightlight_color="white", bg_color="#2B2B2B", 
                                          fg_color="#2B2B2B", select_color="black",
                                          command=show_selected_file)
        self._list_of_images.place(relx=0.019, rely=0.358)
        
        self._image_add = customtkinter.CTkImage(Image.open('image/icon_add.png'), size=(15, 15))
        self._image_deleted = customtkinter.CTkImage(Image.open('image/icon_deleted.png'), size=(15, 15))
        
        self._button_add = customtkinter.CTkButton(self.primary_tab, image=self._image_add, 
                                                   text="Add", width=119,text_color="white",
                                                   hover= True, hover_color= "black",
                                                   border_width=2, corner_radius=3,
                                                   border_color= "#d3d3d3", bg_color="#262626",
                                                   fg_color= "#262626", command=open_file)
        self._button_add.place(relx=0.019, rely=0.940)
        
        self._button_deleted = customtkinter.CTkButton(self.primary_tab, image=self._image_deleted,
                                                       text="Deleted", width=119,text_color="white",
                                                       hover= True, hover_color="black", border_width=2,
                                                       corner_radius=3, border_color= "#d3d3d3",
                                                       bg_color="#262626",fg_color= "#262626",
                                                       command=delete_file)
        self._button_deleted.place(relx=0.51, rely=0.940)

class SecondaryWindow(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.secondary_tab = customtkinter.CTkTabview(self.master, width=320, height=580)
        self.secondary_tab.place(relx=0.45, rely=0.001)
        self.put_secondary_widgets()

    def put_secondary_widgets(self):
        def correct_size(width , height, image):
            if width > 305 or height > 200:
                ratio = min(305 / width, 200 / height)
                return image.resize((int(width * ratio), int(height * ratio)), resample=Image.LANCZOS)
            
        def slider_event(value):
            self._s_label.configure(text=f"FPS: {int(value)}")
               
        def switch_event(image_index=0):
            if len(listt) == 0:
                self._s_label_img = customtkinter.CTkLabel(self.secondary_tab, width=305, height=200, text=None, image=None, bg_color="#3B3B3B")
                self._s_label_img.place(relx=0.024, rely=0.050)
                self._s_switch.configure(text="Animation : OFF")
            else:
                if self._s_switch.get() == "on":
                    if image_index < len(listt):
                        self._s_switch.configure(text="Animation : ON")
                        img = Image.open(listt[image_index])
                        img = correct_size(img.size[0], img.size[1], img)
                        size = img.size[0], img.size[1]
                        self._s_image = customtkinter.CTkImage(light_image=img, size=size)
                        self._s_label_img.configure(image=self._s_image)
                        self._s_label_img.image = self._s_image
                        
                        fps = self._s_slider.get()
                        interval = int(100 / fps)
                        
                        self.after(interval, switch_event, image_index + 1)
                        self._s_frames.configure(text = f"Frames: {image_index}")
                    else:
                        self._s_switch.configure(text="Animation : OFF")
                        self._s_label_img = customtkinter.CTkLabel(self.secondary_tab, width=305, height=200, text=None, image=None, bg_color="#3B3B3B")
                        self._s_label_img.place(relx=0.024, rely=0.050)
                        self._s_switch.deselect()
                        
                elif self._s_switch.get() == 'off':
                    self._s_switch.configure(text="Animation : OFF")
                    self._s_label_img = customtkinter.CTkLabel(self.secondary_tab, width=305, height=200, text=None, image=None, bg_color="#3B3B3B")
                    self._s_label_img.place(relx=0.024, rely=0.050)
           
        def saves(optimize):
                file_name = self._s_file_name.get(1.0, 'end-1c')
                if self._s_save_checbox.get() == "on":
                    frames[0].save(f"{file_name}.gif", save_all=True, append_images=frames[1:], optimize=optimize, duration=self._s_slider.get(), loop=0)
                elif self._s_save_checbox.get() == "off":
                    select_floder = fd.askdirectory(mustexist=True)
                    if select_floder:
                        frames[0].save(f"{select_floder}/{file_name}.gif", save_all=True, append_images=frames[1:], optimize=False, duration=self._s_slider.get(), loop=0)
        
        def convert():
            self._list_of_downloads.configure(state="normal")
            count = 0
            for item in listt:
                self._s_progressbar.configure(progress_color="black")
                self._s_progressbar.start()
                frame = Image.open(item)
                frames.append(frame)
                count += 1
                self._list_of_downloads.delete(1.0, f'end-1c')
                self._list_of_downloads.insert('end', f'Frame: {count}')
            self._list_of_downloads.configure(state="disabled")
                
            if self._s_quality_checbox.get() == "on":
                saves(optimize=True)
            else:
                saves(optimize=False)
                
            self._s_progressbar.stop()
            self._s_progressbar.configure(progress_color="#4A4D50")
            
            self._s_notification.configure(state="normal")
            self._s_notification.delete(1.0, 'end')
            self._s_notification.insert("end","File saved ✅")
            self._s_notification.configure(state="disabled")
             
        def tread():
            file_name : str = self._s_file_name.get(1.0,'end-1c')
            
            if len(listt) == 0:
                self._s_notification.configure(state="normal")
                self._s_notification.delete(1.0, 'end')
                self._s_notification.insert("end","Files are missing...")
                self._s_notification.configure(state="disabled")
            elif len(file_name) == 0:
                self._s_notification.configure(state="normal")
                self._s_notification.delete(1.0, 'end')
                self._s_notification.insert("end","Enter the file name")
                self._s_notification.configure(state="disabled")
            else:
                t1 = Thread(target=convert)
                t1.start()
            
        def open_link():
            url = "https://github.com/LostUnion"  # Замените этот URL на нужный вам
            webbrowser.open_new(url)  

        self._s_label_img = customtkinter.CTkLabel(self.secondary_tab, width=305, 
                                                   height=200, text=None, image=None, 
                                                   bg_color="#3B3B3B")
        self._s_label_img.place(relx=0.024, rely=0.050)
        
        self._s_slider = customtkinter.CTkSlider(self.secondary_tab, from_=0, to=60,
                                                 height=10, width=250, progress_color="#0FCAFD",
                                                 fg_color="white", button_color="white",
                                                 button_hover_color="black", command=slider_event)
        self._s_slider.configure(number_of_steps = 60)
        self._s_slider.place(relx=0.013, rely=0.458)
        
        self._s_label = customtkinter.CTkLabel(self.secondary_tab,height=9, width=70, text="FPS: 30", fg_color="transparent")
        self._s_label.place(relx=0.795, rely=0.455)
        
        self._s_frames = customtkinter.CTkLabel(self.secondary_tab, text="Frames: ", bg_color="transparent", width=40, height=25)
        
        self._s_frames.place(relx=0.024, rely=0.41)
        
        self._s_switch_var_on = customtkinter.StringVar(value="on")
        self._s_switch_var_off = customtkinter.StringVar(value="off")
        
        self._s_switch = customtkinter.CTkSwitch(self.secondary_tab, text="Animation : OFF", 
                                                 variable=self._s_switch_var_off, onvalue="on", 
                                                 offvalue="off", command=switch_event)
        self._s_switch.configure(state="disabled")
        self._s_switch.place(relx=0.56, rely=0.41)
        
        self.check_quality_var_on = customtkinter.StringVar(value="on")
        self.check_quality_var_off = customtkinter.StringVar(value="off")
        
        self._s_quality_checbox = customtkinter.CTkCheckBox(self.secondary_tab, text="Quality", 
                                                            command=None, border_width=1, hover_color="black",
                                                            fg_color = "black", checkbox_width=20, checkbox_height=20,
                                                            variable=self.check_quality_var_off, width=1, height=1,
                                                            onvalue="on", offvalue="off")
        self._s_quality_checbox.place(relx=0.024, rely=0.50)
        
        
        self.check_save_var_on = customtkinter.StringVar(value="on")
        self.check_save_var_off = customtkinter.StringVar(value="off")
        
        self._s_save_checbox = customtkinter.CTkCheckBox(self.secondary_tab, text="Save to this folder", 
                                                         command=None, border_width=1, hover_color="black",
                                                         fg_color = "black", checkbox_width=20, checkbox_height=20,
                                                         variable=self.check_save_var_off, width=1, height=1, onvalue="on", 
                                                         offvalue="off")
        self._s_save_checbox.place(relx=0.024, rely=0.55)
        
        self._list_of_downloads = customtkinter.CTkTextbox(self.secondary_tab, width=153, height=46)
        self._list_of_downloads.configure(state="disabled")
        self._list_of_downloads.place(relx=0.5, rely=0.50)
        
        self._s_label_file_name = customtkinter.CTkLabel(self.secondary_tab, text="File name", width=10, height=30)
        self._s_label_file_name.place(relx=0.024, rely=0.59)
        
        self._s_file_name = customtkinter.CTkTextbox(self.secondary_tab, width=233, height=10)
        self._s_file_name.place(relx=0.25, rely=0.59)
        
        self._s_progressbar = customtkinter.CTkProgressBar(self.secondary_tab, orientation="horizontal",
                                                           progress_color="#4A4D50", mode="indeterminate",
                                                           width=305)
        self._s_progressbar.place(relx=0.026, rely=0.652)
        
        self._image_convert = customtkinter.CTkImage(Image.open('image/icon_convert.png'), size=(15, 15))
        
        self._s_notification = customtkinter.CTkTextbox(self.secondary_tab, width=200, height=10, fg_color="transparent" )
        self._s_notification.configure(state="disabled")
        self._s_notification.place(relx=0.024, rely=0.670)
        
        self._s_button_convert = customtkinter.CTkButton(self.secondary_tab, image=self._image_convert, 
                                                         text="Convert", width=100, text_color="white",
                                                         hover= True, hover_color= "black", border_width=2,
                                                         corner_radius=3, border_color= "#d3d3d3", bg_color="#262626",
                                                         fg_color= "#262626", command=tread)
        self._s_button_convert.place(relx=0.66, rely=0.675)
        
        self._test_label = customtkinter.CTkLabel(self.secondary_tab, justify="left", 
                                                  text="The source code of the program is publicly\n available on the page https://github.com/LostUnion", 
                                                  text_color="#878787", bg_color="transparent", width=10, height=10)
        self._test_label.place(relx=0.042, rely=0.740)
        
        self._image_git = customtkinter.CTkImage(Image.open('image/git_img.png'), size=(290, 110))

        self._test_label = customtkinter.CTkButton(self.secondary_tab, image=self._image_git, hover=True,
                                                   hover_color="#2B2B2B", width=10, height=10,
                                                   corner_radius=50, border_color="#d3d3d3",
                                                   fg_color="#2B2B2B", text=None, command=open_link)
        self._test_label.place(relx=0.024, rely=0.795)

if __name__ == "__main__":
    app = Application()
    app.mainloop()