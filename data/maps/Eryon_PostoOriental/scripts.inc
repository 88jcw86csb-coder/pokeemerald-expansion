Eryon_PostoOriental_MapScripts::
	.byte 0

@ Cargo mystery progresses from Crystal Ridge through Rocky Passage to this outpost.
EryonPostoOriental_EventScript_Quartermaster::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPostoOriental_EventScript_QuartermasterClue
	msgbox EryonPostoOriental_Text_QuartermasterBefore, MSGBOX_DEFAULT
	release
	end

EryonPostoOriental_EventScript_QuartermasterClue::
	msgbox EryonPostoOriental_Text_QuartermasterClue, MSGBOX_DEFAULT
	release
	end

EryonPostoOriental_EventScript_Merchant::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonPostoOriental_EventScript_MerchantClue
	msgbox EryonPostoOriental_Text_MerchantBefore, MSGBOX_DEFAULT
	release
	end

EryonPostoOriental_EventScript_MerchantClue::
	msgbox EryonPostoOriental_Text_MerchantClue, MSGBOX_DEFAULT
	release
	end

EryonPostoOriental_Text_QuartermasterBefore:
	.string "CHEFE: Este posto recebe\n"
	.string "caravanas da serra.\p"
	.string "Uma carga misteriosa\n"
	.string "passou durante a noite.$"

EryonPostoOriental_Text_QuartermasterClue:
	.string "CHEFE: Voce viu as caixas\n"
	.string "da EQUIPE ECLIPSE?\p"
	.string "O registro foi falsificado.\n"
	.string "Seguiram para o vale.$"

EryonPostoOriental_Text_MerchantBefore:
	.string "MERCADORA: Viajantes\n"
	.string "descansam aqui antes do vale.\p"
	.string "Ouvi carrocas ao amanhecer.$"

EryonPostoOriental_Text_MerchantClue:
	.string "MERCADORA: Os cristais\n"
	.string "brilhavam dentro das caixas.\p"
	.string "A ECLIPSE pagou para\n"
	.string "nao fazermos perguntas.$"
