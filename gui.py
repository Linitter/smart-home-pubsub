import tkinter as tk
from tkinter import ttk
from contextlib import redirect_stdout
from io import StringIO

from pubsub import PubSub
from publishers import Publisher
from subscribers import Subscriber


class SmartHomeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home - Sistema Pub/Sub")
        self.root.geometry("1180x720")
        self.root.minsize(1000, 650)

        # Broker
        self.broker = PubSub()

        # Publishers
        self.publishers = {
            "presenca": Publisher(
                "Sensor de Presença da Sala",
                self.broker
            ),
            "fumaca": Publisher(
                "Detector de Fumaça da Cozinha",
                self.broker
            ),
            "seguranca": Publisher(
                "Fechadura Eletrônica",
                self.broker
            ),
            "temperatura": Publisher(
                "Sensor de Temperatura do Quarto",
                self.broker
            ),
        }

        # Subscribers
        self.subscribers = {
            "iluminacao": Subscriber(
                "Sistema de Iluminação"
            ),
            "alarme": Subscriber(
                "Central de Alarme"
            ),
            "aplicativo": Subscriber(
                "Aplicativo do Morador"
            ),
            "climatizacao": Subscriber(
                "Sistema de Climatização"
            ),
        }

        # Inscrições iniciais
        self.inscricoes = [
            (
                "Sala_Presenca",
                self.subscribers["iluminacao"]
            ),
            (
                "Cozinha_Fumaca",
                self.subscribers["alarme"]
            ),
            (
                "Cozinha_Fumaca",
                self.subscribers["aplicativo"]
            ),
            (
                "Geral_Seguranca",
                self.subscribers["alarme"]
            ),
            (
                "Geral_Seguranca",
                self.subscribers["aplicativo"]
            ),
            (
                "Quarto_Temperatura",
                self.subscribers["climatizacao"]
            ),
        ]

        self.variaveis_inscricao = {}

        self.configurar_estilo()
        self.criar_interface()
        self.ativar_inscricoes_iniciais()

    def configurar_estilo(self):
        estilo = ttk.Style()

        estilo.configure(
            "Titulo.TLabel",
            font=("TkDefaultFont", 18, "bold")
        )

        estilo.configure(
            "Subtitulo.TLabel",
            font=("TkDefaultFont", 11)
        )

        estilo.configure(
            "Secao.TLabelframe.Label",
            font=("TkDefaultFont", 11, "bold")
        )

        estilo.configure(
            "Evento.TButton",
            padding=(10, 9)
        )

    def criar_interface(self):
        container = ttk.Frame(
            self.root,
            padding=16
        )

        container.pack(
            fill="both",
            expand=True
        )

        # Cabeçalho
        cabecalho = ttk.Frame(container)

        cabecalho.pack(
            fill="x",
            pady=(0, 14)
        )

        ttk.Label(
            cabecalho,
            text="Smart Home - Sistema Publish/Subscribe",
            style="Titulo.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            cabecalho,
            text=(
                "Publique eventos e altere as inscrições "
                "para visualizar o funcionamento do padrão Pub/Sub."
            ),
            style="Subtitulo.TLabel",
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        # Área principal
        area_principal = ttk.Frame(container)

        area_principal.pack(
            fill="both",
            expand=True
        )

        area_principal.columnconfigure(
            0,
            weight=1
        )

        area_principal.columnconfigure(
            1,
            weight=1
        )

        area_principal.columnconfigure(
            2,
            weight=2
        )

        area_principal.rowconfigure(
            0,
            weight=1
        )

        self.criar_painel_eventos(
            area_principal
        )

        self.criar_painel_inscricoes(
            area_principal
        )

        self.criar_painel_log(
            area_principal
        )

        # Rodapé
        rodape = ttk.Frame(container)

        rodape.pack(
            fill="x",
            pady=(12, 0)
        )

        self.status_var = tk.StringVar()

        ttk.Label(
            rodape,
            textvariable=self.status_var
        ).pack(side="left")

        ttk.Button(
            rodape,
            text="Restaurar inscrições",
            command=self.restaurar_inscricoes,
        ).pack(side="right")

        self.atualizar_status()

    def criar_painel_eventos(self, parent):
        painel = ttk.LabelFrame(
            parent,
            text="Eventos / Publishers",
            padding=12,
        )

        painel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )

        eventos = [
            (
                "Detectar presença",
                "Sensor de Presença da Sala",
                lambda: self.publicar_evento(
                    "presenca",
                    "Sala_Presenca",
                    "Movimento detectado na sala.",
                ),
            ),
            (
                "Detectar fumaça",
                "Detector de Fumaça da Cozinha",
                lambda: self.publicar_evento(
                    "fumaca",
                    "Cozinha_Fumaca",
                    "Fumaça detectada na cozinha!",
                ),
            ),
            (
                "Abrir porta principal",
                "Fechadura Eletrônica",
                lambda: self.publicar_evento(
                    "seguranca",
                    "Geral_Seguranca",
                    "Porta principal foi aberta.",
                ),
            ),
            (
                "Registrar 28 °C no quarto",
                "Sensor de Temperatura do Quarto",
                lambda: self.publicar_evento(
                    "temperatura",
                    "Quarto_Temperatura",
                    "Temperatura atual do quarto: 28°C.",
                ),
            ),
        ]

        for linha, evento in enumerate(eventos):
            texto_botao, descricao, comando = evento

            ttk.Button(
                painel,
                text=texto_botao,
                command=comando,
                style="Evento.TButton",
            ).grid(
                row=linha * 2,
                column=0,
                sticky="ew",
                pady=(0, 3)
            )

            ttk.Label(
                painel,
                text=descricao,
                wraplength=260,
            ).grid(
                row=linha * 2 + 1,
                column=0,
                sticky="w",
                pady=(0, 14),
            )

        painel.columnconfigure(
            0,
            weight=1
        )

    def criar_painel_inscricoes(self, parent):
        painel = ttk.LabelFrame(
            parent,
            text="Inscrições / Subscribers",
            padding=12,
        )

        painel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=8
        )

        ttk.Label(
            painel,
            text=(
                "Marque ou desmarque para executar "
                "subscribe/unsubscribe."
            ),
            wraplength=280,
        ).pack(
            anchor="w",
            pady=(0, 12)
        )

        for topico, assinante in self.inscricoes:
            chave = (
                topico,
                assinante.nome
            )

            variavel = tk.BooleanVar(
                value=True
            )

            self.variaveis_inscricao[chave] = variavel

            bloco = ttk.Frame(painel)

            bloco.pack(
                fill="x",
                pady=5
            )

            ttk.Checkbutton(
                bloco,
                text=assinante.nome,
                variable=variavel,
                command=lambda t=topico,
                a=assinante,
                v=variavel: self.alternar_inscricao(
                    t,
                    a,
                    v
                ),
            ).pack(anchor="w")

            ttk.Label(
                bloco,
                text=f"Tópico: {topico}",
            ).pack(
                anchor="w",
                padx=(24, 0)
            )

    def criar_painel_log(self, parent):
        painel = ttk.LabelFrame(
            parent,
            text="Log de eventos",
            padding=12,
        )

        painel.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=(8, 0)
        )

        painel.columnconfigure(
            0,
            weight=1
        )

        painel.rowconfigure(
            0,
            weight=1
        )

        self.log = tk.Text(
            painel,
            wrap="word",
            state="disabled",
            font=("TkFixedFont", 10),
        )

        self.log.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar = ttk.Scrollbar(
            painel,
            orient="vertical",
            command=self.log.yview,
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.log.configure(
            yscrollcommand=scrollbar.set
        )

        ttk.Button(
            painel,
            text="Limpar log",
            command=self.limpar_log,
        ).grid(
            row=1,
            column=0,
            sticky="e",
            pady=(10, 0)
        )

    def ativar_inscricoes_iniciais(self):
        self.adicionar_log(
            "=== INSCRIÇÕES INICIAIS ===\n"
        )

        for topico, assinante in self.inscricoes:
            self.executar_capturando(
                self.broker.subscribe,
                topico,
                assinante,
            )

        self.adicionar_log(
            "\nSistema pronto para receber eventos.\n"
        )

        self.atualizar_status()

    def executar_capturando(
        self,
        funcao,
        *args
    ):
        buffer = StringIO()

        with redirect_stdout(buffer):
            funcao(*args)

        saida = buffer.getvalue()

        if saida:
            self.adicionar_log(saida)

    def adicionar_log(self, texto):
        self.log.configure(
            state="normal"
        )

        self.log.insert(
            "end",
            texto
        )

        self.log.see("end")

        self.log.configure(
            state="disabled"
        )

    def publicar_evento(
        self,
        publisher,
        topico,
        mensagem
    ):
        self.executar_capturando(
            self.publishers[publisher].publicar,
            topico,
            mensagem,
        )

        self.atualizar_status()

    def alternar_inscricao(
        self,
        topico,
        assinante,
        variavel
    ):
        if variavel.get():
            self.executar_capturando(
                self.broker.subscribe,
                topico,
                assinante,
            )

        else:
            self.executar_capturando(
                self.broker.unsubscribe,
                topico,
                assinante,
            )

        self.atualizar_status()

    def restaurar_inscricoes(self):
        self.adicionar_log(
            "\n=== RESTAURANDO INSCRIÇÕES ===\n"
        )

        for topico, assinante in self.inscricoes:
            chave = (
                topico,
                assinante.nome
            )

            self.variaveis_inscricao[
                chave
            ].set(True)

            self.executar_capturando(
                self.broker.subscribe,
                topico,
                assinante,
            )

        self.adicionar_log(
            "Inscrições restauradas.\n"
        )

        self.atualizar_status()

    def limpar_log(self):
        self.log.configure(
            state="normal"
        )

        self.log.delete(
            "1.0",
            "end"
        )

        self.log.configure(
            state="disabled"
        )

    def atualizar_status(self):
        quantidade_topicos = len(
            self.broker.topicos
        )

        quantidade_inscricoes = sum(
            len(assinantes)
            for assinantes
            in self.broker.topicos.values()
        )

        self.status_var.set(
            f"{quantidade_topicos} tópicos | "
            f"{quantidade_inscricoes} inscrições ativas"
        )


def main():
    root = tk.Tk()

    SmartHomeGUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()