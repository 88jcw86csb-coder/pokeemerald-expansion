Eryon_FlorestaDosEcos_MapScripts::
	.byte 0

@ Interference from Ignivar makes the forest sing with unnatural echoes.
EryonEcos_EventScript_Researcher::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonEcos_EventScript_ResearcherClue
	msgbox EryonEcos_Text_ResearcherBefore, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_ResearcherClue::
	msgbox EryonEcos_Text_ResearcherClue, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_EclipseObserver::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonEcos_EventScript_EclipseObserverClue
	msgbox EryonEcos_Text_ObserverBefore, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_EclipseObserverClue::
	msgbox EryonEcos_Text_ObserverClue, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_ResonantStone::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonEcos_EventScript_ResonantStoneClue
	msgbox EryonEcos_Text_StoneBefore, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_ResonantStoneClue::
	msgbox EryonEcos_Text_StoneClue, MSGBOX_DEFAULT
	release
	end

EryonEcos_Text_ResearcherBefore:
	.string "PESQUISADORA: O vento\n"
	.string "faz as arvores ecoarem.\p"
	.string "Mas hoje o som vem\n"
	.string "debaixo do solo.$"

EryonEcos_Text_ResearcherClue:
	.string "PESQUISADORA: A rede de\n"
	.string "Ignivar afeta a floresta!\p"
	.string "Uma frequencia estranha\n"
	.string "altera o canto Pokemon.$"

EryonEcos_Text_ObserverBefore:
	.string "VIAJANTE: Os ecos daqui\n"
	.string "sao quase musicais.\p"
	.string "Nao procure a origem\n"
	.string "dos sons a noite.$"

EryonEcos_Text_ObserverClue:
	.string "ECLIPSE: A frequencia\n"
	.string "de Ignivar chegou aqui!\p"
	.string "Logo a floresta toda\n"
	.string "vai responder ao sinal.$"

EryonEcos_Text_StoneBefore:
	.string "Uma rocha vibra quando\n"
	.string "o vento muda de direcao.\p"
	.string "Ha marcas antigas\n"
	.string "sob o musgo.$"

EryonEcos_Text_StoneClue:
	.string "O cristal da rocha\n"
	.string "responde ao sinal.\p"
	.string "As marcas apontam\n"
	.string "para ALDEIA DOS ECOS.$"

@ Additional local witness to the Eclipse signal crossing Eryon.
EryonEcos_EventScript_ForestRanger::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_FOREST_PHANTUMP_RESOLVED, EryonEcos_EventScript_RangerGroveSafe
	goto_if_set FLAG_ERYON_FOREST_SIGNAL_LOG_READ, EryonEcos_EventScript_RangerLogFound
	msgbox EryonEcos_Text_ForestRanger, MSGBOX_DEFAULT
	release
	end

EryonEcos_Text_ForestRanger:
	.string "GUARDA: Pokemon se agitam\n"
	.string "quando o sinal toca.\p"
	.string "Procure as pedras que\n"
	.string "vibram junto ao vento.$"

@ Regional aftermath of Eclipse's transmission experiment.
EryonEcos_EventScript_SignalSurveyor::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonEcos_EventScript_SignalSurveyorInformed
	msgbox EryonEcos_Text_SignalSurveyorBefore, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_SignalSurveyorInformed::
	msgbox EryonEcos_Text_SignalSurveyor, MSGBOX_DEFAULT
	release
	end

EryonEcos_Text_SignalSurveyorBefore:
	.string "MORADOR: A cidade e\n"
	.string "a floresta mudaram.\p"
	.string "Ha um ruido estranho\n"
	.string "perto das trilhas.$"

EryonEcos_Text_SignalSurveyor:
	.string "TECNICO: Os cristais\n"
	.string "reagem em sequencia.\p"
	.string "O ultimo pulso segue\n"
	.string "alem destas arvores.$"

@ Investigation stations along the eastern forest path.
EryonEcos_EventScript_CableJunction::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonEcos_EventScript_CableJunctionClue
	msgbox EryonEcos_Text_CableJunctionBefore, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_CableJunctionClue::
	msgbox EryonEcos_Text_CableJunctionClue, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_OldTrailSign::
	lock
	msgbox EryonEcos_Text_OldTrailSign, MSGBOX_DEFAULT
	release
	end

EryonEcos_Text_CableJunctionBefore:
	.string "Um cabo escuro surge\n"
	.string "entre as raizes.\p"
	.string "Ha pegadas recentes\n"
	.string "junto a trilha.$"

EryonEcos_Text_CableJunctionClue:
	.string "A marca ECLIPSE esta\n"
	.string "gravada no conector.\p"
	.string "O fio segue para alem\n"
	.string "da floresta.$"

