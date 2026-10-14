# Pokémon Eryon — direção de arte e estrutura regional próprias

**Decisão do projeto (14/10/2026):** Eryon pode usar a engine e a compatibilidade técnica de `pokeemerald-expansion`, mas **não** deve reproduzir mapas, sequência geográfica, silhuetas de personagens, retratos dos líderes, aparência de ginásios ou identidade gráfica de Pokémon Emerald/Hoenn.

## Situação técnica verificada

- Eryon já possui **42 layouts binários próprios**, mas possuir um `map.bin` diferente não significa possuir arte final independente.
- Os layouts ainda referenciam tilesets da base, como `gTileset_General`, `gTileset_Rustboro` e `gTileset_Petalburg`; esses nomes representam **arte provisória**, não a identidade final.
- Mapas de Eryon ainda utilizam gráficos de NPCs existentes (por exemplo, `OBJ_EVENT_GFX_AQUA_MEMBER_M` para integrantes da Equipe Eclipse).
- As equipes de líderes estão implementadas em `src/data/trainers.party` com retratos herdados, como `Pic: Leader Wattson` e `Pic: Elite Four Drake`: suas **equipes de batalha não devem ser apagadas** ao criar novos retratos.
- Nenhum arquivo de sprite ou tileset com nome Eryon foi encontrado na inspeção do diretório de gráficos da branch nesta data.
- O fluxo de história, os oito ginásios, as classificatórias e os saves são sistemas existentes: a remodelação visual deverá respeitar seus scripts, flags, colisões e entradas/saídas.

**Não confundir:** mapa independente, arte gráfica inédita e jogo visualmente finalizado são marcos de qualidade diferentes.

**Inventário automático inicial (GitHub Actions, 14/10/2026):** 42/42 layouts marcados para revisão de terreno por uma heurística de diversidade de metatiles; tilesets secundários herdados: 38 Rustboro e 4 Petalburg; 0 referências a gráficos de campo prefixados `OBJ_EVENT_GFX_ERYON_`; 34 treinadores Eryon com campo de retrato `Pic` herdado; 0 arquivos `map.bin` de Eryon exatamente iguais por hash a mapas binários da base. Estes números **não provam** que todos os mapas sejam cópias nem que qualquer arte seja original; apenas identificam trabalho visual pendente. Execute `python3 tools/eryon_visual_audit.py` para refazer o inventário. A ausência de duplicatas binárias exatas de Hoenn não certifica originalidade estética.

## Identidade-mãe

Paisagens com geologia de cristais ressonantes e marcas de antigas observações astronômicas, misturando natureza, infraestrutura de pesquisa e arquitetura regional. Motivos recorrentes: arcos quebrados, relevos assimétricos, terraços, lanternas, anéis concêntricos, passarelas de pesquisa e formas de estrela/eclíptica. Paleta-base azul-petróleo, âmbar e pedra-creme, modulada por cada bioma. Evitar reproduzir fachadas icônicas, disposição de cidades e cores/silhuetas dos personagens de Emerald.

### Regra para rotas e exploração

1. **Não seguir o passo a passo de Hoenn**, seja na ordem de biomas, na rede de conexões ou na localização de desafios. Não usar uma rota antiga como molde geométrico.
2. **Desenhar primeiro a topologia** (gargalos, desvios, laços, atalhos de retorno e áreas opcionais), depois pintar os metatiles. O arco principal pode ter progressão por insígnias, mas a exploração não deve ser uma linha cidade → corredor → cidade.
3. Rotas extensas têm ao menos um marco geográfico inconfundível e, onde couber, uma bifurcação opcional com consequência (item, história, treinador ou habitat). Trechos curtos de ligação são exceções documentadas.
4. Misturar gradualmente fronteiras de bioma: floresta/cânion, vale/ruína, ponte/encosta, vale de cristais/observatório. Não repetir a geometria padronizada ou o mesmo corredor central em várias áreas.
5. A história da Equipe Eclipse deve alterar leitura de locais revisitados (NPCs, eventos, iluminação e pontos de interesse), sem copiar a sequência de eventos Team Aqua/Magma.
6. **Novas conexões devem ser de fato construídas** (layout, warp/connection, reciprocal, colisão, eventos e teste de alcance), e não apenas desenhadas na documentação.

### Direções distintas para as oito cidades e ginásios

