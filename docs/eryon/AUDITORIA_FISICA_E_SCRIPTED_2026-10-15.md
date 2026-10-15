# Eryon — auditoria de trânsito físico e warps por script (15/10/2026)

## Escopo e método

Auditoria independente sobre o estado da branch `eryon-development` posterior ao merge do PR #2, sem substituir os testes locais ou do motor GBA.

- Conferidos os **42 arquivos `data/maps/Eryon_*/map.json`**: identidade, saída de cada warp, coordenadas de eventos e encadeamento da região. As conexões registradas de `VilaAurora` (conexão de borda para `Rota01`) e os pares de warps formam rotas de ida e volta entre os mapas externos. Os quartos da Liga são conectados por warps em `scripts.inc`, não por `warp_events`.
- Conferidos os **42 `map.bin` registrados**, decodificando os bytes do GitHub e comparando com `width * height * 2` do layout.
- Para cada mapa, calculada a componente conexa dos blocos sem os bits de colisão `0x0C00` a partir de `VilaAurora (10,10)` ou do primeiro evento cadastrado. Comparados os pontos de `warp_events`, `object_events`, `bg_events` e `coord_events` com a componente. **Resultado observado: 42/42 arquivos no tamanho esperado, sem eventos cadastrados fora da componente avaliada.**
- Decodificados separadamente os quatro interiores da Liga a partir das coordenadas usadas pelos comandos `warp`: recepção `(12,12)`, classificatória `(22,30)`, recuperação `(12,14)`, Elite Four `(28,37)`. Nenhuma dessas chegadas está bloqueada pelos bits de colisão e todos os eventos das salas são acessíveis no grafo de terreno.
- Identificados **7 comandos `warp` por script**, apontando para **4 mapas internos** da Liga. Os destinos registrados são válidos e estão dentro do tamanho de seus layouts.

## Alteração permanente

Incluído `tools/eryon_script_warp_audit.py` para verificar automaticamente os comandos de warp por script, os destinos, o limite de coordenadas, os bits de colisão e o acesso físico aos objetos das quatro salas da Liga. Incluído `tools/test_eryon_script_warp_audit.py` com contratos de parsing, colisão e geometria real. O validador agora participa de `tools/build_eryon.sh` e do job `eryon-validation` em `.github/workflows/build.yml`. O contrato de build também exige sua execução.

Essa auditoria cobre uma lacuna anterior: a análise apenas de `map.json` não observava o ponto de chegada das salas que dependem de `warp MAP_...` no script.

## Limites de validação

- Os testes acima foram **inspeções estruturais independentes dos dados existentes**, e não a execução da suíte Python completa nem a compilação do jogo.
- O algoritmo de colisão é conservador: não simula eventos que alteram metatiles, movimentos dos NPCs, níveis de elevação, scripts disparados, passagem real de fronteira, batalhas ou condições de flags.
- **Compilação do HEAD atual:** ainda não confirmada. É preciso executar `bash tools/build_eryon.sh` no runner com toolchain ARM. O conector utilizado para alterações no GitHub não disponibilizou disparo de `workflow_dispatch`; também não foram observadas novas execuções de Actions para os novos commits.
- **Delta:** não há evidência de playtest completo, save/load, sistema de EXP ou passagem por todos os desafios. Nenhuma destas verificações foi marcada como aprovada.

## Portas de aceite antes de liberar o arquivo GBA

1. GitHub Actions → `CI` → `Run workflow` → branch `eryon-development`; confirmar sucesso de `ROM (Eryon)`, `eryon-validation` e `eryon-build-gate`.
2. Identificar artefato `eryon-gba`, hash SHA-256 e o commit que gerou a ROM.
3. Jogo novo no Delta: Riolu, capturas, EXP, oito insígnias, exploração bidirecional das regiões, Equipe Eclipse, oito classificatórias, reinício após derrota, recuperação, Elite Four, Aurélio, cerimônia, save/load e reentrada.
4. Antes do lançamento, concluir a substituição dos sprites e metatiles provisórios observados no inventário visual.

Esta auditoria não declara Eryon terminado ou jogável até a compilação e os playtests serem efetivamente realizados.
