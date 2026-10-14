Eryon_CaminhoDaLiga_MapScripts::
	.byte 0

@ League road accessible on foot, linking the Star Grotto to the League capital.
EryonLigaCaminho_EventScript_RouteGuardian::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonLigaCaminho_EventScript_GuardianChampion
	goto_if_set FLAG_ERYON_QUALIFIED, EryonLigaCaminho_EventScript_GuardianQualified
	goto_if_set FLAG_ERYON_GROTTO_ECLIPSE_SCOUT_DEFEATED, EryonLigaCaminho_EventScript_GuardianScoutDefeated
	goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, EryonLigaCaminho_EventScript_GuardianRelayDisabled
	msgbox EryonLigaCaminho_Text_Guardian, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_Medic::
	lock
	faceplayer
	msgbox EryonLigaCaminho_Text_Medic, MSGBOX_DEFAULT
	special HealPlayerParty
	release
	end

EryonLigaCaminho_EventScript_Observer::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_LEAGUE_PARK_ESPURR_RESOLVED, EryonLigaCaminho_EventScript_ObserverParkRestored
	goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, EryonLigaCaminho_EventScript_ObserverRelayOff
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonLigaCaminho_EventScript_ObserverReported
	goto_if_set FLAG_ERYON_STAR_CHART_READ, EryonLigaCaminho_EventScript_ObserverClue
	msgbox EryonLigaCaminho_Text_ObserverBefore, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_ObserverClue::
	msgbox EryonLigaCaminho_Text_ObserverClue, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_BadgeBoard::
	lock
	msgbox EryonLigaCaminho_Text_BadgeBoard, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_LeagueGate::
	lock
	msgbox EryonLigaCaminho_Text_LeagueGate, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_Guardian:
	.string "GUARDIAO: Bem-vindo\n"
	.string "ao CAMINHO DA LIGA!\p"
	.string "Toda a travessia pode\n"
	.string "ser feita a pe.$"

EryonLigaCaminho_Text_Medic:
	.string "SOCORRISTA: Ninguem\n"
	.string "precisa de HM aqui.\p"
	.string "Vou curar seus Pokemon\n"
	.string "antes do ultimo trecho.$"

EryonLigaCaminho_Text_ObserverBefore:
	.string "PESQUISADOR: O brilho\n"
	.string "das estrelas mudou.\p"
	.string "Investigue a gruta\n"
	.string "ao oeste desta rota.$"

EryonLigaCaminho_Text_ObserverClue:
	.string "PESQUISADOR: A carta\n"
	.string "confirmou as ligacoes!\p"
	.string "A ECLIPSE preparou\n"
	.string "uma grande antena.$"

EryonLigaCaminho_Text_BadgeBoard:
	.string "TRILHA DA LIGA:\n"
	.string "Treine sua equipe.\p"
	.string "As HMs sao opcionais.\n"
	.string "Nao bloqueiam a rota.$"

EryonLigaCaminho_Text_LeagueGate:
	.string "LESTE: CIDADE DA LIGA!\n"
	.string "Entrada da competicao.\p"
	.string "O edificio principal\n"
	.string "fica na praca central.$"

@ Optional route investigation: the Eclipse scouts trail the Star Chart.
@ These events do not require HMs or block access to the League.
EryonLigaCaminho_EventScript_ScoutWitness::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonLigaCaminho_EventScript_ScoutWitnessChampion
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonLigaCaminho_EventScript_ScoutWitnessReported
	goto_if_set FLAG_ERYON_STAR_CHART_READ, EryonLigaCaminho_EventScript_ScoutWitnessAfter
	msgbox EryonLigaCaminho_Text_ScoutWitnessBefore, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_ScoutWitnessAfter::
	msgbox EryonLigaCaminho_Text_ScoutWitnessAfter, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_LigaCourier::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonLigaCaminho_EventScript_LigaCourierChampion
	goto_if_set FLAG_ERYON_QUALIFIED, EryonLigaCaminho_EventScript_LigaCourierAfter
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonLigaCaminho_EventScript_LigaCourierEvidence
	msgbox EryonLigaCaminho_Text_LigaCourierBefore, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_LigaCourierAfter::
	msgbox EryonLigaCaminho_Text_LigaCourierAfter, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_ScoutWitnessBefore:
	.string "VIAJANTE: Vi pessoas\n"
	.string "de preto perto da\n"
	.string "GRUTA DAS ESTRELAS.\p"
	.string "Pareciam procurar\n"
	.string "um mapa antigo.$"

