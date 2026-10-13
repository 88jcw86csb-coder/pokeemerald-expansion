Eryon_TrilhaGlacial_MapScripts::
	.byte 0

@ First hint of Team Eclipse activity in the northern pass.
EryonTrilhaGlacial_EventScript_Hiker::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_MIST_SIGNAL_REPAIRED, EryonTrilhaGlacial_EventScript_HikerAfterSignal
	msgbox EryonTrilhaGlacial_Text_Hiker, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_Text_Hiker:
	.string "GUIA: Cuidado com o gelo!\n"
	.string "A trilha leva a Frostheim.\p"
	.string "Vi pessoas com um simbolo\n"
	.string "de eclipse nas montanhas.$"

@ Optional battle as the story advances from Neonara toward Frostheim.
@ Level 27-29 opponents provide trainer experience before the level-31 Gym.
EryonTrilhaGlacial_EventScript_EclipseResearcher::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_GLACIAL_ECLIPSE_RESEARCHER_DEFEATED, EryonTrilhaGlacial_EventScript_ResearcherAfterBattle
	goto_if_set FLAG_BADGE02_GET, EryonTrilhaGlacial_EventScript_ResearcherBattleOffer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonTrilhaGlacial_EventScript_EclipseResearcherExposed
	msgbox EryonTrilhaGlacial_Text_EclipseResearcher, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_EventScript_ResearcherBattleOffer::
	msgbox EryonTrilhaGlacial_Text_ResearcherBattleOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonTrilhaGlacial_EventScript_ResearcherDecline
	closemessage
	trainerbattle_single TRAINER_ERYON_GLACIAL_ECLIPSE_RESEARCHER, EryonTrilhaGlacial_Text_ResearcherIntro, EryonTrilhaGlacial_Text_ResearcherLoss, EryonTrilhaGlacial_EventScript_ResearcherVictory, FALSE
	msgbox EryonTrilhaGlacial_Text_ResearcherAfter, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_EventScript_ResearcherVictory::
	msgbox EryonTrilhaGlacial_Text_ResearcherVictory, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_EventScript_ResearcherDecline::
	closemessage
	release
	end

EryonTrilhaGlacial_EventScript_ResearcherAfterBattle::
	msgbox EryonTrilhaGlacial_Text_ResearcherAfter, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_Text_EclipseResearcher:
	.string "PESQUISADOR: O gelo guarda\n"
	.string "energia de muitos seculos.\p"
	.string "A EQUIPE ECLIPSE vai\n"
	.string "desvendar esse segredo.\p"
	.string "Voce nao deveria estar\n"
	.string "investigando esta area.$"

@ The same NPC reacts to the clue obtained from the abandoned Crystal Ridge camp.
EryonTrilhaGlacial_EventScript_EclipseResearcherExposed::
	msgbox EryonTrilhaGlacial_Text_EclipseResearcherExposed, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_Text_EclipseResearcherExposed:
	.string "PESQUISADOR: Voce viu\n"
	.string "nossas caixas na serra?\p"
	.string "Nao conte a Frostheim\n"
	.string "sobre os cristais!$"


@ New upper pass: recovering the mountain emergency kit after repairing
@ the nearby mist radio. The player can visit with a full bag and retry.
EryonTrilhaGlacial_EventScript_ResearchSupplies::
	lock
	goto_if_set FLAG_ERYON_GLACIAL_SUPPLY_RETRIEVED, EryonTrilhaGlacial_EventScript_SuppliesEmpty
	goto_if_unset FLAG_ERYON_MIST_SIGNAL_REPAIRED, EryonTrilhaGlacial_EventScript_SuppliesSealed
	msgbox EryonTrilhaGlacial_Text_SuppliesFound, MSGBOX_DEFAULT
	giveitem ITEM_SUPER_POTION
	goto_if_eq VAR_RESULT, FALSE, EryonTrilhaGlacial_EventScript_SuppliesFull
	setflag FLAG_ERYON_GLACIAL_SUPPLY_RETRIEVED
	release
	end

EryonTrilhaGlacial_EventScript_SuppliesEmpty::
	msgbox EryonTrilhaGlacial_Text_SuppliesEmpty, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_EventScript_SuppliesSealed::
	msgbox EryonTrilhaGlacial_Text_SuppliesSealed, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_EventScript_SuppliesFull::
	msgbox EryonTrilhaGlacial_Text_SuppliesFull, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_EventScript_HikerAfterSignal::
	msgbox EryonTrilhaGlacial_Text_HikerAfterSignal, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_Text_SuppliesSealed:
	.string "ESTOJO DE PESQUISA:\p"
	.string "Acesso bloqueado ate\n"
	.string "restaurar o observatorio\n"
	.string "nas COLINAS DA NEBLINA.$"

