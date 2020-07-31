# Trabalho COS738: Recuperação - Modelo Vetorial

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

**Resultados**:

 `Consulta ; [ Posição, DocNumber, Similaridade - Cos Θ] `
 - 1; [ 1, 533, 0.22]
 - 1; [ 2, 52, 0.20]
 - 1; [ 3, 437, 0.20]
....
 - 100; [  1,   579, 0.36]
 - 100; [  2,   183, 0.33]
 - 100; [  3,  1017, 0.32]

