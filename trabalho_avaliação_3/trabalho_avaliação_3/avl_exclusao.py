class No:
    def __init__(self, valor):
        self.esquerda = None
        self.valor = valor
        self.direita = None
        self.altura = 1

class ArvoreAVL:
    def __init__(self, raiz=None):
        self.raiz = raiz

    def vazia(self):
        if self.raiz is None:
            return True
        return False

    def adicionar_no(self, valor):
        if self.vazia():
            novo_No = No(valor)
            self.raiz = novo_No
        else:
            self.raiz = self._adicionar_no_folha(self.raiz, valor)

    def _adicionar_no_folha(self, no_atual, valor):
        if not no_atual:
            novo_No = No(valor)
            return novo_No
        elif valor == no_atual.valor:
            print(f"Valor {valor} já existe. Ignorando a Inserção.")
            return no_atual
        elif valor < no_atual.valor:
            no_atual.esquerda = self._adicionar_no_folha(no_atual.esquerda, valor)
        else:
            no_atual.direita = self._adicionar_no_folha(no_atual.direita, valor)

        no_atual.altura = 1 + max(
            self._altura(no_atual.esquerda),
            self._altura(no_atual.direita)
        )
        balanceamento = self._balanceamento(no_atual)

        if balanceamento < -1:
            if valor < no_atual.esquerda.valor:
                return self._rotacao_direita(no_atual)
            else:
                no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda)
                return self._rotacao_direita(no_atual)

        if balanceamento > 1:
            if valor > no_atual.direita.valor:
                return self._rotacao_esquerda(no_atual)
            else:
                no_atual.direita = self._rotacao_direita(no_atual.direita)
                return self._rotacao_esquerda(no_atual)

        return no_atual

    def remover_no(self, valor):
        if self.vazia():
            print("Árvore vazia, nada a remover.")
            return
        self.raiz = self._remover_no(self.raiz, valor)

    def _remover_no(self, no_atual, valor):
        if not no_atual:
            print(f"Valor {valor} não encontrado na árvore.")
            return no_atual

        if valor < no_atual.valor:
            no_atual.esquerda = self._remover_no(no_atual.esquerda, valor)
        elif valor > no_atual.valor:
            no_atual.direita = self._remover_no(no_atual.direita, valor)
        else:
            if no_atual.esquerda is None:
                temp = no_atual.direita
                no_atual = None
                return temp
            elif no_atual.direita is None:
                temp = no_atual.esquerda
                no_atual = None
                return temp

            temp = self._menor_valor_no(no_atual.direita)
            no_atual.valor = temp.valor
            no_atual.direita = self._remover_no(no_atual.direita, temp.valor)

        if no_atual is None:
            return no_atual

        no_atual.altura = 1 + max(
            self._altura(no_atual.esquerda),
            self._altura(no_atual.direita)
        )

        balanceamento = self._balanceamento(no_atual)

        if balanceamento < -1 and self._balanceamento(no_atual.esquerda) <= 0:
            return self._rotacao_direita(no_atual)

        if balanceamento < -1 and self._balanceamento(no_atual.esquerda) > 0:
            no_atual.esquerda = self._rotacao_esquerda(no_atual.esquerda)
            return self._rotacao_direita(no_atual)

        if balanceamento > 1 and self._balanceamento(no_atual.direita) >= 0:
            return self._rotacao_esquerda(no_atual)

        if balanceamento > 1 and self._balanceamento(no_atual.direita) < 0:
            no_atual.direita = self._rotacao_direita(no_atual.direita)
            return self._rotacao_esquerda(no_atual)

        return no_atual

    def _menor_valor_no(self, no):
        atual = no
        while   atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def _altura(self, no):
        if not no:
            return 0
        return no.altura

    def _balanceamento(self, no):
        if not no:
            return 0
        fb = self._altura(no.direita) - self._altura(no.esquerda)
        return fb

    def _rotacao_esquerda(self, pai):
        if not pai or not pai.direita:
            print(f"Rotação à esquerda não realizada: Filho direito inexistente.")
            return pai
        filhoD = pai.direita
        neto =   filhoD.esquerda

        filhoD.esquerda = pai
        pai.direita = neto

        pai.altura = 1 + max(
            self._altura(pai.esquerda),
            self._altura(pai.direita))
        filhoD.altura = 1 + max(
            self._altura(filhoD.esquerda),
            self._altura(filhoD.direita))

        return filhoD

    def _rotacao_direita(self, pai):
        if not pai or not pai.esquerda:
            print("Rotação à direita não realizada: filho esquerdo inexistente.")
            return pai

        filhoE = pai.esquerda
        neto = filhoE.direita

        filhoE.direita = pai
        pai.esquerda = neto

        pai.altura = 1 + max(
            self._altura(pai.esquerda),
            self._altura(pai.direita))
        filhoE.altura = 1 + max(
            self._altura(filhoE.esquerda),
            self._altura(filhoE.direita))
        return filhoE

    def imprimir(self):
        if self.vazia():
            print("========== Árvore vazia ==========")
            return
        print("\n=============== Árvore ================")
        self._imprimir(self.raiz)
        print("=========================================\n")

    def _imprimir(self, no_atual):
        if no_atual is not None:
            self._imprimir(no_atual.esquerda)
            print(f"Nó: {str(no_atual)[-5:]} -- Esq.{str(no_atual.esquerda)[-5:]} Valor: {str(no_atual.valor)}  Dir.{str(no_atual.direita)[-5:]} Alt.{str(no_atual.altura)}")
            self._imprimir(no_atual.direita)

def popular_arvore(arvore):
    lista_entradas = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
    print("--- Inserindo elementos ---")
    for e in lista_entradas:
        arvore.adicionar_no(e)
    arvore.imprimir()

    print("--- Removendo 70 (nó folha) ---")
    arvore.remover_no(70)
    arvore.imprimir()

    print("--- Removendo 90 (nó com um filho) ---")
    arvore.remover_no(90)
    arvore.imprimir()

    print("--- Removendo 40 (nó com dois filhos) ---")
    arvore.remover_no(40)
    arvore.imprimir()

    print("--- Removendo 30 (nó que causa desbalanceamento e rotação) ---")
    arvore.remover_no(30)
    arvore.imprimir()

if __name__ == "__main__":
    arvore = ArvoreAVL()
    popular_arvore(arvore)
