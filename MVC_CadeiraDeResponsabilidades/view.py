import tkinter as tk
from tkinter import ttk, messagebox
import controller 

class View:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Análise da Saúde Física")
        self.root.geometry("900x650")
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
        self.createDetalhes()

        for frame in (self.home, self.cardio, self.musculo, self.dados, self.detalhes):
            frame.grid(row=0, column=0, sticky="nsew")

        self.showHome()
        self.root.mainloop()

    def showHome(self): self.home.tkraise()
    def showCardio(self): self.cardio.tkraise()
    def showMusculo(self): self.musculo.tkraise()
    def showDados(self): self.dados.tkraise()
    def showDetalhes(self): self.detalhes.tkraise()

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
    # TELA CARDIOVASCULAR
    # ======================================================================================
    def createCardio(self):
        self.cardio = tk.Frame(self.container, bg="#e6e6e6")

        btn_voltar = tk.Button(
            self.cardio, text="VOLTAR",
            bg="#1565C0", fg="white",
            font=("Arial", 10, "bold"),
            width=10,
            command=self.showHome
        )
        btn_voltar.pack(anchor="nw", pady=10, padx=10)

        titulo = tk.Label(
            self.cardio,
            text="AVALIAÇÃO CARDIOVASCULAR",
            font=("Arial", 18, "bold"),
            bg="#e6e6e6"
        )
        titulo.pack()

        info = tk.Frame(self.cardio, bg="#e6e6e6")
        info.pack(pady=15)

        tk.Label(info, text="ALUNO", font=("Arial", 10, "bold"), bg="#e6e6e6").grid(row=0, column=0)
        self.entry_nome = tk.Entry(info, width=25)
        self.entry_nome.grid(row=1, column=0, padx=10)

        tk.Label(info, text="IDADE", font=("Arial", 10, "bold"), bg="#e6e6e6").grid(row=0, column=1)
        self.entry_idade = tk.Entry(info, width=10)
        self.entry_idade.grid(row=1, column=1, padx=10)

        tk.Label(info, text="SEXO", font=("Arial", 10, "bold"), bg="#e6e6e6").grid(row=0, column=2)
        self.sexo = ttk.Combobox(info, values=["Masculino", "Feminino"], width=12)
        self.sexo.grid(row=1, column=2, padx=10)

        cols = tk.Frame(self.cardio, bg="#e6e6e6")
        cols.pack(pady=20)

        left = tk.Frame(cols, bg="#e6e6e6")
        left.grid(row=0, column=0, padx=40)

        tk.Label(left, text="IMC", font=("Arial", 14, "bold"), bg="#e6e6e6").pack()

        tk.Label(left, text="PESO", font=("Arial", 10, "bold"), bg="#e6e6e6").pack(anchor="w")
        self.entry_peso = tk.Entry(left, width=20)
        self.entry_peso.pack(pady=5)

        tk.Label(left, text="ALTURA", font=("Arial", 10, "bold"), bg="#e6e6e6").pack(anchor="w")
        self.entry_altura = tk.Entry(left, width=20)
        self.entry_altura.pack(pady=5)

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
        self.entry_metros = tk.Entry(right, width=20)
        self.entry_metros.pack(pady=5)
        

        tk.Button(
            self.cardio, text="SALVAR DADOS",
            bg="#1565C0", fg="white", font=("Arial", 12, "bold"),
            width=15,
            command= lambda: controller.Controller.salvar_dados_cardiovasculares(self, self.entry_nome.get(), self.entry_idade.get(), self.sexo.get(), self.entry_peso.get(), self.entry_altura.get(), self.entry_metros.get())
        ).pack(pady=20)

    # ======================================================================================
    # TELA MUSCULOESQUELÉTICA
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
    # TELA DE DADOS DOS ALUNOS
    # ======================================================================================
    def createDados(self):
        self.dados = tk.Frame(self.container, bg="#f5f5f5")
        
        # Header
        header_frame = tk.Frame(self.dados, bg="#f5f5f5")
        header_frame.pack(fill="x", padx=20, pady=15)
        
        btn_voltar = tk.Button(
            header_frame, text="← VOLTAR",
            bg="#424242", fg="white",
            font=("Arial", 10, "bold"),
            width=12, bd=0,
            command=self.showHome
        )
        btn_voltar.pack(side="left")
        
        titulo = tk.Label(
            header_frame,
            text="DADOS DOS ALUNOS",
            font=("Arial", 20, "bold"),
            bg="#f5f5f5"
        )
        titulo.pack(side="left", padx=30)
        
        # Frame para a tabela com scrollbar
        table_frame = tk.Frame(self.dados, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        
        # Canvas para scroll
        canvas = tk.Canvas(table_frame, bg="white", highlightthickness=0, yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=canvas.yview)
        
        # Frame interno do canvas
        self.alunos_container = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=self.alunos_container, anchor="nw")
        
        # Header da tabela
        header_table = tk.Frame(self.alunos_container, bg="#424242", height=50)
        header_table.pack(fill="x", pady=(0, 2))
        
        tk.Label(
            header_table, text="NOME", font=("Arial", 11, "bold"),
            bg="#424242", fg="white", width=25, anchor="w"
        ).pack(side="left", padx=15, pady=10)
        
        tk.Label(
            header_table, text="IDADE", font=("Arial", 11, "bold"),
            bg="#424242", fg="white", width=8
        ).pack(side="left", padx=5, pady=10)
        
        tk.Label(
            header_table, text="SEXO", font=("Arial", 11, "bold"),
            bg="#424242", fg="white", width=10
        ).pack(side="left", padx=5, pady=10)
        
        tk.Label(
            header_table, text="CARDIOVASCULAR", font=("Arial", 11, "bold"),
            bg="#424242", fg="white", width=18
        ).pack(side="left", padx=5, pady=10)
        
        tk.Label(
            header_table, text="MUSCULOESQUELÉTICA", font=("Arial", 11, "bold"),
            bg="#424242", fg="white", width=20
        ).pack(side="left", padx=5, pady=10)
        
        # Dados de exemplo (isso virá do Controller depois)
        alunos_exemplo = [
            {"nome": "João Silva", "idade": 12, "sexo": "M", "cardio": "ok", "musculo": "risco"},
            {"nome": "Maria Oliveira", "idade": 14, "sexo": "F", "cardio": "ok", "musculo": "ok"},
            {"nome": "Pedro Santos", "idade": 13, "sexo": "M", "cardio": "risco", "musculo": "ok"},
            {"nome": "Ana Costa", "idade": 11, "sexo": "F", "cardio": "ok", "musculo": "ok"},
            {"nome": "Lucas Ferreira", "idade": 15, "sexo": "M", "cardio": "risco", "musculo": "risco"},
            {"nome": "Beatriz Lima", "idade": 12, "sexo": "F", "cardio": "ok", "musculo": "ok"},
            {"nome": "Gabriel Souza", "idade": 14, "sexo": "M", "cardio": "ok", "musculo": "risco"},
        ]
        
        # Criar linhas de alunos
        for i, aluno in enumerate(alunos_exemplo):
            bg_color = "#f9f9f9" if i % 2 == 0 else "white"
            self.criarLinhaAluno(aluno, bg_color)
        
        # Atualizar scroll region
        self.alunos_container.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
        
        # Legenda
        legenda_frame = tk.Frame(self.dados, bg="#f5f5f5")
        legenda_frame.pack(pady=15)
        
        tk.Label(
            legenda_frame, text="● Zona Saudável",
            font=("Arial", 10), bg="#f5f5f5", fg="#2E7D32"
        ).pack(side="left", padx=15)
        
        tk.Label(
            legenda_frame, text="● Zona de Risco",
            font=("Arial", 10), bg="#f5f5f5", fg="#C62828"
        ).pack(side="left", padx=15)

    def criarLinhaAluno(self, aluno, bg_color):
        """Cria uma linha na tabela para um aluno"""
        linha = tk.Frame(self.alunos_container, bg=bg_color, cursor="hand2", height=60)
        linha.pack(fill="x", pady=1)
        
        # Efeito hover
        def on_enter(e):
            linha.config(bg="#e3f2fd")
            for child in linha.winfo_children():
                if isinstance(child, (tk.Label, tk.Frame)):
                    child.config(bg="#e3f2fd")
        
        def on_leave(e):
            linha.config(bg=bg_color)
            for child in linha.winfo_children():
                if isinstance(child, (tk.Label, tk.Frame)):
                    child.config(bg=bg_color)
        
        def on_click(e):
            self.showDetalhes()
        
        linha.bind("<Enter>", on_enter)
        linha.bind("<Leave>", on_leave)
        linha.bind("<Button-1>", on_click)
        
        # Nome
        nome_label = tk.Label(
            linha, text=aluno["nome"],
            font=("Arial", 11), bg=bg_color,
            width=25, anchor="w"
        )
        nome_label.pack(side="left", padx=15, pady=15)
        nome_label.bind("<Button-1>", on_click)
        
        # Idade
        idade_label = tk.Label(
            linha, text=str(aluno["idade"]),
            font=("Arial", 11), bg=bg_color, width=8
        )
        idade_label.pack(side="left", padx=5, pady=15)
        idade_label.bind("<Button-1>", on_click)
        
        # Sexo
        sexo_label = tk.Label(
            linha, text=aluno["sexo"],
            font=("Arial", 11), bg=bg_color, width=10
        )
        sexo_label.pack(side="left", padx=5, pady=15)
        sexo_label.bind("<Button-1>", on_click)
        
        # Status Cardiovascular
        cardio_color = "#2E7D32" if aluno["cardio"] == "ok" else "#C62828"
        cardio_text = "✓ Saudável" if aluno["cardio"] == "ok" else "✗ Zona de Risco"
        cardio_label = tk.Label(
            linha, text=cardio_text,
            font=("Arial", 11, "bold"), bg=bg_color,
            fg=cardio_color, width=18
        )
        cardio_label.pack(side="left", padx=5, pady=15)
        cardio_label.bind("<Button-1>", on_click)
        
        # Status Musculoesquelético
        musculo_color = "#2E7D32" if aluno["musculo"] == "ok" else "#C62828"
        musculo_text = "✓ Saudável" if aluno["musculo"] == "ok" else "✗ Zona de Risco"
        musculo_label = tk.Label(
            linha, text=musculo_text,
            font=("Arial", 11, "bold"), bg=bg_color,
            fg=musculo_color, width=20
        )
        musculo_label.pack(side="left", padx=5, pady=15)
        musculo_label.bind("<Button-1>", on_click)

    # ======================================================================================
    # TELA DE DETALHES DO ALUNO
    # ======================================================================================
    def createDetalhes(self):
        self.detalhes = tk.Frame(self.container, bg="#f5f5f5")
        
        # Header
        header = tk.Frame(self.detalhes, bg="#424242")
        header.pack(fill="x")
        
        btn_voltar = tk.Button(
            header, text="← VOLTAR",
            bg="#424242", fg="white",
            font=("Arial", 10, "bold"),
            bd=0,
            command=self.showDados
        )
        btn_voltar.pack(side="left", padx=20, pady=15)
        
        tk.Label(
            header, text="DETALHES DO ALUNO",
            font=("Arial", 18, "bold"),
            bg="#424242", fg="white"
        ).pack(side="left", padx=20)
        
        # Informações do aluno
        info_frame = tk.Frame(self.detalhes, bg="white", padx=30, pady=20)
        info_frame.pack(fill="x", padx=40, pady=20)
        
        tk.Label(
            info_frame, text="João Silva",
            font=("Arial", 20, "bold"), bg="white"
        ).pack(anchor="w")
        
        detalhes_text = "Idade: 12 anos  |  Sexo: Masculino"
        tk.Label(
            info_frame, text=detalhes_text,
            font=("Arial", 11), bg="white", fg="#666"
        ).pack(anchor="w", pady=5)
        
        # Container para as avaliações
        avaliacoes_container = tk.Frame(self.detalhes, bg="#f5f5f5")
        avaliacoes_container.pack(fill="both", expand=True, padx=40, pady=10)
        
        # Avaliação Cardiovascular
        cardio_frame = tk.Frame(avaliacoes_container, bg="white", padx=25, pady=20)
        cardio_frame.pack(fill="x", pady=10)
        
        cardio_header = tk.Frame(cardio_frame, bg="#1565C0")
        cardio_header.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            cardio_header, text="AVALIAÇÃO CARDIOVASCULAR",
            font=("Arial", 14, "bold"), bg="#1565C0", fg="white"
        ).pack(pady=10)
        
        # Status
        status_cardio = tk.Frame(cardio_frame, bg="white")
        status_cardio.pack(fill="x", pady=10)
        
        tk.Label(
            status_cardio, text="Status:",
            font=("Arial", 11, "bold"), bg="white"
        ).pack(side="left")
        
        tk.Label(
            status_cardio, text="✓ Zona Saudável",
            font=("Arial", 11, "bold"), bg="white", fg="#2E7D32"
        ).pack(side="left", padx=10)
        
        # Resultados
        tk.Label(
            cardio_frame, text="IMC: 18.5 kg/m² (Ideal: 16-20 kg/m²)",
            font=("Arial", 10), bg="white", anchor="w"
        ).pack(fill="x", pady=5)
        
        tk.Label(
            cardio_frame, text="Teste de Corrida: 1200m (Ideal: ≥1100m)",
            font=("Arial", 10), bg="white", anchor="w"
        ).pack(fill="x", pady=5)
        
        # Avaliação Musculoesquelética
        musculo_frame = tk.Frame(avaliacoes_container, bg="white", padx=25, pady=20)
        musculo_frame.pack(fill="x", pady=10)
        
        musculo_header = tk.Frame(musculo_frame, bg="#D32F2F")
        musculo_header.pack(fill="x", pady=(0, 15))
        
        tk.Label(
            musculo_header, text="AVALIAÇÃO MUSCULOESQUELÉTICA",
            font=("Arial", 14, "bold"), bg="#D32F2F", fg="white"
        ).pack(pady=10)
        
        # Status
        status_musculo = tk.Frame(musculo_frame, bg="white")
        status_musculo.pack(fill="x", pady=10)
        
        tk.Label(
            status_musculo, text="Status:",
            font=("Arial", 11, "bold"), bg="white"
        ).pack(side="left")
        
        tk.Label(
            status_musculo, text="✗ Zona de Risco",
            font=("Arial", 11, "bold"), bg="white", fg="#C62828"
        ).pack(side="left", padx=10)
        
        # Resultados
        tk.Label(
            musculo_frame, text="Sentar e Alcançar: 18cm (Ideal: ≥25cm)",
            font=("Arial", 10), bg="white", anchor="w"
        ).pack(fill="x", pady=5)
        
        tk.Label(
            musculo_frame, text="Abdominais: 25 rep. (Ideal: ≥35 rep.)",
            font=("Arial", 10), bg="white", anchor="w"
        ).pack(fill="x", pady=5)


View()