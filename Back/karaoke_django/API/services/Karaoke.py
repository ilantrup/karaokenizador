import os

from django.conf import settings
from pytube import YouTube
from moviepy.editor import *
from spleeter.separator import Separator
import librosa
import numpy as np
import soundfile as sf
import requests
import googleapiclient.discovery
import shutil
from pygame import mixer
import time
import cv2
from moviepy.editor import VideoFileClip, AudioFileClip, clips_array


API_KEY = 'AIzaSyA2fuJQvbacMNYatVgHSr57hsbIsdejC2Q'

SERVICES_ROOT = os.path.dirname(os.path.abspath(__file__))


def crear_carpeta(nombre_carpeta):
  ruta_completa = os.path.join(SERVICES_ROOT, nombre_carpeta)
  print("la ruta completa es: ", ruta_completa)
  try:
    os.mkdir(ruta_completa)
    print(f"La carpeta '{nombre_carpeta}' se ha creado exitosamente.")
  except OSError as error:
    print(f"Error al crear la carpeta: {error}")

def karaokenizador(url, directory):
  
  # Download the video
  yt = YouTube(url)
  stream = yt.streams.get_highest_resolution()
  title = stream.title.replace("(", "").replace(")", "").replace("/", " ").replace("|", "").replace('"', "")

  stream.download(filename=f"{title}.mp4", output_path=directory)

  # Extract the audio
  video = VideoFileClip(f"{directory}/{title}.mp4")
  audio = video.audio
  audio.write_audiofile(f"{directory}/{title}.mp3")
  # Delete the downloaded video file
  try:
    separateSong(title, directory)
  except:
    print("")
  video.close()
  audio.close()
  os.remove(f"{directory}/{title}.mp3")
  return title


def separateSong(filename, directory):
  separator = Separator('spleeter:2stems')
  audio, sr = librosa.load(f"{directory}/{filename}.mp3", sr=None)
  audio_estereo = np.column_stack((audio, audio))
  separation = separator.separate(audio_estereo)
  for stem_name, stem_audio in separation.items():
    stem_filename = f"{directory}/{filename}_{stem_name}.wav"  
    sf.write(stem_filename, stem_audio, sr, closefd=True)
  print("se separo la cancion")


def buscar_video_por_titulo(titulo):
  youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)

  request = youtube.search().list(
    q=titulo,
    type='video',
    part='id',
    maxResults=1  
  )

  response = request.execute()

  if 'items' in response and len(response['items']) > 0:
    video_id = response['items'][0]['id']['videoId']
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    return video_url
  else:
    return None


def reemplazar_espacios_con_mas(cadena):
  cadena_reemplazada = cadena.replace(" ", "+")
  return cadena_reemplazada

def reemplazar_barras_con_espacios(cadena):
    return cadena.replace("/", " ")


def reproducir_acompanamento(ruta):
  archivos_en_directorio = os.listdir(ruta)
  for archivo in archivos_en_directorio:
    if archivo.endswith("accompaniment.wav"):
      mixer.init()
      mixer.music.load(f"{ruta}/{archivo}")
      mixer.music.play()
      while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(1)


def reproducir_video(ruta):
  archivos_en_directorio = os.listdir(ruta)
  for archivo in archivos_en_directorio:
    if archivo.endswith(".mp4"):
      cap = cv2.VideoCapture(f"{ruta}/{archivo}")
      #check if the video capture is open
      if(cap.isOpened() == False):
        print("Error Opening Video Stream Or File")
      while(cap.isOpened()):
        ret, frame =cap.read()
        if ret == True:
          cv2.imshow('frame', frame)
          if cv2.waitKey(25)  == ord('q'):
            break
        else:
          break
      cap.release()
      cv2.destroyAllWindows()


def reproductor(ruta):
  archivos_en_directorio = os.listdir(ruta)
  for archivo in archivos_en_directorio:
    if archivo.endswith(".mp4"):
      video_clip = VideoFileClip(os.path.join(ruta,archivo))
    elif archivo.endswith("accompaniment.wav"):
      audio_clip = AudioFileClip(os.path.join(ruta,archivo))

  directorio_api = os.path.dirname(SERVICES_ROOT)
  directorio_back = os.path.dirname(directorio_api)
  directorio_media = os.path.join(directorio_back, "media")
  directorio_videos = os.path.join(directorio_media, "videos")

  final_clip = video_clip.set_audio(audio_clip)
  try:
    os.remove(f"{directorio_videos}/output.mp4")
  except:
    pass
  final_clip.write_videofile(f"{directorio_videos}/output.mp4", codec="libx264", audio_codec="aac")

  #final_clip.preview()
  audio_clip.close()
  final_clip.close()
  video_clip.close()
  



def funcion_completa(titulo):
  #titulo = str(input("Ingresar cancion que se desea buscar: "))
  #while titulo != "fin":
  direc_actual = SERVICES_ROOT
  crear_carpeta(titulo)
  direc_des = os.path.join(direc_actual, titulo)
  link = buscar_video_por_titulo(f"{titulo} lyrics")
  #print(link)
  title = karaokenizador(link, direc_actual)
  mover(direc_actual, direc_des)
  reproductor(direc_des)
  shutil.rmtree(direc_des)

  #os.remove(f"{title}.mp4")
  #titulo = str(input("Ingresar cancion que se desea buscar: "))



def mover(directorio_origen, directorio_destino):
  extensiones = ['.wav', '.mp4']
  archivos_en_directorio = os.listdir(directorio_origen)
  for archivo in archivos_en_directorio:
    for extension in extensiones:
      if archivo.endswith(extension):
        ruta_origen = os.path.join(directorio_origen, archivo)
        ruta_destino = os.path.join(directorio_destino, archivo)
        try:
          shutil.move(ruta_origen, ruta_destino)
          print(f'Se movió {archivo} a {directorio_destino}')
        except Exception as e:
          print(f'Error al mover {archivo}: {e}')

"""
if __name__ == "__main__":
  funcion_completa()
"""