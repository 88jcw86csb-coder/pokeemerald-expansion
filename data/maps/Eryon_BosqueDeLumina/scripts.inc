@ First persistent clue of the Eclipse mystery. The player can revisit this researcher.
EryonBosque_EventScript_Researcher::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonBosque_EventScript_ResearcherFollowup
	msgbox EryonBosque_Text_Researcher, MSGBOX_DEFAULT
	setvar VAR_ERYON_LUMINA_CLUE_FOUND, 1
	msgbox EryonBosque_Text_ClueFound, MSGBOX_DEFAULT
	release
	end

EryonBosque_EventScript_ResearcherFollowup::
	msgbox EryonBosque_Text_ResearcherFollowup, MSGBOX_DEFAULT
	release
	end

EryonBosque_Text_Researcher:
	.string "PESQUISADOR: Que estranho...\p"
	.string "Os Pokemon daqui estao agitados.\p"
	.string "Encontrei uma marca em forma de\n"
	.string "eclipse nas pedras antigas.$"

EryonBosque_Text_ClueFound:
	.string "Voce observou a marca!\p"
	.string "Alguem esteve aqui antes de nos.\n"
	.string "Procure respostas em Verdelume.$"

EryonBosque_Text_ResearcherFollowup:
	.string "A marca de eclipse ainda esta\n"
	.string "aqui. Nao e um sinal natural.\p"
	.string "Converse com o povo de Verdelume.$"

@ A separate encounter hints at human interference without revealing the villains yet.
EryonBosque_EventScript_SilentTraveler::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonBosque_EventScript_TravelerAfterClue
	msgbox EryonBosque_Text_TravelerBeforeClue, MSGBOX_DEFAULT
	release
	end

EryonBosque_EventScript_TravelerAfterClue::
	msgbox EryonBosque_Text_TravelerAfterClue, MSGBOX_DEFAULT
	release
	end

EryonBosque_Text_TravelerBeforeClue:
	.string "VIAJANTE: Nao siga as luzes\\n"
	.string "que surgem ao anoitecer.\\p"
	.string "Vi pessoas levando caixas para\\n"
	.string "dentro da mata. Estranho, nao?$"

EryonBosque_Text_TravelerAfterClue:
	.string "VIAJANTE: A marca nas pedras?\\p"
	.string "As caixas tinham o mesmo sinal.\\n"
	.string "Nao pareciam pesquisadores.$"
