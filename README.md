# 🏠 Smart Home Pub/Sub

Projeto desenvolvido para a disciplina **Sistemas Computacionais Distribuídos e Computação em Nuvem**, com o objetivo de demonstrar na prática o funcionamento do padrão arquitetural **Publish/Subscribe (Pub/Sub)** aplicado a um cenário de **Casa Inteligente e Automação Residencial (Smart Home)**.

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

## 📌 Sobre o projeto

Uma casa inteligente pode possuir diversos sensores, dispositivos e serviços que precisam reagir a eventos como:

- presença detectada em um cômodo;
- fumaça detectada na cozinha;
- abertura de uma porta;
- alteração de temperatura.

Em uma abordagem com comunicação direta, um sensor precisaria conhecer todos os sistemas interessados nos seus eventos.

Por exemplo, um detector de fumaça poderia precisar comunicar-se diretamente com:

- a Central de Alarme;
- o Aplicativo do Morador;
- outros serviços interessados.

Com o padrão **Publish/Subscribe**, o sensor apenas publica uma mensagem em determinado tópico.

O **Broker** é responsável por identificar os Subscribers inscritos naquele tópico e encaminhar a mensagem para eles.

Dessa forma, o Publisher não precisa conhecer diretamente os consumidores das suas mensagens.

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

O detector de fumaça não precisa conhecer a Central de Alarme nem o Aplicativo do Morador.

Ele conhece apenas o **Broker** e o **tópico** no qual deseja publicar.

---

## 📡 Publishers

Os **Publishers** representam os dispositivos responsáveis por gerar eventos dentro da casa.

| Publisher | Evento |
|---|---|
| Sensor de Presença da Sala | Detecta movimento na sala |
| Detector de Fumaça da Cozinha | Detecta fumaça |
| Fechadura Eletrônica | Informa abertura da porta |
| Sensor de Temperatura do Quarto | Informa a temperatura |

---

## 📥 Subscribers

Os **Subscribers** representam os sistemas interessados em receber determinados eventos.

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

Um Subscriber recebe somente as mensagens dos tópicos nos quais está inscrito.

---

## ⚙️ Broker Pub/Sub

A classe `PubSub`, localizada em `pubsub.py`, representa o **Broker** da aplicação.

Ela mantém os tópicos existentes e os Subscribers inscritos em cada um deles.

O Broker implementa três operações principais.

### `subscribe(topico, assinante)`

Inscreve um Subscriber em determinado tópico.

```python
broker.subscribe(
    "Cozinha_Fumaca",
    aplicativo_morador
)
```

Depois da inscrição, o Subscriber passa a receber as novas mensagens publicadas naquele tópico.

---

### `unsubscribe(topico, assinante)`

Remove um Subscriber de determinado tópico.

```python
broker.unsubscribe(
    "Cozinha_Fumaca",
    aplicativo_morador
)
```

Depois da remoção, novas mensagens publicadas naquele tópico deixam de ser entregues ao Subscriber removido.

---

### `publish(topico, mensagem)`

Publica uma mensagem em determinado tópico.

```python
broker.publish(
    "Cozinha_Fumaca",
    "Fumaça detectada na cozinha!"
)
```

O Broker identifica todos os Subscribers atualmente inscritos e encaminha a mensagem para cada um deles.

---

## 🧪 Simulação em terminal

O arquivo `main.py` executa automaticamente uma demonstração do sistema.

A simulação está dividida em três cenários.

### Cenário 1 — Funcionamento normal

Primeiro são realizadas todas as inscrições.

Em seguida, são simulados eventos como:

```text
Movimento detectado na sala
Fumaça detectada na cozinha
Porta principal aberta
Temperatura do quarto registrada
```

No caso da fumaça:

```text
Detector de Fumaça
       │
       ▼
Cozinha_Fumaca
       │
       ▼
     Broker
       │
   ┌───┴──────────┐
   ▼              ▼
Central de     Aplicativo
 Alarme        do Morador
```

Como os dois Subscribers estão inscritos em `Cozinha_Fumaca`, ambos recebem a mensagem.

