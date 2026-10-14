Eryon_Ignivar_MapScripts::
	.byte 0

@ The city receives unstable geothermal power after Eclipse's desert relay activates.
EryonIgnivar_EventScript_Engineer::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonIgnivar_EventScript_EngineerClue
	msgbox EryonIgnivar_Text_EngineerBefore, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_EventScript_EngineerClue::
	msgbox EryonIgnivar_Text_EngineerClue, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_EventScript_GymSteward::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonIgnivar_EventScript_GymStewardClue
	msgbox EryonIgnivar_Text_GymStewardBefore, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_EventScript_GymStewardClue::
	msgbox EryonIgnivar_Text_GymStewardClue, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_EventScript_EclipseTechnician::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonIgnivar_EventScript_EclipseTechnicianClue
	msgbox EryonIgnivar_Text_EclipseTechnicianBefore, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_EventScript_EclipseTechnicianClue::
	msgbox EryonIgnivar_Text_EclipseTechnicianClue, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_EventScript_PowerGridNotice::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonIgnivar_EventScript_PowerGridNoticeClue
	msgbox EryonIgnivar_Text_PowerGridNoticeBefore, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_EventScript_PowerGridNoticeClue::
	msgbox EryonIgnivar_Text_PowerGridNoticeClue, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_EventScript_BurntFuse::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonIgnivar_EventScript_BurntFuseClue
	msgbox EryonIgnivar_Text_BurntFuseBefore, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_EventScript_BurntFuseClue::
	msgbox EryonIgnivar_Text_BurntFuseClue, MSGBOX_DEFAULT
	release
	end

@ Emergency medic helps travelers while Ignivar's grid is unstable.
EryonIgnivar_EventScript_EmergencyMedic::
	lock
	faceplayer
	msgbox EryonIgnivar_Text_Medic, MSGBOX_DEFAULT
	special HealPlayerParty
	release
	end

EryonIgnivar_Text_Medic:
	.string "SOCORRISTA: A usina\n"
	.string "ainda esta instavel.\p"
	.string "Vou cuidar da sua equipe\n"
	.string "antes da travessia.$"

EryonIgnivar_Text_EngineerBefore:
	.string "ENGENHEIRA: O calor\n"
	.string "mantem a cidade viva.\p"
	.string "Mas a rede eletrica\n"
	.string "anda instavel.$"

EryonIgnivar_Text_EngineerClue:
	.string "ENGENHEIRA: Descobriu\n"
	.string "a antena de Solaris?\p"
	.string "Ela injeta energia na\n"
	.string "rede sem permissao!$"

EryonIgnivar_Text_GymStewardBefore:
	.string "GUIA: O GINASIO de\n"
	.string "Ignivar usa tipo FOGO.\p"
	.string "Dizem que a arena\n"
	.string "testa sua paciencia.$"

EryonIgnivar_Text_GymStewardClue:
	.string "GUIA: O lider investiga\n"
	.string "as falhas da usina.\p"
	.string "A ECLIPSE pode estar\n"
	.string "por tras de tudo isso.$"

EryonIgnivar_Text_EclipseTechnicianBefore:
	.string "TECNICO: Nao ha nada\n"
	.string "para ver na subestacao.\p"
	.string "A manutencao segue\n"
	.string "o cronograma normal.$"

EryonIgnivar_Text_EclipseTechnicianClue:
	.string "ECLIPSE: O deserto\n"
	.string "so alimenta a maquina!\p"
	.string "O sinal vai seguir\n"
	.string "para a FLORESTA DOS ECOS.$"

EryonIgnivar_Text_PowerGridNoticeBefore:
	.string "REDE DE IGNIVAR:\n"
	.string "Oscilacoes em analise.\p"
	.string "Evite equipamentos\n"
	.string "de alta tensao.$"

EryonIgnivar_Text_PowerGridNoticeClue:
	.string "REDE DE IGNIVAR:\n"
	.string "Entrada nao autorizada.\p"
	.string "Origem do sinal:\n"
	.string "DESERTO DE SOLARIS.$"

EryonIgnivar_Text_BurntFuseBefore:
	.string "Um fusivel queimado\n"
	.string "foi deixado na praca.\p"
	.string "O metal ainda esta\n"
	.string "morno.$"

EryonIgnivar_Text_BurntFuseClue:
	.string "No fusivel existe um\n"
	.string "selo da ECLIPSE.\p"
	.string "Um cabo segue para\n"
	.string "a FLORESTA DOS ECOS.$"

@ Additional local witness to the Eclipse signal crossing Eryon.
EryonIgnivar_EventScript_GridInspector::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_RIVER_SAMPLE_RECORDED, EryonIgnivar_EventScript_GridInspectorRiverSample
	msgbox EryonIgnivar_Text_GridInspector, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_Text_GridInspector:
	.string "TECNICA: A usina sofre\n"
	.string "pulsos de Solaris.\p"
	.string "A rede da floresta\n"
	.string "tambem foi atingida.$"

