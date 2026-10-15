Eryon_TrilhaLunar_MapScripts::
	.byte 0

@ The old lunar observations explain why Eclipse follows the ancient song.
EryonLunar_EventScript_Astronomer::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonLunar_EventScript_AstronomerClue
	msgbox EryonLunar_Text_AstronomerBefore, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_AstronomerClue::
	msgbox EryonLunar_Text_AstronomerClue, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_Watchman::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_ECHO_TRACE_RECORDED, EryonLunar_EventScript_WatchmanTrace
	msgbox EryonLunar_Text_Watchman, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_EclipseSurveyor::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonLunar_EventScript_EclipseSurveyorExposed
	msgbox EryonLunar_Text_SurveyorBefore, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_EclipseSurveyorExposed::
	msgbox EryonLunar_Text_SurveyorExposed, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_MoonMarker::
	lock
	goto_if_set FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED, EryonLunar_EventScript_MoonMarkerArchive
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonLunar_EventScript_MoonMarkerClue
	msgbox EryonLunar_Text_MoonMarkerBefore, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_MoonMarkerClue::
	msgbox EryonLunar_Text_MoonMarkerClue, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_ClosedPass::
	lock
	msgbox EryonLunar_Text_ClosedPass, MSGBOX_DEFAULT
	release
	end

EryonLunar_Text_AstronomerBefore:
	.string "ASTRONOMA: As pedras\n"
	.string "guardam um velho canto.\p"
	.string "A LUA muda a forma\n"
	.string "como elas respondem.$"

EryonLunar_Text_AstronomerClue:
	.string "ASTRONOMA: Os pulsos\n"
	.string "de IGNIVAR vieram ate ca.\p"
	.string "A ECLIPSE quer forcar\n"
	.string "o canto dos cristais.$"

EryonLunar_Text_Watchman:
	.string "VIGIA: A trilha passa\n"
	.string "por claros e bosques.\p"
	.string "LUNARIS fica adiante,\n"
	.string "use o desvio leste.$"

EryonLunar_Text_SurveyorBefore:
	.string "TECNICO: O observatorio\n"
	.string "esta em reparos.\p"
	.string "A area leste segue\n"
	.string "aberta sob vigilancia.$"

EryonLunar_Text_SurveyorExposed:
	.string "ECLIPSE: O arquivo da\n"
	.string "aldeia revelou a rota!\p"
	.string "Um sinal maior deve\n"
	.string "surgir em LUNARIS.$"

EryonLunar_Text_MoonMarkerBefore:
	.string "Uma pedra polida\n"
	.string "mostra fases da LUA.\p"
	.string "Uma melodia baixa\n"
	.string "parece vir da terra.$"

EryonLunar_Text_MoonMarkerClue:
	.string "O selo da ECLIPSE\n"
	.string "esta sob a pedra.\p"
	.string "Um desenho aponta\n"
	.string "para LUNARIS.$"

EryonLunar_Text_ClosedPass:
	.string "PONTE EM MANUTENCAO!\n"
	.string "Desvio para LUNARIS aberto.\p"
	.string "Os viajantes podem\n"
	.string "seguir pela trilha.$"

@ Optional chart connects Echo Valley, its village archive, and Lunaris.
EryonLunar_EventScript_StarCalibration::
	lock
	goto_if_set FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED, EryonLunar_EventScript_StarCalibrationComplete
	goto_if_set FLAG_ERYON_ECHO_TRACE_RECORDED, EryonLunar_EventScript_StarCalibrationPending
	msgbox EryonLunar_Text_StarCalibrationBefore, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_StarCalibrationPending::
	msgbox EryonLunar_Text_StarCalibrationPending, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_StarCalibrationComplete::
	msgbox EryonLunar_Text_StarCalibrationComplete, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_WatchmanTrace::
	msgbox EryonLunar_Text_WatchmanTrace, MSGBOX_DEFAULT
	release
	end

EryonLunar_Text_StarCalibrationBefore:
	.string "MARCADOR ESTELAR:\n"
	.string "Este disco segue a LUA.\p"
	.string "O vale ainda nao tem\n"
	.string "dados registrados.$"

EryonLunar_Text_StarCalibrationPending:
	.string "MARCADOR ESTELAR:\n"
	.string "O som do vale aponta\n"
	.string "para o OBSERVATORIO.\p"
	.string "Consulte antes o\n"
	.string "ARQUIVO DA ALDEIA.$"

