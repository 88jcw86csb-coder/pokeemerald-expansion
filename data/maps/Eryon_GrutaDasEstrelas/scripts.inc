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
	goto_if_set FLAG_ERYON_STAR_CHART_READ, EryonEstrelas_EventScript_ScoutAfterChart
	msgbox EryonEstrelas_Text_ScoutBefore, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_ScoutAfterChart::
	msgbox EryonEstrelas_Text_ScoutAfter, MSGBOX_DEFAULT
	release
	end

EryonEstrelas_EventScript_Astronomer::
	lock
	faceplayer
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
