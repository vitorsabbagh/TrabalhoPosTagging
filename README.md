# Trabalho COS738: Recuperação - Modelo Vetorial

**Configurações**
 1. A ativação e desativação do STEMMER deve ser feita em cfg/general.cfg

**Base de Documentos**
 1. cf75.xml 
 2. cf76.xml
 3. cf77.xml
 4. cf78.xml
 5. cf79.xml

**Base de Consultas**
 1. cfquery.xml

**Módulos**
 1. Processador de Consultas: pc.py
 2. Gerador de Lista Invertida: gli.py
 3. Indexador: index.py
 4. Buscador: busca.py

**Outputs**:
 1. esperados.csv (pontuação de relevância dada pelos pesquisadores)
 2. consultas.csv
 3. gli.csv (lista invertida)
 4. modelo.json (Pesos, IDFs e Lista de Documentos)
 5. resultados:csv

**Resultados sem Stemmer**:

 `Consulta ; [ Posição, DocNumber, Similaridade - Cos Θ] `
 - 1; [ 1, 533, 0.22]
 - 1; [ 2, 52, 0.20]
 - 1; [ 3, 437, 0.20]
....
 - 100; [  1,   579, 0.36]
 - 100; [  2,   183, 0.33]
 - 100; [  3,  1017, 0.32]


**Resultados com Stemmer**:

 `Consulta ; [ Posição, DocNumber, Similaridade - Cos Θ] `
  -  1; [  1,   533, 0.28]
  -  1; [  2,    52, 0.25]
  -  1; [  3,   437, 0.24]
....

 - 100; [  1,   579, 0.39]
 - 100; [  2,  1017, 0.38]
 - 100; [  3,   183, 0.37]


[11pontos-nostemmer-1.pdf]("https://github.com/vitorsabbagh/TrabalhoRecuperacaoVetorial/tree/master/avalia/11pontos-nostemmer-1.pdf").