# Importa o NumPy para manipulação de vetores e matrizes numéricas
import numpy as np
# Importa a função 'root' do SciPy para resolver sistemas de equações algébricas não-lineares
from scipy.optimize import root

# Exibe o cabeçalho visual do simulador no terminal
print("=" * 75)
# Exibe o título principal do programa com foco em Graus de Liberdade
print("SIMULADOR GENÉRICO DE DESTILAÇÃO BINÁRIA (9 VARIÁVEIS / 4 GRAUS DE LIBERDADE)")
# Exibe a linha divisória do cabeçalho
print("=" * 75)
# Orienta o usuário sobre como preencher apenas as 4 variáveis conhecidas
print("Instruções:")
print("1. O sistema possui 9 variáveis e 5 equações independentes (GdL = 4).")
print("2. Digite o valor de EXATAMENTE 4 variáveis e pressione [ENTER] nas outras 5.")
print("3. Para rodar o exemplo padrão (F=1000, xF=0.12, xD=0.85, xB=0.005),")
print("   basta pressionar [ENTER] em todas as perguntas.\n")

# Define a lista ordenada com os nomes internos das 9 variáveis do processo
nomes_variaveis = ["F", "D", "B", "xF", "wF", "xD", "wD", "xB", "wB"]

# Define um dicionário com a descrição amigável de cada variável para exibir no input
descricoes = {
    "F":  "Vazão mássica de Alimentação F [kg/h]",
    "D":  "Vazão mássica de Destilado/Topo D [kg/h]",
    "B":  "Vazão mássica de Fundo/Resíduo B [kg/h]",
    "xF": "Fração mássica de Etanol na Alimentação (xF)",
    "wF": "Fração mássica de Água na Alimentação (wF)",
    "xD": "Fração mássica de Etanol no Destilado (xD)",
    "wD": "Fração mássica de Água no Destilado (wD)",
    "xB": "Fração mássica de Etanol no Fundo (xB)",
    "wB": "Fração mássica de Água no Fundo (wB)"
}

# Cria um dicionário vazio para armazenar os valores informados pelo usuário (None = incógnita)
especificacoes = {}

# Percorre cada uma das 9 variáveis solicitando a entrada do usuário no console
for var in nomes_variaveis:
    # Lê a resposta do usuário como texto e remove espaços em branco nas pontas
    entrada = input(f"Informe {descricoes[var]:45s}: ").strip()
    # Verifica se o usuário digitou algum número ou se deixou em branco
    if entrada != "":
        # Converte o texto digitado (trocando vírgula por ponto, se houver) para float
        especificacoes[var] = float(entrada.replace(",", "."))
    else:
        # Marca a variável como None (incógnita a ser calculada pelo Python)
        especificacoes[var] = None

# Conta quantas variáveis foram efetivamente preenchidas pelo usuário
qtd_informada = sum(1 for valor in especificacoes.values() if valor is not None)

# Se o usuário apertou ENTER em todas as 9 perguntas, carrega o caso padrão automaticamente
if qtd_informada == 0:
    # Informa ao usuário que o caso base da aula foi carregado por padrão
    print("\n[AVISO]: Nenhuma variável digitada. Carregando as 4 especificações padrão...")
    # Define F = 1000 kg/h como especificação padrão
    especificacoes["F"] = 1000.0
    # Define xF = 0.12 como especificação padrão
    especificacoes["xF"] = 0.12
    # Define xD = 0.85 como especificação padrão
    especificacoes["xD"] = 0.85
    # Define xB = 0.005 como especificação padrão
    especificacoes["xB"] = 0.005
    # Atualiza o contador de variáveis informadas para 4
    qtd_informada = 4


# ==============================================================================
# ETAPA 1: VALIDAÇÃO DOS GRAUS DE LIBERDADE E DEPENDÊNCIA LINEAR (PRÉ-SOLVER)
# ==============================================================================

# Cria uma variável booleana para controlar se os dados passaram em todos os testes
dados_validos = True

# RESTRIÇÃO 1: Verifica se o número de variáveis especificadas é exatamente 4
if qtd_informada != 4:
    # Exibe erro explicando se o sistema está sub-especificado (<4) ou sobre-especificado (>4)
    print(f"\n[ERRO DE GRAUS DE LIBERDADE]: Você informou {qtd_informada} variáveis.")
    print("Para resolver as 9 variáveis com 5 equações, informe EXATAMENTE 4 variáveis.")
    # Invalida a execução do cálculo
    dados_validos = False

