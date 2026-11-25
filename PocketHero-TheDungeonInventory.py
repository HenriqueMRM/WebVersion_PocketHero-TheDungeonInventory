# Pocket Hero: The Dungeon Inventory - Versão Web (PyScript)

# 'document' e 'window' são a ponte entre o Python e a página HTML (PyScript).
from pyscript import document, window
import random

# ==========================================
# 1. DICIONÁRIOS DO JOGO E ITENS
# ==========================================
# Dicionário com todos os itens do jogo (armas, armaduras e comidas).
# Chaves possíveis de cada item:
#   "preço"        -> custo na loja (itens de drop de boss não têm preço)
#   "dano"         -> dano base (existe apenas em armas)
#   "durabilidade" -> quantidade de usos antes de quebrar (existe apenas em armas)
#   "tipo"         -> Sword, Bow, Axe, Scythe ou Armor
#   "armadura"     -> redução de dano (existe apenas em armaduras)
#   "cura"         -> HP recuperado (existe apenas em comidas)
#   "descrição"    -> texto opcional exibido na loja e na mochila
tabela_itens = {
    # Espadas
    "Wooden Sword": {"preço": 5, "dano": 5, "durabilidade": 10, "tipo": "Sword"},
    "Stone Sword": {"preço": 20, "dano": 15, "durabilidade": 25, "tipo": "Sword"},
    "Iron Sword": {"preço": 40, "dano": 25, "durabilidade": 35, "tipo": "Sword"},
    "Diamond Sword": {"preço": 70, "dano": 35, "durabilidade": 50, "tipo": "Sword"},
    "Soul Reaver": {"preço": 250, "dano": 75, "durabilidade": 100, "tipo": "Sword"},
    # Arcos
    "Wooden Bow": {"preço": 5, "dano": 5, "durabilidade": 10, "tipo": "Bow", "descrição": "Dispara duas vezes, mas consome o dobro de durabilidade."},
    "Hunter Bow": {"preço": 30, "dano": 15, "durabilidade": 20, "tipo": "Bow", "descrição": "Dispara duas vezes, mas consome o dobro de durabilidade."},
    "Bone Bow": {"preço": 50, "dano": 25, "durabilidade": 30, "tipo": "Bow", "descrição": "Dispara duas vezes, mas consome o dobro de durabilidade."},
    "Shadow Bow": {"preço": 75, "dano": 30, "durabilidade": 40, "tipo": "Bow", "descrição": "Dispara duas vezes, mas consome o dobro de durabilidade."},
    "Soulseeker": {"preço": 250, "dano": 50, "durabilidade": 100, "tipo": "Bow", "descrição": "Dispara duas vezes, mas consome o dobro de durabilidade."},
    # Machados
    "Wooden Axe": {"preço": 5, "dano": 10, "durabilidade": 5, "tipo": "Axe"},
    "Stone Axe": {"preço": 20, "dano": 25, "durabilidade": 15, "tipo": "Axe"},
    "Iron Axe": {"preço": 40, "dano": 35, "durabilidade": 25, "tipo": "Axe"},
    "Diamond Axe": {"preço": 70, "dano": 50, "durabilidade": 35, "tipo": "Axe"},
    "Soul Cleaver": {"preço": 250, "dano": 100, "durabilidade": 75, "tipo": "Axe"},
    # Drops de Bosses (não vendidos na loja, por isso não possuem "preço")
    "Soul Reaper": {"dano": 250, "durabilidade": 250, "tipo": "Scythe", "descrição": "A arma definitiva dos deuses da morte."},
    "Vampiric Blade": {"dano": 50, "durabilidade": 20, "tipo": "Sword", "descrição": "Cura 5 de HP a cada golpe."},
    "Dragon Bow": {"dano": 50, "durabilidade": 10, "tipo": "Bow", "descrição": "Dispara duas vezes, mas consome o dobro de durabilidade."},
    "Alpha's Cleaver": {"dano": 75, "durabilidade": 15, "tipo": "Axe"},
    # Armaduras
    "Leather Armor": {"preço": 25, "armadura": 5, "tipo": "Armor"},
    "Chainmail Armor": {"preço": 50, "armadura": 10, "tipo": "Armor"},
    "Bronze Armor": {"preço": 75, "armadura": 15, "tipo": "Armor"},
    "Steel Armor": {"preço": 100, "armadura": 25, "tipo": "Armor"},
    "Dragon's Scale Armor": {"preço": 150, "armadura": 50, "tipo": "Armor"},
    # Comidas
    "Cookie": {"preço": 5, "cura": 15},
    "Bread": {"preço": 15, "cura": 30},
    "Cake": {"preço": 25, "cura": 50},
    "Apple Pie": {"preço": 40, "cura": 75}
}

