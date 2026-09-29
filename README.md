# 🏠 Smart Home Pub/Sub

Projeto desenvolvido para a disciplina **Sistemas Computacionais Distribuídos e Computação em Nuvem**, com o objetivo de demonstrar, na prática, o funcionamento do padrão arquitetural **Publish/Subscribe (Pub/Sub)** aplicado a um cenário de **Casa Inteligente e Automação Residencial (Smart Home)**.

O sistema simula sensores e serviços de uma residência inteligente comunicando-se através de um **Broker**, sem que Publishers e Subscribers precisem conhecer diretamente uns aos outros.

---

## 👨‍🏫 Disciplina

**Disciplina:** Sistemas Computacionais Distribuídos e Computação em Nuvem  
**Professora:** Ana Paula

### 👥 Integrantes

- Cauã Línitter Arantes Lima
- Gabriel de Godoy Santos
- Guilherme Rodrigues de Castro
- Daniel Moreira

---

## 🎯 Objetivo

O objetivo do projeto é demonstrar os principais conceitos do padrão **Publish/Subscribe**, especialmente:

- comunicação baseada em eventos;
- desacoplamento entre componentes;
- Publishers;
- Subscribers;
- Broker;
- tópicos;
- inscrição (`subscribe`);
- desinscrição (`unsubscribe`);
- publicação (`publish`);
- múltiplos Subscribers em um mesmo tópico.

O cenário escolhido foi:

> **Tema 9 — Casa Inteligente e Automação Residencial (Smart Home)**

---

## 📌 Cenário do projeto

Uma casa inteligente pode possuir diversos sensores e serviços que precisam reagir a eventos como:

- presença detectada em um cômodo;
- fumaça detectada na cozinha;
- abertura de uma porta;
- alteração de temperatura.

Uma abordagem baseada em comunicação direta criaria dependência entre os dispositivos.

Por exemplo, um detector de fumaça precisaria conhecer individualmente:

- a Central de Alarme;
- o Aplicativo do Morador;
- qualquer outro serviço interessado no alerta.

Com o padrão **Publish/Subscribe**, o sensor apenas publica o evento em um tópico.

O **Broker** fica responsável por descobrir quais Subscribers estão interessados naquele tópico e encaminhar a mensagem para eles.

---

## 🔄 Arquitetura Pub/Sub

O fluxo básico da aplicação é:

```text
Publisher
    │
    │ publish()
    ▼
┌───────────────┐
│     Broker    │
│    Pub/Sub    │
└───────┬───────┘
        │
        │ Tópico
        ▼
   Subscribers
```

### Exemplo: detector de fumaça

```text
Detector de Fumaça
        │
        │ publica
        ▼
  Cozinha_Fumaca
        │
        ▼
   ┌──────────┐
   │  Broker  │
   └────┬─────┘
        │
     ┌──┴───────────┐
     ▼              ▼
Central de      Aplicativo
 Alarme         do Morador
```

O **Publisher não precisa conhecer os Subscribers**.

Ele conhece apenas o Broker e o tópico no qual deseja publicar.

Isso reduz o acoplamento entre os componentes.

---

## 📡 Publishers

Os **Publishers** são os componentes responsáveis por gerar eventos.

Neste projeto são utilizados:

| Publisher | Evento |
|---|---|
| Sensor de Presença da Sala | Detecta movimento |
| Detector de Fumaça da Cozinha | Detecta fumaça |
| Fechadura Eletrônica | Informa abertura da porta |
| Sensor de Temperatura do Quarto | Informa a temperatura |

---

## 📥 Subscribers

Os **Subscribers** são os sistemas interessados em receber determinados tipos de evento.

Neste projeto são utilizados:

| Subscriber | Responsabilidade |
|---|---|
| Sistema de Iluminação | Reagir à presença detectada |
| Central de Alarme | Receber alertas de segurança |
| Aplicativo do Morador | Notificar o morador |
| Sistema de Climatização | Reagir às informações de temperatura |

---

## 🗂️ Tópicos

O Broker organiza as mensagens através de tópicos.

| Tópico | Evento |
|---|---|
| `Sala_Presenca` | Movimento detectado na sala |
| `Cozinha_Fumaca` | Fumaça detectada na cozinha |
| `Geral_Seguranca` | Eventos relacionados à segurança |
| `Quarto_Temperatura` | Leitura de temperatura do quarto |

Um Subscriber recebe somente mensagens dos tópicos nos quais está inscrito.

---

## ⚙️ Broker Pub/Sub

A classe `PubSub`, localizada em `pubsub.py`, representa o **Broker** da aplicação.

Ela mantém os tópicos e os Subscribers inscritos em cada um deles.

As três operações principais são:

### `subscribe(topico, assinante)`

Inscreve um Subscriber em um tópico.

```python
broker.subscribe(
    "Cozinha_Fumaca",
    aplicativo_morador
)
```

