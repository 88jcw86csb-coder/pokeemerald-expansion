# Pokémon Eryon — ordem regional planejada

Este documento é um roteiro de conexões, não warps já implementados.
As cidades dos oito ginásios seguem a lista oficial aprovada.
Cada seta representa uma conexão FUTURA a implementar/testar no motor.

| Ordem | Local | Categoria | Próximo destino |
|---:|---|---|---|
| 1 | Vila Aurora | village | Rota 01 |
| 2 | Rota 01 | route | Bosque De Lumina |
| 3 | Bosque De Lumina | forest | Rota 02 |
| 4 | Rota 02 | route | Verdelume |
| 5 | Verdelume | gym | Estrada Dos Pomares |
| 6 | Estrada Dos Pomares | route | Vila Dos Pomares |
| 7 | Vila Dos Pomares | village | Rota 04 |
| 8 | Rota 04 | route | Rota 03 |
| 9 | Rota 03 | route | Neonara |
| 10 | Neonara | gym | Colinas Da Neblina |
| 11 | Colinas Da Neblina | route | Vila Da Neblina |
| 12 | Vila Da Neblina | village | Trilha Glacial |
| 13 | Trilha Glacial | route | Frostheim |
| 14 | Frostheim | gym | Serra Dos Cristais |
| 15 | Serra Dos Cristais | mountain | Refugio Cristal |
| 16 | Refugio Cristal | village | Passagem Rochosa |
| 17 | Passagem Rochosa | mountain | Arkhara |
| 18 | Arkhara | gym | Estrada Oriental |
| 19 | Estrada Oriental | route | Posto Oriental |
| 20 | Posto Oriental | village | Vale Dos Ventos |
| 21 | Vale Dos Ventos | valley | Umbra |
| 22 | Umbra | gym | Rota Das Cachoeiras |
| 23 | Rota Das Cachoeiras | route | Vila Das Aguas |
| 24 | Vila Das Aguas | village | Trilha Do Oasis |
| 25 | Trilha Do Oasis | route | Deserto De Solaris |
| 26 | Deserto De Solaris | desert | Ignivar |
| 27 | Ignivar | gym | Floresta Dos Ecos |
| 28 | Floresta Dos Ecos | forest | Aldeia Dos Ecos |
| 29 | Aldeia Dos Ecos | village | Trilha Lunar |
| 30 | Trilha Lunar | route | Lunaris |
| 31 | Lunaris | gym | Trilha Dos Dragoes |
| 32 | Trilha Dos Dragoes | route | Vila Do Pico |
| 33 | Vila Do Pico | village | Drakonia |
| 34 | Drakonia | gym | Gruta Das Estrelas |
| 35 | Gruta Das Estrelas | mountain | Caminho Da Liga |
| 36 | Caminho Da Liga | route | Liga Eryon |
| 37 | Liga Eryon | league | Fim |

## Critérios de implementação
- Não colocar cidades de ginásio consecutivas.
- Inserir trilhas, biomas, vilas de descanso e encontros selvagens entre marcos.
- Manter Bosque de Lumina entre a primeira rota e Verdelume.
- Preservar saídas já registradas: Serra → Passagem → Estrada → Vale.
- Refúgio Cristal e Posto Oriental são desvios laterais planejados; a tabela é ordem narrativa, não exige quebrar os warps diretos existentes.
- Os novos locais são propostas de expansão; não alegar que possuem map.json, layout ou warp.
- Confirmar em Porymap e no emulador cada transição antes de liberar a ROM.
