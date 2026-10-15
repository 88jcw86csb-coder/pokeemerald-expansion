# Auditoria tecnica de mapas Eryon — 15 de outubro de 2026

## Evidencias obtidas nesta rodada

**Branch:** eryon-development. A auditoria anterior partiu de aeecf97e52249891fe5647bcf98bb6bbf7163ea7.

- Foram inspecionados individualmente os 42 arquivos map.json e seus respectivos 42 map.bin. Foram conferidas as dimensoes, bits de colisao dos eventos e alcance desde uma entrada ou NPC inicial.
- Problema reproduzido nos binarios anteriores: Caminho da Liga tinha sete eventos em posicoes bloqueadas/desconectadas; Cidade da Liga, quatro. Os planos ASCII correspondentes ja continham esses locais em terreno acessivel. Foram reconstruidos 60 e 107 blocos divergentes, respectivamente, deixando todos os eventos de ambos acessiveis no grafo de colisao.
- Vale dos Ecos possuia 931 barreiras no formato 0x300D (colisao zero). Agora utilizam 0x3C0D, preservando o ID visual do metatile e ativando colisao. Todos os eventos e as duas saidas permanecem ligados; pisos decorativos isolados nao representam percurso obrigatorio.
- Bosque de Lumina, Passagem Rochosa, Estrada Oriental, Vale dos Ventos, Estrada dos Pomares, Vila dos Pomares, Colinas da Neblina, Vila da Neblina, Refugio Cristal, Posto Oriental, Rota das Cachoeiras, Vila das Aguas, Trilha do Oasis e Deserto de Solaris tinham blocos sem colisao coerente com as paredes dos planos. Seus 14 arquivos map.bin foram regenerados a partir dos planos, com validacao das entradas, saidas e NPCs.
- Aldeia dos Ecos: o NPC testemunha (21,20) ficava sobre uma parede no plano. Foi criada passagem conectada do patio central, atualizado o gerador de vilas e passado a gerar o map.bin desta vila registrada. O workflow de previews foi ajustado para nao tratar esta vila como um mapa nao instalado.
- A Rota 04 e os demais mapas nao corrigidos permanecem sob os layouts ja existentes; nenhuma rota obrigatoria, treinador, Pokemon, insignia ou cadeia de qualificatorias foi substituida.
- **18 binarios com plano ASCII foram comparados byte a byte apos a gravacao**: nenhum bloco divergente encontrado nas 18 verificacoes independentes. A auditoria inclui Caminho da Liga, Cidade da Liga, Rota 04 e Aldeia dos Ecos.

## Protecoes adicionadas

- tools/eryon_map_traversal_audit.py: audita tamanho dos blocos, colisao em eventos, acesso fisico a eventos, warp reciproco, direcoes de conexao e grafo regional, incluindo warp de scripts.
- tests/test_eryon_world_traversal_contract.py: protege o inventario dos 42 mapas, pontos-chave da Liga, os 18 binarios sincronizados com seus planos e a colisao no Vale dos Ecos.
- tools/build_eryon.sh: executara a auditoria de transitabilidade antes da compilacao do GBA.
- tools/test_eryon_villages.py: protege a testemunha e o binario reconstruido de Aldeia dos Ecos.
- Os testes foram **gravados**, mas nao foi observada execucao de CI para o commit atual. As verificacoes de arquivos executadas via API GitHub nao substituem a suite Python.

## Limitacoes explicitas

- Os blocos foram analisados por bits de colisao e BFS em quatro direcoes. Isso nao demonstra a totalidade das propriedades dos metatiles, graficos sobrepostos, bloqueios dinamicos de NPCs ou transicoes acionadas na engine.
- Os 42 mapas tem layout e eventos registrados, mas os interiores e a arte definitiva de tilesets, NPCs, sprites de lideres e fachadas ainda sao provisios. O sistema visual detecta uso de recursos herdados do Emerald.
- Nao foi possivel acessar uma copia completa do repositorio no ambiente de compilacao: o acesso de rede para git clone nao foi disponibilizado e nao ha arm-none-eabi-gcc instalado. O conector GitHub permite ler/gravar arquivos, mas nao disparar um workflow novo.
- O GitHub Actions ainda nao exibiu execucao para o HEAD novo. **Compilacao atual da ROM e teste no Delta: NAO CONFIRMADOS.**
- Nenhum erro de compilacao foi corrigido com base em log atual, pois nao existem logs atuais consultaveis. Uma compilacao antiga verde nao prova que as mudancas recentes compilaram.

## Procedimento para obter prova de compilacao

1. Executar Actions > CI > Run workflow em eryon-development, usando o HEAD mais recente.
2. O job ROM (Eryon) executa bash tools/build_eryon.sh, incluindo geracao de layouts, testes estaticos, auditoria de transito e compilacao com arm-none-eabi.
3. Se falhar, abrir o log eryon-build-diagnostics para identificar a linha exata do compilador ou do teste. Nao usar um binario .gba de commit anterior como evidencia.
4. Em sucesso, conferir o artefato eryon-gba, arquivo pokeeryon.gba, cabecalho e SHA-256, e testar com Delta.
5. No Delta, validar principalmente deslocamentos por todas as rotas e interiores, batalhas e EXP, Riolu/Lucario, saves, retornos apos derrota, 8 insignias, 8 classificatorias, Elite Four, Campeao, Eclipse e epilogo nas duas ordens possiveis.

**Status:** estrutura dos mapas fortemente corrigida e com verificacoes estaticas, sem certificacao de jogo final ou compilacao atual.