EryonLigaCaminho_Text_ScoutWitnessAfter:
	.string "VIAJANTE: A ECLIPSE\n"
	.string "seguiu a Carta Estelar!\p"
	.string "Um deles foi para a\n"
	.string "grande CIDADE DA LIGA.$"

EryonLigaCaminho_Text_LigaCourierBefore:
	.string "MENSAGEIRO: A LIGA\n"
	.string "recebe treinadores\n"
	.string "de toda a regiao.\p"
	.string "Siga a leste para a\n"
	.string "cidade e o torneio.$"

EryonLigaCaminho_Text_LigaCourierAfter:
	.string "MENSAGEIRO: Voce\n"
	.string "venceu as oito fases!\p"
	.string "A equipe da LIGA\n"
	.string "aguarda na cidade.$"

@ The final route acknowledges the League investigation outcome.
EryonLigaCaminho_EventScript_ObserverReported::
	msgbox EryonLigaCaminho_Text_ObserverReported, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_ObserverReported:
	.string "PESQUISADOR: A LIGA\n"
	.string "recebeu as provas!\p"
	.string "Os guardas seguem\n"
	.string "a rede da ECLIPSE.\p"
	.string "Boa sorte no torneio!$"

@ The League road observer confirms the optional relay sabotage.
EryonLigaCaminho_EventScript_ObserverRelayOff::
	msgbox EryonLigaCaminho_Text_ObserverRelayOff, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_ObserverRelayOff:
	.string "PESQUISADOR: O sinal\n"
	.string "na gruta se apagou!\p"
	.string "A rede da ECLIPSE\n"
	.string "perdeu uma antena.\p"
	.string "Continue sua jornada\n"
	.string "ate a CIDADE DA LIGA.$"

@ Optional supplies are granted once; a full bag does not consume the cache.
EryonLigaCaminho_EventScript_SupplyCache::
	lock
	goto_if_set FLAG_ERYON_LEAGUE_ROAD_CACHE_TAKEN, EryonLigaCaminho_EventScript_CacheEmpty
	msgbox EryonLigaCaminho_Text_CacheFound, MSGBOX_DEFAULT
	giveitem ITEM_MAX_POTION
	goto_if_eq VAR_RESULT, FALSE, EryonLigaCaminho_EventScript_CacheFull
	setflag FLAG_ERYON_LEAGUE_ROAD_CACHE_TAKEN
	release
	end

EryonLigaCaminho_EventScript_CacheFull::
	msgbox EryonLigaCaminho_Text_CacheFull, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_CacheEmpty::
	msgbox EryonLigaCaminho_Text_CacheEmpty, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_CacheFound:
	.string "Um estojo de socorro\n"
	.string "escondido na trilha!\p"
	.string "Ha um MAX POTION\n"
	.string "guardado aqui.$"

EryonLigaCaminho_Text_CacheFull:
	.string "Sua BOLSA esta cheia.\p"
	.string "O remedio ficara\n"
	.string "aqui ate voce voltar.$"

EryonLigaCaminho_Text_CacheEmpty:
	.string "O estojo esta vazio.\p"
	.string "Voce ja recolheu\n"
	.string "os suprimentos.$"

