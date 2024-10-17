import streamlit as st
import pandas as pd
import requests

BASE_URL = "https://aps-3-flask-rest-mongo-haseduu.onrender.com"
def fazer_requisicao(endpoint, method="GET", params=None, data=None):
    # Constrói a URL completa concatenando o endpoint específico com a base URL
    url = f"{BASE_URL}/{endpoint}"

    # Monta a requisição de acordo com o método HTTP fornecido
    try:
        if method == "GET":
            response = requests.get(url, params=params)
            # Método GET: Envia os parâmetros da requisição (params) como query strings na URL.
            # Exemplo: /imoveis?tipo_imovel=Casa&preco_min=200000&preco_max=1000000

        elif method == "POST":
            response = requests.post(url, json=data)
            # Método POST: Envia os dados no corpo da requisição em formato JSON para criar novos recursos no backend.
            # Exemplo: POST /imoveis para criar um novo imóvel, enviando os detalhes no corpo da requisição.

        elif method == "PUT":
            response = requests.put(url, json=data)
            # Método PUT: Envia os dados no corpo da requisição em formato JSON para atualizar um recurso existente.

        elif method == "DELETE":
            response = requests.delete(url, params=params)
            # Método DELETE: Envia parâmetros na URL para deletar um recurso específico no backend.

        else:
            st.error("Método HTTP não suportado.")
            # Caso um método HTTP não suportado seja passado, exibe um erro no frontend do Streamlit.
        # Verifica o status HTTP da resposta
        if response.status_code == 200:
            return response.json()  # Resposta 200 (OK): Retorna o corpo da resposta como um JSON (dicionário Python).
        elif response.status_code == 404:
            st.error("⚠️ Recurso não encontrado")
            # Se o status for 404 (Not Found), exibe um aviso de que o recurso não foi encontrado.
        elif response.status_code == 500:
            st.error("⚠️ Erro interno do servidor.")
            # Se o status for 500 (Internal Server Error), exibe um erro genérico de servidor.
        else:
            st.error(f"⚠️ Erro: {response.status_code} - {response.text}")
            # Para outros códigos de status, exibe um erro genérico mostrando o código e a mensagem da resposta.

        return None  # Se não houver sucesso, retorna None para indicar falha.

    except Exception as e:
        st.error(f"⚠️ Erro de conexão: {e}")
        # Captura e exibe exceções, como erros de conexão ou outros problemas ao tentar fazer a requisição.
        return None




def intro():
    import streamlit as st

    st.write("# Bem vindo ao nosso serviço de empréstimos de bicicletas 👋")
    st.sidebar.success("Selecione uma função acima")

    st.markdown(
        """
        O nosso serviço permite conectar bicicletas à possíveis usuários

        👈 Selecione qualquer função ao lado

    """
    )

def buscar_usuario():
    st.title("Pesquisar Usuarios")
    id = st.text_input("Digite o ID do usuario que quer pesquisar ou deixe vazio para visualizar todas as usuarios")
    if st.button("PESQUISAR"):
        buscar_usuarios_action(id)

def buscar_usuarios_action(id=None):
    if id:
        data = fazer_requisicao(f"usuarios/{id}", method="GET")
    else:
        data = fazer_requisicao("usuarios", method="GET")

    # Se houver dados na resposta, exibir os imóveis
    if data:
        # Se a resposta contiver resultados (quantidade de imóveis for maior que 0), exibe os imóveis encontrados.
        if "usuarios" in data:
            df = pd.DataFrame(data["usuarios"])
        else:
            df = pd.DataFrame(data, index=[0])
        st.write("### 👤 Resultados da Pesquisa")
        st.dataframe(df)
    elif data:
        st.write("❌ Nenhuma usuario encontra com esse id")


def deletar_usuario():
    st.title("Deletar Usuarios")
    id = st.text_input("Digite o ID do usuario que quer deletar")
    if st.button("DELETAR"):
        deletar_usuario_action(id)

def deletar_usuario_action(id):
    if not id:
        st.warning("⚠️ É necessário especificar um id para deletar uma usuario")
    data = fazer_requisicao(f"usuarios/{id}", method="DELETE")
    if data:
        if "success" in data:
            st.subheader(data["success"])

def adcionar_usuario():
    st.title("Cadastrar Usuarios")
    nome = st.text_input("Digite o nome do usuario")
    cpf = st.text_input("Digite o cpf do usuario")
    data_de_nascimento = st.text_input("Digite a data de nascimento do usuario")
    if st.button("CADASTRAR"):
        adcionar_usuario_action(nome, cpf, data_de_nascimento)

def adcionar_usuario_action(nome, cpf, data_de_nascimento):
    data = None
    if not nome or not cpf or not data_de_nascimento:
        st.warning("⚠️ Para cadastrar um usuario voçê precisa preencher todos os campos")
    else:   
        data = fazer_requisicao(endpoint="usuarios", method="POST", data={"nome": nome, "data_de_nascimento": data_de_nascimento, "cpf": cpf})
    if data:
        if "success" in data:
            st.subheader("Usuário criado com sucesso!")
            df = pd.DataFrame(data['success'], index=[0])
            st.dataframe(df)

