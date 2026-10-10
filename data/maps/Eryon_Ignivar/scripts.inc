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
	msgbox EryonIgnivar_Text_GridInspector, MSGBOX_DEFAULT
	release
	end

EryonIgnivar_Text_GridInspector:
	.string "TECNICA: A usina sofre pulsos\n"
	.string "vindos de Solaris.\p"
	.string "A rede da floresta\n"
	.string "tambem foi atingida.$"
