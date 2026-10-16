GymEryon_Neonara_MapScripts::
	.byte 0

GymEryonNeonara_EventScript_Leader::
	goto_if_set FLAG_BADGE02_GET, EryonNeonara_EventScript_GymLeader
	goto_if_unset FLAG_ERYON_GYM_NEONARA_READY, GymEryonNeonara_EventScript_NotReady
	goto EryonNeonara_EventScript_GymLeader

GymEryonNeonara_EventScript_NotReady::
	lock
	faceplayer
	msgbox GymEryonNeonara_Text_NotReady, MSGBOX_DEFAULT
	release
	end

GymEryonNeonara_EventScript_Guide::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_GYM_NEONARA_READY, GymEryonNeonara_EventScript_GuideReady
	msgbox GymEryonNeonara_Text_Guide, MSGBOX_DEFAULT
	release
	end

GymEryonNeonara_EventScript_GuideReady::
	msgbox GymEryonNeonara_Text_GuideReady, MSGBOX_DEFAULT
	release
	end

GymEryonNeonara_EventScript_First::
	lock
	goto_if_set FLAG_ERYON_GYM_NEONARA_PRIMED, GymEryonNeonara_EventScript_FirstAgain
	msgbox GymEryonNeonara_Text_First, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GYM_NEONARA_PRIMED
	release
	end

GymEryonNeonara_EventScript_FirstAgain::
	msgbox GymEryonNeonara_Text_FirstAgain, MSGBOX_DEFAULT
	release
	end

GymEryonNeonara_EventScript_Second::
	lock
	goto_if_unset FLAG_ERYON_GYM_NEONARA_PRIMED, GymEryonNeonara_EventScript_SecondEarly
	goto_if_set FLAG_ERYON_GYM_NEONARA_READY, GymEryonNeonara_EventScript_SecondAgain
	msgbox GymEryonNeonara_Text_Second, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GYM_NEONARA_READY
	release
	end

GymEryonNeonara_EventScript_SecondEarly::
	msgbox GymEryonNeonara_Text_SecondEarly, MSGBOX_DEFAULT
	release
	end

GymEryonNeonara_EventScript_SecondAgain::
	msgbox GymEryonNeonara_Text_SecondAgain, MSGBOX_DEFAULT
	release
	end

GymEryonNeonara_EventScript_Exit::
	lock
	msgbox GymEryonNeonara_Text_Exit, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, GymEryonNeonara_EventScript_Stay
	closemessage
	warp MAP_ERYON_NEONARA, 38, 27
	waitstate
	end

GymEryonNeonara_EventScript_Stay::
	closemessage
	release
	end

GymEryonNeonara_Text_Guide:
	.string "GUIA: Bem-vindo ao\n"
	.string "GINASIO de NEONARA.\p"
	.string "Ative o painel esquerdo\n"
	.string "e depois o direito.$"

GymEryonNeonara_Text_GuideReady:
	.string "GUIA: CIRCUITO liberado!\p"
	.string "O lider espera ao norte.\n"
	.string "Boa sorte no desafio!$"

GymEryonNeonara_Text_First:
	.string "PAINEL CIRCUITOS:\p"
	.string "Primeira etapa concluida.\n"
	.string "Busque o segundo sinal.$"

GymEryonNeonara_Text_FirstAgain:
	.string "PAINEL CIRCUITOS:\n"
	.string "Sinal registrado.$"

GymEryonNeonara_Text_Second:
	.string "PAINEL RESSONANCIA:\p"
	.string "Dois sinais em harmonia.\n"
	.string "O desafio foi liberado!$"

GymEryonNeonara_Text_SecondEarly:
	.string "PAINEL RESSONANCIA:\p"
	.string "Falta ativar o painel\n"
	.string "do lado esquerdo.$"

GymEryonNeonara_Text_SecondAgain:
	.string "PAINEL RESSONANCIA:\n"
	.string "Ressonancia estabilizada.$"

GymEryonNeonara_Text_NotReady:
	.string "LIDER: Antes da batalha,\n"
	.string "resolva os dois paineis\p"
	.string "na ordem indicada!$"

GymEryonNeonara_Text_Exit:
	.string "Sair do GINASIO agora?$"