def editar_usuario():
    st.title("Editar Usuarios")
    id_usuario = st.text_input("Digite o ID do usuario")
    nome = st.text_input("Digite o nome do usuario")
    cpf = st.text_input("Digite o cpf do usuario")
    data_de_nascimento = st.text_input("Digite a data de nascimento do usuario")
    if st.button("EDITAR usuario"):
        editar_usuario_action(id_usuario, nome, cpf, data_de_nascimento)


def editar_usuario_action(id_usuario, nome=None, cpf=None, data_de_nascimento=None):
    dados = {}
    if not id_usuario:
        st.warning("⚠️ É necessário fornecer o ID para poder editar")
    if nome:
        dados["nome"] = nome
    if cpf:
        dados["cpf"] = cpf
    if data_de_nascimento:
        dados["data_de_nascimento"] = data_de_nascimento
    request = fazer_requisicao(endpoint=f"usuarios/{id_usuario}", method="PUT", data=dados)
    if request:
        if "success" in request:
            st.subheader("Usuário editado com sucesso!")
            df = pd.DataFrame(request['success'], index=[0])
            st.dataframe(df)

#BICICLETAS

def buscar_bicicleta():
    st.title("Pesquisar Bicicletas")
    id = st.text_input("Digite o ID da bicicleta que quer pesquisar ou deixe vazio para visualizar todas as bicicletas")
    if st.button("PESQUISAR"):
        buscar_bicicletas_action(id)

def buscar_bicicletas_action(id=None):
    if id:
        data = fazer_requisicao(f"bicicletas/{id}", method="GET")
    else:
        data = fazer_requisicao("bicicletas", method="GET")

    # Se houver dados na resposta, exibir os imóveis
    if data:
        # Se a resposta contiver resultados (quantidade de imóveis for maior que 0), exibe os imóveis encontrados.
        if "bicicletas" in data:
            df = pd.DataFrame(data["bicicletas"])
        else:
            df = pd.DataFrame(data, index=[0])
        st.write("### 🚲 Resultados da Pesquisa")
        st.dataframe(df)
    elif data:
        st.write("❌ Nenhuma bicicleta encontra com esse id")


def deletar_bicicleta():
    st.title("Deletar Bicicletas")
    id = st.text_input("Digite o ID da bicicleta que quer deletar")
    if st.button("DELETAR"):
        deletar_bicicleta_action(id)

def deletar_bicicleta_action(id):
    if not id:
        st.warning("⚠️ É necessário especificar um id para deletar uma bicicleta")
    data = fazer_requisicao(f"bicicletas/{id}", method="DELETE")
    if data:
        if "success" in data:
            st.subheader(data["success"])

def adcionar_bicicleta():
    st.title("Cadastrar Bicicletas")
    marca = st.text_input("Digite a marca da bicicleta")
    modelo = st.text_input("Digite o modelo da bicicleta")
    cidade = st.text_input("Digite a cidade da bicicleta")
    status = st.selectbox("Status de disponibilidade", ["Disponivel", "Em uso"])
    if st.button("CADASTRAR"):
        adcionar_bicicleta_action(marca, modelo, cidade, status)

def adcionar_bicicleta_action(marca,modelo,cidade,status):
    if not marca or not modelo or not cidade or not status:
        st.warning("⚠️ Para cadastrar uma bicicleta voçeê preciisa preencher todos os campos")
    else:
        data = fazer_requisicao(endpoint="bicicletas", method="POST", data={"marca": marca, "modelo": modelo, "cidade": cidade, "status": status})
    if data:
        if "success" in data:
            st.subheader("Bicicleta criada com sucesso!")
            df = pd.DataFrame(data['success'], index=[0])
            st.dataframe(df)

def editar_bicicleta():
    st.title("Editar Bicicletas")
    id_bicicleta = st.text_input("Digite o ID da bicicleta")
    marca = st.text_input("Digite a marca da bicicleta")
    modelo = st.text_input("Digite o modelo da bicicleta")
    cidade = st.text_input("Digite a cidade da bicicleta")
    status = st.selectbox("Status de disponibilidade",["Disponível", "Em Uso"])
    if st.button("EDITAR BICICLETA"):
        editar_bicicleta_action(id_bicicleta, marca, modelo, cidade, status)


def editar_bicicleta_action(id_bicicleta, marca, modelo, cidade, status):
    dados = {}
    if not id_bicicleta:
        st.warning("⚠️ É necessário fornecer o ID para poder editar")
    if marca:
        dados["marca"] = marca
    if modelo:
        dados["modelo"] = modelo
    if cidade:
        dados["cidade"] = cidade
    if status:
        dados["status"] = status
    request = fazer_requisicao(endpoint=f"bicicletas/{id_bicicleta}", method="PUT", data=dados)
    if request:
        if "success" in request:
            st.subheader("Bicicleta editada com sucesso!")
            df = pd.DataFrame(request['success'], index=[0])
            st.dataframe(df)

# EMPPRESTIMOS