---

### Cenário 2 — Unsubscribe parcial

O **Aplicativo do Morador** é removido do tópico:

```text
Cozinha_Fumaca
```

A operação utilizada é:

```python
broker.unsubscribe(
    "Cozinha_Fumaca",
    aplicativo_morador
)
```

Depois disso, um novo alerta de fumaça é publicado.

O fluxo passa a ser:

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

A **Central de Alarme continua recebendo a mensagem**, pois permanece inscrita.

O **Aplicativo do Morador não recebe mais**, demonstrando o funcionamento do `unsubscribe()`.

---

### Cenário 3 — Tópico sem assinantes

O **Sistema de Iluminação** é removido do tópico:

```text
Sala_Presenca
```

Como ele era o único Subscriber daquele tópico, uma nova publicação encontra o tópico sem assinantes.

O Broker informa:

```text
Nenhum assinante neste tópico.
```

Esse cenário demonstra que o sistema também trata publicações realizadas em tópicos sem Subscribers ativos.

---

# 🖥️ Interface gráfica

Além da demonstração automatizada em terminal, o projeto possui uma **interface gráfica desenvolvida com Tkinter**.

A interface permite visualizar e controlar interativamente o funcionamento do Pub/Sub.

Ela apresenta três áreas principais:

```text
┌──────────────────────────────────────────────────────────────┐
│             SMART HOME - SISTEMA PUB/SUB                   │
├────────────────┬───────────────────┬─────────────────────────┤
│    Eventos     │    Inscrições    │      Log de eventos    │
│   Publishers   │    Subscribers   │                         │
│                │                   │                         │
│ Detectar       │ ☑ Iluminação     │ Publicações             │
│ presença       │ ☑ Alarme         │ Inscrições              │
│                │ ☑ Aplicativo     │ Desinscrições           │
│ Detectar       │ ☑ Climatização   │ Mensagens recebidas     │
│ fumaça         │                   │                         │
│                │                   │                         │
│ Abrir porta    │                   │                         │
│                │                   │                         │
│ Temperatura    │                   │                         │
└────────────────┴───────────────────┴─────────────────────────┘
```

---

## 🔘 Eventos da interface

Os botões da interface representam os Publishers.

É possível simular:

- presença detectada;
- fumaça detectada;
- abertura da porta principal;
- alteração de temperatura.

Ao clicar em um botão, o respectivo Publisher envia a mensagem para o Broker.

---

## ☑️ Subscribe e Unsubscribe pela interface

Os checkboxes representam as inscrições dos Subscribers.

Ao desmarcar um Subscriber, a interface executa:

```python
unsubscribe()
```

Ao marcá-lo novamente:

```python
subscribe()
```

Isso permite visualizar interativamente o comportamento do sistema.

### Exemplo

Inicialmente:

```text
Cozinha_Fumaca

☑ Central de Alarme
☑ Aplicativo do Morador
```

Ao publicar um alerta:

```text
Central de Alarme        → recebeu
Aplicativo do Morador    → recebeu
```

Depois de desmarcar o Aplicativo do Morador:

```text
Cozinha_Fumaca

☑ Central de Alarme
☐ Aplicativo do Morador
```

Uma nova publicação resulta em:

```text
Central de Alarme        → recebeu
Aplicativo do Morador    → não recebe
```

Dessa forma, a GUI permite visualizar diretamente o fluxo:

```text
subscribe
    ↓
publish
    ↓
entrega aos inscritos
    ↓
unsubscribe
    ↓
nova publicação
```

---

## 📊 Log de eventos

A interface também possui um painel de log.

Ele apresenta:

```text
[INSCRIÇÃO]
[PUBLICAÇÃO]
[DESINSCRIÇÃO]
mensagens recebidas pelos Subscribers
```

Exemplo:

```text
[PUBLICAÇÃO] Tópico: Cozinha_Fumaca
Mensagem: Fumaça detectada na cozinha!

[Central de Alarme] recebeu do tópico 'Cozinha_Fumaca':
Fumaça detectada na cozinha!

[Aplicativo do Morador] recebeu do tópico 'Cozinha_Fumaca':
Fumaça detectada na cozinha!
```

