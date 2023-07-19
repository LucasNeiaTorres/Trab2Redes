import socket
import libmensagem
import libconexao
import random
import time

HOST_PORT = socket.gethostbyname(socket.gethostname())
JOGADOR_CARTEADOR = 1

def jogar_grande_dalmuti(jogador_atual, total_jogadores, enderecos_portas):
    # Verificar se é a vez do jogador atual enviar a mensagem

    proximo_jogador = (jogador_atual + 1) % total_jogadores if jogador_atual != total_jogadores - 1 else 0
    proximo_endereco, proxima_porta = enderecos_portas[proximo_jogador].split(':')
    endereco_atual = enderecos_portas[jogador_atual].split(':')[0]
    porta_atual = int(enderecos_portas[jogador_atual].split(':')[1])

    tem_bastao = False
    if jogador_atual == JOGADOR_CARTEADOR:
        tem_bastao = True
    
    if jogador_atual == JOGADOR_CARTEADOR: 
        baralho = criar_baralho()
        # cartas sobrando
        cartas = distribuir_cartas(total_jogadores, baralho)
        jogador = 0
        for mao_jogador in cartas:
            mensagem = ','.join(str(carta) for carta in mao_jogador)
            if jogador != jogador_atual:
                mensagem = libmensagem.formatar_mensagem(mensagem, str(jogador_atual), str(jogador))
                libconexao.enviar_mensagem(mensagem, proximo_endereco, int(proxima_porta))
                recebe_confirmacao(mensagem, porta_atual, jogador_atual, proximo_endereco, proxima_porta, proximo_jogador)
            else:
                mao = mensagem
            jogador += 1
        mensagem = libmensagem.formatar_mensagem("PRONTO", str(jogador_atual), str(jogador_atual))
        libconexao.enviar_mensagem(mensagem, proximo_endereco, int(proxima_porta))
    else:
        ultimo_jogador = total_jogadores - 1
        while True:
            msg_atual = libconexao.receber_mensagem(porta_atual, jogador_atual, proximo_endereco, int(proxima_porta), proximo_jogador)
            if msg_atual != None:
                if libmensagem.obter_destino(msg_atual) == str(jogador_atual):
                    mao = libmensagem.obter_jogada(msg_atual)
                elif libmensagem.obter_jogada(msg_atual) == "PRONTO":
                    break
    
    print ("\n")
    print ("\n")

    #ordena a mao   
    mao = [int(carta) for carta in mao.split(",")]
    mao.sort()
    print(f"Suas cartas: {mao}")

    #conta quantidade de tipo de cartas na mão
    cartas = {}
    for carta in mao:
        if carta in cartas:
            cartas[carta] += 1
        else:
            cartas[carta] = 1

    #imprime cartas
    for i in cartas:
        print(f"Carta {i} quantidade: {cartas[i]}")
    mensagem = ""
    jogada_anterior = ""
    while True:
        if tem_bastao:
            print(f"\033[94mMão: {mao}\033[0m")        
            if jogada_anterior:
                sequencia2 = libmensagem.obter_sequencia(jogada_anterior)
                if int(libmensagem.obter_sequencia(jogada_anterior)) >= total_jogadores:
                        if libmensagem.obter_menor_origem(jogada_anterior) != str(jogador_atual):
                            tem_bastao = False
                            bastao = libmensagem.formatar_mensagem("BASTAO1", str(jogador_atual), libmensagem.obter_menor_origem(jogada_anterior))
                            libconexao.enviar_mensagem(bastao, proximo_endereco, int(proxima_porta)) 
                            jogada_anterior = ""
                            continue
                if not tem_menor_carta(mao, jogada_anterior):
                    print("\033[91mSem jogadas válidas!\033[0m")
                    passa_vez = "S"
                else:
                    passa_vez = input("Deseja passar a vez? (S/N): ")
                
                if passa_vez == "S": 
                    tem_bastao = False
                    if int(libmensagem.obter_sequencia(jogada_anterior)) >= total_jogadores:
                        mensagem = libmensagem.formatar_mensagem("BASTAO1", str(jogador_atual), libmensagem.obter_menor_origem(jogada_anterior)[1])
                    else:
                        mensagem = libmensagem.formatar_mensagem("BASTAO", str(jogador_atual), str(proximo_jogador))
                    libconexao.enviar_mensagem(mensagem, proximo_endereco, int(proxima_porta))
                    continue
            qtde_coringa_jogados = 0
            if qtde_coringa_mao(mao) > 0:
                coringa = input("Deseja jogar o coringa? (S/N): ")
                if coringa == "S":
                    qtde_coringa_jogados = int(input("Digite a quantidade de coringas que deseja jogar: "))
                    while qtde_coringa_jogados > qtde_coringa_mao(mao):
                        qtde_coringa_jogados = int(input("Digite uma quantidade de coringas válida: "))
                    
                    cartas[13] -= int(qtde_coringa_jogados)
                    for i in range(qtde_coringa_jogados):
                        mao.remove(13)

            # ver se há a quantidade que falta para completar a sequencia
            mensagem = input("\nJogue sua carta: ")
            while not eh_jogada_valida(cartas, mensagem, mao, jogada_anterior, qtde_coringa_jogados):
                mensagem = input("Jogada inválida! Jogue uma carta válida: ") 
            
            qtde = input(f"Digite a quantidade de cartas {mensagem} que deseja jogar: ")
            while not tem_qtde_cartas(cartas, mensagem, qtde, jogada_anterior, qtde_coringa_jogados):
                qtde = input("Jogada inválida! Digite uma quantidade válida: ") 
            
            for i in range(int(qtde)):
                mao.remove(int(mensagem))

            cartas[int(mensagem)] -= int(qtde)

            #verifica se a mão do jogador ficou vazia 
            if len(mao) == 0:
                print ("Você se tornou o Grande Dalmuti. Parabéns!!!!")
                mensagem = "FIM"
                mensagem = libmensagem.formatar_mensagem(mensagem, str(jogador_atual), str(jogador_atual))
                libconexao.enviar_mensagem(mensagem, proximo_endereco, int(proxima_porta))
            #imprime a mão do jogador
            mensagem_qtde = mensagem + "," + qtde
            # botar coringa na mensagem
            if jogada_anterior:
                sequencia = str(int(libmensagem.obter_sequencia(jogada_anterior)) + 1)
            else:
                sequencia = "1"
            if qtde_coringa_jogados > 0:
                if not jogada_anterior:
                    mensagem = mensagem_qtde + ", 13," + str(qtde_coringa_jogados) + ", " + mensagem + ", " + str(jogador_atual) + ", " + sequencia
                else:
                    if int(libmensagem.obter_menor_carta(jogada_anterior)) > int(mensagem):
                        mensagem = mensagem_qtde + ", 13," + str(qtde_coringa_jogados) + ", " + mensagem + ", " + str(jogador_atual) + ", " + sequencia
                    else:
                        mensagem = mensagem_qtde + ", 13," + str(qtde_coringa_jogados) + ", " + libmensagem.obter_menor_carta(jogada_anterior) + ", " + libmensagem.obter_menor_origem(jogada_anterior) + ", " + sequencia
            else:
                if not jogada_anterior:
                    mensagem = mensagem_qtde + ", 0, 0, " + mensagem + ", " + str(jogador_atual) + ", " + sequencia 
                else:
                    if int(libmensagem.obter_menor_carta(jogada_anterior)) > int(mensagem):
                        mensagem = mensagem_qtde + ", 0, 0, " + mensagem + ", " + str(jogador_atual) + ", " + sequencia 
                    else:
                        mensagem = mensagem_qtde + ", 0, 0, " + libmensagem.obter_menor_carta(jogada_anterior) + ", " + libmensagem.obter_menor_origem(jogada_anterior) + ", " + sequencia 

            mensagem = libmensagem.formatar_mensagem(mensagem, str(jogador_atual), str(jogador_atual))
            libconexao.enviar_mensagem(mensagem, proximo_endereco, int(proxima_porta))
            tem_bastao = False
        else:
            mensagem_recebida = libconexao.receber_mensagem(porta_atual, jogador_atual, proximo_endereco, int(proxima_porta), proximo_jogador)
            if mensagem_recebida != None:
                if libmensagem.obter_jogada(mensagem_recebida) == "BASTAO":
                    if libmensagem.obter_destino(mensagem_recebida) == str(jogador_atual):
                        tem_bastao = True
                    else:
                        libconexao.enviar_mensagem(mensagem_recebida, proximo_endereco, int(proxima_porta))
                elif libmensagem.obter_jogada(mensagem_recebida) == "BASTAO1":
                    if libmensagem.obter_destino(mensagem_recebida) == str(jogador_atual):
                        tem_bastao = True
                        jogada_anterior = ""
                    else: 
                        libconexao.enviar_mensagem(mensagem_recebida, proximo_endereco, int(proxima_porta))
                elif libmensagem.obter_jogada(mensagem_recebida) == "CONFIRMACAO":
                    continue
                else:
                    carta_jogada = libmensagem.obter_carta_jogada(mensagem_recebida)
                    qtde_jogada = libmensagem.obter_qtde_jogada(mensagem_recebida)
                    qtde_coringa = int(libmensagem.obter_qtde_coringas(mensagem_recebida))
                    origem = libmensagem.obter_origem(mensagem_recebida)

                    if int(libmensagem.obter_sequencia(mensagem_recebida)) == total_jogadores:
                        jogada_anterior = ""
                    else:
                        jogada_anterior = mensagem_recebida

                    print(f"\nJogada do jogador {str(int(origem) + 1)}:")
                    print(f"Carta: {carta_jogada} Quantidade: {qtde_jogada}")
                    if qtde_coringa > 0:
                        print(f"Carta: 13 (Coringa) Quantidade: {qtde_coringa}")
                    

