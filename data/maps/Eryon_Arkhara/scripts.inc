Eryon_Arkhara_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Eryon_Arkhara_RespawnCheckpoint
	.byte 0

@ Native whiteout/Teleport checkpoint. Preserve all existing NPC and gym scripts.
Eryon_Arkhara_RespawnCheckpoint:
	setrespawn HEAL_LOCATION_ERYON_ARKHARA
	end

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
	goto_if_set FLAG_BADGE04_GET, EryonArkhara_EventScript_GymAfter
	goto_if_unset FLAG_BADGE03_GET, EryonArkhara_EventScript_GymNotReady
	goto_if_set FLAG_ERYON_ARKHARA_RELAY_READ, EryonArkhara_EventScript_GymOffer
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
	goto_if_set FLAG_ERYON_SERRA_ECLIPSE_SIGNAL_DISABLED, EryonArkhara_EventScript_GeologistResonance
	goto_if_set FLAG_ERYON_SERRA_CORE_GUARD_DEFEATED, EryonArkhara_EventScript_GeologistGuardDefeated
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
	goto_if_set FLAG_ERYON_SERRA_ECLIPSE_SIGNAL_DISABLED, EryonArkhara_EventScript_EclipseCourierResonance
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
	.string "Ela treina com rochas;\n"
	.string "seu principal e CLAYDOL.$"

EryonArkhara_Text_TessaBefore:
	.string "TESSA: Protejo as\n"
	.string "rochas desta cidade.\p"
	.string "Um sinal desconhecido\n"
	.string "abala a montanha.$"

EryonArkhara_Text_TessaInformed:
	.string "TESSA: As provas ligam\n"
	.string "a ECLIPSE a ARKHARA!\p"
	.string "Meu desafio oficial\n"
	.string "ja esta disponivel!$"

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

@ Tactical badge battle — Arkhara: ace level 36, badge 4.
EryonArkhara_EventScript_GymOffer::
	msgbox EryonArkhara_Text_GymOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonArkhara_EventScript_GymDecline
	closemessage
	trainerbattle_single TRAINER_ERYON_GYM_ARKHARA, EryonArkhara_Text_GymIntro, EryonArkhara_Text_GymLoss, EryonArkhara_EventScript_GymVictory, FALSE
	msgbox EryonArkhara_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_GymVictory::
	message EryonArkhara_Text_GymBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	setflag FLAG_BADGE04_GET
	msgbox EryonArkhara_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_GymDecline::
	closemessage
	release
	end

EryonArkhara_EventScript_GymNotReady::
	msgbox EryonArkhara_Text_GymNotReady, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_GymAfter::
	goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN, EryonArkhara_EventScript_GymAfterEclipse
	goto_if_set FLAG_ERYON_SERRA_ECLIPSE_SIGNAL_DISABLED, EryonArkhara_EventScript_TessaResonance
	msgbox EryonArkhara_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonArkhara_Text_GymOffer:
	.string "TESSA: Meu GINASIO\n"
	.string "treina com rochas antigas.\p"
	.string "Desafiar meu time\n"
	.string "de Pokemon agora?$"

EryonArkhara_Text_GymIntro:
	.string "TESSA: Mostre sua\n"
	.string "forca e estrategia!$"

EryonArkhara_Text_GymLoss:
	.string "TESSA: Voce encontrou\n"
	.string "uma boa resposta!$"

EryonArkhara_Text_GymBadge:
	.string "Venceu o 4o GINASIO!\p"
	.string "Recebeu a INSIGNIA\n"
	.string "de numero 4!$"

EryonArkhara_Text_GymAfter:
	.string "TESSA: Bela vitoria!\p"
	.string "Guarde as runas de ARKHARA.$"

EryonArkhara_Text_GymNotReady:
	.string "TESSA: Primeiro,\n"
	.string "conquiste a INSIGNIA\n"
	.string "do GINASIO anterior.$"


@ Successful Serra signal shutdown is acknowledged by Arkhara's geology team.
@ Optional PP UP reward is available exactly once and retryable if Bag is full.
EryonArkhara_EventScript_GeologistResonance::
	goto_if_set FLAG_ERYON_SERRA_SURVEY_REWARD_CLAIMED, EryonArkhara_EventScript_GeologistResonanceDone
	msgbox EryonArkhara_Text_GeologistReward, MSGBOX_DEFAULT
	giveitem ITEM_PP_UP
	goto_if_eq VAR_RESULT, FALSE, EryonArkhara_EventScript_GeologistRewardFull
	setflag FLAG_ERYON_SERRA_SURVEY_REWARD_CLAIMED
	msgbox EryonArkhara_Text_GeologistRewardSuccess, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_GeologistRewardFull::
	msgbox EryonArkhara_Text_GeologistRewardFull, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_GeologistResonanceDone::
	msgbox EryonArkhara_Text_GeologistResonanceDone, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_EclipseCourierResonance::
	msgbox EryonArkhara_Text_EclipseCourierResonance, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_TessaResonance::
	msgbox EryonArkhara_Text_TessaResonance, MSGBOX_DEFAULT
	release
	end

EryonArkhara_Text_GeologistReward:
	.string "GEOLOGO: Voce desligou\n"
	.string "a rede da ECLIPSE!\p"
	.string "As pedras da serra\n"
	.string "voltaram ao normal.\p"
	.string "Receba nossa ajuda\n"
	.string "pela pesquisa.$"

