# Eryon — Direção visual oficial (referência de produção)

Este documento registra a preferência aprovada para o visual final da ROM de GBA.
A ilustração conceitual aprovada na conversa é uma **meta artística**, não uma captura da ROM compilada nem a garantia de que os sprites e tiles já estejam implementados.

## Linguagem visual

- Pixel art 2D clássica de Game Boy Advance, perspectiva superior, legibilidade e escala compatíveis com Pokémon Emerald.
- Mapas de Eryon com **geometria original**, sem copiar ruas, edifícios ou roteiros espaciais de Hoenn.
- Cidades grandes, praças, fontes, jardins, canais, pontes e prédios com características regionais.
- Cidade da Liga: edifício central dominante, vias e jardins interligados, Anfiteatro das Folhas, Passeio das Encostas e Terraço das Oito Estrelas.
- Liga: interior monumental com classificatórias de oito adversários, possibilidade de recuperação antes da Elite Four e progressão integral já definida nos scripts.
- Trilha do Oásis: areia quente, rochas, palmeiras, riachos, pontes e Refúgio da Caravana. O cenário deve diferenciar visualmente a rota da cidade e dos demais biomas.
- Interfaces de batalha, mensagens e menus no padrão legível de GBA; usar sprites oficiais existentes de Pokémon até Kalos, sem fakemon.

## Requisitos de implementação

1. Validar tilesets, metatiles, colisões e alturas no mapa **real**.
2. Verificar que objetos, NPCs, entradas e warp events correspondem ao layout compilado.
3. Preservar scripts, progresso, treinadores, insígnias, Pokémon selvagens e EXP.
4. Distinguir mockups, planos ASCII, blockdata compilado, ROM compilada e teste no emulador: nenhum deles comprova sozinho os outros.
5. Testar cenas com capturas do emulador GBA antes de declarar o visual concluído.

## Evoluções

- Riolu → Lucario no nível **35**.
- Pokémon disponíveis até Kalos: eliminar exigências de troca e amizade em favor de evolução por nível.
- Outras evoluções especiais (por item, ambiente ou movimento) devem ser revisadas separadamente, garantindo escolhas inequívocas em espécies com múltiplos caminhos; não declarar que todas já foram migradas sem validação.