def recebe_confirmacao(mensagem, porta_atual, jogador_atual, proximo_endereco, proxima_porta, proximo_jogador):
    mensagem_confirmacao = None
    while mensagem_confirmacao == None:
        mensagem_confirmacao = libconexao.receber_mensagem(porta_atual, jogador_atual, proximo_endereco, int(proxima_porta), proximo_jogador)
        if mensagem_confirmacao != None:
            if (libmensagem.obter_confirmacao(mensagem_confirmacao) == "1") and (libmensagem.obter_destino(mensagem_confirmacao) == str(jogador_atual)):
                break
            else:
                mensagem_confirmacao = None
        else:
            libconexao.enviar_mensagem(mensagem, proximo_endereco, int(proxima_porta))

def configurar_jogo():
    with open('config.txt', 'r') as file:
        total_jogadores_line = file.readline().strip()
        total_jogadores = int(total_jogadores_line.split('#')[0].strip())
        enderecos_portas = [line.strip().split('#')[0].strip() for line in file.readlines() if line.strip()]

    print("Total de jogadores:", total_jogadores)
    print("Endereços e portas:")
    for endereco_porta in enderecos_portas:
        print(endereco_porta)

    return total_jogadores, enderecos_portas

def criar_baralho():
    baralho = []
    for i in range(1, 13):
        for _ in range(i):
            baralho.append(i)
    baralho.append(13)
    baralho.append(13)
    random.shuffle(baralho)

    return baralho
    
