from enum import Enum


class DownloadType(Enum):
    NORMAL = 1
    ONLY_MP3 = 2
    HIGH_BITRATE_AUDIO_AND_VIDEO = 3
    ONLY_MP4 = 4
