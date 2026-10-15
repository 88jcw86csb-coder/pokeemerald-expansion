Eryon_TrilhaDosDragoes_MapScripts::
	.byte 0

@ Expedition through the rocky approach to Drakonia.
EryonDragoes_EventScript_RidgeGuide::
	lock
	faceplayer
	goto_if_set FLAG_BADGE08_GET, EryonDragoes_EventScript_RidgeGuideAfterBadge
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, EryonDragoes_EventScript_RidgeGuideManifest
	goto_if_set FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED, EryonDragoes_EventScript_RidgeGuideEcho
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
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonDragoes_EventScript_MarkerEvidenceFiled
	goto_if_set FLAG_ERYON_PICO_SIGNAL_REPAIRED, EryonDragoes_EventScript_MarkerRelayWorking
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, EryonDragoes_EventScript_MarkerManifest
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


@ Kalos wildlife encounter in the newly connected northern nesting terrace.
@ Captured or defeated Noibat is persistent; fleeing or teleporting permits retry.
@ No new wild-encounter table entries are required for this scripted encounter.
EryonDragoes_EventScript_NoibatNest::
	lock
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_NOIBAT_RESOLVED, EryonDragoes_EventScript_NoibatNestQuiet
	msgbox EryonDragoes_Text_NoibatNestIntro, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonDragoes_EventScript_NoibatNestLeave
	closemessage
	setwildbattle SPECIES_NOIBAT, 38
	waitse
	playmoncry SPECIES_NOIBAT, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, EryonDragoes_EventScript_NoibatNestResolved
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, EryonDragoes_EventScript_NoibatNestResolved
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, EryonDragoes_EventScript_NoibatNestEscaped
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, EryonDragoes_EventScript_NoibatNestEscaped
	release
	end

EryonDragoes_EventScript_NoibatNestResolved::
	setflag FLAG_ERYON_DRAGON_TRAIL_NOIBAT_RESOLVED
	msgbox EryonDragoes_Text_NoibatNestResolved, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_NoibatNestEscaped::
	msgbox EryonDragoes_Text_NoibatNestEscaped, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_NoibatNestQuiet::
	msgbox EryonDragoes_Text_NoibatNestQuiet, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_NoibatNestLeave::
	closemessage
	release
	end

@ Optional researcher interprets the nesting disturbance without blocking travel.
EryonDragoes_EventScript_NestResearcher::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_NOIBAT_RESOLVED, EryonDragoes_EventScript_NestResearcherAfter
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonDragoes_EventScript_NestResearcherEclipse
	msgbox EryonDragoes_Text_NestResearcherBefore, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_NestResearcherEclipse::
	msgbox EryonDragoes_Text_NestResearcherEclipse, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_NestResearcherAfter::
	msgbox EryonDragoes_Text_NestResearcherAfter, MSGBOX_DEFAULT
	release
	end

EryonDragoes_Text_NoibatNestIntro:
	.string "Um som agudo vem\n"
	.string "do ninho entre pedras!\p"
	.string "Um NOIBAT selvagem\n"
	.string "observa voce.\p"
	.string "Investigar o ninho?$"

EryonDragoes_Text_NoibatNestResolved:
	.string "O encontro terminou.\p"
	.string "O eco do ninho\n"
	.string "agora esta calmo.$"

EryonDragoes_Text_NoibatNestEscaped:
	.string "NOIBAT fugiu entre\n"
	.string "as pedras do pico!\p"
	.string "Talvez volte depois.$"

EryonDragoes_Text_NoibatNestQuiet:
	.string "Um pequeno ninho\n"
	.string "fica entre as rochas.\p"
	.string "Nao ha mais Pokemon\n"
	.string "aqui por enquanto.$"

EryonDragoes_Text_NestResearcherBefore:
	.string "ORNITOLOGA: Ha uma\n"
	.string "colonia de NOIBAT!\p"
	.string "Os ecos os ajudam\n"
	.string "a voar no escuro.$"

EryonDragoes_Text_NestResearcherEclipse:
	.string "ORNITOLOGA: A ECLIPSE\n"
	.string "perturba o voo deles.\p"
	.string "O ninho ao norte\n"
	.string "guarda um NOIBAT raro.$"

EryonDragoes_Text_NestResearcherAfter:
	.string "ORNITOLOGA: O ninho\n"
	.string "finalmente sossegou!\p"
	.string "Vou registrar a sua\n"
	.string "descoberta na vila.$"

@ The existing ridge guide follows the investigation from Echo Village through Drakonia.
@ Optional conversation only: no new flags, battles, species, or progression gates.
EryonDragoes_EventScript_RidgeGuideEcho:
	msgbox EryonDragoes_Text_RidgeGuideEcho, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_RidgeGuideManifest:
	msgbox EryonDragoes_Text_RidgeGuideManifest, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_RidgeGuideAfterBadge:
	msgbox EryonDragoes_Text_RidgeGuideAfterBadge, MSGBOX_DEFAULT
	release
	end

