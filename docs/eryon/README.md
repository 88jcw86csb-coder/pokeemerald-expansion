# Eryon — estado dos mapas (outubro de 2026)

## O que já existe

- Cinco plantas de terreno 48 × 44 em `docs/eryon/*_terrain_plan.txt`, geradas por `tools/eryon_terrain_plan.py`.
- Cinco layouts registrados em `data/layouts/layouts.json`, com caminhos próprios para `map.bin`.
- Conversor `tools/build_eryon_map_bins.py` que transforma símbolos ASCII em palavras de metatile e gera os cinco arquivos binários.
- Testes de conectividade e de sincronização entre o gerador e as plantas versionadas.

## Limitações críticas

Os valores de metatile utilizados na geração são **provisórios**. A existência de um `map.bin` não comprova que o terreno tenha aparência adequada, colisões corretas ou que os mapas estejam jogáveis. As áreas chamadas de lago, ruínas, posto ou caverna são, por enquanto, **formas de terreno planejadas**; não incluem necessariamente gráficos, água, edifícios ou eventos próprios.

O Bosque de Lumina usa entrada/saída norte-sul. Serra dos Cristais, Passagem Rochosa e Estrada Oriental usam conexões oeste-leste. O Vale dos Ventos tem entrada oeste e **borda leste fechada**, pois não há warp cadastrado ali.

## Próximas verificações obrigatórias

1. Executar `python3 -m unittest discover -s tools -p 'test_eryon_*py'`.
2. Regenerar os planos com `python3 tools/eryon_terrain_plan.py` e verificar se não há diferenças inesperadas.
3. Gerar os binários com `python3 tools/build_eryon_map_bins.py --wall 0x3c01 --path 0x3001 --meadow 0x3002 --stone 0x3003`.
4. Inspecionar os metatiles reais no Porymap, confirmar colisões e elevação 3, depois compilar e testar a ROM no emulador.
5. Implementar gráficos, eventos e encontros selvagens para as novas áreas.

**Não declarar a ROM pronta sem compilação e teste de jogo.**
