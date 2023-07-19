def distribuir_cartas(total_jogadores, baralho, enderecos_portas):
    cartas_por_jogador = len(baralho) // total_jogadores
    conjunto_cartas = {}
    for i in range(total_jogadores):
        cartas = baralho[i * cartas_por_jogador: (i + 1) * cartas_por_jogador]
        conjunto_cartas[f"cartas{i + 1}"] = cartas
        cartas_str = ','.join(str(carta) for carta in cartas)
        mensagem = libmensagem.formatar_mensagem("CARTAS", cartas_str)
        endereco, porta = enderecos_portas[i].split(':')
        libconexao.enviar_mensagem(mensagem, endereco, int(porta))
        print("Cartas enviadas para Jogador", i + 1)
        mensagem = []
        # imprime pulando linha para cada jogador
        print(conjunto_cartas[f"cartas{i + 1}"], "\n")
    # imprime todos os conjuntos de cartas
    for i in range(total_jogadores):
        print(conjunto_cartas[f"cartas{i + 1}"])

def main():
    total_jogadores, enderecos_portas = configurar_jogo()
    jogador_atual = next((i for i, elemento in enumerate(enderecos_portas) if elemento.split(':')[0] == HOST_PORT), -1)
    if jogador_atual == 0:
        baralho = criar_baralho()
        print (baralho)
        distribuir_cartas(total_jogadores, baralho, enderecos_portas)
    jogar_grande_dalmuti(jogador_atual, total_jogadores, enderecos_portas)