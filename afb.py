from datetime import datetime

class Transacao:
    transacoes = []

    def __init__(self, id_transacao, valor, data, localizacao, cliente_id):
        self.id_transacao = id_transacao
        self.valor = valor
        self.data = self._to_datetime(data)
        self.localizacao = localizacao
        self.cliente_id = cliente_id
        self._suspeita = False
        Transacao.transacoes.append(self)

    @staticmethod
    def _to_datetime(data):
        try:
            return datetime.strptime(data, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValueError(f"Data inválida: {data}")

    @property
    def suspeita(self):
        return "⊠" if self._suspeita else "☐"

    def __str__(self):
        return f"{self.id_transacao:<10}{self.valor:<10}{self.data:<20}{self.localizacao:<20}{self.cliente_id:<10}{self.suspeita:<10}"

    def marcar_suspeita(self):
        self._suspeita = True

def criar_transacoes():
    dados = [
        (1, 1500.00, '2023-08-21 10:00:00', 'Sao Paulo', 101),
        (2, 20000.00, '2023-08-21 11:00:00', 'Sao Paulo', 101),
        (3, 50.00, '2023-08-21 12:00:00', 'Rio de Janeiro', 101),
        (4, 12000.00, '2023-08-21 10:05:00', 'Sao Paulo', 102),
        (5, 1500.00, '2023-08-21 10:00:00', 'Nova York', 101)
    ]
    
    for id_transacao, valor, data, localizacao, cliente_id in dados:
        Transacao(id_transacao, valor, data, localizacao, cliente_id)

def detectar_suspeitas_por_valor(limite):
    for transacao in Transacao.transacoes:
        if transacao.valor > limite:
            transacao.marcar_suspeita()

def detectar_duplicatas():
    seen = {}
    duplicatas = []

    for transacao in Transacao.transacoes:
        key = (transacao.valor, transacao.data, transacao.localizacao)
        if key in seen:
            duplicatas.append(transacao.id_transacao)
            duplicatas.append(seen[key])
        else:
            seen[key] = transacao.id_transacao

    for transacao in Transacao.transacoes:
        if transacao.id_transacao in duplicatas:
            transacao.marcar_suspeita()

def detectar_suspeitas_por_localizacao():
    transacoes_ordenadas = sorted(Transacao.transacoes, key=lambda t: (t.cliente_id, t.data))
    
    for i in range(1, len(transacoes_ordenadas)):
        atual = transacoes_ordenadas[i]
        anterior = transacoes_ordenadas[i - 1]
        
        if atual.cliente_id == anterior.cliente_id:
            tempo_diferenca = (atual.data - anterior.data).total_seconds() / 3600.0
            if atual.localizacao != anterior.localizacao and tempo_diferenca < 1:
                atual.marcar_suspeita()
                anterior.marcar_suspeita()

def exibir_transacoes():
    print(f"{'ID':<10}{'Valor':<10}{'Data':<20}{'Localizacao':<20}{'Cliente_ID':<10}{'Suspeita':<10}")
    for transacao in Transacao.transacoes:
        print(transacao)

# Executando as funções
criar_transacoes()
detectar_suspeitas_por_valor(10000)
detectar_duplicatas()
detectar_suspeitas_por_localizacao()
exibir_transacoes()



