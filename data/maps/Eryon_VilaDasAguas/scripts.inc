Eryon_VilaDasAguas_MapScripts::
	.byte 0

@ River pollution links the village to Eclipse's stolen crystal cargo.
EryonAguas_EventScript_Fisher::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonAguas_EventScript_FisherClue
	msgbox EryonAguas_Text_FisherBefore, MSGBOX_DEFAULT
	release
	end

EryonAguas_EventScript_FisherClue::
	msgbox EryonAguas_Text_FisherClue, MSGBOX_DEFAULT
	release
	end

EryonAguas_EventScript_Healer::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonAguas_EventScript_HealerClue
	msgbox EryonAguas_Text_HealerBefore, MSGBOX_DEFAULT
	release
	end

EryonAguas_EventScript_HealerClue::
	msgbox EryonAguas_Text_HealerClue, MSGBOX_DEFAULT
	release
	end

EryonAguas_EventScript_WaterNotice::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonAguas_EventScript_WaterNoticeClue
	msgbox EryonAguas_Text_WaterNoticeBefore, MSGBOX_DEFAULT
	release
	end

EryonAguas_EventScript_WaterNoticeClue::
	msgbox EryonAguas_Text_WaterNoticeClue, MSGBOX_DEFAULT
	release
	end

EryonAguas_Text_FisherBefore:
	.string "PESCADOR: O rio esta\n"
	.string "estranho desde ontem.\p"
	.string "Os peixes sumiram perto\n"
	.string "da grande cachoeira.$"

EryonAguas_Text_FisherClue:
	.string "PESCADOR: Cristais da\n"
	.string "ECLIPSE cairam no rio?\p"
	.string "Vi uma barcaca seguir\n"
	.string "para o sul, ao oasis.$"

EryonAguas_Text_HealerBefore:
	.string "MORADORA: A agua anda\n"
	.string "turva perto das pedras.\p"
	.string "Pedimos que os viajantes\n"
	.string "evitem beber do rio.$"

EryonAguas_Text_HealerClue:
	.string "MORADORA: O brilho na\n"
	.string "agua nao e natural.\p"
	.string "Os cristais podem estar\n"
	.string "afetando os Pokemon.$"

EryonAguas_Text_WaterNoticeBefore:
	.string "AVISO: Acesso ao rio\n"
	.string "sob observacao.\p"
	.string "A vila esta analisando\n"
	.string "a qualidade da agua.$"

EryonAguas_Text_WaterNoticeClue:
	.string "AVISO: Residuos de\n"
	.string "cristal foram encontrados.\p"
	.string "Investigue a rota que\n"
	.string "leva ao oasis.$"