EryonEcos_Text_OldTrailSign:
	.string "TRILHA DOS ECOS:\n"
	.string "Siga as pedras antigas.\p"
	.string "A aldeia fica adiante,\n"
	.string "apos o vale.$"

@ The eastern survey gives the player a concrete objective before leaving
@ the forest. This encounter deliberately uses the existing Serra clue.
EryonEcos_EventScript_EasternSurvey::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonEcos_EventScript_EasternSurveyInformed
	msgbox EryonEcos_Text_EasternSurveyBefore, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_EasternSurveyInformed::
	msgbox EryonEcos_Text_EasternSurveyInformed, MSGBOX_DEFAULT
	release
	end

EryonEcos_Text_EasternSurveyBefore:
	.string "VIGIA: O vale adiante\n"
	.string "esta cheio de ecos.\p"
	.string "Os moradores pediram\n"
	.string "ajuda em Ignivar.$"

EryonEcos_Text_EasternSurveyInformed:
	.string "VIGIA: A ECLIPSE ligou\n"
	.string "os cabos as pedras!\p"
	.string "Precisamos avisar a\n"
	.string "ALDEIA DOS ECOS.$"

@ Makes the expedition sustainable while pursuing Eclipse through the woods.
EryonEcos_EventScript_RescueMedic::
	lock
	faceplayer
	msgbox EryonEcos_Text_RescueMedic, MSGBOX_DEFAULT
	special HealPlayerParty
	release
	end

EryonEcos_Text_RescueMedic:
	.string "SOCORRISTA: Os ecos\n"
	.string "assustam os viajantes.\p"
	.string "Vou recuperar sua equipe\n"
	.string "antes da proxima trilha.$"

@ A second clue extends the investigation beyond simple dialogue.
EryonEcos_EventScript_RelayRecord::
	lock
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonEcos_EventScript_RelayRecordExposed
	msgbox EryonEcos_Text_RelayRecordHidden, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_RelayRecordExposed::
	msgbox EryonEcos_Text_RelayRecordExposed, MSGBOX_DEFAULT
	release
	end

EryonEcos_Text_RelayRecordHidden:
	.string "Um pequeno terminal\n"
	.string "esta coberto de musgo.\p"
	.string "O visor mostra uma\n"
	.string "onda interrompida.$"

EryonEcos_Text_RelayRecordExposed:
	.string "TERMINAL ECLIPSE:\n"
	.string "Rede SOLARIS-IGNIVAR.\p"
	.string "Proximo ponto: VALE\n"
	.string "DOS ECOS. Sinal ativo.$"

@ North-canopy grove: the original east/west route never requires this detour.
EryonEcos_EventScript_CanopyLog::
	lock
	goto_if_set FLAG_ERYON_FOREST_SIGNAL_LOG_READ, EryonEcos_EventScript_LogRepeat
	goto_if_set FLAG_ERYON_RIVER_SAMPLE_RECORDED, EryonEcos_EventScript_LogRiver
	msgbox EryonEcos_Text_LogFirst, MSGBOX_DEFAULT
	setflag FLAG_ERYON_FOREST_SIGNAL_LOG_READ
	release
	end

EryonEcos_EventScript_LogRiver::
	msgbox EryonEcos_Text_LogRiver, MSGBOX_DEFAULT
	setflag FLAG_ERYON_FOREST_SIGNAL_LOG_READ
	release
	end

EryonEcos_EventScript_LogRepeat::
	msgbox EryonEcos_Text_LogRepeat, MSGBOX_DEFAULT
	release
	end

@ Victory or capture persists; flee, teleport and decline permit retries.
@ Uses the regular wild battle and EXP routines.
EryonEcos_EventScript_PhantumpNest::
	lock
	goto_if_set FLAG_ERYON_FOREST_PHANTUMP_RESOLVED, EryonEcos_EventScript_PhantumpQuiet
	goto_if_unset FLAG_ERYON_FOREST_SIGNAL_LOG_READ, EryonEcos_EventScript_PhantumpHidden
	msgbox EryonEcos_Text_PhantumpOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonEcos_EventScript_PhantumpLeave
	closemessage
	setwildbattle SPECIES_PHANTUMP, 40
	waitse
	playmoncry SPECIES_PHANTUMP, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, EryonEcos_EventScript_PhantumpResolved
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, EryonEcos_EventScript_PhantumpResolved
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, EryonEcos_EventScript_PhantumpEscaped
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, EryonEcos_EventScript_PhantumpEscaped
	release
	end