EryonDragoes_Text_RidgeGuideEcho:
	.string "GUIA: O arquivo dos\n"
	.string "ECOS detectou dois sons!\p"
	.string "As caixas na trilha\n"
	.string "podem revelar a origem.$"

EryonDragoes_Text_RidgeGuideManifest:
	.string "GUIA: Seu manifesto\n"
	.string "liga LUNARIS ao PICO!\p"
	.string "Os guardioes precisam\n"
	.string "conhecer essa rota.$"

EryonDragoes_Text_RidgeGuideAfterBadge:
	.string "GUIA: Oito INSIGNIAS!\p"
	.string "A ECLIPSE deixou marcas\n"
	.string "em toda a montanha.\p"
	.string "Siga para a LIGA\n"
	.string "e proteja os cristais.$"


@ Trail sign reflects prior decisions without changing travel, battles or save flags.

EryonDragoes_EventScript_MarkerEvidenceFiled::
	msgbox EryonDragoes_Text_MarkerEvidenceFiled, MSGBOX_DEFAULT
	release
	end

EryonDragoes_Text_MarkerEvidenceFiled:
	.string "OESTE: LUNARIS.\n"
	.string "LESTE: VILA DO PICO.\p"
	.string "A LIGA recebeu provas\n"
	.string "da rede ECLIPSE.$"

EryonDragoes_EventScript_MarkerRelayWorking::
	msgbox EryonDragoes_Text_MarkerRelayWorking, MSGBOX_DEFAULT
	release
	end

EryonDragoes_Text_MarkerRelayWorking:
	.string "OESTE: LUNARIS.\n"
	.string "LESTE: VILA DO PICO.\p"
	.string "A radio do PICO\n"
	.string "ja envia alertas.$"

EryonDragoes_EventScript_MarkerManifest::
	msgbox EryonDragoes_Text_MarkerManifest, MSGBOX_DEFAULT
	release
	end

EryonDragoes_Text_MarkerManifest:
	.string "OESTE: LUNARIS.\n"
	.string "LESTE: VILA DO PICO.\p"
	.string "As caixas ECLIPSE\n"
	.string "revelaram sua rota.$"
@ Eastern Aurora Crystal Terrace is an optional branch of the Dragon Trail.
@ The array records original crystal resonance, not mandatory story progress.
EryonDragoes_EventScript_AuroraCrystalArray::
	lock
	goto_if_set FLAG_ERYON_DRAGON_AURORA_ARRAY_READ, EryonDragoes_EventScript_AuroraArrayRepeat
	goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN, EryonDragoes_EventScript_AuroraArrayPeace
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, EryonDragoes_EventScript_AuroraArrayManifest
	msgbox EryonDragoes_Text_AuroraArrayBefore, MSGBOX_DEFAULT
	setflag FLAG_ERYON_DRAGON_AURORA_ARRAY_READ
	release
	end

EryonDragoes_EventScript_AuroraArrayManifest::
	msgbox EryonDragoes_Text_AuroraArrayManifest, MSGBOX_DEFAULT
	setflag FLAG_ERYON_DRAGON_AURORA_ARRAY_READ
	release
	end

EryonDragoes_EventScript_AuroraArrayPeace::
	msgbox EryonDragoes_Text_AuroraArrayPeace, MSGBOX_DEFAULT
	setflag FLAG_ERYON_DRAGON_AURORA_ARRAY_READ
	release
	end

EryonDragoes_EventScript_AuroraArrayRepeat::
	goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN, EryonDragoes_EventScript_AuroraArrayRestored
	msgbox EryonDragoes_Text_AuroraArrayRepeat, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_AuroraArrayRestored::
	msgbox EryonDragoes_Text_AuroraArrayRestored, MSGBOX_DEFAULT
	release
	end

@ Normal wild battle/EXP: capture or faint resolves, flee or refusal retries.
EryonDragoes_EventScript_CarbinkChamber::
	lock
	goto_if_set FLAG_ERYON_DRAGON_CARBINK_RESOLVED, EryonDragoes_EventScript_CarbinkQuiet
	goto_if_unset FLAG_ERYON_DRAGON_AURORA_ARRAY_READ, EryonDragoes_EventScript_CarbinkHidden
	msgbox EryonDragoes_Text_CarbinkOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonDragoes_EventScript_CarbinkDecline
	closemessage
	setwildbattle SPECIES_CARBINK, 43
	waitse
	playmoncry SPECIES_CARBINK, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, EryonDragoes_EventScript_CarbinkResolved
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, EryonDragoes_EventScript_CarbinkResolved
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, EryonDragoes_EventScript_CarbinkEscaped
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, EryonDragoes_EventScript_CarbinkEscaped
	release
	end

