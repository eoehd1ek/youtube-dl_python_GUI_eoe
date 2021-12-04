# youtube-dl GUI helper
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import *  # https://pythonbasics.org/tkinter-filedialog/
import tkinter.font		# 글씨 크기 변경할 때 필요함
import subprocess		# 쉘 명령 결과 반환
import os				# 저장 위치를 알기 위해
import threading		# 새 쓰레드에 다운로드 작업을 지시
import time				# time.sleep(1)을 사용하기 위해
import webbrowser


# 전역 변수
youtube_dl = f"\"{os.getcwd()}\\youtube-dl\""		# youtube-dl 파일 경로


# 메뉴 바 함수
def site_ytdl():
    webbrowser.open("https://ytdl-org.github.io/youtube-dl")


def site_ffmpeg():
    webbrowser.open("https://www.ffmpeg.org")


def ytdl_update():
    subprocess.run(f"{youtube_dl} --update", shell=True)


# 커맨드 실행 target 함수
def download_thread(*shell_cmd):
    for cmd in shell_cmd:
        subprocess.run(cmd)
        time.sleep(0.2)     # 너무 빨리 하면 에러가 날 것 같아서? ㅋㅋ


# 파일을 다운받을 폴더를 설정하는 함수
def set_directory():
    # fileDirectory = asksaveasfile(parent = tk, mode = "w", defaultextension = ".mp4", filetypes = (("MP4 파일", "*.mp4"), ("모든 파일", "*")))
    file_Directory = askdirectory()
    DirectoryUrl.set(file_Directory)  # 저장할 폴더 위치 저장


# 현재 경로를 파일 탐색기에서 열어주는 함수
def open_file_explorer():
    try:
        os.startfile(bsdir)
    except:
        messagebox.showinfo("알림", "폴더 경로명이 잘못되어있습니다.\n존재하지 않는 경로명일 수 있습니다.")


# 쉘 명령어 작성
def clickDownload():
    shell_cmd = []
    target_url = urlEntry.get()

    if (downloadFormat.get() == 1):		# 비디오
        shell_cmd.append(
            f"{youtube_dl} -f bestvideo[ext=mp4]+bestaudio[ext=m4a] -o \"{DirectoryUrl.get()}\\%(title)s.%(ext)s\" {target_url}")

    elif (downloadFormat.get() == 2):  # mp3
        # mp3만 다운로드
        if(addThumbnail.get() == 0):
            if(mp3Quality.get() == 1):
                shell_cmd.append(
                    f"{youtube_dl} -x --audio-format mp3 --audio-quality 0 -o \"{DirectoryUrl.get()}\\%(title)s.%(ext)s\" {target_url}")
            elif(mp3Quality.get() == 2):
                shell_cmd.append(
                    f"{youtube_dl} -x --audio-format mp3 --audio-quality 2 -o \"{DirectoryUrl.get()}\\%(title)s.%(ext)s\" {target_url}")
            elif(mp3Quality.get() == 3):
                shell_cmd.append(
                    f"{youtube_dl} -x --audio-format mp3 --audio-quality 5 -o \"{DirectoryUrl.get()}\\%(title)s.%(ext)s\" {target_url}")

        # 썸네일과 mp3 다운로드
        else:
            if(mp3Quality.get() == 1):
                shell_cmd.append(
                    f"{youtube_dl} -x --audio-format mp3 --audio-quality 0 --write-thumbnail -o \"{DirectoryUrl.get()}\\%(title)s.%(ext)s\" {target_url}")
            elif(mp3Quality.get() == 2):
                shell_cmd.append(
                    f"{youtube_dl} -x --audio-format mp3 --audio-quality 2 --write-thumbnail -o \"{DirectoryUrl.get()}\\%(title)s.%(ext)s\" {target_url}")
            elif(mp3Quality.get() == 3):
                shell_cmd.append(
                    f"{youtube_dl} -x --audio-format mp3 --audio-quality 5 --write-thumbnail -o \"{DirectoryUrl.get()}\\%(title)s.%(ext)s\" {target_url}")

    elif (downloadFormat.get() == 3):  # 고kbps음질 동영상
        # 파일 이름 저장하기
        filename = subprocess.check_output(
            f"{youtube_dl} --get-title {target_url}")
        filename = filename.decode("cp949")
        filename = filename.replace("/", "-")
        filename = filename.replace("\\", "-")
        filename = filename.strip()

        # 파일 id 저장하기 (삭제하기 위해서)
        fileid = subprocess.check_output(f"{youtube_dl} --get-id {target_url}")
        fileid = fileid.decode("cp949")
        fileid = fileid.strip()

        # 비디오 다운로드
        shell_cmd.append(
            f"{youtube_dl} -f bestvideo[ext=mp4] -o \"{os.getcwd()}\\%(id)s.%(ext)s\" {target_url}")

        # 오디오 다운로드
        shell_cmd.append(
            f"{youtube_dl} -x --audio-format mp3 --audio-quality 0 -o \"{os.getcwd()}\\%(id)s.%(ext)s\" {target_url}")

        # 둘이 합치기
        output_path = f"\"{DirectoryUrl.get()}\\{filename}.mp4\""
        shell_cmd.append(
            f"\"{os.getcwd()}\\ffmpeg\" -i {fileid}.mp4 -i {fileid}.mp3 -c copy {output_path}")

    elif(downloadFormat.get() == 4):
        if(eachFiles.get() == 0):  # 비디오만
            shell_cmd.append(
                f"{youtube_dl} -f bestvideo[ext=mp4] -o \"{DirectoryUrl.get()}\\%(title)s.%(ext)s\" {target_url}")

        else:  # 비디오, 영상 따로따로 다운로드
            shell_cmd.append(
                f"{youtube_dl} -f bestvideo[ext=mp4] -o \"{DirectoryUrl.get()}\\%(title)s.%(ext)s\" {target_url}")
            shell_cmd.append(
                f"{youtube_dl} -x --audio-format mp3 --audio-quality 0 -o \"{DirectoryUrl.get()}\\%(title)s.%(ext)s\" {target_url}")

    # 다운로드를 수행하는 쓰레드 생성
    t1 = threading.Thread(target=download_thread,
                          args=(shell_cmd), daemon=True)
    t1.start()


