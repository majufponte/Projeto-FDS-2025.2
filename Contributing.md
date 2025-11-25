# 🤝 Contribuindo com o Ecos do Fim

Olá! 👋 Que bom ter você por aqui.  
Se você está pensando em contribuir com o projeto **Ecos do Fim**, seja muito bem-vindo!  
Este guia contém tudo o que você precisa para começar a colaborar com o nosso desenvolvimento.

---

## 🧰 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python**
- **Git**
- **Visual Studio Code (VSCode)**

---

## 🚀 Configurando o Ambiente

Siga os passos abaixo para rodar o projeto localmente:

### **1. Clone o repositório**

Abra seu terminal, navegue até o diretório onde deseja salvar o projeto e execute:

- `git clone https://github.com/majufponte/Projeto-FDS-2025.2.git`

### **2. Acesse o diretório do projeto**

- `cd Projeto-FDS-2025.2`

### **3. Crie e ative um ambiente virtual**

Instale o virtualenv caso ainda não tenha:

- `pip install virtualenv`

Crie o ambiente virtual:

- `python -m venv venv`

Ative o ambiente:

- **Windows:** `venv/Scripts/activate`  
- **macOS/Linux:** `source venv/bin/activate`

### **4. Instale as dependências**

Com o ambiente virtual ativado, instale as dependências:

- `pip install -r requirements.txt`

### **5. Execute as migrações**

Crie as migrações do banco:

- `python manage.py makemigrations`

Aplique as migrações:

- `python manage.py migrate`

> 💡 Em alguns ambientes, você pode precisar usar `py` no lugar de `python`.

### **6. Inicie o servidor de desenvolvimento**

Execute:

- `python manage.py runserver`

Acesse o projeto no navegador:

- **http://localhost:8000/**

---

## 🧑‍💻 Contribuindo com Código

Recomendamos utilizar o **VSCode**.

Para abrir o projeto:

1. Abra o VSCode  
2. Vá em **File > Open Folder…**  
3. Escolha o diretório do projeto **Ecos do Fim**  
4. Certifique-se de que o ambiente virtual está ativado no terminal integrado  

Após concluir suas alterações:

- Faça seus commits  
- Abra um **Pull Request**  

---

## 🔍 Processo de Revisão

Todos os PRs enviados passarão por análise.  
Apenas serão aceitos aqueles que:

- Estiverem coerentes com a proposta do projeto  
- Forem bem estruturados  
- Seguírem as boas práticas descritas neste documento  

---

## 📏 Diretrizes de Desenvolvimento

Para manter o projeto organizado e fácil de evoluir, siga estas recomendações:

- Use boas práticas de codificação em **Python, HTML, CSS e JavaScript**  
- Mantenha o código bem identado  
- Organize corretamente os **imports**  
- Adicione comentários úteis quando necessário  
- Nomeie arquivos, funções, classes e variáveis de forma clara e objetiva  

---

## ❓ Dúvidas?

Se tiver dúvidas, sugestões ou encontrar algum problema, fique à vontade para abrir uma **issue** no repositório.  
Estamos felizes em ter você contribuindo! 🚀