EryonDragoes_EventScript_CarbinkResolved::
	setflag FLAG_ERYON_DRAGON_CARBINK_RESOLVED
	msgbox EryonDragoes_Text_CarbinkResolved, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_CarbinkHidden::
	msgbox EryonDragoes_Text_CarbinkHidden, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_CarbinkEscaped::
	msgbox EryonDragoes_Text_CarbinkEscaped, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_CarbinkQuiet::
	msgbox EryonDragoes_Text_CarbinkQuiet, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_CarbinkDecline::
	closemessage
	release
	end

@ Max Ether remains claimable when Bag is full.
EryonDragoes_EventScript_AuroraSupplies::
	lock
	goto_if_set FLAG_ERYON_DRAGON_AURORA_SUPPLIES_TAKEN, EryonDragoes_EventScript_AuroraSuppliesEmpty
	goto_if_unset FLAG_ERYON_DRAGON_CARBINK_RESOLVED, EryonDragoes_EventScript_AuroraSuppliesLocked
	msgbox EryonDragoes_Text_AuroraSuppliesFound, MSGBOX_DEFAULT
	giveitem ITEM_MAX_ETHER
	goto_if_eq VAR_RESULT, FALSE, EryonDragoes_EventScript_AuroraSuppliesFull
	setflag FLAG_ERYON_DRAGON_AURORA_SUPPLIES_TAKEN
	release
	end

EryonDragoes_EventScript_AuroraSuppliesLocked::
	msgbox EryonDragoes_Text_AuroraSuppliesLocked, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_AuroraSuppliesFull::
	msgbox EryonDragoes_Text_AuroraSuppliesFull, MSGBOX_DEFAULT
	release
	end

EryonDragoes_EventScript_AuroraSuppliesEmpty::
	msgbox EryonDragoes_Text_AuroraSuppliesEmpty, MSGBOX_DEFAULT
	release
	end

EryonDragoes_Text_AuroraArrayBefore:
	.string "MIRANTE DA AURORA:\p"
	.string "Os cristais guardam\n"
	.string "um eco muito antigo.\p"
	.string "Uma luz artificial\n"
	.string "perturbou a encosta.$"

EryonDragoes_Text_AuroraArrayManifest:
	.string "MIRANTE DA AURORA:\p"
	.string "O manifesto da ECLIPSE\n"
	.string "cita estes cristais!\p"
	.string "Sua energia foi\n"
	.string "levada a DRAKONIA.$"

EryonDragoes_Text_AuroraArrayPeace:
	.string "MIRANTE DA AURORA:\p"
	.string "REDE ECLIPSE INATIVA.\p"
	.string "A montanha voltou\n"
	.string "ao equilibrio natural.$"

EryonDragoes_Text_AuroraArrayRepeat:
	.string "O mirante aponta\n"
	.string "para um CARBINK\n"
	.string "escondido nas pedras.$"

EryonDragoes_Text_AuroraArrayRestored:
	.string "A energia artificial\n"
	.string "desapareceu do mirante.\p"
	.string "Os cristais naturais\n"
	.string "continuam brilhando.$"

EryonDragoes_Text_CarbinkHidden:
	.string "Algo brilha entre\n"
	.string "as rochas.\p"
	.string "Leia o painel do\n"
	.string "MIRANTE primeiro.$"

EryonDragoes_Text_CarbinkOffer:
	.string "Um CARBINK surge\n"
	.string "dos cristais!\p"
	.string "Deseja investigar?$"

EryonDragoes_Text_CarbinkResolved:
	.string "CARBINK retorna\n"
	.string "aos cristais antigos.\p"
	.string "O mirante esta calmo.$"

EryonDragoes_Text_CarbinkEscaped:
	.string "CARBINK desapareceu\n"
	.string "entre as rochas.\p"
	.string "Pode voltar depois.$"

EryonDragoes_Text_CarbinkQuiet:
	.string "O mirante esta em paz\n"
	.string "e o eco ficou suave.$"

EryonDragoes_Text_AuroraSuppliesLocked:
	.string "Uma caixa fechada\n"
	.string "fica nas rochas.\p"
	.string "Um CARBINK vigia\n"
	.string "seu interior.$"

EryonDragoes_Text_AuroraSuppliesFound:
	.string "CAIXA DA AURORA:\p"
	.string "Um MAX ETHER estava\n"
	.string "guardado aqui.$"

EryonDragoes_Text_AuroraSuppliesFull:
	.string "Sua BOLSA esta cheia!\p"
	.string "O item pode ser\n"
	.string "recolhido depois.$"

EryonDragoes_Text_AuroraSuppliesEmpty:
	.string "A caixa da AURORA\n"
	.string "esta vazia.$"
