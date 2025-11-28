import tkinter as tk
from tkinter import ttk, messagebox


class View:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Análise da Saúde Física")
        self.root.geometry("700x600")
        self.root.configure(bg="#f5f5f5")

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.container = tk.Frame(self.root, bg="#f5f5f5")
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        # Criar telas
        self.createHome()
        self.createCardio()
        self.createMusculo()
        self.createDados()

        for frame in (self.home, self.cardio, self.musculo, self.dados):
            frame.grid(row=0, column=0, sticky="nsew")

        self.showHome()
        self.root.mainloop()

    def showHome(self): self.home.tkraise()
    def showCardio(self): self.cardio.tkraise()
    def showMusculo(self): self.musculo.tkraise()
    def showDados(self): self.dados.tkraise()

    # ======================================================================================
    # TELA PRINCIPAL
    # ======================================================================================
    def createHome(self):
        self.home = tk.Frame(self.container, bg="#f5f5f5")
        self.home.rowconfigure(0, weight=1)
        self.home.rowconfigure(1, weight=2)
        self.home.rowconfigure(2, weight=1)
        self.home.columnconfigure(0, weight=1)

        header = tk.Label(
            self.home,
            text="Sistema de Análise da Saúde Física de Crianças e Adolescentes",
            font=("Arial", 16, "bold"),
            bg="#f5f5f5",
            wraplength=450
        )
        header.grid(row=0, column=0, pady=20)

        frame = tk.Frame(self.home, bg="white", padx=20, pady=30)
        frame.grid(row=1, column=0, pady=10)

        btn_cardio = tk.Button(
            frame,
            text="Avaliação Cardiovascular",
            font=("Arial", 14, "bold"),
            bg="#1565C0", fg="white",
            width=25, height=2, bd=0,
            command=self.showCardio
        )
        btn_cardio.pack(pady=15, fill="x")

        btn_musculo = tk.Button(
            frame,
            text="Avaliação Musculoesquelética",
            font=("Arial", 14, "bold"),
            bg="#D32F2F", fg="white",
            width=25, height=2, bd=0,
            command=self.showMusculo
        )
        btn_musculo.pack(pady=15, fill="x")

        btn_dados = tk.Button(
            self.home,
            text="Dados de Alunos",
            font=("Arial", 12, "bold"),
            bg="#424242", fg="white",
            width=20, bd=0,
            command=self.showDados
        )
        btn_dados.grid(row=2, column=0, pady=20)

    # ======================================================================================
    # TELA CARDIOVASCULAR COMPLETA
    # ======================================================================================
    def createCardio(self):
        self.cardio = tk.Frame(self.container, bg="#e6e6e6")

        # Botão voltar
        btn_voltar = tk.Button(
            self.cardio, text="VOLTAR",
            bg="#1565C0", fg="white",
            font=("Arial", 10, "bold"),
            width=10,
            command=self.showHome
        )
        btn_voltar.pack(anchor="nw", pady=10, padx=10)

        # Título
        titulo = tk.Label(
            self.cardio,
            text="AVALIAÇÃO CARDIOVASCULAR",
            font=("Arial", 18, "bold"),
            bg="#e6e6e6"
        )
        titulo.pack()

        # Informações do aluno
        info = tk.Frame(self.cardio, bg="#e6e6e6")
        info.pack(pady=15)

        tk.Label(info, text="ALUNO", font=("Arial", 10, "bold"), bg="#e6e6e6").grid(row=0, column=0)
        tk.Entry(info, width=25).grid(row=1, column=0, padx=10)

        tk.Label(info, text="IDADE", font=("Arial", 10, "bold"), bg="#e6e6e6").grid(row=0, column=1)
        tk.Entry(info, width=10).grid(row=1, column=1, padx=10)

        tk.Label(info, text="SEXO", font=("Arial", 10, "bold"), bg="#e6e6e6").grid(row=0, column=2)
        ttk.Combobox(info, values=["Masculino", "Feminino"], width=12).grid(row=1, column=2, padx=10)

        # Container de colunas
        cols = tk.Frame(self.cardio, bg="#e6e6e6")
        cols.pack(pady=20)

        # Coluna IMC
        left = tk.Frame(cols, bg="#e6e6e6")
        left.grid(row=0, column=0, padx=40)

        tk.Label(left, text="IMC", font=("Arial", 14, "bold"), bg="#e6e6e6").pack()

        tk.Label(left, text="PESO", font=("Arial", 10, "bold"), bg="#e6e6e6").pack(anchor="w")
        tk.Entry(left, width=20).pack(pady=5)

        tk.Label(left, text="ALTURA", font=("Arial", 10, "bold"), bg="#e6e6e6").pack(anchor="w")
        tk.Entry(left, width=20).pack(pady=5)

        # Coluna corrida
        right = tk.Frame(cols, bg="#e6e6e6")
        right.grid(row=0, column=1, padx=40)

        tk.Label(right, text="TESTE DE CORRIDA", font=("Arial", 14, "bold"), bg="#e6e6e6").pack()

        tk.Label(
            right,
            text="O TESTE TEM COMO OBJETIVO MEDIR A\nDISTÂNCIA PERCORRIDA EM 6 MINUTOS.",
            font=("Arial", 9),
            bg="#e6e6e6", justify="left"
        ).pack()

        tk.Label(right, text="METROS", font=("Arial", 10, "bold"), bg="#e6e6e6").pack(anchor="w")
        tk.Entry(right, width=20).pack(pady=5)

        # Botão Salvar
        tk.Button(
            self.cardio, text="SALVAR DADOS",
            bg="#1565C0", fg="white", font=("Arial", 12, "bold"),
            width=15
        ).pack(pady=20)

    # ======================================================================================
    # TELA MUSCULOESQUELÉTICA COMPLETA
    # ======================================================================================
    def createMusculo(self):
        self.musculo = tk.Frame(self.container, bg="#e6e6e6")

        btn_voltar = tk.Button(
            self.musculo, text="VOLTAR",
            bg="#1565C0", fg="white",
            font=("Arial", 10, "bold"),
            width=10,
            command=self.showHome
        )
        btn_voltar.pack(anchor="nw", pady=10, padx=10)

        titulo = tk.Label(
            self.musculo,
            text="AVALIAÇÃO MUSCULOESQUELÉTICA",
            font=("Arial", 18, "bold"),
            bg="#e6e6e6"
        )
        titulo.pack()

        info = tk.Frame(self.musculo, bg="#e6e6e6")
        info.pack(pady=15)

        tk.Label(info, text="ALUNO", font=("Arial", 10, "bold"), bg="#e6e6e6").grid(row=0, column=0)
        tk.Entry(info, width=25).grid(row=1, column=0, padx=10)

        tk.Label(info, text="IDADE", font=("Arial", 10, "bold"), bg="#e6e6e6").grid(row=0, column=1)
        tk.Entry(info, width=10).grid(row=1, column=1, padx=10)

        tk.Label(info, text="SEXO", font=("Arial", 10, "bold"), bg="#e6e6e6").grid(row=0, column=2)
        ttk.Combobox(info, values=["Masculino", "Feminino"], width=12).grid(row=1, column=2, padx=10)

        cols = tk.Frame(self.musculo, bg="#e6e6e6")
        cols.pack(pady=20)

        # Esquerda
        left = tk.Frame(cols, bg="#e6e6e6")
        left.grid(row=0, column=0, padx=40)

        tk.Label(left, text="TESTE DE SENTAR E ALCANÇAR", font=("Arial", 14, "bold"), bg="#e6e6e6").pack()

        tk.Label(
            left,
            text="O TESTE MEDE O ALCANCE EM CENTÍMETROS\nA PARTIR DE UMA TENTATIVA EM BARRA DE\n"
                 "FLEXÃO. A FLEXIBILIDADE DOS MÚSCULOS\nPOSTERIORES DEVE SER OBSERVADA.",
            font=("Arial", 9), bg="#e6e6e6", justify="left"
        ).pack()

        tk.Label(left, text="CENTÍMETROS", font=("Arial", 10, "bold"), bg="#e6e6e6").pack(anchor="w")
        tk.Entry(left, width=20).pack(pady=5)

        # Direita
        right = tk.Frame(cols, bg="#e6e6e6")
        right.grid(row=0, column=1, padx=40)

        tk.Label(right, text="TESTE DE ABDOMINAIS", font=("Arial", 14, "bold"), bg="#e6e6e6").pack()

        tk.Label(
            right,
            text="O TESTE MEDE QUANTAS REPETIÇÕES\nDE ABDOMINAIS O ALUNO CONSEGUE\nEM UM MINUTO.",
            font=("Arial", 9), bg="#e6e6e6", justify="left"
        ).pack()

        tk.Label(right, text="ABDÔMINAIS", font=("Arial", 10, "bold"), bg="#e6e6e6").pack(anchor="w")
        tk.Entry(right, width=20).pack(pady=5)

        tk.Button(
            self.musculo, text="SALVAR DADOS",
            bg="#1565C0", fg="white", font=("Arial", 12, "bold"),
            width=15
        ).pack(pady=20)

    # ======================================================================================
    # TELA DADOS (ainda simples)
    # ======================================================================================
    def createDados(self):
        self.dados = tk.Frame(self.container, bg="white")

        title = tk.Label(
            self.dados,
            text="Dados de Alunos",
            font=("Arial", 18, "bold"),
            bg="white"
        )
        title.pack(pady=20)

        tk.Button(
            self.dados, text="Voltar",
            bg="#424242", fg="white",
            width=20,
            command=self.showHome
        ).pack(pady=20)


View()
