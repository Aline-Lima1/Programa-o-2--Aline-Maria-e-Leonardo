import tkinter as tk  # Biblioteca para criar interfaces gráficas
from tkinter import messagebox  # Para mostrar mensagens em pop-up
import random, sys  # random para embaralhar, sys para sair do app

# Classe que representa uma pergunta
class Pergunta:
    def __init__(self, enunciado, alternativas, correta, curiosidade):
        # Armazena os dados da pergunta
        self.__enunciado = enunciado
        self.__alternativas = alternativas
        self.__correta = correta
        self.__curiosidade = curiosidade

    # Métodos para acessar os dados da pergunta
    def get_enunciado(self):
        return self.__enunciado

    def get_alternativas(self):
        return self.__alternativas

    def get_correta(self):
        return self.__correta

    def get_curiosidade(self):
        return self.__curiosidade

# Lista de perguntas do quiz
perguntas = [
    Pergunta(
        "Qual é o papel da RNA polimerase na transcrição?",
        ["Ligar aminoácidos ao tRNA", "Ler o DNA e formar uma fita de RNA", "Traduzir RNA em proteína", "Romper a dupla-hélice"],
        "Ler o DNA e formar uma fita de RNA",
        "A RNA polimerase é a enzima que sintetiza RNA a partir da fita molde de DNA."
    ),
    Pergunta(
        "Durante a tradução, o que o ribossomo faz?",
        ["Replica o DNA", "Produz energia", "Liga aminoácidos em sequência para formar uma proteína", "Corta o RNA"],
        "Liga aminoácidos em sequência para formar uma proteína",
        "O ribossomo lê os códons do RNA mensageiro e monta a proteína correspondente."
    ),
    Pergunta(
        "O que são íntrons?",
        ["Regiões codificantes do DNA", "Partes do RNA que formam proteínas", "Segmentos removidos do pré-mRNA", "Genes mitocondriais"],
        "Segmentos removidos do pré-mRNA",
        "Íntrons são regiões que não codificam proteínas e são retiradas durante o splicing do RNA."
    ),
    Pergunta(
        "Qual a principal função dos plasmídeos em biotecnologia?",
        ["Produzir ATP", "Codificar enzimas digestivas", "Atuar como vetores de DNA", "Realizar a fotossíntese"],
        "Atuar como vetores de DNA",
        "Plasmídeos são usados para introduzir genes em organismos como bactérias."
    ),
    Pergunta(
        "Em que fase do ciclo celular ocorre a duplicação do DNA?",
        ["G1", "G2", "S", "Mitose"],
        "S",
        "A fase S (síntese) é onde ocorre a replicação do DNA antes da divisão celular."
    )
]

# Classe principal que controla o quiz
class QuizApp:
    def __init__(self, root):
        self.root = root
        root.title("DNA Quiz 🎓")
        root.geometry("520x450")
        root.configure(bg="#e0ffff")

        # Embaralha as perguntas
        self.perguntas = random.sample(perguntas, len(perguntas))
        self.indice = self.pontos = 0  # Índice da pergunta atual e pontuação

        # Título da pergunta
        self.lbl = tk.Label(root, font=("Arial", 14, "bold"), wraplength=480, bg="#e0ffff")
        self.lbl.pack(pady=20)

        # Botões para alternativas
        self.botoes = [tk.Button(root, width=40, font=("Arial", 10), bg="#add8e6",
                                 command=lambda i=i: self.responder(i)) for i in range(4)]
        for b in self.botoes:
            b.pack(pady=5)

        # Feedback de resposta
        self.feedback = tk.Label(root, font=("Arial", 12), bg="#e0ffff")
        self.feedback.pack(pady=10)

        # Pontuação atual
        self.pontuacao = tk.Label(root, text="Pontuação: 0", font=("Arial", 12, "bold"), bg="#e0ffff")
        self.pontuacao.pack()

        # Botão de sair
        self.botao_sair = tk.Button(root, text="❌ Sair", bg="#ffcc99", font=("Arial", 12), command=self.sair)
        self.botao_sair.pack(pady=10)

        # Confirma ação ao fechar a janela
        root.protocol("WM_DELETE_WINDOW", self.sair)

        # Exibe a primeira pergunta
        self.proxima()

    # Mostra a próxima pergunta
    def proxima(self):
        self.feedback.config(text="")
        if self.indice < len(self.perguntas):
            p = self.perguntas[self.indice]
            self.lbl.config(text=p.get_enunciado())
            alternativas = p.get_alternativas()
            random.shuffle(alternativas)
            for i, alt in enumerate(alternativas):
                self.botoes[i].config(text=alt, state="normal", bg="#add8e6")
        else:
            self.final()

    # Avalia a resposta escolhida
    def responder(self, i):
        for b in self.botoes:
            b.config(state="disabled")

        p = self.perguntas[self.indice]
        correta = p.get_correta()
        curiosidade = p.get_curiosidade()
        escolha = self.botoes[i].cget("text")
        acerto = escolha == correta

        self.pontos += acerto
        self.pontuacao.config(text=f"Pontuação: {self.pontos}")

        emoji = "✅" if acerto else "❌"
        cor = "#90ee90" if acerto else "#ff6347"
        self.feedback.config(
            text=f"{emoji} {('Correto!' if acerto else f'Errado! Correto: {correta}')}\n💡 {curiosidade}",
            fg="green" if acerto else "red"
        )

        # Destaca a resposta correta
        for b in self.botoes:
            if b.cget("text") == correta:
                b.config(bg="#90ee90")
        self.botoes[i].config(bg=cor)

        # Vai para a próxima pergunta após 3 segundos
        self.root.after(3000, self.avancar)

    # Avança para próxima pergunta
    def avancar(self):
        self.indice += 1
        self.proxima()

    # Finaliza o quiz com mensagem
    def final(self):
        nota = self.pontos / len(self.perguntas)
        if nota == 1:
            msg = "🏆 Gabaritou! Você é um mestre da Biologia!"
        elif nota >= 0.6:
            msg = "👏 Muito bem! Quase lá!"
        else:
            msg = "📚 Que tal revisar um pouco mais?"

        resultado = f"Você acertou {self.pontos} de {len(self.perguntas)}!\n{msg}"

        self.lbl.config(text=resultado)
        self.feedback.config(text="Fim de jogo 🎉", fg="blue")
        messagebox.showinfo("Fim", resultado)

        for b in self.botoes:
            b.config(state="disabled")

    # Pergunta se o usuário quer sair do jogo
    def sair(self):
        if messagebox.askyesno("Sair", "Deseja realmente sair?"):
            self.root.destroy()
            sys.exit()

# Executa o programa
if __name__ == "__main__":
    tk.Tk().after(0, lambda: QuizApp(tk._default_root))
    tk.mainloop()
