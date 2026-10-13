Eryon_EstradaDosPomares_MapScripts::
	.byte 0


@ A scenic orchard bypass connects Verdelume to Neonara without field HMs.
EryonPomaresEstrada_EventScript_Ranger::
	lock
	faceplayer
	msgbox EryonPomaresEstrada_Text_Ranger, MSGBOX_DEFAULT
	release
	end

EryonPomaresEstrada_EventScript_Orchardist::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonPomaresEstrada_EventScript_OrchardistClue
	msgbox EryonPomaresEstrada_Text_OrchardistBefore, MSGBOX_DEFAULT
	release
	end

EryonPomaresEstrada_EventScript_OrchardistClue::
	msgbox EryonPomaresEstrada_Text_OrchardistClue, MSGBOX_DEFAULT
	release
	end

EryonPomaresEstrada_EventScript_Tracks::
	lock
	msgbox EryonPomaresEstrada_Text_Tracks, MSGBOX_DEFAULT
	release
	end

EryonPomaresEstrada_Text_Ranger:
	.string "GUIA: Ha uma trilha\n"
	.string "livre entre os pomares.\p"
	.string "Nao precisa cortar\n"
	.string "arvores para passar.$"

EryonPomaresEstrada_Text_OrchardistBefore:
	.string "AGRICULTORA: As frutas\n"
	.string "amadurecem muito cedo.\p"
	.string "O solo esta diferente\n"
	.string "desde a ultima chuva.$"

EryonPomaresEstrada_Text_OrchardistClue:
	.string "AGRICULTORA: Encontramos\n"
	.string "um simbolo de ECLIPSE!\p"
	.string "Vi caixas seguindo\n"
	.string "para a VILA DOS POMARES.$"

EryonPomaresEstrada_Text_Tracks:
	.string "Marcas de rodas cortam\n"
	.string "a terra entre arvores.\p"
	.string "O transporte seguiu\n"
	.string "para a vila.$"