EryonArkhara_Text_GeologistRewardSuccess:
	.string "GEOLOGO: Os dados\n"
	.string "ja chegaram a ARKHARA.\p"
	.string "Agora podemos vigiar\n"
	.string "as rotas com seguranca.$"

EryonArkhara_Text_GeologistRewardFull:
	.string "GEOLOGO: Sua BOLSA\n"
	.string "esta cheia.\p"
	.string "Volte para receber\n"
	.string "a recompensa.$"

EryonArkhara_Text_GeologistResonanceDone:
	.string "GEOLOGO: Os cristais\n"
	.string "estao silenciosos.\p"
	.string "A rede da ECLIPSE\n"
	.string "na serra foi interrompida.$"

EryonArkhara_Text_EclipseCourierResonance:
	.string "ECLIPSE: A frequencia\n"
	.string "da serra desapareceu!\p"
	.string "Nao consigo rastrear\n"
	.string "nossa proxima carga.$"

EryonArkhara_Text_TessaResonance:
	.string "TESSA: Voce protegeu\n"
	.string "ARKHARA e a serra!\p"
	.string "Minha INSIGNIA e sua\n"
	.string "prova de coragem.$"


@ Reports arrive in Arkhara as the Crystal Serra operation progresses.
EryonArkhara_EventScript_GeologistGuardDefeated::
	msgbox EryonArkhara_Text_GeologistGuardDefeated, MSGBOX_DEFAULT
	release
	end

EryonArkhara_Text_GeologistGuardDefeated:
	.string "GEOLOGO: Venceu o\n"
	.string "sentinela da ECLIPSE?!\p"
	.string "Volte ao NUCLEO\n"
	.string "na SERRA DOS CRISTAIS.\p"
	.string "Desligar o sinal\n"
	.string "protegera ARKHARA.$"

@ Public shipment ledger connects the Crystal Serra survey to later Eclipse cities.
@ No duplicate reward/flag: all conclusions follow existing saved milestones.
EryonArkhara_EventScript_CaravanBoard::
	lock
	goto_if_set FLAG_ERYON_SERRA_ECLIPSE_SIGNAL_DISABLED, EryonArkhara_EventScript_CaravanBoardQuiet
	goto_if_set FLAG_ERYON_SERRA_CORE_GUARD_DEFEATED, EryonArkhara_EventScript_CaravanBoardGuard
	goto_if_set FLAG_BADGE04_GET, EryonArkhara_EventScript_CaravanBoardBadge
	msgbox EryonArkhara_Text_CaravanBoardBefore, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_CaravanBoardBadge::
	msgbox EryonArkhara_Text_CaravanBoardBadge, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_CaravanBoardGuard::
	msgbox EryonArkhara_Text_CaravanBoardGuard, MSGBOX_DEFAULT
	release
	end

EryonArkhara_EventScript_CaravanBoardQuiet::
	msgbox EryonArkhara_Text_CaravanBoardQuiet, MSGBOX_DEFAULT
	release
	end

EryonArkhara_Text_CaravanBoardBefore:
	.string "QUADRO DE CARGAS:\n"
	.string "Cristais desapareceram\n"
	.string "da rota da SERRA.\p"
	.string "Destino da remessa:\n"
	.string "ainda desconhecido.$"

EryonArkhara_Text_CaravanBoardBadge:
	.string "QUADRO DE CARGAS:\n"
	.string "A liga local recebeu\n"
	.string "um alerta de TESSA.\p"
	.string "Verifique as trilhas\n"
	.string "da SERRA DOS CRISTAIS.$"

EryonArkhara_Text_CaravanBoardGuard:
	.string "QUADRO DE CARGAS:\n"
	.string "Sentinela ECLIPSE\n"
	.string "afastado do NUCLEO.\p"
	.string "A estacao continua\n"
	.string "ligada nas montanhas.$"

EryonArkhara_Text_CaravanBoardQuiet:
	.string "QUADRO DE CARGAS:\n"
	.string "Sinal da SERRA: OFF.\p"
	.string "Carrocas da ECLIPSE\n"
	.string "seguiram para UMBRA.\p"
	.string "Outros relatorios citam\n"
	.string "a usina de IGNIVAR.$"
 
@ Epilogue only; previous badge, Serra and battle routes remain unchanged.
EryonArkhara_EventScript_GymAfterEclipse::
	msgbox EryonArkhara_Text_GymAfterEclipse, MSGBOX_DEFAULT
	release
	end

EryonArkhara_Text_GymAfterEclipse:
	.string "TESSA: As ruinas agora\n"
	.string "podem repousar.\p"
	.string "O sinal da ECLIPSE\n"
	.string "sumiu das pedras.$"

@ Separate playable gym interior. The existing badge and trainer battle scripts
@ are not duplicated: the interior leader calls this city's original challenge.
EryonArkhara_EventScript_GymEntrance::
	lock
	faceplayer
	msgbox EryonArkhara_Text_GymEntrance, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonArkhara_EventScript_GymEntranceCancel
	closemessage
	warp MAP_GYMERYON_ARKHARA, 12, 15
	waitstate
	end

EryonArkhara_EventScript_GymEntranceCancel::
	closemessage
	release
	end

EryonArkhara_Text_GymEntrance:
	.string "ENTRADA DO GINASIO:\p"
	.string "Entrar na arena de\\n"
	.string "ARKHARA agora?$"
