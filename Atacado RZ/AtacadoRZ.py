import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector

conexao = None

# Função para abrir a conexão com o banco de dados
def abrir_conexao():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="atacadorz"
        )
    except mysql.connector.Error as err:
        print("Erro ao abrir a conexão com o banco de dados:", err)
        return None

# Função para fechar a conexão com o banco de dados
def fechar_conexao(conexao):
    try:
        if conexao is not None and conexao.is_connected():
            conexao.close()
    except mysql.connector.Error as err:
        print("Erro ao fechar a conexão com o banco de dados:", err)

# Função para abrir a tela de cadastro de novo produto
def cadastrar_produto():
    root.withdraw()

    tela_cadastro = tk.Toplevel(root)
    tela_cadastro.title("Cadastro de Produto")

    # Adiciona campos de entrada
    label_nome = ttk.Label(tela_cadastro, text="Nome do Produto:")
    entry_nome = ttk.Entry(tela_cadastro)
    label_nome.grid(row=0, column=0, padx=10, pady=5)
    entry_nome.grid(row=0, column=1, padx=10, pady=5)

    label_descricao = ttk.Label(tela_cadastro, text="Descrição:")
    entry_descricao = ttk.Entry(tela_cadastro)
    label_descricao.grid(row=1, column=0, padx=10, pady=5)
    entry_descricao.grid(row=1, column=1, padx=10, pady=5)

    label_preco = ttk.Label(tela_cadastro, text="Preço:")
    entry_preco = ttk.Entry(tela_cadastro)
    label_preco.grid(row=2, column=0, padx=10, pady=5)
    entry_preco.grid(row=2, column=1, padx=10, pady=5)

    label_quantidade = ttk.Label(tela_cadastro, text="Quantidade:")
    entry_quantidade = ttk.Entry(tela_cadastro)
    label_quantidade.grid(row=3, column=0, padx=10, pady=5)
    entry_quantidade.grid(row=3, column=1, padx=10, pady=5)

    # Função para salvar os dados no banco de dados
    def salvar_produto():
        global conexao  # Declarar a variável conexao como global

        # Verificar se a conexão foi aberta
        if conexao is None:
            tk.messagebox.showerror("Erro", "Conexão com o banco de dados não foi estabelecida.")
            return

        # Obter os valores dos campos de entrada
        nome = entry_nome.get()
        descricao = entry_descricao.get()
        preco = entry_preco.get()
        quantidade = entry_quantidade.get()

        # Criar um cursor para executar comandos SQL
        cursor = conexao.cursor()

        # Executar a inserção na tabela produtos
        cursor.execute("INSERT INTO produtos (nome, descricao, preco, quantidade) VALUES (%s, %s, %s, %s)",
                       (nome, descricao, preco, quantidade))

        # Commit (salvar) as alterações no banco de dados
        conexao.commit()

        # Fechar o cursor
        cursor.close()

        # Mostrar uma mensagem de sucesso
        tk.messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")

        # Limpar os campos após o cadastro
        entry_nome.delete(0, tk.END)
        entry_descricao.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        entry_quantidade.delete(0, tk.END)

    # Adicionar um botão para confirmar e cadastrar
    botao_cadastrar = ttk.Button(tela_cadastro, text="Cadastrar", command=salvar_produto)
    botao_cadastrar.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Botão para voltar para a tela anterior
    botao_voltar = ttk.Button(tela_cadastro, text="Voltar", command=tela_cadastro.destroy)
    botao_voltar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
    pass

