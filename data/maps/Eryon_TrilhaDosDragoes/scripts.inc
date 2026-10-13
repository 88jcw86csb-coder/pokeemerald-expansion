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
