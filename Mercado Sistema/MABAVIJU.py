import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from pyzbar.pyzbar import decode
from tkinter import PhotoImage, Label, Tk
import pyautogui
import time

# Usuário e senha para autenticação
USUARIO = ""
SENHA = ""

# Dicionário com códigos de barras dos produtos
codigos_produtos = {}
quantidade_produtos = {}

# Função para autenticar usuário e senha
def autenticar_usuario_senha(usuario, senha, callback):
    def verificar_credenciais():
        usuario_input = entry_usuario.get()
        senha_input = entry_senha.get()
        if usuario_input == usuario and senha_input == senha:
            messagebox.showinfo("Sucesso", "Autenticação bem-sucedida!")
            janela_inicial.destroy()
            callback()
        else:
            messagebox.showerror("Erro", "Credenciais incorretas. Tente novamente.")

    janela_autenticacao = tk.Toplevel(janela_inicial)
    janela_autenticacao.title("Autenticação")
    janela_autenticacao.geometry("400x300")

    lbl_usuario = tk.Label(janela_autenticacao, text="Usuário:", font=("Arial", 12))
    lbl_usuario.pack(pady=5)
    entry_usuario = tk.Entry(janela_autenticacao)
    entry_usuario.pack(pady=5)

    lbl_senha = tk.Label(janela_autenticacao, text="Senha:", font=("Arial", 12))
    lbl_senha.pack(pady=5)
    entry_senha = tk.Entry(janela_autenticacao, show="*")
    entry_senha.pack(pady=5)

    btn_verificar = tk.Button(janela_autenticacao, text="Verificar", command=verificar_credenciais, bg="#4CAF50", fg="white", font=("Arial", 12))
    btn_verificar.pack(pady=10)
    
# Função para carregar produtos do arquivo "arquivos.txt"
def carregar_produtos():
    valores = {}
    
    try:
        with open("arquivos.txt", "r") as f:
            for line in f:
                key, value, quantidade, cod_barras = line.strip().split(":")
                valores[key] = float(value)
                codigos_produtos[key] = cod_barras
                quantidade_produtos[key] = int(quantidade)
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo 'arquivos.txt' não encontrado.")
    return valores

# Função para mostrar produtos na Listbox
def mostrar_produtos(lista_produtos):
    lista_produtos.delete(0, tk.END)
    valores = carregar_produtos()
    for produto, preco in valores.items():
        quantidade = quantidade_produtos[produto]
        lista_produtos.insert(tk.END, f"{produto}: R${preco:.2f} - Quantidade:{quantidade}- Código de Barras: {codigos_produtos[produto]}")

# Função para cadastrar produtos
def mostrar_produtos(lista_produtos):
    lista_produtos.delete(0, tk.END)
    valores = carregar_produtos()
    for produto, preco in valores.items():
        quantidade = quantidade_produtos[produto]
        lista_produtos.insert(tk.END, f"{produto}: R${preco:.2f} - Quantidade: {quantidade} - Código de Barras: {codigos_produtos[produto]}")

