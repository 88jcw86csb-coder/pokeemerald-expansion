GymEryon_Lunaris_MapScripts::
	.byte 0

GymEryonLunaris_EventScript_Leader::
	goto_if_set FLAG_BADGE07_GET, EryonLunaris_EventScript_GymLeader
	goto_if_unset FLAG_ERYON_GYM_LUNARIS_READY, GymEryonLunaris_EventScript_NotReady
	goto EryonLunaris_EventScript_GymLeader

GymEryonLunaris_EventScript_NotReady::
	lock
	faceplayer
	msgbox GymEryonLunaris_Text_NotReady, MSGBOX_DEFAULT
	release
	end

GymEryonLunaris_EventScript_Guide::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_GYM_LUNARIS_READY, GymEryonLunaris_EventScript_GuideReady
	msgbox GymEryonLunaris_Text_Guide, MSGBOX_DEFAULT
	release
	end

GymEryonLunaris_EventScript_GuideReady::
	msgbox GymEryonLunaris_Text_GuideReady, MSGBOX_DEFAULT
	release
	end

GymEryonLunaris_EventScript_First::
	lock
	goto_if_set FLAG_ERYON_GYM_LUNARIS_PRIMED, GymEryonLunaris_EventScript_FirstAgain
	msgbox GymEryonLunaris_Text_First, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GYM_LUNARIS_PRIMED
	release
	end

GymEryonLunaris_EventScript_FirstAgain::
	msgbox GymEryonLunaris_Text_FirstAgain, MSGBOX_DEFAULT
	release
	end

GymEryonLunaris_EventScript_Second::
	lock
	goto_if_unset FLAG_ERYON_GYM_LUNARIS_PRIMED, GymEryonLunaris_EventScript_SecondEarly
	goto_if_set FLAG_ERYON_GYM_LUNARIS_READY, GymEryonLunaris_EventScript_SecondAgain
	msgbox GymEryonLunaris_Text_Second, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GYM_LUNARIS_READY
	release
	end

GymEryonLunaris_EventScript_SecondEarly::
	msgbox GymEryonLunaris_Text_SecondEarly, MSGBOX_DEFAULT
	release
	end

GymEryonLunaris_EventScript_SecondAgain::
	msgbox GymEryonLunaris_Text_SecondAgain, MSGBOX_DEFAULT
	release
	end

GymEryonLunaris_EventScript_Exit::
	lock
	msgbox GymEryonLunaris_Text_Exit, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, GymEryonLunaris_EventScript_Stay
	closemessage
	warp MAP_ERYON_LUNARIS, 35, 29
	waitstate
	end

GymEryonLunaris_EventScript_Stay::
	closemessage
	release
	end

GymEryonLunaris_Text_Guide:
	.string "GUIA: Bem-vindo ao\n"
	.string "GINASIO de LUNARIS.\p"
	.string "Ative o painel esquerdo\n"
	.string "e depois o direito.$"

GymEryonLunaris_Text_GuideReady:
	.string "GUIA: ASTROS liberado!\p"
	.string "O lider espera ao norte.\n"
	.string "Boa sorte no desafio!$"

GymEryonLunaris_Text_First:
	.string "PAINEL ESTRELAS:\p"
	.string "Primeira etapa concluida.\n"
	.string "Busque o segundo sinal.$"

GymEryonLunaris_Text_FirstAgain:
	.string "PAINEL ESTRELAS:\n"
	.string "Sinal registrado.$"

GymEryonLunaris_Text_Second:
	.string "PAINEL ORBITAS:\p"
	.string "Dois sinais em harmonia.\n"
	.string "O desafio foi liberado!$"

GymEryonLunaris_Text_SecondEarly:
	.string "PAINEL ORBITAS:\p"
	.string "Falta ativar o painel\n"
	.string "do lado esquerdo.$"

GymEryonLunaris_Text_SecondAgain:
	.string "PAINEL ORBITAS:\n"
	.string "Ressonancia estabilizada.$"

GymEryonLunaris_Text_NotReady:
	.string "LIDER: Antes da batalha,\n"
	.string "resolva os dois paineis\p"
	.string "na ordem indicada!$"

GymEryonLunaris_Text_Exit:
	.string "Sair do GINASIO agora?$"
