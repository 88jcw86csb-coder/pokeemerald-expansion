@ The town guide acknowledges the forest discovery without forcing progression.
EryonVerdelume_EventScript_Guide::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonVerdelume_EventScript_GuideClue
	msgbox EryonVerdelume_Text_Guide, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_EventScript_GuideClue::
	msgbox EryonVerdelume_Text_GuideClue, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_Text_Guide:
	.string "Bem-vindo a Verdelume!\p"
	.string "Kael protege nosso ginasio, mas\n"
	.string "o bosque preocupa a cidade.$"

EryonVerdelume_Text_GuideClue:
	.string "Uma marca de eclipse no bosque?\p"
	.string "Kael tambem ouviu rumores.\n"
	.string "Talvez ele saiba de algo.$"
