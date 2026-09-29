from pubsub import PubSub
from publishers import Publisher
from subscribers import Subscriber


def separador(titulo):
    print("\n" + "=" * 60)
    print(f" {titulo}")
    print("=" * 60)


def main():
    separador("SMART HOME - SISTEMA PUB/SUB")

    # Criação do Broker
    broker = PubSub()

    # Publishers
    sensor_presenca = Publisher(
        "Sensor de Presença da Sala",
        broker
    )

    detector_fumaca = Publisher(
        "Detector de Fumaça da Cozinha",
        broker
    )

    fechadura = Publisher(
        "Fechadura Eletrônica",
        broker
    )

    sensor_temperatura = Publisher(
        "Sensor de Temperatura do Quarto",
        broker
    )

    # Subscribers
    sistema_iluminacao = Subscriber(
        "Sistema de Iluminação"
    )

    central_alarme = Subscriber(
        "Central de Alarme"
    )

    aplicativo_morador = Subscriber(
        "Aplicativo do Morador"
    )

    sistema_climatizacao = Subscriber(
        "Sistema de Climatização"
    )

    separador("REALIZANDO INSCRIÇÕES")

    broker.subscribe(
        "Sala_Presenca",
        sistema_iluminacao
    )

    broker.subscribe(
        "Cozinha_Fumaca",
        central_alarme
    )

    broker.subscribe(
        "Cozinha_Fumaca",
        aplicativo_morador
    )

    broker.subscribe(
        "Geral_Seguranca",
        central_alarme
    )

    broker.subscribe(
        "Geral_Seguranca",
        aplicativo_morador
    )

    broker.subscribe(
        "Quarto_Temperatura",
        sistema_climatizacao
    )

    # ---------------------------------------------------------
    # CENÁRIO 1
    # ---------------------------------------------------------

    separador(
        "CENÁRIO 1 - FUNCIONAMENTO NORMAL"
    )

    sensor_presenca.publicar(
        "Sala_Presenca",
        "Movimento detectado na sala."
    )

    detector_fumaca.publicar(
        "Cozinha_Fumaca",
        "Fumaça detectada na cozinha!"
    )

    fechadura.publicar(
        "Geral_Seguranca",
        "Porta principal foi aberta."
    )

    sensor_temperatura.publicar(
        "Quarto_Temperatura",
        "Temperatura atual do quarto: 28°C."
    )

    # ---------------------------------------------------------
    # CENÁRIO 2
    # ---------------------------------------------------------

    separador(
        "CENÁRIO 2 - UNSUBSCRIBE PARCIAL"
    )

    print(
        "\nO Aplicativo do Morador deixará de receber "
        "alertas de fumaça, mas a Central de Alarme "
        "continuará inscrita."
    )

    broker.unsubscribe(
        "Cozinha_Fumaca",
        aplicativo_morador
    )

    detector_fumaca.publicar(
        "Cozinha_Fumaca",
        "Novo alerta de fumaça detectado!"
    )

    # ---------------------------------------------------------
    # CENÁRIO 3
    # ---------------------------------------------------------

    separador(
        "CENÁRIO 3 - TÓPICO SEM ASSINANTES"
    )

    print(
        "\nO Sistema de Iluminação será removido "
        "de Sala_Presenca. Depois disso, o tópico "
        "ficará sem assinantes."
    )

    broker.unsubscribe(
        "Sala_Presenca",
        sistema_iluminacao
    )

    sensor_presenca.publicar(
        "Sala_Presenca",
        "Novo movimento detectado na sala."
    )

    separador("FIM DA SIMULAÇÃO")


if __name__ == "__main__":
    main()