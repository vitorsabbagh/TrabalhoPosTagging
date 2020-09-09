# Trabalho COS738: POS Tagging

**Base de Documentos**
 1. corpus100.txt 

**Módulos**
 1. Separação (teste / treino) e Aprendizado> learning.py
 2. Decoder e Avaliação: decode.py

**Palavras Desconhecidas**:
 - Foi implementada uma matriz de observação de sufixos de 2 caracteres.
 - Sempre que o algoritmo de Viterbi recebe uma palavra desconhecida, ele calcula a probabilidade de observação por meio da matriz de sufixos (temp/hmm_learning_sufixes.json) ao invés da matriz de observação convencional. 
 - As palavras desconhecidas de todas as cross-validations foram salvas em hmm_unknown_words.txt. 

**Arquivos Gerados**
 - hmm_accuracy: acurácia de cada tag
 - hmm_learning_apriori: matriz apriori
 - hmm_learning_emissions: matriz de observações
 - hmm_learning_sufixes: matriz de sufixos
 - hmm_learning_transitions: matriz de transição 
 - hmm_testing_data: dados de teste
 - hmm_unknown_words: palavras desconhecidas
 - hmm_relatorio
 - Obs.: Os arquivos json estão divididos em chaves de 0 a 9, que correspondem ao índice ten_fold (cross-validation), de forma a manter sempre os dados de aprendizado diferentes dos dados de teste.

**Resultados**: hmm_relatorio.txt

- Taxa de acerto geral: 86.14% 
- Qtde de tags processadas: 104963 
- Qtde de tags processadas corretamente: 90419 


- Taxa de acerto da classe VTD
- VTD: 72.31% 
- Total da classe: 72.31%


- Taxa de acerto da classe ART
- ART: 95.46% 
- Total da classe: 95.46%

- Taxa de acerto da classe N
- N: 92.77% 
- Total da classe: 92.77%

