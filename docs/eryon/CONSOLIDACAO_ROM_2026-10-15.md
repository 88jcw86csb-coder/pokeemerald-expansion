# Consolidação da ROM Eryon — 15 de outubro de 2026

## Critérios observáveis

| Etapa | Estado verificado | Próxima validação |
|---|---|---|
| Registro regional | 42 mapas em `gMapGroup_Eryon` | Percorrer toda a região no Delta |
| Oito ginásios | IDs, equipes, scripts e insígnias registrados | Lutar contra cada líder e salvar |
| Liga | 8 classificatórias, Elite Four e Campeão em scripts | Testar ordem, derrota, recomeço e conclusão |
| Eclipse | Investigações, combate final e epílogo registrados | Testar flags em diferentes ordens de missão |
| Encontros | Rotas e encontros especiais cadastrados | Conferir metatile de grama, EXP e captura real |
| Evoluções | Mudanças até Kalos, com exceções de gerações anteriores | Revisar ramificações e níveis no jogo |
| Terrenos | Quatro cidades com colisões corrigidas a partir das plantas | Verificar metatiles visuais e travessia em Porymap/Delta |
| Arte | Tilesets, retratos e sprites provisórios registrados | Refinar identidade GBA própria |
| Build atual | Nenhuma execução Actions encontrada para os commits recentes até a auditoria | CI manual na branch atual |
| Emulador | Nenhum playtest completo demonstrado | Campanha integral no Delta |

## Caminho de compilação existente

O repositório já possui `.github/workflows/build.yml` com `workflow_dispatch`. O job `ROM (Eryon)` instala o compilador ARM em Ubuntu, executa `bash tools/build_eryon.sh`, roda validadores, limpa uma ROM antiga antes do build, compila `pokeeryon.gba`, testa cabeçalho e gera SHA-256. O job `eryon-validation` executa uma auditoria independente.

**Ação externa ainda necessária:** acionar manualmente o workflow `CI` em `eryon-development`. A integração usada para gravar código não oferece uma ação de disparo do workflow. O sucesso antigo de 14/10 não valida o HEAD novo.

1. Abra a aba **Actions** do repositório e selecione o workflow **CI**.
2. Use **Run workflow** e escolha a branch **eryon-development**.
3. Após a conclusão, confira todos os jobs. Em caso de falha, use o artefato **eryon-build-diagnostics** e os logs do job para corrigir o erro exato.
4. Se houver sucesso, baixe **eryon-gba** e confira a presença de `pokeeryon.gba` e o hash em `build/eryon-rom.sha256`.
5. Teste no Delta: novo jogo com Riolu, deslocamentos e colisões, capturas, EXP, oito ginásios, Eclipse, classificação da Liga, Elite Four e Campeão. Salve e recarregue em pontos críticos.

Este relatório **não** atesta ROM compilada nem prontidão para lançamento; documenta o caminho para evidências reproduzíveis.


## Lote do desfecho e terrenos — 15/10/2026, branch de verificacao

Este lote parte de b2c74a3a073d930672f3172ee2841b232412da3f e preserva a estrutura existente.

- Encerramento da campanha: o combate final Eclipse, o transmissor da Gruta e o manifesto entregue continuam controlando o desligamento em Drakonia. O Campeonato exige as oito insignias e as oito classificatorias, mas nao exige acabar com Eclipse.
- Apos obter o titulo e desligar a rede, o Painel dos Cristais da Cidade da Liga oferece uma cerimonia opcional e unica (flag 0x4BB). A homenagem reconhece os oito lideres, Aurelio, Elya, Riolu e o restabelecimento da regiao. Tanto derrotar Eclipse antes quanto depois de se tornar Campeao leva ao mesmo encerramento. Sem batalhas repetidas ou reinicio de progresso.
- O trofeu da Elite Four, a professora em Vila Aurora e o terminal de Drakonia acompanham as conquistas. Os oito lideres mantem os dialogos de epilogo ja existentes.
- A Rota 04 foi fisicamente ampliada de 471 para 716 blocos acessiveis e conectados (grafo de 48x44). Novo pomar leste (23,10) e acampamento ao sul (21,34). Full Heal unico com flag 0x4BC, item recuperavel apos falha por Bolsa cheia.
- Binario registrado data/layouts/Eryon_Rota04/map.bin: 4224 bytes. Uma auditoria independente de comparacao dos 2112 metatiles com o plano nao encontrou divergencias nem eventos inacessiveis.
- Testes estruturais acrescentados: tests/test_eryon_story_completion.py e tests/test_eryon_route04_map_completion.py. **Gravados, nao executados na ferramenta do compilador.**
- Inventario de todos os 42 mapas registrados: cada map.json apresenta ao menos um objeto ou evento de cenario. Isto nao prova interiores finais, metatiles exclusivos, sprites definitivos nem campanha percorrida.

### Bloqueios para declarar o jogo concluido
1. Nenhuma execucao nova do GitHub Actions/compilacao ARM foi observada para esta branch. Criar PR nao equivale a obter CI.
2. A ROM .gba mais recente certificada continua anterior aos novos scripts; nao se pode afirmar que o novo lote compila ate obter um job verde e artefato com SHA identificavel.
3. Ha cenarios ainda com metatiles provisorios e retratos de lideres ainda sem sprites GBA proprios finalizados.
4. Fazer teste completo no Delta: fluxos de batalha, encontros selvagens, nivel de Riolu e Lucario, EXP, checkpoints, dezesseis? Nao: **oito classificatorias**, quatro membros da Elite e Campeao, saves, historia Eclipse nas duas ordens, cerimonia e retorno ao inicio.

A integracao deve manter o teste de regressao que protege as oito classificatorias e o retorno apos perda, sem alterar flags de insiginias, montagem de equipes ou capacidade de treinadores.
