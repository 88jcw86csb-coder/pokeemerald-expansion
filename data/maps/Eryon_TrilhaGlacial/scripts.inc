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

@ Optional route encounter: an Eclipse agent surveys anomalous ice.
@ Story setup only; the full battle and quest flag are not yet installed.
EryonTrilhaGlacial_EventScript_EclipseResearcher::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonTrilhaGlacial_EventScript_EclipseResearcherExposed
	msgbox EryonTrilhaGlacial_Text_EclipseResearcher, MSGBOX_DEFAULT
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
