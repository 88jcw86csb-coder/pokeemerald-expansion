Eryon_Arkhara_MapScripts::
	.byte 0

EryonArkhara_EventScript_Medic::
	lock
	faceplayer
	msgbox EryonArkhara_Text_Medic, MSGBOX_DEFAULT
	special HealPlayerParty
	release
	end

EryonArkhara_EventScript_GymSteward::
	lock
	faceplayer
	msgbox EryonArkhara_Text_GymSteward, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_Tessa::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_ARKHARA_RELAY_READ, EryonArkhara_EventScript_TessaInformed
	msgbox EryonArkhara_Text_TessaBefore, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_TessaInformed::
	msgbox EryonArkhara_Text_TessaInformed, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_Geologist::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_ARKHARA_RELAY_READ, EryonArkhara_EventScript_GeologistInformed
	msgbox EryonArkhara_Text_GeologistBefore, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_GeologistInformed::
	msgbox EryonArkhara_Text_GeologistInformed, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_EclipseCourier::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_ARKHARA_RELAY_READ, EryonArkhara_EventScript_CourierExposed
	msgbox EryonArkhara_Text_CourierBefore, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_CourierExposed::
	msgbox EryonArkhara_Text_CourierExposed, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_RelayNotes::
	lock
	goto_if_set FLAG_ERYON_ARKHARA_RELAY_READ, EryonArkhara_EventScript_RelayKnown
	msgbox EryonArkhara_Text_RelayBefore, MSGBOX_DEFAULT
	setflag FLAG_ERYON_ARKHARA_RELAY_READ
	msgbox EryonArkhara_Text_RelayDiscovery, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_RelayKnown::
	msgbox EryonArkhara_Text_RelayKnown, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_CitySign::
	lock
	msgbox EryonArkhara_Text_CitySign, MSGBOX_DEFAULT
	release
	end

EryonArkhara_Text_Medic:
	.string "SOCORRISTA: Descanse!\p"
	.string "Vou curar seus Pokemon.$"

EryonArkhara_Text_GymSteward:
	.string "GUIA: O quarto GINASIO\n"
	.string "pertence a TESSA.\p"
	.string "Ela treina tipo PEDRA;\n"
	.string "seu principal e ARMALDO.$"

EryonArkhara_Text_TessaBefore:
	.string "TESSA: Protejo as\n"
	.string "rochas desta cidade.\p"
	.string "Um sinal desconhecido\n"
	.string "abala a montanha.$"

EryonArkhara_Text_TessaInformed:
	.string "TESSA: As provas ligam\n"
	.string "a ECLIPSE a ARKHARA!\p"
	.string "Meu desafio oficial\n"
	.string "ainda nao esta pronto.$"

EryonArkhara_Text_GeologistBefore:
	.string "GEOLOGO: Ha cabos\n"
	.string "escondidos na praca.\p"
	.string "Precisamos descobrir\n"
	.string "quem os instalou.$"

EryonArkhara_Text_GeologistInformed:
	.string "GEOLOGO: A ECLIPSE\n"
	.string "usa rochas como antenas.\p"
	.string "Os fios seguem para\n"
	.string "o VALE DOS VENTOS.$"

EryonArkhara_Text_CourierBefore:
	.string "MENSAGEIRO: Levo pecas\n"
	.string "pela estrada leste.\p"
	.string "Nao abra as caixas.$"

EryonArkhara_Text_CourierExposed:
	.string "ECLIPSE: Encontrou\n"
	.string "nosso registro!\p"
	.string "O transporte agora\n"
	.string "segue para UMBRA.$"

EryonArkhara_Text_RelayBefore:
	.string "Um mapa de cabos\n"
	.string "esta preso na praca.\p"
	.string "Ha marcas da ECLIPSE\n"
	.string "junto as rotas.$"

EryonArkhara_Text_RelayDiscovery:
	.string "Voce registrou a rota\n"
	.string "da rede clandestina!\p"
	.string "Os fios seguem rumo\n"
	.string "ao VALE DOS VENTOS.$"

EryonArkhara_Text_RelayKnown:
	.string "Voce ja anotou\n"
	.string "o esquema da ECLIPSE.$"

EryonArkhara_Text_CitySign:
	.string "ARKHARA: CIDADE PEDRA.\n"
	.string "OESTE: PASSAGEM ROCHOSA.\p"
	.string "LESTE: ESTRADA ORIENTAL.\n"
	.string "Nao e preciso HM.$"
