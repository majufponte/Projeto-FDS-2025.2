from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
import sounddevice as sd
import numpy as np
from .models import DetecaoAudio,locais_explorado
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return  redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username,password=password)
        if usuario is not None:
            login(request,usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuario ou senha invalido")
            return redirect('/')
    else:
        redirect('/')

LIMIARES = {
    "1": -50,
    "2": -40,
    "3": -35,
    "4": -30,
}
# sujeito a alterações esse valores  a media que a gente for textando o jogo
def escolher_dificuldade(request):
    niveis = [1, 2, 3, 4]

    if request.method == "POST":
        dificuldade_escolhida = request.POST.get("dificuldade")  
        limiar = LIMIARES.get(dificuldade_escolhida)
        print("Nível escolhido:", dificuldade_escolhida, "→ limiar:", limiar)

      
        request.session["limiar_dificuldade"] = limiar


    return render(request, "escolher_dificuldade.html", {"niveis": niveis})

 #considerações pra maju: aqui esse def ele funciona pra gente seleciona a dificuldade do jogo
 #o objetivo aqui é que la na frente quandoa a gente for trabalhar com o Dcbs ja tenha a dificuldade do jogo estabelecida


def testar_dificuldade(request): #Podemos rodardo lado do cliente com JS
    limiar = request.session.get("limiar_dificuldade")
    if request.user.is_authenticated:
        usuario = request.user
    else:
        usuario=None


    if request.method == "POST":
        detectado = request.POST.get("audio_detectado", "0")
        detectado_bool = bool(int(detectado))

        DetecaoAudio.objects.create(
            usuario=usuario,
            detectado=detectado_bool
        )
    return render(request, "testar_dificuldade.html", {"limiar": limiar})

def mapa(request):
    if request.user.is_authenticated:
        usuario = request.user
    else:
        usuario=None
    explorados=list(locais_explorado.objects.filter(
        usuario=usuario
        ).values_list("id_do_local",flat=True))
    if request.method=="POST":
        id_do_local=int(request.POST.get("id_do_local"))
        locais_explorado.objects.create(
            usuario=usuario,
            id_do_local=id_do_local
            )
        return HttpResponseRedirect(request.path_info)
        

    return render(request, "mapa.html", {"explorados": explorados})

def home(request):
    return render(request,"inicial.html")





"""def detector_audio(limiar):
    print(sd.query_devices())

    DURATION = 0.01 # aqui tbm ta sujeito a alteraçoes isso ai é o tempo que eleme da valor de audio 
    FS = 44100 # ao meu entedimento isso faz parte da captção de audio tipo frequencia (coisa de maluco)
    sd.default.device = 0

    def dbfs(audio_data):
        rms = np.sqrt(np.mean(audio_data.flatten()**2))
        return -np.inf if rms == 0 else 20 * np.log10(rms)

    try:
        while True:
            audio = sd.rec(int(DURATION * FS), samplerate=FS, channels=1, dtype='float64')
            sd.wait()
            decibels = dbfs(audio)
            print(f"Nível de som: {decibels:.2f} dBFS")

            if decibels > limiar:   
                print("Detecção!")

    except KeyboardInterrupt:
        print("\nPrograma finalizado.")

        #falta um html pra esse def mas ele ta aqui pq vai servir de base pra gente começar a trabalhar com o audio
        #sujeito a alteraçoes """