Eryon_TrilhaGlacial_MapScripts::
	.byte 0

@ First hint of Team Eclipse activity in the northern pass.
EryonTrilhaGlacial_EventScript_Hiker::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_GLACIAL_BERGMITE_RESOLVED, EryonTrilhaGlacial_EventScript_HikerGrottoSafe
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

@ The northern Ice Rift uses existing rock trail and never gates Frostheim.
EryonTrilhaGlacial_EventScript_IceRiftJournal::
	lock
	goto_if_set FLAG_ERYON_GLACIAL_RIFT_LOG_READ, EryonTrilhaGlacial_EventScript_IceRiftJournalRepeat
	goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN, EryonTrilhaGlacial_EventScript_IceRiftJournalPeace
	goto_if_set FLAG_ERYON_GLACIAL_ECLIPSE_RESEARCHER_DEFEATED, EryonTrilhaGlacial_EventScript_IceRiftJournalVictory
	msgbox EryonTrilhaGlacial_Text_IceRiftJournal, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GLACIAL_RIFT_LOG_READ
	release
	end

EryonTrilhaGlacial_EventScript_IceRiftJournalVictory::
	msgbox EryonTrilhaGlacial_Text_IceRiftJournalVictory, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GLACIAL_RIFT_LOG_READ
	release
	end

EryonTrilhaGlacial_EventScript_IceRiftJournalPeace::
	msgbox EryonTrilhaGlacial_Text_IceRiftJournalPeace, MSGBOX_DEFAULT
	setflag FLAG_ERYON_GLACIAL_RIFT_LOG_READ
	release
	end

EryonTrilhaGlacial_EventScript_IceRiftJournalRepeat::
	goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN, EryonTrilhaGlacial_EventScript_IceRiftJournalQuiet
	msgbox EryonTrilhaGlacial_Text_IceRiftJournalRepeat, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_EventScript_IceRiftJournalQuiet::
	msgbox EryonTrilhaGlacial_Text_IceRiftJournalQuiet, MSGBOX_DEFAULT
	release
	end

@ Standard catchable Kalos Bergmite; flee/decline do not consume event.
EryonTrilhaGlacial_EventScript_BergmiteNest::
	lock
	goto_if_set FLAG_ERYON_GLACIAL_BERGMITE_RESOLVED, EryonTrilhaGlacial_EventScript_BergmiteCalm
	goto_if_unset FLAG_ERYON_GLACIAL_RIFT_LOG_READ, EryonTrilhaGlacial_EventScript_BergmiteHidden
	msgbox EryonTrilhaGlacial_Text_BergmiteOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonTrilhaGlacial_EventScript_BergmiteDecline
	closemessage
	setwildbattle SPECIES_BERGMITE, 29
	waitse
	playmoncry SPECIES_BERGMITE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, EryonTrilhaGlacial_EventScript_BergmiteResolved
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, EryonTrilhaGlacial_EventScript_BergmiteResolved
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, EryonTrilhaGlacial_EventScript_BergmiteEscaped
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, EryonTrilhaGlacial_EventScript_BergmiteEscaped
	release
	end

EryonTrilhaGlacial_EventScript_BergmiteResolved::
	setflag FLAG_ERYON_GLACIAL_BERGMITE_RESOLVED
	msgbox EryonTrilhaGlacial_Text_BergmiteResolved, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_EventScript_BergmiteHidden::
	msgbox EryonTrilhaGlacial_Text_BergmiteHidden, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_EventScript_BergmiteEscaped::
	msgbox EryonTrilhaGlacial_Text_BergmiteEscaped, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_EventScript_BergmiteCalm::
	msgbox EryonTrilhaGlacial_Text_BergmiteCalm, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_EventScript_BergmiteDecline::
	closemessage
	release
	end

@ Reward remains retriable when the Bag is full.
EryonTrilhaGlacial_EventScript_RiftSupplies::
	lock
	goto_if_set FLAG_ERYON_GLACIAL_RIFT_SUPPLIES_TAKEN, EryonTrilhaGlacial_EventScript_RiftSuppliesEmpty
	goto_if_unset FLAG_ERYON_GLACIAL_BERGMITE_RESOLVED, EryonTrilhaGlacial_EventScript_RiftSuppliesLocked
	msgbox EryonTrilhaGlacial_Text_RiftSuppliesFound, MSGBOX_DEFAULT
	giveitem ITEM_REVIVE
	goto_if_eq VAR_RESULT, FALSE, EryonTrilhaGlacial_EventScript_RiftSuppliesFull
	setflag FLAG_ERYON_GLACIAL_RIFT_SUPPLIES_TAKEN
	release
	end

