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

@ A traveling cartographer foreshadows the eclipse mystery without blocking the road.
EryonRota02_EventScript_Cartographer::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonRota02_EventScript_CartographerAfterBadge
	goto_if_ge VAR_ERYON_KAEL_BRIEFED, 1, EryonRota02_EventScript_CartographerAfterKael
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonRota02_EventScript_CartographerAfterClue
	msgbox EryonRota02_Text_CartographerWelcome, MSGBOX_DEFAULT
	release
	end

EryonRota02_EventScript_CartographerAfterBadge::
	msgbox EryonRota02_Text_CartographerAfterBadge, MSGBOX_DEFAULT
	release
	end

EryonRota02_EventScript_CartographerAfterClue::
	msgbox EryonRota02_Text_CartographerAfterClue, MSGBOX_DEFAULT
	release
	end

EryonRota02_EventScript_CartographerAfterKael::
	msgbox EryonRota02_Text_CartographerAfterKael, MSGBOX_DEFAULT
	release
	end

EryonRota02_Text_CartographerWelcome:
	.string "Estou desenhando um mapa\n"
	.string "das trilhas de Eryon.\p"
	.string "O bosque parece mudar a cada dia.$"

EryonRota02_Text_CartographerAfterClue:
	.string "Uma marca de eclipse?\p"
	.string "Vi o mesmo desenho num mapa\n"
	.string "antigo. Kael pode ajudar.$"

EryonRota02_Text_CartographerAfterKael:
	.string "Kael ouviu sua historia?\p"
	.string "Vou comparar meu mapa com\n"
	.string "os registros de Verdelume.$"

@ The first badge unlocks an optional hint for the next stage of the journey.
EryonRota02_Text_CartographerAfterBadge:
	.string "Kael me contou da sua vitoria!\p"
	.string "O mapa antigo mostra outra\n"
	.string "trilha alem de Verdelume.\p"
	.string "Ainda preciso confirmar\n"
	.string "onde ela comeca.$"
