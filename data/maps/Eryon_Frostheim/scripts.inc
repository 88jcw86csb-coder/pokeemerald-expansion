Eryon_Frostheim_MapScripts::
	.byte 0

@ Frostheim connects the route's mystery to the third gym.
EryonFrostheim_EventScript_Researcher::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonFrostheim_EventScript_ResearcherAfterClue
	msgbox EryonFrostheim_Text_Researcher, MSGBOX_DEFAULT
	release
	end

EryonFrostheim_Text_Researcher:
	.string "CIENTISTA: O gelo das\n"
	.string "montanhas esta mudando.\p"
	.string "A EQUIPE ECLIPSE levou\n"
	.string "amostras sem permissao.\p"
	.string "Bjorn, lider do GINASIO,\n"
	.string "investiga os incidentes.$"

@ Returning from the Crystal Ridge investigation changes the scientist's report.
EryonFrostheim_EventScript_ResearcherAfterClue::
	msgbox EryonFrostheim_Text_ResearcherAfterClue, MSGBOX_DEFAULT
	release
	end

EryonFrostheim_Text_ResearcherAfterClue:
	.string "CIENTISTA: Voce encontrou\n"
	.string "o acampamento da ECLIPSE!\p"
	.string "Os cristais da serra e\n"
	.string "o gelo tem a mesma energia.\p"
	.string "Bjorn precisa saber disso.$"
