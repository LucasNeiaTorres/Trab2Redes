import socket
import libmensagem

TIMEOUT = 0.2 # segundos
MAX_TENTATIVAS = 10

# Função para enviar mensagem para o próximo jogador no anel
def enviar_mensagem(mensagem, endereco, porta):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(mensagem.encode(), (endereco, porta))

# Função para receber mensagem do jogador anterior no anel
def receber_mensagem(porta, jogador_atual, proximo_endereco, proxima_porta, proximo_jogador):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', porta))
        s.settimeout(TIMEOUT)
        try:
            mensagem, endereco = s.recvfrom(1024)
            mensagem = mensagem.decode()

            if libmensagem.eh_mensagem_valida(mensagem):
                origem = libmensagem.obter_origem(mensagem)
                destino = libmensagem.obter_destino(mensagem)
                jogada = libmensagem.obter_jogada(mensagem)

                if destino == str(jogador_atual) and origem != destino:
                    if libmensagem.obter_confirmacao(mensagem) == "0" and libmensagem.obter_jogada(mensagem) != "BASTAO":
                        mensagem_confirmacao = libmensagem.formatar_mensagem("CONFIRMACAO", libmensagem.obter_destino(mensagem), libmensagem.obter_origem(mensagem))
                        mensagem_confirmacao = libmensagem.criar_confirmacao(mensagem_confirmacao)
                        # print(f"Mensagem recebida: {mensagem} enviando confirmacao {mensagem_confirmacao}") 
                        enviar_mensagem(mensagem_confirmacao, proximo_endereco, int(proxima_porta))
                    return mensagem     
                elif origem == str(jogador_atual):
                    bastao = libmensagem.formatar_mensagem("BASTAO", str(jogador_atual), str(proximo_jogador))
                    enviar_mensagem(bastao, proximo_endereco, int(proxima_porta))
                    return None
                else:
                    enviar_mensagem(mensagem, proximo_endereco, int(proxima_porta))
                    return mensagem
            else:
                return None
        except socket.timeout:
            return None