EryonTrilhaGlacial_EventScript_RiftSuppliesLocked::
	msgbox EryonTrilhaGlacial_Text_RiftSuppliesLocked, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_EventScript_RiftSuppliesFull::
	msgbox EryonTrilhaGlacial_Text_RiftSuppliesFull, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_EventScript_RiftSuppliesEmpty::
	msgbox EryonTrilhaGlacial_Text_RiftSuppliesEmpty, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_EventScript_HikerGrottoSafe::
	msgbox EryonTrilhaGlacial_Text_HikerGrottoSafe, MSGBOX_DEFAULT
	release
	end

EryonTrilhaGlacial_Text_IceRiftJournal:
	.string "DIARIO GLACIAL:\p"
	.string "A ECLIPSE estudou\n"
	.string "a fenda gelada.\p"
	.string "Um Pokemon ficou\n"
	.string "preso na encosta.$"

EryonTrilhaGlacial_Text_IceRiftJournalVictory:
	.string "DIARIO GLACIAL:\p"
	.string "O tecnico ECLIPSE\n"
	.string "abandonou a fenda.\p"
	.string "Resta recuperar\n"
	.string "a fauna do gelo.$"

EryonTrilhaGlacial_Text_IceRiftJournalPeace:
	.string "DIARIO GLACIAL:\p"
	.string "REDE ECLIPSE INATIVA!\p"
	.string "O gelo recupera\n"
	.string "a energia natural.$"

EryonTrilhaGlacial_Text_IceRiftJournalRepeat:
	.string "Os registros marcam\n"
	.string "um BERGMITE na fenda.\p"
	.string "A vida da montanha\n"
	.string "ainda precisa de ajuda.$"

EryonTrilhaGlacial_Text_IceRiftJournalQuiet:
	.string "O diario confirma\n"
	.string "o fim da ECLIPSE.\p"
	.string "Os sinais naturais\n"
	.string "voltaram as montanhas.$"

EryonTrilhaGlacial_Text_BergmiteHidden:
	.string "Um bloco de gelo\n"
	.string "se move de leve.\p"
	.string "Leia o DIARIO GLACIAL\n"
	.string "primeiro.$"

EryonTrilhaGlacial_Text_BergmiteOffer:
	.string "Um BERGMITE aparece\n"
	.string "perto dos cristais!\p"
	.string "Investigar agora?$"

EryonTrilhaGlacial_Text_BergmiteResolved:
	.string "BERGMITE se acalmou!\p"
	.string "A fenda pode respirar\n"
	.string "novamente.$"

EryonTrilhaGlacial_Text_BergmiteEscaped:
	.string "BERGMITE deslizou\n"
	.string "para a neve profunda.\p"
	.string "Pode retornar depois.$"

EryonTrilhaGlacial_Text_BergmiteCalm:
	.string "A fenda gelada\n"
	.string "esta tranquila.$"

EryonTrilhaGlacial_Text_RiftSuppliesLocked:
	.string "Uma caixa de gelo\n"
	.string "esta protegida.\p"
	.string "BERGMITE vigia\n"
	.string "estes suprimentos.$"

EryonTrilhaGlacial_Text_RiftSuppliesFound:
	.string "CAIXA GLACIAL:\p"
	.string "Um REVIVE foi deixado\n"
	.string "para emergencias.$"

EryonTrilhaGlacial_Text_RiftSuppliesFull:
	.string "Sua BOLSA esta cheia!\p"
	.string "O item ficara aqui\n"
	.string "para sua volta.$"

EryonTrilhaGlacial_Text_RiftSuppliesEmpty:
	.string "A caixa de gelo\n"
	.string "ja esta vazia.$"

EryonTrilhaGlacial_Text_HikerGrottoSafe:
	.string "GUIA: A fenda gelada\n"
	.string "esta segura agora!\p"
	.string "FROSTHEIM agradece\n"
	.string "por sua ajuda.$"
