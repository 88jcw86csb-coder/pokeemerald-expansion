# Pokémon Eryon — Plano de implementação GBA

## Objetivo
Criar uma aventura original e completa para Game Boy Advance baseada em pokeemerald-expansion, com ROM compilada e testada em emulador compatível com GBA (incluindo Delta).

## Requisitos confirmados
- Pokémon inicial: Riolu.
- Idioma da aventura: português brasileiro (PT-BR) em todos os diálogos, avisos, missões e textos narrativos originais de Eryon.
- Tradução de menus, mensagens de batalha, itens e demais textos herdados da engine será uma etapa específica de localização, com revisão de fontes, acentos e largura das caixas no GBA.
- Manter nomes oficiais dos Pokémon; revisar termos e quebras de linha para evitar texto cortado na ROM.
- Apenas Pokémon oficiais, com espécies até a sexta geração (Kalos) disponíveis ao longo da campanha e pós-game.
- Oito ginásios, Equipe Eclipse, Liga Pokémon e pós-game.
- Progressão gradual; regiões naturais entre assentamentos; sem sucessão artificial de cidades.
- Mapas originais: bosques, cavernas, desertos, montanhas, rotas aquáticas e áreas opcionais.
- Protagonista com identidade própria, sem semelhança intencional com May.
- Dificuldade progressiva e equilibrada; manter os ajustes de ginásios aprovados no histórico antes de fixar níveis.
- Não apresentar protótipo web ou base de engine como ROM GBA final.

## Próxima etapa técnica — vertical slice inicial
1. Auditar arquivos alterados na branch eryon-development e registrar commits reais.
2. Confirmar scripts de introdução e seleção de Riolu na engine.
3. Verificar conexões e colisões dos mapas iniciais, incluindo bosque entre Rota 1 e primeira cidade importante.
4. Validar encontros selvagens e batalhas dos primeiros treinadores.
5. Verificar flags, variáveis e scripts para evitar bloqueios de progressão.
6. Compilar ROM GBA com toolchain apropriada e guardar logs.
7. Testar inicialização, deslocamento, batalha, salvamento e carregamento em emulador.
8. Somente após aprovação do trecho inicial, expandir a campanha.

## Critérios de aceitação do trecho inicial
- Novo jogo começa sem travamento.
- Jogador recebe Riolu corretamente.
- Conexões entre mapas funcionam em ambas as direções.
- Encontros selvagens e batalhas de treinadores funcionam.
- Eventos não repetem indevidamente.
- Save/load mantém estado.
- ROM gerada de fato; nenhuma declaração de compatibilidade Delta sem teste.

## Status
Este documento registra requisitos e checklist. **Não comprova implementação nem compilação.** A conclusão de cada etapa deve ser acompanhada por caminhos de arquivos, commit SHA e evidência de testes.
