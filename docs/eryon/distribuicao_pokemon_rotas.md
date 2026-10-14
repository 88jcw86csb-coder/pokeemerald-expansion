# Eryon — distribuição planejada de Pokémon selvagens

**Estado:** referência de design e faixas históricas de captura. Em 14/10/2026, todas as 21 rotas/cavernas registradas receberam tabelas terrestres reais em `src/data/wild_encounters.json`. A composição compilada varia desta proposta original; verificar no jogo os metatiles que ativam os encontros. Apenas espécies oficiais até Kalos; Riolu permanece o inicial.

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

## Auditoria da implementação — 14/10/2026

- **21 de 21** mapas do tipo rota/caverna possuem agora `land_mons` (12 posições por mapa, com chance padronizada de espécies comuns e raras); foram preservados os três mapas iniciais previamente registrados.
- **18 mapas** ganharam tabelas nesta etapa; as áreas incluem Serra dos Cristais, Passagem Rochosa, Estrada Oriental, trilhas intermediárias, Oásis, Solaris, Floresta dos Ecos, Trilha Lunar, Trilha dos Dragões, Gruta das Estrelas e Caminho da Liga.
- Os níveis variam de 11–16 na Rota 03 até 50–57 na Gruta das Estrelas. O Caminho da Liga conserva por enquanto a faixa anterior de 44–52.
- O pequeno mistério do rio entre Rota das Cachoeiras, Vila das Águas, Trilha do Oásis, Deserto de Solaris e Ignivar foi implementado em scripts. Na vila, uma amostra coletada rende `ITEM_MYSTIC_WATER` somente uma vez.
- **Pendente:** confirmação de encontros disparando em grama/solo/caverna; artes e comportamento de metatiles provisórios podem não acionar encontros automaticamente. Também faltam fontes para várias espécies, pesca/Surf, trocas, evoluções e eventos especiais até completar a Pokédex de Kalos. Testes estáticos e ROM compilada não substituem o teste no Delta.
