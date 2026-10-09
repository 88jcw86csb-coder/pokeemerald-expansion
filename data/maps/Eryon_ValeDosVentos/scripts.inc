Eryon_ValeDosVentos_MapScripts::
	.byte 0

@ A quiet valley beyond the eastern road; the caravan trail continues.
EryonVale_EventScript_Ranger::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonVale_EventScript_RangerClue
	msgbox EryonVale_Text_RangerBefore, MSGBOX_DEFAULT
	release
	end

EryonVale_EventScript_RangerClue::
	msgbox EryonVale_Text_RangerClue, MSGBOX_DEFAULT
	release
	end

EryonVale_EventScript_Researcher::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonVale_EventScript_ResearcherBadge
	msgbox EryonVale_Text_ResearcherBefore, MSGBOX_DEFAULT
	release
	end

EryonVale_EventScript_ResearcherBadge::
	msgbox EryonVale_Text_ResearcherBadge, MSGBOX_DEFAULT
	release
	end

EryonVale_EventScript_CartWheel::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonVale_EventScript_CartWheelClue
	msgbox EryonVale_Text_CartWheelBefore, MSGBOX_DEFAULT
	release
	end

EryonVale_EventScript_CartWheelClue::
	msgbox EryonVale_Text_CartWheelClue, MSGBOX_DEFAULT
	release
	end

EryonVale_Text_RangerBefore:
	.string "GUARDA-FLORESTAL: O vento\n"
	.string "muda de direcao no vale.\p"
	.string "Explore com calma. A trilha\n"
	.string "nao termina aqui.$"

EryonVale_Text_RangerClue:
	.string "GUARDA-FLORESTAL: Vi um\n"
	.string "comboio cruzar este vale.\p"
	.string "Seguia a trilha oriental,\n"
	.string "longe dos viajantes.$"

EryonVale_Text_ResearcherBefore:
	.string "PESQUISADORA: Ha minerais\n"
	.string "raros nas encostas daqui.\p"
	.string "O vento espalha seu po.$"

EryonVale_Text_ResearcherBadge:
	.string "PESQUISADORA: Apos vencer\n"
	.string "KAEL, chegou ate o vale?\p"
	.string "Estude as rochas antes de\n"
	.string "seguir os rastros.$"

EryonVale_Text_CartWheelBefore:
	.string "Uma roda de carroca\n"
	.string "quebrada jaz na trilha.\p"
	.string "A madeira parece recente.$"

EryonVale_Text_CartWheelClue:
	.string "A roda tem um pequeno\n"
	.string "selo com um eclipse.\p"
	.string "O comboio passou por aqui,\n"
	.string "mas seu destino e incerto.$"