EryonLunar_Text_StarCalibrationComplete:
	.string "MARCADOR ESTELAR:\n"
	.string "A frequencia natural\n"
	.string "e a da ECLIPSE diferem.\p"
	.string "LUNARIS pode comparar\n"
	.string "ambos os sinais.$"

EryonLunar_Text_WatchmanTrace:
	.string "VIGIA: O ARQUIVO\n"
	.string "precisa de sua prova!\p"
	.string "Depois siga a LUNARIS\n"
	.string "pela trilha leste.$"

@ The existing lunar marker reveals a new chapter after the optional archive delivery.
@ No new flag, item, trainer or badge state is introduced.
EryonLunar_EventScript_MoonMarkerArchive:
	goto_if_set FLAG_BADGE07_GET, EryonLunar_EventScript_MoonMarkerBadge
	msgbox EryonLunar_Text_MoonMarkerArchive, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_MoonMarkerBadge:
	msgbox EryonLunar_Text_MoonMarkerBadge, MSGBOX_DEFAULT
	release
	end

EryonLunar_Text_MoonMarkerArchive:
	.string "O registro da ALDEIA\n"
	.string "faz o disco ressoar!\p"
	.string "As marcas indicam que\n"
	.string "a ECLIPSE mudou o sinal.\p"
	.string "A ASTRONOMA de LUNARIS\n"
	.string "pode comparar os dados.$"

EryonLunar_Text_MoonMarkerBadge:
	.string "A 7a INSIGNIA brilha\n"
	.string "diante do disco lunar.\p"
	.string "Um novo padrao aponta\n"
	.string "para DRAKONIA.\p"
	.string "A jornada continua\n"
	.string "pela TRILHA DOS DRAGOES.$"

@ Moonfall Sanctuary: an optional southward expedition, west of Lunaris.
@ Reading the receiver makes a wild Inkay visible; no Gym/warp locks.
EryonLunar_EventScript_MoonfallArray::
	lock
	goto_if_set FLAG_ERYON_LUNAR_ARRAY_READ, EryonLunar_EventScript_MoonfallArrayAgain
	goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN, EryonLunar_EventScript_MoonfallArrayPeace
	goto_if_set FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED, EryonLunar_EventScript_MoonfallArrayArchive
	msgbox EryonLunar_Text_MoonfallArrayBefore, MSGBOX_DEFAULT
	setflag FLAG_ERYON_LUNAR_ARRAY_READ
	release
	end

EryonLunar_EventScript_MoonfallArrayArchive::
	msgbox EryonLunar_Text_MoonfallArrayArchive, MSGBOX_DEFAULT
	setflag FLAG_ERYON_LUNAR_ARRAY_READ
	release
	end

EryonLunar_EventScript_MoonfallArrayPeace::
	msgbox EryonLunar_Text_MoonfallArrayPeace, MSGBOX_DEFAULT
	setflag FLAG_ERYON_LUNAR_ARRAY_READ
	release
	end

EryonLunar_EventScript_MoonfallArrayAgain::
	goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN, EryonLunar_EventScript_MoonfallArrayAfterPeace
	msgbox EryonLunar_Text_MoonfallArrayAgain, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_MoonfallArrayAfterPeace::
	msgbox EryonLunar_Text_MoonfallArrayAfterPeace, MSGBOX_DEFAULT
	release
	end

@ Standard wild encounter: capture or knock-out persists; escape permits retry.
EryonLunar_EventScript_InkayPool::
	lock
	goto_if_set FLAG_ERYON_LUNAR_INKAY_RESOLVED, EryonLunar_EventScript_InkayQuiet
	goto_if_unset FLAG_ERYON_LUNAR_ARRAY_READ, EryonLunar_EventScript_InkayHidden
	msgbox EryonLunar_Text_InkayOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonLunar_EventScript_InkayLeave
	closemessage
	setwildbattle SPECIES_INKAY, 45
	waitse
	playmoncry SPECIES_INKAY, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, EryonLunar_EventScript_InkayResolved
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, EryonLunar_EventScript_InkayResolved
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, EryonLunar_EventScript_InkayEscaped
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, EryonLunar_EventScript_InkayEscaped
	release
	end

