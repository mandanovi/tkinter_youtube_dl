import youtube_dl
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
from tkinter import font as tkFont
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi


class YoutubeDownload(Tk):
    def __init__(self):
        super().__init__()
        self.title("Youtube Download")
        self.geometry("410x400")  # Define the geometry of the window
        self.configure(bg='pink')
        self.widget()

    def widget(self):
        helv26 = tkFont.Font(family='Helvetica', size=26, weight=tkFont.BOLD)
        title = Label(width=25, text="Youtube Download App", font=helv26, anchor=CENTER, background='black', foreground='pink',)
        title.pack(side=TOP, pady=50)
        link_label = Label(text="URL Link:", font=tkFont.Font(family='Helvetica', size=11, weight=tkFont.BOLD), background='pink', foreground='black',)
        link_label.pack(side=TOP)
        input_text = StringVar()
        self.link = Entry(width=50, font=tkFont.Font(family='Helvetica', size=10, weight=tkFont.BOLD), textvariable=input_text, justify=CENTER)
        self.link.pack(pady=5)
        choices = ['MP4/Video', 'Audio Only']
        variable = StringVar(self)
        variable.set('MP4/Video')
        self.w = Combobox(self, values=choices, font=tkFont.Font(family='Helvetica', size=8, weight=tkFont.BOLD))
        self.w.pack()
        space_label = Label(text="", font=tkFont.Font(family='Helvetica', size=25, weight=tkFont.BOLD),
                           background='pink', foreground='black', )
        space_label.pack(side=BOTTOM)
        caption_button = Button(text="Download English Caption", width=25, command=self.download_caption)
        style = Style()
        style.configure('TButton', background='pink')
        style.configure('TButton', foreground="black")
        style.configure("TButton", font=('Helvetica', 10, "bold"))
        caption_button.pack(side=BOTTOM, pady=5)
        download_button = Button(text="Download Video/Audio", width=25, command=self.download)
        download_button.pack(side=BOTTOM)

    def download(self):
        link = self.link.get()

        if link == "":
            tkinter.messagebox.showerror("URL LINK", "You need to write the video URL, try again")
        else:
            if self.w.get() == "MP4/Video":
                ydl_opts = {}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])
                tkinter.messagebox.showinfo("Success", f"Video has been successfully downloaded")
            elif self.w.get() == "Audio Only":
                class MyLogger(object):
                    def debug(self, msg):
                        pass

                    def warning(self, msg):
                        pass

                    def error(self, msg):
                        print(msg)

                def my_hook(d):
                    if d['status'] == 'finished':
                        print('Done downloading, now converting ...')

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'logger': MyLogger(),
                    'progress_hooks': [my_hook],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])
                tkinter.messagebox.showinfo("Success", f"Audio has been successfully downloaded")
            else:
                tkinter.messagebox.showinfo("Not Complete", "Choose format file first!")

    def download_caption(self):
        youtube_link = self.link.get()
        link = youtube_link.split("v=")
        from_separated_list = link[1]
        today = datetime.now().date()
        try:
            srt = YouTubeTranscriptApi.get_transcript(from_separated_list)
            length = len(srt)
            with open(f"Output_{today}.txt", "w") as text_file:
                for i in range(0, length):
                    start = f"start : {srt[i]['start']}"
                    duration = f"duration : {srt[i]['duration']}"
                    text = srt[i]["text"]
                    text_file.writelines([start,"\n", duration, "\n", text, "\n"])
                tkinter.messagebox.showinfo("SUCCESS", f"txt file has been successfully downloaded")
        except:
            tkinter.messagebox.showerror("ERROR", "No subtitle available.")


App = YoutubeDownload()
App.mainloop()











