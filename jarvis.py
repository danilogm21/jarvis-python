import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import datetime
import threading
import tkinter as tk
import math

engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)

intensidade_fala = 0

def falar(texto):
    global intensidade_fala
    print(f"JARVIS: {texto}")
    
    intensidade_fala = 1.0
    engine.say(texto)
    engine.runAndWait()
    intensidade_fala = 0.0

def ouvir():
    rec = sr.Recognizer()
    with sr.Microphone() as mic:
        print("\n[Ouvindo...]")
        rec.adjust_for_ambient_noise(mic, duration=0.8)    
        try:
            audio = rec.listen(mic, timeout=5, phrase_time_limit=5)
            texto = rec.recognize_google(audio, language="pt-BR")
            print(f"VOCÊ DISSE: {texto}")
            return texto.lower()
        except (sr.UnknownValueError, sr.WaitTimeoutError):
            return ""
        except sr.RequestError:
            falar("Erro de conexão com a internet.")
            return ""

def executar_comando(comando):
    if "horas" in comando:
        hora_atual = datetime.datetime.now().strftime("%H:%M")
        falar(f"Agora são {hora_atual}.")

    elif "abrir youtube" in comando:
        falar("Abrindo o Youtube.")
        webbrowser.open("https://www.youtube.com")

    elif "abrir navegador" in comando or "pesquisar" in comando:
        falar("Abrindo o navegador.")
        webbrowser.open("https://www.google.com")

    elif "bloco de notas" in comando:
        falar("Abrindo o Bloco de Notas.")
        os.system("notepad")

    elif "desligar" in comando or "parar" in comando or "fechar" in comando:
        falar("Desligando sistemas. Até logo!")
        janela.after(1000, janela.destroy)
        return False

    elif comando != "":
        falar("Ainda não tenho um comando configurado para isso.")        
    
    return True

def iniciar_jarvis():
    falar("Sistemas inicializados. Estou à sua disposição.")
    executando = True

    while executando:
        comando_usuario = ouvir()

        if comando_usuario != "":
            executando = executar_comando(comando_usuario)

janela = tk.Tk()
janela.title("J.A.R.V.I.S.")
janela.geometry("500x500")
janela.configure(bg="#03070d")

canvas = tk.Canvas(janela, width=500, height=500, bg="#03070d", highlightthickness=0)
canvas.pack(fill="both", expand=True)

centro_x, centro_y = 250, 250
angulo = 0

def desenhar_orbe():
    global angulo
    canvas.delete("holograma")
    
    raio_base = 80 + (intensidade_fala * 35) + (math.sin(angulo * 0.1) * 5)
    
    canvas.create_oval(centro_x - raio_base - 40, centro_y - raio_base - 40, 
                       centro_x + raio_base + 40, centro_y + raio_base + 40, 
                       outline="#ff7700", width=1, dash=(15, 10), tags="holograma")
    
    canvas.create_oval(centro_x - raio_base - 20, centro_y - raio_base - 20, 
                       centro_x + raio_base + 20, centro_y + raio_base + 20, 
                       outline="#ffaa00", width=2, tags="holograma")
    
    canvas.create_oval(centro_x - raio_base, centro_y - raio_base, 
                       centro_x + raio_base, centro_y + raio_base, 
                       outline="#ff5500", width=3, dash=(5, 5), tags="holograma")

    canvas.create_oval(centro_x - 30, centro_y - 30, 
                       centro_x + 30, centro_y + 30, 
                       fill="#ff8800", outline="#ffeecc", width=2, tags="holograma")

    angulo += 3
    janela.after(30, desenhar_orbe)

desenhar_orbe()

thread_jarvis = threading.Thread(target=iniciar_jarvis, daemon=True)
thread_jarvis.start()

janela.mainloop()