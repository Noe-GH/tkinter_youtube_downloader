import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
# Make sure to install pytube version 10.0.0, because the latest one (until
# now) (10.4.1) seems to be unstable (03/01/2021).
# pip install pytube == 10.0.0
import pytube
from pytube.cli import on_progress

# Colors and fonts:
frame_logo_color = 'black'
frame_link_color = 'black'
frame_options_color = 'black'
window_bg_color = 'black'
lbl_bg_color = 'black'
lbl_font_color = 'white'
lbl_link_font = 'arial 15 bold'
e_link_font = 'arial 20'
btn_bg_color = 'red'
btn_fg_color = 'black'
btn_font = 'arial 15 bold'
rbtn_fg_color = 'white'
rbtn_active_bg = 'red'
rbtn_font = 'arial 12'


class VideoDownloader():

    def __init__(self):
        self.w = tk.Tk()
        self.w.configure(bg=window_bg_color)
        self.w.title('Youtube Downloader')
        self.w.resizable(0, 0)
        self.w.geometry('1280x720+300+200')

        # Widgets creation starts:
        self.img_logo = tk.PhotoImage(file='assets/logo.png')
        self.frame_logo = tk.Frame(self.w, bg=frame_logo_color, pady=40)
        self.lbl_logo = tk.Label(self.frame_logo, image=self.img_logo,
                                 bg=lbl_bg_color)
        self.frame_link = tk.Frame(self.w, bg=frame_link_color)
        self.lbl_link = tk.Label(self.frame_link, text='  Video URL:  ',
                                 font=lbl_link_font, bg=lbl_bg_color,
                                 fg=lbl_font_color, pady=30)
        self.e_link = tk.Entry(self.frame_link, font=e_link_font, width=60)
        self.btn_download = tk.Button(self.frame_link, font=btn_font,
                                      bg=btn_bg_color, fg=btn_fg_color, bd=0,
                                      text='GET', width=4, height=1,
                                      command=lambda:
                                      self.download_content(self.e_link.get(),
                                                            (self.rbtn_option
                                                            .get())
                                                            ))
        self.frame_options = tk.Frame(self.w, bg=frame_options_color)
        self.rbtn_option = tk.StringVar()
        self.rbtn_video_audio = tk.Radiobutton(self.frame_options,
                                               text='Video and audio', value=0,
                                               bg=frame_options_color,
                                               fg=rbtn_fg_color,
                                               font=rbtn_font,
                                               activebackground=rbtn_active_bg,
                                               selectcolor='red',
                                               var=self.rbtn_option)
        self.rbtn_audio = tk.Radiobutton(self.frame_options, text='Audio only',
                                         value=1, bg=frame_options_color,
                                         fg=rbtn_fg_color,
                                         font=rbtn_font,
                                         activebackground=rbtn_active_bg,
                                         selectcolor='red',
                                         var=self.rbtn_option)
        self.rbtn_video = tk.Radiobutton(self.frame_options, text='Video only',
                                         value=2, bg=frame_options_color,
                                         fg=rbtn_fg_color,
                                         font=rbtn_font,
                                         activebackground=rbtn_active_bg,
                                         selectcolor='red',
                                         var=self.rbtn_option)

        self.rbtn_video_audio.select()

        # Widgets creation ends.

        # Widgets placing starts:

        self.frame_logo.pack(fill='x')
        self.lbl_logo.pack()
        self.frame_link.pack()
        self.lbl_link.pack(side='left')
        self.e_link.pack(side='left')
        self.btn_download.pack(side='left', padx=5)
        self.frame_options.pack()
        self.rbtn_video_audio.pack(side='left')
        self.rbtn_audio.pack(side='left')
        self.rbtn_video.pack(side='left')

        # Widgets placing ends.

        self.w.mainloop()

    def download_content(self, video_link, option):
        '''
        Function that manages the downloading of the Youtube content (video,
        audio or video & audio). It shows a progress bar in the CLI and user
        messages when it finishes downloading and when there is a problem with
        the URL.
            -video_link: Reveives the URL of the YouTube video as a string.
            -option: Receives string values from 0 to 2 to manage the content
            downloaded ('0': video & audio, '1': audio, '2': 'video').
        '''
        save_dir = filedialog.askdirectory()

        try:
            print('Preparing download')
            yt_video = pytube.YouTube(video_link,
                                      on_progress_callback=on_progress)

            if option == '0':
                yt_stream = yt_video.streams.get_highest_resolution()
            elif option == '1':
                yt_stream = yt_video.streams.filter(only_audio=True).first()
            else:
                yt_stream = (yt_video.streams.filter(only_video=True)
                             .order_by('resolution').desc().first())
            print('Downloading')
            yt_stream.download(save_dir)
            print('Done ')
            messagebox.showinfo('Done', 'Video downloaded.')

        except pytube.exceptions.RegexMatchError:
            messagebox.showwarning('URL Error',
                                   'The video could not be downloaded.'
                                   '\nPlease, check the URL.')


app = VideoDownloader()
