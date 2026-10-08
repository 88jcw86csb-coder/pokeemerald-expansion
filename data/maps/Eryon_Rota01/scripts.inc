EryonRota01_EventScript_Explorer::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonRota01_EventScript_ExplorerAfterBadge
	goto_if_eq VAR_ERYON_STARTER_RECEIVED, 0, EryonRota01_EventScript_ExplorerNoStarter
	goto_if_ge VAR_ERYON_KAEL_BRIEFED, 1, EryonRota01_EventScript_ExplorerAfterKael
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonRota01_EventScript_ExplorerAfterClue
	msgbox EryonRota01_Text_Explorer, MSGBOX_DEFAULT
	release
	end

EryonRota01_EventScript_ExplorerAfterBadge::
	msgbox EryonRota01_Text_ExplorerAfterBadge, MSGBOX_DEFAULT
	release
	end

EryonRota01_EventScript_ExplorerNoStarter::
	msgbox EryonRota01_Text_ExplorerNoStarter, MSGBOX_DEFAULT
	release
	end

EryonRota01_EventScript_ExplorerAfterClue::
	msgbox EryonRota01_Text_ExplorerAfterClue, MSGBOX_DEFAULT
	release
	end

EryonRota01_EventScript_ExplorerAfterKael::
	msgbox EryonRota01_Text_ExplorerAfterKael, MSGBOX_DEFAULT
	release
	end

EryonRota01_Text_Explorer:
	.string "O Bosque de Lumina fica adiante!\p"
	.string "Dizem que as luzes entre as arvores\n"
	.string "mudaram nos ultimos dias.$"

@ An optional trail marker encourages exploring the forest before reaching Verdelume.
EryonRota01_EventScript_TrailMarker::
	lock
	msgbox EryonRota01_Text_TrailMarker, MSGBOX_DEFAULT
	release
	end

EryonRota01_Text_TrailMarker:
	.string "ROTA 01 - TRILHA DA AURORA\p"
	.string "Adiante: Bosque de Lumina.\n"
	.string "Observe as clareiras com calma.$"

EryonRota01_Text_ExplorerNoStarter:
	.string "Antes de entrar no bosque,\n"
	.string "visite a Prof. Elya na vila.\p"
	.string "Ela ajuda novos treinadores.$"

EryonRota01_Text_ExplorerAfterClue:
	.string "Voce encontrou uma marca\n"
	.string "estranha no bosque?\p"
	.string "Conte a Kael em Verdelume!$"

EryonRota01_Text_ExplorerAfterKael:
	.string "Kael ja sabe sobre a marca?\p"
	.string "Otimo! Explore as trilhas,\n"
	.string "mas nao se arrisque sozinho.$"

@ Revisiting the first route after Kael rewards attentive exploration.
EryonRota01_Text_ExplorerAfterBadge:
	.string "Sua primeira insignia! Parabens!\p"
	.string "O bosque continua misterioso.\n"
	.string "Talvez valha voltar com calma.$"
