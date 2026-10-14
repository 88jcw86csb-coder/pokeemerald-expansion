# Pokémon Eryon — estado de desenvolvimento (14/10/2026)

A ROM de GBA segue em desenvolvimento na branch `eryon-development`. **Ter arquivos de jogo e testes estáticos aprovados não equivale a ter uma ROM completa validada no Delta.**

## Região e jornada
- O grupo Eryon registra **42 mapas**. Inclui Vila Aurora, Bosque de Lumina, os oito centros de ginásio, vilas intermediárias, Serra dos Cristais, Passagem Rochosa, Trilha dos Dragões, Drakonia e Cidade da Liga.
- Os cenários têm arquivos de terreno `map.bin` registrados, mas boa parte dos gráficos/metatiles e interiores é provisória e necessita revisão visual em Porymap e emulador.
- Riolu permanece como inicial; espécies oficiais até Kalos, sem Fakemon. Os limites de espécies têm testes específicos.
- A Equipe Eclipse aparece progressivamente nas rotas e grandes cidades; vários encontros, documentos, terminais e consequências persistentes estão nos scripts.

## Ginásios, Liga e combate
- Os oito ginásios possuem equipes, batalhas de líderes e lógica de insígnias verificadas por testes estruturais. A escala de principais é 18, 25, 31, 36, 41, 46, 51 e 56.
- Há testes automatizados para progressão de níveis e EXP; o equilíbrio real em jogo ainda exige playtest.
- A Cidade da Liga possui terreno 96×72 e acesso ao edifício central. Recepção, oito adversários classificatórios, sala de recuperação, Elite Four e Campeão têm mapas/scripts registrados. Verificar o funcionamento integral **no jogo** continua obrigatório.
- A derrota na classificatória deve reiniciar os oito confrontos após a perda normal de dinheiro; isso precisa ser exercitado em emulador, além dos testes de lógica.

## Trabalhos recentes
- Os mapas de Trilha dos Dragões, Vila do Pico e Drakonia foram sincronizados com expansões físicas de 218, 9 e 122 blocos respectivamente; os geradores foram ajustados para preservar esses acessos.
- A missão opcional da Serra dos Cristais inclui estações de ressonância, sentinela Eclipse e desativação do sinal; Arkhara e Passagem Rochosa reconhecem a conclusão.
- Novos acontecimentos foram colocados na Passagem Rochosa (engenheira de frequência), Arkhara (quadro de cargas) e Cidade da Liga (delegada de pesquisa), utilizando os flags existentes.
- Corrigidos testes obsoletos de capacidade de treinadores e discrepância entre a validação e a equipe real de Kael.
- Verifique o build atual do GitHub Actions antes de declarar a ROM compilada; alterações recentes atacam falhas de sintaxe no arquivo de equipes.

## Capturas e nova história regional — 14/10/2026

- As **21 rotas/cavernas** no grupo Eryon receberam tabelas terrestres `land_mons`; nenhuma das três primeiras tabelas foi substituída. Os 18 novos habitats usam somente espécies oficiais até Kalos e níveis previstos para sua fase na jornada.
- A missão opcional **O Rio Contaminado** conecta a Rota das Cachoeiras, Vila das Águas, Trilha do Oásis, Deserto de Solaris e Ignivar. Suas pistas reagem a flags persistentes sem alterar os ginásios ou a Liga.
- Foi criada uma coleta de amostra com prêmio único `Mystic Water` na vila; a recompensa pode ser resgatada depois, caso a Bolsa esteja cheia.
- Os testes de mapa e o validador de espécies cobrem as tabelas, locais e flags. Ainda é preciso comprovar no **Delta** os encontros no terreno, a entrega da recompensa, o salvamento e a jornada completa.

## Pendências prioritárias
1. Compilação limpa e verificação da ROM GBA via `tools/build_eryon.sh` e GitHub Actions.
2. Auditoria das tabelas `land_mons`, evolução, disponibilidade e distribuição de capturas por rota.
3. Conferência visual e funcional de sprites, insígnias, tilesets, interiores e colisões.
4. Jogabilidade completa no Delta: novo jogo, oito insígnias, história Eclipse, classificatória, Elite Four, Campeão, salvamento e retorno após derrotas.

## Comandos de verificação
- `python3 tools/eryon_validate.py`
- `python3 -m unittest discover -s tools -p 'test_eryon_event_flow.py' -v`
- `python3 -m unittest discover -s tests -p 'test_eryon_gym_balance.py' -v`
- `python3 tools/eryon_readiness_report.py`
- `bash tools/build_eryon.sh`

**Critério de conclusão:** uma ROM .gba produzida por compilação limpa, com mapas, capturas e progressão funcionalmente testados no Delta. As rotinas estáticas não certificam sozinhas que o jogo está terminado.
