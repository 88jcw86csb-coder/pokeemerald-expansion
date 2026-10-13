# Eryon — blocos de terreno (etapa provisória)

Arquivos de terreno GBA registrados até agora: 29 novos map.bin (22 mapas preexistentes, Vale dos Ecos, Aldeia dos Ecos, Trilha Lunar, Lunaris, Trilha dos Dragoes, Vila do Pico e Drakonia).

Os terrenos usam os metatiles General Grass (0x001) e General TallGrass (0x00D) com elevacao 3, bits de colisao zero, gerados como superficies transitaveis provisórias. Foram deixados corredores centrais largos; detalhes visuais, objetos decorativos, paredes, cidades, entradas, rotas e encontros ainda exigem trabalho no Porymap. Nao significa mapa artistico concluido.

Os mapas que continuam apontando para terreno herdado de Hoenn ainda precisam de uma etapa de redesign dedicada. O sucesso de compilacao, deslocamento no emulador e testes de batalha/save ainda não foi confirmado.

Lunaris esta registrada como cidade 64x56, com acesso reciproco pela Trilha Lunar, NPCs e posto de cura. O interior do ginasio, os combates do lider e a validacao no emulador permanecem pendentes.

A Trilha dos Dragoes (48x44) liga Lunaris a Vila do Pico (36x30), com terrain, eventos, personagens e pontos de investigacao registrados. Drakonia e o oitavo ginasio ainda nao possuem acesso fisico por esta vila.

Drakonia (64x56) agora possui mapa registrado e warp reciproco com Vila do Pico, com moradores, posto de cura, pesquisa de runas e suspeitos Eclipse. O ginásio de Dragao ainda precisa de interior e batalha.
