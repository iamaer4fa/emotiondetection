import subprocess

command = "C:\emotionapp\emotion\Lib\site-packages\deep_audio_features\bin\basic_test.py -m c:\emotionapp\emotion\pkl\model_all.pt -i c:\emotionapp\test1.wav"

subprocess.run(command, shell=True)  
