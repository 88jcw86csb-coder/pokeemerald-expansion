@ Eryon: early route foreshadowing, no battles or story flags yet.
EryonRota02_EventScript_Hiker::
	lock
	faceplayer
	msgbox EryonRota02_Text_Hiker, MSGBOX_DEFAULT
	release
	end

EryonRota02_Text_Hiker:
	.string "O caminho ate Verdelume e longo.\p"
	.string "Nao se apresse: ha trilhas\n"
	.string "escondidas entre estas colinas.$"

@ An optional roadside first-aid cache, independent from the main quest.
EryonRota02_EventScript_RoadsideCache::
	lock
	goto_if_ge VAR_ERYON_ROTA02_SUPPLY_FOUND, 1, EryonRota02_EventScript_RoadsideCacheEmpty
	msgbox EryonRota02_Text_RoadsideCache, MSGBOX_DEFAULT
	giveitem ITEM_ANTIDOTE
	goto_if_eq VAR_RESULT, FALSE, EryonRota02_EventScript_RoadsideCacheFull
	setvar VAR_ERYON_ROTA02_SUPPLY_FOUND, 1
	release
	end

EryonRota02_EventScript_RoadsideCacheFull::
	msgbox EryonRota02_Text_RoadsideCacheFull, MSGBOX_DEFAULT
	release
	end

EryonRota02_EventScript_RoadsideCacheEmpty::
	msgbox EryonRota02_Text_RoadsideCacheEmpty, MSGBOX_DEFAULT
	release
	end

EryonRota02_Text_RoadsideCache:
	.string "Uma caixa de primeiros socorros\n"
	.string "foi deixada perto da trilha.$"

EryonRota02_Text_RoadsideCacheFull:
	.string "Nao ha espaco na bolsa.\p"
	.string "O antidoto continuara aqui.$"

EryonRota02_Text_RoadsideCacheEmpty:
	.string "A caixa esta vazia.\p"
	.string "Alguem cuidou dos viajantes.$"
