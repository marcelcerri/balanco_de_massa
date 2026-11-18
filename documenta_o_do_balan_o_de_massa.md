# 📊 Simulador de Balanço de Massa — Coluna de Destilação Binária

Este documento descreve a fundamentação teórica, a modelagem matemática, a estruturação matricial e as regras de validação física utilizadas para a resolução do balanço de massa em uma coluna de destilação contínua operando em regime permanente.

---

## 1. Enunciado do Problema

Uma coluna de destilação contínua, operando em regime permanente e sem reação química, é alimentada com uma mistura binária contendo **1000 kg/h** de etanol (componente mais volátil, $E$) e água (componente menos volátil, $A$). A corrente de alimentação ($F$) possui **12% em massa de etanol** (típico de um vinho de fermentação) e **88% em massa de água**.

O equipamento é projetado para separar a mistura em duas correntes de saída:
* **Destilado ou Topo ($D$):** Corrente rica em etanol, contendo **85% em massa de etanol**.
* **Resíduo ou Fundo ($B$, de *bottoms*):** Corrente pobre em etanol, contendo apenas **0,5% em massa de etanol** (fração mássica de $0{,}005$).

**Objetivos:**
1. Determinar as vazões mássicas totais das correntes de destilado ($D$) e de fundo ($B$).
2. Determinar as vazões parciais de etanol e água em cada corrente.
3. Calcular a eficiência de recuperação de etanol no topo da coluna ($\eta$).

---

## 2. Fluxograma e Variáveis do Processo

O volume de controle da unidade de separação é representado pelo diagrama abaixo:

```text
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
```

### Nomenclatura
* $F, D, B$: Vazões mássicas totais de Alimentação, Destilado e Fundo ($\text{kg/h}$).
* $x_F, x_D, x_B$: Frações mássicas do componente mais volátil (etanol) nas correntes $F$, $D$ e $B$.
* $w_F, w_D, w_B$: Frações mássicas do componente menos volátil (água) nas correntes $F$, $D$ e $B$, onde $w_i = 1 - x_i$.

---

## 3. Equacionamento e Resolução Analítica

Em regime permanente ($\text{Acúmulo} = 0$) e na ausência de reações químicas ($\text{Geração} = \text{Consumo} = 0$), a equação geral de conservação de massa reduz-se a:

$$\text{Massa que Entra} = \text{Massa que Sai}$$

Para um sistema binário (2 componentes), podemos escrever **2 equações linearmente independentes**:

### 3.1. Balanço de Massa Global
$$F = D + B$$

Substituindo $F = 1000\text{ kg/h}$:
$$1000 = D + B \implies B = 1000 - D \quad \text{(Equação 1)}$$

### 3.2. Balanço de Massa por Componente (Etanol)
$$F \cdot x_F = D \cdot x_D + B \cdot x_B$$

Substituindo os valores conhecidos ($F = 1000$, $x_F = 0{,}12$, $x_D = 0{,}85$, $x_B = 0{,}005$):
$$1000 \cdot 0{,}12 = 0{,}85 \cdot D + 0{,}005 \cdot B$$
$$120 = 0{,}85 \cdot D + 0{,}005 \cdot B \quad \text{(Equação 2)}$$

### 3.3. Solução por Substituição
Substituindo a **Equação 1** na **Equação 2**:
$$120 = 0{,}85 \cdot D + 0{,}005 \cdot (1000 - D)$$
$$120 = 0{,}85 \cdot D + 5 - 0{,}005 \cdot D$$
$$115 = 0{,}845 \cdot D \implies D = \frac{115}{0{,}845} \approx 136{,}09\text{ kg/h}$$

Calculando a vazão de fundo ($B$):
$$B = 1000 - 136{,}09 = 863{,}91\text{ kg/h}$$

### 3.4. Recuperação de Etanol no Topo ($\eta$)
A recuperação percentual indica a fração de todo o etanol alimentado na coluna que foi efetivamente recolhida no produto de topo:

$$\eta = \left( \frac{D \cdot x_D}{F \cdot x_F} \right) \cdot 100 = \left( \frac{136{,}09 \cdot 0{,}85}{120} \right) \cdot 100 \approx 96{,}40\%$$

---

## 4. Formulação Matricial ($A \cdot X = Y$)

Para que o algoritmo resolva o problema de forma genérica e escalável utilizando Álgebra Linear, as equações do balanço de massa são organizadas no formato matricial clássico:

$$A \cdot X = Y$$

### 4.1. Alinhamento das Equações Lineares
Isolando os termos que contêm as incógnitas ($D$ e $B$) no lado esquerdo e os termos independentes (conhecidos a partir da alimentação) no lado direito:

$$\begin{cases} 1{,}0 \cdot D &+ &1{,}0 \cdot B &= &F \\ x_D \cdot D &+ &x_B \cdot B &= &F \cdot x_F \end{cases}$$

