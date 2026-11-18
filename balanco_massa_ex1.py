"""
Enunciado do Exercício
Uma coluna de destilação contínua operando em regime permanente é alimentada com uma mistura binária contendo 1000 kg/h de etanol (E) e água (A). 
A corrente de alimentação ($F$) possui 12% em massa de etanol (típico de um vinho de fermentação) e 88% de água.
O processo é projetado para produzir:Uma corrente de topo ou destilado ($D$) rica em etanol, contendo 85% em massa de etanol.
Uma corrente de fundo ou resíduo ($B$, de bottoms) pobre em etanol, contendo apenas 0,5% em massa de etanol (fração mássica de 0,005).
Determine as vazões mássicas totais das correntes de destilado ($D$) e de fundo ($B$), bem como a porcentagem de recuperação de etanol no topo da coluna.
Destilado (Topo)
                          D = ? (kg/h)
                        x_D = 0,850 (kg E / kg)
                        w_D = 0,150 (kg A / kg)
                               ▲
                               │
                     ┌─────────┴─────────┐
                     │                   │
   Alimentação (F)   │                   │
   F = 1000 kg/h ───►│     COLUNA DE     │
   x_F = 0,120       │    DESTILAÇÃO     │
   w_F = 0,880       │                   │
                     └─────────┬─────────┘
                               │
                               ▼
                         Resíduo (Fundo)
                          B = ? (kg/h)
                        x_B = 0,005 (kg E / kg)
                        w_B = 0,995 (kg A / kg)
"""
# Importa a biblioteca NumPy para resolução de sistemas lineares matriciais
import numpy as np

# Exibe o cabeçalho do programa no console
print("=" * 65)
# Exibe o título da calculadora de balanço de massa
print("SIMULADOR DE BALANÇO DE MASSA - COLUNA DE DESTILAÇÃO BINÁRIA")
# Exibe a linha divisória do cabeçalho
print("=" * 65)
# Informa ao usuário que ele pode usar os valores padrão do exercício
print("Dica: Pressione [ENTER] para utilizar os valores padrão do exercício.\n")

# Solicita a vazão de alimentação (F) ou assume 1000.0 kg/h caso o usuário aperte Enter
entrada_F = input("Digite a vazão mássica de alimentação F [kg/h] (Padrão = 1000): ")
# Converte a entrada para float ou atribui 1000.0 se a string estiver vazia
F = float(entrada_F) if entrada_F.strip() != "" else 1000.0

# Solicita a fração mássica de etanol na alimentação (xF) ou assume 0.12
entrada_xF = input("Digite a fração mássica do componente volátil na alimentação xF (Padrão = 0.12): ")
# Converte a entrada para float ou atribui 0.12 se a string estiver vazia
xF = float(entrada_xF) if entrada_xF.strip() != "" else 0.12

# Solicita a fração mássica de etanol no destilado (xD) ou assume 0.85
entrada_xD = input("Digite a fração mássica do componente volátil no topo xD (Padrão = 0.85): ")
# Converte a entrada para float ou atribui 0.85 se a string estiver vazia
xD = float(entrada_xD) if entrada_xD.strip() != "" else 0.85

# Solicita a fração mássica de etanol no fundo (xB) ou assume 0.005
entrada_xB = input("Digite a fração mássica do componente volátil no fundo xB (Padrão = 0.005): ")
# Converte a entrada para float ou atribui 0.005 se a string estiver vazia
xB = float(entrada_xB) if entrada_xB.strip() != "" else 0.005

# Verifica se as frações mássicas estão dentro do intervalo físico válido entre 0 e 1
if not (0.0 <= xF <= 1.0 and 0.0 <= xD <= 1.0 and 0.0 <= xB <= 1.0):
    # Exibe mensagem de erro caso alguma fração seja menor que 0 ou maior que 1
    print("\n[ERRO FÍSICO]: As frações mássicas devem estar estritamente entre 0 e 1.")