@ After the optional Star Grotto battle, the last route recognizes the victory.
EryonLigaCaminho_EventScript_GuardianScoutDefeated::
	msgbox EryonLigaCaminho_Text_GuardianScoutDefeated, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_GuardianScoutDefeated:
	.string "GUARDIAO: Soube que\n"
	.string "venceu um ECLIPSE\n"
	.string "na Gruta das Estrelas!\p"
	.string "A estrada esta livre.\n"
	.string "Siga para a LIGA!$"


@ The final road ecosystem responds after the League capital garden recovers.
EryonLigaCaminho_EventScript_ObserverParkRestored::
	msgbox EryonLigaCaminho_Text_ObserverParkRestored, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_ObserverParkRestored:
	.string "PESQUISADOR: O ESPURR\n"
	.string "da LIGA foi estudado!\p"
	.string "A natureza se recupera\n"
	.string "quando o sinal da\n"
	.string "ECLIPSE desaparece.$"


@ Optional memorial reached by the new northern path between both summits.
@ Does not award items, set flags, block access or modify League battles.
EryonLigaCaminho_EventScript_StarMemorial::
	lock
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonLigaCaminho_EventScript_StarMemorialChampion
	goto_if_set FLAG_ERYON_QUALIFIED, EryonLigaCaminho_EventScript_StarMemorialQualified
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonLigaCaminho_EventScript_StarMemorialReported
	goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, EryonLigaCaminho_EventScript_StarMemorialSilent
	goto_if_set FLAG_BADGE08_GET, EryonLigaCaminho_EventScript_StarMemorialBadges
	msgbox EryonLigaCaminho_Text_StarMemorialBefore, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_StarMemorialReported::
	msgbox EryonLigaCaminho_Text_StarMemorialReported, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_StarMemorialSilent::
	msgbox EryonLigaCaminho_Text_StarMemorialSilent, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_StarMemorialBadges::
	msgbox EryonLigaCaminho_Text_StarMemorialBadges, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_StarMemorialBefore:
	.string "MEMORIAL ESTELAR:\p"
	.string "Oito caminhos antigos\n"
	.string "se encontram no cume.\p"
	.string "Dois mirantes revelam\n"
	.string "a rota por Eryon.$"

EryonLigaCaminho_Text_StarMemorialBadges:
	.string "Suas oito INSIGNIAS\n"
	.string "brilham diante do arco!\p"
	.string "A LIGA fica alem\n"
	.string "da estrada do leste.$"

EryonLigaCaminho_Text_StarMemorialSilent:
	.string "O eco artificial\n"
	.string "da ECLIPSE se calou.\p"
	.string "As estrelas agora\n"
	.string "refletem na montanha.$"

EryonLigaCaminho_Text_StarMemorialReported:
	.string "MEMORIAL ESTELAR:\p"
	.string "A LIGA conhece a rede\n"
	.string "secreta da ECLIPSE.\p"
	.string "Os viajantes voltam\n"
	.string "a subir estes montes.$"


@ The roadside guardian hears that the underground Eclipse signal was stopped.
EryonLigaCaminho_EventScript_GuardianRelayDisabled:
	msgbox EryonLigaCaminho_Text_GuardianRelayDisabled, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_GuardianRelayDisabled:
	.string "GUARDIAO: A ECLIPSE\n"
	.string "perdeu a antena da gruta!\p"
	.string "O acesso a CIDADE\n"
	.string "DA LIGA segue livre.$"


@ After qualifying, the road directs the player to recovery, not another qualifier.
@ After becoming Champion, the original road remains open for revisits.
EryonLigaCaminho_EventScript_GuardianQualified::
	msgbox EryonLigaCaminho_Text_GuardianQualified, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_GuardianChampion::
	msgbox EryonLigaCaminho_Text_GuardianChampion, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_LigaCourierEvidence::
	msgbox EryonLigaCaminho_Text_LigaCourierEvidence, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_LigaCourierChampion::
	msgbox EryonLigaCaminho_Text_LigaCourierChampion, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_GuardianQualified:
	.string "GUARDIAO: Oito duelos\n"
	.string "vencidos na LIGA!\p"
	.string "Recupere seus Pokemon\n"
	.string "antes da ELITE FOUR.$"