| Área | Identidade espacial e visual do ginásio | Princípio de desafio |
| --- | --- | --- |
| Verdelume | Estufa em terraços e pontes entre raízes, não a planta de um ginásio de Hoenn | Alternância de passagens sob copas e caminhos de irrigação |
| Neonara | Subestação de ressonância com lâminas de luz âmbar e cabos suspensos | Sincronizar circuitos em salas conectadas, sem repetir Wattson |
| Frostheim | Observatório alpino escavado na rocha, com vitrais de gelo | Correntes de vento e passagens em alturas diferentes |
| Arkhara | Museu-cânion com rochas gravadas e passarelas arqueológicas | Reconstituir sequências de símbolos e escolher galerias |
| Umbra | Jardim de névoa, reflexos de água rasa e lanternas | Ler marcos de iluminação e explorar trilhas alternativas |
| Ignivar | Instalação termal/forja de pesquisa, com calor e condutos | Redirecionar pressão/fluxo entre plataformas |
| Lunaris | Planetário com anéis e instrumentos astronômicos | Alinhar constelações em câmaras circulares |
| Drakonia | Santuário de pedra em desníveis, pontes e pátios de dragões | Padrões de eco que destravam trajetos opcionais |

Estas são **direções de arte e arquitetura**, não afirmações de que interiores ou puzzles já estão implementados. Preservar os oito líderes e a escala **efetivamente usada** pelo jogo (níveis máximos 18, 25, 31, 36, 41, 46, 51, 56), sem reverter para metas obsoletas de documentos antigos.

### Personagens e sprites

- **Protagonistas:** desenho próprio, sem a silhueta da May/Brendan. Seguir a ficha `docs/ERYON_CHARACTER_DESIGN.md`, com variantes consistentes para andar, correr, bicicleta, surfar, batalha e menus.
- **Líderes de ginásio:** cada líder deve ter retrato de batalha, sprite de campo, paleta, gestual e roupa distintos; o sprite não pode continuar visualmente sendo Roxanne, Wattson, Drake etc.
- **Equipe Eclipse:** uniforme, cores, insígnias, retratos e sprites próprios, não reutilizar visuais de Team Aqua/Magma no produto final.
- **NPCs recorrentes:** famílias de roupas por localidade (exploradores da serra, pesquisadores do observatório, comerciantes do deserto etc.), mantendo consistência de proporções GBA.
- **Pokémon:** espécies oficiais somente até Kalos, sem Fakemon. A exigência de sprites originais refere-se a **personagens humanos, cenários, ícones e interface**; não inventar novas espécies ou trocar arbitrariamente as espécies oficiais.

### Técnicas de implementação e aceitação

- Criar arte como arquivos-fonte editáveis quando possível e gerar recursos GBA compatíveis; usar paletas indexadas, proporções, metatiles, animação e limites de VRAM conforme a engine.
- Registrar novos símbolos e gráficos **sem sobrescrever** recursos compartilhados de Emerald; ligar mapas específicos a tilesets próprios quando estes existirem.
- Para cada área visualmente concluída, inspecionar Porymap ou ferramenta equivalente, compilar e testar no emulador: colisão, transições, movimentação do personagem, profundidade/sobreposição, paleta, animação e resolução de encontros.
- Para cada NPC ou líder redesenhado, verificar visão de frente/costas, direções, movimento, retrato de batalha e associação correta ao script/treinador.
- Antes de substituir arte temporária, mapear as referências e preservar a compatibilidade com os saves já criados, flags, lógica de ginásios, tabela selvagem, EXP e Liga.
- Não marcar um item como concluído apenas porque há documentação, `map.bin`, compilação verde ou teste estático. Exigir inspeção visual e testes reais de jogo.

## Sequência de execução sugerida

1. Auditar todos os 42 layouts por tileset reutilizado, monotonia de metatiles e geometria de corredores; auditar NPCs e retratos de treinadores por recurso legado.
2. Prototipar **um trecho de rota e uma cidade** com metatiles exclusivos, alternativa de navegação e cenografia própria; testar ROM e salvamento.
3. Implementar sprite de protagonista completo, um líder e um integrante Eclipse como referência de proporções/paleta; integrar e validar.
4. Generalizar um kit gráfico por bioma, cidade e tipo de interior sem duplicar padrões de Hoenn.
5. Substituir recursos temporários em fases, com testes automatizados, compilação e playtest no Delta ao longo da campanha.

**Regra de entrega:** diferenciar sempre **conceito definido**, **arquivo gravado**, **compilação aprovada** e **funcionalidade/visual confirmado em emulador**.