# Função para cadastrar produtos
def cadastrar_produto():

        produtos_a_cadastrar = []

        def adicionar_produto(produto, preco, quantidade, cod_barras):
            produtos_a_cadastrar.append((produto, preco, quantidade, cod_barras))
            lista_a_cadastrar.insert(tk.END, f"{produto}: R${preco:.2f} - Quantidade: {quantidade} - Código de Barras: {cod_barras}")

        def salvar_produtos():
            with open("arquivos.txt", "a") as f:
                for produto, preco, quantidade, cod_barras in produtos_a_cadastrar:
                    f.write(f"{produto}:{preco}:{quantidade}:{cod_barras}\n")
            messagebox.showinfo("Sucesso", "Produtos cadastrados com sucesso!")
            produtos_a_cadastrar.clear()
            mostrar_produtos(lista_produtos)

        def remover_produto():
            def remover():
                produto = entry_nome.get()
                valores = carregar_produtos()
                if produto in valores:
                    with open("arquivos.txt", "w") as f:
                        for key, value in valores.items():
                            if key != produto:
                                f.write(f"{key}:{value}:{codigos_produtos[key]}:{quantidade_produtos[key]}\n")
                    messagebox.showinfo("Sucesso", "Produto removido com sucesso.")
                    mostrar_produtos(lista_produtos)
                    entry_nome.delete(0, tk.END)
                else:
                    messagebox.showerror("Erro", f"{produto} não encontrado.")

            janela_remover = tk.Toplevel(janela_cadastro)
            janela_remover.title("Remover Produto")
            janela_remover.geometry("800x600")

            lbl_produtos_disponiveis = tk.Label(janela_remover, text="Produtos Disponíveis:", font=("Arial", 18))
            lbl_produtos_disponiveis.pack(pady=20)

            lista_produtos_remover = tk.Listbox(janela_remover, font=("Arial", 14))
            lista_produtos_remover.pack(pady=20, fill=tk.BOTH, expand=True)
            mostrar_produtos(lista_produtos_remover)

            lbl_nome = tk.Label(janela_remover, text="Nome do Produto:", font=("Arial", 16))
            lbl_nome.pack(pady=10)
            entry_nome = tk.Entry(janela_remover, font=("Arial", 12))  # Fonte menor
            entry_nome.pack(pady=10, fill=tk.X, padx=20)  # Menor largura

            btn_remover = tk.Button(janela_remover, text="Remover Produto", command=remover, bg="#f44336", fg="white", font=("Arial", 16))
            btn_remover.pack(pady=20)

        janela_cadastro = tk.Toplevel(janela)
        janela_cadastro.title("Cadastrar Produtos")
        janela_cadastro.attributes('-fullscreen', True)  # Abre em tela cheia

        lbl_nome = tk.Label(janela_cadastro, text="Nome do Produto:", font=("Arial", 18))
        lbl_nome.pack(pady=10)
        entry_nome = tk.Entry(janela_cadastro, font=("Arial", 14))
        entry_nome.pack(pady=10, fill=tk.X, padx=20)

        lbl_preco = tk.Label(janela_cadastro, text="Preço do Produto:", font=("Arial", 18))
        lbl_preco.pack(pady=10)
        entry_preco = tk.Entry(janela_cadastro, font=("Arial", 14))
        entry_preco.pack(pady=10, fill=tk.X, padx=20)

        lbl_cod_barras = tk.Label(janela_cadastro, text="Código de Barras:", font=("Arial", 18))
        lbl_cod_barras.pack(pady=10)
        entry_cod_barras = tk.Entry(janela_cadastro, font=("Arial", 14))
        entry_cod_barras.pack(pady=10, fill=tk.X, padx=20)

        lbl_quantidade = tk.Label(janela_cadastro, text="Quantidade:", font=("Arial", 18))
        lbl_quantidade.pack(pady=10)
        entry_quantidade = tk.Entry(janela_cadastro, font=("Arial", 14))
        entry_quantidade.pack(pady=10, fill=tk.X, padx=20)

        def validar_e_adicionar():
            try:
                nome = entry_nome.get()
                preco = float(entry_preco.get())
                cod_barras = entry_cod_barras.get()
                quantidade = int(entry_quantidade.get())
                adicionar_produto(nome, preco, quantidade, cod_barras)
            except ValueError:
                messagebox.showerror("Erro", "Preço ou quantidade inválidos. Por favor, insira valores válidos.")

        frame_botoes = tk.Frame(janela_cadastro)
        frame_botoes.pack(pady=20)

        btn_adicionar = tk.Button(frame_botoes, text="Adicionar à Lista", command=validar_e_adicionar, bg="#2062D6", fg="white", font=("Arial", 16))
        btn_adicionar.pack(side=tk.LEFT, padx=10, pady=10)

        btn_salvar = tk.Button(frame_botoes, text="Salvar Produtos", command=salvar_produtos, bg="#2062D6", fg="white", font=("Arial", 16))
        btn_salvar.pack(side=tk.LEFT, padx=10, pady=10)

        btn_remover = tk.Button(frame_botoes, text="Remover Produto", command=remover_produto, bg="#f44336", fg="white", font=("Arial", 16))
        btn_remover.pack(side=tk.LEFT, padx=10, pady=10)

        lbl_a_cadastrar = tk.Label(janela_cadastro, text="Produtos a Cadastrar:", font=("Arial", 18))
        lbl_a_cadastrar.pack(pady=20)

        lista_a_cadastrar = tk.Listbox(janela_cadastro, font=("Arial", 14))
        lista_a_cadastrar.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        mostrar_produtos(lista_produtos)




