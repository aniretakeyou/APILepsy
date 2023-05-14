import cv2
import cv2 as cv
from PIL import Image, ImageEnhance
import numpy as np
from moviepy.editor import *
import moviepy.editor as mp

# Функция для определения яркости кадра
def func_brightness(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    return np.mean(gray)

# Функция для определения среднеквадратичной ошибки между двумя изображениями
def mse(img1, img2):
   h, w = img1.shape[:2]
   diff = cv.subtract(img1, img2)
   err = np.sum(diff**2)
   mse = err/(float(h*w))
   return mse

# Функция для определения среднеквадратичной ошибки между двумя изображениями в обратном порядке
def mse1(img1, img2):
   h, w = img1.shape[:2]
   diff = cv.subtract(img2, img1)
   err = np.sum(diff**2)
   mse = err/(float(h*w))
   return mse

# считываем видеофайл
name = input()
video = cv2.VideoCapture(name)

# Создаем объект VideoFileClip для получения аудиодорожки видеофайла
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
critical_difference = 40
k = 0

# Цикл по всем кадрам видеофайла
while True:
    is_read, frame = video.read()
    if not is_read:
        # Выходим из цикла, если нет фреймов для чтения
        break
    frame_name = f"{count}.jpg"
    frame_1 = frame
    if count > 1:
        # Определяем среднеквадратичную ошибку между текущим и предыдущим кадром, а также определяем яркость текущего кадра
        if mse(previous_frame, frame) > critical_difference or mse1(previous_frame, frame) > critical_difference or func_brightness(frame) > 200:
            # Если среднеквадратичная ошибка или яркость выше порогового значения, то добавляем номер кадра в список lst, увеличиваем счетчик k
            # затемняем кадр и добавляем его в список buffer
            lst.append(count)
            k += 1
            im = Image.fromarray(frame)
            enhancer = ImageEnhance.Brightness(im)
            factor = 0.1
            frame = np.array(enhancer.enhance(factor))
            buffer.append(frame)
        else:
            # Иначе просто добавляем текущий кадр в список buffer
            buffer.append(frame)
    else:
        # Если это первый кадр, то просто добавляем его в список buffer
        buffer.append(frame)
    previous_frame = frame_1.copy()
    count += 1
m = 0
# Определяем количество "опасных" кадров и проверяем, является ли видео безопасным для просмотра
if k / count * 100 < 40:
    for i in range(len(lst) - 50):
        if all(abs(lst[i + j] - lst[i + j + 1]) in (1, 2) for j in range(49)):
            m += 1
if m > 0 or k / count * 100 > 40:
    # Если видео опасно для просмотра, то создаем новое видео с уменьшенной яркостью опасных кадров и предупреждением, добавляем аудиодорожку
    # начало создания нового видео
    height, width, channels = buffer[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter("result.avi", fourcc, fps, (width, height))

    # запись кадров из буфера в новое видео
    for frame in buffer:
        video_writer.write(frame)
    video_writer.release()

    if height > width: # проверяем, сделано видео под вертикальный просмотр или горизонтальный
        video1 = VideoFileClip("disclaimer_for_vertical.mp4")
    else:
        video1 = VideoFileClip("disclaimer.mp4")
    # Соединяем предупреждение и новое видео, добавляем аудиодорожку и сохраняем конечное видео
    video2 = VideoFileClip("result.avi")
    # соединение аудиодорожки и видео
    video2 = video2.set_audio(audio)
    resized_video1 = video1.resize((width, height))
    resized_video2 = video2.resize((width, height))

    videos = [resized_video1, resized_video2]  # объединение предупреждения и нового видео

    final_video = concatenate_videoclips(videos, method="compose")
    final_video.write_videofile("safe_video.mp4")  # конечное видео
    os.remove("result.avi") # удаление затемненного видео без предупреждения
if (k == 0) or (k / count * 100 < 40 and m == 0):
    # Если видео безопасно для просмотра, то выводим соответствующее сообщение
    print("Видео безопасно для просмотра!")
