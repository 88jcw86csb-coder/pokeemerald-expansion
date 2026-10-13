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
	.string "mas a ponte caiu.$"

EryonLunar_Text_SurveyorBefore:
	.string "TECNICO: O observatorio\n"
	.string "esta em reparos.\p"
	.string "A area leste segue\n"
	.string "temporariamente fechada.$"

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
	.string "PASSAGEM INTERDITADA!\n"
	.string "Ponte de LUNARIS fechada.\p"
	.string "A equipe do vale\n"
	.string "ainda avalia os danos.$"
