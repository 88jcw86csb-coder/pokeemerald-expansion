Eryon_SerraDosCristais_MapScripts::
	.byte 0

@ Eryon: the first foothills beyond the eastern trail.
EryonSerra_EventScript_Geologist::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_SERRA_ECLIPSE_SIGNAL_DISABLED, EryonSerra_EventScript_GeologistResonanceQuiet
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonSerra_EventScript_GeologistBadge
	msgbox EryonSerra_Text_GeologistBefore, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_GeologistBadge::
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonSerra_EventScript_GeologistAfterClue
	msgbox EryonSerra_Text_GeologistBadge, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_GeologistAfterClue::
	msgbox EryonSerra_Text_GeologistAfterClue, MSGBOX_DEFAULT
	release
	end

@ The explorer reacts to the discovered Eclipse camp, preserving the slow investigation arc.
EryonSerra_EventScript_Explorer::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_SERRA_ECLIPSE_SIGNAL_DISABLED, EryonSerra_EventScript_ExplorerResonanceQuiet
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonSerra_EventScript_ExplorerAfterClue
	msgbox EryonSerra_Text_Explorer, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_ExplorerAfterClue::
	msgbox EryonSerra_Text_ExplorerAfterClue, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_CrystalOutcrop::
	lock
	msgbox EryonSerra_Text_CrystalOutcrop, MSGBOX_DEFAULT
	release
	end

EryonSerra_Text_GeologistBefore:
	.string "GEOLOGO: Esta serra e antiga.\p"
	.string "As pedras guardam marcas\n"
	.string "de muito antes das cidades.$"

EryonSerra_Text_GeologistBadge:
	.string "GEOLOGO: O simbolo do eclipse\n"
	.string "apareceu nos meus estudos.\p"
	.string "Alguem retirou cristais\n"
	.string "desta encosta recentemente.$"

EryonSerra_Text_GeologistAfterClue:
	.string "GEOLOGO: Voce encontrou\n"
	.string "o acampamento abandonado?\p"
	.string "Os cristais foram retirados\n"
	.string "com ferramentas recentes.\p"
	.string "Nao e uma escavacao antiga.\n"
	.string "Alguem planejou essa coleta.$"

EryonSerra_Text_Explorer:
	.string "EXPLORADORA: Nao tenha pressa.\p"
	.string "Ha caminhos escondidos\n"
	.string "entre as pedras da serra.$"

EryonSerra_Text_ExplorerAfterClue:
	.string "EXPLORADORA: As pegadas do\n"
	.string "acampamento seguem para leste.\p"
	.string "A passagem rochosa pode\n"
	.string "esconder mais pistas.$"

EryonSerra_Text_CrystalOutcrop:
	.string "Uma rocha foi escavada.\p"
	.string "Pequenos fragmentos brilham\n"
	.string "sob a luz do sol.$"


@ New Serra characters: scout, historian and repeatable field medic.
EryonSerra_EventScript_YoungScout::
	lock
	faceplayer
	msgbox EryonSerra_Text_YoungScout, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_Archivist::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonSerra_EventScript_ArchivistBadge
	msgbox EryonSerra_Text_ArchivistBefore, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_ArchivistBadge::
	msgbox EryonSerra_Text_ArchivistBadge, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_Medic::
	lock
	faceplayer
	msgbox EryonSerra_Text_MedicOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonSerra_EventScript_MedicDecline
	special HealPlayerParty
	msgbox EryonSerra_Text_MedicHealed, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_MedicDecline::
	msgbox EryonSerra_Text_MedicDecline, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_AbandonedCamp::
	lock
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonSerra_EventScript_AbandonedCampBadge
	msgbox EryonSerra_Text_AbandonedCampBefore, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_AbandonedCampBadge::
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonSerra_EventScript_AbandonedCampKnown
	msgbox EryonSerra_Text_AbandonedCampBadge, MSGBOX_DEFAULT
	setvar VAR_ERYON_SERRA_CLUE_FOUND, 1
	release
	end

