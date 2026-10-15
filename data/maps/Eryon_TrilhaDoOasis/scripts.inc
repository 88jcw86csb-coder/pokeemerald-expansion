Eryon_TrilhaDoOasis_MapScripts::
	.byte 0

@ The cargo trail leaves the river and heads toward the Solaris desert.
EryonOasis_EventScript_Guide::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_OASIS_HELIOPTILE_RESOLVED, EryonOasis_EventScript_GuideHelioptile
	goto_if_set FLAG_ERYON_RIVER_SAMPLE_RECORDED, EryonOasis_EventScript_GuideWaterEvidence
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonOasis_EventScript_GuideClue
	msgbox EryonOasis_Text_GuideBefore, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_GuideClue::
	msgbox EryonOasis_Text_GuideClue, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_EclipseCarrier::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_RIVER_SAMPLE_RECORDED, EryonOasis_EventScript_CarrierWaterEvidence
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonOasis_EventScript_EclipseCarrierClue
	msgbox EryonOasis_Text_CarrierBefore, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_EclipseCarrierClue::
	msgbox EryonOasis_Text_CarrierClue, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_DryCanister::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonOasis_EventScript_DryCanisterClue
	msgbox EryonOasis_Text_CanisterBefore, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_DryCanisterClue::
	msgbox EryonOasis_Text_CanisterClue, MSGBOX_DEFAULT
	release
	end

EryonOasis_Text_GuideBefore:
	.string "GUIA: Esta trilha liga\n"
	.string "o rio ao deserto.\p"
	.string "Leve agua e procure\n"
	.string "abrigo nas palmeiras.$"

EryonOasis_Text_GuideClue:
	.string "GUIA: Uma caravana\n"
	.string "trouxe caixas de Umbra.\p"
	.string "Seguiram para Solaris\n"
	.string "antes do amanhecer.$"

EryonOasis_Text_CarrierBefore:
	.string "VIAJANTE: Transporto\n"
	.string "mantimentos ao deserto.\p"
	.string "Nao tenho tempo para\n"
	.string "conversas.$"

EryonOasis_Text_CarrierClue:
	.string "ECLIPSE: Os cristais\n"
	.string "ja estao em Solaris!\p"
	.string "Nosso plano nao pode\n"
	.string "ser interrompido.$"

EryonOasis_Text_CanisterBefore:
	.string "Um recipiente vazio\n"
	.string "esta entre as pedras.\p"
	.string "O rotulo foi removido.$"

EryonOasis_Text_CanisterClue:
	.string "O recipiente contem\n"
	.string "po azul cristalino.\p"
	.string "Um selo da ECLIPSE\n"
	.string "aponta para Solaris.$"

@ Waterfall sample follows Eclipse's transport route past the oasis.
EryonOasis_EventScript_CaravanWaterRecord::
	lock
	goto_if_set FLAG_ERYON_RIVER_SAMPLE_RECORDED, EryonOasis_EventScript_WaterRecordConfirmed
	msgbox EryonOasis_Text_WaterRecordBefore, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_WaterRecordConfirmed::
	msgbox EryonOasis_Text_WaterRecordConfirmed, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_GuideWaterEvidence::
	msgbox EryonOasis_Text_GuideWaterEvidence, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_CarrierWaterEvidence::
	msgbox EryonOasis_Text_CarrierWaterEvidence, MSGBOX_DEFAULT
	release
	end

EryonOasis_Text_WaterRecordBefore:
	.string "MANIFESTO DA CARAVANA:\n"
	.string "Cargas trazidas do rio.\p"
	.string "Destino: IGNIVAR.\n"
	.string "Conteudo: sigiloso.$"

EryonOasis_Text_WaterRecordConfirmed:
	.string "MANIFESTO DA CARAVANA:\n"
	.string "O residuo coincide com\n"
	.string "o sinal da ECLIPSE!\p"
	.string "A proxima antena fica\n"
	.string "no DESERTO DE SOLARIS.$"

EryonOasis_Text_GuideWaterEvidence:
	.string "GUIA: A vila confirmou\n"
	.string "a origem dos residuos!\p"
	.string "Proteja seus Pokemon.\n"
	.string "As dunas vem adiante.$"

EryonOasis_Text_CarrierWaterEvidence:
	.string "ECLIPSE: Descobriram\n"
	.string "nossa carga no rio?!\p"
	.string "O reator de IGNIVAR\n"
	.string "ainda nos espera.$"



@ Optional Kalos wildlife in Eryon's river-to-desert passage.
@ Running or teleporting leaves the encounter available for another attempt.
EryonOasis_EventScript_HelioptileNest::
	lock
	goto_if_set FLAG_ERYON_OASIS_HELIOPTILE_RESOLVED, EryonOasis_EventScript_HelioptileQuiet
	msgbox EryonOasis_Text_HelioptileIntro, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonOasis_EventScript_HelioptileLeave
	closemessage
	setwildbattle SPECIES_HELIOPTILE, 32
	waitse
	playmoncry SPECIES_HELIOPTILE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, EryonOasis_EventScript_HelioptileResolved
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, EryonOasis_EventScript_HelioptileResolved
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, EryonOasis_EventScript_HelioptileEscaped
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, EryonOasis_EventScript_HelioptileEscaped
	release
	end

