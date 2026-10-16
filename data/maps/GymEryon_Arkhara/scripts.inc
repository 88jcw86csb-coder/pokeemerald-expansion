GymEryon_Arkhara_MapScripts::
	.byte 0

GymEryonArkhara_EventScript_Leader::
	goto_if_set FLAG_BADGE04_GET, EryonArkhara_EventScript_Tessa
	goto_if_unset FLAG_ERYON_GYM_ARKHARA_READY, GymEryonArkhara_EventScript_NotReady
	goto EryonArkhara_EventScript_Tessa

GymEryonArkhara_EventScript_NotReady::
	lock
	faceplayer
	msgbox GymEryonArkhara_Text_NotReady, MSGBOX_DEFAULT
	release
	end

GymEryonArkhara_EventScript_Guide::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_GYM_ARKHARA_READY, GymEryonArkhara_EventScript_GuideReady
	msgbox GymEryonArkhara_Text_Guide, MSGBOX_DEFAULT
	release
	end

GymEryonArkhara_EventScript_GuideReady::
	msgbox GymEryonArkhara_Text_GuideReady, MSGBOX_DEFAULT
	release
	end

GymEryonArkhara_EventScript_First::
	lock
	goto_if_set FLAG_ERYON_GYM_ARKHARA_PRIMED, GymEryonArkhara_EventScript_FirstAgain
	msgbox GymEryonArkhara_Text_First, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GYM_ARKHARA_PRIMED
	release
	end

GymEryonArkhara_EventScript_FirstAgain::
	msgbox GymEryonArkhara_Text_FirstAgain, MSGBOX_DEFAULT
	release
	end

GymEryonArkhara_EventScript_Second::
	lock
	goto_if_unset FLAG_ERYON_GYM_ARKHARA_PRIMED, GymEryonArkhara_EventScript_SecondEarly
	goto_if_set FLAG_ERYON_GYM_ARKHARA_READY, GymEryonArkhara_EventScript_SecondAgain
	msgbox GymEryonArkhara_Text_Second, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GYM_ARKHARA_READY
	release
	end

GymEryonArkhara_EventScript_SecondEarly::
	msgbox GymEryonArkhara_Text_SecondEarly, MSGBOX_DEFAULT
	release
	end

GymEryonArkhara_EventScript_SecondAgain::
	msgbox GymEryonArkhara_Text_SecondAgain, MSGBOX_DEFAULT
	release
	end

GymEryonArkhara_EventScript_Exit::
	lock
	msgbox GymEryonArkhara_Text_Exit, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, GymEryonArkhara_EventScript_Stay
	closemessage
	warp MAP_ERYON_ARKHARA, 31, 27
	waitstate
	end

GymEryonArkhara_EventScript_Stay::
	closemessage
	release
	end

GymEryonArkhara_Text_Guide:
	.string "GUIA: Bem-vindo ao\n"
	.string "GINASIO de ARKHARA.\p"
	.string "Ative o painel esquerdo\n"
	.string "e depois o direito.$"

GymEryonArkhara_Text_GuideReady:
	.string "GUIA: RUINAS liberado!\p"
	.string "O lider espera ao norte.\n"
	.string "Boa sorte no desafio!$"

GymEryonArkhara_Text_First:
	.string "PAINEL RUNAS:\p"
	.string "Primeira etapa concluida.\n"
	.string "Busque o segundo sinal.$"

GymEryonArkhara_Text_FirstAgain:
	.string "PAINEL RUNAS:\n"
	.string "Sinal registrado.$"

GymEryonArkhara_Text_Second:
	.string "PAINEL MEMORIAS:\p"
	.string "Dois sinais em harmonia.\n"
	.string "O desafio foi liberado!$"

GymEryonArkhara_Text_SecondEarly:
	.string "PAINEL MEMORIAS:\p"
	.string "Falta ativar o painel\n"
	.string "do lado esquerdo.$"

GymEryonArkhara_Text_SecondAgain:
	.string "PAINEL MEMORIAS:\n"
	.string "Ressonancia estabilizada.$"

GymEryonArkhara_Text_NotReady:
	.string "LIDER: Antes da batalha,\n"
	.string "resolva os dois paineis\p"
	.string "na ordem indicada!$"

GymEryonArkhara_Text_Exit:
	.string "Sair do GINASIO agora?$"