# Função de verificar senha antes de cadastrar produtos
def entrar_sistema():
    def verificar_senha1():
        senha_input = entry_senha1.get()
        if senha_input == SENHA:
            cadastrar_produto()  # Somente após a senha correta, a função de cadastro será chamada
            janela_senha1.destroy()
        else:
            messagebox.showerror("Erro", "Senha incorreta. Não foi possível acessar o cadastro de produtos.")

    janela_senha1 = tk.Toplevel(janela)
    janela_senha1.title("Confirmação de Entrada")
    janela_senha1.geometry("300x150")

    lbl_senha1 = tk.Label(janela_senha1, text="Digite a senha para entrar:")
    lbl_senha1.pack(pady=5)

    entry_senha1 = tk.Entry(janela_senha1, show="*")
    entry_senha1.pack(pady=5)

    btn_confirmar1 = tk.Button(janela_senha1, text="Confirmar", command=verificar_senha1)
    btn_confirmar1.pack(pady=10)

# Função para escanear códigos de barras
def escanear_codigo(callback):
    cap = cv2.VideoCapture(1)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        codigo_barras = decode(frame)
        for codigo in codigo_barras:
            texto = codigo.data.decode('utf-8')
            cap.release()
            cv2.destroyAllWindows()
            callback(texto)
            return

        cv2.imshow('Camera', frame)
        if cv2.waitKey(2) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




# Função para realizar o pagamento com base nos códigos de barras escaneados
def realizar_pagamento():
    valores = carregar_produtos()
    produtos_selecionados = []

    def adicionar_produto_ao_carrinho(codigo_barras):
        for produto, cod in codigos_produtos.items():
            if cod == codigo_barras:
                if quantidade_produtos[produto] > 0:  # Verifica se há estoque disponível
                    produtos_selecionados.append((produto, valores[produto]))
                    quantidade_produtos[produto] -= 1
                    lista_selecionados.insert(tk.END, f"{produto}: R${valores[produto]:.2f}")
                    messagebox.showinfo("Produto Adicionado", f"{produto} adicionado ao carrinho.")
                else:
                    messagebox.showwarning("Produto Indisponível", f"{produto} está fora de estoque.")
                return

    def calcular_total():
        total = sum([preco for _, preco in produtos_selecionados])
        messagebox.showinfo("Total a Pagar", f"Valor total: R${total:.2f}")
        return total

    def finalizar_pagamento():
        total = calcular_total()
        if total > 0:
            janela_pagamento = tk.Toplevel(janela)
            janela_pagamento.title("Método de Pagamento")
            janela_pagamento.geometry("300x200")
            janela_pagamento.attributes('-topmost', True)

            lbl_pagamento = tk.Label(janela_pagamento, text="Método de Pagamento:", font=("Arial", 12))
            lbl_pagamento.pack(pady=10)

            combobox_pagamento = ttk.Combobox(janela_pagamento, values=["Dinheiro", "Cartão de Crédito", "Pix"], state="readonly")
            combobox_pagamento.pack(pady=5)

            def confirmar_pagamento():
                metodo_pagamento = combobox_pagamento.get()
                if metodo_pagamento:
                    with open("pagamentos.txt", "a") as f:
                        for produto, preco in produtos_selecionados:
                            f.write(f"{produto}: R${preco:.2f}\n")
                        f.write(f"Total: R${total:.2f} - Pagamento via {metodo_pagamento}\n\n")
                    messagebox.showinfo("Pagamento Realizado", "Pagamento concluído com sucesso!")
                    produtos_selecionados.clear()
                    lista_selecionados.delete(0, tk.END)
                    janela_pagamento.destroy()
                else:
                    messagebox.showwarning("Erro", "Por favor, selecione um método de pagamento.")

            btn_confirmar = tk.Button(janela_pagamento, text="Confirmar", command=confirmar_pagamento, bg="#4CAF50", fg="white", font=("Arial", 12))
            btn_confirmar.pack(pady=20)
        else:
            messagebox.showwarning("Carrinho Vazio", "Nenhum produto no carrinho.")

    janela_pagamento = tk.Toplevel(janela)
    janela_pagamento.title("Comprar")
    janela_pagamento.geometry("400x400")
    janela_pagamento.attributes('-fullscreen', True)

    lbl_instrucao = tk.Label(janela_pagamento, text="Selecione a opção:")
    lbl_instrucao.pack(pady=10)

    def adicionar_produto_ao_carrinho_escanear():
        escanear_codigo(adicionar_produto_ao_carrinho)

    btn_escanear = tk.Button(janela_pagamento, text="Escanear Produto", command=adicionar_produto_ao_carrinho_escanear, bg="#4CAF50", fg="white", font=("Arial", 12))
    btn_escanear.pack(pady=10)

    lbl_selecionados = tk.Label(janela_pagamento, text="Produtos no Carrinho:", font=("Arial", 16, "bold"))
    lbl_selecionados.pack(pady=5)

    lista_selecionados = tk.Listbox(janela_pagamento)
    lista_selecionados.pack(pady=5, fill=tk.BOTH, expand=True)

    btn_finalizar = tk.Button(janela_pagamento, text="Finalizar Pagamento", command=finalizar_pagamento, bg="#4CAF50", fg="white", font=("Arial", 12))
    btn_finalizar.pack(pady=20)





