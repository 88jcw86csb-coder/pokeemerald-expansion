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
- A compilação anterior em `6d28df64901e3b51ca3298a38f59800d0d33af0f` foi aprovada com cabeçalho GBA válido. Cada novo HEAD precisa repetir o processo de compilação e testes; o Delta ainda não foi testado.

## Capturas e nova história regional — 14/10/2026

- As **21 rotas/cavernas** no grupo Eryon receberam tabelas terrestres `land_mons`; nenhuma das três primeiras tabelas foi substituída. Os 18 novos habitats usam somente espécies oficiais até Kalos e níveis previstos para sua fase na jornada.
- A missão opcional **O Rio Contaminado** conecta a Rota das Cachoeiras, Vila das Águas, Trilha do Oásis, Deserto de Solaris e Ignivar. Suas pistas reagem a flags persistentes sem alterar os ginásios ou a Liga.
- Foi criada uma coleta de amostra com prêmio único `Mystic Water` na vila; a recompensa pode ser resgatada depois, caso a Bolsa esteja cheia.
- A missão opcional **Os Ecos do Observatório** adiciona um gravador de pulsos ao Vale dos Ecos, entrega dos registros ao arquivista da Aldeia dos Ecos, um marcador na Trilha Lunar e reações narrativas em Lunaris e Drakonia. O arquivista concede `Star Piece` uma vez; flags permanentes independentes `0x4A2` e `0x4A3` não modificam o sétimo e oitavo ginásios.
- Os testes de mapa e o validador de espécies cobrem as tabelas, locais e flags. Ainda é preciso comprovar no **Delta** os encontros no terreno, a entrega da recompensa, o salvamento e a jornada completa.

## Continuidade do desfecho Eclipse na Cidade da Liga — 15/10/2026

- A capital reconhece o desligamento opcional da rede Eclipse em Drakonia por meio da repórter, do investigador e da pesquisadora. Há diálogos próprios para a combinação de Campeão com rede desativada.
- O novo **Painel dos Cristais** foi colocado na praça junto ao prédio central, em (50,39), sobre caminho transitável no plano 96×72. Ele acompanha o estado das provas, o desligamento e a conquista da Liga.
- O investigador verifica primeiro sua recompensa anterior da Gruta das Estrelas, preservando o direito de buscá-la quando a Bolsa estiver cheia.
- O epílogo alcança também a astrônoma e o arquivista da **Gruta das Estrelas**, a testemunha do **Caminho da Liga** e o comunicado da **Vila do Pico**, com diálogos especiais quando o jogador já é Campeão.
- Nenhum acesso, requisito de insígnia, resultado de batalha, evolução ou registro de classificação foi alterado. Os testes novos conferem a estrutura e não substituem compilação nem jogo no emulador.

## Clareira da Copa — Floresta dos Ecos (15/10/2026)

- Nova trilha física no norte do mapa 48×44: passagem (25,8–13) e clareira (22–28,14–18). As duas saídas originais para Ignivar e o Vale dos Ecos continuam registradas.
- Corrigida a divergência preexistente de `map.bin`: paredes da floresta estavam codificadas sem colisão. O novo binário corresponde ao plano autoritativo e à paleta de `tools/build_eryon_map_bins.py`, com paredes `0x3C01` e pisos `0x3001`/`0x3002`.
- O Caderno da Copa encontra a interferência Eclipse e reage à amostra opcional do rio (`FLAG_ERYON_FOREST_SIGNAL_LOG_READ=0x4AC`).
- Phantump, Pokémon oficial de Kalos, aparece no nível 40 após a leitura. Captura ou vitória registra a resolução (`0x4AD`); fuga, recusa e teleporte permitem tentar novamente. A batalha utiliza o fluxo padrão do motor de EXP, que ainda necessita de playtest.
- Após resolver o encontro, uma Dusk Ball é entregue uma única vez (`0x4AE`), sem consumo em caso de Bolsa cheia.
- O guarda existente, a engenheira da cidade de Ignivar e uma testemunha da Aldeia dos Ecos comentam a restauração da clareira. Sem alteração do sexto ginásio, da Liga e da estrutura de treinadores.
- Todas as evoluções por itens da geração Kalos foram convertidas para nível: Phantump, Spritzee, Swirlix e as quatro formas de Pumpkaboo evoluem no nível 36; Doublade no nível 42; todas as formas normais de Floette para Florges no nível 38. As formas originais são preservadas e testes de regressão foram acrescentados ao conjunto já executado por `tools/build_eryon.sh`.
- As gerações 1, 2, 3 e 5 ainda contêm regras de item/pedra que precisam de migração individual, sobretudo famílias de evoluções ramificadas como Eevee e Clamperl; não converter automaticamente sem controlar destinos duplicados.
- Os testes estáticos não certificam funcionamento gráfico nem gameplay real no Delta.

