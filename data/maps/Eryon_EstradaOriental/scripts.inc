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
