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

@ Optional inspection beside the Umbra approach; no route blocking.
EryonVale_EventScript_SealedCargo::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonVale_EventScript_SealedCargoClue
	msgbox EryonVale_Text_SealedCargoBefore, MSGBOX_DEFAULT
	release
	end

EryonVale_EventScript_SealedCargoClue::
	msgbox EryonVale_Text_SealedCargoClue, MSGBOX_DEFAULT
	release
	end

EryonVale_Text_SealedCargoBefore:
	.string "Um lacre de carga esta\n"
	.string "preso entre as rochas.\p"
	.string "O simbolo foi raspado.$"

EryonVale_Text_SealedCargoClue:
	.string "O lacre tem residuos\n"
	.string "dos cristais da serra!\p"
	.string "O destino marcado e\n"
	.string "a cidade de Umbra.$"

@ A second route witness links the cargo trail to Umbra's factory.
EryonVale_EventScript_CaravanWitness::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonVale_EventScript_CaravanWitnessClue
	msgbox EryonVale_Text_CaravanWitnessBefore, MSGBOX_DEFAULT
	release
	end

EryonVale_EventScript_CaravanWitnessClue::
	msgbox EryonVale_Text_CaravanWitnessClue, MSGBOX_DEFAULT
	release
	end

EryonVale_Text_CaravanWitnessBefore:
	.string "VIAJANTE: Carrocas\n"
	.string "cruzaram o vale a noite.\p"
	.string "Evitaram os postos\n"
	.string "de fiscalizacao.$"

EryonVale_Text_CaravanWitnessClue:
	.string "VIAJANTE: As caixas\n"
	.string "tinham marcas da ECLIPSE.\p"
	.string "Foram descarregadas\n"
	.string "perto da fabrica de Umbra.$"


@ Wind-sheltered garden carved into the original valley landscape.
EryonVale_EventScript_WindGarden::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonVale_EventScript_WindGardenClue
	msgbox EryonVale_Text_WindGardenBefore, MSGBOX_DEFAULT
	release
	end

EryonVale_EventScript_WindGardenClue::
	msgbox EryonVale_Text_WindGardenClue, MSGBOX_DEFAULT
	release
	end

EryonVale_Text_WindGardenBefore:
	.string "JARDIM DOS VENTOS:\p"
	.string "As rochas protegem\n"
	.string "flores raras do vento.\p"
	.string "Marcas de carrocas\n"
	.string "seguem para o leste.$"

EryonVale_Text_WindGardenClue:
	.string "JARDIM DOS VENTOS:\p"
	.string "Os rastros da ECLIPSE\n"
	.string "passaram por aqui.\p"
	.string "O vento escondeu\n"
	.string "as marcas da caravana.$"


@ Optional medicine in the newly accessible windbreak; no gym flags affected.
EryonVale_EventScript_WindGardenSupplies::
	lock
	goto_if_set FLAG_ERYON_WIND_GARDEN_REWARD_CLAIMED, EryonVale_EventScript_WindGardenEmpty
	msgbox EryonVale_Text_WindGardenSupplies, MSGBOX_DEFAULT
	giveitem ITEM_SUPER_POTION
	goto_if_eq VAR_RESULT, FALSE, EryonVale_EventScript_WindGardenBagFull
	setflag FLAG_ERYON_WIND_GARDEN_REWARD_CLAIMED
	release
	end

EryonVale_EventScript_WindGardenBagFull::
	msgbox EryonVale_Text_WindGardenBagFull, MSGBOX_DEFAULT
	release
	end

EryonVale_EventScript_WindGardenEmpty::
	msgbox EryonVale_Text_WindGardenEmpty, MSGBOX_DEFAULT
	release
	end

EryonVale_Text_WindGardenSupplies:
	.string "SUPRIMENTOS DO VALE:\p"
	.string "Uma SUPER POTION\n"
	.string "foi protegida do vento.$"

EryonVale_Text_WindGardenBagFull:
	.string "Sua BOLSA esta cheia!\p"
	.string "O remedio ficara aqui.$"

EryonVale_Text_WindGardenEmpty:
	.string "A caixa de suprimentos\n"
	.string "ja esta vazia.$"
