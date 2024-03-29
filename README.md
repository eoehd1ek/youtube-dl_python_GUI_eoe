# youtube-dl 프로그램을 편하게 사용할려고 GUI로 만들었습니다.

이 프로그램은 선택한 옵션에 맞는 youtube-dl 커맨드를 대신 입력해주는 프로그램입니다.  
[youtube-dl GUI Helper Download(go to releases page)](https://github.com/eoehd1ek/youtube-dl_python_GUI_eoe/releases)

ffmpeg 프로그램과 youtube-dl 프로그램이 있어야 사용 가능하며 다운로드는 다음 링크에서 받을 수 있습니다.

- ~~[youtube-dl Download](http://ytdl-org.github.io/youtube-dl/download.html)~~ (업데이트 종료로 미사용)
- [yt-dlp Download](https://github.com/yt-dlp/yt-dlp/releases/)
- [ffmpeg Download](https://ffmpeg.org/download.html)

## program preview

<img src="https://user-images.githubusercontent.com/49092390/126894929-73481415-10b5-441e-a775-72396192a90c.png" width="600" height="378">

### 2023-3-20 업데이트
1. youtube-dl -> yt-dlp로 사용 프로그램 변경  
   youtube-dl 프로그램이 21년부터 지원 종료되어 사용하는 프로그램을 변경했습니다.  
   영상이 다운로드 되지 않는 버그가 고쳐졌습니다.
   yt-dlp 찬양해~

2. 소스코드 리펙토링을 진행했습니다.  
   옛날에 쓴 코드 컨벤션 실화냐.

### 2021-12-04 업데이트

1. 폴더 이름에 공백이 존재하면 다운로드가 정상 작동하지 않는 버그 해결  
   \\\"경로명\\\" 과 같이 따옴표로 묶어주어 해결함

### 2021-03-16 업데이트

1. 이제 다운로드 버튼을 눌러도 프로그램이 멈추지 않아 한 프로그램에서 여러 다운로드를 수행할 수 있습니다. 와~ 너무좋아!  
   다운로드 버튼을 누르면 새로운 쓰레드를 생성하고 이 쓰레드에서 youtube-dl 명령어를 사용합니다.  
   다운로드 버튼을 눌러도 프로그램 창이 멈추지 않기 때문에 다운로드 버튼을 여러번 누르지 않도록 조심해 주세요.

2. 이제 다운로드 완료 알림이 뜨지 않습니다. 앞으론 콘솔 창을 잘 확인하세요!  
   이전에는 다운로드가 완료되고 알림창이 떴습니다.  
   그런데 이번 업데이트를 하면서 알림창을 띄우면 불편할 것 같다 생각하여 완료 알림창을 삭제했습니다.  
   youtube와의 연결 끊김으로 인한 다운로드 실패를 알려주지 않으니 다운로드 후 콘솔 창에 완료 메세지를 확인해주세요.

3. 메뉴바를 추가하고 있습니다. 뭘 넣어야 하지?  
   우선 youtube-dl과 ffmpeg의 공식 사이트를 여는 기능을 추가했습니다.  
   지금까진 제가 쓰기에 불편한 점 없이 매우 만족하니 다른 기능을 추가할진 모르겠네요.

4. 썸네일 추가 다운로드도 생겼습니다. 음악 파일에 앨범아트를 추가해보세요.  
   음악만(MP3) 옵션을 선택하고 썸네일 다운로드 부분을 체크하면 해당 영상의 썸네일도 함께 받아집니다.  
   mp3에 앨범아트를 추가하는 프로그램을 사용하여 앨범아트를 넣어보세요~
