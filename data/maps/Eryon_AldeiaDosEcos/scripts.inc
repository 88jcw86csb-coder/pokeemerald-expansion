Eryon_AldeiaDosEcos_MapScripts::
	.byte 0

@ A settlement protects an ancient archive now targeted by Team Eclipse.
EryonAldeia_EventScript_Elder::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonAldeia_EventScript_ElderInformed
	msgbox EryonAldeia_Text_ElderBefore, MSGBOX_DEFAULT
	release
	end

EryonAldeia_EventScript_ElderInformed::
	msgbox EryonAldeia_Text_ElderInformed, MSGBOX_DEFAULT
	release
	end

EryonAldeia_EventScript_Healer::
	lock
	faceplayer
	msgbox EryonAldeia_Text_Healer, MSGBOX_DEFAULT
	special HealPlayerParty
	release
	end

EryonAldeia_EventScript_Archivist::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED, EryonAldeia_EventScript_ArchivistReportDone
	goto_if_set FLAG_ERYON_ECHO_TRACE_RECORDED, EryonAldeia_EventScript_ArchivistReceiveTrace
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonAldeia_EventScript_ArchivistClue
	msgbox EryonAldeia_Text_ArchivistBefore, MSGBOX_DEFAULT
	release
	end

EryonAldeia_EventScript_ArchivistClue::
	msgbox EryonAldeia_Text_ArchivistClue, MSGBOX_DEFAULT
	release
	end

EryonAldeia_EventScript_Witness::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_FOREST_PHANTUMP_RESOLVED, EryonAldeia_EventScript_WitnessGroveSafe
	goto_if_set FLAG_ERYON_FOREST_SIGNAL_LOG_READ, EryonAldeia_EventScript_WitnessCanopyLog
	msgbox EryonAldeia_Text_Witness, MSGBOX_DEFAULT
	release
	end

EryonAldeia_EventScript_Notice::
	lock
	msgbox EryonAldeia_Text_Notice, MSGBOX_DEFAULT
	release
	end

EryonAldeia_EventScript_OldMonument::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonAldeia_EventScript_OldMonumentClue
	msgbox EryonAldeia_Text_MonumentBefore, MSGBOX_DEFAULT
	release
	end

EryonAldeia_EventScript_OldMonumentClue::
	msgbox EryonAldeia_Text_MonumentClue, MSGBOX_DEFAULT
	release
	end

EryonAldeia_Text_ElderBefore:
	.string "ANCIA: A aldeia guarda\n"
	.string "cantos antigos do vale.\p"
	.string "Ultimamente a terra\n"
	.string "parece responder.$"

EryonAldeia_Text_ElderInformed:
	.string "ANCIA: A ECLIPSE quer\n"
	.string "controlar nossos ecos!\p"
	.string "Investigue os cristais\n"
	.string "e proteja o arquivo.$"

EryonAldeia_Text_Healer:
	.string "CUIDADORA: Quem chega\n"
	.string "do vale precisa parar.\p"
	.string "Vou curar seus Pokemon\n"
	.string "antes da pesquisa.$"

EryonAldeia_Text_ArchivistBefore:
	.string "ARQUIVISTA: O canto\n"
	.string "das pedras e antigo.\p"
	.string "Estou reunindo notas\n"
	.string "sobre sua origem.$"

EryonAldeia_Text_ArchivistClue:
	.string "ARQUIVISTA: Os pulsos\n"
	.string "da ECLIPSE sao artificiais!\p"
	.string "Os ecos naturais sao\n"
	.string "muito mais lentos.$"

EryonAldeia_Text_Witness:
	.string "JOVEM: Vi um tecnico\n"
	.string "com caixas no vale.\p"
	.string "Entrou na mata quando\n"
	.string "ouviu o sino da vila.$"

EryonAldeia_Text_Notice:
	.string "ALDEIA DOS ECOS:\n"
	.string "Cuidado com os cristais.\p"
	.string "Avisem a guardia se\n"
	.string "o som mudar.$"

EryonAldeia_Text_MonumentBefore:
	.string "Um monumento antigo\n"
	.string "tem marcas musicais.\p"
	.string "Uma brisa faz sua\n"
	.string "superficie vibrar.$"

EryonAldeia_Text_MonumentClue:
	.string "O simbolo da ECLIPSE\n"
	.string "foi riscado na pedra.\p"
	.string "Alguem tentou alterar\n"
	.string "o som do monumento.$"

@ Archived valley signal rewards one Star Piece; failed Bag transfer is retriable.
EryonAldeia_EventScript_ArchivistReceiveTrace::
	msgbox EryonAldeia_Text_ArchivistReceiveTrace, MSGBOX_DEFAULT
	giveitem ITEM_STAR_PIECE
	goto_if_eq VAR_RESULT, FALSE, EryonAldeia_EventScript_ArchivistBagFull
	setflag FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED
	msgbox EryonAldeia_Text_ArchivistResearchDone, MSGBOX_DEFAULT
	release
	end

EryonAldeia_EventScript_ArchivistBagFull::
	msgbox EryonAldeia_Text_ArchivistBagFull, MSGBOX_DEFAULT
	release
	end

EryonAldeia_EventScript_ArchivistReportDone::
	msgbox EryonAldeia_Text_ArchivistResearchDone, MSGBOX_DEFAULT
	release
	end

EryonAldeia_Text_ArchivistReceiveTrace:
	.string "ARQUIVISTA: Seu registro\n"
	.string "revela duas frequencias!\p"
	.string "Uma e natural; a outra\n"
	.string "foi criada pela ECLIPSE.\p"
	.string "Receba isto por ajudar\n"
	.string "a salvar o arquivo.$"

EryonAldeia_Text_ArchivistBagFull:
	.string "Sua BOLSA esta cheia!\p"
	.string "Guardarei a recompensa.\n"
	.string "Volte quando puder.$"

EryonAldeia_Text_ArchivistResearchDone:
	.string "ARQUIVISTA: A LUA pode\n"
	.string "ampliar as frequencias.\p"
	.string "Mostre os resultados\n"
	.string "no OBSERVATORIO LUNAR.$"

@ The valley village learns the results of the optional forest grove survey.
EryonAldeia_EventScript_WitnessCanopyLog::
	msgbox EryonAldeia_Text_WitnessCanopyLog, MSGBOX_DEFAULT
	release
	end

EryonAldeia_EventScript_WitnessGroveSafe::
	msgbox EryonAldeia_Text_WitnessGroveSafe, MSGBOX_DEFAULT
	release
	end

EryonAldeia_Text_WitnessCanopyLog:
	.string "JOVEM: Achou o caderno\n"
	.string "da copa da floresta?\p"
	.string "PHANTUMP mora numa\n"
	.string "clareira escondida!$"

EryonAldeia_Text_WitnessGroveSafe:
	.string "JOVEM: A floresta\n"
	.string "esta em paz novamente!\p"
	.string "As arvores voltaram\n"
	.string "a cantar naturalmente.$"
