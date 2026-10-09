Eryon_TrilhaGlacial_MapScripts::
	.byte 0

@ First hint of Team Eclipse activity in the northern pass.
EryonTrilhaGlacial_EventScript_Hiker::
	lock
	faceplayer
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
