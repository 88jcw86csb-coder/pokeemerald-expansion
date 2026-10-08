@ First persistent clue of the Eclipse mystery. The player can revisit this researcher.
EryonBosque_EventScript_Researcher::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonBosque_EventScript_ResearcherKnownClue
	msgbox EryonBosque_Text_Researcher, MSGBOX_DEFAULT
	setvar VAR_ERYON_LUMINA_CLUE_FOUND, 1
	msgbox EryonBosque_Text_ClueFound, MSGBOX_DEFAULT
	release
	end

EryonBosque_EventScript_ResearcherKnownClue::
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonBosque_EventScript_ResearcherAfterBadge
	goto EryonBosque_EventScript_ResearcherFollowup

EryonBosque_EventScript_ResearcherAfterBadge::
	msgbox EryonBosque_Text_ResearcherAfterBadge, MSGBOX_DEFAULT
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

EryonBosque_Text_ResearcherAfterBadge:
	.string "PESQUISADOR: Kael contou que\n"
	.string "voce ganhou sua insignia!\p"
	.string "Comparei a marca com desenhos\n"
	.string "de antigos mapas da regiao.\p"
	.string "Ela parece indicar um caminho,\n"
	.string "mas ainda faltam pistas.$"

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

@ The stone independently unlocks the forest clue, even if the researcher is skipped.
EryonBosque_EventScript_AncientStone::
	lock
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonBosque_EventScript_StoneRecognized
	msgbox EryonBosque_Text_StoneUnknown, MSGBOX_DEFAULT
	setvar VAR_ERYON_LUMINA_CLUE_FOUND, 1
	msgbox EryonBosque_Text_StoneDiscovery, MSGBOX_DEFAULT
	release
	end

EryonBosque_EventScript_StoneRecognized::
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonBosque_EventScript_StoneAfterBadge
	msgbox EryonBosque_Text_StoneRecognized, MSGBOX_DEFAULT
	release
	end

@ Returning after the first badge reveals an environmental clue,
@ without requiring an item or locking the next part of the story.
EryonBosque_EventScript_StoneAfterBadge::
	msgbox EryonBosque_Text_StoneAfterBadge, MSGBOX_DEFAULT
	release
	end

EryonBosque_Text_StoneUnknown:
	.string "Uma pedra coberta de musgo.\p"
	.string "Ha um circulo dividido em\n"
	.string "duas metades na superficie.$"

EryonBosque_Text_StoneDiscovery:
	.string "Voce examinou a marca!\p"
	.string "O simbolo parece recente.\n"
	.string "Alguem esteve aqui.$"

EryonBosque_Text_StoneAfterBadge:
	.string "Ha flores novas entre as\n"
	.string "rachaduras da pedra.\p"
	.string "O simbolo do eclipse parece\n"
	.string "mais nitido do que antes.\p"
	.string "Talvez a botanica de\n"
	.string "Verdelume saiba explicar.$"

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

@ A suspicious observer foreshadows Team Eclipse without revealing their identity.
@ This optional encounter does not set story flags or block exploration.
EryonBosque_EventScript_EclipseScout::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonBosque_EventScript_EclipseScoutAfterBadge
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonBosque_EventScript_EclipseScoutAfterClue
	msgbox EryonBosque_Text_EclipseScoutBeforeClue, MSGBOX_DEFAULT
	release
	end

EryonBosque_EventScript_EclipseScoutAfterClue::
	trainerbattle_single TRAINER_ERYON_SCOUT, EryonBosque_Text_EclipseScoutChallenge, EryonBosque_Text_EclipseScoutDefeat, EryonBosque_EventScript_EclipseScoutVictory, FALSE
	msgbox EryonBosque_Text_EclipseScoutAfterClue, MSGBOX_DEFAULT
	release
	end

EryonBosque_EventScript_EclipseScoutVictory::
	msgbox EryonBosque_Text_EclipseScoutVictory, MSGBOX_DEFAULT
	release
	end

@ The optional battle remains available even if Kael was defeated first.
EryonBosque_EventScript_EclipseScoutAfterBadge::
	trainerbattle_single TRAINER_ERYON_SCOUT, EryonBosque_Text_EclipseScoutChallenge, EryonBosque_Text_EclipseScoutDefeat, EryonBosque_EventScript_EclipseScoutVictory, FALSE
	msgbox EryonBosque_Text_EclipseScoutAfterBadge, MSGBOX_DEFAULT
	release
	end

EryonBosque_Text_EclipseScoutBeforeClue:
	.string "ESTRANHO: Procurando luzes?\p"
	.string "Algumas coisas da floresta\n"
	.string "devem continuar escondidas.$"

EryonBosque_Text_EclipseScoutAfterClue:
	.string "ESTRANHO: Voce viu o simbolo?\p"
	.string "Entao ja sabe demais...\p"
	.string "Esqueca o que encontrou.$"

EryonBosque_Text_EclipseScoutAfterBadge:
	.string "ESTRANHO: Kael se envolveu?\p"
	.string "Isso complica nossos planos...\p"
	.string "Nao ouviu nada. Entendido?$"

EryonBosque_Text_EclipseScoutChallenge:
	.string "ESTRANHO: Nao vai embora?\p"
	.string "Entao vou fazer voce desistir!$"

EryonBosque_Text_EclipseScoutDefeat:
	.string "Como conseguiu me vencer?!$"

EryonBosque_Text_EclipseScoutVictory:
	.string "ESTRANHO: Nao devia ter\n"
	.string "chamado tanta atencao...\p"
	.string "Nao conte isso a ninguem.$"