# RESTRIÇÃO 2: Verifica se pelo menos uma vazão mássica (F, D ou B) foi informada (Base de Cálculo)
if dados_validos and (especificacoes["F"] is None and especificacoes["D"] is None and especificacoes["B"] is None):
    # Exibe erro caso o usuário tenha informado apenas 4 frações mássicas e nenhuma vazão
    print("\n[ERRO DE BASE DE CÁLCULO]: Você informou apenas composições (frações mássicas).")
    print("É obrigatório informar pelo menos UMA vazão mássica (F, D ou B) para dimensionar as correntes.")
    # Invalida a execução do cálculo
    dados_validos = False

# RESTRIÇÃO 3: Verifica se o usuário informou F, D e B ao mesmo tempo (dependentes pelo Balanço Global)
if dados_validos and (especificacoes["F"] is not None and especificacoes["D"] is not None and especificacoes["B"] is not None):
    # Verifica se F = D + B foi violado diretamente pelo usuário
    if abs(especificacoes["F"] - (especificacoes["D"] + especificacoes["B"])) > 1e-5:
        # Exibe erro de violação da conservação da massa global
        print("\n[ERRO NO BALANÇO GLOBAL]: Você informou F, D e B, mas F != D + B!")
    else:
        # Exibe erro de redundância (informar F, D e B gasta apenas 2 graus de liberdade reais, faltando 1 composição)
        print("\n[ERRO DE DEPENDÊNCIA LINEAR]: Como F = D + B, você não pode escolher as 3 vazões livremente.")
        print("Informe no máximo 2 vazões globais e complete as 4 especificações com frações mássicas.")
    # Invalida a execução do cálculo
    dados_validos = False

# RESTRIÇÃO 4: Verifica se o usuário informou x e w da mesma corrente simultaneamente
pares_correntes = [("xF", "wF", "Alimentação"), ("xD", "wD", "Destilado"), ("xB", "wB", "Fundo")]
# Percorre os 3 pares (Alimentação, Destilado e Fundo) para checar redundância de composição
for var_x, var_w, nome_corrente in pares_correntes:
    # Se tanto a fração de etanol quanto a de água da mesma corrente foram digitadas
    if dados_validos and (especificacoes[var_x] is not None and especificacoes[var_w] is not None):
        # Exibe erro explicando que x + w = 1 já faz parte das 5 equações do modelo
        print(f"\n[ERRO DE DEPENDÊNCIA LINEAR]: Você informou {var_x} e {var_w} na corrente de {nome_corrente}.")
        print(f"Como {var_x} + {var_w} = 1 já é uma equação do sistema, informar ambos tira um Grau de Liberdade de outra corrente.")
        print(f"Informe apenas {var_x} OU {var_w}, nunca os dois juntos.")
        # Invalida a execução do cálculo
        dados_validos = False

# RESTRIÇÃO 5: Verifica se os valores digitados respeitam os limites físicos básicos antes de calcular
if dados_validos:
    # Verifica se alguma vazão digitada é menor ou igual a zero
    for var_vazao in ["F", "D", "B"]:
        if especificacoes[var_vazao] is not None and especificacoes[var_vazao] <= 0:
            print(f"\n[ERRO FÍSICO]: A vazão {var_vazao} deve ser estritamente maior que zero.")
            dados_validos = False
    # Verifica se alguma fração mássica digitada está fora do intervalo [0, 1]
    for var_frac in ["xF", "wF", "xD", "wD", "xB", "wB"]:
        if especificacoes[var_frac] is not None and not (0.0 <= especificacoes[var_frac] <= 1.0):
            print(f"\n[ERRO FÍSICO]: A fração mássica {var_frac} deve estar entre 0.0 e 1.0.")
            dados_validos = False


# ==============================================================================
# ETAPA 2 CORRIGIDA: SISTEMA ESCALONADO E ROBUSTO (LEVENBERG-MARQUARDT)
# ==============================================================================

