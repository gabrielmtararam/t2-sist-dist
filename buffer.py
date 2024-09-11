from collections import deque

class Buffer:
    def __init__(self, tamanho_max):
        self.buffer = deque(maxlen=tamanho_max)

    def adicionar(self, item):
        self.buffer.append(item)
        self.verificar_nivel()

    def consumir(self):
        if self.buffer:
            return self.buffer.popleft()
        return None

    def nivel_atual(self):
        return len(self.buffer)

    def verificar_nivel(self):
        if self.nivel_atual() == 0:
            print("Buffer está vazio, possível necessidade de reabastecimento.")

