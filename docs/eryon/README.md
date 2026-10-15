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

## Mirante da Aurora — Trilha dos Dragões (15/10/2026)

- Extensão física do ramo norte já existente entre Lunaris e Vila do Pico: 57 metatiles adicionais na área (39–45,7–13), ligados pela passagem da encosta, sem mexer na estrada principal, na sala do ninho de Noibat, na recompensa do Mirante Sul e nos NPCs anteriores.
- O `map.bin` foi regenerado a partir do plano autoritativo de terreno, mantendo bits de colisão correspondentes; duas saídas antigas e todos os locais já registrados continuaram alcançáveis.
- **Painel da Aurora** (`0x4B6`) reconhece o manifesto Eclipse, o desfecho em Drakonia e o estudo dos cristais; **Carbink nível 43** (`0x4B7`) entra por batalha selvagem padrão, podendo ser capturado ou derrotado. Fugir ou recusar não consome o encontro.
- A caixa da encosta oferece um único Max Ether (`0x4B8`) após resolver o encontro, sem consumir a recompensa quando a Bolsa está cheia.
- O geólogo da Vila do Pico e o pesquisador de Drakonia respondem à descoberta. Quando Carbink e Noibat já foram encontrados, os diálogos mencionam ambos, evitando ocultar a missão antiga; o oitavo ginásio e o encerramento da rede Eclipse não foram alterados.
- Teste `tests/test_eryon_dragon_aurora.py` integrado ao script de build verifica caminho, binário, flags, recompensas, interações e ligações às cidades. **Verificação estrutural não equivale a compilar nem jogar no Delta.**

## Consolidação de colisões em cidades (15/10/2026)

- **Falha detectada:** os binários versionados de Neonara, Frostheim, Umbra e Ignivar continham zero blocos com colisão ativa, divergindo das plantas já existentes que possuem mais de duas mil paredes cada. O processo `tools/build_eryon.sh` regenerava esses mapas antes de compilar, mas `make` direto ou arquivos baixados sem regeneração poderiam manter a geometria incorreta.
- **Correção:** regenerados apenas os quatro `data/layouts/Eryon_*/map.bin` a partir dos planos `docs/eryon/cidades/*_city_plan.txt`, com a paleta do gerador oficial (`#=0x3C01`, pisos `0x3001`, vegetação `0x3002`, pedra `0x3003`). Entradas, NPCs e placas foram avaliados por busca de caminhos sem remover recursos. Arkhara e Drakonia já eram consistentes; também foram incluídas nos testes.
- O novo `tools/test_eryon_city_collision.py` verifica binários, colisões, alcance dos NPCs e saídas, posições de eventos e acesso às praças de ginásio. Foi integrado ao script de build e ao job de validação separado do CI.
- **Não modificar Lunaris automaticamente:** o binário dessa cidade usa metatiles diferentes do padrão compartilhado; requer inspeção visual no Porymap antes de qualquer repintura.
- **Para compilar o HEAD atual:** GitHub → Actions → `CI` → `Run workflow` → branch `eryon-development`. Baixar o artefato `eryon-gba` apenas se a execução da branch passar, conferindo `build/eryon-rom.sha256` e os logs. Commits gravados pelo conector não produziram nova execução automática até esta auditoria.
- **Aprovação final ainda exige** jogar a ROM compilada no Delta: captura, EXP, oito insígnias, história Eclipse, oito batalhas classificatórias, Elite Four, Campeão, whiteout, menus e save/load. Teste Python não equivale à jogabilidade.

## Consolidação do gerador da Trilha Lunar (15/10/2026)

- Corrigido o erro de classificação: `Eryon_TrilhaLunar` já tem layout oficial `LAYOUT_ERYON_TRILHA_LUNAR` e seu próprio `map.bin`, mas estava na lista `PREVIEW_SPECS`, excluída da regeneração de mapas registrados.
- Agora consta em `SPECS`, portanto `bash tools/build_eryon.sh` gera o `data/layouts/Eryon_TrilhaLunar/map.bin` verdadeiro a partir do plano de 48×44 antes dos testes e do build, sem mudar os eventos, a história, Inkay ou o treinador Nilo.
- Acrescentada regressão em `tools/test_eryon_map_bins.py` que exige layout registrado, gerador correto e identidade byte a byte do binário da Trilha Lunar com a planta. O teste é descoberto pelo workflow de terrenos.
- **Limite:** a verificação confirma o contrato de geração; ainda é necessária compilação GBA no Actions e validação da travessia no Delta.

