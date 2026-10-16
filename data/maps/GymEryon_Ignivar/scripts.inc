GymEryonIgnivar_MapScripts::
	.byte 0

GymEryonIgnivar_EventScript_Leader::
	goto_if_set FLAG_BADGE06_GET, EryonIgnivar_EventScript_GymLeader
	goto_if_unset FLAG_ERYON_GYM_IGNIVAR_READY, GymEryonIgnivar_EventScript_NotReady
	goto EryonIgnivar_EventScript_GymLeader

GymEryonIgnivar_EventScript_NotReady::
	lock
	faceplayer
	msgbox GymEryonIgnivar_Text_NotReady, MSGBOX_DEFAULT
	release
	end

GymEryonIgnivar_EventScript_Guide::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_GYM_IGNIVAR_READY, GymEryonIgnivar_EventScript_GuideReady
	msgbox GymEryonIgnivar_Text_Guide, MSGBOX_DEFAULT
	release
	end

GymEryonIgnivar_EventScript_GuideReady::
	msgbox GymEryonIgnivar_Text_GuideReady, MSGBOX_DEFAULT
	release
	end

GymEryonIgnivar_EventScript_First::
	lock
	goto_if_set FLAG_ERYON_GYM_IGNIVAR_PRIMED, GymEryonIgnivar_EventScript_FirstAgain
	msgbox GymEryonIgnivar_Text_First, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GYM_IGNIVAR_PRIMED
	release
	end

GymEryonIgnivar_EventScript_FirstAgain::
	msgbox GymEryonIgnivar_Text_FirstAgain, MSGBOX_DEFAULT
	release
	end

GymEryonIgnivar_EventScript_Second::
	lock
	goto_if_unset FLAG_ERYON_GYM_IGNIVAR_PRIMED, GymEryonIgnivar_EventScript_SecondEarly
	goto_if_set FLAG_ERYON_GYM_IGNIVAR_READY, GymEryonIgnivar_EventScript_SecondAgain
	msgbox GymEryonIgnivar_Text_Second, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GYM_IGNIVAR_READY
	release
	end

GymEryonIgnivar_EventScript_SecondEarly::
	msgbox GymEryonIgnivar_Text_SecondEarly, MSGBOX_DEFAULT
	release
	end

GymEryonIgnivar_EventScript_SecondAgain::
	msgbox GymEryonIgnivar_Text_SecondAgain, MSGBOX_DEFAULT
	release
	end

GymEryonIgnivar_EventScript_Exit::
	lock
	msgbox GymEryonIgnivar_Text_Exit, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, GymEryonIgnivar_EventScript_Stay
	closemessage
	warp MAP_ERYON_IGNIVAR, 35, 30
	waitstate
	end

GymEryonIgnivar_EventScript_Stay::
	closemessage
	release
	end

GymEryonIgnivar_Text_Guide:
	.string "GUIA: Bem-vindo ao\n"
	.string "GINASIO de IGNIVAR.\p"
	.string "Ative o painel esquerdo\n"
	.string "e depois o direito.$"

GymEryonIgnivar_Text_GuideReady:
	.string "GUIA: FORJA liberado!\p"
	.string "O lider espera ao norte.\n"
	.string "Boa sorte no desafio!$"

GymEryonIgnivar_Text_First:
	.string "PAINEL FORNALHAS:\p"
	.string "Primeira etapa concluida.\n"
	.string "Busque o segundo sinal.$"

GymEryonIgnivar_Text_FirstAgain:
	.string "PAINEL FORNALHAS:\n"
	.string "Sinal registrado.$"

GymEryonIgnivar_Text_Second:
	.string "PAINEL PRESSAO:\p"
	.string "Dois sinais em harmonia.\n"
	.string "O desafio foi liberado!$"

GymEryonIgnivar_Text_SecondEarly:
	.string "PAINEL PRESSAO:\p"
	.string "Falta ativar o painel\n"
	.string "do lado esquerdo.$"

GymEryonIgnivar_Text_SecondAgain:
	.string "PAINEL PRESSAO:\n"
	.string "Ressonancia estabilizada.$"

GymEryonIgnivar_Text_NotReady:
	.string "LIDER: Antes da batalha,\n"
	.string "resolva os dois paineis\p"
	.string "na ordem indicada!$"

GymEryonIgnivar_Text_Exit:
	.string "Sair do GINASIO agora?$"
