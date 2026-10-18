import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import csv

class EscalaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Escala 5x2 - Automação RH")
        self.root.geometry("700x650")
        self.root.configure(bg="#F4F6F9")

        # Título
        lbl_titulo = tk.Label(root, text="📅 Gerador de Escala 5x2", font=("Helvetica", 18, "bold"), bg="#F4F6F9", fg="#2C3E50")
        lbl_titulo.pack(pady=15)

        # Frame de Configuração do Modo
        frame_modo = tk.LabelFrame(root, text=" ⚙️ Período de Funcionamento ", font=("Helvetica", 11, "bold"), bg="#F4F6F9", fg="#34495E", padx=15, pady=10)
        frame_modo.pack(fill="x", padx=20, pady=5)

        self.modo_var = tk.StringVar(value="6")
        rb1 = tk.Radiobutton(frame_modo, text="Segunda a Sábado (6 dias)", variable=self.modo_var, value="6", font=("Helvetica", 10), bg="#F4F6F9")
        rb2 = tk.Radiobutton(frame_modo, text="Segunda a Domingo (7 dias)", variable=self.modo_var, value="7", font=("Helvetica", 10), bg="#F4F6F9")
        rb1.pack(anchor="w")
        rb2.pack(anchor="w")

        # Frame de Funcionários
        frame_func = tk.LabelFrame(root, text=" 👥 Cadastro da Equipe ", font=("Helvetica", 11, "bold"), bg="#F4F6F9", fg="#34495E", padx=15, pady=10)
        frame_func.pack(fill="x", padx=20, pady=10)

        lbl_instrucao = tk.Label(frame_func, text="Digite os nomes dos funcionários (um por linha):", bg="#F4F6F9", font=("Helvetica", 9))
        lbl_instrucao.pack(anchor="w")

        self.txt_funcionarios = tk.Text(frame_func, height=6, font=("Helvetica", 10))
        self.txt_funcionarios.pack(fill="x", pady=5)
        # Nomes de exemplo
        self.txt_funcionarios.insert("1.0", "Ana Silva\nBruno Souza\nCarlos Eduardo\nDiana Lima\nEduardo Costa\nFernanda Alves")

        # Botão Gerar
        btn_gerar = tk.Button(root, text="🚀 GERAR ESCALA 5x2", font=("Helvetica", 12, "bold"), bg="#27AE60", fg="white", activebackground="#219150", activeforeground="white", command=self.gerar_escala, relief="flat", pady=8)
        btn_gerar.pack(fill="x", padx=20, pady=10)

        # Tabela de Resultados
        frame_tabela = tk.Frame(root, bg="#F4F6F9")
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=5)

        self.tree = ttk.Treeview(frame_tabela, show="headings")
        self.tree.pack(fill="both", expand=True)

        # Botão Exportar CSV / Excel
        self.btn_exportar = tk.Button(root, text="📥 Salvar em Excel / CSV", font=("Helvetica", 10, "bold"), bg="#2980B9", fg="white", state="disabled", command=self.exportar_csv, relief="flat", pady=6)
        self.btn_exportar.pack(fill="x", padx=20, pady=15)

        self.dados_escala_pronta = []

    def gerar_escala(self):
        # Limpar tabela anterior
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obter modo
        if self.modo_var.get() == "6":
            dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
        else:
            dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

        # Obter funcionários
        texto_nomes = self.txt_funcionarios.get("1.0", tk.END).strip()
        funcionarios = [n.strip() for n in texto_nomes.split("\n") if n.strip()]

        if len(funcionarios) < 2:
            messagebox.showwarning("Aviso", "Cadastre pelo menos 2 funcionários!")
            return

        # Configurar colunas da tabela
        self.tree["columns"] = ["Funcionário"] + dias
        self.tree.heading("Funcionário", text="Funcionário")
        self.tree.column("Funcionário", width=130, anchor="w")

        for d in dias:
            self.tree.heading(d, text=d)
            self.tree.column(d, width=75, anchor="center")

        # Algoritmo de Folgas 5x2
        self.dados_escala_pronta = []
        for func in funcionarios:
            folgas = random.sample(dias, 2)
            linha = [func]
            dict_linha = {"Funcionário": func}
            for d in dias:
                status = "FOLGA" if d in folgas else "TRABALHA"
                linha.append(status)
                dict_linha[d] = status
            
            self.tree.insert("", tk.END, values=linha)
            self.dados_escala_pronta.append(dict_linha)

        self.btn_exportar.config(state="normal")
        messagebox.showinfo("Sucesso", "Escala gerada com sucesso!")

    def exportar_csv(self):
        if not self.dados_escala_pronta:
            return

        caminho_arquivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivo CSV (Excel)", "*.csv")],
            title="Salvar Escala"
        )

        if caminho_arquivo:
            colunas = list(self.dados_escala_pronta[0].keys())
            with open(caminho_arquivo, mode="w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=colunas)
                writer.writeheader()
                writer.writerows(self.dados_escala_pronta)
            messagebox.showinfo("Salvo!", f"Escala salva em:\n{caminho_arquivo}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EscalaApp(root)
    root.mainloop()
