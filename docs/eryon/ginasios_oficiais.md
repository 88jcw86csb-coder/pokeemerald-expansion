# Ginásios de Pokémon Eryon — implementação vigente

Esta página distingue a **proposta histórica** daquilo que está gravado na
branch `eryon-development`. Não alterar equipes, flags ou identidades sem
verificar `src/data/trainers.party`, `data/maps/Eryon_*/scripts.inc` e
`data/maps/GymEryon_*/map.json`.

## Oito líderes implementados

| Ordem | Cidade | Líder no jogo | Estilo de cenário | Nível máximo real |
|---:|---|---|---|---:|
| 1 | Verdelume | Kael | Estufa e raízes | 18 |
| 2 | Neonara | Volt | Circuitos de ressonância | 25 |
| 3 | Frostheim | Bjorn | Gelo e observatório | 31 |
| 4 | Arkhara | Tessa | Galerias arqueológicas | 36 |
| 5 | Umbra | Nyx | Jardim de névoa | 41 |
| 6 | Ignivar | Kaio | Condutos termais | 46 |
| 7 | Lunaris | Lyra | Anéis do planetário | 51 |
| 8 | Drakonia | Ryu | Santuário dos dragões | 56 |

A identificação acima é compatível com os nomes `Name:` e os níveis
`Level:` da tabela de treinadores da revisão verificada em 16/10/2026.
Os oito líderes possuem NPCs próprios e sprites de campo Eryon nos mapas
registrados. Os times e insígnias existentes continuam sendo a autoridade
para balanceamento e progressão.

## O que está implementado e o que falta

- Cada ginásio possui um interior 24×18 vinculado à cidade, NPC do líder,
  guia, dois painéis em sequência e saída por evento. Os pontos de evento
  permanecem nas coordenadas originais.
- `tools/eryon_gym_interiors.py` gera agora oito topologias distintas para
  os obstáculos, inspiradas na identidade de cada cidade, e valida o acesso
  físico aos dois painéis, à saída e aos NPCs, incluindo sua ocupação.
- Os painéis ainda são interações simples por flags. **Não** estão prontos
  puzzles dinâmicos, adversários internos adicionais ou interiores com arte
  arquitetônica completamente nova. A verificação automatizada não equivale
  a uma partida real no Delta.
- Os temas gráficos atuais são bancos Eryon gerados sobre metatiles
  existentes; futuras substituições gráficas devem manter colisões,
  índices, elevação e compatibilidade GBA.

## Histórico de decisões

O primeiro planejamento previa Kael, Lyra, Bjorn, Tessa, Nox, Ragna,
Seraphine e Draven, com tetos 18, 26, 33, 39, 45, 51, 57 e 64.
Esse documento era um **plano antigo**, não o retrato fiel do jogo atual.
As decisões consolidadas posteriormente adotaram os líderes e a escala
18, 25, 31, 36, 41, 46, 51 e 56 acima. Não usar o plano antigo para
sobrescrever scripts, sprites, mapas ou equipes já implementados.