@ Regional aftermath of Eclipse's transmission experiment.
EryonIgnivar_EventScript_EvacuationCoordinator::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonIgnivar_EventScript_EvacuationCoordinatorInformed
	msgbox EryonIgnivar_Text_EvacuationCoordinatorBefore, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_EventScript_EvacuationCoordinatorInformed::
	msgbox EryonIgnivar_Text_EvacuationCoordinator, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_Text_EvacuationCoordinatorBefore:
	.string "MORADOR: A cidade e\n"
	.string "a floresta mudaram.\p"
	.string "Ha um ruido estranho\n"
	.string "perto das trilhas.$"

EryonIgnivar_Text_EvacuationCoordinator:
	.string "COORDENADOR: O bairro\n"
	.string "leste ficou sem luz.\p"
	.string "A equipe de resgate\n"
	.string "espera perto da mata.$"

@ Public emergency board tracks the same mission thread as the city witnesses.
EryonIgnivar_EventScript_EmergencyBoard::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonIgnivar_EventScript_EmergencyBoardAlert
	msgbox EryonIgnivar_Text_EmergencyBoardQuiet, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_EventScript_EmergencyBoardAlert::
	msgbox EryonIgnivar_Text_EmergencyBoardAlert, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_Text_EmergencyBoardQuiet:
	.string "AVISO: A subestacao\n"
	.string "esta em manutencao.\p"
	.string "Siga pela trilha leste\n"
	.string "com cuidado.$"

EryonIgnivar_Text_EmergencyBoardAlert:
	.string "ALERTA: Sinal vindo\n"
	.string "do deserto detectado!\p"
	.string "A equipe tecnica segue\n"
	.string "para a floresta.$"

@ Eryon: KAIO is the city leader, separate from the Gym guide.
EryonIgnivar_EventScript_GymLeader::
	lock
	faceplayer
	goto_if_set FLAG_BADGE06_GET, EryonIgnivar_EventScript_GymAfter
	goto_if_unset FLAG_BADGE05_GET, EryonIgnivar_EventScript_GymNotReady
	goto EryonIgnivar_EventScript_GymOffer
	end

@ Tactical badge battle — Ignivar: ace level 46, badge 6.
EryonIgnivar_EventScript_GymOffer::
	msgbox EryonIgnivar_Text_GymOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonIgnivar_EventScript_GymDecline
	closemessage
	trainerbattle_single TRAINER_ERYON_GYM_IGNIVAR, EryonIgnivar_Text_GymIntro, EryonIgnivar_Text_GymLoss, EryonIgnivar_EventScript_GymVictory, FALSE
	msgbox EryonIgnivar_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_EventScript_GymVictory::
	message EryonIgnivar_Text_GymBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	setflag FLAG_BADGE06_GET
	msgbox EryonIgnivar_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_EventScript_GymDecline::
	closemessage
	release
	end

EryonIgnivar_EventScript_GymNotReady::
	msgbox EryonIgnivar_Text_GymNotReady, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_EventScript_GymAfter::
	msgbox EryonIgnivar_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_Text_GymOffer:
	.string "KAIO: Meu GINASIO\n"
	.string "treina com fogo.\p"
	.string "Desafiar meu time\n"
	.string "de Pokemon agora?$"

EryonIgnivar_Text_GymIntro:
	.string "KAIO: Mostre sua\n"
	.string "forca e estrategia!$"

EryonIgnivar_Text_GymLoss:
	.string "KAIO: Voce encontrou\n"
	.string "uma boa resposta!$"

EryonIgnivar_Text_GymBadge:
	.string "Venceu o 6o GINASIO!\p"
	.string "Recebeu a INSIGNIA\n"
	.string "de numero 6!$"

EryonIgnivar_Text_GymAfter:
	.string "KAIO: Bela vitoria!\p"
	.string "Ajude a cidade a manter a luz.$"

EryonIgnivar_Text_GymNotReady:
	.string "KAIO: Primeiro,\n"
	.string "conquiste a INSIGNIA\n"
	.string "do GINASIO anterior.$"

@ Reports from the western waterway reach the large city power station.
EryonIgnivar_EventScript_RiverTransportBoard::
	lock
	goto_if_set FLAG_ERYON_RIVER_SAMPLE_RECORDED, EryonIgnivar_EventScript_RiverBoardSample
	msgbox EryonIgnivar_Text_RiverBoardBefore, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_EventScript_RiverBoardSample::
	msgbox EryonIgnivar_Text_RiverBoardSample, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_EventScript_GridInspectorRiverSample::
	msgbox EryonIgnivar_Text_InspectorRiverSample, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_Text_RiverBoardBefore:
	.string "QUADRO DA USINA:\n"
	.string "Cargas de origem\n"
	.string "desconhecida chegaram.\p"
	.string "Analise de agua:\n"
	.string "ainda sem resultado.$"

EryonIgnivar_Text_RiverBoardSample:
	.string "QUADRO DA USINA:\n"
	.string "A ECLIPSE contaminou\n"
	.string "o rio das CACHOEIRAS.\p"
	.string "A energia segue do\n"
	.string "SOLARIS aos ECOS.$"

EryonIgnivar_Text_InspectorRiverSample:
	.string "TECNICA: A analise\n"
	.string "da vila chegou aqui!\p"
	.string "A usina e a floresta\n"
	.string "partilham o mesmo sinal.\p"
	.string "A ECLIPSE nao controla\n"
	.string "somente o deserto.$"

