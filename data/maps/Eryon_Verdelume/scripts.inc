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

@ A local resident introduces Kael without forcing the story forward.
EryonVerdelume_EventScript_LocalKid::
	lock
	faceplayer
	msgbox EryonVerdelume_Text_LocalKid, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_Text_LocalKid:
	.string "Kael treina Pokemon de planta!\p"
	.string "Dizem que sua ROSERADE nunca\n"
	.string "desiste de uma batalha.$"

@ Kael's first encounter; the gym battle is not yet implemented.
EryonVerdelume_EventScript_Kael::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonVerdelume_EventScript_KaelClue
	msgbox EryonVerdelume_Text_KaelWelcome, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_EventScript_KaelClue::
	msgbox EryonVerdelume_Text_KaelClue, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_Text_KaelWelcome:
	.string "KAEL: Eu cuido das trilhas daqui.\p"
	.string "Se visitar o Bosque de Lumina,\n"
	.string "preste atencao nas pedras.$"

EryonVerdelume_Text_KaelClue:
	.string "KAEL: Entao viu a marca antiga!\p"
	.string "A floresta precisa de ajuda.\n"
	.string "Vamos investigar com cuidado.$"

@ A public notice changes once the player has investigated the forest.
EryonVerdelume_EventScript_ForestNotice::
	lock
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonVerdelume_EventScript_ForestNoticeClue
	msgbox EryonVerdelume_Text_ForestNotice, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_EventScript_ForestNoticeClue::
	msgbox EryonVerdelume_Text_ForestNoticeClue, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_Text_ForestNotice:
	.string "AVISO AOS VIAJANTES\p"
	.string "Luzes estranhas foram vistas\n"
	.string "no Bosque de Lumina.\p"
	.string "Explore com cuidado.$"

EryonVerdelume_Text_ForestNoticeClue:
	.string "AVISO AOS VIAJANTES\p"
	.string "A antiga marca de eclipse\n"
	.string "esta sendo investigada.\p"
	.string "Informe Kael sobre pistas.$"
