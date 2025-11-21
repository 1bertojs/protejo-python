import tkinter as tk
from tkinter import messagebox

tela = tk.Tk()
tela.title("Cadastro de Usuário")
tela.geometry("320x360")

nome_legal = tk.Label(tela, text="Bem-vindo.\nCadastre-se para acessar nossos serviços:", font=("Arial", 9, "bold"))
nome_legal.pack(pady=10)

def validar_cadastro():
    nome = entry_nome.get().strip()
    email = entry_email.get().strip()
    senha = entry_senha.get()
    confirmasenha = entry_confirmasenha.get()
    termos = caixa_checkbox.get()
    if not nome or not email or not senha or not confirmasenha:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        return False
    if not termos:
        messagebox.showerror("Erro", "Você deve aceitar os termos de uso.")
        return False
    return True

def validar_senhas():
    senha = entry_senha.get()
    confirmasenha = entry_confirmasenha.get()
    if senha != confirmasenha:
        messagebox.showerror("Erro", "As senhas não coincidem!")
        entry_senha.delete(0, tk.END)
        entry_confirmasenha.delete(0, tk.END)
        return False
    return True

def mostrar_emoji(caminho='janela/imagem/pngegg.png'):
    try:
        tela.emoji_img = tk.PhotoImage(file=caminho)
        if hasattr(tela, "emoji_label") and tela.emoji_label.winfo_exists():
            tela.emoji_label.config(image=tela.emoji_img)
        else:
            tela.emoji_label = tk.Label(tela, image=tela.emoji_img)
            tela.emoji_label.pack(pady=5)
    except Exception as e:
        messagebox.showwarning("Imagem", f"Não foi possível carregar a imagem: {caminho}\n{e}")

def cadastrar_usuario():
    if not validar_cadastro():
        return
    if not validar_senhas():
        return
    messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
    entry_nome.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_senha.delete(0, tk.END)
    entry_confirmasenha.delete(0, tk.END)
    caixa_checkbox.set(False)
    mostrar_emoji()

menuCriado = tk.Menu(tela)
menu = tk.Menu(menuCriado, tearoff = 0)
menu.add_command(label="Oi")
menu.add_command(label="Professor")
menu.add_command(label="Rafael")
menu.add_command(label="Muniz")
menuCriado.add_cascade(label="Menu", menu=menu)
tela.config(menu=menuCriado)

label_nome = tk.Label(tela, text="Nome do Usuário:")
label_nome.pack()
entry_nome = tk.Entry(tela)
entry_nome.pack(padx=10, pady=2)

label_email = tk.Label(tela, text="Email:")
label_email.pack()
entry_email = tk.Entry(tela)
entry_email.pack(padx=10, pady=2)

label_senha = tk.Label(tela, text="Senha:")
label_senha.pack()
entry_senha = tk.Entry(tela, show="*")
entry_senha.pack(padx=10, pady=2)

label_confirmasenha = tk.Label(tela, text="Confirme a senha:")
label_confirmasenha.pack()
entry_confirmasenha = tk.Entry(tela, show="*")
entry_confirmasenha.pack(padx=10, pady=2)

caixa_checkbox = tk.BooleanVar()
check = tk.Checkbutton(tela, text="Aceito os termos de uso", variable=caixa_checkbox)
check.pack(pady=10)

botao_cadastrar = tk.Button(tela, text="Cadastrar", command=cadastrar_usuario)
botao_cadastrar.pack(pady=5)

tela.mainloop()