## Consolidação da bateria completa de testes (15/10/2026)

- Corrigida a cobertura incompleta em `tools/build_eryon.sh`: 11 módulos que **já existiam** em `tests/` não eram executados pelo roteiro principal. Entre eles, testes da classificatória da Liga, acesso à capital, missões Eclipse e conexões do fim do jogo.
- `tools/build_eryon.sh` e o job `eryon-validation` agora descobrem **automaticamente todos os arquivos `test_eryon_*.py`** de `tools/` e `tests/`, em vez de manter listas manuais que podem ficar defasadas.
- A compilação verifica também a sintaxe Python de toda a suíte e executa `eryon_validate.py`, `eryon_layout_audit.py` e `eryon_world_audit.py` antes de chamar `make`. Mantidos o descarte de ROM antiga, a validação do cabeçalho e o SHA-256 na produção da ROM.
- Novo teste de contrato `tools/test_eryon_build_contract.py` impede que o roteiro volte a omitir módulos e assegura que a checagem da ROM continua após os testes.
- **Validação ainda não equivale a GBA/Delta:** uma falha da suíte completa deverá ser corrigida nos arquivos reais; um status de sucesso antigo não vale para o HEAD atual.

## Consolidação de referências dos scripts (15/10/2026)

- Auditoria de **42 mapas registrados** confirmou, em inspeção remota dos arquivos, que as batalhas roteirizadas apontam para IDs e equipes cadastradas, as flags Eclipse/Liga são definidas e as espécies selvagens roteirizadas existem no enum do motor.
- Criado `tools/test_eryon_script_linkage.py`, descoberto automaticamente pelas suítes de testes do build e do CI, para sinalizar futuras referências ausentes, evolução de IDs duplicados, espécie inexistente ou nível selvagem fora do intervalo válido.
- Estas verificações são **estáticas**. A etapa bloqueadora continua sendo uma compilação do HEAD recente pelo GitHub Actions, seguida do teste integral em Delta.

## Consolidação da Liga — reinício da Elite Four (15/10/2026)

- **Endurecimento preventivo**, não correção de softlock comprovado: o motor `GetEryonTrainerFlagId` já associa `cleartrainerflag` às mesmas flags de progresso da Elite Four; assim, a transição anterior provavelmente já reiniciava a série. Adicionadas `clearflag` explícitas para tornar o reinício independente dessa relação implícita e protegê-lo contra alterações futuras.
- Corrigido `EryonLigaElite_OnTransition`: enquanto o jogador não for Campeão, a transição limpa as quatro flags de rodadas, a flag de batalha do Campeão e as cinco flags de treinador; preserva `FLAG_ERYON_QUALIFIED` e as oito fases classificatórias.
- A vitória final (`FLAG_ERYON_CHAMPION_CROWNED`) continua **permanente**, e o guard é avaliado antes de quaisquer resets.
- Dois novos testes de regressão foram acrescentados a `tests/test_eryon_league_contract.py`, já incluído pela descoberta automática do build. O jogo ainda precisa comprovar esses cenários em emulador: desistir após Aria, perder para Bastian e retornar, passar pela cura e vencer o Campeão.

## Auditoria de navegação regional e Liga (15/10/2026)

- A estrutura da região contém 42 mapas, saídas por `warp_events` e uma conexão de borda entre Vila Aurora e Rota 01. A recepção, as oito classificatórias, a sala de cura e a Elite Four usam transições por scripts.
- Acrescentado `tests/test_eryon_world_map_network.py`: valida índices e pares de retorno dos warps, conexões de borda recíprocas, dimensões dos mapas e posições de warps roteirizados e conectividade global desde a Vila Aurora até a Liga. Descoberta automática já presente no `tools/build_eryon.sh` e CI.
- O novo teste detecta mapas ou ligações desconectadas antes da compilação, mas **não substitui o teste das colisões, renderização e transferências no Delta**.