EryonTrilhaGlacial_Text_SuppliesFound:
	.string "O repetidor confirma\n"
	.string "sua identidade!\p"
	.string "Ha uma SUPER POTION\n"
	.string "para a viagem.$"

EryonTrilhaGlacial_Text_SuppliesEmpty:
	.string "O estojo ja foi\n"
	.string "recolhido pelo treinador.$"

EryonTrilhaGlacial_Text_SuppliesFull:
	.string "Sua BOLSA esta cheia.\p"
	.string "O estojo permanece\n"
	.string "aqui para depois.$"

EryonTrilhaGlacial_Text_HikerAfterSignal:
	.string "GUIA: O observatorio\n"
	.string "de NEONARA esta ativo!\p"
	.string "O posto no alto da\n"
	.string "trilha guarda remedios.\p"
	.string "A ECLIPSE ja nao pode\n"
	.string "se esconder no sinal.$"


@ Hidden lab cache on the new upper route. Open after the optional battle;
@ a full bag preserves the reward and never blocks access to Frostheim.
EryonTrilhaGlacial_EventScript_EclipseIceSample::
	lock
	goto_if_set FLAG_ERYON_GLACIAL_ECLIPSE_SAMPLE_TAKEN, EryonTrilhaGlacial_EventScript_IceSampleEmpty
	goto_if_unset FLAG_ERYON_GLACIAL_ECLIPSE_RESEARCHER_DEFEATED, EryonTrilhaGlacial_EventScript_IceSampleSealed
	msgbox EryonTrilhaGlacial_Text_IceSampleFound, MSGBOX_DEFAULT
	giveitem ITEM_NEVER_MELT_ICE
	goto_if_eq VAR_RESULT, FALSE, EryonTrilhaGlacial_EventScript_IceSampleFull
	setflag FLAG_ERYON_GLACIAL_ECLIPSE_SAMPLE_TAKEN
	release
	end

EryonTrilhaGlacial_EventScript_IceSampleSealed::
	msgbox EryonTrilhaGlacial_Text_IceSampleSealed, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_EventScript_IceSampleFull::
	msgbox EryonTrilhaGlacial_Text_IceSampleFull, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_EventScript_IceSampleEmpty::
	msgbox EryonTrilhaGlacial_Text_IceSampleEmpty, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_Text_ResearcherBattleOffer:
	.string "ECLIPSE: A INSIGNIA de\n"
	.string "NEONARA lhe deu coragem?\p"
	.string "Quer enfrentar minha\n"
	.string "equipe no gelo?$"

EryonTrilhaGlacial_Text_ResearcherIntro:
	.string "ECLIPSE: Nossos estudos\n"
	.string "nao serao interrompidos!$"

EryonTrilhaGlacial_Text_ResearcherLoss:
	.string "ECLIPSE: A equipe\n"
	.string "perdeu o controle do gelo!$"

EryonTrilhaGlacial_Text_ResearcherVictory:
	.string "ECLIPSE: Voce venceu!\p"
	.string "Abandonamos amostras\n"
	.string "na encosta ao norte.\p"
	.string "Mas nossa pesquisa\n"
	.string "ainda nao acabou.$"

EryonTrilhaGlacial_Text_ResearcherAfter:
	.string "ECLIPSE: Recuamos\n"
	.string "para as montanhas.\p"
	.string "As amostras ficaram\n"
	.string "na encosta ao norte.$"

EryonTrilhaGlacial_Text_IceSampleFound:
	.string "Um laboratorio abandonado\n"
	.string "contem NEVER-MELT ICE!\p"
	.string "Pode fortalecer\n"
	.string "ataques de gelo.$"

EryonTrilhaGlacial_Text_IceSampleSealed:
	.string "Caixas marcadas com\n"
	.string "o simbolo ECLIPSE.\p"
	.string "A equipe ainda vigia\n"
	.string "os materiais.$"

EryonTrilhaGlacial_Text_IceSampleFull:
	.string "Sua BOLSA esta cheia!\p"
	.string "A amostra pode ser\n"
	.string "recolhida depois.$"

EryonTrilhaGlacial_Text_IceSampleEmpty:
	.string "As caixas estao vazias.\p"
	.string "A amostra foi recolhida.$"
