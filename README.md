# 🏠 Smart Home Pub/Sub

Projeto desenvolvido para a disciplina **Sistemas Computacionais Distribuídos e Computação em Nuvem**, com o objetivo de demonstrar na prática o funcionamento do padrão arquitetural **Publish/Subscribe (Pub/Sub)** em um cenário de **Casa Inteligente e Automação Residencial (Smart Home)**.

## 👨‍🏫 Disciplina

**Disciplina:** Sistemas Computacionais Distribuídos e Computação em Nuvem  
**Professor:** Ana Paula

## 👥 Integrantes

- Cauã Línitter Arantes Lima
- Gabriel de Godoy Santos
- Guilherme Rodrigues de Castro
- Daniel Moreira

---

## 📌 Sobre o projeto

O projeto simula uma **casa inteligente** composta por sensores, dispositivos e serviços que precisam trocar informações em tempo real.

Para evitar que os dispositivos fiquem diretamente dependentes uns dos outros, foi utilizado o padrão **Publish/Subscribe**.

Nesse modelo:

- os **Publishers** detectam eventos e publicam mensagens;
- o **Broker** gerencia os tópicos e seus assinantes;
- os **Subscribers** recebem apenas as mensagens dos tópicos nos quais estão inscritos.

Dessa forma, um sensor não precisa conhecer diretamente todos os sistemas que utilizarão suas informações.

---

## 🔄 Arquitetura Pub/Sub

O funcionamento básico do sistema pode ser representado da seguinte forma:

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

Por exemplo, quando o detector de fumaça identifica fumaça na cozinha:

```text
Detector de Fumaça
        │
        ▼
  Cozinha_Fumaca
        │
        ▼
       Broker
       /    \
      /      \
     ▼        ▼
Central de   Aplicativo
 Alarme      do Morador
```

O detector apenas publica o evento no tópico. O Broker é responsável por localizar os assinantes e distribuir a mensagem.

---

## 📡 Publishers

Os Publishers representam os dispositivos responsáveis por gerar eventos dentro da casa.

Neste projeto foram utilizados:

- Sensor de Presença da Sala
- Detector de Fumaça da Cozinha
- Fechadura Eletrônica
- Sensor de Temperatura do Quarto

---

## 📥 Subscribers

Os Subscribers representam os sistemas interessados nos eventos publicados.

Foram utilizados:

- Sistema de Iluminação
- Central de Alarme
- Aplicativo do Morador
- Sistema de Climatização

---

## 🗂️ Tópicos

O sistema utiliza os seguintes tópicos:

| Tópico | Evento |
|---|---|
| `Sala_Presenca` | Detecção de movimento na sala |
| `Cozinha_Fumaca` | Detecção de fumaça na cozinha |
| `Geral_Seguranca` | Eventos relacionados à segurança da residência |
| `Quarto_Temperatura` | Alterações ou leituras de temperatura do quarto |

---

## ⚙️ Operações do Broker

A classe `PubSub` é responsável pelo gerenciamento da comunicação entre Publishers e Subscribers.

Ela possui três operações principais:

### `subscribe(topico, assinante)`

Inscreve um Subscriber em determinado tópico.

```python
broker.subscribe("Cozinha_Fumaca", aplicativo_morador)
```

---

### `unsubscribe(topico, assinante)`

Remove um Subscriber de determinado tópico.

```python
broker.unsubscribe("Cozinha_Fumaca", aplicativo_morador)
```

Depois da remoção, o Subscriber deixa de receber novas mensagens publicadas naquele tópico.

---

### `publish(topico, mensagem)`

Publica uma mensagem em um tópico.

```python
broker.publish(
    "Cozinha_Fumaca",
    "Fumaça detectada na cozinha!"
)
```

Todos os Subscribers que estiverem inscritos naquele tópico recebem a mensagem.

---

## 🧪 Simulação

O arquivo `main.py` executa uma simulação completa do sistema.

Primeiro os dispositivos são inscritos nos tópicos correspondentes.

Em seguida são simulados eventos como:

- movimento detectado na sala;
- fumaça detectada na cozinha;
- abertura da porta principal;
- leitura da temperatura do quarto.

Também é realizado um teste do método `unsubscribe()`.

Durante esse teste, o **Aplicativo do Morador** é removido do tópico:

```text
Cozinha_Fumaca
```

Depois disso, um novo alerta de fumaça é publicado.

A **Central de Alarme continua recebendo a mensagem**, porém o **Aplicativo do Morador deixa de recebê-la**, demonstrando o funcionamento da desinscrição.

---

## 📁 Estrutura do projeto

```text
smart-home-pubsub/
│
├── main.py
├── publishers.py
├── pubsub.py
├── subscribers.py
├── README.md
└── .gitignore
```

### `pubsub.py`

Contém a classe `PubSub`, responsável pelo Broker e pelas operações:

```text
subscribe
unsubscribe
publish
```

### `publishers.py`

Contém a classe responsável pelos dispositivos que publicam eventos.

### `subscribers.py`

Contém a classe utilizada pelos sistemas que recebem as mensagens.

### `main.py`

Responsável por criar os objetos, realizar as inscrições e executar a simulação do sistema.

---

## 💻 Tecnologias utilizadas

- Python 3
- Git
- GitHub
- WSL2
- Visual Studio Code

O projeto não necessita de bibliotecas externas.

---

## ▶️ Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/Linitter/smart-home-pubsub.git
```

### 2. Entre na pasta do projeto

```bash
cd smart-home-pubsub
```

### 3. Verifique se o Python está instalado

```bash
python3 --version
```

### 4. Execute o sistema

```bash
python3 main.py
```

---

## 📋 Exemplo de funcionamento

Durante a execução será possível visualizar as inscrições:

```text
[INSCRIÇÃO] Sistema de Iluminação inscrito no tópico 'Sala_Presenca'.

[INSCRIÇÃO] Central de Alarme inscrito no tópico 'Cozinha_Fumaca'.

[INSCRIÇÃO] Aplicativo do Morador inscrito no tópico 'Cozinha_Fumaca'.
```

Quando um evento for detectado:

```text
[Detector de Fumaça da Cozinha] Novo evento detectado.

[PUBLICAÇÃO] Tópico: Cozinha_Fumaca
Mensagem: Fumaça detectada na cozinha!

[Central de Alarme] recebeu do tópico 'Cozinha_Fumaca': Fumaça detectada na cozinha!

[Aplicativo do Morador] recebeu do tópico 'Cozinha_Fumaca': Fumaça detectada na cozinha!
```

Posteriormente é realizada a desinscrição:

```text
[DESINSCRIÇÃO] Aplicativo do Morador removido do tópico 'Cozinha_Fumaca'.
```

Em uma nova publicação, apenas os assinantes ainda ativos recebem a mensagem.

---

## 🎯 Conceitos demonstrados

O projeto demonstra os principais conceitos do padrão Publish/Subscribe:

- comunicação baseada em eventos;
- Publishers;
- Subscribers;
- Broker;
- tópicos;
- inscrição (`subscribe`);
- desinscrição (`unsubscribe`);
- publicação (`publish`);
- múltiplos Subscribers em um mesmo tópico;
- desacoplamento entre os componentes.

---

## 🏠 Cenário escolhido

**Tema 9 — Casa Inteligente e Automação Residencial (Smart Home)**

O cenário representa a integração entre dispositivos IoT de uma residência, permitindo que diferentes serviços reajam aos eventos gerados pelos sensores sem a necessidade de comunicação direta entre todos os componentes.