# Função para remover produtos
def remover_produto():
    def remover():
        produto = entry_nome.get()
        valores = carregar_produtos()
        if produto in valores:
            with open("arquivos.txt", "w") as f:
                for key, value in valores.items():
                    if key != produto:
                        f.write(f"{key}:{value}:{codigos_produtos[key]}\n")
            messagebox.showinfo("Sucesso", "Produto removido com sucesso.")
            mostrar_produtos('lista_produtos')
            entry_nome.delete(0, tk.END)
        else:
            messagebox.showerror("Erro", f"{produto} não encontrado.")

    janela_remover = tk.Toplevel(janela)
    janela_remover.title("Remover Produto")
    janela_remover.geometry("400x200")

    lbl_nome = tk.Label(janela_remover, text="Nome do Produto:")
    lbl_nome.pack(pady=5)
    entry_nome = tk.Entry(janela_remover)
    entry_nome.pack(pady=5)

    btn_remover = tk.Button(janela_remover, text="Remover Produto", command=remover)
    btn_remover.pack(pady=10)

# Função para ver produtos disponíveis
def ver_produtos():
    valores = carregar_produtos()

    janela_produtos = tk.Toplevel(janela)
    janela_produtos.title("Produtos Disponíveis")
    janela_produtos.attributes('-fullscreen', True)  # Janela maior para acomodar a tabela

    # Frame principal que contém todos os elementos
    frame_principal = tk.Frame(janela_produtos, bg="#F0F0F0")
    frame_principal.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Frame para o título
    frame_titulo = tk.Frame(frame_principal, bg="#4CAF50")
    frame_titulo.pack(fill=tk.X, pady=10)
    
    lbl_produtos = tk.Label(frame_titulo, text="Produtos Disponíveis:", font=("Arial", 18, "bold"), bg="#4CAF50", fg="white")
    lbl_produtos.pack(pady=10)

    # Frame para a tabela de produtos
    frame_tabela = tk.Frame(frame_principal, bg="#FFFFFF")
    frame_tabela.pack(fill=tk.BOTH, expand=True, pady=10)

    # Criação da tabela utilizando Treeview
    colunas = ("Nome", "Preço", "Quantidade", "Código de Barras")
    tabela_produtos = ttk.Treeview(frame_tabela, columns=colunas, show='headings', height=15)

    # Definir as colunas e cabeçalhos
    tabela_produtos.heading("Nome", text="Nome")
    tabela_produtos.heading("Preço", text="Preço (R$)")
    tabela_produtos.heading("Quantidade", text="Quantidade")
    tabela_produtos.heading("Código de Barras", text="Código de Barras")

    
    # Ajustar largura das colunas
    tabela_produtos.column("Nome", anchor="center", width=200)
    tabela_produtos.column("Preço", anchor="center", width=100)
    tabela_produtos.column("Quantidade", anchor="center", width=100)
    tabela_produtos.column("Código de Barras", anchor="center", width=200)

    # Inserir os dados na tabela
    for produto, preco in valores.items():
        quantidade = quantidade_produtos[produto]
        codigo_barras = codigos_produtos[produto]
        tabela_produtos.insert("", "end", values=(produto, f"R${preco:.2f}", quantidade, codigo_barras))

    # Configurar o estilo da tabela
    estilo_tabela = ttk.Style()
    estilo_tabela.configure("Treeview", font=("Arial", 14), rowheight=30)
    estilo_tabela.configure("Treeview.Heading", font=("Arial", 16, "bold"))

    tabela_produtos.pack(pady=10, fill=tk.BOTH, expand=True)

    # Barra de rolagem para o Treeview
    scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tabela_produtos.yview)
    tabela_produtos.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Frame para os botões (caso haja necessidade de adicionar botões no futuro)
    frame_botoes = tk.Frame(frame_principal)
    frame_botoes.pack(fill=tk.X, pady=10)

    # Exemplo de botão dentro do frame de botões
    btn_fechar = tk.Button(frame_botoes,width=30, text="Fechar", command=janela_produtos.destroy, bg="#D32F2F", fg="white", font=("Arial", 14, "bold"))
    btn_fechar.pack(pady=10)