## Santuário Lunar — extensão da Trilha Lunar (15/10/2026)

- Nova área lateral **Santuário Lunar** ao sul da Trilha Lunar, ligada pela antiga clareira do sudoeste, com 48 blocos adicionais de caminho acessível. A travessia Aldeia dos Ecos ⇄ Lunaris permanece livre e sem HMs.
- Plano 48×44 e `map.bin` regenerados com bits corretos de colisão, usando a paleta dos geradores existentes. Não foram removidas as trilhas nem os eventos anteriores.
- Receptor de pesquisa (`FLAG_ERYON_LUNAR_ARRAY_READ`, 0x4B0) conecta dados da Aldeia e o desfecho da Eclipse à área nova; Inkay oficial de Kalos nível 45 pode ser capturado/derrotado (`0x4B1`), sendo novamente tentável após fuga ou recusa.
- Suprimentos opcionais oferecem uma única Max Revive (`0x4B2`), após a resolução do encontro; Bolsa cheia não consome a recompensa.
- NILO, guarda do santuário, desafia voluntariamente o jogador com Lunatone nível 46 e Solrock nível 47. O ID de treinador 891 foi registrado em `opponents.h`, com flag exclusiva `0x4AF` em `GetEryonTrainerFlagId`; contagem de treinadores ajustada para 892. O motor padrão cuida de batalha, prêmio e EXP, ainda dependentes de jogo no emulador.
- Astrônoma de Lunaris e anciã da Aldeia dos Ecos agora reagem à pesquisa e ao Inkay sem mudar o sétimo ginásio. Teste `test_eryon_moonfall_sanctuary.py` integrado à compilação e teste antigo ajustado para não presumir capacidade fixa de 891 treinadores.
- Esses testes e inspeções estáticas não certificam a compilação GBA nem a compatibilidade visual com Delta.

## Encosta norte e Fenda Glacial — Trilha Glacial (15/10/2026)

- Corrigida a divergência anterior entre plano 48×44 e `data/layouts/Eryon_TrilhaGlacial/map.bin`, que continha paredes codificadas como pisos sem colisão. O novo binário foi gerado do mesmo plano de terreno que o build utiliza.
- Uma passagem sinuosa pela encosta norte acrescentou 80 células transitáveis, alcançando os dois suprimentos preexistentes da Eclipse em (35,12) e (39,12), antes isolados por paredes do plano; nenhum script antigo foi removido.
- Na fenda de gelo, o Diário Glacial (`0x4B3`) conecta a pesquisa da Eclipse ao estado da equipe inimiga e ao final da rede em Drakonia. Bergmite nível 29 pode ser encontrado após examinar o diário; captura ou vitória registra `0x4B4`, enquanto recusa, fuga e teleporte permitem tentar novamente.
- A recompensa da fenda é uma única Revive (`0x4B5`), entregue somente após a resolução de Bergmite e mantendo nova tentativa com Bolsa cheia. O guia original comenta a recuperação do local.
- A cientista de Frostheim e a anciã da Vila da Neblina agora respondem ao novo acontecimento. O terceiro ginásio de Bjorn, a batalha já existente do pesquisador da Eclipse, suas recompensas e ambas as saídas da trilha foram mantidos.
- Novo teste estático `tests/test_eryon_glacial_rift.py`, chamado por `tools/build_eryon.sh`, cobre terreno/binário, alcançabilidade de caches/eventos, referências de scripts, flags e recompensa. Necessários ainda compilação e testes no Delta.

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