## Checkpoints de Eryon — derrota, retorno e Liga (15/10/2026)

- **Falha funcional provável identificada:** NPCs de Eryon usavam `special HealPlayerParty`, mas nenhum mapa de Eryon era registrado em `src/data/heal_locations.json` nem usava `setrespawn`. Assim, a derrota podia usar o último ponto de cura de Hoenn/Kanto, isolando o jogador da região original.
- **Correção em 16 locais existentes:** a Vila Aurora, os oito centros urbanos de ginásio, a Cidade da Liga, a recepção e cinco vilas de passagem agora registram `HEAL_LOCATION_ERYON_*` na tabela nativa gerada e usam `MAP_SCRIPT_ON_TRANSITION` + `setrespawn`. Os locais não precisam de NPC de cura novo e não disparam uma cena de enfermaria de Hoenn (`LOCALID_NONE`).
- O ponto da recepção é `(12,12)`, dentro do prédio, para manter a regra de perda de dinheiro e retorno às **oito classificatórias desde a fase 1**. A credencial de classificado e o título de Campeão continuam sujeitos às flags anteriores, sem alterações.
- Verificações sobre os binários de todos os 16 mapas confirmaram chão com colisão zero, ausência de eventos sobrepostos e acesso desde a entrada (ou spawn de Riolu). Novo teste `tests/test_eryon_whiteout_checkpoints.py` protege IDs, tabela gerada, scripts e coordenadas.
- **Ainda não é um teste no Delta**: deve ser validado perdendo uma batalha nas primeiras rotas, depois de visitar cada cidade e dentro da Liga, além de executar `bash tools/build_eryon.sh` com o compilador ARM.

## Regresso à origem — conclusão narrativa da Eclipse (15/10/2026)

- O mistério apresentado pela pedra do Bosque de Lumina, o aviso da Vila Aurora, as falas de Kael e a Prof. Elya agora reagem à flag **já existente** `FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN`, registrada somente após os três pré-requisitos de encerramento em Drakonia.
- O retorno é **opcional**: nenhuma missão, flag, batalha ou bloqueio de rota foi acrescentado. Elya continua oferecendo as Poké Bolas pendentes antes do diálogo final e mantém o atendimento de cura depois dele.
- A pedra ancestral indica visualmente o fim do sinal, o aviso da vila passa a divulgar o encerramento da crise, Kael reconhece a recuperação da floresta, e Elya encerra o arco do Riolu inicial.
- Teste estático acrescentado em `tests/test_eryon_eclipse_finale.py` para garantir as quatro reações, a prioridade do kit e a preservação da primeira insígnia. O jogo ainda requer compilação e verificação de diálogos no Delta.

## Resposta dos oito líderes ao desfecho Eclipse (15/10/2026)

- Conectado o encerramento opcional da rede de cristais em Drakonia aos diálogos pós-insígnia dos oito líderes: Kael já reconhece a recuperação de Lumina; Volt comenta a eletricidade de Neonara; Bjorn, o gelo de Frostheim; Tessa, as ruínas de Arkhara; Nyx, o encerramento das cargas de Umbra; Kaio, a usina de Ignivar; Lyra, a observação astronômica de Lunaris; e Ryu, a segurança do santuário de Drakonia.
- Reutilizada exclusivamente `FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN`, sem criar flags, treinadores, insígnias, recompensas ou viagens obrigatórias. Nenhuma equipe de Pokémon, nível ou script original de batalha foi substituído.
- As falas originais dos líderes e os desdobramentos intermediários de Tessa continuam acessíveis enquanto o desfecho da Eclipse não ocorreu. Novo teste integrado à descoberta automática `test_eryon_eclipse_finale.py` valida os oito ramos, flags e ausência de novos efeitos.
- **Arte e execução:** as ilustrações conceituais dos líderes apresentadas no chat não são sprites incorporados à ROM. Seus retratos de batalha atuais ainda são provisórios; a compilação do HEAD e o playtest no Delta são pendências separadas.

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
