# Eryon — encontros selvagens da abertura (estado real do código)

As três tabelas abaixo **já estão cadastradas** em `src/data/wild_encounters.json`, grupo `gWildMonHeaders`. Os dados foram conferidos diretamente no blob GitHub `348ee0fbafe1439fb02e6202a9f67e6c80f91d8f`. **Não há compilação ou teste no emulador confirmado.** Os mapas ainda reutilizam terrenos de Hoenn; a presença de grama acessível não foi verificada.

O motor usa 12 slots de encontros terrestres com pesos **20%, 20%, 10%, 10%, 10%, 10%, 5%, 5%, 4%, 4%, 1%, 1%**, nessa ordem. As faixas abaixo correspondem ao conteúdo real de cada slot, não a uma proposta.

## Rota 01 — taxa de encontro 20

| Slot | Peso | Espécie | Nível |
|---:|---:|---|---|
| 1 | 20% | Wurmple | 2–3 |
| 2 | 20% | Starly | 2–3 |
| 3 | 10% | Bidoof | 2–3 |
| 4 | 10% | Wurmple | 3–4 |
| 5 | 10% | Starly | 3–4 |
| 6 | 10% | Bidoof | 3–4 |
| 7–8 | 5% cada | Pidove | 3–4 |
| 9–10 | 4% cada | Sewaddle | 3–4 |
| 11–12 | 1% cada | Ralts | 3 |

## Bosque de Lúmina — taxa de encontro 25

| Slot | Peso | Espécie | Nível |
|---:|---:|---|---|
| 1 | 20% | Caterpie | 4–6 |
| 2 | 20% | Sewaddle | 4–6 |
| 3 | 10% | Weedle | 4–6 |
| 4 | 10% | Oddish | 5–7 |
| 5 | 10% | Shroomish | 5–7 |
| 6 | 10% | Caterpie | 5–7 |
| 7 | 5% | Venipede | 5–7 |
| 8 | 5% | Sewaddle | 5–7 |
| 9 | 4% | Petilil | 5–7 |
| 10 | 4% | Shroomish | 5–7 |
| 11–12 | 1% cada | Phantump | 6–7 |

## Rota 02 — taxa de encontro 20

| Slot | Peso | Espécie | Nível |
|---:|---:|---|---|
| 1 | 20% | Zigzagoon | 5–7 |
| 2 | 20% | Fletchling | 5–7 |
| 3 | 10% | Budew | 5–7 |
| 4 | 10% | Bunnelby | 6–8 |
| 5 | 10% | Fletchling | 6–8 |
| 6 | 10% | Zigzagoon | 6–8 |
| 7 | 5% | Budew | 6–8 |
| 8 | 5% | Bunnelby | 6–8 |
| 9–10 | 4% cada | Skiddo | 6–8 |
| 11–12 | 1% cada | Mareep | 7–8 |

## Situação e próximos testes

- [x] Três tabelas cadastradas, cada uma com 12 slots.
- [x] Espécies limitadas à primeira até a sexta geração.
- [x] Riolu nível 5 é entregue separadamente pela Professora Elya.
- [ ] Compilar `pokeeryon.gba` e verificar inclusão das tabelas.
- [ ] Substituir os terrenos herdados por mapas originais com grama acessível.
- [ ] Testar encontros, frequências e níveis em emulador.

**Nota:** o planejamento anterior com Pidgey, Sentret, Shinx, Scatterbug, Pikachu, Abra etc. não corresponde às tabelas implementadas. Esses Pokémon poderão ser avaliados para áreas futuras, mas não devem ser apresentados como disponíveis na abertura.
