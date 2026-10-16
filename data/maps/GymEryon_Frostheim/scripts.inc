GymEryonFrostheim_MapScripts::
	.byte 0

GymEryonFrostheim_EventScript_Leader::
	goto_if_set FLAG_BADGE03_GET, EryonFrostheim_EventScript_Bjorn
	goto_if_unset FLAG_ERYON_GYM_FROSTHEIM_READY, GymEryonFrostheim_EventScript_NotReady
	goto EryonFrostheim_EventScript_Bjorn

GymEryonFrostheim_EventScript_NotReady::
	lock
	faceplayer
	msgbox GymEryonFrostheim_Text_NotReady, MSGBOX_DEFAULT
	release
	end

GymEryonFrostheim_EventScript_Guide::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_GYM_FROSTHEIM_READY, GymEryonFrostheim_EventScript_GuideReady
	msgbox GymEryonFrostheim_Text_Guide, MSGBOX_DEFAULT
	release
	end

GymEryonFrostheim_EventScript_GuideReady::
	msgbox GymEryonFrostheim_Text_GuideReady, MSGBOX_DEFAULT
	release
	end

GymEryonFrostheim_EventScript_First::
	lock
	goto_if_set FLAG_ERYON_GYM_FROSTHEIM_PRIMED, GymEryonFrostheim_EventScript_FirstAgain
	msgbox GymEryonFrostheim_Text_First, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GYM_FROSTHEIM_PRIMED
	release
	end

GymEryonFrostheim_EventScript_FirstAgain::
	msgbox GymEryonFrostheim_Text_FirstAgain, MSGBOX_DEFAULT
	release
	end

GymEryonFrostheim_EventScript_Second::
	lock
	goto_if_unset FLAG_ERYON_GYM_FROSTHEIM_PRIMED, GymEryonFrostheim_EventScript_SecondEarly
	goto_if_set FLAG_ERYON_GYM_FROSTHEIM_READY, GymEryonFrostheim_EventScript_SecondAgain
	msgbox GymEryonFrostheim_Text_Second, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GYM_FROSTHEIM_READY
	release
	end

GymEryonFrostheim_EventScript_SecondEarly::
	msgbox GymEryonFrostheim_Text_SecondEarly, MSGBOX_DEFAULT
	release
	end

GymEryonFrostheim_EventScript_SecondAgain::
	msgbox GymEryonFrostheim_Text_SecondAgain, MSGBOX_DEFAULT
	release
	end

GymEryonFrostheim_EventScript_Exit::
	lock
	msgbox GymEryonFrostheim_Text_Exit, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, GymEryonFrostheim_EventScript_Stay
	closemessage
	warp MAP_ERYON_FROSTHEIM, 34, 26
	waitstate
	end

GymEryonFrostheim_EventScript_Stay::
	closemessage
	release
	end

GymEryonFrostheim_Text_Guide:
	.string "GUIA: Bem-vindo ao\n"
	.string "GINASIO de FROSTHEIM.\p"
	.string "Ative o painel esquerdo\n"
	.string "e depois o direito.$"

GymEryonFrostheim_Text_GuideReady:
	.string "GUIA: GELO liberado!\p"
	.string "O lider espera ao norte.\n"
	.string "Boa sorte no desafio!$"

GymEryonFrostheim_Text_First:
	.string "PAINEL VENTOS:\p"
	.string "Primeira etapa concluida.\n"
	.string "Busque o segundo sinal.$"

GymEryonFrostheim_Text_FirstAgain:
	.string "PAINEL VENTOS:\n"
	.string "Sinal registrado.$"

GymEryonFrostheim_Text_Second:
	.string "PAINEL OBSERVATORIO:\p"
	.string "Dois sinais em harmonia.\n"
	.string "O desafio foi liberado!$"

GymEryonFrostheim_Text_SecondEarly:
	.string "PAINEL OBSERVATORIO:\p"
	.string "Falta ativar o painel\n"
	.string "do lado esquerdo.$"

GymEryonFrostheim_Text_SecondAgain:
	.string "PAINEL OBSERVATORIO:\n"
	.string "Ressonancia estabilizada.$"

GymEryonFrostheim_Text_NotReady:
	.string "LIDER: Antes da batalha,\n"
	.string "resolva os dois paineis\p"
	.string "na ordem indicada!$"

GymEryonFrostheim_Text_Exit:
	.string "Sair do GINASIO agora?$"
