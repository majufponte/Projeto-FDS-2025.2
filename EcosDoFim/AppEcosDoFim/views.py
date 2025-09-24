from django.shortcuts import render

def escolher_dificuldade(request):
    niveis = [1, 2, 3, 4]  

    if request.method == "POST":
        dificuldade_escolhida = request.POST.get("dificuldade")
        print("Dificuldade escolhida:", dificuldade_escolhida)#aqui e so pra ligar co o html
        

    return render(request, "escolher_dificuldade.html", {"niveis": niveis})


 #considerações pra maju: aqui esse def ele funciona pra gente seleciona a dificuldade do jogo
 #o objetivo aqui é que la na frente quandoa a gente for trabalhar com o Dcbs ja tenha a dificuldade do jogo estabelecida
