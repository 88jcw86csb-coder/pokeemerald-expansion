Eryon_ValeDosEcos_MapScripts::
	.byte 0

@ The Eclipse signal travels through old crystals between the forest and village.
EryonEcoVale_EventScript_Trailkeeper::
	lock
	faceplayer
	msgbox EryonEcoVale_Text_Trailkeeper, MSGBOX_DEFAULT
	release
	end

EryonEcoVale_EventScript_Researcher::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonEcoVale_EventScript_ResearcherInformed
	msgbox EryonEcoVale_Text_ResearcherBefore, MSGBOX_DEFAULT
	release
	end

EryonEcoVale_EventScript_ResearcherInformed::
	msgbox EryonEcoVale_Text_ResearcherInformed, MSGBOX_DEFAULT
	release
	end

EryonEcoVale_EventScript_EclipseOperator::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonEcoVale_EventScript_EclipseOperatorExposed
	trainerbattle_single TRAINER_ERYON_ECHO_VALLEY_ECLIPSE, EryonEcoVale_Text_OperatorBefore, EryonEcoVale_Text_OperatorDefeat, EryonEcoVale_EventScript_EclipseOperatorVictory, FALSE
	msgbox EryonEcoVale_Text_OperatorAfter, MSGBOX_DEFAULT
	release
	end

EryonEcoVale_EventScript_EclipseOperatorExposed::
	trainerbattle_single TRAINER_ERYON_ECHO_VALLEY_ECLIPSE, EryonEcoVale_Text_OperatorExposed, EryonEcoVale_Text_OperatorDefeat, EryonEcoVale_EventScript_EclipseOperatorVictory, FALSE
	msgbox EryonEcoVale_Text_OperatorAfter, MSGBOX_DEFAULT
	release
	end

EryonEcoVale_EventScript_EclipseOperatorVictory::
	msgbox EryonEcoVale_Text_OperatorAfter, MSGBOX_DEFAULT
	release
	end

EryonEcoVale_EventScript_CrystalArray::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonEcoVale_EventScript_CrystalArrayClue
	msgbox EryonEcoVale_Text_CrystalBefore, MSGBOX_DEFAULT
	release
	end

EryonEcoVale_EventScript_CrystalArrayClue::
	msgbox EryonEcoVale_Text_CrystalClue, MSGBOX_DEFAULT
	release
	end

EryonEcoVale_EventScript_VillageSign::
	lock
	msgbox EryonEcoVale_Text_VillageSign, MSGBOX_DEFAULT
	release
	end

EryonEcoVale_Text_Trailkeeper:
	.string "VIGIA: No vale o eco\n"
	.string "faz perder a direcao.\p"
	.string "Siga pelo caminho ate\n"
	.string "a ALDEIA DOS ECOS.$"

EryonEcoVale_Text_ResearcherBefore:
	.string "PESQUISADOR: Os cristais\n"
	.string "parecem cantar sozinhos.\p"
	.string "Ninguem sabe de onde\n"
	.string "vem essa energia.$"

EryonEcoVale_Text_ResearcherInformed:
	.string "PESQUISADOR: O pulso\n"
	.string "vem da usina IGNIVAR!\p"
	.string "A ECLIPSE esta usando\n"
	.string "o vale como antena.$"

EryonEcoVale_Text_OperatorBefore:
	.string "TECNICO: Nao toque\n"
	.string "no nosso equipamento!\p"
	.string "Vou impedir sua\n"
	.string "passagem pelo vale!$"

EryonEcoVale_Text_OperatorExposed:
	.string "ECLIPSE: Descobriu\n"
	.string "nosso sinal de Ignivar?\p"
	.string "Entao enfrente minha\n"
	.string "equipe Pokemon!$"

EryonEcoVale_Text_OperatorDefeat:
	.string "O reator perdeu\n"
	.string "a frequencia...$"

EryonEcoVale_Text_OperatorAfter:
	.string "ECLIPSE: O arquivo da\n"
	.string "aldeia e nosso alvo.\p"
	.string "Outros membros ainda\n"
	.string "estao investigando.$"

EryonEcoVale_Text_CrystalBefore:
	.string "Cristais antigos\n"
	.string "brilham entre as rochas.\p"
	.string "Um som grave ecoa\n"
	.string "sob seus pes.$"

EryonEcoVale_Text_CrystalClue:
	.string "Marcas ECLIPSE cobrem\n"
	.string "os cristais do vale.\p"
	.string "Cabos seguem para a\n"
	.string "ALDEIA DOS ECOS.$"

EryonEcoVale_Text_VillageSign:
	.string "LESTE: ALDEIA DOS ECOS.\n"
	.string "OESTE: FLORESTA DOS ECOS.$"

@ Optional signal study; records evidence without changing the Eclipse battle.
EryonEcoVale_EventScript_PulseRecorder::
	lock
	goto_if_set FLAG_ERYON_ECHO_TRACE_RECORDED, EryonEcoVale_EventScript_PulseRecorderDone
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonEcoVale_EventScript_PulseRecorderOffer
	msgbox EryonEcoVale_Text_RecorderWaiting, MSGBOX_DEFAULT
	release
	end

EryonEcoVale_EventScript_PulseRecorderOffer::
	msgbox EryonEcoVale_Text_RecorderOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonEcoVale_EventScript_PulseRecorderDecline
	closemessage
	setflag FLAG_ERYON_ECHO_TRACE_RECORDED
	msgbox EryonEcoVale_Text_RecorderSaved, MSGBOX_DEFAULT
	release
	end

EryonEcoVale_EventScript_PulseRecorderDecline::
	closemessage
	release
	end

EryonEcoVale_EventScript_PulseRecorderDone::
	msgbox EryonEcoVale_Text_RecorderDone, MSGBOX_DEFAULT
	release
	end

EryonEcoVale_Text_RecorderWaiting:
	.string "GRAVADOR DE ECOS:\n"
	.string "As pedras vibram.\p"
	.string "Faltam pistas para\n"
	.string "comparar a frequencia.$"

EryonEcoVale_Text_RecorderOffer:
	.string "Os pulsos lembram a\n"
	.string "pesquisa da SERRA!\p"
	.string "Registrar os dados\n"
	.string "para a ALDEIA DOS ECOS?$"

EryonEcoVale_Text_RecorderSaved:
	.string "O eco foi registrado!\p"
	.string "Leve os dados a\n"
	.string "ALDEIA DOS ECOS.\p"
	.string "A ECLIPSE procura\n"
	.string "o mesmo som.$"

EryonEcoVale_Text_RecorderDone:
	.string "GRAVADOR DE ECOS:\n"
	.string "Frequencia armazenada.\p"
	.string "O ARQUIVO DA ALDEIA\n"
	.string "pode analisar o sinal.$"
