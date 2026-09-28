class Publisher:
    def __init__(self, nome, broker):
        self.nome = nome
        self.broker = broker

    def publicar(self, topico, mensagem):
        print(f"\n[{self.nome}] Novo evento detectado.")

        self.broker.publish(topico, mensagem)