# Listas com os possíveis itens que a loja pode sortear.
# Armas e comidas são sorteadas aleatoriamente a cada visita/compra.
estoque_armas = ["Wooden Sword", "Stone Sword", "Iron Sword", "Diamond Sword", "Soul Reaver",
                 "Wooden Bow", "Hunter Bow", "Bone Bow", "Shadow Bow", "Soulseeker",
                 "Wooden Axe", "Stone Axe", "Iron Axe", "Diamond Axe", "Soul Cleaver"]
estoque_comidas = ["Cookie", "Bread", "Cake", "Apple Pie"]
# As armaduras NÃO são sorteadas: seguem uma ordem fixa (da mais fraca para a mais forte),
# e o índice da próxima armadura à venda é controlado pela variável 'id_armadura'.
estoque_armaduras = ["Leather Armor", "Chainmail Armor", "Bronze Armor", "Steel Armor", "Dragon's Scale Armor"]

# Dicionário com todos os monstros comuns (bosses e minibosses não incluídos).
# Atributos: "hp" (vida), "dano" (dano causado ao jogador por turno) e "ouro" (recompensa).
tabela_monstros = {
    "Esqueleto": {"hp": 40, "dano": 15, "ouro": 25},
    "Goblin": {"hp": 30, "dano": 10, "ouro": 15},
    "Lobo": {"hp": 20, "dano": 20, "ouro": 20},
    "Orc": {"hp": 50, "dano": 25, "ouro": 30},
    "Rato Gigante": {"hp": 15, "dano": 10, "ouro": 5},
    "Slime": {"hp": 25, "dano": 5, "ouro": 5},
    "Zumbi": {"hp": 30, "dano": 20, "ouro": 25}
}

# Dicionário com todos os minibosses (aparecem a cada 5 ondas).
tabela_minibosses = {
    "Dragãozinho": {"hp": 80, "dano": 30, "ouro": 50},
    "Lobisomem": {"hp": 70, "dano": 40, "ouro": 50},
    "Vampiro": {"hp": 75, "dano": 35, "ouro": 50}
}

# Dicionário com todos os bosses (aparecem a cada 10 ondas).
# Cada boss derrotado dropa uma arma exclusiva (ver 'checar_fim_turno').
tabela_bosses = {
    "Dragão": {"hp": 125, "dano": 50, "ouro": 100},
    "Lobisomem Alfa": {"hp": 100, "dano": 75, "ouro": 100},
    "Vampiro Rei": {"hp": 110, "dano": 65, "ouro": 100}
}

# Dicionário com o chefão final (aparece a cada 100 ondas).
tabela_bossfinal = {
    "The Soul Reaper": {"hp": 2500, "dano": 250, "ouro": 10000}
}

# ==========================================
# 2. VARIÁVEIS DE ESTADO
# ==========================================
# Lista que armazena os itens do jogador. Cada item é um dicionário:
#   arma   -> {"nome": ..., "durabilidade": ...}  (a durabilidade é individual de cada exemplar)
#   comida -> {"nome": ...}
mochila = []
# Fila com os nomes dos monstros que ainda vão ser enfrentados na onda atual.
monstros = []

# Variáveis com atributos do jogador.
player_hp = 100
player_gold = 50
player_armor = 0       # Armadura base, comprada na loja.
player_class = ""      # "Warrior", "Archer" ou "Berserker".
hp_perdido = 0         # HP perdido na onda atual (alimenta a passiva e a habilidade do Berserker).

# Variáveis com atributos do jogo.
onda = 1
quantidade_monstros = 1   # Quantos monstros aparecem por onda (+1 a cada boss derrotado).
id_armadura = 0           # Índice da próxima armadura disponível em 'estoque_armaduras'.

# Variáveis do estado de combate atual.
monstro_nome_atual = ""
monstro_tipo_atual = ""        # "Monstro", "Miniboss", "Boss" ou "Boss Supremo".
monstro_hp_max = 0
monstro_hp_atual = 0
monstro_dano_atual = 0
monstro_ouro_atual = 0
habilidade_disponivel = True   # A habilidade especial só pode ser usada uma vez por onda.
# Itens atualmente sorteados na loja (guardados para a compra saber o que foi exibido).
item_arma_loja = None
item_comida_loja = None

# Histórico do log
historico_log = []

# ==========================================
# 3. FUNÇÕES AUXILIARES DE INTERFACE
# ==========================================
# Adiciona uma mensagem ao log da tela.
# Mostra apenas as 30 últimas mensagens e rola o contêiner para o fim automaticamente.
def atualizar_log(mensagem):
    historico_log.append(mensagem)
    log_elem = document.querySelector("#log-texto")
    if log_elem:
        log_elem.innerHTML = "<br>".join(historico_log[-30:])
    container = document.querySelector("#log-container")
    if container:
        container.scrollTop = container.scrollHeight

