GymEryon_Verdelume_MapScripts::
	.byte 0

GymEryonVerdelume_EventScript_Leader::
	goto_if_set FLAG_BADGE01_GET, EryonVerdelume_EventScript_Kael
	goto_if_unset FLAG_ERYON_GYM_VERDELUME_READY, GymEryonVerdelume_EventScript_NotReady
	goto EryonVerdelume_EventScript_Kael

GymEryonVerdelume_EventScript_NotReady::
	lock
	faceplayer
	msgbox GymEryonVerdelume_Text_NotReady, MSGBOX_DEFAULT
	release
	end

GymEryonVerdelume_EventScript_Guide::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_GYM_VERDELUME_READY, GymEryonVerdelume_EventScript_GuideReady
	msgbox GymEryonVerdelume_Text_Guide, MSGBOX_DEFAULT
	release
	end

GymEryonVerdelume_EventScript_GuideReady::
	msgbox GymEryonVerdelume_Text_GuideReady, MSGBOX_DEFAULT
	release
	end

GymEryonVerdelume_EventScript_First::
	lock
	goto_if_set FLAG_ERYON_GYM_VERDELUME_PRIMED, GymEryonVerdelume_EventScript_FirstAgain
	msgbox GymEryonVerdelume_Text_First, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GYM_VERDELUME_PRIMED
	release
	end

GymEryonVerdelume_EventScript_FirstAgain::
	msgbox GymEryonVerdelume_Text_FirstAgain, MSGBOX_DEFAULT
	release
	end

GymEryonVerdelume_EventScript_Second::
	lock
	goto_if_unset FLAG_ERYON_GYM_VERDELUME_PRIMED, GymEryonVerdelume_EventScript_SecondEarly
	goto_if_set FLAG_ERYON_GYM_VERDELUME_READY, GymEryonVerdelume_EventScript_SecondAgain
	msgbox GymEryonVerdelume_Text_Second, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GYM_VERDELUME_READY
	release
	end

GymEryonVerdelume_EventScript_SecondEarly::
	msgbox GymEryonVerdelume_Text_SecondEarly, MSGBOX_DEFAULT
	release
	end

GymEryonVerdelume_EventScript_SecondAgain::
	msgbox GymEryonVerdelume_Text_SecondAgain, MSGBOX_DEFAULT
	release
	end

GymEryonVerdelume_EventScript_Exit::
	lock
	msgbox GymEryonVerdelume_Text_Exit, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, GymEryonVerdelume_EventScript_Stay
	closemessage
	warp MAP_ERYON_VERDELUME, 19, 22
	waitstate
	end

GymEryonVerdelume_EventScript_Stay::
	closemessage
	release
	end

GymEryonVerdelume_Text_Guide:
	.string "GUIA: Bem-vindo ao\n"
	.string "GINASIO de VERDELUME.\p"
	.string "Ative o painel esquerdo\n"
	.string "e depois o direito.$"

GymEryonVerdelume_Text_GuideReady:
	.string "GUIA: ESTUFA liberado!\p"
	.string "O lider espera ao norte.\n"
	.string "Boa sorte no desafio!$"

GymEryonVerdelume_Text_First:
	.string "PAINEL RAIZES:\p"
	.string "Primeira etapa concluida.\n"
	.string "Busque o segundo sinal.$"

GymEryonVerdelume_Text_FirstAgain:
	.string "PAINEL RAIZES:\n"
	.string "Sinal registrado.$"

GymEryonVerdelume_Text_Second:
	.string "PAINEL IRRIGACAO:\p"
	.string "Dois sinais em harmonia.\n"
	.string "O desafio foi liberado!$"

GymEryonVerdelume_Text_SecondEarly:
	.string "PAINEL IRRIGACAO:\p"
	.string "Falta ativar o painel\n"
	.string "do lado esquerdo.$"

GymEryonVerdelume_Text_SecondAgain:
	.string "PAINEL IRRIGACAO:\n"
	.string "Ressonancia estabilizada.$"

GymEryonVerdelume_Text_NotReady:
	.string "LIDER: Antes da batalha,\n"
	.string "resolva os dois paineis\p"
	.string "na ordem indicada!$"

GymEryonVerdelume_Text_Exit:
	.string "Sair do GINASIO agora?$"
