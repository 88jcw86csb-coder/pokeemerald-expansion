Eryon_GrutaDasEstrelas_MapScripts::
	.byte 0

@ An on-foot passage with no mandatory field moves. The chart is optional.
EryonEstrelas_EventScript_TrailEngineer::
	lock
	faceplayer
	msgbox EryonEstrelas_Text_TrailEngineer, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_EclipseScout::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, EryonEstrelas_EventScript_ScoutRelayOff
	goto_if_set FLAG_ERYON_GROTTO_ECLIPSE_SCOUT_DEFEATED, EryonEstrelas_EventScript_ScoutDefeated
	goto_if_set FLAG_ERYON_STAR_CHART_READ, EryonEstrelas_EventScript_ScoutBattleOffer
	msgbox EryonEstrelas_Text_ScoutBefore, MSGBOX_DEFAULT
	release
	end

@ Optional battle only after the chart is decoded; disabling the relay remains possible without battle.
EryonEstrelas_EventScript_ScoutBattleOffer::
	msgbox EryonEstrelas_Text_ScoutBattleOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonEstrelas_EventScript_ScoutDecline
	closemessage
	trainerbattle_single TRAINER_ERYON_GROTTO_ECLIPSE, EryonEstrelas_Text_ScoutIntro, EryonEstrelas_Text_ScoutLoss, EryonEstrelas_EventScript_ScoutVictory, FALSE
	msgbox EryonEstrelas_Text_ScoutDefeated, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_ScoutDecline::
	closemessage
	msgbox EryonEstrelas_Text_ScoutDecline, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_ScoutVictory::
	msgbox EryonEstrelas_Text_ScoutVictory, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_ScoutDefeated::
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonEstrelas_EventScript_ScoutAfterReport
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, EryonEstrelas_EventScript_ScoutManifest
	msgbox EryonEstrelas_Text_ScoutDefeated, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_ScoutRelayOff::
	msgbox EryonEstrelas_Text_ScoutRelayOff, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_ScoutAfterChart::
	msgbox EryonEstrelas_Text_ScoutAfter, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_Astronomer::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonEstrelas_EventScript_AstronomerChampion
	goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN, EryonEstrelas_EventScript_AstronomerPeace
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonEstrelas_EventScript_AstronomerEvidence
	goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, EryonEstrelas_EventScript_AstronomerRelayOff
	goto_if_set FLAG_ERYON_STAR_CHART_READ, EryonEstrelas_EventScript_AstronomerAfterChart
	msgbox EryonEstrelas_Text_AstronomerBefore, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_AstronomerAfterChart::
	msgbox EryonEstrelas_Text_AstronomerAfter, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_StarChart::
	lock
	goto_if_set FLAG_ERYON_STAR_CHART_READ, EryonEstrelas_EventScript_StarChartRead
	msgbox EryonEstrelas_Text_ChartBefore, MSGBOX_DEFAULT
	setflag FLAG_ERYON_STAR_CHART_READ
	msgbox EryonEstrelas_Text_ChartDiscovery, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_StarChartRead::
	msgbox EryonEstrelas_Text_ChartRepeat, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_OldBridge::
	lock
	msgbox EryonEstrelas_Text_Bridge, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_Text_TrailEngineer:
	.string "ENGENHEIRO: Abrimos\n"
	.string "uma passagem a pe!\p"
	.string "Nao precisa de CUT,\n"
	.string "STRENGTH ou ROCK SMASH.$"

EryonEstrelas_Text_ScoutBefore:
	.string "ECLIPSE: Nao toque\n"
	.string "naquelas estrelas!\p"
	.string "Os cristais pertencem\n"
	.string "ao nosso projeto.$"

EryonEstrelas_Text_ScoutAfter:
	.string "ECLIPSE: Leu o mapa?\n"
	.string "Nosso chefe vai saber!\p"
	.string "Ha uma rota ate a LIGA\n"
	.string "alem deste tunel.$"

EryonEstrelas_Text_AstronomerBefore:
	.string "ASTRONOMA: Uma carta\n"
	.string "celeste fica na gruta.\p"
	.string "Ela revela a origem\n"
	.string "dos sinais antigos.$"