# Controla qual "tela" está visível.
# Esconde todas as telas da lista e exibe somente a tela cujo seletor foi passado.
def mostrar_tela(id_tela):
    telas = [".class_selection", "#menu-principal", "#menu-luta", "#menu-loja", "#menu-mochila", "#tela-final"]
    for tela in telas:
        elem = document.querySelector(tela)
        if elem:
            elem.style.display = "none"
    if id_tela:
        tela_alvo = document.querySelector(id_tela)
        if tela_alvo:
            tela_alvo.style.display = "block"

# Exibe a tela final (fim de jogo ou saída) com o título recebido.
def mostrar_fim(titulo):
    elem = document.querySelector("#msg-final")
    if elem:
        elem.innerText = titulo
    mostrar_tela("#tela-final")

# Reinicia o jogo recarregando a página inteira (botão "Jogar novamente").
def reiniciar_jogo(event):
    window.location.reload()

# Retorna a armadura total do jogador.
# O Warrior recebe +5 de armadura por monstro da onda (habilidade passiva).
def get_armadura_efetiva():
    if player_class == "Warrior":
        return player_armor + (quantidade_monstros * 5)
    return player_armor

# Atualiza os dados do jogador exibidos no menu principal (classe, HP, armadura, ouro e onda).
def atualizar_status_menu():
    document.querySelector("#info-classe").innerText = player_class
    document.querySelector("#info-hp").innerText = str(player_hp)
    document.querySelector("#info-armadura").innerText = str(get_armadura_efetiva())
    document.querySelector("#info-ouro").innerText = str(player_gold)
    document.querySelector("#info-onda").innerText = str(onda)

# Função para adicionar itens à mochila.
# Armas guardam a durabilidade individual; comidas guardam apenas o nome.
# Obs.: diferente do terminal, armaduras compradas não vão para a mochila (apenas definem 'player_armor').
def adicionar_item_mochila(nome_item):
    if "dano" in tabela_itens[nome_item]:
        mochila.append({
            "nome": nome_item,
            "durabilidade": tabela_itens[nome_item]["durabilidade"]
        })
    else:
        mochila.append({"nome": nome_item})

# ==========================================
# 4. SELEÇÃO DE CLASSE E NAVEGAÇÃO
# ==========================================
# Cada função de escolha de classe (chamada pelo clique no botão da classe):
#   1. Define a classe e o HP inicial;
#   2. Adiciona a arma inicial e 4 Cookies na mochila;
#   3. Registra no log, atualiza o status e abre o menu principal.

# Warrior: 100 HP, Wooden Sword.
def escolher_warrior(event):
    global player_class, player_hp
    player_class = "Warrior"
    player_hp = 100
    adicionar_item_mochila("Wooden Sword")
    for _ in range(4):
        adicionar_item_mochila("Cookie")
    atualizar_log("⚔️ Você escolheu Warrior! Pronto para proteger o reino.")
    atualizar_status_menu()
    mostrar_tela("#menu-principal")

# Archer: 75 HP, Wooden Bow.
def escolher_archer(event):
    global player_class, player_hp
    player_class = "Archer"
    player_hp = 75
    adicionar_item_mochila("Wooden Bow")
    for _ in range(4):
        adicionar_item_mochila("Cookie")
    atualizar_log("🏹 Você escolheu Archer! Suas flechas vão chover sobre os monstros.")
    atualizar_status_menu()
    mostrar_tela("#menu-principal")

# Berserker: 125 HP, Wooden Axe.
def escolher_berserker(event):
    global player_class, player_hp
    player_class = "Berserker"
    player_hp = 125
    adicionar_item_mochila("Wooden Axe")
    for _ in range(4):
        adicionar_item_mochila("Cookie")
    atualizar_log("🪓 Você escolheu Berserker! O sangue e a fúria guiam sua lâmina.")
    atualizar_status_menu()
    mostrar_tela("#menu-principal")

# Abre a loja: sorteia os itens à venda e exibe a tela da loja.
def abrir_loja(event):
    atualizar_log("🛒 Bem-vindo à loja! Escolha suas compras.")
    gerar_itens_loja()
    mostrar_tela("#menu-loja")

# Abre a mochila: monta a lista de itens e exibe a tela da mochila.
def abrir_mochila(event):
    atualizar_log("🎒 Visualizando inventário da mochila.")
    renderizar_mochila()
    mostrar_tela("#menu-mochila")

# Volta ao menu principal (usada ao sair da loja, da mochila, ao fugir e ao vencer uma onda).
def voltar_menu_principal(event):
    atualizar_status_menu()
    mostrar_tela("#menu-principal")

