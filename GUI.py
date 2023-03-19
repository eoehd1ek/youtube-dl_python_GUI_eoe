# youtube-dl GUI helper
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
import tkinter.font		# 글씨 크기 변경할 때 필요함
import os				# 저장 위치를 알기 위해
import webbrowser

from audio_bitrate import AudioBitrate
from download_type import DownloadType
import download_util


# 메뉴 바 함수
def on_click_open_ytdlp_download_menu():
    webbrowser.open("https://github.com/yt-dlp/yt-dlp/releases")


def on_click_open_ffmpeg_download_menu():
    webbrowser.open("https://www.ffmpeg.org")

# 파일을 다운받을 폴더를 설정하는 함수


def on_click_select_file_saved_path_button():
    # fileDirectory = asksaveasfile(parent = tk, mode = "w", defaultextension = ".mp4", filetypes = (("MP4 파일", "*.mp4"), ("모든 파일", "*")))
    file_saved_path = askdirectory()
    global file_saved_path_value
    file_saved_path_value.set(file_saved_path)


# 현재 경로를 파일 탐색기에서 열어주는 함수
def on_click_open_file_saved_path_button():
    try:
        global file_saved_path_value
        os.startfile(file_saved_path_value.get())
    except:
        messagebox.showinfo("알림", "존재하지 않는 폴더 경로입니다.")


# 쉘 명령어 작성
def on_click_start_download_button():
    global download_url_value
    global file_saved_path_value
    global selected_download_type_value
    global selected_mp3_quality_type_value

    target_url = download_url_value.get()
    if not target_url:
        print("URL 항목 값이 비어있습니다.")

    path_to_save = file_saved_path_value.get()
    selected_download_type = selected_download_type_value.get()
    if (selected_download_type == DownloadType.NORMAL.value):
        download_util.normal_download(target_url, path_to_save)
    elif (selected_download_type == DownloadType.ONLY_MP3.value):
        download_util.only_mp3_download(
            target_url, path_to_save, selected_mp3_quality_type_value.get())

        ''' 썸네일과 mp3 다운로드
        else:
            if (selected_mp3_quality_type == 1):
                shell_cmd.append(
                    f"{youtube_dl} -x --audio-format mp3 --audio-quality 0 --write-thumbnail -o \"{file_saved_path_value.get()}\\%(title)s.%(ext)s\" {target_url}")
            elif (selected_mp3_quality_type == 2):
                shell_cmd.append(
                    f"{youtube_dl} -x --audio-format mp3 --audio-quality 2 --write-thumbnail -o \"{file_saved_path_value.get()}\\%(title)s.%(ext)s\" {target_url}")
            elif (selected_mp3_quality_type == 3):
                shell_cmd.append(
                    f"{youtube_dl} -x --audio-format mp3 --audio-quality 5 --write-thumbnail -o \"{file_saved_path_value.get()}\\%(title)s.%(ext)s\" {target_url}")
        '''
    elif (selected_download_type == DownloadType.HIGH_BITRATE_AUDIO_AND_VIDEO.value):
        download_util.high_bitrate_download(
            target_url, path_to_save, selected_mp3_quality_type_value.get())
    elif (selected_download_type == DownloadType.ONLY_MP4.value):
        print("리팩토리 과정 중, 사용 빈도가 낮아 현재 미지원")
        '''
        shell_cmd.append(
            f"{youtube_dl} -f bestvideo[ext=mp4] -o \"{file_saved_path_value.get()}\\%(title)s.%(ext)s\" {target_url}")
        '''

        '''  
        # 비디오, 영상 따로 둘 다 다운로드
            shell_cmd.append(
                f"{youtube_dl} -f bestvideo[ext=mp4] -o \"{file_saved_path_value.get()}\\%(title)s.%(ext)s\" {target_url}")
            shell_cmd.append(
                f"{youtube_dl} -x --audio-format mp3 --audio-quality 0 -o \"{file_saved_path_value.get()}\\%(title)s.%(ext)s\" {target_url}")
        '''


tk: Tk = None
file_saved_path_value: StringVar = None
download_url_value: StringVar = None
selected_download_type_value: IntVar = None
selected_mp3_quality_type_value: IntVar = None
selected_is_additional_download_thumbnail_value: IntVar = None


def init_tkinter():
    # tkinter GUI 구성 코드
    global tk
    tk = Tk()
    tk.title("yt-dlp GUI Helper Kor By_eoe")
    tk.geometry("683x384")
    tk.resizable(False, False)
    # 배경 색상 설정
    # tk.configure(background = "#FFFFFF")


