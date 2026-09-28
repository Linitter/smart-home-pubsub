from pubsub import PubSub
from publishers import Publisher
from subscribers import Subscriber


def main():
    print("=" * 60)
    print(" SMART HOME - SISTEMA PUB/SUB")
    print("=" * 60)

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

    print("\n--- REALIZANDO INSCRIÇÕES ---")

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

    print("\n" + "=" * 60)
    print(" SIMULAÇÃO DOS EVENTOS")
    print("=" * 60)

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

    print("\n" + "=" * 60)
    print(" TESTE DE UNSUBSCRIBE")
    print("=" * 60)

    broker.unsubscribe(
        "Cozinha_Fumaca",
        aplicativo_morador
    )

    detector_fumaca.publicar(
        "Cozinha_Fumaca",
        "Novo alerta de fumaça detectado!"
    )

    print("\n" + "=" * 60)
    print(" FIM DA SIMULAÇÃO")
    print("=" * 60)


if __name__ == "__main__":
    main()