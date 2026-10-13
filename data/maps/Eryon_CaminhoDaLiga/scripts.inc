Eryon_CaminhoDaLiga_MapScripts::
	.byte 0

@ League road accessible on foot; the League facility is not yet built.
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
