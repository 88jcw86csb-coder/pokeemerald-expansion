Eryon_TrilhaLunar_MapScripts::
	.byte 0

@ The old lunar observations explain why Eclipse follows the ancient song.
EryonLunar_EventScript_Astronomer::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonLunar_EventScript_AstronomerClue
	msgbox EryonLunar_Text_AstronomerBefore, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_AstronomerClue::
	msgbox EryonLunar_Text_AstronomerClue, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_Watchman::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_ECHO_TRACE_RECORDED, EryonLunar_EventScript_WatchmanTrace
	msgbox EryonLunar_Text_Watchman, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_EclipseSurveyor::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonLunar_EventScript_EclipseSurveyorExposed
	msgbox EryonLunar_Text_SurveyorBefore, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_EclipseSurveyorExposed::
	msgbox EryonLunar_Text_SurveyorExposed, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_MoonMarker::
	lock
	goto_if_set FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED, EryonLunar_EventScript_MoonMarkerArchive
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonLunar_EventScript_MoonMarkerClue
	msgbox EryonLunar_Text_MoonMarkerBefore, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_MoonMarkerClue::
	msgbox EryonLunar_Text_MoonMarkerClue, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_ClosedPass::
	lock
	msgbox EryonLunar_Text_ClosedPass, MSGBOX_DEFAULT
	release
	end

EryonLunar_Text_AstronomerBefore:
	.string "ASTRONOMA: As pedras\n"
	.string "guardam um velho canto.\p"
	.string "A LUA muda a forma\n"
	.string "como elas respondem.$"

EryonLunar_Text_AstronomerClue:
	.string "ASTRONOMA: Os pulsos\n"
	.string "de IGNIVAR vieram ate ca.\p"
	.string "A ECLIPSE quer forcar\n"
	.string "o canto dos cristais.$"

EryonLunar_Text_Watchman:
	.string "VIGIA: A trilha passa\n"
	.string "por claros e bosques.\p"
	.string "LUNARIS fica adiante,\n"
	.string "use o desvio leste.$"

EryonLunar_Text_SurveyorBefore:
	.string "TECNICO: O observatorio\n"
	.string "esta em reparos.\p"
	.string "A area leste segue\n"
	.string "aberta sob vigilancia.$"

EryonLunar_Text_SurveyorExposed:
	.string "ECLIPSE: O arquivo da\n"
	.string "aldeia revelou a rota!\p"
	.string "Um sinal maior deve\n"
	.string "surgir em LUNARIS.$"

EryonLunar_Text_MoonMarkerBefore:
	.string "Uma pedra polida\n"
	.string "mostra fases da LUA.\p"
	.string "Uma melodia baixa\n"
	.string "parece vir da terra.$"

EryonLunar_Text_MoonMarkerClue:
	.string "O selo da ECLIPSE\n"
	.string "esta sob a pedra.\p"
	.string "Um desenho aponta\n"
	.string "para LUNARIS.$"

EryonLunar_Text_ClosedPass:
	.string "PONTE EM MANUTENCAO!\n"
	.string "Desvio para LUNARIS aberto.\p"
	.string "Os viajantes podem\n"
	.string "seguir pela trilha.$"

@ Optional chart connects Echo Valley, its village archive, and Lunaris.
EryonLunar_EventScript_StarCalibration::
	lock
	goto_if_set FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED, EryonLunar_EventScript_StarCalibrationComplete
	goto_if_set FLAG_ERYON_ECHO_TRACE_RECORDED, EryonLunar_EventScript_StarCalibrationPending
	msgbox EryonLunar_Text_StarCalibrationBefore, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_StarCalibrationPending::
	msgbox EryonLunar_Text_StarCalibrationPending, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_StarCalibrationComplete::
	msgbox EryonLunar_Text_StarCalibrationComplete, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_WatchmanTrace::
	msgbox EryonLunar_Text_WatchmanTrace, MSGBOX_DEFAULT
	release
	end

EryonLunar_Text_StarCalibrationBefore:
	.string "MARCADOR ESTELAR:\n"
	.string "Este disco segue a LUA.\p"
	.string "O vale ainda nao tem\n"
	.string "dados registrados.$"

EryonLunar_Text_StarCalibrationPending:
	.string "MARCADOR ESTELAR:\n"
	.string "O som do vale aponta\n"
	.string "para o OBSERVATORIO.\p"
	.string "Consulte antes o\n"
	.string "ARQUIVO DA ALDEIA.$"

EryonLunar_Text_StarCalibrationComplete:
	.string "MARCADOR ESTELAR:\n"
	.string "A frequencia natural\n"
	.string "e a da ECLIPSE diferem.\p"
	.string "LUNARIS pode comparar\n"
	.string "ambos os sinais.$"

EryonLunar_Text_WatchmanTrace:
	.string "VIGIA: O ARQUIVO\n"
	.string "precisa de sua prova!\p"
	.string "Depois siga a LUNARIS\n"
	.string "pela trilha leste.$"

@ The existing lunar marker reveals a new chapter after the optional archive delivery.
@ No new flag, item, trainer or badge state is introduced.
EryonLunar_EventScript_MoonMarkerArchive:
	goto_if_set FLAG_BADGE07_GET, EryonLunar_EventScript_MoonMarkerBadge
	msgbox EryonLunar_Text_MoonMarkerArchive, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_MoonMarkerBadge:
	msgbox EryonLunar_Text_MoonMarkerBadge, MSGBOX_DEFAULT
	release
	end

EryonLunar_Text_MoonMarkerArchive:
	.string "O registro da ALDEIA\n"
	.string "faz o disco ressoar!\p"
	.string "As marcas indicam que\n"
	.string "a ECLIPSE mudou o sinal.\p"
	.string "A ASTRONOMA de LUNARIS\n"
	.string "pode comparar os dados.$"

EryonLunar_Text_MoonMarkerBadge:
	.string "A 7a INSIGNIA brilha\n"
	.string "diante do disco lunar.\p"
	.string "Um novo padrao aponta\n"
	.string "para DRAKONIA.\p"
	.string "A jornada continua\n"
	.string "pela TRILHA DOS DRAGOES.$"
