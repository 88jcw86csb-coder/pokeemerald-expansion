@ Eryon Route 03: the eastern trail, following Kael's first badge.
@ The route is exploratory; the next area is not yet connected.
EryonRota03_EventScript_Prospector::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonRota03_EventScript_ProspectorBadge
	msgbox EryonRota03_Text_ProspectorBefore, MSGBOX_DEFAULT
	release
	end

EryonRota03_EventScript_ProspectorBadge::
	msgbox EryonRota03_Text_ProspectorBadge, MSGBOX_DEFAULT
	release
	end

EryonRota03_EventScript_Traveler::
	lock
	faceplayer
	msgbox EryonRota03_Text_Traveler, MSGBOX_DEFAULT
	release
	end

EryonRota03_EventScript_CrystalTracks::
	lock
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonRota03_EventScript_CrystalTracksBadge
	msgbox EryonRota03_Text_CrystalTracksBefore, MSGBOX_DEFAULT
	release
	end

EryonRota03_EventScript_CrystalTracksBadge::
	msgbox EryonRota03_Text_CrystalTracksBadge, MSGBOX_DEFAULT
	release
	end

EryonRota03_Text_ProspectorBefore:
	.string "GARIMPEIRO: A trilha do leste\n"
	.string "leva ate as pedras antigas.\p"
	.string "Ha pegadas de gente que nao\n"
	.string "costuma passar por aqui.$"

EryonRota03_Text_ProspectorBadge:
	.string "GARIMPEIRO: Kael lhe deu\n"
	.string "a primeira insignia?\p"
	.string "Entao observe estas marcas:\n"
	.string "as carrocas levavam cristais.$"

EryonRota03_Text_Traveler:
	.string "VIAJANTE: A estrada e longa.\p"
	.string "Os caminhos de pedra escondem\n"
	.string "historias muito antigas.$"

EryonRota03_Text_CrystalTracksBefore:
	.string "Ha riscos profundos no solo.\p"
	.string "Parecem marcas de rodas\n"
	.string "carregadas de pedras.$"

EryonRota03_Text_CrystalTracksBadge:
	.string "Entre os rastros de rodas\n"
	.string "ha um po que brilha.\p"
	.string "As pedras tem um desenho\n"
	.string "parecido com um eclipse.$"

EryonRota03_EventScript_Scout::
	lock
	faceplayer
	msgbox EryonRota03_Text_Scout, MSGBOX_DEFAULT
	release
	end

EryonRota03_Text_Scout:
	.string "ESCOTEIRO: Vi marcas de pneus\n"
	.string "perto da encosta.\p"
	.string "O caminho de pedra parece\n"
	.string "ficar mais estreito adiante.$"

EryonRota03_EventScript_Researcher::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonRota03_EventScript_ResearcherBadge
	msgbox EryonRota03_Text_Researcher, MSGBOX_DEFAULT
	release
	end

EryonRota03_EventScript_ResearcherBadge::
	msgbox EryonRota03_Text_ResearcherBadge, MSGBOX_DEFAULT
	release
	end

EryonRota03_Text_Researcher:
	.string "PESQUISADORA: Estas rochas\n"
	.string "guardam sinais antigos.\p"
	.string "Ainda nao sei sua origem.$"

EryonRota03_Text_ResearcherBadge:
	.string "PESQUISADORA: Kael confirmou\n"
	.string "as marcas do eclipse?\p"
	.string "Encontrei cristais parecidos\n"
	.string "nas pegadas das carrocas.$"
