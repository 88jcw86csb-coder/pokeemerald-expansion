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

@ Bjorn appears in the plaza before his Gym interior is built.
@ Dialogue responds to the existing Serra investigation flag.
EryonFrostheim_EventScript_Bjorn::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonFrostheim_EventScript_BjornAfterClue
	msgbox EryonFrostheim_Text_BjornBefore, MSGBOX_DEFAULT
	release
	end

EryonFrostheim_EventScript_BjornAfterClue::
	msgbox EryonFrostheim_Text_BjornAfter, MSGBOX_DEFAULT
	release
	end

EryonFrostheim_Text_BjornBefore:
	.string "BJORN: Sou o lider do\n"
	.string "GINASIO de Frostheim.\p"
	.string "A ECLIPSE roubou amostras\n"
	.string "das montanhas geladas.\p"
	.string "Investigue a Serra dos\n"
	.string "Cristais e volte aqui.$"

EryonFrostheim_Text_BjornAfter:
	.string "BJORN: Encontrou o campo\n"
	.string "abandonado da ECLIPSE?\p"
	.string "O gelo e os cristais\n"
	.string "reagem a mesma energia.\p"
	.string "Seu desafio no GINASIO\n"
	.string "sera nosso proximo passo.$"