EryonEstrelas_Text_AstronomerAfter:
	.string "ASTRONOMA: A carta\n"
	.string "mostra a rede ECLIPSE.\p"
	.string "O verdadeiro eco\n"
	.string "nao pode ser forjado.$"

EryonEstrelas_Text_ChartBefore:
	.string "Pedras iluminadas\n"
	.string "formam uma constelacao.\p"
	.string "Voce decifra a carta\n"
	.string "sem usar nenhuma HM.$"

EryonEstrelas_Text_ChartDiscovery:
	.string "A ECLIPSE ligou SOLARIS\n"
	.string "a DRAKONIA por cristais!\p"
	.string "O caminho da LIGA\n"
	.string "pode revelar a verdade.$"

EryonEstrelas_Text_ChartRepeat:
	.string "A carta celeste\n"
	.string "continua brilhando.\p"
	.string "Sua descoberta ficou\n"
	.string "registrada na memoria.$"

EryonEstrelas_Text_Bridge:
	.string "PONTE DE MADEIRA:\n"
	.string "passagem segura a pe.\p"
	.string "O desvio evita pedras\n"
	.string "e blocos quebraveis.$"

@ The cave expedition ties the Solaris/Drakonia crystal network to the League.
@ Optional lore event: reading the chart remains optional and no HM is required.
EryonEstrelas_EventScript_ExpeditionArchivist::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN, EryonEstrelas_EventScript_ArchivistPeace
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonEstrelas_EventScript_ArchivistReported
	goto_if_set FLAG_ERYON_STAR_CHART_READ, EryonEstrelas_EventScript_ArchivistAfter
	msgbox EryonEstrelas_Text_ArchivistBefore, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_ArchivistAfter::
	msgbox EryonEstrelas_Text_ArchivistAfter, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_Text_ArchivistBefore:
	.string "ARQUIVISTA: A gruta\n"
	.string "guarda mapas antigos.\p"
	.string "Os cristais brilham\n"
	.string "quando o ceu muda.\p"
	.string "Observe a carta no\n"
	.string "fundo da caverna.$"

EryonEstrelas_Text_ArchivistAfter:
	.string "ARQUIVISTA: Entao\n"
	.string "voce leu a carta!\p"
	.string "SOLARIS e DRAKONIA\n"
	.string "fazem parte de uma\n"
	.string "mesma rede antiga.\p"
	.string "Leve essa descoberta\n"
	.string "ate a CIDADE DA LIGA.$"

@ Eclipse scouts retreat from their cave outpost when the shipment network is exposed.
EryonEstrelas_EventScript_ScoutManifest::
	msgbox EryonEstrelas_Text_ScoutManifest, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_ScoutAfterReport::
	msgbox EryonEstrelas_Text_ScoutAfterReport, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_Text_ScoutManifest:
	.string "ECLIPSE: Esse papel\n"
	.string "e o manifesto?!\p"
	.string "O transporte era\n"
	.string "segredo da equipe.$"

EryonEstrelas_Text_ScoutAfterReport:
	.string "ECLIPSE: A LIGA\n"
	.string "descobriu nossas\n"
	.string "rotas de cristais!\p"
	.string "Esta gruta ja nao\n"
	.string "e um esconderijo.$"

EryonEstrelas_EventScript_ArchivistReported::
	msgbox EryonEstrelas_Text_ArchivistReported, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_Text_ArchivistReported:
	.string "ARQUIVISTA: A LIGA\n"
	.string "arquivou suas provas!\p"
	.string "Agora podemos estudar\n"
	.string "esta gruta sem medo\n"
	.string "dos agentes ECLIPSE.$"

@ Optional interaction after discovering the Star Chart. Shutdown is persistent.
EryonEstrelas_EventScript_RelayConsole::
	lock
	goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, EryonEstrelas_EventScript_RelayOff
	goto_if_unset FLAG_ERYON_STAR_CHART_READ, EryonEstrelas_EventScript_RelayUnknown
	msgbox EryonEstrelas_Text_RelayPrompt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonEstrelas_EventScript_RelayLeave
	closemessage
	setflag FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED
	msgbox EryonEstrelas_Text_RelayDisabled, MSGBOX_DEFAULT
	special HealPlayerParty
	release
	end

