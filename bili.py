import requests
import re
import json
import subprocess
import os


###
default = 1
target_url = 'https://www.bilibili.com/video/BV1Gv4y1S7Zp/?spm_id_from=333.999.0.0&vd_source=26b8648980045bfe830e75a93987fede'
output_file_name = '随机的'
headers = {
    #'content-type': 'text/html; charset=utf-8',
    'referer': 'https://www.bilibili.com/',
    "origin": "https://www.bilibili.com",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

if default == 1:
    target_url = input("Enter the whole url link of your requesting Bilibili video page: ")
    output_file_name = input("What name do you want for this video?: ")
    user_cookie = input("Enter your current bilibili video page cookie(find in readme file, otherwise video is 360p. if no, just leave it blank): ")
    if user_cookie == '':
        headers = {
            #'content-type': 'text/html; charset=utf-8',
            'referer': 'https://www.bilibili.com/',
            "origin": "https://www.bilibili.com",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        }
    else:
        headers = {
            #'content-type': 'text/html; charset=utf-8',
            'referer': 'https://www.bilibili.com/',
            "origin": "https://www.bilibili.com",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            "Cookie": f"{user_cookie}"
        }

response = requests.get(target_url,headers=headers)
if response.status_code != 200:
    print("Cookie or url problem. exiting...")
    exit()

html_data = response.text

#zhengze
play_info = re.findall('window.__playinfo__=(.*?)</script>', html_data)[0]
#with open('bilitest.txt',"w") as file:
#    file.write(play_info)

json_data = json.loads(play_info) #dict type
#print(json_data)
video = json_data['data']['dash']['video'][0]['baseUrl']
audio = json_data['data']['dash']['audio'][0]['baseUrl']

print("Start Downloading.....")
video_data = requests.get(video,headers=headers).content
with open('tempv.mp4',"wb") as f:
    f.write(video_data)

audio_data = requests.get(audio,headers=headers).content
with open('tempa.mp3',"wb") as f:
    f.write(audio_data)

print("Download Done!\nCombining video and audio...")
ffmpeg = f'ffmpeg -i tempv.mp4 -i tempa.mp3 -acodec copy -vcodec copy {output_file_name+".mp4"}'
subprocess.run(ffmpeg)
os.remove('tempv.mp4')
os.remove('tempa.mp3')

#print(json_data)