EryonEcos_EventScript_PhantumpResolved::
	setflag FLAG_ERYON_FOREST_PHANTUMP_RESOLVED
	msgbox EryonEcos_Text_PhantumpResolved, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_PhantumpEscaped::
	msgbox EryonEcos_Text_PhantumpEscaped, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_PhantumpHidden::
	msgbox EryonEcos_Text_PhantumpHidden, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_PhantumpQuiet::
	msgbox EryonEcos_Text_PhantumpQuiet, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_PhantumpLeave::
	closemessage
	release
	end

@ The one-time Dusk Ball is not consumed if the Bag is full.
EryonEcos_EventScript_GroveCache::
	lock
	goto_if_set FLAG_ERYON_FOREST_GROVE_CACHE_TAKEN, EryonEcos_EventScript_GroveCacheEmpty
	goto_if_unset FLAG_ERYON_FOREST_PHANTUMP_RESOLVED, EryonEcos_EventScript_GroveCacheSealed
	msgbox EryonEcos_Text_GroveCacheOffer, MSGBOX_DEFAULT
	giveitem ITEM_DUSK_BALL
	goto_if_eq VAR_RESULT, FALSE, EryonEcos_EventScript_GroveCacheFull
	setflag FLAG_ERYON_FOREST_GROVE_CACHE_TAKEN
	release
	end

EryonEcos_EventScript_GroveCacheSealed::
	msgbox EryonEcos_Text_GroveCacheSealed, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_GroveCacheFull::
	msgbox EryonEcos_Text_GroveCacheFull, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_GroveCacheEmpty::
	msgbox EryonEcos_Text_GroveCacheEmpty, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_RangerLogFound::
	msgbox EryonEcos_Text_RangerLogFound, MSGBOX_DEFAULT
	release
	end

EryonEcos_EventScript_RangerGroveSafe::
	msgbox EryonEcos_Text_RangerGroveSafe, MSGBOX_DEFAULT
	release
	end

EryonEcos_Text_LogFirst:
	.string "CADERNO DA COPA:\p"
	.string "A ECLIPSE alterou\n"
	.string "o eco das arvores.\p"
	.string "Ha um sinal estranho\n"
	.string "escondido na mata.$"

EryonEcos_Text_LogRiver:
	.string "CADERNO DA COPA:\p"
	.string "A amostra do rio\n"
	.string "confirma esta energia!\p"
	.string "SOLARIS enviou pulsos\n"
	.string "para IGNIVAR.$"

EryonEcos_Text_LogRepeat:
	.string "O caderno aponta\n"
	.string "para uma clareira.\p"
	.string "Um Pokemon precisa\n"
	.string "de ajuda por perto.$"

EryonEcos_Text_PhantumpHidden:
	.string "As folhas se movem.\p"
	.string "Leia o caderno da\n"
	.string "copa primeiro.$"

EryonEcos_Text_PhantumpOffer:
	.string "Um PHANTUMP assustado\n"
	.string "surge das raizes!\p"
	.string "Investigar de perto?$"

EryonEcos_Text_PhantumpResolved:
	.string "PHANTUMP se acalmou!\p"
	.string "Os ecos naturais\n"
	.string "voltaram a floresta.$"

EryonEcos_Text_PhantumpEscaped:
	.string "PHANTUMP voltou para\n"
	.string "dentro das arvores.\p"
	.string "Pode retornar depois.$"

EryonEcos_Text_PhantumpQuiet:
	.string "A clareira esta\n"
	.string "silenciosa agora.$"

EryonEcos_Text_GroveCacheSealed:
	.string "Uma bolsa esquecida\n"
	.string "esta nas folhas.\p"
	.string "PHANTUMP vigia aqui.$"

EryonEcos_Text_GroveCacheOffer:
	.string "BOLSA DA FLORESTA:\p"
	.string "Uma DUSK BALL ficou\n"
	.string "guardada nas folhas.$"

EryonEcos_Text_GroveCacheFull:
	.string "Sua BOLSA esta cheia!\p"
	.string "O item ficara aqui\n"
	.string "ate voce voltar.$"

EryonEcos_Text_GroveCacheEmpty:
	.string "A bolsa antiga\n"
	.string "esta vazia.$"

EryonEcos_Text_RangerLogFound:
	.string "GUARDA: Voce leu o\n"
	.string "CADERNO DA COPA!\p"
	.string "Procure o PHANTUMP\n"
	.string "na clareira ao norte.$"

EryonEcos_Text_RangerGroveSafe:
	.string "GUARDA: A clareira\n"
	.string "voltou a ter paz!\p"
	.string "PHANTUMP evolui\n"
	.string "no nivel 36.$"
