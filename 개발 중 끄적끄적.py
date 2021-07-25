#### 오디오 파일 변경 ####
###### wav to mp3
ffmpeg -i inputFileName.wav -codec:a libmp3lame -b:a 320k outputFileName.mp3

ffmpeg -i "" -codec:a libmp3lame -b:a 320k ""


###### mp3만 추출 1. mp4 to mp3, [mp4가 aac 코덱을 사용하므로 aac 확장자로 풀면 더 좋은듯]
## aac로 풀고 m4a 로 파일이름 확장자 변경해서 사용하는게 베스트
ffmpeg -i maco.mp4 -vn -acodec copy output.aac

###### mp3만 추출 2. mp3로 재 인코딩,  [아래 방법은 aac에서 mp3로 변경하는 작업을 하므로 시간이 오래 걸림]
ffmpeg -i maco.mp4 -map 0:a -acodec libmp3lame -b:a 192k out.mp3

ffmpeg -i "" -map 0:a -acodec libmp3lame -b:a 320k ""


#### python 파일을 exe 파일로 만들기
pyinstaller
pyinstaller -F -n Youtube-dl_GUI_Helper.exe GUI_main.py

pyinstaller -F -n Rule34Downloader_Kor20200601.exe multiRule34.py


#### 최상의 비디오 다운로드 Download best mp4 format available or any other best if no mp4 available
youtube-dl -f bestvideo[ext=mp4]+bestaudio[ext=m4a]

youtube-dl -f best

1번째로 사용하니 제일 좋은 화질로 받아짐 음질은 128인듯
다른거 사용하면 360p으로 받아짐 병신이네 진짜
		youtube-dl -f bestvideo[ext=mp4]+bestaudio[ext=m4a] --audio-quality 0 ksCl7Lw2kAs
		이거 안되는거 보면 256kbps로 받는 방법 찾기 존나 귀찮을듯 안함 ㅅㄱ


# mp3 파일 다운로드
youtube-dl -x --audio-format mp3 --audio-quality 0 URL

음질 최상0 250 이상
상		 2 
보통 	 5 128kbps

썸네일 앨범 아트 등록
1. 썸네일 같이 다운로드
	--write-thumbnail

2. 저장한 파일 이름을 어디에 저장 (1개면 변수에, 플레이리스트면 리스트에)
	youtube-dl --get-filename URL 	# 파일 전체 이름 ex)name.mp4
	youtube-dl -e URL 
	== --get-title  				# 이름만 받아옴  ex)name
	#결과
	ボーカロイドボサノバメドレー_feat.初音ミク-4vIrjQVcc3U.mp4
	
	다른 확장자가 올 수 있으니 
	filename = get_filename[:-4] .확장자 를 지우고 저장

3. 앨범아트를 넣는 방법을 사용해 파일이름.mp3 와 파일이름.jpg를 합침


# 플레이 리스트 저장할 때 이름 선정 방식 Download YouTube playlist videos in separate directory indexed by video order in a playlist
$ youtube-dl -o '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s' https://www.youtube.com/playlist?list=PLwiyx1dc3P2JR9N8gQaQN_BCvlSlap7re

# 파일 이름 부분
-o '%(title)s.%(ext)s' URL


# 비디오 다운로드
youtube-dl -f bestvideo[ext=mp4]+bestaudio[ext=m4a] -o '%(title)s.%(ext)s' URL

# 오디오 다운로드
youtube-dl -x --audio-format mp3 --audio-quality -o %(title)s.%(ext)s URL + "0" + "URL"

##### 비디오 + 오디오 합치기
ffmpeg -i 동영상이름.확장자 -i 오디오이름.확장자 -c copy 최종추출될파일이름.확장자
"ffmpeg -i " + filename + ".mp4 -i " + filename + ".mp3 -c copy " + filename + "mp4"			(공백 없어야 함!!)
ex :
	ffmpeg -i video.mp4 -i sound.mp3 -c copy result.mp4
	ffmpeg -i video.ts -i audio.aac -c copy video2.ts



업데이트 할 것
    1. youtube-dl 업데이트 명령어 버튼 추가 (메뉴 바로 추가하는게 보기 좋을 것 같음)
        " youtube-dl -U " <- 업데이트 명령어 (안되더라??)
        구 youtube-dl.exe파일은 현재 날짜명을 가진 폴더를 생성하여 추가
    
    # 완료 2. 다운로드 받은 폴더를 여는 버튼 (다운받고 바로 영상 볼려는거 폴더 찾아가기 너무 귀찮음) 
    
    3. UI 수정
		프로그레스 바 추가?
	
	
4vIrjQVcc3U			보컬로이드 보사노바 메들리
nkClzDKzeC0			128인 커넥팅 니코니코 코러스
QgPmL7YuAsw			150인 blessing 니코니코 코러스
ksCl7Lw2kAs			하나땅 첫소리
