# Eryon — distribuição planejada de Pokémon selvagens

**Estado:** tabela de design, NÃO é tabela de encontros compilada na ROM. Apenas espécies oficiais até Kalos (gerações 1–6). O Riolu permanece o inicial da história; encontros selvagens não substituem o inicial.

| Área | Níveis previstos | Encontros comuns | Incomuns | Raros / especiais |
|---|---:|---|---|---|
| Rota 01 | 2–5 | Pidgey, Sentret, Zigzagoon | Shinx, Budew | Ralts |
| Bosque de Lumina | 4–9 | Caterpie, Wurmple, Sewaddle | Oddish, Shroomish, Pikachu | Eevee |
| Rota 02 | 7–12 | Poochyena, Bunnelby, Nidoran♀ | Growlithe, Abra | Riolu (muito raro, pós-ginásio 1) |
| Rota 03 | 11–16 | Mareep, Electrike, Taillow | Magnemite, Helioptile | Emolga |
| Serra dos Cristais | 15–21 | Geodude, Roggenrola, Zubat | Aron, Sableye | Carbink |
| Passagem Rochosa | 19–25 | Machop, Onix, Woobat | Nosepass, Mawile | Axew |
| Estrada Oriental | 23–29 | Sandile, Numel, Doduo | Trapinch, Skiddo | Absol |
| Vale dos Ventos | 27–33 | Hoppip, Swablu, Yanma | Gligar, Hawlucha | Noibat |
| Rota das Cachoeiras | 30–36 | Poliwag, Buizel, Lotad | Corphish, Clauncher | Dratini (pesca) |
| Deserto de Solaris | 34–40 | Sandshrew, Cacnea, Dwebble | Sigilyph, Helioptile | Gible |
| Floresta dos Ecos | 38–44 | Phantump, Pumpkaboo, Foongus | Zorua, Karrablast | Larvesta |
| Caminho da Liga (futuro) | 44–52 | Golbat, Graveler, Gurdurr | Zweilous, Gabite | Bagon |

## Diretrizes de implementação

- As espécies são **propostas**, não garantias de disponibilidade até os arquivos de encontros serem editados, compilados e testados.
- Equilibrar percentuais de encontro (comuns / incomuns / raros) por grama, água, pesca e caverna; não misturar habitats incompatíveis.
- Evoluções, itens de evolução, trocas e fósseis precisam de rotas de obtenção para permitir completar a Pokédex até Kalos.
- Pokémon lendários e míticos terão eventos próprios, não encontros comuns na grama.
- O restante da Pokédex até Kalos será distribuído entre rotas adicionais, áreas pós-jogo, pesca, surf, cavernas e eventos; esta tabela **não** afirma cobrir todas as espécies.
- A ordem final de cidades, ginásios, tipos e níveis é provisória e deve ser reconciliada com os líderes e equipes aprovados antes da implementação.
