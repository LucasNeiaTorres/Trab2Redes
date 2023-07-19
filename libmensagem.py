MARCADOR_INICIO = "<<"
MARCADOR_FIM = ">>"

def formatar_mensagem(mensagem, origem, destino):
    return MARCADOR_INICIO + origem + destino + mensagem + "0" + MARCADOR_FIM

def desformatar_mensagem(mensagem):
    return mensagem[len(MARCADOR_INICIO) : -len(MARCADOR_FIM)]

def obter_jogada(mensagem):
    return mensagem[len(MARCADOR_INICIO) + 2 : -len(MARCADOR_FIM) - 1]

def obter_carta_jogada(mensagem):
    mensagem = obter_jogada(mensagem)
    return mensagem.split(",")[0]

def obter_qtde_jogada(mensagem):
    mensagem = obter_jogada(mensagem)
    return mensagem.split(",")[1]

def obter_qtde_coringas(mensagem):
    mensagem = obter_jogada(mensagem)
    return mensagem.split(",")[3]

def obter_menor_carta(mensagem):
    mensagem = obter_jogada(mensagem)
    return mensagem.split(",")[4]

def obter_menor_origem(mensagem):
    mensagem = obter_jogada(mensagem)
    return mensagem.split(",")[5]

def obter_sequencia(mensagem):
    mensagem = obter_jogada(mensagem)
    return mensagem.split(",")[6]

def obter_origem(mensagem):
    return mensagem[len(MARCADOR_INICIO) : len(MARCADOR_INICIO) + 1]

def obter_destino(mensagem):
    return mensagem[len(MARCADOR_INICIO) + 1 : len(MARCADOR_INICIO) + 2]

def obter_confirmacao(mensagem):
    return mensagem[-len(MARCADOR_FIM) - 1 : -len(MARCADOR_FIM)]

def eh_mensagem_valida(mensagem):
    return mensagem.startswith(MARCADOR_INICIO) and mensagem.endswith(MARCADOR_FIM)

def criar_confirmacao(mensagem):
    return mensagem[:-len(MARCADOR_FIM) - 1] + "1" + MARCADOR_FIM
