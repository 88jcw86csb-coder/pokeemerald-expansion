Eryon_CidadeDaLiga_MapScripts::
	.byte 0

EryonCidadeLiga_EventScript_Medic::
	lock
	faceplayer
	msgbox EryonCidadeLiga_Text_Medic, MSGBOX_DEFAULT
	special HealPlayerParty
	release
	end

EryonCidadeLiga_EventScript_Guide::
	lock
	faceplayer
	msgbox EryonCidadeLiga_Text_Guide, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_Fan::
	lock
	faceplayer
	msgbox EryonCidadeLiga_Text_Fan, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_PlazaSign::
	lock
	msgbox EryonCidadeLiga_Text_CitySign, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_Notice::
	lock
	msgbox EryonCidadeLiga_Text_Notice, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_Text_Medic:
	.string "SOCORRISTA: Bem-vindo\n"
	.string "a CIDADE DA LIGA!\p"
	.string "Vou restaurar sua\n"
	.string "equipe Pokemon.$"

EryonCidadeLiga_Text_Guide:
	.string "GUIA: O grande edificio\n"
	.string "fica no CENTRO da cidade.\p"
	.string "Primeiro, oito batalhas\n"
	.string "da CLASSIFICATORIA.$"

EryonCidadeLiga_Text_Fan:
	.string "TORCEDORA: Uma derrota\n"
	.string "zera sua sequencia.\p"
	.string "Guarde dinheiro antes\n"
	.string "de entrar na arena!$"

EryonCidadeLiga_Text_CitySign:
	.string "CIDADE DA LIGA DE ERYON.\n"
	.string "PRACA DA COMPETICAO.\p"
	.string "O edificio da LIGA\n"
	.string "fica nesta praca.$"

EryonCidadeLiga_Text_Notice:
	.string "TORNEIO DA LIGA:\n"
	.string "8 duelos consecutivos.\p"
	.string "Venca, cure sua equipe\n"
	.string "e siga para a ELITE 4.$"
