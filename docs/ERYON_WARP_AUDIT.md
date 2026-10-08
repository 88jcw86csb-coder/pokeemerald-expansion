# Eryon — auditoria das transições iniciais

Atualizado em 2026-10-08 a partir dos arquivos `map.json` da branch `eryon-development`. Este documento descreve o estado atual dos dados, não uma prova de funcionamento no emulador.

## Transições declaradas

| Origem | Tipo | Coordenada | Destino | Índice de destino | Retorno declarado |
|---|---|---|---|---:|---|
| Vila Aurora | conexão de mapa (norte) | borda | Rota 01 | — | conexão sul na Rota 01 |
| Rota 01 | warp 0 | (19,10) | Bosque de Lúmina | 0 | warp 0 do Bosque |
| Bosque de Lúmina | warp 0 | (16,38) | Rota 01 | 0 | warp 0 da Rota 01 |
| Bosque de Lúmina | warp 1 | (14,5) | Rota 02 | 0 | warp 0 da Rota 02 |
| Rota 02 | warp 0 | (0,10) | Bosque de Lúmina | 1 | warp 1 do Bosque |
| Rota 02 | warp 1 | (49,10) | Verdelume | 0 | warp 0 de Verdelume |
| Verdelume | warp 0 | (0,30) | Rota 02 | 1 | warp 1 da Rota 02 |
| Verdelume | warp 1 | (39,30) | Rota 03 | 0 | conferir continuidade com Rota 03 |

**Importante:** Vila Aurora e Rota 01 usam `connections` entre si, não um par de `warp_events`. Uma conexão de borda depende da geometria e da passagem do motor; não pode ser validada como se fosse um warp de porta.

## Estado da base

- Os cinco mapas já têm NPCs e/ou placas registrados em `object_events` e `bg_events`.
- Os layouts ainda reutilizam terreno herdado de Hoenn; posições e índices corretos não garantem acesso físico aos pontos de passagem.
- A compilação GBA passou na execução GitHub Actions [37841661556](https://github.com/88jcw86csb-coder/pokeemerald-expansion/actions/runs/37841661556), com artefato `eryon-gba`. Isso **não** comprova que as transições funcionem no emulador.

## Critérios para aprovação da navegação

1. Substituir os blocos herdados por terrenos originais, mantendo limites e tiles de passagem compatíveis.
2. Testar os dois sentidos de Vila Aurora ↔ Rota 01 como **conexão de borda**.
3. Testar os dois sentidos de Rota 01 ↔ Bosque, Bosque ↔ Rota 02 e Rota 02 ↔ Verdelume como **warps**.
4. Conferir as posições de chegada, colisão, orientação, NPCs e salvamento em emulador.
5. Registrar resultados de cada passagem; até lá, classificar a navegação como **não validada**.