# Encerra o jogo e mostra a tela final de agradecimento.
def sair_jogo(event):
    atualizar_log("👋 Obrigado por jogar Pocket Hero!")
    mostrar_fim("Obrigado por jogar Pocket Hero!")

# ==========================================
# 5. SISTEMA DA LOJA
# ==========================================
# Sorteia e exibe os itens da loja: 1 arma aleatória, 1 comida aleatória e a próxima armadura da fila.
# É chamada ao abrir a loja e após cada compra (o que renova o sorteio de arma e comida).
def gerar_itens_loja():
    global item_arma_loja, item_comida_loja
    document.querySelector("#player_gold").innerText = str(player_gold)

    # Soteia os itens da loja.
    item_arma_loja = random.choice(estoque_armas)
    item_comida_loja = random.choice(estoque_comidas)

    # Slot 1: arma (mostra tipo, preço, dano, durabilidade e descrição).
    d_arma = tabela_itens[item_arma_loja]
    document.querySelector("#item1").innerText = item_arma_loja
    document.querySelector("#item1_tipo").innerText = f"({d_arma['tipo']})"
    document.querySelector("#preco1").innerText = str(d_arma["preço"])
    document.querySelector("#item1_dano").innerText = str(d_arma["dano"])
    document.querySelector("#item1_durabilidade").innerText = str(d_arma["durabilidade"])
    document.querySelector("#item1_descricao").innerText = d_arma.get("descrição", "Item sem descrição.")

    # Slot 2: comida (mostra preço e cura).
    d_comida = tabela_itens[item_comida_loja]
    document.querySelector("#item2").innerText = item_comida_loja
    document.querySelector("#preco2").innerText = str(d_comida["preço"])
    document.querySelector("#item2_cura").innerText = str(d_comida["cura"])

    # Slot 3: armadura. Se todas já foram compradas, mostra o aviso de estoque esgotado.
    if id_armadura < len(estoque_armaduras):
        nome_arm = estoque_armaduras[id_armadura]
        d_arm = tabela_itens[nome_arm]
        document.querySelector("#item3").innerText = nome_arm
        document.querySelector("#preco3").innerText = str(d_arm["preço"])
        document.querySelector("#valor_armadura").innerText = str(d_arm["armadura"])
    else:
        document.querySelector("#item3").innerText = "Armadura Máxima Adquirida"
        document.querySelector("#preco3").innerText = "(Esgotado)"
        document.querySelector("#valor_armadura").innerText = "MAX"

# Compra a arma exibida no slot 1: desconta o ouro, adiciona à mochila e renova a loja.
def comprar_arma(event):
    global player_gold
    preco = tabela_itens[item_arma_loja]["preço"]
    if player_gold >= preco:
        player_gold -= preco
        adicionar_item_mochila(item_arma_loja)
        atualizar_log(f"✅ Comprou {item_arma_loja} com sucesso!")
        gerar_itens_loja()
    else:
        atualizar_log("❌ Ouro insuficiente!")

# Compra a comida exibida no slot 2: desconta o ouro, adiciona à mochila e renova a loja.
def comprar_comida(event):
    global player_gold
    preco = tabela_itens[item_comida_loja]["preço"]
    if player_gold >= preco:
        player_gold -= preco
        adicionar_item_mochila(item_comida_loja)
        atualizar_log(f"✅ Comprou {item_comida_loja} com sucesso!")
        gerar_itens_loja()
    else:
        atualizar_log("❌ Ouro insuficiente!")

# Compra a próxima armadura da fila (slot 3).
# A nova armadura SUBSTITUI a anterior (player_armor recebe o novo valor, não soma),
# e o índice 'id_armadura' avança para a armadura seguinte.
def comprar_armadura(event):
    global player_gold, player_armor, id_armadura
    if id_armadura < len(estoque_armaduras):
        nome_arm = estoque_armaduras[id_armadura]
        preco = tabela_itens[nome_arm]["preço"]
        if player_gold >= preco:
            player_gold -= preco
            player_armor = tabela_itens[nome_arm]["armadura"]
            id_armadura += 1
            atualizar_log(f"🛡️ Comprou {nome_arm}! Armadura base agora é {player_armor}.")
            gerar_itens_loja()
        else:
            atualizar_log("❌ Ouro insuficiente!")
    else:
        atualizar_log("❌ Estoque de armaduras esgotado!")

