@ Eryon: narrow trail after the crystal highlands.
EryonPassagem_EventScript_Guard::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPassagem_EventScript_GuardClue
	msgbox EryonPassagem_Text_GuardBefore, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_GuardClue::
	msgbox EryonPassagem_Text_GuardClue, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_Traveler::
	lock
	faceplayer
	msgbox EryonPassagem_Text_Traveler, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_CrystalMark::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPassagem_EventScript_CrystalMarkClue
	msgbox EryonPassagem_Text_CrystalMarkBefore, MSGBOX_DEFAULT
	release
	end

EryonPassagem_EventScript_CrystalMarkClue::
	msgbox EryonPassagem_Text_CrystalMarkClue, MSGBOX_DEFAULT
	release
	end

EryonPassagem_Text_GuardBefore:
	.string "GUARDA: Os trilhos de pedra\n"
	.string "levam a um velho desfiladeiro.\p"
	.string "Cuidado com o terreno.$"

EryonPassagem_Text_GuardClue:
	.string "GUARDA: Voce viu o simbolo\n"
	.string "do eclipse na serra?\p"
	.string "Carrocas seguiram por aqui\n"
	.string "antes do amanhecer.$"

EryonPassagem_Text_Traveler:
	.string "VIAJANTE: As montanhas\n"
	.string "escondem caminhos antigos.\p"
	.string "Ainda falta muito ate a\n"
	.string "proxima cidade.$"

EryonPassagem_Text_CrystalMarkBefore:
	.string "Ha sulcos fundos na pedra.\p"
	.string "Talvez sejam marcas de rodas.$"

EryonPassagem_Text_CrystalMarkClue:
	.string "Os sulcos combinam com as\n"
	.string "rodas vistas na serra.\p"
	.string "A carga seguiu para leste.$"