# Função principal para exibir o menu principal após o login
def menu_principal():
    global janela
    janela = tk.Tk()
    janela.title("Supermercado MABAVIJU")
    janela.geometry("400x300")
    janela.attributes('-fullscreen', True)

    lbl_instrucao = tk.Label(janela, width=21, height=10, text="Selecione uma opção:", font=("Arial", 14))
    lbl_instrucao.pack(pady=10)

    btn_cadastrar = tk.Button(janela, width=23, height=5, text="Cadastrar Produtos", command=entrar_sistema, bg="#4CAF50", fg="white", font=("Arial", 12))
    btn_cadastrar.pack(pady=10)

    btn_ver_produtos = tk.Button(janela, width=23, height=5, text="Ver Produtos", command=ver_produtos, bg="#4CAF50", fg="white", font=("Arial", 12))
    btn_ver_produtos.pack(pady=10)
    

    btn_pagamento = tk.Button(janela, width=23, height=5, text="Comprar e Finalizar compra", command=realizar_pagamento, bg="#4CAF50", fg="white", font=("Arial", 12))
    btn_pagamento.pack(pady=10)
    
    
    

    btn_sair = tk.Button(janela, width=23, height=5, text="Sair", command=sair_do_sistema, bg="#f44336", fg="white", font=("Arial", 12))
    btn_sair.pack(pady=10)

    janela.mainloop()
    
    # Função para realizar o pagamento com base nos códigos de barras escaneados