# ==========================================
# 6. MOCHILA / INVENTÁRIO
# ==========================================
# Monta na tela a lista de itens da mochila.
# Para cada item cria um <div> com as informações:
#   - armas: tipo, dano, durabilidade atual e descrição (se houver);
#   - comidas: quantidade de cura.
def renderizar_mochila():
    container = document.querySelector("#lista-mochila")
    container.innerHTML = ""
    if not mochila:
        container.innerHTML = "<p>Sua mochila está vazia!</p>"
        return

    for i, item in enumerate(mochila, start=1):
        nome = item["nome"]
        div = document.createElement("div")
        div.className = "loja-item"

        # Verifica se o item é uma arma
        if "dano" in tabela_itens[nome]:
            dano = tabela_itens[nome]["dano"]
            dur = item["durabilidade"]
            tipo = tabela_itens[nome]["tipo"]
            desc = tabela_itens[nome].get("descrição", "")
            html = f"<p><strong>[{i}] {nome}</strong> ({tipo})</p>" \
                   f"<p>⚔️ Dano: {dano} | 🛡️ Durabilidade: {dur}</p>"
            if desc:
                html += f"<p>ℹ️ {desc}</p>"
            div.innerHTML = html
        # Se não for arma, é comida
        else:
            cura = tabela_itens[nome]["cura"]
            div.innerHTML = f"<p><strong>[{i}] {nome}</strong> (Comida)</p>" \
                            f"<p>❤️ Cura: {cura}</p>"
        container.appendChild(div)

# ==========================================
# 7. SISTEMA DE COMBATE
# ==========================================
# Função que define qual tabela usar pra geração de monstros dependendo da onda atual.
#   Onda múltipla de 100 -> Boss Supremo
#   Onda múltipla de 10  -> Boss
#   Onda múltipla de 5   -> Miniboss
#   Demais ondas         -> Monstro comum
def obter_tabela_atual():
    if onda % 100 == 0:
        return tabela_bossfinal, "Boss Supremo"
    elif onda % 10 == 0:
        return tabela_bosses, "Boss"
    elif onda % 5 == 0:
        return tabela_minibosses, "Miniboss"
    else:
        return tabela_monstros, "Monstro"

# Inicia uma onda (botão "Enfrentar Monstro").
# Reseta o HP perdido e a habilidade especial, sorteia os monstros da onda e inicia o primeiro combate.
# Em ondas de miniboss/boss (múltiplas de 5) aparece apenas 1 inimigo; nas demais, 'quantidade_monstros'.
def iniciar_combate_menu(event):
    global monstros, habilidade_disponivel, hp_perdido
    monstros.clear()
    hp_perdido = 0
    habilidade_disponivel = True

    tabela, tipo = obter_tabela_atual()

    if onda % 5 == 0:
        qtd = 1
    else:
        qtd = quantidade_monstros

    for _ in range(qtd):
        m = random.choice(list(tabela.keys()))
        monstros.append(m)

    atualizar_log(f"⚔️ A onda {onda} começou com {len(monstros)} inimigo(s)!")
    esconder_selecao_combate()
    proximo_monstro()

# Retira o próximo monstro da fila e prepara o combate contra ele.
# Se a fila estiver vazia, a onda foi vencida.
# Também aplica o escalonamento de dificuldade:
#   - HP:   minibosses e bosses multiplicam o HP por 'quantidade_monstros';
#           monstros comuns ganham +5 de HP por monstro extra (após a onda 10).
#   - Dano: bosses ganham +25, minibosses +10 e monstros +5 por monstro extra (após a onda 10).
def proximo_monstro():
    global monstro_nome_atual, monstro_tipo_atual, monstro_hp_atual, monstro_hp_max, monstro_dano_atual, monstro_ouro_atual

    if len(monstros) == 0:
        vitoria_onda()
        return

    tabela, monstro_tipo_atual = obter_tabela_atual()
    monstro_nome_atual = monstros.pop(0)

    # Puxa os atributos usando a tabela escolhida
    hp = tabela[monstro_nome_atual]["hp"]
    dano = tabela[monstro_nome_atual]["dano"]
    ouro = tabela[monstro_nome_atual]["ouro"]

    # Aumenta o HP dos monstros ao passar das ondas
    if monstro_tipo_atual in ["Miniboss", "Boss"]:
        hp *= quantidade_monstros
    elif monstro_tipo_atual == "Monstro" and onda > 10:
        hp += (quantidade_monstros - 1) * 5

    # Aumenta o dano dos monstros ao passar das ondas
    if monstro_tipo_atual == "Boss" and onda > 10:
        dano += (quantidade_monstros - 1) * 25
    elif monstro_tipo_atual == "Miniboss" and onda > 10:
        dano += (quantidade_monstros - 1) * 10
    elif monstro_tipo_atual == "Monstro" and onda > 10:
        dano += (quantidade_monstros - 1) * 5

    # Guarda os atributos finais do monstro nas variáveis globais do combate atual.
    monstro_hp_atual = hp
    monstro_hp_max = hp
    monstro_dano_atual = dano
    monstro_ouro_atual = ouro

    atualizar_interface_combate()
    mostrar_tela("#menu-luta")