EryonLunar_EventScript_InkayResolved::
	setflag FLAG_ERYON_LUNAR_INKAY_RESOLVED
	msgbox EryonLunar_Text_InkayResolved, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_InkayHidden::
	msgbox EryonLunar_Text_InkayHidden, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_InkayEscaped::
	msgbox EryonLunar_Text_InkayEscaped, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_InkayQuiet::
	msgbox EryonLunar_Text_InkayQuiet, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_InkayLeave::
	closemessage
	release
	end

@ Reusable interaction after full Bag: only successful gift saves flag.
EryonLunar_EventScript_MoonfallSupplies::
	lock
	goto_if_set FLAG_ERYON_LUNAR_SUPPLIES_TAKEN, EryonLunar_EventScript_MoonfallEmpty
	goto_if_unset FLAG_ERYON_LUNAR_INKAY_RESOLVED, EryonLunar_EventScript_MoonfallSealed
	msgbox EryonLunar_Text_MoonfallSupplies, MSGBOX_DEFAULT
	giveitem ITEM_MAX_REVIVE
	goto_if_eq VAR_RESULT, FALSE, EryonLunar_EventScript_MoonfallBagFull
	setflag FLAG_ERYON_LUNAR_SUPPLIES_TAKEN
	release
	end

EryonLunar_EventScript_MoonfallSealed::
	msgbox EryonLunar_Text_MoonfallSealed, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_MoonfallBagFull::
	msgbox EryonLunar_Text_MoonfallBagFull, MSGBOX_DEFAULT
	release
	end

EryonLunar_EventScript_MoonfallEmpty::
	msgbox EryonLunar_Text_MoonfallEmpty, MSGBOX_DEFAULT
	release
	end

EryonLunar_Text_MoonfallArrayBefore:
	.string "SANTUARIO LUNAR:\p"
	.string "Um antigo receptor\n"
	.string "capta ecos da ECLIPSE.\p"
	.string "O brilho segue para\n"
	.string "o lago entre rochas.$"

EryonLunar_Text_MoonfallArrayArchive:
	.string "SANTUARIO LUNAR:\p"
	.string "Os dados da ALDEIA\n"
	.string "explicam estes ecos!\p"
	.string "O aparelho compara\n"
	.string "luz lunar e cristais.$"

EryonLunar_Text_MoonfallArrayPeace:
	.string "SANTUARIO LUNAR:\p"
	.string "REDE ECLIPSE INATIVA!\p"
	.string "O receptor capta\n"
	.string "apenas a luz da LUA.$"

EryonLunar_Text_MoonfallArrayAgain:
	.string "O receptor aponta\n"
	.string "para a agua ao sul.\p"
	.string "Um Pokemon observa\n"
	.string "o reflexo da LUA.$"

EryonLunar_Text_MoonfallArrayAfterPeace:
	.string "O eco artificial\n"
	.string "desapareceu da trilha.\p"
	.string "As pedras naturais\n"
	.string "brilham novamente.$"

EryonLunar_Text_InkayHidden:
	.string "Algo se move na agua.\p"
	.string "Leia o receptor\n"
	.string "lunar primeiro.$"

EryonLunar_Text_InkayOffer:
	.string "Um INKAY gira sobre\n"
	.string "a agua iluminada!\p"
	.string "Investigar de perto?$"

EryonLunar_Text_InkayResolved:
	.string "INKAY sumiu entre\n"
	.string "os reflexos da LUA.\p"
	.string "O lago esta tranquilo.$"

EryonLunar_Text_InkayEscaped:
	.string "INKAY nadou para\n"
	.string "uma caverna pequena.\p"
	.string "Pode voltar depois.$"

EryonLunar_Text_InkayQuiet:
	.string "A agua agora reflete\n"
	.string "apenas as estrelas.$"

EryonLunar_Text_MoonfallSealed:
	.string "Uma caixa protegida\n"
	.string "por cristais lunares.\p"
	.string "INKAY segue observando.$"

EryonLunar_Text_MoonfallSupplies:
	.string "CAIXA DO SANTUARIO:\p"
	.string "Um MAX REVIVE ficou\n"
	.string "guardado aqui.$"

EryonLunar_Text_MoonfallBagFull:
	.string "Sua BOLSA esta cheia!\p"
	.string "O item ficara na\n"
	.string "caixa ate sua volta.$"

EryonLunar_Text_MoonfallEmpty:
	.string "A caixa de suprimentos\n"
	.string "esta vazia.$"