Após a inscrição, o Subscriber passa a receber as mensagens publicadas naquele tópico.

---

### `unsubscribe(topico, assinante)`

Remove um Subscriber de um tópico.

```python
broker.unsubscribe(
    "Cozinha_Fumaca",
    aplicativo_morador
)
```

Após a remoção, novas mensagens daquele tópico deixam de ser entregues ao Subscriber removido.

---

### `publish(topico, mensagem)`

Publica uma mensagem em determinado tópico.

```python
broker.publish(
    "Cozinha_Fumaca",
    "Fumaça detectada na cozinha!"
)
```

O Broker procura os Subscribers atualmente inscritos no tópico e encaminha a mensagem para cada um deles.

---

## 🧪 Simulação

O arquivo `main.py` executa uma demonstração completa do sistema.

A simulação foi dividida em **três cenários** para facilitar a visualização do comportamento do padrão Pub/Sub.

### Cenário 1 — Funcionamento normal

Primeiro são realizadas todas as inscrições.

Depois são simulados eventos como:

- movimento detectado na sala;
- fumaça detectada na cozinha;
- abertura da porta principal;
- leitura da temperatura do quarto.

Exemplo:

```text
Detector de Fumaça
       │
       ▼
Cozinha_Fumaca
       │
       ▼
     Broker
       │
   ┌───┴─────┐
   ▼         ▼
Central   Aplicativo
Alarme    do Morador
```

Como os dois Subscribers estão inscritos em `Cozinha_Fumaca`, ambos recebem o alerta.

---

### Cenário 2 — Unsubscribe parcial

Neste cenário, o **Aplicativo do Morador** deixa de receber alertas do tópico:

```text
Cozinha_Fumaca
```

A operação executada é equivalente a:

```python
broker.unsubscribe(
    "Cozinha_Fumaca",
    aplicativo_morador
)
```

Depois disso, um novo alerta é publicado.

O resultado esperado é:

```text
Detector de Fumaça
       │
       ▼
Cozinha_Fumaca
       │
       ▼
     Broker
       │
       ▼
Central de Alarme
```

A **Central de Alarme continua recebendo a mensagem**, pois continua inscrita.

O **Aplicativo do Morador não recebe mais o alerta**, demonstrando o funcionamento do `unsubscribe()`.

---

### Cenário 3 — Tópico sem assinantes

Por fim, o **Sistema de Iluminação** é removido do tópico:

```text
Sala_Presenca
```

Como ele era o único Subscriber daquele tópico, uma nova publicação encontra o tópico sem assinantes.

O Broker informa:

```text
Nenhum assinante neste tópico.
```

Esse cenário demonstra que o sistema também consegue tratar publicações em tópicos que não possuem Subscribers ativos.

---

## ✅ Testes automatizados

O projeto possui testes automatizados utilizando o módulo `unittest`, que faz parte da biblioteca padrão do Python.

Portanto, não é necessário instalar nenhuma biblioteca externa para executar os testes.

Os testes estão localizados em:

```text
tests/test_pubsub.py
```

Atualmente são verificados cinco comportamentos principais do Broker:

1. inscrição de um Subscriber em um tópico;
2. prevenção de inscrição duplicada;
3. publicação para todos os Subscribers inscritos;
4. interrupção do recebimento após `unsubscribe`;
5. publicação em um tópico sem Subscribers.

### Executar os testes

Na raiz do projeto:

```bash
python3 -m unittest discover -s tests -v
```

Resultado esperado:

```text
test_publish_notifica_todos_os_assinantes ... ok
test_publish_sem_assinantes_nao_falha ... ok
test_subscribe_adiciona_assinante_ao_topico ... ok
test_subscribe_nao_duplica_assinante ... ok
test_unsubscribe_impede_novas_mensagens ... ok

----------------------------------------------------------------------
Ran 5 tests

OK
```

Os testes ajudam a verificar automaticamente se as principais operações do Broker continuam funcionando corretamente após alterações no código.

---

## 📁 Estrutura do projeto

```text
smart-home-pubsub/
│
├── tests/
│   └── test_pubsub.py
│
├── main.py
├── publishers.py
├── pubsub.py
├── subscribers.py
├── README.md
└── .gitignore
```

### `pubsub.py`

Contém a classe `PubSub`, que representa o Broker e implementa:

```text
subscribe()
unsubscribe()
publish()
```

### `publishers.py`

Contém a classe `Publisher`, utilizada pelos sensores e dispositivos que geram eventos.

### `subscribers.py`

Contém a classe `Subscriber`, utilizada pelos serviços interessados em receber eventos.

### `main.py`

Responsável por:

- criar o Broker;
- criar Publishers;
- criar Subscribers;
- realizar inscrições;
- publicar eventos;
- executar os três cenários da demonstração.

### `tests/test_pubsub.py`

Contém os testes automatizados do Broker utilizando `unittest`.

---

## 💻 Tecnologias utilizadas