def draw_ui():
    # 메뉴바 생성
    menubar = Menu(tk)
    open_site_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="필수 파일 다운로드 사이트", menu=open_site_menu)
    '''open_site_menu.add_command(
        label="youtube-dl 공식 사이트", command=on_click_open_ytdlp_download_menu)'''
    open_site_menu.add_command(
        label="yt-dlp 공식 깃허브", command=on_click_open_ytdlp_download_menu)
    open_site_menu.add_command(
        label="ffmpeg 공식 사이트", command=on_click_open_ffmpeg_download_menu)

    # 윈도우에 메뉴바 등록
    tk.config(menu=menubar)

    # 폰트 데이터 저장 위치
    download_type_radiobutton_fontdata = ("Verdana", 12)
    fontData_checkButton_Format = ("Verdana", 11)

    # 다운로드할 영상의 주소 입력 창
    url_label_fontdata = ("Verdana", 12)
    url_label = Label(tk, text="URL", justify="right",
                      font=url_label_fontdata)		# URL 텍스트
    url_entry_fontdata = ("Verdana", 12)
    global download_url_value
    download_url_value = StringVar()
    url_entry = Entry(tk, width=65, text=download_url_value, justify='left',
                      font=url_entry_fontdata)  # url 입력하는 곳
    url_label.place(x=11, y=10)
    url_entry.place(x=13, y=30)

    # 다운로드 타입 선택 부분
    global selected_download_type_value
    selected_download_type_value = IntVar()
    global selected_mp3_quality_type_value
    selected_mp3_quality_type_value = IntVar()  # mp3 음질 선택 라디오 버튼

    download_type_mp4_radio = Radiobutton(tk, text="동영상(MP4)", variable=selected_download_type_value,
                                          value=DownloadType.NORMAL.value, font=download_type_radiobutton_fontdata)
    download_type_mp3_radio = Radiobutton(tk, text="음악만(MP3)", variable=selected_download_type_value,
                                          value=DownloadType.ONLY_MP3.value, font=download_type_radiobutton_fontdata)
    download_type_high_bitrate_radio = Radiobutton(tk, text="고kbps음질 동영상", variable=selected_download_type_value,
                                                   value=DownloadType.HIGH_BITRATE_AUDIO_AND_VIDEO.value, font=download_type_radiobutton_fontdata)
    download_type_only_mp4_radio = Radiobutton(tk, text="소리없이 영상만", variable=selected_download_type_value,
                                               value=DownloadType.ONLY_MP4.value, font=download_type_radiobutton_fontdata)
    download_type_mp4_radio.place(x=10, y=65)
    download_type_mp3_radio.place(x=160, y=65)
    download_type_high_bitrate_radio.place(x=310, y=65)
    download_type_only_mp4_radio.place(x=500, y=65)

    download_type_mp4_radio.select()

    # 썸네일 체크 박스
    global selected_is_additional_download_thumbnail_value
    selected_is_additional_download_thumbnail_value = IntVar()
    # TODO eachFiles 체크박스 옵션은 없애고  영상, 소리 따로 받기 옵션 만들기
    eachFiles = IntVar()
    additional_download_thumbnail_check = Checkbutton(
        tk, text="썸네일 다운로드", variable=selected_is_additional_download_thumbnail_value, font=fontData_checkButton_Format)
    download_file_each_other_check = Checkbutton(
        tk, text="영상, 소리 따로", variable=eachFiles, font=fontData_checkButton_Format)
    additional_download_thumbnail_check.place(x=160, y=95)
    download_file_each_other_check.place(x=500, y=95)

    # mp3 음질 선택 라디오 부분
    select_audio_bitrate_label_fontdata = ("Verdana", 12)
    select_audio_bitrate_label = Label(tk, text="※ 음악만(MP3), 고음질 동영상 옵션의 음질 비트레이트",
                                       justify="center", font=select_audio_bitrate_label_fontdata)
    select_audio_bitrate_label.place(x=10, y=130)

    select_audio_level_radio_fontdata = ("Verdana", 10)
    audio_bitrate_best_radio = Radiobutton(tk, text="Over 256kbps", variable=selected_mp3_quality_type_value,
                                           value=AudioBitrate.BEST.value, font=select_audio_level_radio_fontdata)
    audio_bitrate_good_radio = Radiobutton(tk, text="192kbps?", variable=selected_mp3_quality_type_value,
                                           value=AudioBitrate.GOOD.value, font=select_audio_level_radio_fontdata)
    audio_bitrate_normal_radio = Radiobutton(tk, text="128kbps?", variable=selected_mp3_quality_type_value,
                                             value=AudioBitrate.NORMAL.value, font=select_audio_level_radio_fontdata)
    audio_bitrate_best_radio.place(x=10, y=155)
    audio_bitrate_good_radio.place(x=140, y=155)
    audio_bitrate_normal_radio.place(x=240, y=155)

    audio_bitrate_best_radio.select()

    # 저장 경로 설정 부분
    download_path_label_fontdata = ("Verdana", 12)
    download_path_label = Label(
        tk, text="파일 저장 경로", font=download_path_label_fontdata)
    download_path_label.place(x=10, y=190)

    global file_saved_path_value
    file_saved_path_value = StringVar()
    bsdir = os.getcwd()			# bsdir에 'C:/Users/eoehd1ek/Desktop' 식으로 저장됨
    file_saved_path_value.set(bsdir)
    file_saved_path_entry_fontdata = ("Verdana", 10)
    file_saved_path_entry = Entry(tk, width=79, text=file_saved_path_value,
                                  justify='left', font=file_saved_path_entry_fontdata)  # url 입력하는 곳
    file_saved_path_entry.place(x=12, y=215)

    open_file_saved_path_button = Button(
        tk, text="저장 폴더 열기", width=16, command=on_click_open_file_saved_path_button)
    open_file_saved_path_button.place(x=150, y=190)
    select_file_saved_path_button = Button(
        tk, text="...", width=2, command=on_click_select_file_saved_path_button)
    select_file_saved_path_button.place(x=645, y=215)

    # 다운로드 버튼 부분
    start_download_button_fontdata = ("Verdana", 12)
    start_download_button = Button(tk, width=20, text="Download", justify="right",
                                   font=start_download_button_fontdata, command=on_click_start_download_button)  # 클릭시 다운로드
    start_download_button.place(x=235, y=320)

    tk.mainloop()
