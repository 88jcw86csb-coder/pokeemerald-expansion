Eryon_VilaDasAguas_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Eryon_VilaDasAguas_RespawnCheckpoint
	.byte 0

@ Rest stop: remember the safe village, preserve all Eclipse events.
Eryon_VilaDasAguas_RespawnCheckpoint:
	setrespawn HEAL_LOCATION_ERYON_VILA_DAS_AGUAS
	end

@ River pollution links the village to Eclipse's stolen crystal cargo.
EryonAguas_EventScript_Fisher::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_RIVER_SAMPLE_RECORDED, EryonAguas_EventScript_FisherSample
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonAguas_EventScript_FisherClue
	msgbox EryonAguas_Text_FisherBefore, MSGBOX_DEFAULT
	release
	end

EryonAguas_EventScript_FisherClue::
	msgbox EryonAguas_Text_FisherClue, MSGBOX_DEFAULT
	release
	end

EryonAguas_EventScript_Healer::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonAguas_EventScript_HealerClue
	msgbox EryonAguas_Text_HealerBefore, MSGBOX_DEFAULT
	release
	end

EryonAguas_EventScript_HealerClue::
	msgbox EryonAguas_Text_HealerClue, MSGBOX_DEFAULT
	release
	end

EryonAguas_EventScript_WaterNotice::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonAguas_EventScript_WaterNoticeClue
	msgbox EryonAguas_Text_WaterNoticeBefore, MSGBOX_DEFAULT
	release
	end

EryonAguas_EventScript_WaterNoticeClue::
	msgbox EryonAguas_Text_WaterNoticeClue, MSGBOX_DEFAULT
	release
	end

EryonAguas_Text_FisherBefore:
	.string "PESCADOR: O rio esta\n"
	.string "estranho desde ontem.\p"
	.string "Os peixes sumiram perto\n"
	.string "da grande cachoeira.$"

EryonAguas_Text_FisherClue:
	.string "PESCADOR: Cristais da\n"
	.string "ECLIPSE cairam no rio?\p"
	.string "Vi uma barcaca seguir\n"
	.string "para o sul, ao oasis.$"

EryonAguas_Text_HealerBefore:
	.string "MORADORA: A agua anda\n"
	.string "turva perto das pedras.\p"
	.string "Pedimos que os viajantes\n"
	.string "evitem beber do rio.$"

EryonAguas_Text_HealerClue:
	.string "MORADORA: O brilho na\n"
	.string "agua nao e natural.\p"
	.string "Os cristais podem estar\n"
	.string "afetando os Pokemon.$"

EryonAguas_Text_WaterNoticeBefore:
	.string "AVISO: Acesso ao rio\n"
	.string "sob observacao.\p"
	.string "A vila esta analisando\n"
	.string "a qualidade da agua.$"

EryonAguas_Text_WaterNoticeClue:
	.string "AVISO: Residuos de\n"
	.string "cristal foram encontrados.\p"
	.string "Investigue a rota que\n"
	.string "leva ao oasis.$"

@ River sample reward can be claimed once, even when the Bag was full.
EryonAguas_EventScript_RiverResearcher::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_RIVER_SAMPLE_REWARD_CLAIMED, EryonAguas_EventScript_RiverResearcherDone
	goto_if_unset FLAG_ERYON_RIVER_SAMPLE_RECORDED, EryonAguas_EventScript_RiverResearcherWaiting
	msgbox EryonAguas_Text_RiverResearcherReward, MSGBOX_DEFAULT
	giveitem ITEM_MYSTIC_WATER
	goto_if_eq VAR_RESULT, FALSE, EryonAguas_EventScript_RiverResearcherFull
	setflag FLAG_ERYON_RIVER_SAMPLE_REWARD_CLAIMED
	msgbox EryonAguas_Text_RiverResearcherAwarded, MSGBOX_DEFAULT
	release
	end

EryonAguas_EventScript_RiverResearcherWaiting::
	msgbox EryonAguas_Text_RiverResearcherWaiting, MSGBOX_DEFAULT
	release
	end

EryonAguas_EventScript_RiverResearcherFull::
	msgbox EryonAguas_Text_RiverResearcherFull, MSGBOX_DEFAULT
	release
	end

EryonAguas_EventScript_RiverResearcherDone::
	msgbox EryonAguas_Text_RiverResearcherDone, MSGBOX_DEFAULT
	release
	end

EryonAguas_EventScript_FisherSample::
	msgbox EryonAguas_Text_FisherSample, MSGBOX_DEFAULT
	release
	end

EryonAguas_Text_RiverResearcherWaiting:
	.string "PESQUISADORA: O rio\n"
	.string "esta contaminado.\p"
	.string "Na ROTA DAS CACHOEIRAS\n"
	.string "ha um posto de coleta.\p"
	.string "Traga dados para que\n"
	.string "possamos investigar.$"

EryonAguas_Text_RiverResearcherReward:
	.string "PESQUISADORA: A amostra\n"
	.string "confirmou a ECLIPSE!\p"
	.string "Receba este premio\n"
	.string "pela sua ajuda.$"

EryonAguas_Text_RiverResearcherAwarded:
	.string "O rio deve melhorar\n"
	.string "quando a rede parar.\p"
	.string "A trilha do OASIS leva\n"
	.string "as cargas a IGNIVAR.$"

EryonAguas_Text_RiverResearcherFull:
	.string "Sua BOLSA esta cheia.\p"
	.string "Voltarei a guardar\n"
	.string "seu premio ate voltar.$"

EryonAguas_Text_RiverResearcherDone:
	.string "PESQUISADORA: Obrigada!\p"
	.string "Seguiremos os dados\n"
	.string "ate a usina de IGNIVAR.$"

EryonAguas_Text_FisherSample:
	.string "PESCADOR: A amostra\n"
	.string "mostrou o que ocorreu!\p"
	.string "A ECLIPSE contaminou\n"
	.string "as aguas do rio.$"