EryonSerra_EventScript_AbandonedCampKnown::
	msgbox EryonSerra_Text_AbandonedCampKnown, MSGBOX_DEFAULT
	release
	end

EryonSerra_Text_YoungScout:
	.string "ESCOTEIRO: Encontrei marcas\n"
	.string "de botas perto das rochas.\p"
	.string "Nao parecem de turistas.$"

EryonSerra_Text_ArchivistBefore:
	.string "HISTORIADOR: Esta serra\n"
	.string "tem historias esquecidas.\p"
	.string "Os cristais nao sao comuns.$"

EryonSerra_Text_ArchivistBadge:
	.string "HISTORIADOR: O eclipse era\n"
	.string "um simbolo de antigas lendas.\p"
	.string "Quem busca os cristais pode\n"
	.string "estar seguindo essas lendas.$"

EryonSerra_Text_MedicOffer:
	.string "SOCORRISTA: Posso recuperar\n"
	.string "sua equipe Pokemon. Aceita?$"

EryonSerra_Text_MedicHealed:
	.string "Seus Pokemon estao bem!\n"
	.string "Cuidado nas trilhas.$"

EryonSerra_Text_MedicDecline:
	.string "Estarei aqui se precisar.$"

EryonSerra_Text_AbandonedCampBefore:
	.string "Um acampamento foi deixado\n"
	.string "as pressas entre as pedras.$"

EryonSerra_Text_AbandonedCampBadge:
	.string "Uma caixa vazia traz um\n"
	.string "simbolo de eclipse.\p"
	.string "Ha sinais de cristais que\n"
	.string "foram levados daqui.$"

EryonSerra_EventScript_EclipseScout::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonSerra_EventScript_EclipseScoutAfterClue
	trainerbattle_single TRAINER_ERYON_SERRA_ECLIPSE, EryonSerra_Text_TrainerChallenge, EryonSerra_Text_TrainerDefeat, EryonSerra_EventScript_TrainerVictory, FALSE
	msgbox EryonSerra_Text_TrainerAfter, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_EclipseScoutAfterClue::
	trainerbattle_single TRAINER_ERYON_SERRA_ECLIPSE, EryonSerra_Text_TrainerClueChallenge, EryonSerra_Text_TrainerDefeat, EryonSerra_EventScript_TrainerVictory, FALSE
	msgbox EryonSerra_Text_TrainerAfterClue, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_TrainerVictory::
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonSerra_EventScript_TrainerVictoryAfterClue
	msgbox EryonSerra_Text_TrainerAfter, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_TrainerVictoryAfterClue::
	msgbox EryonSerra_Text_TrainerAfterClue, MSGBOX_DEFAULT
	release
	end

EryonSerra_Text_TrainerChallenge:
	.string "VIGIA: Ninguem deve ver\n"
	.string "o que levamos da serra!$"

EryonSerra_Text_TrainerDefeat:
	.string "VIGIA: Fui derrotado!$"

EryonSerra_Text_TrainerAfter:
	.string "VIGIA: Voce nao deveria\n"
	.string "ter chegado tao longe.$"

EryonSerra_Text_TrainerClueChallenge:
	.string "VIGIA: Mexeu no acampamento?\p"
	.string "Entao viu nossas caixas!\n"
	.string "Nao vai passar daqui!$"

EryonSerra_Text_TrainerAfterClue:
	.string "VIGIA: Aquelas caixas ja\n"
	.string "foram levadas daqui.\p"
	.string "Nao sei para onde foram.\n"
	.string "Pare de fazer perguntas!$"


@ Optional one-time supply find, with retry if the bag is full.
EryonSerra_EventScript_SupplyCrate::
	lock
	goto_if_ge VAR_ERYON_SERRA_SUPPLY_FOUND, 1, EryonSerra_EventScript_SupplyCrateEmpty
	msgbox EryonSerra_Text_SupplyCrate, MSGBOX_DEFAULT
	giveitem ITEM_SUPER_POTION
	goto_if_eq VAR_RESULT, FALSE, EryonSerra_EventScript_SupplyCrateFull
	setvar VAR_ERYON_SERRA_SUPPLY_FOUND, 1
	release
	end

