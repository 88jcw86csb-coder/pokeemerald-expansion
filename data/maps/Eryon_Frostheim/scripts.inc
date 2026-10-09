Eryon_Frostheim_MapScripts::
	.byte 0

@ Frostheim connects the route's mystery to the third gym.
EryonFrostheim_EventScript_Researcher::
	lock
	faceplayer
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
