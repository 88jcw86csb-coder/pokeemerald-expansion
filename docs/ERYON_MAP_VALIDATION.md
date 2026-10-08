# Auditoria técnica — mapas iniciais de Eryon

Data: 2026-10-08. Esta auditoria é estática, não substitui compilação.

## Confirmado nos arquivos
- `data/maps/map_groups.json` contém `gMapGroup_Eryon`.
- Os mapas Vila Aurora, Rota 01, Bosque de Lúmina, Rota 02 e Verdelume têm arquivos `map.json`.
- A Rota 02 foi corrigida para usar `MAP_ERYON_ROTA02`, consistente com a nomenclatura do arquivo e das demais referências.
- `src/starter_choose.c` contém `SPECIES_RIOLU` como única espécie da lista de iniciais.

## Bloqueios antes de considerar jogável
1. Os `map.json` ainda não têm `object_events`, `coord_events` ou `bg_events` para introdução e história.
2. Os layouts registrados reutilizam arquivos de mapas de Hoenn; é necessário criar arquivos binários de blocos próprios, com colisão, entradas e saídas coerentes.
3. Os `warp_events` foram definidos em coordenadas de borda sem verificar se há tiles de warp correspondentes; validar no editor e em execução.
4. Confirmar geração de constantes dos novos mapas e integração no pipeline de build.
5. Confirmar que a inicialização do jogo em Vila Aurora é compatível com o fluxo original de intro, scripts e flags.
6. Verificar se a escolha única de inicial não deixa caminhos de interface dependentes de três opções.
7. Executar compilação limpa e testar novo jogo, movimentação, transições e salvamento.

## Critério de aprovação da abertura
Novo jogo inicia sem travar; protagonista aparece em Vila Aurora; Professor Elya entrega Riolu nível 5; o jogador percorre Rota 01, Bosque de Lúmina e Rota 02 até Verdelume; encontros selvagens, colisões, warps e salvamento funcionam; mapas têm geometria própria.

**Status:** pendente de implementação e testes. Não declarar ROM pronta com base apenas neste documento.
