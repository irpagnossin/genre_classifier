O problema
==========

Dado um arquivo CSV no formato abaixo, agrupar as estações de rádio (audio_source_id) e trilhas de áudio (track_id) em gêneros musicais. created_at é o datetime em que a trilha de áudio track_id foi identificada na estação de rádio audio_source_id.

| created_at  | audio_source_id | track_id |
|-------------|-----------------|----------|
| 20160401... | 1               | 2        |
| 20160401... | 7               | 4        |
| 20160401... | 382             | 20       |


Solução proposta
================

Considerando que os ID das faixas de áudio (track_id, que potencialmente - mas não necessariamente - representa uma música) e das rádios (audio_source_id) têm significado apenas no contexto no qual foram gerados (ie, esses ID não são globalmente padronizados), e que não há qualquer correlação entre o horário em que uma faixa de áudio e seu gênero musical, concluimos que os dados apresentados oferecem apenas informações de frequência. Dito de outra forma: sabemos apenas quantas vezes cada faixa de áudio foi tocada em cada rádio. Logo, qualquer esforço para determinar o gênero, das trilhas de áudio e das rádios, deve ser feito com base nessa informação.

Nesse intento, a pergunta que surge é: como definir o gênero musical a partir das frequências? Uma ideia é a seguinte.

Primeiramente,  consideramos que músicas e rádios têm um atributo comum: o gênero, que é essencialmente UM rótulo, tal como "rock", "X" ou simplesmente 3 (um número qualquer).

Segundo, supomos que uma rádio do gênero X tenda a apresentar músicas do mesmo gênero X. Assim, tipicamente esperamos que em cada rádio ocorram mais músicas do mesmo gênero e menos músicas de gêneros distintos.

Com isso em mente, voltamos a atenção para as músicas: como sabemos o gênero de cada música? Ao invés de classificarmos uma música como sendo de um único gênero, imaginamos um espectro de gêneros, que é simplesmente a frequência com que essa música é tocada nas várias rádios. Por exemplo, suponha que tenhamos 2 rádios: R1 e R2. Podemos escrever o seguinte:

|        |R1   | R2  |
| -------|:---:|----:|
| track_1| 20% | 80% |
| track_2| 30% | 70% |
| track_3| 90% | 10% |

Isto é, 80% das ocorrências da música track_1 ocorre na rádio R2, e apenas 20% na rádio R1. A música track_2 segue o mesmo padrão, e a música track_3 tem um espectro bem distinto: é muito mais ouvida na rádio R1. Essa proposta permite, então, definir uma métrica de similaridade entre músicas.

Matematicamente, podemos escrever cada trilha sonora como um vetor com coordenadas retangulares R1 e R2. Por exemplo:
$$
\text{track}_1 = 0.2 |R_1\rangle + 0.8 |R_2\rangle
$$

Olhando para esse exemplo, podemos dizer que as músicas track_1 e track_2 têm o mesmo gênero da rádio R2 (chamemo-lo "gênero 1"), enquanto a música track_3 é mais consonante, em gênero, com a rádio R1 ("gênero 2"). Isso nos permite escrever:

| Música   | Gênero   |
|----------|----------|
| track_1  | gênero 1 |
| track_2  | gênero 1 |
| track_3  | gênero 2 |

| Rádio | Gênero   | 
|-------|----------|
| R1    | Gênero 2 |
| R2    | Gênero 1 |

O algoritmo implementado aqui realiza essa análise para milhares de músicas e rádios, utilizando k-means e análise de silhueta para decidir quanto à quantidade de classes (gêneros).

Nessa abordagem, cada rádio tem um gênero (é uma componente cartesiana num espaço euclidiano). 

Funcionamento básico
====================

