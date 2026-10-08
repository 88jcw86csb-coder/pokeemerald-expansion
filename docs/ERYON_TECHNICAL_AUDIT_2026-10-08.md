# Eryon — Auditoria técnica inicial (2026-10-08)

## Arquivos inspecionados na branch eryon-development
- `src/starter_choose.c`: `STARTER_MON_COUNT` é 1 e a lista `sStarterMon` contém `SPECIES_RIOLU`. **Configuração encontrada no código**, ainda sem prova de compilação ou teste em jogo.
- `data/maps/LittlerootTown/map.json`: mantém `MAP_LITTLEROOT_TOWN`, `REGION_HOENN`, eventos e NPCs originais.
- `data/maps/Route101/map.json`: mantém `MAP_ROUTE101`, `REGION_HOENN`, ligação com Oldale Town e sequência de resgate do Professor Birch.
- `docs/ERYON_IMPLEMENTATION_PLAN.md`: checklist e critérios de aceitação previamente registrados.

## Diagnóstico
O Riolu inicial tem implementação parcial identificável. Os dois mapas de abertura consultados **não constituem mapas originais de Eryon**. Não afirmar que a campanha ou ROM final estão prontas.

## Sequência de migração recomendada
1. Inventariar dependências dos mapas iniciais: `map.json`, `scripts.inc`, `text.inc`, `layouts`, `map_groups.json`, `wild_encounters.json`, constantes, flags e variáveis.
2. Definir identidade da vila inicial, Rota 1, Bosque de Lúmina e primeira cidade com especificações de layout e conexões.
3. Criar mapas e layouts próprios com IDs consistentes; evitar renomear mapas sem atualizar referências.
4. Criar eventos próprios de introdução e entrega de Riolu, removendo dependências narrativas do resgate de Birch.
5. Adicionar encontros selvagens e treinadores adequados ao início da jornada, com distribuição de espécies oficial até Kalos.
6. Testar flags e progressão: início, entrega do Riolu, saída da vila, bosque, chegada à primeira cidade e retorno.
7. Compilar com toolchain GBA e executar testes de novo jogo, batalha, save/load e transições.

## Testes ainda pendentes
- [ ] Compilação bem-sucedida
- [ ] Inicialização em emulador
- [ ] Entrega de Riolu em jogo
- [ ] Mapas originais e conexões
- [ ] Eventos sem softlock
- [ ] Salvamento e carregamento
- [ ] Compatibilidade Delta

**Nota:** auditoria limitada aos arquivos explicitamente consultados. Outros arquivos podem já ter alterações não examinadas.