EryonLigaCaminho_Text_GuardianChampion:
	.string "GUARDIAO: O CAMPEAO\n"
	.string "retorna a esta trilha!\p"
	.string "A estrada continua\n"
	.string "aberta para explorar.$"

EryonLigaCaminho_Text_LigaCourierEvidence:
	.string "MENSAGEIRO: A LIGA\n"
	.string "recebeu as provas\n"
	.string "contra a ECLIPSE.\p"
	.string "O torneio segue\n"
	.string "na cidade a leste.$"

EryonLigaCaminho_Text_LigaCourierChampion:
	.string "MENSAGEIRO: A LIGA\n"
	.string "tem um novo CAMPEAO!\p"
	.string "Os oito duelos e a\n"
	.string "ELITE foram superados.$"


@ The road witness follows the evidence after it has been officially filed.
@ Revisits remain optional and never reset the tournament or Eclipse story.
EryonLigaCaminho_EventScript_ScoutWitnessReported::
	msgbox EryonLigaCaminho_Text_ScoutWitnessReported, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_ScoutWitnessReported:
	.string "VIAJANTE: A LIGA\n"
	.string "recebeu as provas!\p"
	.string "A ECLIPSE perdeu\n"
	.string "seu esconderijo.\p"
	.string "Mas a investigacao\n"
	.string "continua em ERYON.$"


@ Summit epilogue: old northern mountain route remains accessible after the tournament.
@ These are alternate texts on the existing memorial, without new events or flags.
EryonLigaCaminho_EventScript_StarMemorialQualified::
	msgbox EryonLigaCaminho_Text_StarMemorialQualified, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_StarMemorialChampion::
	msgbox EryonLigaCaminho_Text_StarMemorialChampion, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_StarMemorialQualified:
	.string "MEMORIAL ESTELAR:\p"
	.string "Oito vitorias acendem\n"
	.string "a trilha das estrelas!\p"
	.string "A ELITE FOUR espera\n"
	.string "na cidade a leste.$"

EryonLigaCaminho_Text_StarMemorialChampion:
	.string "MEMORIAL ESTELAR:\p"
	.string "O CAMPEAO de ERYON\n"
	.string "retorna a montanha!\p"
	.string "Mesmo apos a LIGA,\n"
	.string "ha caminhos a explorar.$"


@ On a return trip after the League, the original trail witness remembers the Champion.
@ This is an optional epilogue, with no new flag or battle.
EryonLigaCaminho_EventScript_ScoutWitnessChampion::
	msgbox EryonLigaCaminho_Text_ScoutWitnessChampion, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_ScoutWitnessChampion:
	.string "VIAJANTE: O CAMPEAO\n"
	.string "voltou pela trilha!\p"
	.string "A rede da ECLIPSE\n"
	.string "ainda sera estudada.\p"
	.string "Ha caminhos antigos\n"
	.string "a descobrir em ERYON.$"


@ Optional Crystal Survey marker on the existing walkable League road.
@ This environmental discovery reacts to Eclipse progress, never gates traversal.
EryonLigaCaminho_EventScript_CrystalSurvey::
	lock
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonLigaCaminho_EventScript_CrystalSurveyChampion
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonLigaCaminho_EventScript_CrystalSurveyFiled
	goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, EryonLigaCaminho_EventScript_CrystalSurveyQuiet
	msgbox EryonLigaCaminho_Text_CrystalSurveyBefore, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_CrystalSurveyQuiet::
	msgbox EryonLigaCaminho_Text_CrystalSurveyQuiet, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_CrystalSurveyFiled::
	msgbox EryonLigaCaminho_Text_CrystalSurveyFiled, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_CrystalSurveyChampion::
	msgbox EryonLigaCaminho_Text_CrystalSurveyChampion, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_CrystalSurveyBefore:
	.string "MARCO DOS CRISTAIS:\p"
	.string "Pulsos estranhos vem\n"
	.string "da GRUTA DAS ESTRELAS.\p"
	.string "Siga a oeste para\n"
	.string "investigar a origem.$"

