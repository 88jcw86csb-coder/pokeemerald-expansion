# Pokémon Eryon — entrega de teste e estado do build (15/10/2026)

## ROM disponível para teste exploratório

- Artefato GitHub Actions: `eryon-gba` no run **38634880588** (14/10/2026).
- Commit da ROM: `dc2016fef106023d165c255ef44af94e1d9d3d85`.
- Arquivo contido no artefato: `pokeeryon.gba` de 33.554.432 bytes.
- SHA-256 verificado: `c5a4d10755936ebcdf931027bea834103d991ac4bc19db9b7fee76724b2f3ca3`.
- Cabeçalho GBA validado separadamente; a execução real da campanha no Delta permanece **não verificada**.

**Esta ROM antiga não possui as alterações subsequentes de 15/10/2026.** É aceitável apenas para teste exploratório inicial, não para aprovar o lançamento.

## Alterações que exigem um novo build

Após as inspeções físicas de 42 mapas, foram integrados ao desenvolvimento:
1. `tools/eryon_script_warp_audit.py`: analisa entradas por script na Liga, colisões e acesso a eventos.
2. `tools/test_eryon_script_warp_audit.py`: regressão de destinos por script.
3. `tests/test_eryon_bidirectional_terrain.py`: protege transitabilidade em ambas as direções e links da Vila Aurora.
4. `tests/test_eryon_dialogue_links.py`: protege rótulos de NPCs e declarações de diálogos nos 42 mapas.
5. `Eryon_Verdelume`: novo vendedor de suprimentos em (25,19), com estoque básico, intermediário e avançado após as insígnias 3 e 6.
6. `tests/test_eryon_supply_merchant.py`: protege posição não bloqueada e os três estoques.

PR de integração: **#3** (mesclado). Os scripts e dados anteriores da campanha foram preservados.

## Próxima compilação obrigatória

A partir do HEAD atual de `eryon-development`, executar **Actions → CI → Run workflow** (ou `bash tools/build_eryon.sh` em checkout com toolchain ARM) e exigir resultado verde nos jobs `build-emerald`, `eryon-validation`, `eryon-build-gate`. O build precisa produzir **novo** `pokeeryon.gba` com SHA e artefato vinculados ao commit compilado. Não aceitar a ROM antiga como prova.

Após compilar, testar em **Delta**: início/Riolu/capturas/EXP, lojas e itens, idas e voltas dos mapas, cura/derrota/checkpoints, oito ginásios, Equipe Eclipse, oito classificatórias e perda monetária/reinício, Elite Four, Aurélio, epílogo em ambas as ordens, salvamento e recarga.

## Pontos ainda pendentes para a versão final

- Executar integralmente a suíte de regressão e a compilação **nesta revisão**.
- Testar de fato no emulador, incluindo estados de flags e diálogos em diferentes ordens.
- Completar a identidade visual própria (tilesets, retratos, sprites) e interiores/puzzles de ginásios ainda provisórios.
- Revisar equilíbrio, progressão e economia depois de horas de jogo, e não apenas por scripts.

**A integridade estática e o êxito do build de 14/10 não equivalem a jogabilidade certificada da versão de 15/10.**
