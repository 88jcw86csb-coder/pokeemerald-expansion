Eryon_CaminhoDaLiga_MapScripts::
	.byte 0

@ League road accessible on foot, linking the Star Grotto to the League capital.
EryonLigaCaminho_EventScript_RouteGuardian::
	lock
	faceplayer
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
	goto_if_set FLAG_ERYON_QUALIFIED, EryonLigaCaminho_EventScript_LigaCourierAfter
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