EryonLigaCaminho_Text_CrystalSurveyQuiet:
	.string "MARCO DOS CRISTAIS:\p"
	.string "O pulso da ECLIPSE\n"
	.string "foi interrompido!\p"
	.string "O vale recupera\n"
	.string "seu brilho natural.$"

EryonLigaCaminho_Text_CrystalSurveyFiled:
	.string "MARCO DOS CRISTAIS:\p"
	.string "A LIGA catalogou\n"
	.string "as provas da ECLIPSE.\p"
	.string "Os estudos continuam\n"
	.string "pelas rotas de ERYON.$"

EryonLigaCaminho_Text_CrystalSurveyChampion:
	.string "MARCO DOS CRISTAIS:\p"
	.string "O CAMPEAO retornou!\p"
	.string "A trilha permanece\n"
	.string "aberta a exploradores.$"


@ Eastern overlook on the existing road; visits remain optional and HM-free.
@ The lookout foreshadows the city's Eclipse investigation without changing flags.
EryonLigaCaminho_EventScript_EastLookout::
	lock
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonLigaCaminho_EventScript_EastLookoutChampion
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonLigaCaminho_EventScript_EastLookoutFiled
	goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, EryonLigaCaminho_EventScript_EastLookoutQuiet
	msgbox EryonLigaCaminho_Text_EastLookoutBefore, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_EastLookoutQuiet::
	msgbox EryonLigaCaminho_Text_EastLookoutQuiet, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_EastLookoutFiled::
	msgbox EryonLigaCaminho_Text_EastLookoutFiled, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_EastLookoutChampion::
	msgbox EryonLigaCaminho_Text_EastLookoutChampion, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_EastLookoutBefore:
	.string "MIRANTE LESTE:\p"
	.string "A cidade da LIGA\n"
	.string "surge entre os picos.\p"
	.string "Uma luz estranha vem\n"
	.string "da gruta a oeste.$"

EryonLigaCaminho_Text_EastLookoutQuiet:
	.string "MIRANTE LESTE:\p"
	.string "O sinal da ECLIPSE\n"
	.string "na gruta desapareceu.\p"
	.string "As luzes da cidade\n"
	.string "brilham sem interferencia.$"

EryonLigaCaminho_Text_EastLookoutFiled:
	.string "MIRANTE LESTE:\p"
	.string "Guardas investigam\n"
	.string "a rede da ECLIPSE.\p"
	.string "A LIGA continua aberta\n"
	.string "a novos desafiantes.$"

EryonLigaCaminho_Text_EastLookoutChampion:
	.string "MIRANTE LESTE:\p"
	.string "As bandeiras da LIGA\n"
	.string "celebram o CAMPEAO!\p"
	.string "Ainda ha rotas para\n"
	.string "explorar em ERYON.$"


@ Newly walkable eastern summit alcove. An optional observation site above the road.
@ The League and Eclipse story flags only change its description.
EryonLigaCaminho_EventScript_SummitAlcove::
	lock
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonLigaCaminho_EventScript_SummitAlcoveChampion
	goto_if_set FLAG_ERYON_QUALIFIED, EryonLigaCaminho_EventScript_SummitAlcoveQualified
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonLigaCaminho_EventScript_SummitAlcoveFiled
	msgbox EryonLigaCaminho_Text_SummitAlcoveBefore, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_SummitAlcoveFiled::
	msgbox EryonLigaCaminho_Text_SummitAlcoveFiled, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_SummitAlcoveChampion::
	msgbox EryonLigaCaminho_Text_SummitAlcoveChampion, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_SummitAlcoveBefore:
	.string "NICHO DO CUME:\p"
	.string "Daqui se ve a LIGA\n"
	.string "e a GRUTA ESTELAR.\p"
	.string "Marcas de cristais\n"
	.string "cortam a pedra antiga.$"

