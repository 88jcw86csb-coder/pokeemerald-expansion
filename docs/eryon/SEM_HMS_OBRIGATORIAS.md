# Pokémon Eryon — progressão sem HMs obrigatórias

**Regra obrigatória de projeto:** o jogador nunca precisará ensinar uma HM a um Pokémon para percorrer a campanha principal de Eryon, acessar as cidades de ginásio ou alcançar a Liga.

## Aplicação

- Cut, Rock Smash e Strength **não** podem ser exigidos para abrir caminhos ou alcançar recompensas necessárias à história.
- Surf, Waterfall, Dive e Flash também **não** podem ser pré-requisitos da progressão principal. Fly é apenas uma conveniência para viagem rápida.
- Florestas têm passagens naturais; rochas usam trilhas laterais e pontes; rios possuem pontes e balsas com eventos, sem exigir golpes de Pokémon.
- Cavernas, incluindo Gruta das Estrelas, sempre terão uma rota transitável a pé. Puzzles podem usar pistas, personagens, mecanismos e exploração, mas nunca exigir HM.
- Uma HM opcional pode oferecer atalhos ou segredos não essenciais, mas **nenhuma etapa da história, ginásio, ponto de cura ou Liga pode depender dela**.
- A ausência de HM precisa ser validada por testes de scripts, conexões recíprocas e análise conservadora de colisão dos mapas binários. Testes reais no emulador ainda serão necessários.

## Trecho auditado automaticamente

Ignivar → Floresta dos Ecos → Vale dos Ecos → Aldeia dos Ecos → Trilha Lunar → Lunaris → Trilha dos Dragões → Vila do Pico → Drakonia → Gruta das Estrelas → Caminho da Liga.

A Liga, seus interiores e batalhas finais ainda são etapas de implementação. A verificação atual não certifica todas as interações de metatiles no emulador nem os caminhos dos cinco mapas iniciais recem-corrigidos; todos continuam sujeitos a testes praticos antes da conclusao.