### 4.2. Estrutura dos Blocos Matriciais
Separando os coeficientes multiplicadores, o vetor de incógnitas e o vetor de entradas, obtemos:

$$\underbrace{\begin{bmatrix} 1{,}0 & 1{,}0 \\ x_D & x_B \end{bmatrix}}_{\text{Matriz } A} \cdot \underbrace{\begin{bmatrix} D \\ B \end{bmatrix}}_{\text{Vetor } X} = \underbrace{\begin{bmatrix} F \\ F \cdot x_F \end{bmatrix}}_{\text{Vetor } Y}$$

* **Matriz dos Coeficientes ($A$):** Matriz $2 \times 2$ onde a primeira linha contém os coeficientes do **Balanço Global** ($[1{,}0 \quad 1{,}0]$) e a segunda linha contém as frações mássicas de saída referentes ao **Balanço do Componente Mais Volátil** ($[x_D \quad x_B]$).
* **Vetor de Incógnitas ($X$):** Vetor coluna contendo as vazões de saída desconhecidas ($D$ na posição $0$ e $B$ na posição $1$).
* **Vetor dos Termos Independentes ($Y$):** Vetor coluna contendo a vazão total de entrada ($F$) na primeira linha e a vazão mássica de entrada do componente volátil ($F \cdot x_F$) na segunda linha.

*(Nota: Caso se optasse por utilizar o balanço de água na segunda linha em substituição ao balanço global, a matriz $A$ seria composta por $[[x_D, x_B], [w_D, w_B]]$ e o vetor $Y$ por $[F \cdot x_F, F \cdot w_F]$, conduzindo exatamente ao mesmo resultado numérico).*

---

## 5. Restrições Físicas e Tratamento de Erros no Algoritmo

Como o simulador permite que o usuário altere livremente os valores de entrada ($F$, $x_F$, $x_D$ e $x_B$), o programa implementa duas camadas de validação antes de executar o solucionador matricial para evitar resultados matematicamente possíveis, porém fisicamente impossíveis (como vazões mássicas negativas ou divisão por zero):

### 5.1. Restrição de Domínio das Frações Mássicas (Erro Físico)
Por definição física, nenhuma fração mássica pode ser negativa ou superar $100\%$ da composição da corrente.
* **Condição exigida:**
  $$0{,}0 \le x_F \le 1{,}0 \quad \text{e} \quad 0{,}0 \le x_D \le 1{,}0 \quad \text{e} \quad 0{,}0 \le x_B \le 1{,}0$$
* **Comportamento:** Caso qualquer valor inserido esteja fora do intervalo $[0, 1]$, o programa interrompe a execução e emite um `[ERRO FÍSICO]`.

### 5.2. Regra da Alavanca e Coerência de Separação (Erro de Especificação)
Para que uma unidade de separação divida uma alimentação $F$ em duas correntes de composições diferentes sem gerar vazões negativas, a composição da alimentação deve estar estritamente situada entre a composição da corrente pobre (fundo) e a da corrente rica (topo). Além disso, se $x_D = x_B$, as linhas da Matriz $A$ tornam-se proporcionalmente idênticas (determinante igual a zero, $\det(A) = 0$), tornando o sistema linear singular (impossível ou indeterminado).
* **Condição exigida:**
  $$x_B < x_F < x_D$$
* **Demonstração pela Regra da Alavanca:**
  Isolando $D$ e $B$ algebricamente em função das frações mássicas, temos:
  $$D = F \cdot \left( \frac{x_F - x_B}{x_D - x_B} \right) \quad \text{e} \quad B = F \cdot \left( \frac{x_D - x_F}{x_D - x_B} \right)$$
  Para que $D > 0$ e $B > 0$, tanto os numeradores $(x_F - x_B)$ e $(x_D - x_F)$ quanto o denominador $(x_D - x_B)$ devem ser simultaneamente positivos, o que só ocorre se $x_B < x_F < x_D$.
* **Comportamento:** Caso o usuário insira, por exemplo, uma alimentação mais concentrada que o próprio topo ($x_F \ge x_D$) ou mais diluída que o fundo ($x_F \le x_B$), o programa bloqueia o cálculo e exibe um `[ERRO DE ESPECIFICAÇÃO]`.

### 5.3. Verificação de Fechamento Numérico
Após a resolução do sistema linear, o programa calcula o **Resíduo Numérico Global** ($\epsilon$):

$$\epsilon = |F - (D + B)|$$

Esse indicador confirma na saída do relatório que o erro de arredondamento em ponto flutuante é desprezível (da ordem de $10^{-13}\text{ kg/h}$ ou $0{,}00\text{e+}00$), garantindo a conservação estrita da massa.