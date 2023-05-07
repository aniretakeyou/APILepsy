import cv2
import cv2 as cv
from PIL import Image, ImageEnhance
import numpy as np
from moviepy.editor import *
import moviepy.editor as mp

def func_brightness(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    return np.mean(gray)

def mse(img1, img2): # Mean Square Error - Средний квадрат ошибки
   h, w = img1.shape[:2]
   diff = cv.subtract(img1, img2)
   err = np.sum(diff**2)
   mse = err/(float(h*w))
   return mse

def mse1(img1, img2): # Mean Square Error - Средний квадрат ошибки
   h, w = img1.shape[:2]
   diff = cv.subtract(img2, img1)
   err = np.sum(diff**2)
   mse = err/(float(h*w))
   return mse


name = input()
video = cv2.VideoCapture(name)  # считываем видеофайл
video_1 = cv2.VideoCapture("disclaimer.mp4")

# создание объекта VideoFileClip
videozvuk = mp.VideoFileClip(name)
audio = videozvuk.audio


# определяем длину видефайла
video_length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# определяем фреймрейт(кадры в секунду)
fps = int(video.get(cv2.CAP_PROP_FPS))

count = 1
lst = []
previous_frame = []
buffer = []
critical_difference = 100
k = 0

while True:
    is_read, frame = video.read()
    if not is_read:
        # выйти из цикла, если нет фреймов для чтения
        break
    frame_name = f"{count}.jpg"
    frame_1 = frame
    if count > 1:
        print(mse(previous_frame, frame))
        print(mse1(previous_frame, frame))
        if mse(previous_frame, frame) > critical_difference or mse1(previous_frame, frame) > critical_difference or func_brightness(frame) > 200:
            lst.append(count)
            k += 1
            im = Image.fromarray(frame)
            enhancer = ImageEnhance.Brightness(im)
            factor = 0.1
            frame = np.array(enhancer.enhance(factor))
            buffer.append(frame)
            print(f"{frame_name} сохранён")
        else:
            buffer.append(frame)
            print(f"{frame_name} сохранён")
    else:
        buffer.append(frame)
        print(f"{frame_name} сохранён")
    previous_frame = frame_1.copy()
    count += 1
print(k)
m = 0
if k / count * 100 < 5:
    for i in range(len(lst) - 10):
        if (abs(lst[i + j] - lst[i + j + 1]) == 1 for j in range(2)) or (abs(lst[i + j] - lst[i + j + 1]) == 2 for j in range(2)):
            m += 1
print(m)
if m > 0 or k / count * 100 > 5:
    # начало создания нового видео
    height, width, channels = buffer[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter("result.avi", fourcc, fps, (width, height))

    # запись кадров из буфера в новое видео
    for frame in buffer:
        video_writer.write(frame)

    cv2.destroyAllWindows()
    video_writer.release()

    # конец создания нового видео
    video1 = VideoFileClip("disclaimer.mp4")
    video2 = VideoFileClip("result.avi")
    # соединение аудиодорожки и видео
    video2 = video2.set_audio(audio)
    resized_video1 = video1.resize((width, height))
    resized_video2 = video2.resize((width, height))

    videos = [resized_video1, resized_video2]  # объединение предупреждения и нового видео

    final_video = concatenate_videoclips(videos, method="compose")
    final_video.write_videofile("3.mp4")  # конечное видео
if (k == 0) or (k / count * 100 < 5 and m == 0):
    print("Видео безопасно для просмотра!")