EryonOasis_EventScript_HelioptileResolved::
	setflag FLAG_ERYON_OASIS_HELIOPTILE_RESOLVED
	msgbox EryonOasis_Text_HelioptileResolved, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_HelioptileEscaped::
	msgbox EryonOasis_Text_HelioptileEscaped, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_HelioptileQuiet::
	msgbox EryonOasis_Text_HelioptileQuiet, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_HelioptileLeave::
	closemessage
	release
	end

EryonOasis_Text_HelioptileIntro:
	.string "Entre as pedras quentes\n"
	.string "ha um HELIOPTILE!\p"
	.string "Sua pele absorve a luz\n"
	.string "do sol do deserto.\p"
	.string "Investigar o abrigo?$"

EryonOasis_Text_HelioptileResolved:
	.string "O encontro terminou!\p"
	.string "O abrigo esta tranquilo.$"

EryonOasis_Text_HelioptileEscaped:
	.string "HELIOPTILE correu para\n"
	.string "tras das rochas!\p"
	.string "Ele pode voltar.$"

EryonOasis_Text_HelioptileQuiet:
	.string "As pedras ainda estao\n"
	.string "quentes ao sol.$"


@ A previously blocked caravan alcove branches off Eryon's desert approach.
EryonOasis_EventScript_CaravanAlcove::
	lock
	goto_if_set FLAG_ERYON_OASIS_HELIOPTILE_RESOLVED, EryonOasis_EventScript_AlcoveWildlifeSafe
	goto_if_set FLAG_ERYON_RIVER_SAMPLE_RECORDED, EryonOasis_EventScript_AlcoveRiverEvidence
	msgbox EryonOasis_Text_AlcoveBefore, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_AlcoveRiverEvidence::
	msgbox EryonOasis_Text_AlcoveRiverEvidence, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_AlcoveWildlifeSafe::
	msgbox EryonOasis_Text_AlcoveWildlifeSafe, MSGBOX_DEFAULT
	release
	end

EryonOasis_Text_AlcoveBefore:
	.string "REFUGIO DA CARAVANA:\p"
	.string "Uma passagem entre\n"
	.string "rochas leva ao norte.\p"
	.string "A areia cobre marcas\n"
	.string "de antigas carrocas.$"

EryonOasis_Text_AlcoveRiverEvidence:
	.string "REFUGIO DA CARAVANA:\p"
	.string "A agua do rio chegou\n"
	.string "ate esta passagem.\p"
	.string "Os rastros seguem\n"
	.string "rumo a SOLARIS.$"

EryonOasis_Text_AlcoveWildlifeSafe:
	.string "REFUGIO DA CARAVANA:\p"
	.string "O HELIOPTILE ja foi\n"
	.string "encontrado na trilha.\p"
	.string "O calor protege este\n"
	.string "pequeno refugio.$"


@ One-time desert survival medicine at the optional caravan refuge.
@ The item remains available if the player's bag is full.
EryonOasis_EventScript_AlcoveSupplies::
	lock
	goto_if_set FLAG_ERYON_OASIS_ALCOVE_SUPPLIES_TAKEN, EryonOasis_EventScript_AlcoveSuppliesEmpty
	msgbox EryonOasis_Text_AlcoveSupplies, MSGBOX_DEFAULT
	giveitem ITEM_HYPER_POTION
	goto_if_eq VAR_RESULT, FALSE, EryonOasis_EventScript_AlcoveSuppliesBagFull
	setflag FLAG_ERYON_OASIS_ALCOVE_SUPPLIES_TAKEN
	release
	end

EryonOasis_EventScript_AlcoveSuppliesBagFull::
	msgbox EryonOasis_Text_AlcoveSuppliesBagFull, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_AlcoveSuppliesEmpty::
	msgbox EryonOasis_Text_AlcoveSuppliesEmpty, MSGBOX_DEFAULT
	release
	end

EryonOasis_Text_AlcoveSupplies:
	.string "MANTIMENTOS ANTIGOS:\p"
	.string "Uma HYPER POTION\n"
	.string "resistiu ao deserto.$"

EryonOasis_Text_AlcoveSuppliesBagFull:
	.string "Sua BOLSA esta cheia!\p"
	.string "O remedio ainda\n"
	.string "ficara no abrigo.$"

EryonOasis_Text_AlcoveSuppliesEmpty:
	.string "A caixa da caravana\n"
	.string "agora esta vazia.$"


@ Existing guide recognizes the optional Kalos wildlife encounter.
EryonOasis_EventScript_GuideHelioptile::
	msgbox EryonOasis_Text_GuideHelioptile, MSGBOX_DEFAULT
	release
	end

EryonOasis_Text_GuideHelioptile:
	.string "GUIA: Voce encontrou\n"
	.string "o HELIOPTILE da trilha!\p"
	.string "Ele pode evoluir com\n"
	.string "treino, no nivel 36.\p"
	.string "Siga ate SOLARIS para\n"
	.string "explorar novas areas.$"