O algoritmo roda em 4 estágios, sendo que cada estágio consome os insumos gerados no estágio anterior, exceto pelo primeiro, que começa com o arquivo de deteções:
- Estágio 1: avalia as detecções e constrói os espectros das músicas numa grande matriz de dimensões n_tracks x n_sources, onde n_tracks é a quantidade de trilhas de áudio distintas (são as amostras do "vetor de gênero") e n_sources é a quantidade de estações de rádio distintas (são as componentes do vetor). Execute "python stage1.py <threshold>", onde <threshold> é a quantidade mínima de vezes que uma trilha de áudio precisa estar presente para que seja considerada na análise. O padrão é 1, mas esse caso requer grande quantidade de memória para ser executado (> 8 GiB). Na verdade, qualquer <theshold> inferior a aproximadamente 100 requer mais de 8 GiB.
- Estágio 2: executa o algoritmo de classificação não supervisionado (k-means) várias vezes, uma vez para cada quantidade de gênero (ie, classes ou _clusters_), de 2 até 29, e identifica a quantidade de gêneros mais provável.
- Estágio 3: utiliza o mapeamento track_id -> genre_id para identificar as trilhas de áudio e estações de rádio no arquivo de detecções. Como resultado, gera os arquivos output/<threshold>/track2genre.csv e output/<threshold>/source2genre.csv.
- Estágio 4: amplia a cobertura de trilhas de áudio para aquelas trilhas cuja frequência absoluta tenham ficado abaixo do <threshold>. Isso é feito usando o mapeamento audio_source_id -> genre_id, gerado no estágio anterior.

Arquivos gerados
================

Arquivos gerados, todos na pasta output/<threshold>/, são:
- tracks.npz: é gerado no estágio 1. Contém os espectros de todas as trilhas de áudio, numa única matriz esparsa np.array. O formato é conveniente para tratamento, no estágio seguinte.
- track_ids.pickle: lista dos track_id existentes em tracks.npz, na mesma ordem. É utilizado para associar os genre_id, gerados no estágio 2, com os track_id.
- track2genre.pickle: mapeamento track_id->genre_id (genre_id >= 0), obtido pelo ajuste k-means à melhor quantidade de gêneros (classes ou _clusters_) aos espectros em tracks.npz
- silhouette.csv: diagnóstico da análise de silhueta, evidenciando a quantidade de gêneros selecionada pelo algoritmo.
- track2genre.csv: arquivo CSV relacionando track_id com genre_id. É gerado no estágio 3.
- source2genre.csv: arquivo CSV relacionando audio_source_id com genre_id. É gerado no estágio 3. Por definição, o gênero da estação de rádio é igual ao gênero da trilha de áudio mais frequente nela.
- track2genre_recap.csv: é gerado no estágio 4. Contém os track_id cuja frequência absoluta é inferior ao <threshold>, mas que devido ao mapeamento audio_source_id -> genre_id, gerado no estágio anterior, puderam ter seu gênero musical estimado (nesse caso, o gênero da trilha de áudio foi definido como sendo o gênero da estação de rádio onde ela mais ocorreu).


Resultados
==========

Quantidade de clusters: 2 a 4, sendo 2 o mais provável. Esse resultado foi consistente para todos os <threshold>, de 100 a 900: o gráfico abaixo mostra a pontuação do ajuste k-means para <threshold> >= 200 e <threshold> >= 900. De modo geral, quanto maior o <threshold>, maior é a certeza de que a quantidade de gêneros presentes é 2. 

![Diagnóstico resumido da análise de silhueta][silhouette_dianostic.png]

Próximos passos
===============

- Inverter a análise: ao invés de construir espectros das trilhas de áudio, construir espectros das rádios. Essa abordagem pode oferecer um comparativo para a solução implementada, e requer apenas refatoração do código já implementado.
- Executar o k-means na distância entre os vetores de gênero: como cada trilha de áudio define um vetor de gênero num espaço euclidiano, podemos calcular facilmente a "distância" entre duas trilhas de áudio (trilhas próximas teriam gêneros similares). Isso simplificaria a análise, permitindo a execução do algoritmo para <threshold> = 1 em máquinas menores. Contudo, como as n_sources dimensões seriam todas projetadas numa única dimensão (escalar), o resultado pode não ser muito bom, e teríamos de utilizá-lo apenas como insumo para outras análises.
- Implementar o estágio 2 utilizando Tensorflow, visando agilizar a execução (atualmente, o algoritmo de machine learning utiliza a biblioteca scikit-learn) e, possivelmente, clusterizar o processamento.
- ETL no estágio 1: escrever algoritmo para construir, iterativamente, o espectro compacto das trilhas de áudio (objeto TrackOccurrences). Isso pode ser feito facilmente, sem muito ônus de processamento, de modo a agilizar a execução dos estágios seguintes.