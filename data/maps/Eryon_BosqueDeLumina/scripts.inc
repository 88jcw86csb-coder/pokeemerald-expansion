@ First persistent clue of the Eclipse mystery. The player can revisit this researcher.
EryonBosque_EventScript_Researcher::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonBosque_EventScript_ResearcherFollowup
	msgbox EryonBosque_Text_Researcher, MSGBOX_DEFAULT
	setvar VAR_ERYON_LUMINA_CLUE_FOUND, 1
	msgbox EryonBosque_Text_ClueFound, MSGBOX_DEFAULT
	release
	end

EryonBosque_EventScript_ResearcherFollowup::
	msgbox EryonBosque_Text_ResearcherFollowup, MSGBOX_DEFAULT
	release
	end

EryonBosque_Text_Researcher:
	.string "PESQUISADOR: Que estranho...\p"
	.string "Os Pokemon daqui estao agitados.\p"
	.string "Encontrei uma marca em forma de\n"
	.string "eclipse nas pedras antigas.$"

EryonBosque_Text_ClueFound:
	.string "Voce observou a marca!\p"
	.string "Alguem esteve aqui antes de nos.\n"
	.string "Procure respostas em Verdelume.$"

EryonBosque_Text_ResearcherFollowup:
	.string "A marca de eclipse ainda esta\n"
	.string "aqui. Nao e um sinal natural.\p"
	.string "Converse com o povo de Verdelume.$"

@ A separate encounter hints at human interference without revealing the villains yet.
EryonBosque_EventScript_SilentTraveler::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonBosque_EventScript_TravelerAfterClue
	msgbox EryonBosque_Text_TravelerBeforeClue, MSGBOX_DEFAULT
	release
	end

EryonBosque_EventScript_TravelerAfterClue::
	msgbox EryonBosque_Text_TravelerAfterClue, MSGBOX_DEFAULT
	release
	end

EryonBosque_Text_TravelerBeforeClue:
	.string "VIAJANTE: Nao siga as luzes\n"
	.string "que surgem ao anoitecer.\p"
	.string "Vi pessoas levando caixas para\n"
	.string "dentro da mata. Estranho, nao?$"

EryonBosque_Text_TravelerAfterClue:
	.string "VIAJANTE: A marca nas pedras?\p"
	.string "As caixas tinham o mesmo sinal.\n"
	.string "Nao pareciam pesquisadores.$"

@ Environmental clue on an old stone, accessible independently of the researcher.
EryonBosque_EventScript_AncientStone::
	lock
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonBosque_EventScript_StoneRecognized
	msgbox EryonBosque_Text_StoneUnknown, MSGBOX_DEFAULT
	release
	end

EryonBosque_EventScript_StoneRecognized::
	msgbox EryonBosque_Text_StoneRecognized, MSGBOX_DEFAULT
	release
	end

EryonBosque_Text_StoneUnknown:
	.string "Uma pedra coberta de musgo.\p"
	.string "Ha um circulo dividido em\n"
	.string "duas metades na superficie.$"

EryonBosque_Text_StoneRecognized:
	.string "E a mesma marca mencionada\n"
	.string "pelo pesquisador.\p"
	.string "Quem deixou esse simbolo aqui?$"

@ Optional one-time supply cache. A full bag does not consume the reward.
EryonBosque_EventScript_SupplyCache::
	lock
	goto_if_ge VAR_ERYON_LUMINA_SUPPLY_FOUND, 1, EryonBosque_EventScript_EmptyCache
	msgbox EryonBosque_Text_SupplyCache, MSGBOX_DEFAULT
	giveitem ITEM_POTION
	goto_if_eq VAR_RESULT, FALSE, EryonBosque_EventScript_CacheBagFull
	setvar VAR_ERYON_LUMINA_SUPPLY_FOUND, 1
	release
	end

EryonBosque_EventScript_CacheBagFull::
	msgbox EryonBosque_Text_CacheBagFull, MSGBOX_DEFAULT
	release
	end

EryonBosque_EventScript_EmptyCache::
	msgbox EryonBosque_Text_EmptyCache, MSGBOX_DEFAULT
	release
	end

EryonBosque_Text_SupplyCache:
	.string "Entre as raizes ha uma pequena\n"
	.string "caixa de suprimentos esquecida.$"

EryonBosque_Text_CacheBagFull:
	.string "Sua bolsa esta cheia.\n"
	.string "A caixa ficara aqui.$"

EryonBosque_Text_EmptyCache:
	.string "A caixa esta vazia.\n"
	.string "Alguem a deixou ha muito tempo.$"
