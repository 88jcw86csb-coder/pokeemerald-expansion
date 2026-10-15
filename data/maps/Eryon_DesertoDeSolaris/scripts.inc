Eryon_DesertoDeSolaris_MapScripts::
	.byte 0

@ Eclipse uses a buried relay to move crystal energy toward Ignivar.
EryonSolaris_EventScript_Explorer::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonSolaris_EventScript_ExplorerClue
	msgbox EryonSolaris_Text_ExplorerBefore, MSGBOX_DEFAULT
	release
	end

EryonSolaris_EventScript_ExplorerClue::
	msgbox EryonSolaris_Text_ExplorerClue, MSGBOX_DEFAULT
	release
	end

EryonSolaris_EventScript_EclipseGuard::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonSolaris_EventScript_EclipseGuardClue
	msgbox EryonSolaris_Text_GuardBefore, MSGBOX_DEFAULT
	release
	end

EryonSolaris_EventScript_EclipseGuardClue::
	msgbox EryonSolaris_Text_GuardClue, MSGBOX_DEFAULT
	release
	end

EryonSolaris_EventScript_BuriedDevice::
	lock
	goto_if_set FLAG_ERYON_RIVER_SAMPLE_RECORDED, EryonSolaris_EventScript_DeviceRiverData
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonSolaris_EventScript_BuriedDeviceClue
	msgbox EryonSolaris_Text_DeviceBefore, MSGBOX_DEFAULT
	release
	end

EryonSolaris_EventScript_BuriedDeviceClue::
	msgbox EryonSolaris_Text_DeviceClue, MSGBOX_DEFAULT
	release
	end

EryonSolaris_Text_ExplorerBefore:
	.string "EXPLORADOR: As dunas\n"
	.string "mudam com o vento.\p"
	.string "Siga as pedras para\n"
	.string "alcancar Ignivar.$"

EryonSolaris_Text_ExplorerClue:
	.string "EXPLORADOR: Uma equipe\n"
	.string "enterrou cabos na areia.\p"
	.string "Levam energia para\n"
	.string "a usina de Ignivar.$"

EryonSolaris_Text_GuardBefore:
	.string "VIGIA: A passagem esta\n"
	.string "sob observacao.\p"
	.string "Nao toque no equipamento.$"

EryonSolaris_Text_GuardClue:
	.string "ECLIPSE: Os cristais\n"
	.string "alimentam nosso reator!\p"
	.string "Ignivar nao imagina\n"
	.string "quando vier o pulso.$"

EryonSolaris_Text_DeviceBefore:
	.string "Uma antena emerge\n"
	.string "parcialmente da areia.\p"
	.string "Ha cabos enterrados.$"

EryonSolaris_Text_DeviceClue:
	.string "O selo da ECLIPSE\n"
	.string "cobre um transmissor.\p"
	.string "Um cabo segue na\n"
	.string "direcao da usina.$"

@ Additional local witness to the Eclipse signal crossing Eryon.
EryonSolaris_EventScript_CaravanScout::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_RIVER_SAMPLE_RECORDED, EryonSolaris_EventScript_CaravanScoutWaterEvidence
	msgbox EryonSolaris_Text_CaravanScout, MSGBOX_DEFAULT
	release
	end

EryonSolaris_Text_CaravanScout:
	.string "GUIA: As marcas na areia\n"
	.string "nao sao de Pokemon.\p"
	.string "Um comboio ECLIPSE\n"
	.string "seguiu para Ignivar.$"

@ Evidence collected upriver identifies the buried Eclipse transmitters.
EryonSolaris_EventScript_DeviceRiverData::
	msgbox EryonSolaris_Text_DeviceRiverData, MSGBOX_DEFAULT
	release
	end

EryonSolaris_EventScript_CaravanScoutWaterEvidence::
	msgbox EryonSolaris_Text_CaravanScoutWaterEvidence, MSGBOX_DEFAULT
	release
	end

EryonSolaris_Text_DeviceRiverData:
	.string "A antena usa cristais\n"
	.string "como os vistos no rio!\p"
	.string "O cabo segue para\n"
	.string "a usina de IGNIVAR.$"

EryonSolaris_Text_CaravanScoutWaterEvidence:
	.string "GUIA: Os exames da\n"
	.string "vila chegaram aqui!\p"
	.string "A ECLIPSE deixou provas\n"
	.string "desde as CACHOEIRAS.\p"
	.string "Siga para IGNIVAR,\n"
	.string "mas tome cuidado.$"