# Atualiza todos os textos da tela de luta: tipo/nome/HP/dano do monstro, número da onda,
# monstros restantes, HP e armadura do jogador e nome/estado da habilidade especial.
# (Cada elemento é verificado com 'if' para não gerar erro caso ele não exista no HTML.)
def atualizar_interface_combate():
    elem_tipo = document.querySelector("#tipo")
    if elem_tipo:
        elem_tipo.innerText = monstro_tipo_atual

    elem_monstro_titulo = document.querySelector("#monstro_atual_titulo")
    if elem_monstro_titulo:
        elem_monstro_titulo.innerText = monstro_nome_atual

    elem_hp_titulo = document.querySelector("#hp_monstro_titulo")
    if elem_hp_titulo:
        elem_hp_titulo.innerText = str(monstro_hp_max)

    elem_dano_titulo = document.querySelector("#dano_monstro_titulo")
    if elem_dano_titulo:
        elem_dano_titulo.innerText = str(monstro_dano_atual)

    elem_luta_onda = document.querySelector("#luta-onda")
    if elem_luta_onda:
        elem_luta_onda.innerText = str(onda)

    elem_monstros_restantes = document.querySelector("#monstros-restantes")
    if elem_monstros_restantes:
        elem_monstros_restantes.innerText = str(len(monstros) + 1)

    # O HP nunca é exibido abaixo de 0.
    elem_player_hp = document.querySelector("#player_hp")
    if elem_player_hp:
        elem_player_hp.innerText = str(max(0, player_hp))

    elem_hp_monstro = document.querySelector("#hp_monstro")
    if elem_hp_monstro:
        elem_hp_monstro.innerText = str(max(0, monstro_hp_atual))

    elem_player_armor = document.querySelector("#player_armor")
    if elem_player_armor:
        elem_player_armor.innerText = str(get_armadura_efetiva())

    # Nome da habilidade especial de acordo com a classe.
    nome_hab = "Retaliação de Escudo" if player_class == "Warrior" else "Chuva de Flechas" if player_class == "Archer" else "Grito de Fúria"

    elem_nome_hab = document.querySelector("#nome-habilidade")
    if elem_nome_hab:
        elem_nome_hab.innerText = nome_hab

    elem_status_hab = document.querySelector("#status-habilidade")
    if elem_status_hab:
        elem_status_hab.innerText = "(Disponível)" if habilidade_disponivel else "(Usada)"

# Esconde o painel de seleção de itens (armas/comidas) da tela de luta.
def esconder_selecao_combate():
    container = document.querySelector("#selecao-item-combate")
    if container:
        container.style.display = "none"

# Botão "Atacar": lista as armas da mochila como botões.
# Ao clicar em uma arma, 'executar_ataque' é chamada com aquela arma específica.
def abrir_selecao_armas(event):
    container = document.querySelector("#selecao-item-combate")
    lista = document.querySelector("#lista-itens-combate")
    document.querySelector("#titulo-selecao").innerText = "Escolha uma arma para atacar:"
    lista.innerHTML = ""

    # Armas são os itens que possuem durabilidade.
    armas = [item for item in mochila if "durabilidade" in item]
    if not armas:
        atualizar_log("❌ Você não tem armas na mochila!")
        return

    for item in armas:
        nome = item["nome"]
        tipo = tabela_itens[nome]["tipo"]
        dano = tabela_itens[nome]["dano"]
        dur = item["durabilidade"]

        btn = document.createElement("button")
        btn.innerText = f"{nome} [{tipo}] (Dano: {dano} | Dur: {dur})"

        # 'arma_ref=item' fixa a arma deste botão (evita que todos os botões usem a última arma do loop).
        def realizar_ataque(e, arma_ref=item):
            executar_ataque(arma_ref)

        btn.onclick = realizar_ataque
        lista.appendChild(btn)

    container.style.display = "block"

