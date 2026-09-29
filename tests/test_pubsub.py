import unittest
from contextlib import redirect_stdout
from io import StringIO

from pubsub import PubSub


class AssinanteFake:
    def __init__(self, nome):
        self.nome = nome
        self.mensagens = []

    def receber_mensagem(self, topico, mensagem):
        self.mensagens.append((topico, mensagem))


class TestPubSub(unittest.TestCase):
    def setUp(self):
        self.broker = PubSub()
        self.assinante = AssinanteFake("Assinante de Teste")

    def test_subscribe_adiciona_assinante_ao_topico(self):
        self.broker.subscribe("Teste", self.assinante)

        self.assertIn("Teste", self.broker.topicos)
        self.assertIn(
            self.assinante,
            self.broker.topicos["Teste"]
        )

    def test_subscribe_nao_duplica_assinante(self):
        self.broker.subscribe("Teste", self.assinante)
        self.broker.subscribe("Teste", self.assinante)

        self.assertEqual(
            1,
            len(self.broker.topicos["Teste"])
        )

    def test_publish_notifica_todos_os_assinantes(self):
        outro_assinante = AssinanteFake("Outro Assinante")

        self.broker.subscribe(
            "Alerta",
            self.assinante
        )

        self.broker.subscribe(
            "Alerta",
            outro_assinante
        )

        self.broker.publish(
            "Alerta",
            "Fumaça detectada!"
        )

        esperado = [
            ("Alerta", "Fumaça detectada!")
        ]

        self.assertEqual(
            esperado,
            self.assinante.mensagens
        )

        self.assertEqual(
            esperado,
            outro_assinante.mensagens
        )

    def test_unsubscribe_impede_novas_mensagens(self):
        self.broker.subscribe(
            "Alerta",
            self.assinante
        )

        self.broker.unsubscribe(
            "Alerta",
            self.assinante
        )

        self.broker.publish(
            "Alerta",
            "Novo alerta"
        )

        self.assertEqual(
            [],
            self.assinante.mensagens
        )

    def test_publish_sem_assinantes_nao_falha(self):
        saida = StringIO()

        with redirect_stdout(saida):
            self.broker.publish(
                "Topico_Vazio",
                "Mensagem de teste"
            )

        self.assertIn(
            "Nenhum assinante neste tópico.",
            saida.getvalue()
        )


if __name__ == "__main__":
    unittest.main()