A interface também apresenta a quantidade de tópicos e inscrições atualmente ativas.

---

## 🔄 Restaurar inscrições

A interface possui a opção:

```text
Restaurar inscrições
```

Essa funcionalidade retorna todos os Subscribers às inscrições iniciais da simulação.

Isso facilita repetir diferentes cenários durante a demonstração.

---

## ✅ Testes automatizados

O projeto possui testes automatizados utilizando o módulo `unittest`.

Os testes estão localizados em:

```text
tests/test_pubsub.py
```

São verificados cinco comportamentos principais do Broker:

1. inscrição de um Subscriber em um tópico;
2. prevenção de inscrições duplicadas;
3. publicação para todos os Subscribers inscritos;
4. interrupção do recebimento após `unsubscribe`;
5. publicação em um tópico sem Subscribers.

Os testes utilizam um Subscriber de teste para verificar diretamente o comportamento do Broker.

---

## 📁 Estrutura do projeto

```text
smart-home-pubsub/
│
├── tests/
│   └── test_pubsub.py
│
├── gui.py
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
subscribe()
unsubscribe()
publish()
```

### `publishers.py`

Contém a classe `Publisher`, utilizada pelos dispositivos responsáveis por gerar eventos.

### `subscribers.py`

Contém a classe `Subscriber`, utilizada pelos sistemas que recebem as mensagens.

### `main.py`

Executa automaticamente a demonstração em terminal.

É responsável por:

```text
criar o Broker
criar Publishers
criar Subscribers
realizar inscrições
publicar eventos
demonstrar unsubscribe
demonstrar tópico sem assinantes
```

### `gui.py`

Contém a interface gráfica desenvolvida com Tkinter.

Permite publicar eventos e modificar inscrições interativamente.

### `tests/test_pubsub.py`

Contém os testes automatizados do Broker.

---

## 💻 Tecnologias utilizadas

- Python 3
- Tkinter
- unittest
- Git
- GitHub
- WSL2
- Visual Studio Code

O projeto não possui dependências de pacotes PyPI.

Em distribuições Ubuntu onde o Tkinter não esteja disponível, pode ser necessário instalar o pacote do sistema:

```bash
sudo apt update
sudo apt install python3-tk
```

---

# 🚀 Como executar

## 1. Clonar o repositório

```bash
git clone https://github.com/Linitter/smart-home-pubsub.git
```

Entre na pasta:

```bash
cd smart-home-pubsub
```

---

## 2. Verificar o Python

```bash
python3 --version
```

É necessário possuir o **Python 3** instalado.

---

## 3. Executar a simulação em terminal

```bash
python3 main.py
```

O programa executará automaticamente os três cenários:

```text
CENÁRIO 1 - FUNCIONAMENTO NORMAL

CENÁRIO 2 - UNSUBSCRIBE PARCIAL

CENÁRIO 3 - TÓPICO SEM ASSINANTES
```

---

## 4. Executar a interface gráfica

```bash
python3 gui.py
```

A GUI permite realizar a demonstração do Pub/Sub de forma interativa.

Caso o Tkinter não esteja instalado no Ubuntu:

```bash
sudo apt update
sudo apt install python3-tk
```

Depois execute novamente:

```bash
python3 gui.py
```

---

# 🧪 Como executar os testes

Na raiz do projeto:

```bash
python3 -m unittest discover -s tests -v
```

O resultado esperado é semelhante a:

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

Se aparecer:

```text
OK
```

todos os testes foram aprovados.

---

## 📋 Exemplo de funcionamento

Durante a execução são realizadas as inscrições:

```text
[INSCRIÇÃO] Sistema de Iluminação inscrito no tópico 'Sala_Presenca'.

[INSCRIÇÃO] Central de Alarme inscrito no tópico 'Cozinha_Fumaca'.

[INSCRIÇÃO] Aplicativo do Morador inscrito no tópico 'Cozinha_Fumaca'.
```

Quando o detector de fumaça identifica um evento:

