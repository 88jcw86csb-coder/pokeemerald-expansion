Eryon_DesertoDeSolaris_MapScripts::
	.byte 0

@ Eclipse uses a buried relay to move crystal energy toward Ignivar.
EryonSolaris_EventScript_Explorer::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonSolaris_EventScript_ExplorerClue
	msgbox EryonSolaris_Text_ExplorerBefore, MSGBOX_DEFAULT
	release
	end

EryonSolaris_EventScript_ExplorerClue::
	msgbox EryonSolaris_Text_ExplorerClue, MSGBOX_DEFAULT
	release
	end

EryonSolaris_EventScript_EclipseGuard::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonSolaris_EventScript_EclipseGuardClue
	msgbox EryonSolaris_Text_GuardBefore, MSGBOX_DEFAULT
	release
	end

EryonSolaris_EventScript_EclipseGuardClue::
	msgbox EryonSolaris_Text_GuardClue, MSGBOX_DEFAULT
	release
	end

EryonSolaris_EventScript_BuriedDevice::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonSolaris_EventScript_BuriedDeviceClue
	msgbox EryonSolaris_Text_DeviceBefore, MSGBOX_DEFAULT
	release
	end

EryonSolaris_EventScript_BuriedDeviceClue::
	msgbox EryonSolaris_Text_DeviceClue, MSGBOX_DEFAULT
	release
	end

EryonSolaris_Text_ExplorerBefore:
	.string "EXPLORADOR: As dunas\n"
	.string "mudam com o vento.\p"
	.string "Siga as pedras para\n"
	.string "alcancar Ignivar.$"

EryonSolaris_Text_ExplorerClue:
	.string "EXPLORADOR: Uma equipe\n"
	.string "enterrou cabos na areia.\p"
	.string "Levam energia para\n"
	.string "a usina de Ignivar.$"

EryonSolaris_Text_GuardBefore:
	.string "VIGIA: A passagem esta\n"
	.string "sob observacao.\p"
	.string "Nao toque no equipamento.$"

EryonSolaris_Text_GuardClue:
	.string "ECLIPSE: Os cristais\n"
	.string "alimentam nosso reator!\p"
	.string "Ignivar nao imagina\n"
	.string "quando vier o pulso.$"

EryonSolaris_Text_DeviceBefore:
	.string "Uma antena emerge\n"
	.string "parcialmente da areia.\p"
	.string "Ha cabos enterrados.$"

EryonSolaris_Text_DeviceClue:
	.string "O selo da ECLIPSE\n"
	.string "cobre um transmissor.\p"
	.string "Um cabo segue na\n"
	.string "direcao da usina.$"

@ Additional local witness to the Eclipse signal crossing Eryon.
EryonSolaris_EventScript_CaravanScout::
	lock
	faceplayer
	msgbox EryonSolaris_Text_CaravanScout, MSGBOX_DEFAULT
	release
	end

EryonSolaris_Text_CaravanScout:
	.string "GUIA: As marcas na areia\n"
	.string "nao sao de Pokemon.\p"
	.string "Um comboio ECLIPSE\n"
	.string "seguiu para Ignivar.$"
