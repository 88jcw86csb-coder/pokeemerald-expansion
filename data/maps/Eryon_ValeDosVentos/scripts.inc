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

@ An Eclipse lookout foreshadows the next chapter without forcing an early climax.
EryonVale_EventScript_Lookout::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonVale_EventScript_LookoutClue
	msgbox EryonVale_Text_LookoutBefore, MSGBOX_DEFAULT
	release
	end

EryonVale_EventScript_LookoutClue::
	msgbox EryonVale_Text_LookoutClue, MSGBOX_DEFAULT
	release
	end

EryonVale_EventScript_WindMarker::
	lock
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonVale_EventScript_WindMarkerBadge
	msgbox EryonVale_Text_WindMarkerBefore, MSGBOX_DEFAULT
	release
	end

EryonVale_EventScript_WindMarkerBadge::
	msgbox EryonVale_Text_WindMarkerBadge, MSGBOX_DEFAULT
	release
	end

EryonVale_Text_LookoutBefore:
	.string "VIAJANTE: O vento daqui\n"
	.string "esconde o som dos passos.\p"
	.string "Nao siga estranhos sozinho.$"

EryonVale_Text_LookoutClue:
	.string "VIAJANTE: Homens de azul\n"
	.string "escuro passaram ao amanhecer.\p"
	.string "Levavam caixas com um\n"
	.string "simbolo de eclipse.$"

EryonVale_Text_WindMarkerBefore:
	.string "Uma placa antiga aponta\n"
	.string "para o alto do vale.\p"
	.string "O vento apagou as letras.$"

EryonVale_Text_WindMarkerBadge:
	.string "A placa marca um antigo\n"
	.string "posto de observacao.\p"
	.string "Ha pegadas frescas na\n"
	.string "direcao das montanhas.$"
