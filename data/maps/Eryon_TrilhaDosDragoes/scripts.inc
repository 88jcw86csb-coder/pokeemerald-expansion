Eryon_TrilhaDosDragoes_MapScripts::
	.byte 0

@ Expedition through the rocky approach to Drakonia.
EryonDragoes_EventScript_RidgeGuide::
	lock
	faceplayer
	msgbox EryonDragoes_Text_Guide, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_EclipseCourier::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonDragoes_EventScript_EclipseCourierExposed
	msgbox EryonDragoes_Text_CourierBefore, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_EclipseCourierExposed::
	msgbox EryonDragoes_Text_CourierExposed, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_WildlifeResearcher::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonDragoes_EventScript_WildlifeResearcherClue
	msgbox EryonDragoes_Text_ResearcherBefore, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_WildlifeResearcherClue::
	msgbox EryonDragoes_Text_ResearcherClue, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_SupplyCrate::
	lock
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, EryonDragoes_EventScript_SupplyCrateRecorded
	goto_if_set FLAG_ERYON_STAR_CHART_READ, EryonDragoes_EventScript_SupplyCrateChart
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonDragoes_EventScript_SupplyCrateClue
	msgbox EryonDragoes_Text_CrateBefore, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_SupplyCrateClue::
	msgbox EryonDragoes_Text_CrateClue, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_MountainMarker::
	lock
	msgbox EryonDragoes_Text_Marker, MSGBOX_DEFAULT
	release
	end

EryonDragoes_Text_Guide:
	.string "GUIA: Siga o caminho\n"
	.string "entre as rochas altas.\p"
	.string "Ha Pokemon raros e\n"
	.string "uma vila mais adiante.$"

EryonDragoes_Text_CourierBefore:
	.string "MENSAGEIRO: Transporto\n"
	.string "pecas para as montanhas.\p"
	.string "Nao bloqueie a trilha.\n"
	.string "Tenho pressa.$"

EryonDragoes_Text_CourierExposed:
	.string "ECLIPSE: As pecas\n"
	.string "vieram de LUNARIS!\p"
	.string "DRAKONIA sera o ultimo\n"
	.string "elo da nossa rede.$"

EryonDragoes_Text_ResearcherBefore:
	.string "BIOLOGO: Os Pokemon\n"
	.string "do pico estao agitados.\p"
	.string "Algo perturba o som\n"
	.string "natural destas pedras.$"

EryonDragoes_Text_ResearcherClue:
	.string "BIOLOGO: Este pulso\n"
	.string "nao veio dos Pokemon!\p"
	.string "A ECLIPSE esta usando\n"
	.string "antenas nas montanhas.$"

EryonDragoes_Text_CrateBefore:
	.string "Uma caixa de madeira\n"
	.string "tem sinais de viagem.\p"
	.string "Seu destino marcado:\n"
	.string "VILA DO PICO.$"

EryonDragoes_Text_CrateClue:
	.string "A caixa tem o selo\n"
	.string "da EQUIPE ECLIPSE.\p"
	.string "O envio foi registrado\n"
	.string "em UMBRA e LUNARIS.$"

EryonDragoes_Text_Marker:
	.string "OESTE: LUNARIS.\n"
	.string "LESTE: VILA DO PICO.\p"
	.string "Cuidado com os ventos\n"
	.string "na estrada elevada.$"

@ Optional clues become clearer as the player investigates the Eclipse network.
EryonDragoes_EventScript_SupplyCrateChart::
	msgbox EryonDragoes_Text_CrateChart, MSGBOX_DEFAULT
	setflag FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ
	release
	end

EryonDragoes_EventScript_Ranger::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, EryonDragoes_EventScript_RangerManifest
	goto_if_set FLAG_ERYON_STAR_CHART_READ, EryonDragoes_EventScript_RangerChart
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonDragoes_EventScript_RangerClue
	msgbox EryonDragoes_Text_RangerBefore, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_RangerClue::
	msgbox EryonDragoes_Text_RangerClue, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_RangerChart::
	msgbox EryonDragoes_Text_RangerChart, MSGBOX_DEFAULT
	release
	end

EryonDragoes_Text_CrateChart:
	.string "As etiquetas mostram\n"
	.string "uma rota de cristais.\p"
	.string "LUNARIS, VILA DO PICO,\n"
	.string "DRAKONIA e a LIGA.\p"
	.string "A ECLIPSE organizou\n"
	.string "todas as remessas.$"

EryonDragoes_Text_RangerBefore:
	.string "GUARDA: O vento muda\n"
	.string "perto deste penhasco.\p"
	.string "A trilha ate a vila\n"
	.string "segue aberta a pe.$"

EryonDragoes_Text_RangerClue:
	.string "GUARDA: Encontramos\n"
	.string "marcas da ECLIPSE.\p"
	.string "O transporte segue\n"
	.string "ate VILA DO PICO.$"

EryonDragoes_Text_RangerChart:
	.string "GUARDA: A Carta\n"
	.string "Estelar confirmou\n"
	.string "nosso alerta!\p"
	.string "A rede chega a LIGA.\n"
	.string "Precisamos vigiar.$"

@ Once decoded, the manifest stays registered in the player's save.
EryonDragoes_EventScript_SupplyCrateRecorded::
	msgbox EryonDragoes_Text_CrateRecorded, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_RangerManifest::
	msgbox EryonDragoes_Text_RangerManifest, MSGBOX_DEFAULT
	release
	end

EryonDragoes_Text_CrateRecorded:
	.string "Voce ja copiou\n"
	.string "o manifesto ECLIPSE.\p"
	.string "As provas ligam\n"
	.string "LUNARIS a DRAKONIA.$"

EryonDragoes_Text_RangerManifest:
	.string "GUARDA: Seu manifesto\n"
	.string "confirma o transporte!\p"
	.string "Vamos avisar os\n"
	.string "guardioes de DRAKONIA.$"
