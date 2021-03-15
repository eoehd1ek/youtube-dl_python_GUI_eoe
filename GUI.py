#youtube-dl GUI helper
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import * # https://pythonbasics.org/tkinter-filedialog/
import tkinter.font		# 글씨 크기 변경할 때 필요함
import subprocess		# 쉘 명령 결과 반환
import os				# 저장 위치를 알기 위해
import sys
import threading		# 새 쓰레드에 다운로드 작업을 지시
import time				# time.sleep(1)을 사용하기 위해
import webbrowser
## import eyed3			# 앨범아트 추가 https://stackoverflow.com/questions/38510694/how-to-add-album-art-to-mp3-file-using-python-3
## eyed3  => "pip install eyeD3"

""" 사용하지 않음
## 앨범아트 관련 정보 출처 https://stackoverflow.com/questions/38510694/how-to-add-album-art-to-mp3-file-using-python-3
## mp3에 앨범아트 넣는 함수
def add_album_art(mp3_url, image_url):
	audiofile = eyed3.load(mp3_url)
	if (audiofile.tag == None):
		audiofile.initTag()

	audiofile.tag.images.set(3, open(image_url, "rb").read(), "image/jpeg")

	audiofile.tag.save()
"""

##################
# == 메뉴 바 함수 == #
def site_ytdl():
	webbrowser.open("https://ytdl-org.github.io/youtube-dl")

def site_ffmpeg():
	webbrowser.open("https://www.ffmpeg.org")

def ytdl_update():
	subprocess.run(youtube_dl + "youtube-dl --update", shell=True)

# ====      ==== #
##################

## 새 쓰레드에 다운로드 작업을 지시해 GUI를 멈추게 하지 않음
def download_thread(*shell_cmd):
	for i in range(len(shell_cmd)):
		subprocess.run(shell_cmd[i])	
		time.sleep(0.2)					## 너무 빨리 하면 에러가 날 것 같아서? ㅋㅋ
	
## 파일을 다운받을 폴더를 설정하는 함수
def set_directory():	
	# fileDirectory = asksaveasfile(parent = tk, mode = "w", defaultextension = ".mp4", filetypes = (("MP4 파일", "*.mp4"), ("모든 파일", "*")))
	file_Directory = askdirectory()
	DirectoryUrl.set(file_Directory)		## 저장할 폴더 위치 저장

## 현재 경로를 파일 탐색기에서 열어주는 함수
def open_file_explorer():
	try:
		os.startfile(bsdir)
	except:
		messagebox.showinfo("알림", "폴더 경로명이 잘못되어있습니다.\n존재하지 않는 경로명일 수 있습니다.")
	