EryonLigaCaminho_Text_SummitAlcoveFiled:
	.string "NICHO DO CUME:\p"
	.string "Os estudiosos da LIGA\n"
	.string "catalogaram os cristais.\p"
	.string "A ECLIPSE ja nao pode\n"
	.string "ocultar suas rotas.$"

EryonLigaCaminho_Text_SummitAlcoveChampion:
	.string "NICHO DO CUME:\p"
	.string "O CAMPEAO avista a\n"
	.string "cidade do alto!\p"
	.string "A montanha ainda tem\n"
	.string "segredos a explorar.$"


@ During the League's eight-win qualification, summit explorers can revisit
@ the optional mountain alcove and receive accurate recovery directions.
EryonLigaCaminho_EventScript_SummitAlcoveQualified::
	msgbox EryonLigaCaminho_Text_SummitAlcoveQualified, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_SummitAlcoveQualified:
	.string "NICHO DO CUME:\p"
	.string "Oito vitorias ecoam\n"
	.string "por esta montanha!\p"
	.string "A ELITE FOUR espera\n"
	.string "na cidade abaixo.$"


@ The newly opened northern shortcut bears survey marks from the Eclipse network.
@ This optional landmark is revisitable and does not change badge or League flags.
EryonLigaCaminho_EventScript_NorthShortcut::
	lock
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonLigaCaminho_EventScript_NorthShortcutChampion
	goto_if_set FLAG_ERYON_QUALIFIED, EryonLigaCaminho_EventScript_NorthShortcutQualified
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonLigaCaminho_EventScript_NorthShortcutFiled
	goto_if_set FLAG_ERYON_STAR_CHART_READ, EryonLigaCaminho_EventScript_NorthShortcutChart
	msgbox EryonLigaCaminho_Text_NorthShortcutBefore, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_NorthShortcutChart::
	msgbox EryonLigaCaminho_Text_NorthShortcutChart, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_NorthShortcutFiled::
	msgbox EryonLigaCaminho_Text_NorthShortcutFiled, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_NorthShortcutChampion::
	msgbox EryonLigaCaminho_Text_NorthShortcutChampion, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_NorthShortcutBefore:
	.string "ATALHO NORTE:\p"
	.string "Marcas antigas indicam\n"
	.string "um caminho entre picos.\p"
	.string "O memorial fica a oeste\n"
	.string "da passagem de pedra.$"

EryonLigaCaminho_Text_NorthShortcutChart:
	.string "ATALHO NORTE:\p"
	.string "Os simbolos combinam\n"
	.string "com a CARTA ESTELAR!\p"
	.string "Alguem transportou\n"
	.string "cristais por este atalho.$"

EryonLigaCaminho_Text_NorthShortcutFiled:
	.string "ATALHO NORTE:\p"
	.string "As provas da ECLIPSE\n"
	.string "revelaram esta trilha.\p"
	.string "A LIGA investiga as\n"
	.string "rotas pela montanha.$"

EryonLigaCaminho_Text_NorthShortcutChampion:
	.string "ATALHO NORTE:\p"
	.string "O CAMPEAO encontra\n"
	.string "um velho atalho!\p"
	.string "As montanhas de ERYON\n"
	.string "seguem cheias de vida.$"


