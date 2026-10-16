GymEryon_Umbra_MapScripts::
	.byte 0

GymEryonUmbra_EventScript_Leader::
	goto_if_set FLAG_BADGE05_GET, EryonUmbra_EventScript_GymLeader
	goto_if_unset FLAG_ERYON_GYM_UMBRA_READY, GymEryonUmbra_EventScript_NotReady
	goto EryonUmbra_EventScript_GymLeader

GymEryonUmbra_EventScript_NotReady::
	lock
	faceplayer
	msgbox GymEryonUmbra_Text_NotReady, MSGBOX_DEFAULT
	release
	end

GymEryonUmbra_EventScript_Guide::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_GYM_UMBRA_READY, GymEryonUmbra_EventScript_GuideReady
	msgbox GymEryonUmbra_Text_Guide, MSGBOX_DEFAULT
	release
	end

GymEryonUmbra_EventScript_GuideReady::
	msgbox GymEryonUmbra_Text_GuideReady, MSGBOX_DEFAULT
	release
	end

GymEryonUmbra_EventScript_First::
	lock
	goto_if_set FLAG_ERYON_GYM_UMBRA_PRIMED, GymEryonUmbra_EventScript_FirstAgain
	msgbox GymEryonUmbra_Text_First, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GYM_UMBRA_PRIMED
	release
	end

GymEryonUmbra_EventScript_FirstAgain::
	msgbox GymEryonUmbra_Text_FirstAgain, MSGBOX_DEFAULT
	release
	end

GymEryonUmbra_EventScript_Second::
	lock
	goto_if_unset FLAG_ERYON_GYM_UMBRA_PRIMED, GymEryonUmbra_EventScript_SecondEarly
	goto_if_set FLAG_ERYON_GYM_UMBRA_READY, GymEryonUmbra_EventScript_SecondAgain
	msgbox GymEryonUmbra_Text_Second, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GYM_UMBRA_READY
	release
	end

GymEryonUmbra_EventScript_SecondEarly::
	msgbox GymEryonUmbra_Text_SecondEarly, MSGBOX_DEFAULT
	release
	end

GymEryonUmbra_EventScript_SecondAgain::
	msgbox GymEryonUmbra_Text_SecondAgain, MSGBOX_DEFAULT
	release
	end

GymEryonUmbra_EventScript_Exit::
	lock
	msgbox GymEryonUmbra_Text_Exit, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, GymEryonUmbra_EventScript_Stay
	closemessage
	warp MAP_ERYON_UMBRA, 35, 29
	waitstate
	end

GymEryonUmbra_EventScript_Stay::
	closemessage
	release
	end

GymEryonUmbra_Text_Guide:
	.string "GUIA: Bem-vindo ao\n"
	.string "GINASIO de UMBRA.\p"
	.string "Ative o painel esquerdo\n"
	.string "e depois o direito.$"

GymEryonUmbra_Text_GuideReady:
	.string "GUIA: NEBLINA liberado!\p"
	.string "O lider espera ao norte.\n"
	.string "Boa sorte no desafio!$"

GymEryonUmbra_Text_First:
	.string "PAINEL LANTERNAS:\p"
	.string "Primeira etapa concluida.\n"
	.string "Busque o segundo sinal.$"

GymEryonUmbra_Text_FirstAgain:
	.string "PAINEL LANTERNAS:\n"
	.string "Sinal registrado.$"

GymEryonUmbra_Text_Second:
	.string "PAINEL REFLEXOS:\p"
	.string "Dois sinais em harmonia.\n"
	.string "O desafio foi liberado!$"

GymEryonUmbra_Text_SecondEarly:
	.string "PAINEL REFLEXOS:\p"
	.string "Falta ativar o painel\n"
	.string "do lado esquerdo.$"

GymEryonUmbra_Text_SecondAgain:
	.string "PAINEL REFLEXOS:\n"
	.string "Ressonancia estabilizada.$"

GymEryonUmbra_Text_NotReady:
	.string "LIDER: Antes da batalha,\n"
	.string "resolva os dois paineis\p"
	.string "na ordem indicada!$"

GymEryonUmbra_Text_Exit:
	.string "Sair do GINASIO agora?$"
