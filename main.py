import shutil, os

from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

from rouge import Rouge


def clean_transcripts_folder():
    folders = './Transcripts/'
    for f in os.listdir(folders):
        os.remove(os.path.join(folders, f))


def clean_summary_folder():
    folders = './Summary/'
    for f in os.listdir(folders):
        os.remove(os.path.join(folders, f))


def clean_audio_folder():
    folders = './Audio-File/'
    for f in os.listdir(folders):
        os.remove(os.path.join(folders, f))


def clean_video_folder():
    folders = './Video-File/'
    for f in os.listdir(folders):
        os.remove(os.path.join(folders, f))


def transcript_process():
    print("Transcribing")
    import TranscriptPart
    print("Transcribing.........")
    TranscriptPart.start_TranscriptPart()
    print("Transcribing Done")


def summary_process():
    print("Summarizing")
    import SummaryPart
    print("Summarizing.........")
    SummaryPart.start_SummaryPart(50, 500)
    print("Summarizing Done")


def callback():
    def upload_file(choice):
        def upload_file_save(choice):
            def save_file_at_dir(choice, filename):
                if choice == 'vc':
                    shutil.copy(filename, './Video-File/')
                if choice == 'ac':
                    shutil.copy(filename, './Audio-File/')
                if choice == 'tc':
                    shutil.copy(filename, './Transcripts/')

            def perform_final(choice, filename):
                def do_work(choice):
                    global min_ratio
                    min_ratio = simpledialog.askstring(title="Summarization",prompt="Enter Minimum Length for Summary (Enter None for default):")
                    if choice == 'vc':
                        do_video_work()
                    if choice == 'ac':
                        do_audio_work()
                    if choice == 'tc':
                        do_text_work()

                def open_t():
                    filename = os.listdir("./Transcripts/")
                    file = filename[0]
                    str1 = "notepad.exe Transcripts/" + file
                    osCommandString = str1
                    os.system(osCommandString)

                def open_s(key):
                    filename = os.listdir("./Summary/")
                    file = filename[key]
                    str1 = "notepad.exe Summary/" + file
                    osCommandString = str1
                    os.system(osCommandString)

                def rogue():
                    if option_choice != 'tc':
                        messagebox.showinfo("Information", "Rouge Can only be Calculated when input is a Text.")
                        top.mainloop()
                    ref = simpledialog.askstring(title="Summarization", prompt="Enter Reference Summary")
                    rouge = Rouge()
                    filename = os.listdir("./Summary/")
                    file = filename[5]
                    text_file = open("./Summary/"+file, encoding="utf8")
                    text = text_file.read()
                    text_file.close()
                    rouge_text=rouge.get_scores(text,ref)
                    print(rouge_text)
                    r1=rouge_text[0]['rouge-1']['f']
                    r2=rouge_text[0]['rouge-2']['f']
                    rl=rouge_text[0]['rouge-l']['f']
                    t1 = 'Rouge-1 = '+ str(r1)
                    t2 = 'Rouge-2 = ' + str(r2)
                    tl = 'Rouge-L = '+ str(rl)
                    label_r1 = tk.Label(root, text=t1, font=my_font2, foreground='red')
                    label_r1.place(x=350, y=430)
                    label_r1 = tk.Label(root, text=t2, font=my_font2, foreground='red')
                    label_r1.place(x=350, y=460)
                    label_r1 = tk.Label(root, text=tl, font=my_font2, foreground='red')
                    label_r1.place(x=350, y=490)


                def transcript_work():
                    import TranscriptPart
                    TranscriptPart.start_TranscriptPart(opt)
                    label_transcribe1 = tk.Label(root, text='Transcript Ready', font=my_font4, foreground='red',
                                                 width=20)
                    label_transcribe1.place(x=280, y=200)
                    bt_open = tk.Button(root, text='OPEN', width=12, command=lambda: open_t(), font=my_font2)
                    bt_open.place(x=550, y=200)
                    # bt_save = tk.Button(root, text='SAVE', width=12, command=lambda: None, font=my_font2)
                    # bt_save.place(x=432, y=240)

                def summary_work():
                    import SummaryPart
                    SummaryPart.start_SummaryPart(min_ratio)
                    label_transcribe1 = tk.Label(root, text='Summary Ready', font=my_font4, foreground='red', width=20)
                    label_transcribe1.place(x=280, y=350)
                    print(min_ratio)
                    #print(type(min_ratio))
                    bs_open = tk.Button(root, text='View Summary', width=12, command=lambda: open_s(5), font=my_font2)
                    if min_ratio=='None':
                        bs_open.place(x=550, y=350)
                    else:
                        min_val=int(min_ratio)
                        if min_val <= 100:
                            bs_open.place(x=550, y=350)
                        bs_open = tk.Button(root, text='100 Words', width=12, command=lambda: open_s(1), font=my_font2)
                        if min_val > 100:
                            bs_open.place(x=220, y=390)
                        bs_open = tk.Button(root, text='200 Words', width=12, command=lambda: open_s(2), font=my_font2)
                        if min_val >200:
                            bs_open.place(x=320, y=390)
                        bs_open = tk.Button(root, text='300 Words', width=12, command=lambda: open_s(3), font=my_font2)
                        if min_val>300:
                            bs_open.place(x=420, y=390)
                        bs_open = tk.Button(root, text='400 Words', width=12, command=lambda: open_s(4), font=my_font2)
                        if min_val>400:
                            bs_open.place(x=520, y=390)
                        bs_open = tk.Button(root, text='500 Words', width=12, command=lambda: open_s(5), font=my_font2)
                        if min_val > 500:
                            bs_open.place(x=620, y=390)
                    # bs_save = tk.Button(root, text='SAVE', width=12, command=lambda: None, font=my_font2)
                    # bs_save.place(x=432, y=370)
                    bs_open = tk.Button(root, text='Check ROUGE', width=12, command=lambda: rogue(), font=my_font2)
                    bs_open.place(x=220, y=430)

                def do_video_work():
                    l1.destroy()
                    b1.destroy()
                    label_done.destroy()
                    label_done_txt.destroy()
                    b_done.destroy()
                    butt_start.destroy()
                    file_name = os.listdir('./Video-File/')
                    video_filename = file_name[0]
                    #print(video_filename)
                    import moviepy.editor
                    videoFile = moviepy.editor.VideoFileClip('./Video-File/' + video_filename)
                    audio = videoFile.audio
                    audio_filename = video_filename.split('.')[0] + '.wav'
                    audio.write_audiofile('./Audio-File/' + audio_filename)
                    transcript_work()
                    summary_work()

                def do_audio_work():
                    l1.destroy()
                    b1.destroy()
                    label_done.destroy()
                    label_done_txt.destroy()
                    b_done.destroy()
                    butt_start.destroy()
                    transcript_work()
                    summary_work()

                def do_text_work():
                    l1.destroy()
                    b1.destroy()
                    label_done.destroy()
                    label_done_txt.destroy()
                    b_done.destroy()
                    butt_start.destroy()
                    summary_work()

                b_done.destroy()
                save_file_at_dir(choice, filename)

                x1_value = 260
                t1_value = 'Perform Transcription and Summarization'
                if choice == 'tc':
                    x1_value = 320
                    t1_value = 'Perform Summarization'

                import threading
                butt_start = Button(root, text=t1_value, command=lambda: threading.Thread(target=do_work(choice)).start,
                                    font=my_font3)
                # butt_start = tk.Button(root, text=t1_value, command=lambda: do_work(choice), font=my_font3)
                butt_start.place(x=x1_value, y=410)

            if choice == 'vc':
                f_types = [('Video Files', '*.mp4')]
            if choice == 'ac':
                f_types = [('Audio Files', '*.mp3'),
                           ('Audio Files', '*.wav')]
            if choice == 'tc':
                f_types = [('Text Files', '*.txt')]

            global option_choice
            option_choice=choice

            file = filedialog.askopenfilename(filetypes=f_types)
            if file:
                label_done_txt = tk.Label(root, text=file, font=my_font2, foreground='blue')
                label_done_txt.place(x=200, y=330)
                label_done = tk.Label(root, text='Successful.', width=30, font=my_font2,
                                      foreground='green')
                label_done.place(x=300, y=355)
                b_done = tk.Button(root, text='Upload', width=20, command=lambda: perform_final(choice, file))
                b_done.place(x=330, y=410)
                if choice != 'tc':
                    ws = Tk()
                    ws.title('Audio Language')
                    ws.geometry(f'{300}x{130}+{center_x}+{center_y}')
                    ws.config(bg='#33FF33')

                    def display_selected(choice):
                        global opt
                        opt = variable.get()
                        ws.destroy()

                    countries = ['en-IN', 'en-US']
                    variable = StringVar()
                    variable.set(countries[0])
                    label_lan = Label(ws, bg="#88cffa", text='Select Audio Language:', font=("Helvetica", 14))
                    label_lan.place(x=30, y=10)
                    label_lang = Label(ws, bg="#88cffa", text='Default: en-IN', font=("Helvetica", 8))
                    label_lang.place(x=50, y=50)
                    dropdown = OptionMenu(ws, variable, *countries, command=display_selected)
                    dropdown.pack(expand=True)
                    ws.mainloop()
            else:
                label_done = tk.Label(root, text='No File Chosen', width=30, font=my_font2)
                label_done.place(x=300, y=355)

        video_button.destroy()
        audio_button.destroy()
        text_button.destroy()
        label_opt.destroy()
        my_font1 = ('times', 18, 'bold')
        my_font2 = ('times', 10)
        my_font3 = ('times', 12, 'bold')
        my_font4 = ('times', 15, 'bold')

        if choice == 'vc':
            l1 = tk.Label(root, bg="#88cffa", text='Upload Video File', width=30, font=my_font1)
            l1.place(x=200, y=200)
            b1 = tk.Button(root, text='Choose File', width=20, command=lambda: upload_file_save(choice))
            b1.place(x=330, y=250)
        if choice == 'ac':
            l1 = tk.Label(root, bg="#88cffa", text='Upload Audio File', width=30, font=my_font1)
            l1.place(x=200, y=200)
            b1 = tk.Button(root, text='Choose File', width=20, command=lambda: upload_file_save(choice))
            b1.place(x=330, y=250)
        if choice == 'tc':
            l1 = tk.Label(root, bg="#88cffa", text='Upload Text File', width=30, font=my_font1)
            l1.place(x=200, y=200)
            b1 = tk.Button(root, text='Choose File', width=20, command=lambda: upload_file_save(choice))
            b1.place(x=330, y=250)

    if label_heading1.winfo_exists():
        label_heading1.destroy()
    if label_heading2.winfo_exists():
        label_heading2.destroy()
    if label_heading3.winfo_exists():
        label_heading3.destroy()
    if start_button.winfo_exists():
        start_button.destroy()
    label_heading = Label(root, bg="#88cffa", text='Transcription & Summarization', font=("Helvetica", 37))
    label_heading.place(x=80, y=8)
    label_opt = Label(root, bg="#88cffa", text='Select type of file to upload', font=("Helvetica", 25))
    label_opt.place(x=200, y=160)

    video_button = tk.Button(root, text="Video File", height=2, width=15, command=lambda: upload_file('vc'))
    video_button.place(x=340, y=230)

    audio_button = tk.Button(root, text="Audio File", height=2, width=15, command=lambda: upload_file('ac'))
    audio_button.place(x=340, y=280)

    text_button = tk.Button(root, text="Text File", height=2, width=15, command=lambda: upload_file('tc'))
    text_button.place(x=340, y=330)


clean_video_folder()
clean_audio_folder()
clean_transcripts_folder()
clean_summary_folder()
min_ratio = 0.5
option_choice =''
opt='en-IN'
root = tk.Tk()
root.title('Transcription & Summarization')
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
root.resizable(False, False)
root.iconbitmap('./Assets/logo.ico')
bg = PhotoImage(file="./Assets/background.png")
label_bg = Label(root, image=bg)
label_bg.place(x=-2, y=-2)

label_heading1 = Label(root, bg="#88cffa", text='Transcription', font=("Helvetica", 60))
label_heading1.place(x=170, y=100)
label_heading2 = Label(root, bg="#88cffa", text='&', font=("Helvetica", 60))
label_heading2.place(x=365, y=190)
label_heading3 = Label(root, bg="#88cffa", text='Summarization', font=("Helvetica", 60))
label_heading3.place(x=140, y=280)
start_button = tk.Button(root, text="Start", height=2, width=10, command=callback)
start_button.place(x=360, y=430)

root.mainloop()