# Função para abrir a tela de consulta de produto
def consultar_produto():
    root.withdraw()

    # Abrir a conexão
    global conexao
    conexao = abrir_conexao()

    tela_consulta = tk.Toplevel(root)
    tela_consulta.title("Consultar Produto")

    label_nome = ttk.Label(tela_consulta, text="Nome do Produto:")
    entry_nome = ttk.Entry(tela_consulta)
    label_nome.grid(row=0, column=0, padx=10, pady=5)
    entry_nome.grid(row=0, column=1, padx=10, pady=5)

    def pesquisar_produto():
        nome_produto = entry_nome.get()

        # Verificar se a conexão foi aberta
        if conexao is None:
            tk.messagebox.showerror("Erro", "Conexão com o banco de dados não foi estabelecida.")
            return

        # Criar um cursor para executar comandos SQL
        cursor = conexao.cursor()

        # Executar a consulta no banco de dados para produtos com o mesmo nome
        cursor.execute("SELECT * FROM produtos WHERE nome = %s", (nome_produto,))
        resultados = cursor.fetchall()

        if resultados:
            for resultado in resultados:
                # Exibir as informações do produto
                info_produto = f"ID: {resultado[0]}\nNome: {resultado[1]}\nDescrição: {resultado[2]}\nPreço: {resultado[3]}\nQuantidade: {resultado[4]}"
                tk.messagebox.showinfo("Informações do Produto", info_produto)
        else:
            tk.messagebox.showinfo("Produto não encontrado",
                                   f"Nenhum produto com o nome '{nome_produto}' foi encontrado.")

    botao_pesquisar = ttk.Button(tela_consulta, text="Pesquisar", command=pesquisar_produto)
    botao_pesquisar.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    botao_voltar = ttk.Button(tela_consulta, text="Voltar", command=tela_consulta.destroy)
    botao_voltar.grid(row=2, column=0, columnspan=2, padx=10, pady=10)


# Função para abrir a tela de visualização de estoque
def visualizar_estoque():
    root.withdraw()

    # Abrir a conexão
    global conexao
    conexao = abrir_conexao()

    tela_estoque = tk.Toplevel(root)
    tela_estoque.title("Estoque Completo")

    # Criar um cursor para executar comandos SQL
    cursor = conexao.cursor()

    # Executar a consulta no banco de dados para todos os produtos
    cursor.execute("SELECT * FROM produtos")
    resultados = cursor.fetchall()

    if resultados:
        texto_estoque = "Estoque Completo:\n\n"
        for resultado in resultados:
            texto_estoque += f"ID: {resultado[0]}\nNome: {resultado[1]}\nDescrição: {resultado[2]}\nPreço: {resultado[3]}\nQuantidade: {resultado[4]}\n\n"

        # Exibir as informações do estoque
        label_estoque = ttk.Label(tela_estoque, text=texto_estoque)
        label_estoque.pack()
    else:
        label_vazio = ttk.Label(tela_estoque, text="Nenhum produto no estoque.")
        label_vazio.pack()

    botao_voltar = ttk.Button(tela_estoque, text="Voltar", command=tela_estoque.destroy)
    botao_voltar.pack()


# Função para abrir a tela de exclusão de produto
def excluir_produto():
    root.withdraw()

    tela_exclusao = tk.Toplevel(root)
    tela_exclusao.title("Excluir Produto")

    # Adicione campos de entrada
    label_id = ttk.Label(tela_exclusao, text="ID do Produto:")
    entry_id = ttk.Entry(tela_exclusao)
    label_id.grid(row=0, column=0, padx=10, pady=5)
    entry_id.grid(row=0, column=1, padx=10, pady=5)

    label_quantidade = ttk.Label(tela_exclusao, text="Quantidade a Excluir:")
    entry_quantidade = ttk.Entry(tela_exclusao)
    label_quantidade.grid(row=1, column=0, padx=10, pady=5)
    entry_quantidade.grid(row=1, column=1, padx=10, pady=5)

    def excluir_produto_banco():
        global conexao  # Declarar a variável conexao como global
        id_produto = entry_id.get()
        quantidade_excluir = entry_quantidade.get()

        # Verificar se o ID é um número inteiro
        try:
            id_produto = int(id_produto)
            quantidade_excluir = int(quantidade_excluir)
        except ValueError:
            tk.messagebox.showerror("Erro", "ID e quantidade devem ser números inteiros.")
            return

        # Criar um cursor para executar comandos SQL
        cursor = conexao.cursor()

        # Verificar se o produto com o ID especificado existe
        cursor.execute("SELECT * FROM produtos WHERE id = %s", (id_produto,))
        produto = cursor.fetchone()

        if not produto:
            tk.messagebox.showerror("Erro", "Produto não encontrado.")
        else:
            # Verificar se há quantidade suficiente para excluir
            quantidade_atual = produto[4]  # A quantidade atual do produto
            if quantidade_excluir > quantidade_atual:
                tk.messagebox.showerror("Erro", "Quantidade a excluir é maior do que a quantidade em estoque.")
            else:
                # Atualizar a quantidade no banco de dados
                nova_quantidade = quantidade_atual - quantidade_excluir
                cursor.execute("UPDATE produtos SET quantidade = %s WHERE id = %s", (nova_quantidade, id_produto))
                conexao.commit()
                tk.messagebox.showinfo("Sucesso",
                                       f"{quantidade_excluir} unidades do produto ID {id_produto} excluídas.")

        # Limpar os campos após a exclusão
        entry_id.delete(0, tk.END)
        entry_quantidade.delete(0, tk.END)

    botao_excluir = ttk.Button(tela_exclusao, text="Excluir", command=excluir_produto_banco)
    botao_excluir.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    botao_voltar = ttk.Button(tela_exclusao, text="Voltar", command=tela_exclusao.destroy)
    botao_voltar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


