#youtube-dl GUI helper
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import * # https://pythonbasics.org/tkinter-filedialog/
import tkinter.font		# 글씨 크기 변경할 때 필요함
import subprocess		# 쉘 명령 결과 반환
import os				# 저장 위치를 알기 위해
import eyed3			# 앨범아트 추가 https://stackoverflow.com/questions/38510694/how-to-add-album-art-to-mp3-file-using-python-3

## eyed3  => "pip install eyeD3"

## 앨범아트 관련 https://stackoverflow.com/questions/38510694/how-to-add-album-art-to-mp3-file-using-python-3
def add_album_art(mp3_url, image_url):
	## mp3에 앨범아트 넣는 함수
	audiofile = eyed3.load(mp3_url)
	if (audiofile.tag == None):
		audiofile.initTag()

	audiofile.tag.images.set(3, open(image_url, "rb").read(), "image/jpeg")

	audiofile.tag.save()

def set_directory():
	# 파일을 다운받을 폴더를 설정하는 함수
	# fileDirectory = asksaveasfile(parent = tk, mode = "w", defaultextension = ".mp4", filetypes = (("MP4 파일", "*.mp4"), ("모든 파일", "*")))
	file_Directory = askdirectory()
	DirectoryUrl.set(file_Directory)		## 저장할 폴더 위치 저장

def open_file_explorer():
	## 현재 경로를 파일 탐색기에서 열어주는 함수
	try:
		os.startfile(bsdir)
	except:
		messagebox.showinfo("알림", "폴더 경로명이 잘못되어있습니다.\n존재하지 않는 경로명일 수 있습니다.")
	