EryonEstrelas_EventScript_RelayUnknown::
	msgbox EryonEstrelas_Text_RelayUnknown, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_RelayOff::
	msgbox EryonEstrelas_Text_RelayOff, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonEstrelas_EventScript_RelayLeave
	closemessage
	special HealPlayerParty
	msgbox EryonEstrelas_Text_RelayRestored, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_RelayLeave::
	closemessage
	release
	end

EryonEstrelas_Text_RelayPrompt:
	.string "Terminal da ECLIPSE.\p"
	.string "A Carta Estelar revela\n"
	.string "o codigo de acesso.\p"
	.string "Desligar o transmissor?$"

EryonEstrelas_Text_RelayDisabled:
	.string "Transmissor desligado!\p"
	.string "Os cristais param\n"
	.string "de emitir sinais.\p"
	.string "A gruta fica em paz.$"

EryonEstrelas_Text_RelayUnknown:
	.string "Um terminal estranho.\p"
	.string "Ha um codigo celeste\n"
	.string "que voce nao conhece.$"

EryonEstrelas_Text_RelayOff:
	.string "O transmissor esta\n"
	.string "inativo e seguro.\p"
	.string "Usar sua energia para\n"
	.string "curar seus Pokemon?$"

EryonEstrelas_Text_RelayRestored:
	.string "A energia limpa\n"
	.string "recuperou seus Pokemon!$"


EryonEstrelas_Text_ScoutBattleOffer:
	.string "ECLIPSE: Decifrou\n"
	.string "a Carta Estelar?!\p"
	.string "Vamos resolver isso\n"
	.string "num duelo Pokemon?$"

EryonEstrelas_Text_ScoutIntro:
	.string "ECLIPSE: Nosso sinal\n"
	.string "nao sera interrompido!$"

EryonEstrelas_Text_ScoutLoss:
	.string "ECLIPSE: Voce venceu\n"
	.string "minha equipe?!$"

EryonEstrelas_Text_ScoutVictory:
	.string "ECLIPSE: O terminal\n"
	.string "fica atras da gruta!\p"
	.string "Mas nao pense que\n"
	.string "derrotou a organizacao.$"

EryonEstrelas_Text_ScoutDefeated:
	.string "ECLIPSE: Ja perdi!\p"
	.string "Nao vou impedir\n"
	.string "sua investigacao.$"

EryonEstrelas_Text_ScoutDecline:
	.string "ECLIPSE: Entao\n"
	.string "nao atrapalhe a equipe!$"

EryonEstrelas_Text_ScoutRelayOff:
	.string "ECLIPSE: Voce cortou\n"
	.string "o sinal da antena?!\p"
	.string "Vamos ter de recuar.$"


@ Original upper Star Gallery: a navigable detour connecting the northern
@ crystal chamber to the eastern tunnel, outside the League's mandatory route.
@ Existing story flags only: never blocks travel or awards a duplicate item.
EryonEstrelas_EventScript_ResonanceGallery::
	lock
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonEstrelas_EventScript_GalleryReported
	goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, EryonEstrelas_EventScript_GallerySilent
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, EryonEstrelas_EventScript_GalleryManifest
	msgbox EryonEstrelas_Text_GalleryBefore, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_GalleryReported::
	msgbox EryonEstrelas_Text_GalleryReported, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_GallerySilent::
	msgbox EryonEstrelas_Text_GallerySilent, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_GalleryManifest::
	msgbox EryonEstrelas_Text_GalleryManifest, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_Text_GalleryBefore:
	.string "CAMARA ESTELAR:\p"
	.string "Os cristais da parede\n"
	.string "cantam em dois tons.\p"
	.string "Uma passagem curva\n"
	.string "leva ate a gruta leste.$"

EryonEstrelas_Text_GalleryManifest:
	.string "Marcas das cargas\n"
	.string "ECLIPSE brilham aqui!\p"
	.string "LUNARIS e DRAKONIA\n"
	.string "surgem gravadas na rocha.$"

EryonEstrelas_Text_GallerySilent:
	.string "Os cristais nao emitem\n"
	.string "mais pulsos artificiais.\p"
	.string "Um brilho suave ilumina\n"
	.string "a galeria silenciosa.$"

