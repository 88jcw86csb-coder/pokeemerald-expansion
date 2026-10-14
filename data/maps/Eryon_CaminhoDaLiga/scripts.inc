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
