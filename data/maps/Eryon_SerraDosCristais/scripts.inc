Eryon_SerraDosCristais_MapScripts::
	.byte 0

@ Eryon: the first foothills beyond the eastern trail.
EryonSerra_EventScript_Geologist::
	lock
	faceplayer
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
