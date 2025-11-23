from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from .models import DetecaoAudio,locais_explorado,Jogador,Itens,Inventario,Partida
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import random

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
            return redirect('/login')
    else:
        redirect('/')
        
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            return redirect('/login/')

    return render(request, 'register.html')

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

@login_required(login_url='login_user')
def mapa(request):
    id_partida = request.session.get('id_partida')
    if not id_partida:
        return redirect("criar_partida")

    partida = get_object_or_404(Partida, id=id_partida)

    usuario = request.user if request.user.is_authenticated else None

    explorados = list(locais_explorado.objects.filter(
        usuario=usuario
    ).values_list("id_do_local", flat=True))

    if request.method == "POST":
        id_do_local = int(request.POST.get("id_do_local"))
        locais_explorado.objects.create(
            usuario=usuario,
            partida=partida,
            id_do_local=id_do_local
        )

        return redirect("jogo_audio")  

    return render(request, 'mapa.html', {"explorados": explorados})


def home(request):
    return render(request,"inicial.html")

@login_required(login_url='login_user')
def criar_personagem(request):
    id_partida = request.session.get('id_partida')
    if not id_partida:
        return redirect('escolher_partida')

    partida = get_object_or_404(Partida, id=id_partida)
    if request.method== "POST":
        usuario=request.user
        nome=request.POST.get("nome")
        Jogador.objects.get_or_create(usuario=usuario,partida=partida,nome=nome)
    return render(request,"criar_personagem.html")
    
def criar_itens(request):
    if request.method== "POST":
        nome=request.POST.get("nome")
        tipo=request.POST.get("tipo")
        descricao=request.POST.get("descricao")
        Itens.objects.get_or_create(nome=nome,tipo=tipo,descricao=descricao)
    return render(request,"criar_itens.html")

@login_required(login_url='login_user')
def escolher_personagem(request):
    usuario=request.user
    id_partida = request.session.get('id_partida')
    #bonecos é equivalente a personagens, coloquei assim para ficar mais legivel
    bonecos = Jogador.objects.filter(usuario=usuario, partida_id=id_partida)

    if not bonecos.exists():
        return redirect("criar_personagem")

    if request.method=="POST":
        id_personagem=request.POST.get("id_personagem")
        personagem=get_object_or_404(Jogador,id=id_personagem,usuario=usuario)
        request.session['id_personagem']=personagem.id

        return redirect("testar_dificuldade")
    return render(request, "escolher_personagem.html", {"personagens": bonecos})

def pegar_item(request):
    id_personagem = request.session.get('id_personagem')
    id_partida = request.session.get('id_partida')
    if not id_partida:
        return redirect("criar_partida")
    if not id_personagem:
        return redirect("escolher_personagem")
    jogador=get_object_or_404(Jogador,id=id_personagem, partida=id_partida,usuario=request.user)
    partida=get_object_or_404(Partida, id=id_partida)
    itens=list(Itens.objects.all())
    item_ganho=random.choice(itens)
    Inventario.objects.create(jogador=jogador,partida=partida, item=item_ganho)

    return redirect('mapa')

@login_required(login_url='login_user')
def criar_partida(request):
    if request.method == "POST":
        Nome_partida=request.POST.get("local")
        partida = Partida.objects.create(nome=Nome_partida)
        request.session['id_partida'] = partida.id
        return redirect('escolher_personagem')
    return render(request,'criar_partida.html')

def ver_inventario(request):
    id_personagem=request.session.get('id_personagem')
    jogador =get_object_or_404(Jogador,id=id_personagem,usuario=request.user)
    inventario= Inventario.objects.filter(jogador=jogador)

    return render(request, "inventario.html", {"jogador": jogador, "inventario": inventario})

@login_required(login_url='login_user')
def escolher_partida(request):
    usuario=request.user
    partidas=Partida.objects.all()
    if not partidas.exists():
        return redirect("criar_partida")

    if request.method=="POST":
        id_partida=request.POST.get("id_partida")
        partida=get_object_or_404(Partida,id=id_partida)
        request.session['id_partida']=partida.id

        return redirect("escolher_personagem")
    return render(request, "escolher_partida.html", {"partidas": partidas})

def jogo_audio(request):
    return render(request, "jogo_audio_personagem.html")


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