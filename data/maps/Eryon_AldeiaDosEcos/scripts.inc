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