# Verifica a consistência termodinâmica do balanço (xB < xF < xD) para evitar vazões negativas
elif not (xB < xF < xD):
    # Exibe mensagem de erro caso a alimentação não esteja entre as composições de fundo e topo
    print("\n[ERRO DE ESPECIFICAÇÃO]: Para haver separação física real, é obrigatório que xB < xF < xD.")

# Caso todas as entradas sejam fisicamente válidas, executa a resolução do balanço
else:
    # Calcula a fração mássica do segundo componente (água) na alimentação por diferença
    wF = 1.0 - xF
    # Calcula a fração mássica do segundo componente (água) no destilado por diferença
    wD = 1.0 - xD
    # Calcula a fração mássica do segundo componente (água) no fundo por diferença
    wB = 1.0 - xB

    # Define a matriz dos coeficientes (A) do sistema linear [ [1, 1], [xD, xB] ]
    matriz_A = np.array([[1.0, 1.0], [xD, xB]])
    # Define o vetor dos termos independentes (Y) correspondente às entradas [ F, F * xF ]
    vetor_Y = np.array([F, F * xF])

    # Resolve o sistema de equações lineares A * X = Y para encontrar o vetor incógnita [D, B]
    solucao = np.linalg.solve(matriz_A, vetor_Y)
    # Extrai a vazão de destilado (D) da primeira posição do vetor solução
    D = solucao[0]
    # Extrai a vazão de fundo (B) da segunda posição do vetor solução
    B = solucao[1]

    # Calcula a vazão mássica do componente mais volátil (etanol) na alimentação
    F_volatil = F * xF
    # Calcula a vazão mássica do componente menos volátil (água) na alimentação
    F_pesado = F * wF
    # Calcula a vazão mássica do componente mais volátil no destilado
    D_volatil = D * xD
    # Calcula a vazão mássica do componente menos volátil no destilado
    D_pesado = D * wD
    # Calcula a vazão mássica do componente mais volátil no fundo
    B_volatil = B * xB
    # Calcula a vazão mássica do componente menos volátil no fundo
    B_pesado = B * wB

    # Calcula o percentual de recuperação do componente mais volátil na corrente de topo
    recuperacao = (D_volatil / F_volatil) * 100.0
    # Calcula o erro de fechamento do balanço global para conferência numérica
    erro_fechamento = abs(F - (D + B))

    # Imprime uma linha divisória para destacar a seção de resultados
    print("\n" + "=" * 65)
    # Imprime o título da tabela de resultados
    print("RESULTADOS DO BALANÇO DE MASSA")
    # Imprime a linha divisória abaixo do título
    print("=" * 65)
    # Exibe as vazões globais calculadas formatadas com duas casas decimais
    print(f"Vazão de Alimentação (F) : {F:10.2f} kg/h (Etanol: {F_volatil:7.2f} kg/h | Água: {F_pesado:7.2f} kg/h)")
    # Exibe a vazão de topo (D) e suas vazões parciais com duas casas decimais
    print(f"Vazão de Destilado (D)   : {D:10.2f} kg/h (Etanol: {D_volatil:7.2f} kg/h | Água: {D_pesado:7.2f} kg/h)")
    # Exibe a vazão de fundo (B) e suas vazões parciais com duas casas decimais
    print(f"Vazão de Fundo (B)       : {B:10.2f} kg/h (Etanol: {B_volatil:7.2f} kg/h | Água: {B_pesado:7.2f} kg/h)")
    # Imprime uma linha tracejada para separar os indicadores de desempenho
    print("-" * 65)
    # Exibe a eficiência de recuperação do componente principal no topo da coluna
    print(f"Recuperação no Topo      : {recuperacao:10.2f} %")
    # Exibe o desvio numérico do balanço para comprovar que Entrada = Saída
    print(f"Resíduo Numérico Global  : {erro_fechamento:10.2e} kg/h")
    # Imprime o rodapé de encerramento do relatório
    print("=" * 65)