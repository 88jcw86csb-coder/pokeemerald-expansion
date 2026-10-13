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
	goto_if_set FLAG_BADGE03_GET, EryonFrostheim_EventScript_GymAfter
	goto_if_unset FLAG_BADGE02_GET, EryonFrostheim_EventScript_GymNotReady
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonFrostheim_EventScript_GymOffer
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

@ Tactical badge battle — Frostheim: ace level 31, badge 3.
EryonFrostheim_EventScript_GymOffer::
	msgbox EryonFrostheim_Text_GymOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonFrostheim_EventScript_GymDecline
	closemessage
	trainerbattle_single TRAINER_ERYON_GYM_FROSTHEIM, EryonFrostheim_Text_GymIntro, EryonFrostheim_Text_GymLoss, EryonFrostheim_EventScript_GymVictory, FALSE
	msgbox EryonFrostheim_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonFrostheim_EventScript_GymVictory::
	message EryonFrostheim_Text_GymBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	setflag FLAG_BADGE03_GET
	msgbox EryonFrostheim_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonFrostheim_EventScript_GymDecline::
	closemessage
	release
	end

EryonFrostheim_EventScript_GymNotReady::
	msgbox EryonFrostheim_Text_GymNotReady, MSGBOX_DEFAULT
	release
	end

EryonFrostheim_EventScript_GymAfter::
	msgbox EryonFrostheim_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonFrostheim_Text_GymOffer:
	.string "BJORN: Meu GINASIO\n"
	.string "treina com gelo.\p"
	.string "Desafiar meu time\n"
	.string "de Pokemon agora?$"

EryonFrostheim_Text_GymIntro:
	.string "BJORN: Mostre sua\n"
	.string "forca e estrategia!$"

EryonFrostheim_Text_GymLoss:
	.string "BJORN: Voce encontrou\n"
	.string "uma boa resposta!$"

EryonFrostheim_Text_GymBadge:
	.string "Venceu o 3o GINASIO!\p"
	.string "Recebeu a INSIGNIA\n"
	.string "de numero 3!$"

EryonFrostheim_Text_GymAfter:
	.string "BJORN: Bela vitoria!\p"
	.string "Proteja os cristais da serra.$"

EryonFrostheim_Text_GymNotReady:
	.string "BJORN: Primeiro,\n"
	.string "conquiste a INSIGNIA\n"
	.string "do GINASIO anterior.$"
