"""
 Algebra linear

 Sistemas possiveis e determinados
    → São sistemas que possuem solução única.
    → Para que um sistema seja possível e determinado, é necessário que o número de incógnitas seja igual ao número de equações.
    → Para resolver um sistema possível e determinado, basta calcular o determinante da matriz dos coeficientes e o determinante da matriz dos coeficientes com os termos independentes.
    → O valor das incógnitas será igual ao determinante da matriz dos coeficientes com os termos independentes dividido pelo determinante da matriz dos coeficientes.
 → Como vamos calcular a razão entre os determinantes, e o denominador sempre sera o determinante D,
 para encontrar os valores para as incógnitas é necessário que D ≠ 0.
 → Caso o determinante D seja igual a 0, significa que ou o sistema é impossível,
 ou seja, não possui soluções, ou o sistema é possível indeterminando, ou seja, possui infinitas soluções.
"""

# bibliotecas

import numpy as np
import streamlit as st

# funcoes


def matriz(*args):
    n_linhas = len(args)
    n_colunas = len(args[0])
    Matriz = [[0] * n_colunas for _ in range(n_linhas)]

    for i in range(n_linhas):
        if len(args[i]) != n_colunas:
            raise ValueError("As listas devem ter o mesmo tamanho")

        for j in range(n_colunas):
            Matriz[i][j] = args[i][j]

    return Matriz


def calcular_determinante(matriz):
    n_linhas = len(matriz)
    n_colunas = len(matriz[0])
    if n_linhas != n_colunas:
        raise ValueError("A matriz deve ser quadrada.")

    if n_linhas == 1:
        return matriz[0][0]

    determinante = 0

    for j in range(n_colunas):
        cofator = matriz[0][j] * calcular_determinante(submatriz(matriz, 0, j))
        determinante += (-1) ** j * cofator

    return determinante


def submatriz(matriz, i, j):
    return [linha[:j] + linha[j+1:] for linha in (matriz[:i] + matriz[i+1:])]


def det_cramer(matriz):
    n_linhas = len(matriz)
    n_colunas = len(matriz[0])
    if n_linhas != n_colunas:
        raise ValueError("A matriz deve ser quadrada.")
    n = len(matriz)

    if n == 1:
        return matriz[0][0]  # Caso base: matriz 1x1

    if n == 2:
        # Caso base: matriz 2x2
        return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]

    det = 0
    sinal = 1

    for j in range(n):
        submatriz = []

        for i in range(1, n):
            linha = []

            for k in range(n):
                if k != j:
                    linha.append(matriz[i][k])

            submatriz.append(linha)

        det += sinal * matriz[0][j] * calcular_determinante(submatriz)
        sinal *= -1

    return det


def calcular_determinantes_cramer(matriz_coeficientes, vetor_termos_independentes):
    n_linhas = len(matriz_coeficientes)
    n_colunas = len(matriz_coeficientes[0])
    det_principal = det_cramer(matriz_coeficientes)

    if n_linhas != n_colunas:
        return "A matriz deve ser quadrada."
    elif det_principal == 0:
        return "O sistema não tem solução única"
    determinantes = []
    for i in range(n_linhas):
        matriz_auxiliar = [list(linha) for linha in matriz_coeficientes]
        for j in range(n_linhas):
            matriz_auxiliar[j][i] = vetor_termos_independentes[j]
        det_temp = det_cramer(matriz_auxiliar)
        determinantes.append(det_temp / det_principal)
    return determinantes


def exibir_sistema(resultado):
    letras = ['x', 'y', 'z', 'n', 'a', 'b', 'c', 'd', 'e', 'f']  # Adicione mais letras conforme necessário    
    for i, valor in enumerate(resultado):
        if i < len(letras):
            letra = letras[i]
        else:
            letra = f"x{i+1}"
        string = (f"{letra}: {valor}")
        return string

# funcoes auxiliares


def exibir_matriz_direita(matriz):
    col1, col2 = st.columns([1, 2])
    col1.write('')  # Coluna vazia para criar espaço à esquerda
    with col2:
        st.write('A matriz digitada foi:')
        st.write(matriz)


# interface

st.title('Cálculo de determinantes')

st.write('Cálculo de determinantes,')
st.write('Sistemas possiveis e determinados,')
st.write('→ São sistemas que possuem solução única.')
st.write('→ Para que um sistema seja possível e determinado, é necessário que o número de incógnitas seja igual ao número de equações.')
st.write('→ Para resolver um sistema possível e determinado, basta calcular o determinante da matriz dos coeficientes e o determinante da matriz dos coeficientes com os termos independentes.')
st.write('→ O valor das incógnitas será igual ao determinante da matriz dos coeficientes com os termos independentes dividido pelo determinante da matriz dos coeficientes.')
st.write('→ Como vamos calcular a razão entre os determinantes, e o denominador sempre sera o determinante D,')
st.write('para encontrar os valores para as incógnitas é necessário que D ≠ 0.')
st.write('→ Caso o determinante D seja igual a 0, significa que ou o sistema é impossível,')
st.write(' ou seja, não possui soluções, ou o sistema é possível indeterminando, ou seja, possui infinitas soluções.')


st.write('Aqui você pode calcular o determinante de uma matriz quadrada de qualquer ordem'
         ' e também resolver sistemas lineares utilizando o método de Cramer.'
         ' Para isso, basta digitar os valores da matriz e clicar em calcular.'
         )

# Entrada de dados

n = st.number_input('Digite a ordem da matriz', min_value=1,
                    max_value=10, value=1, step=1)

entrada = st.text_input("Digite os números separados por vírgula")
termos_ind = []
for num in entrada.split(","):
    num = num.strip()
    if num:
        try:
            termos_ind.append(float(num))
        except ValueError:
            st.warning(f"O valor '{num}' não é um número válido. Será ignorado.")


dados = []

for i in range(n):
    linha = []
    for j in range(n):
        elemento = st.number_input(f'Digite o elemento {i+1}x{j+1} da matriz')
        linha.append(elemento)
    dados.append(linha)

matriz_formatada = matriz(*dados)

# Saída de dados
st.write('A matriz digitada foi:')
exibir_matriz_direita(matriz_formatada)

st.write('O determinante da matriz é:')
st.write(det_cramer(matriz_formatada))

# st.write('O determinante da matriz é:')
# st.write(np.linalg.det(matriz_formatada))

if st.button('Calcular sistema'):
    st.write('O resultado do sistema é:')
    resultado = calcular_determinantes_cramer(matriz_formatada, termos_ind)
    valores = exibir_sistema(resultado)
    st.write(valores)
