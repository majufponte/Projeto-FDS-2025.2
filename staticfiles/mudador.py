import os
import re

for nome in os.listdir('.'):
    # Procura número entre parênteses
    m = re.search(r'\((\d+)\)', nome)
    if m:
        numero = m.group(1)

        # verifica se o nome contém "ecos" e "telas" em qualquer formato
        if "ecos" in nome.lower() and "telas" in nome.lower():

            # pega a extensão correta (inclusive PNG maiúsculo)
            _, ext = os.path.splitext(nome)

            novo = f"Carta_num-{numero}{ext}"
            os.rename(nome, novo)
            print(f"{nome}  ->  {novo}")

print("Concluído!")
