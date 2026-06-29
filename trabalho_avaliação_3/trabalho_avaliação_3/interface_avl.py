import tkinter as tk
from tkinter import messagebox
from avl_exclusao import ArvoreAVL, No

class AVLVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Árvore AVL")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2d2d2d")
        
        self.arvore = ArvoreAVL()
        
        self.control_frame = tk.Frame(self.root, bg="#1e1e1e", pady=10)
        self.control_frame.pack(fill=tk.X)
        
        self.lbl_value = tk.Label(self.control_frame, text="Valor:", bg="#1e1e1e", fg="white", font=("Arial", 12, "bold"))
        self.lbl_value.pack(side=tk.LEFT, padx=10)
        
        self.entry_value = tk.Entry(self.control_frame, font=("Arial", 12), width=10, bg="#2d2d2d", fg="white", insertbackground="white")
        self.entry_value.pack(side=tk.LEFT, padx=10)
        self.entry_value.bind("<Return>", lambda event: self.inserir())
        
        self.btn_insert = tk.Button(self.control_frame, text="Inserir", command=self.inserir, bg="#3b82f6", fg="white", font=("Arial", 10, "bold"), activebackground="#2563eb", activeforeground="white", bd=0, padx=15, pady=5)
        self.btn_insert.pack(side=tk.LEFT, padx=5)
        
        self.btn_remove = tk.Button(self.control_frame, text="Remover", command=self.remover, bg="#ef4444", fg="white", font=("Arial", 10, "bold"), activebackground="#dc2626", activeforeground="white", bd=0, padx=15, pady=5)
        self.btn_remove.pack(side=tk.LEFT, padx=5)
        
        self.btn_clear = tk.Button(self.control_frame, text="Limpar", command=self.limpar, bg="#6b7280", fg="white", font=("Arial", 10, "bold"), activebackground="#4b5563", activeforeground="white", bd=0, padx=15, pady=5)
        self.btn_clear.pack(side=tk.LEFT, padx=5)
        
        self.btn_populate = tk.Button(self.control_frame, text="Popular", command=self.popular, bg="#10b981", fg="white", font=("Arial", 10, "bold"), activebackground="#059669", activeforeground="white", bd=0, padx=15, pady=5)
        self.btn_populate.pack(side=tk.LEFT, padx=5)
        
        self.lbl_status = tk.Label(self.root, text="Bem-vindo! Insira valores para começar.", bg="#2d2d2d", fg="#a3a3a3", font=("Arial", 11, "italic"))
        self.lbl_status.pack(pady=10)
        
        self.canvas_frame = tk.Frame(self.root, bg="#2d2d2d")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.root.bind("<Configure>", lambda event: self.redesenhar())
        
    def inserir(self):
        val_str = self.entry_value.get().strip()
        if not val_str:
            return
        try:
            val = int(val_str)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número inteiro válido.")
            return
        
        if self.buscar_no(self.arvore.raiz, val):
            self.lbl_status.configure(text=f"Valor {val} já existe na árvore. Inserção ignorada.", fg="#f59e0b")
        else:
            self.arvore.adicionar_no(val)
            self.lbl_status.configure(text=f"Nó {val} inserido com sucesso.", fg="#10b981")
            
        self.entry_value.delete(0, tk.END)
        self.redesenhar()
        
    def remover(self):
        val_str = self.entry_value.get().strip()
        if not val_str:
            return
        try:
            val = int(val_str)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número inteiro válido.")
            return
            
        if not self.buscar_no(self.arvore.raiz, val):
            self.lbl_status.configure(text=f"Valor {val} não encontrado na árvore para remoção.", fg="#ef4444")
        else:
            self.arvore.remover_no(val)
            self.lbl_status.configure(text=f"Nó {val} removido com sucesso.", fg="#10b981")
            
        self.entry_value.delete(0, tk.END)
        self.redesenhar()
        
    def limpar(self):
        self.arvore = ArvoreAVL()
        self.lbl_status.configure(text="Árvore limpa.", fg="#a3a3a3")
        self.redesenhar()
        
    def popular(self):
        valores = [50, 30, 70, 20, 40, 60, 80, 15, 25, 35, 45]
        for v in valores:
            if not self.buscar_no(self.arvore.raiz, v):
                self.arvore.adicionar_no(v)
        self.lbl_status.configure(text="Árvore populada com valores de teste.", fg="#10b981")
        self.redesenhar()
        
    def buscar_no(self, no_atual, valor):
        if not no_atual:
            return False
        if valor == no_atual.valor:
            return True
        elif valor < no_atual.valor:
            return self.buscar_no(no_atual.esquerda, valor)
        else:
            return self.buscar_no(no_atual.direita, valor)
            
    def redesenhar(self):
        self.canvas.delete("all")
        if self.arvore.vazia():
            self.canvas.create_text(
                self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2,
                text="Árvore AVL Vazia",
                fill="#525252",
                font=("Arial", 16, "bold")
            )
            return
            
        width = self.canvas.winfo_width()
        if width < 100:
            width = 1000
        
        self.desenhar_no_rec(self.arvore.raiz, width / 2, 50, width / 4)
        
    def desenhar_no_rec(self, no, x, y, x_offset):
        if not no:
            return
            
        r = 20
        
        if no.esquerda:
            self.canvas.create_line(x, y, x - x_offset, y + 80, fill="#4b5563", width=2)
            self.desenhar_no_rec(no.esquerda, x - x_offset, y + 80, x_offset / 2)
            
        if no.direita:
            self.canvas.create_line(x, y, x + x_offset, y + 80, fill="#4b5563", width=2)
            self.desenhar_no_rec(no.direita, x + x_offset, y + 80, x_offset / 2)
            
        fb = self.obter_fb(no)
        
        fill_color = "#3b82f6"
        outline_color = "#60a5fa"
        if abs(fb) > 1:
            fill_color = "#ef4444"
            outline_color = "#fca5a5"
        elif abs(fb) == 1:
            fill_color = "#f59e0b"
            outline_color = "#fcd34d"
            
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill_color, outline=outline_color, width=2)
        self.canvas.create_text(x, y, text=str(no.valor), fill="white", font=("Arial", 11, "bold"))
        
        info_str = f"h:{no.altura}\nfb:{fb}"
        self.canvas.create_text(x + 25, y, text=info_str, fill="#a3a3a3", font=("Arial", 8), anchor="w")
        
    def obter_fb(self, no):
        if not no:
            return 0
        return self._altura(no.direita) - self._altura(no.esquerda)
        
    def _altura(self, no):
        if not no:
            return 0
        return no.altura

if __name__ == "__main__":
    root = tk.Tk()
    app = AVLVisualizer(root)
    root.mainloop()