@ Optional canyon cut into the original Solaris route; Eclipse story adapts.
EryonSolaris_EventScript_SolarCanyon::
	lock
	goto_if_set FLAG_ERYON_RIVER_SAMPLE_RECORDED, EryonSolaris_EventScript_SolarCanyonRiver
	msgbox EryonSolaris_Text_SolarCanyonBefore, MSGBOX_DEFAULT
	release
	end

EryonSolaris_EventScript_SolarCanyonRiver::
	msgbox EryonSolaris_Text_SolarCanyonRiver, MSGBOX_DEFAULT
	release
	end

EryonSolaris_Text_SolarCanyonBefore:
	.string "CANION SOLAR:\p"
	.string "Rochas altas formam\n"
	.string "um abrigo na areia.\p"
	.string "Rodas de uma caravana\n"
	.string "deixaram marcas aqui.$"

EryonSolaris_Text_SolarCanyonRiver:
	.string "CANION SOLAR:\p"
	.string "As marcas da caravana\n"
	.string "cruzam todo o deserto.\p"
	.string "A agua investigada\n"
	.string "pode revelar a rota.$"


@ Optional supplies discovered in the shelter of the newly carved canyon.
@ Preserve the item when the player's Bag is full.
EryonSolaris_EventScript_CanyonSupplies::
	lock
	goto_if_set FLAG_ERYON_SOLAR_CANYON_SUPPLIES_CLAIMED, EryonSolaris_EventScript_CanyonSuppliesEmpty
	msgbox EryonSolaris_Text_CanyonSuppliesOffer, MSGBOX_DEFAULT
	giveitem ITEM_HYPER_POTION
	goto_if_eq VAR_RESULT, FALSE, EryonSolaris_EventScript_CanyonSuppliesBagFull
	setflag FLAG_ERYON_SOLAR_CANYON_SUPPLIES_CLAIMED
	release
	end

EryonSolaris_EventScript_CanyonSuppliesBagFull::
	msgbox EryonSolaris_Text_CanyonSuppliesBagFull, MSGBOX_DEFAULT
	release
	end

EryonSolaris_EventScript_CanyonSuppliesEmpty::
	msgbox EryonSolaris_Text_CanyonSuppliesEmpty, MSGBOX_DEFAULT
	release
	end

EryonSolaris_Text_CanyonSuppliesOffer:
	.string "ABRIGO DO CANION:\p"
	.string "Uma HYPER POTION\n"
	.string "foi deixada aqui.$"

EryonSolaris_Text_CanyonSuppliesBagFull:
	.string "Sua BOLSA esta cheia!\p"
	.string "O remedio continuara\n"
	.string "no abrigo.$"

EryonSolaris_Text_CanyonSuppliesEmpty:
	.string "A caixa de suprimentos\n"
	.string "esta vazia.$"


@ Optional battle along the new canyon; defeat uses a dedicated saved trainer flag.
EryonSolaris_EventScript_CanyonRanger::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_SOLAR_CANYON_RANGER_DEFEATED, EryonSolaris_EventScript_CanyonRangerAfter
	msgbox EryonSolaris_Text_CanyonRangerOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonSolaris_EventScript_CanyonRangerDecline
	closemessage
	trainerbattle_single TRAINER_ERYON_SOLAR_CANYON_RANGER, EryonSolaris_Text_CanyonRangerIntro, EryonSolaris_Text_CanyonRangerLoss, EryonSolaris_EventScript_CanyonRangerVictory, FALSE
	msgbox EryonSolaris_Text_CanyonRangerAfter, MSGBOX_DEFAULT
	release
	end

EryonSolaris_EventScript_CanyonRangerDecline::
	closemessage
	release
	end

EryonSolaris_EventScript_CanyonRangerVictory::
	msgbox EryonSolaris_Text_CanyonRangerVictory, MSGBOX_DEFAULT
	release
	end

EryonSolaris_EventScript_CanyonRangerAfter::
	msgbox EryonSolaris_Text_CanyonRangerAfter, MSGBOX_DEFAULT
	release
	end

EryonSolaris_Text_CanyonRangerOffer:
	.string "DARIO: Exploro esta\n"
	.string "trilha sob o sol!\p"
	.string "Quer treinar comigo?$"

EryonSolaris_Text_CanyonRangerIntro:
	.string "Vamos ver como sua\n"
	.string "equipe lida com areia!$"

EryonSolaris_Text_CanyonRangerLoss:
	.string "Que equipe resistente!$"

EryonSolaris_Text_CanyonRangerVictory:
	.string "DARIO: O canion agora\n"
	.string "faz parte de sua rota!$"

EryonSolaris_Text_CanyonRangerAfter:
	.string "DARIO: Um HELIOPTILE\n"
	.string "bem treinado evolui\n"
	.string "no nivel 36.$"
