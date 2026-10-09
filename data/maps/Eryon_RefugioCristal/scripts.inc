Eryon_RefugioCristal_MapScripts::
	.byte 0

@ Caretaker changes his account when the Eclipse camp clue has been found.
EryonRefugioCristal_EventScript_Caretaker::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonRefugioCristal_EventScript_CaretakerAfterClue
	msgbox EryonRefugioCristal_Text_CaretakerBefore, MSGBOX_DEFAULT
	release
	end

EryonRefugioCristal_EventScript_CaretakerAfterClue::
	msgbox EryonRefugioCristal_Text_CaretakerAfterClue, MSGBOX_DEFAULT
	release
	end

EryonRefugioCristal_Text_CaretakerBefore:
	.string "GUARDIAO: Bem-vindo ao\n"
	.string "Refugio Cristal.\p"
	.string "As trilhas estao cheias\n"
	.string "de marcas recentes.\p"
	.string "Procure pistas na serra\n"
	.string "antes de seguir viagem.$"

EryonRefugioCristal_Text_CaretakerAfterClue:
	.string "GUARDIAO: Encontrou o\n"
	.string "acampamento da ECLIPSE?\p"
	.string "As caixas seguiam rumo\n"
	.string "a Passagem Rochosa.\p"
	.string "Alguem busca a energia\n"
	.string "que dorme nos cristais.$"