EryonEstrelas_Text_GalleryReported:
	.string "CAMARA ESTELAR:\p"
	.string "A LIGA recebeu provas\n"
	.string "da rede da ECLIPSE.\p"
	.string "Os ecos antigos\n"
	.string "voltam a ser ouvidos.$"


@ A side alcove on the newly connected lower bypass. Existing progress flags
@ change its description, without any reward or new mandatory battle.
EryonEstrelas_EventScript_ResonanceAlcove::
	lock
	goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, EryonEstrelas_EventScript_AlcoveQuiet
	goto_if_set FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED, EryonEstrelas_EventScript_AlcoveArchive
	msgbox EryonEstrelas_Text_AlcoveBefore, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_AlcoveArchive:
	msgbox EryonEstrelas_Text_AlcoveArchive, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_AlcoveQuiet:
	msgbox EryonEstrelas_Text_AlcoveQuiet, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_Text_AlcoveBefore:
	.string "Cristais se cruzam\n"
	.string "em dois tons distintos.\p"
	.string "Um deles parece vir\n"
	.string "de uma maquina distante.$"

EryonEstrelas_Text_AlcoveArchive:
	.string "O arquivo dos ECOS\n"
	.string "combina com estas marcas!\p"
	.string "O sinal da ECLIPSE\n"
	.string "imita o som natural.$"

EryonEstrelas_Text_AlcoveQuiet:
	.string "Os cristais desta\n"
	.string "galeria silenciaram.\p"
	.string "O transmissor ECLIPSE\n"
	.string "ja nao distorce o eco.$"


@ Existing cave astronomer follows changes after the relay shutdown and League events.
@ Dialogue-only epilogue: no new rewards, battles, map warps, or progression flags.
EryonEstrelas_EventScript_AstronomerRelayOff::
	msgbox EryonEstrelas_Text_AstronomerRelayOff, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_AstronomerEvidence::
	msgbox EryonEstrelas_Text_AstronomerEvidence, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_AstronomerChampion::
	goto_if_set FLAG_ERYON_ECLIPSE_NETWORK_SHUT_DOWN, EryonEstrelas_EventScript_AstronomerChampionPeace
	msgbox EryonEstrelas_Text_AstronomerChampion, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_Text_AstronomerRelayOff:
	.string "ASTRONOMA: O sinal\n"
	.string "artificial se apagou!\p"
	.string "Agora podemos ouvir\n"
	.string "o eco das estrelas.$"

EryonEstrelas_Text_AstronomerEvidence:
	.string "ASTRONOMA: A LIGA\n"
	.string "recebeu suas provas!\p"
	.string "Os mapas da ECLIPSE\n"
	.string "serao investigados.$"

EryonEstrelas_Text_AstronomerChampion:
	.string "ASTRONOMA: O CAMPEAO\n"
	.string "voltou a esta gruta!\p"
	.string "A historia de ERYON\n"
	.string "segue alem da LIGA.$"

@ The old cavern researchers confirm the restoration from Drakonia.
@ This is a dialogue-only consequence of the existing finale flag.
EryonEstrelas_EventScript_AstronomerPeace::
	msgbox EryonEstrelas_Text_AstronomerPeace, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_AstronomerChampionPeace::
	msgbox EryonEstrelas_Text_AstronomerChampionPeace, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_ArchivistPeace::
	msgbox EryonEstrelas_Text_ArchivistPeace, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_Text_AstronomerPeace:
	.string "ASTRONOMA: As estrelas\n"
	.string "voltaram a brilhar!\p"
	.string "A rede ECLIPSE caiu\n"
	.string "em DRAKONIA.\p"
	.string "A gruta guarda apenas\n"
	.string "seus ecos naturais.$"

EryonEstrelas_Text_AstronomerChampionPeace:
	.string "ASTRONOMA: CAMPEAO!\p"
	.string "Voce venceu a LIGA\n"
	.string "e protegeu as estrelas.\p"
	.string "As runas desta gruta\n"
	.string "contarao sua historia.$"

EryonEstrelas_Text_ArchivistPeace:
	.string "ARQUIVISTA: A LIGA\n"
	.string "confirmou a paz!\p"
	.string "Os registros ECLIPSE\n"
	.string "agora sao historia.\p"
	.string "Os cristais continuam\n"
	.string "aqui para estudo.$"
