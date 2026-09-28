class PubSub:
    def __init__(self):
        self.topicos = {}

    def subscribe(self, topico, assinante):
        if topico not in self.topicos:
            self.topicos[topico] = []

        if assinante not in self.topicos[topico]:
            self.topicos[topico].append(assinante)
            print(
                f"[INSCRIÇÃO] {assinante.nome} "
                f"inscrito no tópico '{topico}'."
            )

    def unsubscribe(self, topico, assinante):
        if topico in self.topicos and assinante in self.topicos[topico]:
            self.topicos[topico].remove(assinante)

            print(
                f"[DESINSCRIÇÃO] {assinante.nome} "
                f"removido do tópico '{topico}'."
            )

    def publish(self, topico, mensagem):
        print(f"\n[PUBLICAÇÃO] Tópico: {topico}")
        print(f"Mensagem: {mensagem}")

        if topico not in self.topicos or not self.topicos[topico]:
            print("Nenhum assinante neste tópico.")
            return

        for assinante in self.topicos[topico]:
            assinante.receber_mensagem(topico, mensagem)