def buscar_emprestimo():
    st.title("Ver todos os Emprestimos finalizados")
    if st.button("VER EMPRESTIMOS FINALIZADOS"):
        buscar_emprestimos_action()

def buscar_emprestimos_action(id=None):
    if id:
        data = fazer_requisicao(f"emprestimos/{id}", method="GET")
    else:
        data = fazer_requisicao("emprestimos", method="GET")

    # Se houver dados na resposta, exibir os imóveis
    if data:
        # Se a resposta contiver resultados (quantidade de imóveis for maior que 0), exibe os imóveis encontrados.
        df = pd.DataFrame(data["success"])
        st.write("### 🚲 Resultados da Pesquisa")
        st.dataframe(df)
    elif data:
        st.write("❌ Nenhuma emprestimo encontrado com esse id")


def deletar_emprestimo():
    st.title("Deletar Emprestimos")
    id = st.text_input("Digite o ID do emprestimo que quer deletar")
    if st.button("DELETAR"):
        deletar_emprestimo_action(id)

def deletar_emprestimo_action(id):
    if not id:
        st.warning("⚠️ É necessário especificar um id para deletar uma emprestimo")
    data = fazer_requisicao(f"emprestimos/{id}", method="DELETE")
    if data:
        if "success" in data:
            st.subheader(data["success"])

def adcionar_emprestimo():
    st.title("Cadastrar Emprestimos")
    id_usuario = st.text_input("Digite o id do usuario")
    id_bicicleta = st.text_input("Digite o id da bicicleta")
    if st.button("CADASTRAR"):
        adcionar_emprestimo_action(id_usuario, id_bicicleta)

def adcionar_emprestimo_action(id_usuario, id_bicicleta):
    if not id_bicicleta or not id_usuario:
        st.warning("⚠️ Para cadastrar uma emprestimo voçeê precisa preencher todos os campos")
    else:
        data = fazer_requisicao(endpoint=f"emprestimos/usuarios/{id_usuario}/bicicletas/{id_bicicleta}", method="POST")
    if data:
        if "success" in data:
            df = pd.DataFrame(data["success"]["emprestimos"])
            st.subheader("Emprestimo criado com sucesso")
            st.dataframe(df)
def editar_emprestimo():
    st.title("Editar Emprestimos")
    id_usuario = st.text_input("Digite o ID do usuario")
    id_bicicleta = st.text_input("Digite o ID da bicicleta")
    status = st.selectbox("Escolha o status do emprestimo", ["Em andamento", "Finalizado"])
    if st.button("EDITAR EMPRESTIMO"):
        editar_emprestimo_action(id_bicicleta, id_usuario, status)


def editar_emprestimo_action(id_bicicleta, id_usuario, status):
    if not id_bicicleta or not id_usuario or not status:
        st.warning("⚠️ É necessário fornecer o ID para poder editar")
        return

    dados = {"id_bicicleta": id_bicicleta, "status": status}
    request = fazer_requisicao(endpoint=f"emprestimos/{id_usuario}", method="PUT", data=dados)

    if request and "success" in request:
        st.subheader("Emprestimo editado com sucesso")
        if "finalizado" in request:
            st.write(request["finalizado"])
        else:
            st.subheader("Informacoes do Usuario: ")
            user_data = request["success"]
            df = pd.DataFrame([user_data]) 
            
            st.dataframe(df)
            
            if user_data["emprestimos"]:
                st.write("Empréstimos:")
                emprestimos_df = pd.DataFrame(user_data["emprestimos"])
                st.dataframe(emprestimos_df)
            else:
                st.write("Não há empréstimos para este usuário.")
    else:
        st.error("Falha ao editar o empréstimo. Por favor, tente novamente.")
def users():
    funcs = {
    "—": intro,
    "Cadastrar Usuarios": adcionar_usuario,
    "Pesquisar Usuario": buscar_usuario,
    "Editar Usuario": editar_usuario,
    "Deletar Usuario": deletar_usuario,
    }
    func = st.sidebar.selectbox("Escolha o que quer fazer", funcs.keys())
    funcs[func]()

def bikes():
    funcs = {
    "—": intro,
    "Cadastrar bicicletas": adcionar_bicicleta,
    "Pesquisar bicicleta": buscar_bicicleta,
    "Editar bicicleta": editar_bicicleta,
    "Deletar bicicleta": deletar_bicicleta,
    }
    func = st.sidebar.selectbox("Escolha o que quer fazer", funcs.keys())
    funcs[func]()

def emprestimos():
    funcs = {
    "—": intro,
    "Cadastrar emprestimos": adcionar_emprestimo,
    "Visualizar emprestimos finalizados": buscar_emprestimo,
    "Editar emprestimo": editar_emprestimo,
    "Deletar emprestimo": deletar_emprestimo,
    }
    func = st.sidebar.selectbox("Escolha o que quer fazer", funcs.keys())
    funcs[func]()


funcs = {
        "Usuarios": users,
        "Bicicletas": bikes,
        "Emprestimos": emprestimos
        }   
func = st.sidebar.selectbox("Escolha o campo que deseja", funcs.keys())
funcs[func]()