@ Once the eight-match qualifier is finished, this mountain marker points
@ to the recovery chamber without modifying qualification flags.
EryonLigaCaminho_EventScript_NorthShortcutQualified::
	msgbox EryonLigaCaminho_Text_NorthShortcutQualified, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_NorthShortcutQualified:
	.string "ATALHO NORTE:\p"
	.string "Oito vitorias na LIGA!\p"
	.string "Recupere seus Pokemon\n"
	.string "antes da ELITE FOUR.$"


@ Optional Kalos bird encounter on the newly opened northern ridge.
@ The bird may return after a battle; no new flag or progress gate is needed.
EryonLigaCaminho_EventScript_RidgeFletchling::
	lock
	msgbox EryonLigaCaminho_Text_RidgeFletchling, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonLigaCaminho_EventScript_RidgeFletchlingLeave
	closemessage
	setwildbattle SPECIES_FLETCHLING, 56
	waitse
	playmoncry SPECIES_FLETCHLING, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, EryonLigaCaminho_EventScript_RidgeFletchlingDone
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, EryonLigaCaminho_EventScript_RidgeFletchlingDone
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, EryonLigaCaminho_EventScript_RidgeFletchlingEscaped
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, EryonLigaCaminho_EventScript_RidgeFletchlingEscaped
	release
	end

EryonLigaCaminho_EventScript_RidgeFletchlingDone::
	msgbox EryonLigaCaminho_Text_RidgeFletchlingDone, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_RidgeFletchlingEscaped::
	msgbox EryonLigaCaminho_Text_RidgeFletchlingEscaped, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_RidgeFletchlingLeave::
	closemessage
	release
	end

EryonLigaCaminho_Text_RidgeFletchling:
	.string "Um FLETCHLING selvagem\n"
	.string "observa a trilha!\p"
	.string "Parece proteger seu\n"
	.string "poleiro no cume.\p"
	.string "Aproximar-se?$"

EryonLigaCaminho_Text_RidgeFletchlingDone:
	.string "O FLETCHLING deixou\n"
	.string "o poleiro tranquilo.\p"
	.string "Outros voam ao longe.$"

EryonLigaCaminho_Text_RidgeFletchlingEscaped:
	.string "FLETCHLING voou\n"
	.string "sobre os picos!\p"
	.string "Talvez reapareca.$"


@ Optional clearing reached from the new upper northern trail.
@ No flags, trainer state or League access are changed here.
EryonLigaCaminho_EventScript_BirdwatchClearing::
	lock
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonLigaCaminho_EventScript_BirdwatchChampion
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonLigaCaminho_EventScript_BirdwatchEvidence
	msgbox EryonLigaCaminho_Text_BirdwatchBefore, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_BirdwatchEvidence::
	msgbox EryonLigaCaminho_Text_BirdwatchEvidence, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_BirdwatchChampion::
	msgbox EryonLigaCaminho_Text_BirdwatchChampion, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_BirdwatchBefore:
	.string "CLAREIRA DO VENTO:\p"
	.string "FLETCHLING sobrevoam\n"
	.string "o velho atalho.\p"
	.string "Marcas de cristais\n"
	.string "brilham entre as penas.$"

EryonLigaCaminho_Text_BirdwatchEvidence:
	.string "CLAREIRA DO VENTO:\p"
	.string "A pesquisa da ECLIPSE\n"
	.string "agora e conhecida.\p"
	.string "Os FLETCHLING voltaram\n"
	.string "a voar em paz.$"

EryonLigaCaminho_Text_BirdwatchChampion:
	.string "CLAREIRA DO VENTO:\p"
	.string "O CAMPEAO avista\n"
	.string "a cidade ao sul.\p"
	.string "O vento segue guiando\n"
	.string "novos treinadores.$"


