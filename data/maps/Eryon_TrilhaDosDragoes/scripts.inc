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
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_COURIER_DEFEATED, EryonDragoes_EventScript_CourierAfterBattle
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonDragoes_EventScript_CourierBattleOffer
	msgbox EryonDragoes_Text_CourierBefore, MSGBOX_DEFAULT
	release
	end

@ Defeating the escort is optional; the eastern exit stays open.
EryonDragoes_EventScript_CourierBattleOffer::
	msgbox EryonDragoes_Text_CourierChallenge, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonDragoes_EventScript_CourierDecline
	closemessage
	trainerbattle_single TRAINER_ERYON_DRAGON_TRAIL_COURIER, EryonDragoes_Text_CourierIntro, EryonDragoes_Text_CourierLoss, EryonDragoes_EventScript_CourierVictory, FALSE
	msgbox EryonDragoes_Text_CourierAfter, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_CourierDecline::
	closemessage
	msgbox EryonDragoes_Text_CourierDecline, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_CourierVictory::
	msgbox EryonDragoes_Text_CourierVictory, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_CourierAfterBattle::
	msgbox EryonDragoes_Text_CourierAfter, MSGBOX_DEFAULT
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


@ Southeastern overlook: a hidden one-time reward for stopping the escort.
@ There is no mandatory battle or progression gate on the main road.
EryonDragoes_EventScript_SummitCache::
	lock
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_LOOKOUT_REWARD, EryonDragoes_EventScript_CacheEmpty
	goto_if_unset FLAG_ERYON_DRAGON_TRAIL_COURIER_DEFEATED, EryonDragoes_EventScript_CacheLocked
	msgbox EryonDragoes_Text_CacheOpened, MSGBOX_DEFAULT
	giveitem ITEM_DRAGON_FANG
	goto_if_eq VAR_RESULT, FALSE, EryonDragoes_EventScript_CacheBagFull
	setflag FLAG_ERYON_DRAGON_TRAIL_LOOKOUT_REWARD
	release
	end

EryonDragoes_EventScript_CacheLocked::
	msgbox EryonDragoes_Text_CacheLocked, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_CacheBagFull::
	msgbox EryonDragoes_Text_CacheBagFull, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_CacheEmpty::
	msgbox EryonDragoes_Text_CacheEmpty, MSGBOX_DEFAULT
	release
	end

@ Explorer at the cliffside links the local ecology to Eclipse's network.
EryonDragoes_EventScript_CliffResearcher::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_COURIER_DEFEATED, EryonDragoes_EventScript_CliffResearcherAfter
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonDragoes_EventScript_CliffResearcherClue
	msgbox EryonDragoes_Text_CliffResearcherBefore, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_CliffResearcherClue::
	msgbox EryonDragoes_Text_CliffResearcherClue, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_CliffResearcherAfter::
	msgbox EryonDragoes_Text_CliffResearcherAfter, MSGBOX_DEFAULT
	release
	end

EryonDragoes_Text_CourierChallenge:
	.string "ECLIPSE: Conhece o\n"
	.string "segredo de IGNIVAR?!\p"
	.string "Quer enfrentar minha\n"
	.string "escolta Pokemon?$"

EryonDragoes_Text_CourierIntro:
	.string "ECLIPSE: Ninguem\n"
	.string "interrompe a entrega!$"

EryonDragoes_Text_CourierLoss:
	.string "ECLIPSE: Meus Pokemon\n"
	.string "perderam no desfiladeiro!$"

EryonDragoes_Text_CourierVictory:
	.string "ECLIPSE: A remessa\n"
	.string "ficou desprotegida!\p"
	.string "Deixamos um estojo\n"
	.string "no mirante do sul.$"

EryonDragoes_Text_CourierDecline:
	.string "ECLIPSE: Entao nao\n"
	.string "atrapalhe meu trabalho.$"

EryonDragoes_Text_CourierAfter:
	.string "ECLIPSE: Voce venceu.\p"
	.string "O mirante ao sul\n"
	.string "ainda guarda uma caixa.$"

EryonDragoes_Text_CacheLocked:
	.string "Um estojo lacrado\n"
	.string "com o selo ECLIPSE.\p"
	.string "A escolta ainda\n"
	.string "controla a carga.$"

EryonDragoes_Text_CacheOpened:
	.string "A remessa abandonada\n"
	.string "guarda um DRAGON FANG!$"

EryonDragoes_Text_CacheBagFull:
	.string "Sua BOLSA esta cheia.\p"
	.string "O item ficara aqui\n"
	.string "ate sua volta.$"

EryonDragoes_Text_CacheEmpty:
	.string "O estojo esta vazio.\p"
	.string "A remessa foi recolhida.$"

EryonDragoes_Text_CliffResearcherBefore:
	.string "BIOLOGO: Os ventos\n"
	.string "da encosta sao fortes.\p"
	.string "Pokemon voadores\n"
	.string "costumam passar aqui.$"

EryonDragoes_Text_CliffResearcherClue:
	.string "BIOLOGO: O som\n"
	.string "das pedras mudou!\p"
	.string "A ECLIPSE controla\n"
	.string "algum tipo de carga.$"

EryonDragoes_Text_CliffResearcherAfter:
	.string "BIOLOGO: A escolta\n"
	.string "da ECLIPSE recuou!\p"
	.string "Agora podemos estudar\n"
	.string "o voo dos Pokemon.$"
