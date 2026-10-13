Eryon_LigaRecuperacao_MapScripts::
	.byte 0

EryonLigaRecover_EventScript_Heal::
	lock
	faceplayer
	goto_if_unset FLAG_ERYON_QUALIFIED, EryonLigaRecover_EventScript_NotQualified
	msgbox EryonLigaRecover_Text_Heal, MSGBOX_DEFAULT
	special HealPlayerParty
	release
	end

EryonLigaRecover_EventScript_Official::
	lock
	faceplayer
	goto_if_unset FLAG_ERYON_QUALIFIED, EryonLigaRecover_EventScript_NotQualified
	msgbox EryonLigaRecover_Text_Official, MSGBOX_DEFAULT
	release
	end

EryonLigaRecover_EventScript_ReturnLobby::
	lock
	msgbox EryonLigaRecover_Text_ReturnLobby, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonLigaRecover_EventScript_Stay
	closemessage
	warp MAP_ERYON_LIGA_RECEPCAO, 12, 12
	waitstate
	end

EryonLigaRecover_EventScript_Stay::
	release
	end

EryonLigaRecover_EventScript_EliteGate::
	lock
	goto_if_unset FLAG_ERYON_QUALIFIED, EryonLigaRecover_EventScript_NotQualified
	msgbox EryonLigaRecover_Text_EliteGate, MSGBOX_DEFAULT
	release
	end

EryonLigaRecover_EventScript_NotQualified::
	msgbox EryonLigaRecover_Text_NotQualified, MSGBOX_DEFAULT
	release
	end

EryonLigaRecover_Text_Heal:
	.string "ENFERMEIRA: Parabens\n"
	.string "pela CLASSIFICATORIA!\p"
	.string "Vou recuperar toda\n"
	.string "a sua equipe Pokemon.$"

EryonLigaRecover_Text_Official:
	.string "OFICIAL: As 8 vitorias\n"
	.string "foram registradas!\p"
	.string "Agora vem a ELITE 4.\n"
	.string "Prepare sua equipe.$"

EryonLigaRecover_Text_EliteGate:
	.string "PORTA DA ELITE FOUR:\n"
	.string "credencial aprovada.\p"
	.string "As salas dos 4 mestres\n"
	.string "ainda serao finalizadas.$"

EryonLigaRecover_Text_NotQualified:
	.string "OFICIAL: Primeiro,\n"
	.string "venca as oito fases\n"
	.string "da CLASSIFICATORIA.$"

EryonLigaRecover_Text_ReturnLobby:
	.string "Voltar para a recepcao\n"
	.string "da Liga de Eryon?$"