# Função para sair do sistema
def sair():
    # Fechar a conexão com o banco de dados, se estiver aberta
    if conexao:
        fechar_conexao(conexao)
    root.quit()


# Função para exibir a tela inicial
def iniciar():
    # Esconder a janela principal
    root.withdraw()

    # Cria uma nova janela
    segunda_janela = tk.Toplevel(root)
    segunda_janela.title("Página Inicial")

    # Carrega a imagem com Pillow
    imagem_original = Image.open("C:/Users/antho/Desktop/Meus programas/AtacadoRZ/Perfil.PNG")
    imagem_redimensionada = imagem_original.resize((200, 200))
    imagem_atacado = ImageTk.PhotoImage(imagem_redimensionada)

    # Cria um rótulo para exibir a imagem
    label_imagem = tk.Label(segunda_janela, image=imagem_atacado)
    label_imagem.pack()

    # Configura o rótulo da imagem como imagem de referência para evitar que seja coletado pelo garbage collector
    label_imagem.imagem_atacado = imagem_atacado

    # Frame para botões
    frame_botoes = ttk.Frame(segunda_janela)
    frame_botoes.pack()

    # Botões para ações
    botao_cadastrar_produto = ttk.Button(frame_botoes, text="Cadastrar novo produto", command=cadastrar_produto)
    botao_consultar_produto = ttk.Button(frame_botoes, text="Consultar produto", command=consultar_produto)
    botao_visualizar_estoque = ttk.Button(frame_botoes, text="Visualizar estoque", command=visualizar_estoque)
    botao_excluir_produto = ttk.Button(frame_botoes, text="Excluir produto", command=excluir_produto)

    botao_cadastrar_produto.pack(side=tk.LEFT, padx=10)
    botao_consultar_produto.pack(side=tk.LEFT, padx=10)
    botao_visualizar_estoque.pack(side=tk.LEFT, padx=10)
    botao_excluir_produto.pack(side=tk.LEFT, padx=10)

    botao_sair = ttk.Button(segunda_janela, text="Sair", command=sair)
    botao_sair.pack()

    botao_cadastrar_produto.pack()
    botao_consultar_produto.pack()
    botao_visualizar_estoque.pack()
    botao_excluir_produto.pack()


# Cria a janela principal
root = tk.Tk()
root.title("Atacado RZ")

# Carrega a imagem do atacado usando o Pillow e redimensiona
imagem_original = Image.open("C:/Users/antho/Desktop/Meus programas/AtacadoRZ/Perfil.PNG")
largura, altura = 200, 200
imagem_redimensionada = imagem_original.resize((largura, altura))
imagem_atacado = ImageTk.PhotoImage(imagem_redimensionada)

# Cria um label para exibir a imagem
label_imagem = tk.Label(root, image=imagem_atacado)
label_imagem.pack()

# Adiciona um texto em cima da imagem
texto = "Bem-vindo ao Sistema do Atacado RZ"
subtitulo = "Clique em 'Iniciar' para continuar"
label_texto = tk.Label(root, text=texto, font=("Helvetica", 20))
label_subtitulo = tk.Label(root, text=subtitulo, font=("Helvetica", 12))
label_texto.pack()
label_subtitulo.pack()

# Cria um botão "Iniciar" que chama a função iniciar() quando pressionado
botao_iniciar = ttk.Button(root, text="Iniciar", command=iniciar)
botao_iniciar.pack()

# Inicia a interface gráfica
root.mainloop()