# tkinter GUI 구성 코드
tk = Tk()  # tk 객체 생성
tk.title("youtube-dl GUI Helper Kor By_eoe")
tk.geometry("683x384")						# 프로그램 해상도
tk.resizable(0, 0)							# 화면크기 고정
# tk.configure(background = "#FFFFFF")		# 배경 색상

# 메뉴바 생성 부분
menubar = Menu(tk)

menu_1 = Menu(menubar, tearoff=0)
menubar.add_cascade(label="메뉴 바", menu=menu_1)
# menu_1.add_command(label = "youtube-dl 버전 업데이트", command=ytdl_update)
menu_1.add_command(label="youtube-dl 공식 다운로드 사이트", command=site_ytdl)
menu_1.add_command(label="ffmpeg 공식 다운로드 사이트", command=site_ffmpeg)


tk.config(menu=menubar)  # 메뉴바를 tk에 띄우는 동작


# 폰트 데이터 저장 위치
fontData_url = ("Verdana", 12)
fontData_radioButton_Format = ("Verdana", 12)
fontData_checkButton_Format = ("Verdana", 11)


# "URL" 텍스트 + 주소 입력 창
textLabel_1 = Label(tk, text="URL", justify="right",
                    font=fontData_url)		# URL 텍스트
urlEntry = Entry(tk, width=65, text="", justify='left',
                 font=fontData_url)  # url 입력하는 곳

textLabel_1.place(x=11, y=10)
urlEntry.place(x=13, y=30)


# 동영상, mp3 선택 라디오 부분
downloadFormat = IntVar()  # 뭐지? 라디오 버튼 사용할라면 쓰는건가본데
mp3Quality = IntVar()  # mp3 음질 선택 라디오 버튼

radioMp4 = Radiobutton(tk, text="동영상(MP4)", variable=downloadFormat,
                       value=1, font=fontData_radioButton_Format)
radioMp3 = Radiobutton(tk, text="음악만(MP3)", variable=downloadFormat,
                       value=2, font=fontData_radioButton_Format)
radioHighKbps = Radiobutton(
    tk, text="고kbps음질 동영상", variable=downloadFormat, value=3, font=fontData_radioButton_Format)
radioOnlyVideo = Radiobutton(
    tk, text="소리없이 영상만", variable=downloadFormat, value=4, font=fontData_radioButton_Format)
radioMp4.place(x=10, y=65)
radioMp3.place(x=160, y=65)
radioHighKbps.place(x=310, y=65)
radioOnlyVideo.place(x=500, y=65)

radioMp4.select()

# 썸네일 체크 박스
addThumbnail = IntVar()
eachFiles = IntVar()
checkButtonThumbnail = Checkbutton(
    tk, text="썸네일 다운로드", variable=addThumbnail, font=fontData_checkButton_Format)
checkButtonEachfile = Checkbutton(
    tk, text="영상, 소리 따로", variable=eachFiles, font=fontData_checkButton_Format)
checkButtonThumbnail.place(x=160, y=95)
checkButtonEachfile.place(x=500, y=95)


# mp3 음질 선택 라디오 부분
textLabel_2 = Label(tk, text="※MP3만 음질 선택이 가능합니다.",
                    justify="center", font=fontData_url)
textLabel_2.place(x=10, y=130)

fontData_radioButton_Quality = ("Verdana", 10)
radioQ_Best = Radiobutton(tk, text="Over 256kbps", variable=mp3Quality,
                          value=1, font=fontData_radioButton_Quality)
radioQ_Good = Radiobutton(tk, text="192kbps?", variable=mp3Quality,
                          value=2, font=fontData_radioButton_Quality)
radioQ_Normal = Radiobutton(
    tk, text="128kbps?", variable=mp3Quality, value=3, font=fontData_radioButton_Quality)
radioQ_Best.place(x=10, y=155)
radioQ_Good.place(x=140, y=155)
radioQ_Normal.place(x=240, y=155)

radioQ_Best.select()

# 지정 폴더에 저장 부분
textLabel_3 = Label(tk, text="지정 폴더에 저장", font=fontData_url)
textLabel_3.place(x=10, y=190)

DirectoryUrl = StringVar()
bsdir = os.getcwd()			# bsdir에 'C:/Users/eoehd1ek/Desktop' 식으로 저장됨
DirectoryUrl.set(bsdir)
saveDirectoryEntry = Entry(tk, width=79, text=DirectoryUrl,
                           justify='left', font=("Verdana", 10))  # url 입력하는 곳
saveDirectoryEntry.place(x=12, y=215)


openFileExplorerButton = Button(
    tk, text="폴더열기", width=16, command=open_file_explorer)
openFileExplorerButton.place(x=150, y=190)
openFileButton = Button(tk, text="...", width=2, command=set_directory)
openFileButton.place(x=645, y=215)


# 다운로드 버튼 부분
fontData_downButton = ("Verdana", 12)
downButton = Button(tk, width=20, text="Download", justify="right",
                    font=fontData_downButton, command=clickDownload)  # 클릭시 다운로드
downButton.place(x=235, y=320)

tk.mainloop()