##쉘 명령어 작성
def clickDownload():
	isError = 0
	shell_cmd = []
	
	if (downloadFormat.get() == 1):		# 비디오
		shell_cmd.append(youtube_dl + "youtube-dl -f bestvideo[ext=mp4]+bestaudio[ext=m4a] -o "+ DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
	
	elif (downloadFormat.get() == 2):	# mp3
		# mp3 다운로드
		if(addThumbnail.get() == 0):
			if(mp3Quality.get() == 1):
				shell_cmd.append(youtube_dl + "youtube-dl -x --audio-format mp3 --audio-quality 0 -o "+ DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
			elif(mp3Quality.get() == 2):
				shell_cmd.append(youtube_dl + "youtube-dl -x --audio-format mp3 --audio-quality 2 -o "+ DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
			elif(mp3Quality.get() == 3):
				shell_cmd.append(youtube_dl + "youtube-dl -x --audio-format mp3 --audio-quality 5 -o "+ DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
		
		# 썸네일과 mp3 다운로드
		else:
			if(mp3Quality.get() == 1):
				shell_cmd.append(youtube_dl + "youtube-dl -x --audio-format mp3 --audio-quality 0 --write-thumbnail -o "+ DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
			elif(mp3Quality.get() == 2):
				shell_cmd.append(youtube_dl + "youtube-dl -x --audio-format mp3 --audio-quality 2 --write-thumbnail -o "+ DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
			elif(mp3Quality.get() == 3):
				shell_cmd.append(youtube_dl + "youtube-dl -x --audio-format mp3 --audio-quality 5 --write-thumbnail -o "+ DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
				
	elif (downloadFormat.get() == 3):	# 고kbps음질 동영상
		"""
		# tmp 폴더 생성
		if(not (os.path.exists(os.getcwd() + "\\tmp"))):	## 현재 폴더에 tmp 폴더가 없을 경우 새 tmp 폴더 생성
			os.makedirs("tmp")
		"""
		
		#파일 이름 저장하기
		filename = subprocess.check_output(youtube_dl + "youtube-dl --get-title " + urlEntry.get())
		filename = filename.decode("cp949")
		filename = filename.replace("/", "-")
		filename = filename.replace("\\", "-")
		filename = filename.strip()
		
		#파일 id 저장하기 (삭제하기 위해서)
		fileid = subprocess.check_output(youtube_dl + "youtube-dl --get-id " + urlEntry.get())
		fileid = fileid.decode("cp949")
		fileid = fileid.strip()
		
		# 비디오 다운로드
		shell_cmd.append(youtube_dl + "youtube-dl -f bestvideo[ext=mp4] -o " + youtube_dl + "%(id)s.%(ext)s " + urlEntry.get())
		
		# 오디오 다운로드
		shell_cmd.append(youtube_dl + "youtube-dl -x --audio-format mp3 --audio-quality 0 -o " + youtube_dl + "%(id)s.%(ext)s " + urlEntry.get())
		
		# 둘이 합치기
		output_path = '"' + youtube_dl + filename + '.mp4"'
		shell_cmd.append(youtube_dl + "ffmpeg -i " + fileid + ".mp4 -i " + fileid + ".mp3 -c copy " + output_path)
		
		"""
		# 파일 이동
		shell_cmd.append("move " + youtube_dl + fileid + ".mp3 " + youtube_dl + "tmp\\" + fileid + ".mp3")
		shell_cmd.append("move " + youtube_dl + fileid + ".mp4 " + youtube_dl + "tmp\\" + fileid + ".mp4")
		"""
		
	elif(downloadFormat.get() == 4):
		if(eachFiles.get() == 0):	#비디오만
			shell_cmd.append(youtube_dl + "youtube-dl -f bestvideo[ext=mp4] -o " + DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
		
		else:	#비디오, 영상 따로따로 다운로드
			shell_cmd.append(youtube_dl + "youtube-dl -f bestvideo[ext=mp4] -o " + DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
			shell_cmd.append(youtube_dl + "youtube-dl -x --audio-format mp3 --audio-quality 0 -o "+ DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
			

	## 다운로드를 수행하는 쓰레드 생성
	t1 = threading.Thread(target=download_thread, args=(shell_cmd))
	t1.daemon = True
	t1.start()

#########################
# === GUI 구성 코드 부분 === #
#########################
tk = Tk()									##tk 객체 생성
tk.title("youtube-dl GUI Helper Kor By_eoe")
tk.geometry("683x384")						# 프로그램 해상도
tk.resizable(0, 0)							# 화면크기 고정
##tk.configure(background = "#FFFFFF")		# 배경 색상

#### 메뉴바 생성 부분
menubar = Menu(tk)

menu_1 = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "메뉴 바", menu = menu_1)
## menu_1.add_command(label = "youtube-dl 버전 업데이트", command=ytdl_update)
menu_1.add_command(label = "youtube-dl 공식 다운로드 사이트", command=site_ytdl)
menu_1.add_command(label = "ffmpeg 공식 다운로드 사이트", command=site_ffmpeg)


tk.config(menu = menubar)		## 메뉴바를 tk에 띄우는 동작



#### 폰트 데이터 저장 위치
fontData_url = ("Verdana", 12)
fontData_radioButton_Format = ("Verdana", 12)
fontData_checkButton_Format = ("Verdana", 11)


#### "URL" 텍스트 + 주소 입력 창
textLabel_1 = Label(tk, text = "URL", justify = "right", font = fontData_url)		# URL 텍스트
urlEntry = Entry(tk, width = 65, text = "", justify='left', font = fontData_url )	# url 입력하는 곳

textLabel_1.place(x = 11, y = 10)
urlEntry.place(x = 13, y = 30)




#### 동영상, mp3 선택 라디오 부분
downloadFormat = IntVar()						#뭐지? 라디오 버튼 사용할라면 쓰는건가본데
mp3Quality = IntVar()							#mp3 음질 선택 라디오 버튼

radioMp4 = Radiobutton(tk, text="동영상(MP4)", variable = downloadFormat, value = 1, font = fontData_radioButton_Format)
radioMp3 = Radiobutton(tk, text="음악만(MP3)", variable = downloadFormat, value = 2, font = fontData_radioButton_Format)
radioHighKbps = Radiobutton(tk, text="고kbps음질 동영상", variable = downloadFormat, value = 3, font = fontData_radioButton_Format)
radioOnlyVideo = Radiobutton(tk, text="소리없이 영상만", variable = downloadFormat, value = 4, font = fontData_radioButton_Format)
radioMp4.place(x = 10, y = 65)
radioMp3.place(x = 160, y = 65)
radioHighKbps.place(x = 310, y = 65)
radioOnlyVideo.place(x = 500, y = 65)

radioMp4.select()

#### 썸네일 체크 박스
addThumbnail = IntVar()
eachFiles = IntVar()
checkButtonThumbnail = Checkbutton(tk, text = "썸네일 다운로드", variable = addThumbnail, font = fontData_checkButton_Format)
checkButtonEachfile = Checkbutton(tk, text = "영상, 소리 따로", variable = eachFiles, font = fontData_checkButton_Format)
checkButtonThumbnail.place(x = 160, y = 95)
checkButtonEachfile.place(x = 500, y = 95)


#### mp3 음질 선택 라디오 부분
textLabel_2 = Label(tk, text = "※MP3만 음질 선택이 가능합니다.", justify = "center", font = fontData_url)
textLabel_2.place(x = 10, y = 130)

fontData_radioButton_Quality = ("Verdana", 10)
radioQ_Best = Radiobutton(tk, text = "Over 256kbps", variable = mp3Quality, value = 1, font = fontData_radioButton_Quality)
radioQ_Good = Radiobutton(tk, text = "192kbps?", variable = mp3Quality, value = 2, font = fontData_radioButton_Quality)
radioQ_Normal = Radiobutton(tk, text = "128kbps?", variable = mp3Quality, value = 3, font = fontData_radioButton_Quality)
radioQ_Best.place(x = 10, y = 155)
radioQ_Good.place(x = 140, y = 155)
radioQ_Normal.place(x = 240, y = 155)

radioQ_Best.select()

#### 지정 폴더에 저장 부분
textLabel_3 = Label(tk, text = "지정 폴더에 저장", font = fontData_url)
textLabel_3.place(x = 10, y = 190)

DirectoryUrl = StringVar()
youtube_dl = os.getcwd() + "\\"
bsdir = os.getcwd()			# bsdir에 'C:/Users/eoehd1ek/Desktop' 식으로 저장됨
DirectoryUrl.set(bsdir)
saveDirectoryEntry = Entry(tk, width = 79, text = DirectoryUrl, justify='left', font = ("Verdana", 10))	#url 입력하는 곳
saveDirectoryEntry.place(x = 12, y = 215)



openFileExplorerButton = Button(tk, text = "폴더열기", width = 16, command= open_file_explorer)
openFileExplorerButton.place(x = 150, y = 190)
openFileButton = Button(tk, text = "...", width = 2, command = set_directory)
openFileButton.place(x = 645, y = 215)


#### 다운로드 버튼 부분
fontData_downButton = ("Verdana", 12)
downButton = Button(tk, width = 20, text = "Download", justify = "right", font = fontData_downButton, command = clickDownload)		#클릭시 다운로드
downButton.place(x = 235, y = 320)

tk.mainloop()