def clickDownload():	#쉘 명령어 작성
	isError = 0
	if (downloadFormat.get() == 1):		# 비디오
		os.system(youtube_dl + "youtube-dl -f bestvideo[ext=mp4]+bestaudio[ext=m4a] -o "+ DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
	
	elif (downloadFormat.get() == 2):	# mp3
		#썸네일 없이 mp3 다운로드
		if(addThumbnail.get() == 0):
			if(mp3Quality.get() == 1):
				os.system(youtube_dl + "youtube-dl -x --audio-format mp3 --audio-quality 0 -o "+ DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
			elif(mp3Quality.get() == 2):
				os.system(youtube_dl + "youtube-dl -x --audio-format mp3 --audio-quality 2 -o "+ DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
			elif(mp3Quality.get() == 3):
				os.system(youtube_dl + "youtube-dl -x --audio-format mp3 --audio-quality 5 -o "+ DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
		
		#썸네일을 추가하여 mp3 다운로드
		else:
			try:
				#파일 이름 저장하기
				filename = subprocess.check_output(youtube_dl + "youtube-dl --get-title " + urlEntry.get())
				filename = filename.decode("cp949")
				filename = filename.replace("/", "-")
				filename = filename.replace("\\", "-")
				filename = filename.strip()
				filename = filename.split("\n")
				
				#파일 id 저장하기 (삭제하기 위해서)
				fileid = subprocess.check_output(youtube_dl + "youtube-dl --get-id " + urlEntry.get())
				fileid = fileid.decode("cp949")
				fileid = fileid.strip()
				fileid = fileid.split("\n")
				
				if(mp3Quality.get() == 1):
					os.system(youtube_dl + "youtube-dl -x --audio-format mp3 --audio-quality 0 --write-thumbnail -o "+ DirectoryUrl.get() + "\\%(id)s.%(ext)s " +urlEntry.get())
				elif(mp3Quality.get() == 2):
					os.system(youtube_dl + "youtube-dl -x --audio-format mp3 --audio-quality 2 --write-thumbnail -o "+ DirectoryUrl.get() + "\\%(id)s.%(ext)s " +urlEntry.get())
				elif(mp3Quality.get() == 3):
					os.system(youtube_dl + "youtube-dl -x --audio-format mp3 --audio-quality 5 --write-thumbnail -o "+ DirectoryUrl.get() + "\\%(id)s.%(ext)s " +urlEntry.get())
			
				for i in range(len(filename)):
					if(not (os.path.exists(filename[i] + "mp3")) ):		# mp3 파일이 다운받아져 있지 않을 경우에만
						fileid_url = DirectoryUrl.get() + "\\" + fileid[i]
						filename_url = DirectoryUrl.get() + "\\" + filename[i]
						
						add_album_art(fileid_url + ".mp3", fileid_url + ".jpg")	#썸네일 추가				
						os.rename(fileid_url + ".mp3", filename_url + ".mp3")		# id인 이름에서 영상제목으로 이름 변경
					
					os.remove(fileid_url + ".jpg")	##앨범아트 추가 후 이미지 파일 삭제
			except:
				isError = 1
				messagebox.showinfo("알림", "해당 링크는 앨범아트 포함 mp3 다운로드가 지원되지 않습니다.\n재생 목록일 경우 개별 다운로드를 진행해 주세요")
				pass
				
	elif (downloadFormat.get() == 3):	# 고kbps음질 동영상
		try:
			#파일 이름 저장하기
			filename = subprocess.check_output(youtube_dl + "youtube-dl --get-title " + urlEntry.get())
			filename = filename.decode("cp949")
			filename = filename.replace("/", "-")
			filename = filename.replace("\\", "-")
			filename = filename.strip()
			filename = filename.split("\n")
			
			#파일 id 저장하기 (삭제하기 위해서)
			fileid = subprocess.check_output(youtube_dl + "youtube-dl --get-id " + urlEntry.get())
			fileid = fileid.decode("cp949")
			fileid = fileid.strip()
			fileid = fileid.split("\n")
			
			#비디오 다운로드
			os.system(youtube_dl + "youtube-dl -f bestvideo[ext=mp4] -o " + youtube_dl + "%(id)s.%(ext)s " + urlEntry.get())
			
			#오디오 다운로드
			os.system(youtube_dl + "youtube-dl -x --audio-format mp3 --audio-quality 0 -o " + youtube_dl + "%(id)s.%(ext)s " + urlEntry.get())
			
			#둘이 합치기
			for i in range(len(filename)):
				if(not (os.path.exists(filename[i] + ".mp4")) ): # mp4 파일이 다운받아져 있지 않을 경우에만
					output_path = '"' + filename[i] + '.mp4"'
					os.system(youtube_dl + "ffmpeg -i " + fileid[i] + ".mp4 -i " + fileid[i] + ".mp3 -c copy " + output_path)
				
				# fileid.mp3,mp4 파일 삭제 
				os.remove(fileid[i] + ".mp3")
				os.remove(fileid[i] + ".mp4")
		except:
			isError = 1
			messagebox.showinfo("알림", "오류가 발생했습니다.\n고음질 비디오 다운로드를 다시 시도해주세요.\계속해서 오류 발생시 일반 동영상 다운로드로 시도해주세요.")
			pass
	
	elif(downloadFormat.get() == 4):
		try:
			if(eachFiles.get() == 0):
				#비디오만
				os.system(youtube_dl + "youtube-dl -f bestvideo[ext=mp4] -o " + DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
			
			else:
				#비디오, 영상 따로따로 다운로드
				os.system(youtube_dl + "youtube-dl -f bestvideo[ext=mp4] -o " + DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
				os.system(youtube_dl + "youtube-dl -x --audio-format mp3 --audio-quality 0 -o "+ DirectoryUrl.get() + "\\%(title)s.%(ext)s " + urlEntry.get())
		except:
			isError = 1
			messagebox.showinfo("알림", "해당 링크의 다운로드가 지원되지 않습니다.\n재생 목록일 경우 개별 다운로드를 진행해 주세요")
			pass
			
	if(isError == 0): #try 부분 오류가 안났을 경우 출력
		messagebox.showinfo("알림", "다운로드가 완료되었습니다.")

########################################################
######## 메인코드 실행 부분 #################################
########################################################
tk = Tk()									##tk 객체 생성
tk.title("youtube-dl GUI Helper Kor_eoe")
tk.geometry("683x384")						# 프로그램 해상도
tk.resizable(0, 0)							# 화면크기 고정
##tk.configure(background = "#FFFFFF")		# 배경 색상

#### 메뉴바 생성 부분
menubar = Menu(tk)

menu_1 = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "메뉴 바(현 미완)", menu = menu_1)
menu_1.add_command(label = "youtube-dl 버전 업데이트")
menu_1.add_command(label = "youtube-dl 공식 다운로드 사이트")
menu_1.add_command(label = "ffmpeg 공식 다운로드 사이트")


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
checkButtonThumbnail = Checkbutton(tk, text = "썸네일 추가", variable = addThumbnail, font = fontData_checkButton_Format)
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