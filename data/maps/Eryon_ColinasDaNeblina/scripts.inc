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
	goto_if_set FLAG_ERYON_MIST_SIGNAL_REPAIRED, EryonNeblinaColinas_EventScript_SurveyorRepaired
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


@ Northern overlook: restoring the lookout after Neonara's Electric Badge.
@ A direct route remains open even when this optional event is skipped.
EryonNeblinaColinas_EventScript_MistBeacon::
	lock
	goto_if_set FLAG_ERYON_MIST_SIGNAL_REPAIRED, EryonNeblinaColinas_EventScript_BeaconActive
	goto_if_unset FLAG_BADGE02_GET, EryonNeblinaColinas_EventScript_BeaconNeedsBadge
	msgbox EryonNeblinaColinas_Text_BeaconOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonNeblinaColinas_EventScript_BeaconLeave
	closemessage
	setflag FLAG_ERYON_MIST_SIGNAL_REPAIRED
	msgbox EryonNeblinaColinas_Text_BeaconRestored, MSGBOX_DEFAULT
	release
	end

EryonNeblinaColinas_EventScript_BeaconNeedsBadge::
	msgbox EryonNeblinaColinas_Text_BeaconNeedsBadge, MSGBOX_DEFAULT
	release
	end

EryonNeblinaColinas_EventScript_BeaconActive::
	msgbox EryonNeblinaColinas_Text_BeaconActive, MSGBOX_DEFAULT
	release
	end

EryonNeblinaColinas_EventScript_BeaconLeave::
	closemessage
	release
	end

EryonNeblinaColinas_EventScript_SurveyorRepaired::
	msgbox EryonNeblinaColinas_Text_SurveyorRepaired, MSGBOX_DEFAULT
	release
	end

@ Optional temporary shelter on the overlooking cliff.
EryonNeblinaColinas_EventScript_MistKeeper::
	lock
	faceplayer
	goto_if_unset FLAG_ERYON_MIST_SIGNAL_REPAIRED, EryonNeblinaColinas_EventScript_KeeperWaiting
	msgbox EryonNeblinaColinas_Text_KeeperRest, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonNeblinaColinas_EventScript_BeaconLeave
	closemessage
	special HealPlayerParty
	msgbox EryonNeblinaColinas_Text_KeeperHealed, MSGBOX_DEFAULT
	release
	end

EryonNeblinaColinas_EventScript_KeeperWaiting::
	msgbox EryonNeblinaColinas_Text_KeeperWaiting, MSGBOX_DEFAULT
	release
	end

EryonNeblinaColinas_Text_BeaconOffer:
	.string "OBSERVATORIO DA NEBLINA:\p"
	.string "A INSIGNIA eletrica\n"
	.string "permite ajustar o sinal.\p"
	.string "Reparar o transmissor?$"

EryonNeblinaColinas_Text_BeaconRestored:
	.string "O sinal foi restaurado!\p"
	.string "A VILA DA NEBLINA\n"
	.string "recebe alertas da ECLIPSE.$"

EryonNeblinaColinas_Text_BeaconNeedsBadge:
	.string "Um painel sem energia.\p"
	.string "Precisa de uma INSIGNIA\n"
	.string "do GINASIO de NEONARA.$"

EryonNeblinaColinas_Text_BeaconActive:
	.string "SINAL RESTAURADO:\n"
	.string "Ligacao com FROSTHEIM\n"
	.string "e VILA DA NEBLINA.$"

EryonNeblinaColinas_Text_SurveyorRepaired:
	.string "TECNICO: Obrigado!\p"
	.string "O observatorio ja pode\n"
	.string "vigiar as rotas geladas.\p"
	.string "A ECLIPSE nao passara\n"
	.string "despercebida aqui.$"

EryonNeblinaColinas_Text_KeeperWaiting:
	.string "GUARDA: Este abrigo\n"
	.string "aguarda o retorno\n"
	.string "do sinal de NEONARA.$"

EryonNeblinaColinas_Text_KeeperRest:
	.string "GUARDA: O observatorio\n"
	.string "esta seguro novamente.\p"
	.string "Quer curar seus Pokemon?$"

EryonNeblinaColinas_Text_KeeperHealed:
	.string "GUARDA: Sua equipe esta\n"
	.string "pronta para a trilha!$"