def distribuir_cartas(total_jogadores, baralho):
    cartas_por_jogador = len(baralho) // total_jogadores
    conjunto_cartas = []
    for i in range(total_jogadores):
        cartas = baralho[i * cartas_por_jogador: (i + 1) * cartas_por_jogador]
        conjunto_cartas.append(cartas)

    return conjunto_cartas

def tem_menor_carta(mao, jogada_anterior):
    tem_menor = False
    for i in range(len(mao)):
        if mao[i] <= int(libmensagem.obter_carta_jogada(jogada_anterior)):
            tem_menor = True
    return tem_menor

def qtde_coringa_mao(mao):
    qtde = 0
    for i in range(len(mao)):
        if mao[i] == 13:
            qtde += 1
    return qtde

def tem_qtde_cartas(cartas, mensagem, qtde, jogada_anterior, qtde_coringa_jogados):
    tem_qtde = False
    for carta in cartas:
        if str(carta) == mensagem:
            if cartas[carta] + qtde_coringa_jogados >= int(qtde):
                tem_qtde = True
    if not tem_qtde:
        return False
    if jogada_anterior:
        if int(qtde) + qtde_coringa_jogados != int(libmensagem.obter_qtde_jogada(jogada_anterior)) + int(libmensagem.obter_qtde_coringas(jogada_anterior)):
            return False
    return True

def eh_jogada_valida(cartas, jogada, mao, jogada_anterior, qtde_coringa_jogados):
    tem_carta = False
    for carta in mao:
        if str(carta) == str(jogada):
            tem_carta = True
            break
    if not tem_carta:
        return False
    if jogada_anterior:
        if int(jogada) > int(libmensagem.obter_carta_jogada(jogada_anterior)):
            return False
        if cartas[int(jogada)] + qtde_coringa_jogados < int(libmensagem.obter_qtde_jogada(jogada_anterior)) + int(libmensagem.obter_qtde_coringas(jogada_anterior)):
            return False
    return True

def main():
    total_jogadores, enderecos_portas = configurar_jogo()
    jogador_atual = next((i for i, elemento in enumerate(enderecos_portas) if elemento.split(':')[0] == HOST_PORT), -1)
    jogar_grande_dalmuti(jogador_atual, total_jogadores, enderecos_portas)        

if __name__ == "__main__":
    main()
