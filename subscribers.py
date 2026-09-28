class Subscriber:
    def __init__(self, nome):
        self.nome = nome

    def receber_mensagem(self, topico, mensagem):
        print(
            f"[{self.nome}] recebeu do tópico "
            f"'{topico}': {mensagem}"
        )