# Se passou por todas as travas de pré-validação, prossegue para o cálculo numérico
if dados_validos:
    # Separa os nomes das 5 variáveis que ficaram como incógnitas (valor igual a None)
    incognitas_nomes = [var for var in nomes_variaveis if especificacoes[var] is None]

    # Identifica uma vazão de referência informada pelo usuário para adimensionalizar o sistema
    vazao_ref = next(especificacoes[k] for k in ["F", "D", "B"] if especificacoes[k] is not None)

    # Define a função vetorial com as 5 equações ADIMENSIONALIZADAS (mesma ordem de grandeza)
    def sistema_balanco_massa(vetor_incognitas):
        # Cria um dicionário temporário copiando as 4 variáveis conhecidas
        v = especificacoes.copy()
        # Multiplica as vazões adimensionais de volta por vazao_ref e atribui as frações
        for nome, valor_tentativa in zip(incognitas_nomes, vetor_incognitas):
            if nome in ["F", "D", "B"]:
                # Desfaz a adimensionalização da vazão para calcular o balanço
                v[nome] = valor_tentativa * vazao_ref
            else:
                # Mantém a fração mássica diretamente na escala de 0 a 1
                v[nome] = valor_tentativa

        # Equação 1: Balanço de Etanol dividido por vazao_ref (fica na escala de 0 a 1)
        eq1_balanco_etanol = ((v["F"] * v["xF"]) - (v["D"] * v["xD"]) - (v["B"] * v["xB"])) / vazao_ref
        # Equação 2: Balanço de Água dividido por vazao_ref (fica na escala de 0 a 1)
        eq2_balanco_agua   = ((v["F"] * v["wF"]) - (v["D"] * v["wD"]) - (v["B"] * v["wB"])) / vazao_ref
        # Equação 3: Restrição de soma das frações na Alimentação (escala de 0 a 1)
        eq3_soma_F         = v["xF"] + v["wF"] - 1.0
        # Equação 4: Restrição de soma das frações no Destilado (escala de 0 a 1)
        eq4_soma_D         = v["xD"] + v["wD"] - 1.0
        # Equação 5: Restrição de soma das frações no Fundo (escala de 0 a 1)
        eq5_soma_B         = v["xB"] + v["wB"] - 1.0

        # Retorna os 5 resíduos perfeitamente escalonados
        return [eq1_balanco_etanol, eq2_balanco_agua, eq3_soma_F, eq4_soma_D, eq5_soma_B]

    # Define um dicionário de chutes iniciais ASSIMÉTRICOS e fisicamente coerentes (todos entre 0 e 1)
    chutes_padrao = {
        "F": 1.0,   "D": 0.2,   "B": 0.8,   # Vazões adimensionais (fração de vazao_ref)
        "xF": 0.15, "wF": 0.85,             # Chute típico para alimentação
        "xD": 0.80, "wD": 0.20,             # Chute típico para topo (rico em volátil)
        "xB": 0.02, "wB": 0.98              # Chute típico para fundo (pobre em volátil)
    }

    # Monta o vetor de chute inicial pegando o valor correspondente de cada incógnita
    chute_inicial = [chutes_padrao[nome] for nome in incognitas_nomes]

    # Resolve usando o método 'lm' (Levenberg-Marquardt), imune a Jacobianas singulares no chute inicial
    resultado_solver = root(sistema_balanco_massa, chute_inicial, method="lm")

    # Converte as vazões calculadas de volta da forma adimensional para kg/h antes da Etapa 3
    for i, nome in enumerate(incognitas_nomes):
        if nome in ["F", "D", "B"]:
            resultado_solver.x[i] = resultado_solver.x[i] * vazao_ref

    # ==============================================================================
    # ETAPA 3: VALIDAÇÃO TERMODINÂMICA E FÍSICA DOS RESULTADOS CALCULADOS (PÓS-SOLVER)
    # ==============================================================================

    # Verifica se o algoritmo convergiu matematicamente (resíduos próximos de zero)
    if not resultado_solver.success or np.max(np.abs(resultado_solver.fun)) > 1e-6:
        # Exibe mensagem caso a combinação escolhida gere divisão por zero (ex: xD = xB)
        print("\n[ERRO MATEMÁTICO]: O sistema é singular ou impossível de convergir.")
        print("Verifique se você não especificou composições iguais para correntes diferentes (ex: xD = xB).")
    else:
        # Reconstrói o dicionário completo com todas as 9 variáveis resolvidas
        sol = especificacoes.copy()
        for nome, valor_final in zip(incognitas_nomes, resultado_solver.x):
            sol[nome] = valor_final

        # Verifica se alguma vazão calculada resultou negativa (violação da Regra da Alavanca)
        vazoes_positivas = (sol["F"] > 0) and (sol["D"] >= 0) and (sol["B"] >= 0)
        # Verifica se todas as frações calculadas estão dentro do limite físico entre 0 e 1
        fracoes_validas = all(-1e-7 <= sol[k] <= 1.0 + 1e-7 for k in ["xF", "wF", "xD", "wD", "xB", "wB"])
        # Verifica se a condição de destilação (fundo mais pobre em volátil que alimentação, e topo mais rico) foi atendida
        separacao_coerente = (sol["xB"] < sol["xF"] < sol["xD"])

        # Se houver vazão negativa ou fração fora de [0, 1], explica o erro termodinâmico ao usuário
        if not vazoes_positivas or not fracoes_validas:
            print("\n[ERRO DE CONSISTÊNCIA FÍSICA]: A solução matemática gerou vazões negativas ou frações fora de [0, 1]!")
            print(f"Valores calculados -> F: {sol['F']:.2f}, D: {sol['D']:.2f}, B: {sol['B']:.2f}")
            print(f"Composições (Etanol) -> xB: {sol['xB']:.4f}, xF: {sol['xF']:.4f}, xD: {sol['xD']:.4f}")
            print("Motivo: Violação da Regra da Alavanca. A composição da alimentação (xF) DEVE estar entre xB e xD.")
        else:
            # Caso o usuário tenha invertido topo e fundo (ex: xB > xF > xD), emite um alerta didático
            if not separacao_coerente:
                print("\n[ALERTA TERMODINÂMICO]: O balanço fechou com valores positivos, mas xD <= xF <= xB.")
                print("Na prática, o componente mais volátil deveria se concentrar no topo (xB < xF < xD).")

            # Calcula a recuperação de etanol no destilado em porcentagem
            recuperacao_etanol = ((sol["D"] * sol["xD"]) / (sol["F"] * sol["xF"])) * 100.0
            # Calcula o resíduo do balanço global F - (D + B) para comprovar precisão numérica
            erro_global = abs(sol["F"] - (sol["D"] + sol["B"]))

            # Exibe a tabela final formatada diferenciando variáveis [ESPECIFICADAS] de [CALCULADAS]
            print("\n" + "=" * 75)
            print("TABELA DE RESULTADOS DO BALANÇO DE MASSA (9 VARIÁVEIS)")
            print("=" * 75)
            print(f"{'Variável':<10} | {'Descrição':<35} | {'Valor':>10} | {'Unid.':<6} | {'Status'}")
            print("-" * 75)

            # Define as unidades de medida de cada variável para exibição na tabela
            unidades = {k: "kg/h" if k in ["F", "D", "B"] else "kg/kg" for k in nomes_variaveis}

            # Imprime linha por linha das 9 variáveis do problema
            for var in nomes_variaveis:
                # Identifica se a variável foi entrada do usuário ou calculada pelo código
                status = "Especificada" if especificacoes[var] is not None else "Calculada"
                # Formata vazões com 2 casas decimais e frações com 4 casas decimais
                formato_valor = f"{sol[var]:10.2f}" if var in ["F", "D", "B"] else f"{sol[var]:10.4f}"
                # Exibe a linha formatada da tabela
                print(f"{var:<10} | {descricoes[var][:35]:<35} | {formato_valor} | {unidades[var]:<6} | {status}")

            # Imprime o resumo das vazões parciais por componente e indicadores de processo
            print("-" * 75)
            print(f"Vazões de Etanol [kg/h] -> Entrada (F): {sol['F']*sol['xF']:7.2f} | Topo (D): {sol['D']*sol['xD']:7.2f} | Fundo (B): {sol['B']*sol['xB']:7.2f}")
            print(f"Vazões de Água   [kg/h] -> Entrada (F): {sol['F']*sol['wF']:7.2f} | Topo (D): {sol['D']*sol['wD']:7.2f} | Fundo (B): {sol['B']*sol['wB']:7.2f}")
            print("-" * 75)
            print(f"Recuperação de Etanol no Topo : {recuperacao_etanol:8.2f} %")
            print(f"Erro de Fechamento Global     : {erro_global:8.2e} kg/h")
            print("=" * 75)
        