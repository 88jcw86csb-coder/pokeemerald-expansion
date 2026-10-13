# Revisão técnica de Pokémon Eryon — 13/10/2026

## Escopo conferido

- Inventário de 37 mapas no grupo `gMapGroup_Eryon` e seus arquivos `map.json`, scripts e layouts.
- Ligações recíprocas entre os mapas, incluindo a nova cidade do quarto ginásio, Arkhara.
- Existência de eventos narrativos nos mapas, principalmente na Estrada dos Pomares, Vila dos Pomares e Colinas da Neblina.
- Checagem estática de scripts, constantes, binários de terrenos, caminhos de colisão, e restrição de HMs na progressão principal.
- Validação de que as oito cidades oficiais de ginásio estão representadas no mapa regional.

## Melhorias registradas

1. Arkhara (quarto ginásio, líder Tessa, tipo Pedra, Armaldo) passou de plano conceitual para mapa registrado de 64×56; está entre Passagem Rochosa e Estrada Oriental, com volta nos dois sentidos.
2. Adicionados personagens e acontecimentos da Equipe Eclipse nas três áreas que estavam vazias: Estrada dos Pomares, Vila dos Pomares e Colinas da Neblina.
3. Arkhara possui socorrista que cura a equipe e um registro clandestino investigável, com flag persistente, diálogos alternativos e passagens sem golpes de campo obrigatórios.
4. A cobertura automatizada verifica a presença de conteúdo em cada mapa, o cadastro das oito cidades de ginásio e o percurso livre de HMs no trecho Passagem Rochosa → Arkhara → Estrada Oriental.

## Pendências — não declarar ROM concluída

- **Ginásios:** o confronto oficial de Kael em Verdelume tem script de batalha e insígnia. Os outros **sete** ginásios ainda não têm batalha oficial nem entrega de insígnia nos scripts das cidades. Interiores, quebra-cabeças, equipes, insígnias e pós-batalha seguem como trabalho prioritário. Tessa existe como personagem, mas o desafio de Arkhara não está implantado.
- **Liga:** Caminho da Liga está registrado, porém edifício, Elite Four, campeão, final da história e pós-jogo ainda não foram implementados e aprovados.
- **Encontros selvagens:** verificador atual assegura espécies e tabelas somente nas três primeiras áreas com capturas. É preciso completar e revisar a disponibilidade por toda a região, garantindo os Pokémon oficiais até Kalos e sem fakemon.
- **Mapas herdados:** Vila Aurora, Rota 01, Rota 02, Verdelume e Rota 03 reutilizam terrenos de Hoenn e precisam de auditoria in-game de acessos e metatiles.
- **Arte:** os terrenos binários provisórios utilizam blocos genéricos. Falta acabamento em Porymap, identidade visual exclusiva, detalhes urbanos e revisão de colisões/elevações.
- **HMs:** scripts e caminhos estáticos são testados, mas a ausência de exigências de Cut, Rock Smash, Strength, Surf, Waterfall, Dive e Flash exige confirmação em emulador, especialmente nos cinco mapas herdados.
- **Qualidade geral:** testar batalhas, capturas, entrada e saída de todas as áreas, menus, economia, cura, salvamento, recarga e Delta. Compilação positiva não equivale a esse teste de ponta a ponta.
- **História:** as ações da Equipe Eclipse nos novos mapas têm pistas e eventos, mas a campanha principal precisa de missões, confrontos e resolução narrativa com progressão persistente.

## Critérios mínimos antes de uma ROM completa

1. Todos os oito líderes jogáveis com progressão correta de insígnias e níveis.
2. Derrota e encerramento da Equipe Eclipse, sem dependência de HMs.
3. Liga e final de jogo funcionais com conclusão gravada no save.
4. Encontros, evoluções e itens de progressão revisados em todas as áreas.
5. Teste completo em emulador GBA/Delta, incluindo save/load e ida/volta em todos os mapas.

**Nota de precisão:** este relatório descreve uma auditoria estrutural de repositório e CI. Não afirma ausência de todos os bugs nem jogo completo.