@ Optional battle at the newly accessible windy clearing, off the main League road.
EryonLigaCaminho_EventScript_RidgeBirdwatcher::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_RIDGE_BIRDWATCHER_DEFEATED, EryonLigaCaminho_EventScript_RidgeBirdwatcherAfter
	msgbox EryonLigaCaminho_Text_RidgeBirdwatcherOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonLigaCaminho_EventScript_RidgeBirdwatcherDecline
	closemessage
	trainerbattle_single TRAINER_ERYON_RIDGE_BIRDWATCHER, EryonLigaCaminho_Text_RidgeBirdwatcherIntro, EryonLigaCaminho_Text_RidgeBirdwatcherLoss, EryonLigaCaminho_EventScript_RidgeBirdwatcherVictory, FALSE
	msgbox EryonLigaCaminho_Text_RidgeBirdwatcherAfter, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_RidgeBirdwatcherDecline::
	closemessage
	release
	end

EryonLigaCaminho_EventScript_RidgeBirdwatcherVictory::
	msgbox EryonLigaCaminho_Text_RidgeBirdwatcherVictory, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_RidgeBirdwatcherAfter::
	msgbox EryonLigaCaminho_Text_RidgeBirdwatcherAfter, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_RidgeBirdwatcherOffer:
	.string "ARI: Estudo as aves\n"
	.string "dos picos de ERYON!\p"
	.string "Quer uma batalha\n"
	.string "de treinamento?$"

EryonLigaCaminho_Text_RidgeBirdwatcherIntro:
	.string "ARI: Mostre como sua\n"
	.string "equipe enfrenta o vento!$"

EryonLigaCaminho_Text_RidgeBirdwatcherLoss:
	.string "ARI: Voce conhece\n"
	.string "os caminhos do ceu!$"

EryonLigaCaminho_Text_RidgeBirdwatcherVictory:
	.string "ARI: Meu estudo vai\n"
	.string "ajudar os viajantes.$"

EryonLigaCaminho_Text_RidgeBirdwatcherAfter:
	.string "ARI: Vi FLETCHLING\n"
	.string "ao longo do atalho.\p"
	.string "Proteja os Pokemon\n"
	.string "desta montanha.$"


@ Optional discovery on the original western ravine descent.
@ No new flags or gates: this landmark tracks story progress safely.
EryonLigaCaminho_EventScript_WestRavine::
	lock
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonLigaCaminho_EventScript_WestRavineChampion
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonLigaCaminho_EventScript_WestRavineReported
	goto_if_set FLAG_ERYON_STAR_CHART_READ, EryonLigaCaminho_EventScript_WestRavineChart
	msgbox EryonLigaCaminho_Text_WestRavineBefore, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_WestRavineChart::
	msgbox EryonLigaCaminho_Text_WestRavineChart, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_WestRavineReported::
	msgbox EryonLigaCaminho_Text_WestRavineReported, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_EventScript_WestRavineChampion::
	msgbox EryonLigaCaminho_Text_WestRavineChampion, MSGBOX_DEFAULT
	release
	end

EryonLigaCaminho_Text_WestRavineBefore:
	.string "DESFILADEIRO OESTE:\p"
	.string "A rocha tem marcas\n"
	.string "de antigos cristais.\p"
	.string "O vento segue por\n"
	.string "um caminho oculto.$"

EryonLigaCaminho_Text_WestRavineChart:
	.string "DESFILADEIRO OESTE:\p"
	.string "As marcas lembram\n"
	.string "a CARTA ESTELAR!\p"
	.string "A ECLIPSE pode ter\n"
	.string "usado esta passagem.$"

EryonLigaCaminho_Text_WestRavineReported:
	.string "DESFILADEIRO OESTE:\p"
	.string "A LIGA estuda as\n"
	.string "marcas da ECLIPSE.\p"
	.string "O desfiladeiro esta\n"
	.string "livre para viajantes.$"

EryonLigaCaminho_Text_WestRavineChampion:
	.string "DESFILADEIRO OESTE:\p"
	.string "O CAMPEAO contempla\n"
	.string "os picos de ERYON.\p"
	.string "Ainda ha misterios\n"
	.string "alem desta trilha.$"