# Executa o ataque do jogador com a arma escolhida.
#   - Berserker: +5 de dano a cada 20 de HP perdido na onda (passiva).
#   - Arcos: disparam 2 vezes (3 para o Archer) e gastam 2 de durabilidade.
#   - Vampiric Blade: cura 5 de HP a cada golpe.
#   - A arma perde 1 de durabilidade por ataque e é removida da mochila ao quebrar.
# Ao final, passa a vez para o monstro em 'checar_fim_turno'.
def executar_ataque(arma_escolhida):
    global monstro_hp_atual, player_hp
    esconder_selecao_combate()

    # Pega o dano da arma e ataca
    nome_arma = arma_escolhida["nome"]
    tipo_arma = tabela_itens[nome_arma]["tipo"]
    dano_player = tabela_itens[nome_arma]["dano"]

    # Passiva do Berserker
    if player_class == "Berserker":
        furia = (hp_perdido // 20) * 5
        dano_player += furia

    # Armas que não são arcos atacam uma vez; arcos atacam várias vezes.
    if tipo_arma != "Bow":
        dano_total = dano_player
    else:
        disparos = 3 if player_class == "Archer" else 2
        dano_total = dano_player * disparos

    monstro_hp_atual -= dano_total

    if nome_arma == "Vampiric Blade":
        player_hp += 5

    # Reduz a durabilidade da arma (arcos gastam 1 extra)
    arma_escolhida["durabilidade"] -= 1
    if tipo_arma == "Bow":
        arma_escolhida["durabilidade"] = max(0, arma_escolhida["durabilidade"] - 1)

    msg = f"⚔️ Atacou {monstro_nome_atual} com {nome_arma} e causou {dano_total} de dano!"
    # Se a durabilidade zerar, a arma quebra e some da mochila
    if arma_escolhida["durabilidade"] <= 0:
        msg += f" 💥 {nome_arma} quebrou!"
        mochila.remove(arma_escolhida)

    atualizar_log(msg)
    checar_fim_turno()

# Botão "Usar item de cura": lista as comidas da mochila como botões.
# Ao clicar em uma comida, 'executar_cura' é chamada com aquele item específico.
def abrir_selecao_comidas(event):
    container = document.querySelector("#selecao-item-combate")
    lista = document.querySelector("#lista-itens-combate")
    document.querySelector("#titulo-selecao").innerText = "Escolha uma comida para consumir:"
    lista.innerHTML = ""

    # Comidas são os itens que possuem "cura" na tabela de itens.
    comidas = [item for item in mochila if "cura" in tabela_itens[item["nome"]]]
    if not comidas:
        atualizar_log("❌ Você não tem comidas na mochila!")
        return

    for item in comidas:
        nome = item["nome"]
        cura = tabela_itens[nome]["cura"]

        btn = document.createElement("button")
        btn.innerText = f"{nome} (+{cura} HP)"

        # 'comida_ref=item' fixa a comida deste botão (mesma técnica usada nas armas).
        def realizar_cura(e, comida_ref=item):
            executar_cura(comida_ref)

        btn.onclick = realizar_cura
        lista.appendChild(btn)

    container.style.display = "block"

# Consome a comida escolhida: recupera o HP (sem limite máximo) e remove o item da mochila.
# Usar um item também gasta o turno, então o monstro revida em 'checar_fim_turno'.
def executar_cura(comida_escolhida):
    global player_hp
    esconder_selecao_combate()

    nome_comida = comida_escolhida["nome"]
    cura_player = tabela_itens[nome_comida]["cura"]
    player_hp += cura_player
    mochila.remove(comida_escolhida)

    atualizar_log(f"✨ Comeu {nome_comida} e recuperou {cura_player} de HP!")
    checar_fim_turno()

# Botão "Usar Habilidade Especial" (uma vez por onda). Efeito de cada classe:
#   - Warrior:   Retaliação de Escudo -> dano igual a 2x a armadura total.
#   - Archer:    Chuva de Flechas     -> 30 de dano por monstro na onda.
#   - Berserker: Grito de Fúria       -> soma 40 de "HP perdido" por monstro (equivale a +10 de dano por monstro).
def usar_habilidade(event):
    global habilidade_disponivel, monstro_hp_atual, hp_perdido
    # Se a habilidade special já foi usada.
    if not habilidade_disponivel:
        atualizar_log("⚠️ Habilidade Especial já utilizada nesta onda!")
        return

    esconder_selecao_combate()
    habilidade_disponivel = False

    # Habilidade do Warrior.
    if player_class == "Warrior":
        dano = get_armadura_efetiva() * 2
        monstro_hp_atual -= dano
        atualizar_log(f"🛡️ Retaliação de Escudo causou {dano} de dano em {monstro_nome_atual}!")
    # Habilidade do Archer.
    elif player_class == "Archer":
        dano = 30 * quantidade_monstros
        monstro_hp_atual -= dano
        atualizar_log(f"🏹 Chuva de Flechas causou {dano} de dano em {monstro_nome_atual}!")
    # Habilidade do Berserker.
    elif player_class == "Berserker":
        hp_perdido += 40 * quantidade_monstros
        atualizar_log(f"🪓 Grito de Fúria! Seu dano aumentou em +{10 * quantidade_monstros} até o fim da onda!")

    checar_fim_turno()

# Botão "Tentar fugir": limpa a fila de monstros e volta ao menu principal.
# A fuga sempre funciona e a onda não avança.
def fugir_combate(event):
    global monstros
    monstros.clear()
    esconder_selecao_combate()
    atualizar_log("🏃 Você fugiu da batalha com sucesso!")
    voltar_menu_principal(event)

# Chamada ao final de toda ação do jogador (ataque, cura ou habilidade). Resolve o resto do turno:
#   1. Se o monstro morreu: dá o ouro, entrega o drop do boss (se houver) e chama o próximo monstro.
#   2. Se ainda está vivo: o monstro revida (dano - armadura, mínimo 0).
#   3. Se o HP do jogador chegou a 0: mostra a tela de fim de jogo.
def checar_fim_turno():
    global player_hp, hp_perdido, player_gold

    # Resultado do combate: vitória sobre o monstro atual
    if monstro_hp_atual <= 0:
        atualizar_log(f"🎉 Derrotou {monstro_nome_atual}! Ganhou {monstro_ouro_atual} de ouro!")
        player_gold += monstro_ouro_atual

        # Drops de Bosses
        if monstro_nome_atual == "The Soul Reaper":
            adicionar_item_mochila("Soul Reaper")
            atualizar_log("☠️ A mítica Soul Reaper foi adicionada à sua mochila...")
        elif monstro_nome_atual == "Vampiro Rei":
            adicionar_item_mochila("Vampiric Blade")
            atualizar_log("🧛 A lendária Vampiric Blade foi adicionada à sua mochila...")
        elif monstro_nome_atual == "Dragão":
            adicionar_item_mochila("Dragon Bow")
            atualizar_log("🐉 O poderoso Dragon Bow foi adicionado à sua mochila...")
        elif monstro_nome_atual == "Lobisomem Alfa":
            adicionar_item_mochila("Alpha's Cleaver")
            atualizar_log("🐺 O devastador Alpha's Cleaver foi adicionado à sua mochila...")

        proximo_monstro()
        return

    # Turno do monstro
    # Registra o dano reduzido pela armadura (nunca menor que 0)
    dano_recebido = max(0, monstro_dano_atual - get_armadura_efetiva())
    player_hp -= dano_recebido
    hp_perdido += dano_recebido

    # Envia pro log o dano recebido.
    atualizar_log(f"💥 {monstro_nome_atual} retaliou e causou {dano_recebido} de dano!")

    atualizar_interface_combate()

    # Derrota do jogador
    if player_hp <= 0:
        player_hp = 0
        atualizar_log(f"💀 Você foi derrotado na Onda {onda}... Fim de jogo!")
        mostrar_fim("Fim de Jogo! Seu Herói Tombou em Combate.")

# Chamada quando todos os monstros da onda foram derrotados.
# Reseta o HP perdido (usado pelo Berserker) e avança a onda.
# Se a onda era de boss (múltipla de 10), 'quantidade_monstros' aumenta em 1,
#   fazendo as próximas ondas terem hordas maiores. Depois volta ao menu principal.
def vitoria_onda():
    global onda, quantidade_monstros, hp_perdido
    hp_perdido = 0

    # Verifica se o monstro derrotado foi um boss
    if onda % 10 == 0:
        quantidade_monstros += 1
        atualizar_log(f"🔥 Boss Derrotado! Agora hordas de {quantidade_monstros} monstros vão aparecer!")
    else:
        atualizar_log(f"🏆 Onda {onda} concluída com vitória!")

    onda += 1
    voltar_menu_principal(None)

# ==========================================
# 8. VINCULAR EVENTOS E INICIALIZAR
# ==========================================
# Liga cada botão do HTML (pelo id) à função Python correspondente.

# Seleção de classe
document.querySelector("#btn-warrior").onclick = escolher_warrior
document.querySelector("#btn-archer").onclick = escolher_archer
document.querySelector("#btn-berserker").onclick = escolher_berserker

# Navegação do menu principal
document.querySelector("#btn-ir-loja").onclick = abrir_loja
document.querySelector("#btn-ver-mochila").onclick = abrir_mochila
document.querySelector("#btn-sair-loja").onclick = voltar_menu_principal
document.querySelector("#btn-sair-mochila").onclick = voltar_menu_principal
document.querySelector("#btn-sair-jogo").onclick = sair_jogo
document.querySelector("#btn-reiniciar").onclick = reiniciar_jogo

# Compras na loja
document.querySelector("#btn-comprar-arma").onclick = comprar_arma
document.querySelector("#btn-comprar-comida").onclick = comprar_comida
document.querySelector("#btn-comprar-armadura").onclick = comprar_armadura

# Ações de combate
document.querySelector("#btn-enfrentar-monstro").onclick = iniciar_combate_menu
document.querySelector("#btn-atacar").onclick = abrir_selecao_armas
document.querySelector("#btn-usar-cura").onclick = abrir_selecao_comidas
document.querySelector("#btn-habilidade").onclick = usar_habilidade
document.querySelector("#btn-fugir").onclick = fugir_combate