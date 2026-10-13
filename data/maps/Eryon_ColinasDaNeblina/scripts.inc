Eryon_ColinasDaNeblina_MapScripts::
	.byte 0


@ Mist-covered hills extend the Eclipse mystery toward Frostheim.
EryonNeblinaColinas_EventScript_Guide::
	lock
	faceplayer
	msgbox EryonNeblinaColinas_Text_Guide, MSGBOX_DEFAULT
	release
	end

EryonNeblinaColinas_EventScript_Surveyor::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonNeblinaColinas_EventScript_SurveyorInformed
	msgbox EryonNeblinaColinas_Text_SurveyorBefore, MSGBOX_DEFAULT
	release
	end

EryonNeblinaColinas_EventScript_SurveyorInformed::
	msgbox EryonNeblinaColinas_Text_SurveyorInformed, MSGBOX_DEFAULT
	release
	end

EryonNeblinaColinas_EventScript_Marker::
	lock
	msgbox EryonNeblinaColinas_Text_Marker, MSGBOX_DEFAULT
	release
	end

EryonNeblinaColinas_Text_Guide:
	.string "GUIA: A neblina muda\n"
	.string "de direcao muito rapido.\p"
	.string "Siga a estrada aberta.\n"
	.string "Nao precisa de FLASH.$"

EryonNeblinaColinas_Text_SurveyorBefore:
	.string "TECNICO: As pedras\n"
	.string "atrapalham meus sinais.\p"
	.string "Volte quando a neblina\n"
	.string "ficar mais fina.$"

EryonNeblinaColinas_Text_SurveyorInformed:
	.string "ECLIPSE: A marca do\n"
	.string "BOSQUE chegou ate aqui?\p"
	.string "Estamos medindo os\n"
	.string "cristais de FROSTHEIM.$"

EryonNeblinaColinas_Text_Marker:
	.string "OESTE: NEONARA.\n"
	.string "LESTE: VILA DA NEBLINA.\p"
	.string "A trilha contorna\n"
	.string "as pedras grandes.$"