EryonSerra_EventScript_SupplyCrateFull::
	msgbox EryonSerra_Text_SupplyCrateFull, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_SupplyCrateEmpty::
	msgbox EryonSerra_Text_SupplyCrateEmpty, MSGBOX_DEFAULT
	release
	end

EryonSerra_Text_AbandonedCampKnown:
	.string "Voce ja investigou o\n"
	.string "simbolo do eclipse aqui.\p"
	.string "As pistas seguem pela serra.$"

EryonSerra_Text_SupplyCrate:
	.string "Uma caixa esquecida contem\n"
	.string "uma Super Pocao!$"

EryonSerra_Text_SupplyCrateFull:
	.string "Nao ha espaco na bolsa.\p"
	.string "O item continuara aqui.$"

EryonSerra_Text_SupplyCrateEmpty:
	.string "A caixa esta vazia.$"


@ The player investigates Serra's three Eclipse resonance stations in order.
@ The optional investigation is unlocked by the abandoned camp clue and Badge 3.
@ All four Serra exits stay open; no compulsory route blocker is introduced.
EryonSerra_EventScript_NorthCrystalSeal::
	lock
	goto_if_set FLAG_ERYON_SERRA_ECLIPSE_SIGNAL_DISABLED, EryonSerra_EventScript_ResonanceQuiet
	goto_if_set FLAG_ERYON_SERRA_NORTH_CRYSTAL_CALIBRATED, EryonSerra_EventScript_NorthCrystalCalibrated
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonSerra_EventScript_NorthClueFound
	msgbox EryonSerra_Text_NorthCrystalUnknown, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_NorthClueFound::
	goto_if_unset FLAG_BADGE03_GET, EryonSerra_EventScript_NorthNeedsBadge
	msgbox EryonSerra_Text_NorthCrystalPrompt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonSerra_EventScript_ResonanceLeave
	closemessage
	setflag FLAG_ERYON_SERRA_NORTH_CRYSTAL_CALIBRATED
	msgbox EryonSerra_Text_NorthCrystalDone, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_NorthNeedsBadge::
	msgbox EryonSerra_Text_NorthNeedsBadge, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_NorthCrystalCalibrated::
	msgbox EryonSerra_Text_NorthCrystalCalibrated, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_SouthCrystalSeal::
	lock
	goto_if_set FLAG_ERYON_SERRA_ECLIPSE_SIGNAL_DISABLED, EryonSerra_EventScript_ResonanceQuiet
	goto_if_set FLAG_ERYON_SERRA_SOUTH_CRYSTAL_CALIBRATED, EryonSerra_EventScript_SouthCrystalCalibrated
	goto_if_unset FLAG_ERYON_SERRA_NORTH_CRYSTAL_CALIBRATED, EryonSerra_EventScript_SouthNeedsNorth
	msgbox EryonSerra_Text_SouthCrystalPrompt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonSerra_EventScript_ResonanceLeave
	closemessage
	setflag FLAG_ERYON_SERRA_SOUTH_CRYSTAL_CALIBRATED
	msgbox EryonSerra_Text_SouthCrystalDone, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_SouthNeedsNorth::
	msgbox EryonSerra_Text_SouthNeedsNorth, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_SouthCrystalCalibrated::
	msgbox EryonSerra_Text_SouthCrystalCalibrated, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_EclipseResonanceCore::
	lock
	goto_if_set FLAG_ERYON_SERRA_ECLIPSE_SIGNAL_DISABLED, EryonSerra_EventScript_ResonanceQuiet
	goto_if_unset FLAG_ERYON_SERRA_NORTH_CRYSTAL_CALIBRATED, EryonSerra_EventScript_CoreNeedsSeals
	goto_if_unset FLAG_ERYON_SERRA_SOUTH_CRYSTAL_CALIBRATED, EryonSerra_EventScript_CoreNeedsSeals
	msgbox EryonSerra_Text_CorePrompt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonSerra_EventScript_ResonanceLeave
	closemessage
	setflag FLAG_ERYON_SERRA_ECLIPSE_SIGNAL_DISABLED
	msgbox EryonSerra_Text_CoreDisabled, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_CoreNeedsSeals::
	msgbox EryonSerra_Text_CoreNeedsSeals, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_ResonanceQuiet::
	msgbox EryonSerra_Text_ResonanceQuiet, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_ResonanceLeave::
	closemessage
	release
	end

