Eryon_EstradaOriental_MapScripts::
	.byte 0

@ First investigation site beyond the rocky passage.
EryonEstrada_EventScript_Tracks::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonEstrada_EventScript_TracksClue
	msgbox EryonEstrada_Text_TracksBefore, MSGBOX_DEFAULT
	release
	end

EryonEstrada_EventScript_TracksClue::
	msgbox EryonEstrada_Text_TracksClue, MSGBOX_DEFAULT
	release
	end

EryonEstrada_Text_TracksBefore:
	.string "A estrada tem marcas de\n"
	.string "rodas antigas e recentes.\p"
	.string "A viagem sera longa.$"

EryonEstrada_Text_TracksClue:
	.string "O rastro das carrocas\n"
	.string "continua para o leste.\p"
	.string "Ha po de cristal no solo.\n"
	.string "A Equipe Eclipse passou aqui.$"

@ Travelers give the eastern road a useful stop between the mountain and valley.
EryonEstrada_EventScript_Surveyor::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonEstrada_EventScript_SurveyorClue
	msgbox EryonEstrada_Text_SurveyorBefore, MSGBOX_DEFAULT
	release
	end

EryonEstrada_EventScript_SurveyorClue::
	msgbox EryonEstrada_Text_SurveyorClue, MSGBOX_DEFAULT
	release
	end

EryonEstrada_EventScript_FieldMedic::
	lock
	faceplayer
	msgbox EryonEstrada_Text_FieldMedicOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonEstrada_EventScript_FieldMedicDecline
	special HealPlayerParty
	msgbox EryonEstrada_Text_FieldMedicHealed, MSGBOX_DEFAULT
	release
	end

EryonEstrada_EventScript_FieldMedicDecline::
	msgbox EryonEstrada_Text_FieldMedicDecline, MSGBOX_DEFAULT
	release
	end

EryonEstrada_Text_SurveyorBefore:
	.string "TOPOGRAFO: Esta estrada\n"
	.string "atravessa terreno antigo.\p"
	.string "O Vale dos Ventos fica\n"
	.string "mais adiante.$"

EryonEstrada_Text_SurveyorClue:
	.string "TOPOGRAFO: Carrocas muito\n"
	.string "pesadas passaram aqui.\p"
	.string "As rodas deixaram po\n"
	.string "brilhante nas pedras.$"

EryonEstrada_Text_FieldMedicOffer:
	.string "SOCORRISTA: A estrada e\n"
	.string "longa. Quer curar sua equipe?$"

EryonEstrada_Text_FieldMedicHealed:
	.string "Seus Pokemon estao bem!\n"
	.string "Boa viagem.$"

EryonEstrada_Text_FieldMedicDecline:
	.string "Volte se precisar de ajuda.$"
