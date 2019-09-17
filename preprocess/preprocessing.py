# 영상 -> 오디오  |  json 에서 발화시작, 종료시간별로 오디오 클립 분할 + bad data제거 (bad sampled)
#
#
# sample rate, encoding error 거르는 전처리예시 https://github.com/homink/speech.ko


'''
1. json frame별로 오디오 클립 분할
2. bad data제거
'''

# y index 넣어서 start frame ~
# scipy
# meta data : wave path, emotion label 저장

# matplotlib for displaying the output
import matplotlib.pyplot as plt


# and IPython.display for audio output
import IPython.display

# Librosa for audio
import librosa
# And the display module for visualization
import librosa.display

class preprocessing :
	def __init__(self):

    def transforma(audio_path):
        #audio_path list 받아서 for 문으로 넣을 수 있게
        audio_path = '/Users/stella/dev/korean-audio-sentiment-analysis/model/data/clip_13/clip_13.mp4' #자동화
        y, sr = librosa.load(audio_path)
        y_save.append(y)
        sr_save.append(sr)


        return y_save, sr_save


