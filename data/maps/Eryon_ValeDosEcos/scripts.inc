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
	msgbox EryonEcoVale_Text_OperatorBefore, MSGBOX_DEFAULT
	release
	end

EryonEcoVale_EventScript_EclipseOperatorExposed::
	msgbox EryonEcoVale_Text_OperatorExposed, MSGBOX_DEFAULT
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
	.string "TECNICO: A passagem\n"
	.string "esta em manutencao.\p"
	.string "Nao mexa nas pedras.$"

EryonEcoVale_Text_OperatorExposed:
	.string "ECLIPSE: O sinal veio\n"
	.string "de SOLARIS e IGNIVAR!\p"
	.string "Logo a aldeia ouvira\n"
	.string "nossa frequencia.$"

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
