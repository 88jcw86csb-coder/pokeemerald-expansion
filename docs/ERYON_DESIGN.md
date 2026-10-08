# Eryon — Jornada do Eclipse

## Objetivo
Projeto de ROM GBA completo construído sobre pokeemerald-expansion. Eryon não será tratado como demo: a meta é uma campanha completa, com exploração, progressão, Liga Pokémon e pós-game.

## Regras do projeto
- Pokémon oficiais somente, até Kalos (#001–#721).
- Inicial do jogador: Riolu Lv. 5.
- História com ritmo gradual; a Equipe Eclipse aparece e cresce ao longo da campanha.
- Mundo baseado em rotas e áreas naturais extensas, evitando sequência cidade → rota curta → cidade.
- Uma campanha principal completa, não um slideshow ou protótipo.
- Conteúdo de teste/protótipo deve ser claramente separado do conteúdo final.

## Geografia principal
Vila Aurora → Rota 01 → Bosque de Lúmina → Rota 02 → Verdelume → rotas e áreas naturais → Neonara → região montanhosa → Frostheim → desertos e ruínas → Arkhara → pântanos de Umbra → região vulcânica de Ignivar → observatório de Lunaris → montanhas de Drakonia → Victory Road → Liga Pokémon → pós-game.

## Ginásios e balanceamento aprovado
A dificuldade deve crescer ao longo da campanha, sem exigir treinamento excessivo entre cidades. Cada nível abaixo é o **nível máximo do Pokémon principal** do respectivo líder, não o nível de todos os membros da equipe.

| Ordem | Líder | Especialidade | Cidade | Pokémon principal | Nível máximo |
| --- | --- | --- | --- | --- | ---: |
| 1 | Kael | Planta | Verdelume | Roserade | 18 |
| 2 | Lyra | Elétrico | Neonara | Jolteon | 26 |
| 3 | Bjorn | Gelo | Frostheim | Weavile | 33 |
| 4 | Tessa | Pedra | Arkhara | Armaldo | 39 |
| 5 | Nox | Sombrio/Venenoso | Umbra | Drapion | 45 |
| 6 | Ragna | Fogo | Ignivar | Infernape | 51 |
| 7 | Seraphine | Psíquico/Fada | Lunaris | Gardevoir | 57 |
| 8 | Draven | Dragão | Drakonia | Garchomp | 64 |

**Status de implementação:** apenas Kael possui equipe de batalha cadastrada atualmente. Os níveis dos demais líderes são metas de balanceamento, ainda não implementadas em encontros ou scripts. A Liga Pokémon deve ter dificuldade superior à do oitavo ginásio, com níveis e equipes definidos antes da implementação.

## Liga
Elite 4: Valen (Poison), Kaia (Water), Orion (Ghost), Aeron (Flying).
Champion: Elara, equipe balanceada, ace Metagross.

## Equipe Eclipse e o mistério do eclipse
**Regra inegociável:** não criar espécies de Pokémon. Todas as criaturas capturáveis, vistas em batalhas ou tratadas como Pokémon devem pertencer às gerações I a VI (até Kalos).

Solarion, Noctarion e Eclipsion são **nomes de símbolos e fenômenos antigos**, não espécies ou formas de Pokémon:
- **Solarion:** símbolo da luz gravado nas ruínas de Eryon.
- **Noctarion:** símbolo da escuridão, associado aos registros da Equipe Eclipse.
- **Eclipsion:** nome dado ao evento de desequilíbrio que a equipe pretende provocar.

A trama culmina no Templo do Eclipse, onde a Equipe Eclipse tenta provocar o fenômeno Eclipsion usando artefatos antigos. Eventuais encontros lendários usarão somente Pokémon oficiais até a sexta geração; as espécies e a função narrativa serão definidas antes de implementar os eventos.

## Primeira sequência de mapas
Vila Aurora
Rota 01
Bosque de Lúmina
Rota 02
Verdelume

Essa sequência será implementada primeiro como fundação jogável e expandida gradualmente para o restante do mundo.

## Princípio técnico
Toda alteração de Eryon deve permanecer organizada e versionável no branch eryon-development. A master deve ser preservada como referência da engine.