- Python 3
- Git
- GitHub
- `unittest`
- WSL2
- Visual Studio Code

O projeto utiliza apenas recursos da **biblioteca padrão do Python** e não necessita de dependências externas.

---

## 🚀 Como executar

### Pré-requisitos

É necessário ter:

- Python 3;
- Git.

Verifique a instalação:

```bash
python3 --version
git --version
```

---

### 1. Clone o repositório

```bash
git clone https://github.com/Linitter/smart-home-pubsub.git
```

### 2. Entre na pasta

```bash
cd smart-home-pubsub
```

### 3. Execute a aplicação

```bash
python3 main.py
```

---

## 🧪 Como executar os testes

Na raiz do projeto:

```bash
python3 -m unittest discover -s tests -v
```

Se todos os testes forem aprovados, a execução terminará com:

```text
OK
```

---

## 📋 Exemplo de funcionamento

Durante o início da aplicação são realizadas as inscrições:

```text
[INSCRIÇÃO] Sistema de Iluminação inscrito no tópico 'Sala_Presenca'.

[INSCRIÇÃO] Central de Alarme inscrito no tópico 'Cozinha_Fumaca'.

[INSCRIÇÃO] Aplicativo do Morador inscrito no tópico 'Cozinha_Fumaca'.
```

Quando o detector de fumaça publica um evento:

```text
[Detector de Fumaça da Cozinha] Novo evento detectado.

[PUBLICAÇÃO] Tópico: Cozinha_Fumaca
Mensagem: Fumaça detectada na cozinha!

[Central de Alarme] recebeu do tópico 'Cozinha_Fumaca':
Fumaça detectada na cozinha!

[Aplicativo do Morador] recebeu do tópico 'Cozinha_Fumaca':
Fumaça detectada na cozinha!
```

Posteriormente, o Aplicativo do Morador é removido:

```text
[DESINSCRIÇÃO] Aplicativo do Morador removido do tópico 'Cozinha_Fumaca'.
```

Quando uma nova mensagem é publicada, apenas a Central de Alarme continua recebendo.

---

## 💡 Desacoplamento

Uma das principais vantagens demonstradas pelo projeto é o **desacoplamento**.

Sem Pub/Sub, um sensor poderia precisar chamar diretamente vários sistemas:

```text
Sensor ──► Central de Alarme
       ├─► Aplicativo
       └─► Outro Serviço
```

No modelo Pub/Sub:

```text
Sensor
  │
  ▼
Broker
  │
  ├─► Subscriber A
  ├─► Subscriber B
  └─► Subscriber C
```

O Publisher não precisa saber:

- quantos Subscribers existem;
- quem são os Subscribers;
- como cada Subscriber utilizará a informação.

Ele apenas publica a mensagem no tópico adequado.

---

## ℹ️ Escopo da implementação

Este projeto é uma **implementação didática do padrão Publish/Subscribe em memória**, desenvolvida para demonstrar os conceitos fundamentais da arquitetura.

O Broker é implementado diretamente pela classe `PubSub`, sem utilizar ferramentas externas como:

- Apache Kafka;
- RabbitMQ;
- Redis Pub/Sub.

Nesta implementação, Publisher, Broker e Subscribers são executados no mesmo processo Python.

Em uma arquitetura distribuída de produção, um sistema de mensageria externo poderia assumir o papel do Broker e permitir comunicação entre aplicações executadas em diferentes processos, máquinas ou serviços.

O foco deste projeto é demonstrar corretamente a lógica fundamental do padrão:

```text
subscribe → publish → entrega aos inscritos → unsubscribe
```

---

## 🎓 Conceitos demonstrados

Ao executar o projeto é possível visualizar, na prática:

- padrão Publish/Subscribe;
- arquitetura orientada a eventos;
- Publisher;
- Subscriber;
- Broker;
- tópicos;
- inscrição;
- desinscrição;
- publicação;
- múltiplos Subscribers;
- tópicos sem Subscribers;
- desacoplamento entre produtor e consumidor;
- testes automatizados da lógica do Broker.

---

## 📚 Resumo do fluxo

```text
1. Subscriber realiza subscribe()
                │
                ▼
2. Broker registra a inscrição
                │
                ▼
3. Publisher gera um evento
                │
                ▼
4. Publisher chama publish()
                │
                ▼
5. Broker identifica os inscritos
                │
                ▼
6. Subscribers recebem a mensagem
                │
                ▼
7. Subscriber pode realizar unsubscribe()
                │
                ▼
8. Novas mensagens não são mais entregues a ele
```

---

## 🏠 Resultado

A aplicação demonstra como dispositivos de uma **Smart Home** podem trocar informações utilizando o padrão Pub/Sub sem criar dependências diretas entre sensores e os serviços que consomem seus eventos.

A implementação permite visualizar de forma simples os papéis de **Publisher, Broker, tópico e Subscriber**, além de demonstrar na prática as operações `subscribe`, `publish` e `unsubscribe`.