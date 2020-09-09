# Trabalho COS738: POS Tagging

**Base de Documentos**
 1. corpus100.txt 

**Módulos**
 1. Separação (teste / treino) e Aprendizado> learning.py
 2. Decoder: decode.py
 Obs.: Os arquivos json estão divididos em chaves de 0 a 9, que correspondem ao índice ten_fold (cross-validation), de forma a manter sempre os dados de aprendizado diferentes dos dados de teste.

**Palavras Desconhecidas**:
 - Foi implementada uma matriz de observação de sufixos de 2 caracteres.
 - Sempre que o algoritmo de Viterbi recebe uma palavra desconhecida, ele calcula a probabilidade de observação por meio da matriz de sufixos (temp/hmm_learning_sufixes.json). Por exemplo
 - As palavras desconhecidas de todas as cross-validations foram salvas em hmm_unknown_words.txt. 


**Resultados**: hmm_relatorio.txt
 - Taxa de acerto geral: 82.56% 
 - 
 - Taxa de acerto da classe LPREP
 - LPREP: 54.55% 
 - Total da classe: 54.55%
 - 
 - Taxa de acerto da classe VTD
 - VTD: 72.06% 
 - Total da classe: 72.06%
 - 
 - Taxa de acerto da classe ART
 - ART: 90.43% 
 - Total da classe: 90.43%

**Resultados sem Stemmer**:

 `Consulta ; [ Posição, DocNumber, Similaridade - Cos Θ] `
 - 1; [ 1, 533, 0.22]
 - 1; [ 2, 52, 0.20]
 - 1; [ 3, 437, 0.20]
....
 - 100; [  1,   579, 0.36]
 - 100; [  2,   183, 0.33]
 - 100; [  3,  1017, 0.32]
