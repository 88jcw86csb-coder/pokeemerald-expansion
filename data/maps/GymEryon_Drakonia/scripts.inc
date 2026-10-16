GymEryon_Drakonia_MapScripts::
	.byte 0

GymEryonDrakonia_EventScript_Leader::
	goto_if_set FLAG_BADGE08_GET, EryonDrakonia_EventScript_GymLeader
	goto_if_unset FLAG_ERYON_GYM_DRAKONIA_READY, GymEryonDrakonia_EventScript_NotReady
	goto EryonDrakonia_EventScript_GymLeader

GymEryonDrakonia_EventScript_NotReady::
	lock
	faceplayer
	msgbox GymEryonDrakonia_Text_NotReady, MSGBOX_DEFAULT
	release
	end

GymEryonDrakonia_EventScript_Guide::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_GYM_DRAKONIA_READY, GymEryonDrakonia_EventScript_GuideReady
	msgbox GymEryonDrakonia_Text_Guide, MSGBOX_DEFAULT
	release
	end

GymEryonDrakonia_EventScript_GuideReady::
	msgbox GymEryonDrakonia_Text_GuideReady, MSGBOX_DEFAULT
	release
	end

GymEryonDrakonia_EventScript_First::
	lock
	goto_if_set FLAG_ERYON_GYM_DRAKONIA_PRIMED, GymEryonDrakonia_EventScript_FirstAgain
	msgbox GymEryonDrakonia_Text_First, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GYM_DRAKONIA_PRIMED
	release
	end

GymEryonDrakonia_EventScript_FirstAgain::
	msgbox GymEryonDrakonia_Text_FirstAgain, MSGBOX_DEFAULT
	release
	end

GymEryonDrakonia_EventScript_Second::
	lock
	goto_if_unset FLAG_ERYON_GYM_DRAKONIA_PRIMED, GymEryonDrakonia_EventScript_SecondEarly
	goto_if_set FLAG_ERYON_GYM_DRAKONIA_READY, GymEryonDrakonia_EventScript_SecondAgain
	msgbox GymEryonDrakonia_Text_Second, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GYM_DRAKONIA_READY
	release
	end

GymEryonDrakonia_EventScript_SecondEarly::
	msgbox GymEryonDrakonia_Text_SecondEarly, MSGBOX_DEFAULT
	release
	end

GymEryonDrakonia_EventScript_SecondAgain::
	msgbox GymEryonDrakonia_Text_SecondAgain, MSGBOX_DEFAULT
	release
	end

GymEryonDrakonia_EventScript_Exit::
	lock
	msgbox GymEryonDrakonia_Text_Exit, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, GymEryonDrakonia_EventScript_Stay
	closemessage
	warp MAP_ERYON_DRAKONIA, 33, 24
	waitstate
	end

GymEryonDrakonia_EventScript_Stay::
	closemessage
	release
	end

GymEryonDrakonia_Text_Guide:
	.string "GUIA: Bem-vindo ao\n"
	.string "GINASIO de DRAKONIA.\p"
	.string "Ative o painel esquerdo\n"
	.string "e depois o direito.$"

GymEryonDrakonia_Text_GuideReady:
	.string "GUIA: SANTUARIO liberado!\p"
	.string "O lider espera ao norte.\n"
	.string "Boa sorte no desafio!$"

GymEryonDrakonia_Text_First:
	.string "PAINEL SELOS:\p"
	.string "Primeira etapa concluida.\n"
	.string "Busque o segundo sinal.$"

GymEryonDrakonia_Text_FirstAgain:
	.string "PAINEL SELOS:\n"
	.string "Sinal registrado.$"

GymEryonDrakonia_Text_Second:
	.string "PAINEL DRAGOES:\p"
	.string "Dois sinais em harmonia.\n"
	.string "O desafio foi liberado!$"

GymEryonDrakonia_Text_SecondEarly:
	.string "PAINEL DRAGOES:\p"
	.string "Falta ativar o painel\n"
	.string "do lado esquerdo.$"

GymEryonDrakonia_Text_SecondAgain:
	.string "PAINEL DRAGOES:\n"
	.string "Ressonancia estabilizada.$"

GymEryonDrakonia_Text_NotReady:
	.string "LIDER: Antes da batalha,\n"
	.string "resolva os dois paineis\p"
	.string "na ordem indicada!$"

GymEryonDrakonia_Text_Exit:
	.string "Sair do GINASIO agora?$"