```text
[Detector de Fumaça da Cozinha] Novo evento detectado.

[PUBLICAÇÃO] Tópico: Cozinha_Fumaca
Mensagem: Fumaça detectada na cozinha!

[Central de Alarme] recebeu do tópico 'Cozinha_Fumaca':
Fumaça detectada na cozinha!

[Aplicativo do Morador] recebeu do tópico 'Cozinha_Fumaca':
Fumaça detectada na cozinha!
```

Depois, o Aplicativo do Morador pode ser removido:

```text
[DESINSCRIÇÃO] Aplicativo do Morador removido do tópico 'Cozinha_Fumaca'.
```

Em uma nova publicação, apenas os Subscribers que continuam inscritos recebem a mensagem.

---

# 💡 Desacoplamento

Uma das principais características demonstradas pelo projeto é o **desacoplamento**.

Sem Pub/Sub:

```text
Sensor ─────► Central de Alarme
       │
       ├────► Aplicativo
       │
       └────► Outro Serviço
```

O sensor precisaria conhecer diretamente cada consumidor.

Com Pub/Sub:

```text
              ┌──► Subscriber A
              │
Publisher ─► Broker ─► Subscriber B
              │
              └──► Subscriber C
```

O Publisher não precisa saber:

```text
quantos Subscribers existem
quem são os Subscribers
como os Subscribers utilizarão a mensagem
```

Ele apenas publica um evento em determinado tópico.

O Broker é responsável pela distribuição.

---

# ℹ️ Escopo da implementação

Este projeto apresenta uma **implementação didática do padrão Publish/Subscribe em memória**.

O Broker é implementado diretamente pela classe:

```text
PubSub
```

Não são utilizados brokers externos como:

```text
Apache Kafka
RabbitMQ
Redis Pub/Sub
```

Na implementação atual, Publisher, Broker e Subscribers são executados dentro do mesmo processo Python.

O objetivo é demonstrar claramente a lógica fundamental do padrão:

```text
Subscriber
    │
    │ subscribe()
    ▼
  Broker
    ▲
    │ publish()
Publisher
    │
    ▼
Mensagem distribuída
    │
    ▼
Subscribers inscritos
```

Em um sistema distribuído de produção, uma ferramenta de mensageria poderia assumir o papel do Broker e permitir a comunicação entre serviços executados em processos ou máquinas diferentes.

---

# 🎓 Conceitos demonstrados

O projeto permite visualizar na prática:

- padrão Publish/Subscribe;
- arquitetura orientada a eventos;
- Publisher;
- Subscriber;
- Broker;
- tópicos;
- `subscribe`;
- `unsubscribe`;
- `publish`;
- múltiplos Subscribers em um tópico;
- tópicos sem Subscribers;
- desacoplamento;
- simulação baseada em eventos;
- testes automatizados;
- interface gráfica para visualização do fluxo.

---

# 📚 Resumo do fluxo

```text
1. Subscriber executa subscribe()
                │
                ▼
2. Broker registra a inscrição
                │
                ▼
3. Publisher detecta um evento
                │
                ▼
4. Publisher executa publish()
                │
                ▼
5. Broker localiza os inscritos
                │
                ▼
6. Subscribers recebem a mensagem
                │
                ▼
7. Subscriber pode executar unsubscribe()
                │
                ▼
8. Novas mensagens deixam de ser entregues a ele
```

---

# 🏠 Resultado

A aplicação demonstra como dispositivos de uma **Smart Home** podem comunicar eventos utilizando o padrão **Publish/Subscribe**, evitando dependências diretas entre sensores e sistemas consumidores.

O projeto oferece duas formas de demonstração:

```text
python3 main.py
```

Simulação automática através do terminal.

```text
python3 gui.py
```

Simulação gráfica e interativa.

Além disso, o comportamento central do Broker é validado através de testes automatizados:

```text
python3 -m unittest discover -s tests -v
```

Dessa forma, o projeto demonstra de maneira prática os papéis de **Publisher, Subscriber, Broker e tópicos**, além das operações fundamentais:

```text
subscribe → publish → entrega → unsubscribe
```