def realizar_pagamento():
    valores = carregar_produtos()
    produtos_selecionados = []
    
    def adicionar_produto_ao_carrinho(codigo_barras):
        for produto, cod in codigos_produtos.items():
            if cod == codigo_barras:
                produtos_selecionados.append((produto, valores[produto]))
                quantidade_produtos[produto] -= 1
                lista_selecionados.insert(tk.END, f"{produto}: R${valores[produto]:.2f}")
                
                
                # Usando pyautogui para simular atalhos e cliques

                
                
                try:
                    # Trocar de janela e clicar em uma posição específica
                    pyautogui.moveTo(x = 1043, y = 620)
                    pyautogui.click()
                    time.sleep(2)

                    pyautogui.hotkey('win', 'tab')  # Tenta alternar entre janelas
                    pyautogui.moveTo(567, 300)      # Move o mouse para a coordenada especificada
                    pyautogui.click()               # Clica na posição
                except pyautogui.FailSafeException:
                    messagebox.showerror("Erro", "Falha ao utilizar pyautogui. Verifique as permissões do sistema.")


    def calcular_total():
        total = sum([preco for _, preco in produtos_selecionados])
        messagebox.showinfo("Total a Pagar", f"Valor total: R${total:.2f}")
        return total

    def finalizar_pagamento():
        total = calcular_total()
        if total > 0:
            with open("pagamentos.txt", "a") as f:
                for produto, preco in produtos_selecionados:
                    f.write(f"{produto}: R${preco:.2f}\n")
                f.write(f"Total: R${total:.2f}\n\n")
            messagebox.showinfo("Pagamento Realizado", "Pagamento concluído com sucesso!")
            produtos_selecionados.clear()
            lista_selecionados.delete(0, tk.END)
        else:
            messagebox.showwarning("Carrinho Vazio", "Nenhum produto no carrinho.")
            
    
    janela_pagamento = tk.Toplevel(janela)
    janela_pagamento.title("Comprar")
    janela_pagamento.geometry("400x400")
    janela_pagamento.attributes('-fullscreen', True)


    
    

    # Botão para escanear código
    def adicionar_produto_ao_carrinho_escanear():
        escanear_codigo(adicionar_produto_ao_carrinho)

    btn_escanear = tk.Button(janela_pagamento,width=23,height=2,bg="#4CAF50",fg="white", text="Escanear Produto", command=adicionar_produto_ao_carrinho_escanear,font=("Arial", 12))

    btn_escanear.pack(pady=10)
    

    lbl_selecionados = tk.Label(janela_pagamento,width=30, height=1, font=("Arial",20,"bold"), text="Produtos no Carrinho:")
    lbl_selecionados.pack(pady=5)

    lista_selecionados = tk.Listbox(janela_pagamento)
    lista_selecionados.pack(pady=3, fill=tk.BOTH, expand=True)

    # Separando os botões com mais espaço
    btn_finalizar = tk.Button(janela_pagamento,width=23,height=2,bg="#4CAF50",fg="white", text="Finalizar Pagamento", command=finalizar_pagamento, font=("Arial", 12))
    btn_finalizar.pack(pady=20)  # Espaço extra entre os botões

# Função para sair do sistema com confirmação de senha
def sair_do_sistema():
    def verificar_senha():
        senha_input = entry_senha.get()
        if senha_input == SENHA:
            janela.quit()
        else:
            messagebox.showerror("Erro", "Senha incorreta. Não foi possível sair do sistema.")

    janela_senha = tk.Toplevel(janela)
    janela_senha.title("Confirmação de Saída")
    janela_senha.geometry("300x150")

    lbl_senha = tk.Label(janela_senha, text="Digite a senha para sair:")
    lbl_senha.pack(pady=5)

    entry_senha = tk.Entry(janela_senha, show="*")
    entry_senha.pack(pady=5)

    btn_confirmar = tk.Button(janela_senha, text="Confirmar", command=verificar_senha)
    btn_confirmar.pack(pady=10)

# Função de login
def login():
    def abrir_sistema():
        menu_principal()

    global janela_inicial, logo
    janela_inicial = tk.Tk()
    janela_inicial.title("Sistema de Controle de Produtos")
    janela_inicial.geometry("600x300")
    janela_inicial.configure(bg="white")

    # Nome da empresa com fonte arredondada
    lbl_nome_empresa = tk.Label(janela_inicial, text="Supermercado MABAVIJU", font=("Comic Sans MS", 24, "bold"), fg="#333333", bg="white")
    lbl_nome_empresa.pack(pady=20)

    # Frame principal para organizar imagem e login/telefone lado a lado
    frame_principal = tk.Frame(janela_inicial, bg="white")
    frame_principal.pack(pady=20)

    # Carrega e exibe a imagem à esquerda
    logo = PhotoImage(file="mercado.png")
    logo = logo.subsample(1, 1)
    label_imagem = Label(frame_principal, image=logo, bg="white")
    label_imagem.pack(side=tk.LEFT, padx=20)

    # Frame para conter o botão de login e o telefone, à direita
    frame_login = tk.Frame(frame_principal, bg="white")
    frame_login.pack(side=tk.RIGHT, padx=20)

    # Botão de login
    btn_login = tk.Button(frame_login, text="Login", command=lambda: autenticar_usuario_senha(USUARIO, SENHA, abrir_sistema), bg="#333333", fg="white", font=("Arial", 14), width=20)
    btn_login.pack(pady=10)

    # Telefone da empresa
    lbl_telefone_empresa = tk.Label(frame_login, text="Telefone: (11) 1234-5678", font=("Helvetica", 14), fg="#333333", bg="white")
    lbl_telefone_empresa.pack(pady=10)

    janela_inicial.mainloop()

login()