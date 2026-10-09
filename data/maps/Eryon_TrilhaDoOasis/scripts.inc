Eryon_TrilhaDoOasis_MapScripts::
	.byte 0

@ The cargo trail leaves the river and heads toward the Solaris desert.
EryonOasis_EventScript_Guide::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonOasis_EventScript_GuideClue
	msgbox EryonOasis_Text_GuideBefore, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_GuideClue::
	msgbox EryonOasis_Text_GuideClue, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_EclipseCarrier::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonOasis_EventScript_EclipseCarrierClue
	msgbox EryonOasis_Text_CarrierBefore, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_EclipseCarrierClue::
	msgbox EryonOasis_Text_CarrierClue, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_DryCanister::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonOasis_EventScript_DryCanisterClue
	msgbox EryonOasis_Text_CanisterBefore, MSGBOX_DEFAULT
	release
	end

EryonOasis_EventScript_DryCanisterClue::
	msgbox EryonOasis_Text_CanisterClue, MSGBOX_DEFAULT
	release
	end

EryonOasis_Text_GuideBefore:
	.string "GUIA: Esta trilha liga\n"
	.string "o rio ao deserto.\p"
	.string "Leve agua e procure\n"
	.string "abrigo nas palmeiras.$"

EryonOasis_Text_GuideClue:
	.string "GUIA: Uma caravana\n"
	.string "trouxe caixas de Umbra.\p"
	.string "Seguiram para Solaris\n"
	.string "antes do amanhecer.$"

EryonOasis_Text_CarrierBefore:
	.string "VIAJANTE: Transporto\n"
	.string "mantimentos ao deserto.\p"
	.string "Nao tenho tempo para\n"
	.string "conversas.$"

EryonOasis_Text_CarrierClue:
	.string "ECLIPSE: Os cristais\n"
	.string "ja estao em Solaris!\p"
	.string "Nosso plano nao pode\n"
	.string "ser interrompido.$"

EryonOasis_Text_CanisterBefore:
	.string "Um recipiente vazio\n"
	.string "esta entre as pedras.\p"
	.string "O rotulo foi removido.$"

EryonOasis_Text_CanisterClue:
	.string "O recipiente contem\n"
	.string "po azul cristalino.\p"
	.string "Um selo da ECLIPSE\n"
	.string "aponta para Solaris.$"
