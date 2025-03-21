import tkinter as tk
from tkinter import messagebox
import re

class SistemaEstudantes:
    def __init__(self, listbox_ranking):
        # Armazenar os estudantes
        self.estudantes = []

        # Variáveis globais para exibição na interface gráfica
        self.reprovados_text = None
        self.recuperacao_text = None
        self.melhores_text = None

        # Função de validação das notas (apenas números de 1 a 10)
        self.validar_nota = self._criar_validador_nota()

        # Variável global para o listbox de ranking
        self.listbox_ranking = listbox_ranking 

    def _criar_validador_nota(self):
        def validar_nota(P):
            if P == "":
                return True
            try:
                valor = float(P)
                return 1 <= valor <= 10
            except ValueError:
                return False
        return validar_nota

    # Função de alta ordem para validar as entradas
    def criar_validador(self, validador):
        def validar_entrada(nome, *notas):
            # Verificar se o nome não está vazio
            if not nome.strip():
                raise ValueError("O nome não pode estar vazio.")

            # Verificar se o nome contém apenas letras e espaços
            if not re.match("^[A-Za-záéíóúãõâêîôûÁÉÍÓÚÃÕÂÊÎÔÛ ]+$", nome):
                raise ValueError("O nome não pode conter números ou caracteres especiais.")

            # Verificar se o nome contém pelo menos duas palavras e cada palavra tem no mínimo 3 letras
            palavras = nome.split()
            if len(palavras) < 2:
                raise ValueError("O nome deve conter pelo menos duas palavras.")

            if any(len(palavra) < 3 for palavra in palavras):
                raise ValueError("Cada palavra do nome deve ter no mínimo 3 letras.")

            # Verificar se todas as notas foram preenchidas
            if any(nota == "" for nota in notas):
                raise ValueError(
                    "Todos os campos de notas precisam ser preenchidos, ao inserir as notas use o ponto (.) em vez da vírgula (,).")

            # Tentar converter as notas para float
            try:
                notas = [float(nota) for nota in notas]
            except ValueError:
                raise ValueError("As notas devem ser números válidos.")

            # Verificar se todas as notas estão no intervalo entre 1 e 10
            if any(nota < 1 or nota > 10 for nota in notas):
                raise ValueError("As notas devem estar entre 1 e 10.")

            return validador(notas)

        return validar_entrada

    # Closure para adicionar estudante
    def criar_adicionador(self):
        def adicionar_estudante(entry_nome, entry_nota1, entry_nota2, entry_nota3):
            nome = entry_nome.get().strip()
            notas = [entry_nota1.get(), entry_nota2.get(), entry_nota3.get()]

            try:
                notas = self.criar_validador(lambda notas: notas)(nome, *notas)
                media = sum(notas) / len(notas)

                self.estudantes.append({'nome': nome, 'media': media})

                self.limpar_campos(entry_nome, entry_nota1, entry_nota2, entry_nota3)
                self.atualizar_ranking()

                messagebox.showinfo("Sucesso", f"Estudante {nome} adicionado com sucesso!")

            except ValueError as e:
                messagebox.showerror("Erro", str(e))

        return adicionar_estudante

    # Função para remover estudante
    def remover_estudante(self):
        try:
            selected_index = self.listbox_ranking.curselection()
            if not self.estudantes:  # Verifica se a lista de estudantes está vazia
                raise ValueError("Selecione um estudante para remover.")

            if not self.estudantes:  # Verifica se a lista de estudantes está vazia
                raise ValueError("Nenhum estudante para remover.")

            index = selected_index[0]
            estudante_remover = self.estudantes.pop(index)
            self.atualizar_ranking()

            messagebox.showinfo("Sucesso", f"Estudante {estudante_remover['nome']} removido com sucesso!")

        except ValueError as e:
            messagebox.showerror("Erro", str(e))

    # Atualiza o ranking dos estudantes
    def atualizar_ranking(self):
        self.estudantes.sort(key=lambda e: e['media'], reverse=True)

        self.listbox_ranking.delete(0, tk.END)  # Limpa o listbox
        for i, e in enumerate(self.estudantes):
            self.listbox_ranking.insert(tk.END, f"{i + 1}. {e['nome']} - Média: {e['media']:.2f}")

        # Atualiza os textos de status
        melhores = [e['nome'] for e in self.estudantes if e['media'] >= 7]
        recuperacao = [e['nome'] for e in self.estudantes if 5 <= e['media'] < 7]
        reprovados = [e['nome'] for e in self.estudantes if e['media'] < 5]

        if self.melhores_text:
            self.melhores_text.set(", ".join(melhores) if melhores else "Nenhum aprovado")
        if self.recuperacao_text:
            self.recuperacao_text.set(", ".join(recuperacao) if recuperacao else "Nenhum em recuperação")
        if self.reprovados_text:
            self.reprovados_text.set(", ".join(reprovados) if reprovados else "Nenhum reprovado")

    # Função para limpar os campos
    def limpar_campos(self, entry_nome, entry_nota1, entry_nota2, entry_nota3):
        entry_nome.delete(0, tk.END)
        entry_nota1.delete(0, tk.END)
        entry_nota2.delete(0, tk.END)
        entry_nota3.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ranking de Estudantes")
    root.geometry("600x800")
    root.config(bg="#f4f4f4")

    # Criar a instância do SistemaEstudantes (sem listbox_ranking ainda)
    sistema = SistemaEstudantes(None)

    # Registrar o validate_command após a criação do sistema
    validate_command = root.register(sistema.validar_nota)

    # Frame para a entrada de dados
    frame_entrada = tk.Frame(root, bg="#f4f4f4")
    frame_entrada.pack(pady=15)

    # Labels e Entries para nome e notas
    tk.Label(frame_entrada, text="Nome:", bg="#f4f4f4", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_nome = tk.Entry(frame_entrada, width=30)
    entry_nome.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame_entrada, text="Nota 1:", bg="#f4f4f4", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_nota1 = tk.Entry(frame_entrada, width=10, validate="key", validatecommand=(validate_command, "%P"))
    entry_nota1.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame_entrada, text="Nota 2:", bg="#f4f4f4", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_nota2 = tk.Entry(frame_entrada, width=10, validate="key", validatecommand=(validate_command, "%P"))
    entry_nota2.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(frame_entrada, text="Nota 3:", bg="#f4f4f4", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_nota3 = tk.Entry(frame_entrada, width=10, validate="key", validatecommand=(validate_command, "%P"))
    entry_nota3.grid(row=3, column=1, padx=10, pady=5)

    # Botões
    btn_add = tk.Button(root, text="Adicionar Estudante", command=lambda: sistema.criar_adicionador()(entry_nome, entry_nota1, entry_nota2, entry_nota3),
                        bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), width=25)
    btn_add.pack(pady=15)

    btn_remove = tk.Button(root, text="Remover Estudante", command=lambda: sistema.remover_estudante(),
                            bg="#FF5733", fg="white", font=("Arial", 12, "bold"), width=25)
    btn_remove.pack(pady=10)

    # Frame para o ranking
    frame_ranking = tk.Frame(root, bg="#f4f4f4")
    frame_ranking.pack(pady=10)

    # Label e Listbox para o ranking
    tk.Label(frame_ranking, text="Ranking dos Estudantes:", bg="#f4f4f4", font=("Arial", 12, "bold")).pack()
    listbox_ranking = tk.Listbox(frame_ranking, width=60, height=10, font=("Arial", 10))
    listbox_ranking.pack(pady=10)

    # Atualizar a instância do sistema com o listbox_ranking
    sistema.listbox_ranking = listbox_ranking

    # Frame para os status (melhores, recuperação, reprovados)
    frame_status = tk.Frame(root, bg="#f4f4f4")
    frame_status.pack(pady=10)

    # Melhores estudantes
    sistema.melhores_text = tk.StringVar()
    tk.Label(frame_status, text="Melhores Estudantes:", bg="#f4f4f4", font=("Arial", 12, "bold")).pack()
    tk.Label(frame_status, textvariable=sistema.melhores_text, bg="#f4f4f4", font=("Arial", 10)).pack(pady=5)

    # Estudantes em recuperação
    sistema.recuperacao_text = tk.StringVar()
    tk.Label(frame_status, text="Estudantes em Recuperação:", bg="#f4f4f4", font=("Arial", 12, "bold")).pack()
    tk.Label(frame_status, textvariable=sistema.recuperacao_text, bg="#f4f4f4", font=("Arial", 10)).pack(pady=5)

    # Estudantes reprovados
    sistema.reprovados_text = tk.StringVar()
    tk.Label(frame_status, text="Estudantes Reprovados:", bg="#f4f4f4", font=("Arial", 12, "bold")).pack()
    tk.Label(frame_status, textvariable=sistema.reprovados_text, bg="#f4f4f4", font=("Arial", 10)).pack(pady=5)

    root.mainloop()