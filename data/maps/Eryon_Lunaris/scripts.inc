Eryon_Lunaris_MapScripts::
	.byte 0

@ Lunaris protects the ancient observatory and the seventh gym.
EryonLunaris_EventScript_Medic::
	lock
	faceplayer
	msgbox EryonLunaris_Text_Medic, MSGBOX_DEFAULT
	special HealPlayerParty
	release
	end

EryonLunaris_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonLunaris_EventScript_GymGuideClue
	msgbox EryonLunaris_Text_GymGuideBefore, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_GymGuideClue::
	msgbox EryonLunaris_Text_GymGuideClue, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_Astronomer::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonLunaris_EventScript_AstronomerClue
	msgbox EryonLunaris_Text_AstronomerBefore, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_AstronomerClue::
	msgbox EryonLunaris_Text_AstronomerClue, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_EclipseAnalyst::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonLunaris_EventScript_EclipseAnalystExposed
	msgbox EryonLunaris_Text_AnalystBefore, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_EclipseAnalystExposed::
	msgbox EryonLunaris_Text_AnalystExposed, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_ObservatorySign::
	lock
	msgbox EryonLunaris_Text_ObservatorySign, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_CrystalGenerator::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonLunaris_EventScript_CrystalGeneratorClue
	msgbox EryonLunaris_Text_GeneratorBefore, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_CrystalGeneratorClue::
	msgbox EryonLunaris_Text_GeneratorClue, MSGBOX_DEFAULT
	release
	end

EryonLunaris_Text_Medic:
	.string "SOCORRISTA: A trilha\n"
	.string "e longa e cansativa.\p"
	.string "Vou recuperar seus\n"
	.string "Pokemon agora.$"

EryonLunaris_Text_GymGuideBefore:
	.string "GUIA: O GINASIO de\n"
	.string "LUNARIS usa PSIQUICO.\p"
	.string "Pokemon FADA tambem\n"
	.string "ajudam nos desafios.$"

EryonLunaris_Text_GymGuideClue:
	.string "GUIA: O lider investiga\n"
	.string "os sinais da ECLIPSE.\p"
	.string "O desafio do GINASIO\n"
	.string "ainda nao foi liberado.$"

EryonLunaris_Text_AstronomerBefore:
	.string "ASTRONOMA: Os cristais\n"
	.string "seguem um antigo canto.\p"
	.string "O movimento da LUA\n"
	.string "altera sua frequencia.$"

EryonLunaris_Text_AstronomerClue:
	.string "ASTRONOMA: O sinal\n"
	.string "de IGNIVAR chegou aqui!\p"
	.string "O arquivo da ALDEIA\n"
	.string "revelou uma pista.$"

EryonLunaris_Text_AnalystBefore:
	.string "TECNICO: Estou medindo\n"
	.string "a luz das estrelas.\p"
	.string "O observatorio esta\n"
	.string "sob manutencao.$"

EryonLunaris_Text_AnalystExposed:
	.string "ECLIPSE: A LUA pode\n"
	.string "ampliar nosso sinal!\p"
	.string "As caixas ja seguem\n"
	.string "para DRAKONIA.$"

EryonLunaris_Text_ObservatorySign:
	.string "OBSERVATORIO LUNAR:\n"
	.string "Pesquisa de cristais.\p"
	.string "Acesso restrito na\n"
	.string "fase de manutencao.$"

EryonLunaris_Text_GeneratorBefore:
	.string "Um gerador antigo\n"
	.string "esta desligado.\p"
	.string "Uma carta celeste\n"
	.string "repousa ao lado.$"

EryonLunaris_Text_GeneratorClue:
	.string "O selo da ECLIPSE\n"
	.string "aparece no gerador.\p"
	.string "Cabos levam energia\n"
	.string "de IGNIVAR ate ca.$"
