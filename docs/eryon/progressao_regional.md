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
| 7 | Vila Dos Pomares | village | Rota 03 |
| 8 | Rota 03 | route | Neonara |
| 9 | Neonara | gym | Colinas Da Neblina |
| 10 | Colinas Da Neblina | route | Vila Da Neblina |
| 11 | Vila Da Neblina | village | Trilha Glacial |
| 12 | Trilha Glacial | route | Frostheim |
| 13 | Frostheim | gym | Serra Dos Cristais |
| 14 | Serra Dos Cristais | mountain | Refugio Cristal |
| 15 | Refugio Cristal | village | Passagem Rochosa |
| 16 | Passagem Rochosa | mountain | Arkhara |
| 17 | Arkhara | gym | Estrada Oriental |
| 18 | Estrada Oriental | route | Posto Oriental |
| 19 | Posto Oriental | village | Vale Dos Ventos |
| 20 | Vale Dos Ventos | valley | Umbra |
| 21 | Umbra | gym | Rota Das Cachoeiras |
| 22 | Rota Das Cachoeiras | route | Vila Das Aguas |
| 23 | Vila Das Aguas | village | Trilha Do Oasis |
| 24 | Trilha Do Oasis | route | Deserto De Solaris |
| 25 | Deserto De Solaris | desert | Ignivar |
| 26 | Ignivar | gym | Floresta Dos Ecos |
| 27 | Floresta Dos Ecos | forest | Aldeia Dos Ecos |
| 28 | Aldeia Dos Ecos | village | Trilha Lunar |
| 29 | Trilha Lunar | route | Lunaris |
| 30 | Lunaris | gym | Trilha Dos Dragoes |
| 31 | Trilha Dos Dragoes | route | Vila Do Pico |
| 32 | Vila Do Pico | village | Drakonia |
| 33 | Drakonia | gym | Gruta Das Estrelas |
| 34 | Gruta Das Estrelas | mountain | Caminho Da Liga |
| 35 | Caminho Da Liga | route | Liga Eryon |
| 36 | Liga Eryon | league | fim |

## Critérios de implementação
- Não colocar cidades de ginásio consecutivas.
- Inserir trilhas, biomas, vilas de descanso e encontros selvagens entre marcos.
- Manter Bosque de Lumina entre a primeira rota e Verdelume.
- Preservar saídas já registradas: Serra → Passagem → Estrada → Vale.
- Refúgio Cristal e Posto Oriental são desvios laterais planejados; a tabela é ordem narrativa, não exige quebrar os warps diretos existentes.
- Os novos locais são propostas de expansão; não alegar que possuem map.json, layout ou warp.
- Confirmar em Porymap e no emulador cada transição antes de liberar a ROM.