@ Persistent field reports react to the completed optional investigation.
EryonSerra_EventScript_GeologistResonanceQuiet::
	msgbox EryonSerra_Text_GeologistResonanceQuiet, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_ExplorerResonanceQuiet::
	msgbox EryonSerra_Text_ExplorerResonanceQuiet, MSGBOX_DEFAULT
	release
	end

EryonSerra_Text_NorthCrystalUnknown:
	.string "Um selo brilha\n"
	.string "junto a rocha.\p"
	.string "Investigue as caixas\n"
	.string "do acampamento.$"

EryonSerra_Text_NorthNeedsBadge:
	.string "SINAL DESCONHECIDO:\p"
	.string "A INSIGNIA de\n"
	.string "FROSTHEIM pode ajudar.$"

EryonSerra_Text_NorthCrystalPrompt:
	.string "Selo de cristal norte.\p"
	.string "Usar os dados de gelo\n"
	.string "para alinhar a runa?$"

EryonSerra_Text_NorthCrystalDone:
	.string "O primeiro selo\n"
	.string "foi alinhado!\p"
	.string "O segundo fica\n"
	.string "ao sul da serra.$"

EryonSerra_Text_NorthCrystalCalibrated:
	.string "SELO NORTE:\n"
	.string "alinhamento estavel.$"

EryonSerra_Text_SouthNeedsNorth:
	.string "SELO SUL:\n"
	.string "O cristal norte\n"
	.string "ainda esta ativo.$"

EryonSerra_Text_SouthCrystalPrompt:
	.string "SELO SUL:\n"
	.string "O sinal do norte\n"
	.string "esta sincronizado.\p"
	.string "Alinhar o cristal?$"

EryonSerra_Text_SouthCrystalDone:
	.string "Os dois selos\n"
	.string "estao alinhados!\p"
	.string "O nucleo central\n"
	.string "agora esta exposto.$"

EryonSerra_Text_SouthCrystalCalibrated:
	.string "SELO SUL:\n"
	.string "alinhamento estavel.$"

EryonSerra_Text_CoreNeedsSeals:
	.string "NUCLEO DA ECLIPSE:\p"
	.string "Sinais misturados\n"
	.string "nos cristais.\p"
	.string "Dois selos devem\n"
	.string "ser alinhados.$"

EryonSerra_Text_CorePrompt:
	.string "NUCLEO DA ECLIPSE:\p"
	.string "Os selos estao\n"
	.string "sincronizados.\p"
	.string "Desligar a rede?$"

EryonSerra_Text_CoreDisabled:
	.string "A rede de cristais\n"
	.string "foi desligada!\p"
	.string "A ECLIPSE perdeu\n"
	.string "o sinal nesta serra.$"

EryonSerra_Text_ResonanceQuiet:
	.string "Os cristais estao\n"
	.string "silenciosos.\p"
	.string "A rede da ECLIPSE\n"
	.string "continua desligada.$"

EryonSerra_Text_GeologistResonanceQuiet:
	.string "GEOLOGO: Conseguimos!\p"
	.string "As rochas nao enviam\n"
	.string "mais dados a ECLIPSE.\p"
	.string "Avisarei ARKHARA.$"

EryonSerra_Text_ExplorerResonanceQuiet:
	.string "EXPLORADORA: A serra\n"
	.string "esta mais tranquila!\p"
	.string "A passagem rochosa\n"
	.string "esta pronta para voce.$"
