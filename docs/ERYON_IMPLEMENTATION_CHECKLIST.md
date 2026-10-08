# Pokémon Eryon — implementação e critérios de conclusão

## Princípio
Nenhuma ROM deve ser anunciada como final sem compilação, execução e validação da campanha. O projeto usa apenas espécies oficiais e o Riolu é o inicial.

## Etapa 1 — Fundação verificável
- [x] Registrar mapas iniciais no grupo Eryon
- [x] Configurar Riolu como única opção de inicial na interface
- [x] Ajustar identificador da Rota 02
- [x] Compilar a branch eryon-development sem erros (GitHub Actions 37841661556; artefato `eryon-gba` gerado)
- [ ] Executar o artefato `eryon-gba` em emulador e registrar evidências de boot, save/load e eventos; compilação não comprova jogabilidade
- [ ] Verificar boot, novo jogo, spawn e travessia dos mapas em emulador
- [ ] Conferir limites de layout, warps, scripts e colisões
- [ ] Passar na validação de prontidão: `python3 tools/eryon_validate.py --strict-ready` (bloqueada até substituir terrenos herdados e verificar passagens de borda)

## Etapa 2 — Abertura jogável
- [ ] Layouts originais de Vila Aurora, Rota 01, Bosque de Lúmina, Rota 02 e Verdelume
- [ ] Protagonista original com sprites de campo e batalha
- [ ] Professor Elya, rival, diálogos e flags de progressão
- [ ] Entrega de Riolu nível 5 e Pokédex
- [ ] Encontros selvagens e treinadores de acordo com biomas
- [ ] Primeiro indício da Equipe Eclipse no Bosque de Lúmina
- [ ] Ginásio Kael e primeira insígnia

## Etapa 3 — Campanha
- [ ] Oito cidades de ginásio e rotas interligadas
- [ ] Equipe Eclipse, comandantes, esconderijo e progressão
- [ ] Solarion e Noctarion: símbolos antigos; Eclipsion: fenômeno narrativo (não são espécies de Pokémon)
- [ ] Definir encontros com lendários oficiais até Kalos, sem Fakemon
- [ ] Elite 4, Campeã Elara e créditos
- [ ] Missões opcionais, revisitas e exploração com ritmo gradual

## Etapa 4 — Pós-game e qualidade
- [ ] Áreas pós-Liga, rematches e missões lendárias
- [ ] Verificar disponibilidade planejada das espécies oficiais até Kalos
- [ ] Revisar evolução, golpes, habilidades, itens e balanceamento
- [ ] Testar salvamento/carregamento, softlocks, warps e progressão completa
- [ ] Gerar ROM .gba e testar em emulador GBA e Delta
- [ ] Publicar somente o artefato final validado

## Estado
Este documento é um checklist, não uma declaração de que os itens pendentes foram concluídos. Atualizar os marcadores apenas após implementação e evidência de teste.
