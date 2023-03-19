import os
import subprocess
import threading

YTDLP_FILE_NAME = "yt-dlp.exe"
FFMPEG_FILE_NAME = "ffmpeg.exe"
COMMANDS_TO_CHANGE_TEXT_ENCODING = "chcp 65001"


def get_wrapped_string_by_quote(s: str) -> str:
    return f"\"{s}\""


def get_ytdlp_file_path() -> str:
    return get_wrapped_string_by_quote(os.path.join(os.getcwd(), YTDLP_FILE_NAME))


def get_ffmpeg_file_path() -> str:
    return get_wrapped_string_by_quote(os.path.join(os.getcwd(), FFMPEG_FILE_NAME))


# 파일명으로 사용할 수 없는 반각 문자를 비슷한 전각 문자로 변경
def get_convert_char_fullwidth(string: str) -> str:
    string = string.replace("\\", "＼")
    string = string.replace("/", "／")
    string = string.replace(":", "：")
    string = string.replace("*", "＊")
    string = string.replace("?", "？")
    string = string.replace("\"", "＂")
    string = string.replace("<", "＜")
    string = string.replace(">", "＞")
    string = string.replace("|", "｜")
    return string


def single_download_thread(command: str):
    subprocess.run(COMMANDS_TO_CHANGE_TEXT_ENCODING, shell=True)
    subprocess.run(command, shell=True)
    print(command)


def normal_download(download_url: str, path_to_save: str):
    file_name_to_save = get_wrapped_string_by_quote(
        os.path.join(path_to_save, "%(title)s.%(ext)s"))
    download_url = get_wrapped_string_by_quote(download_url)
    command = f"{get_ytdlp_file_path()} -f bestvideo[ext=mp4]+bestaudio[ext=m4a] -o {file_name_to_save} {download_url}"
    # args= 항목이 모두 분할되어 들어가기 때문에 튜플로 전달.
    thread = threading.Thread(target=single_download_thread,
                              args=((command,)), daemon=True)
    thread.start()


def only_mp3_download(download_url: str, path_to_save: str, selected_audio_bitrate: int):
    file_name_to_save = get_wrapped_string_by_quote(
        os.path.join(path_to_save, "%(title)s.%(ext)s"))
    download_url = get_wrapped_string_by_quote(download_url)
    command = f"{get_ytdlp_file_path()} -x --audio-format mp3 --audio-quality {selected_audio_bitrate} -o {file_name_to_save} {download_url}"
    # args= 항목이 모두 분할되어 들어가기 때문에 튜플로 전달.
    thread = threading.Thread(target=single_download_thread,
                              args=((command,)), daemon=True)
    thread.start()


def high_bitrate_download(download_url: str, path_to_save: str, selected_audio_bitrate: int):
    subprocess.run(COMMANDS_TO_CHANGE_TEXT_ENCODING, shell=True)
    video_id = subprocess.check_output(
        f"{get_ytdlp_file_path()} --get-id {download_url}").decode("cp949").strip()
    video_title = subprocess.check_output(
        f"{get_ytdlp_file_path()} --get-title {download_url}").decode("cp949").strip()
    video_title = get_convert_char_fullwidth(video_title)
    file_name_to_save = get_wrapped_string_by_quote(
        os.path.join(path_to_save, f"{video_title}.mp4"))
    id_name_to_save = get_wrapped_string_by_quote(
        os.path.join(path_to_save, "%(id)s.%(ext)s"))

    only_video_download_command = f"{get_ytdlp_file_path()} -f bestvideo[ext=mp4] -o {id_name_to_save} {download_url}"
    only_audio_download_command = f"{get_ytdlp_file_path()} -x --audio-format mp3 --audio-quality {selected_audio_bitrate} -o {id_name_to_save} {download_url}"
    vidio_download_thread = threading.Thread(target=single_download_thread, args=(
        (only_video_download_command,)), daemon=True)
    vidio_download_thread.start()
    audio_download_thread = threading.Thread(target=single_download_thread, args=(
        (only_audio_download_command,)), daemon=True)
    audio_download_thread.start()

    vidio_download_thread.join()
    audio_download_thread.join()

    merge_command = f"{get_ffmpeg_file_path()} -i {video_id}.mp4 -i {video_id}.mp3 -c copy {file_name_to_save}"
    file_merge_thread = threading.Thread(
        target=single_download_thread, args=((merge_command,)), daemon=True)
    file_merge_thread.start()
