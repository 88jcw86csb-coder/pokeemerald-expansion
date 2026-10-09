Eryon_Rota03_MapScripts::
	.byte 0

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
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonRota03_EventScript_ResearcherSerraClue
	msgbox EryonRota03_Text_ResearcherBadge, MSGBOX_DEFAULT
	release
	end

EryonRota03_EventScript_ResearcherSerraClue::
	msgbox EryonRota03_Text_ResearcherSerraClue, MSGBOX_DEFAULT
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

EryonRota03_Text_ResearcherSerraClue:
	.string "PESQUISADORA: Voce achou\n"
	.string "um acampamento na serra?\p"
	.string "Os fragmentos de cristal\n"
	.string "parecem ter vindo de la.\p"
	.string "Vou comparar as amostras\n"
	.string "antes de seguir a trilha.$"

@ Optional field medic: repeatable healing before the rocky trail.
EryonRota03_EventScript_FieldMedic::
	lock
	faceplayer
	msgbox EryonRota03_Text_FieldMedicOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonRota03_EventScript_FieldMedicDecline
	special HealPlayerParty
	msgbox EryonRota03_Text_FieldMedicHealed, MSGBOX_DEFAULT
	release
	end

EryonRota03_EventScript_FieldMedicDecline::
	msgbox EryonRota03_Text_FieldMedicDecline, MSGBOX_DEFAULT
	release
	end

EryonRota03_Text_FieldMedicOffer:
	.string "SOCORRISTA: Esta trilha\n"
	.string "pode ser cansativa.\p"
	.string "Quer que eu cuide de seus\n"
	.string "Pokemon antes de seguir?$"

EryonRota03_Text_FieldMedicHealed:
	.string "Pronto! Sua equipe esta\n"
	.string "recuperada. Boa viagem!$"

EryonRota03_Text_FieldMedicDecline:
	.string "Tudo bem. Estarei aqui\n"
	.string "se precisar de ajuda.$"

@ The eastern ridge foreshadows the next rocky area.
EryonRota03_EventScript_RockGuide::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonRota03_EventScript_RockGuideBadge
	msgbox EryonRota03_Text_RockGuideBefore, MSGBOX_DEFAULT
	release
	end

EryonRota03_EventScript_RockGuideBadge::
	msgbox EryonRota03_Text_RockGuideBadge, MSGBOX_DEFAULT
	release
	end

EryonRota03_EventScript_CaravanDebris::
	lock
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonRota03_EventScript_CaravanDebrisBadge
	msgbox EryonRota03_Text_CaravanDebrisBefore, MSGBOX_DEFAULT
	release
	end

EryonRota03_EventScript_CaravanDebrisBadge::
	msgbox EryonRota03_Text_CaravanDebrisBadge, MSGBOX_DEFAULT
	release
	end

EryonRota03_Text_RockGuideBefore:
	.string "GUIA: As pedras desta trilha\n"
	.string "ficam perigosas na chuva.\p"
	.string "Volte a Verdelume se sua\n"
	.string "equipe precisar descansar.$"

EryonRota03_Text_RockGuideBadge:
	.string "GUIA: Voce derrotou Kael!\p"
	.string "Os rastros das carrocas\n"
	.string "seguem ate a serra.\p"
	.string "Alguem transportou pedras\n"
	.string "durante a madrugada.$"

EryonRota03_Text_CaravanDebrisBefore:
	.string "Um pedaco de madeira foi\n"
	.string "deixado perto da estrada.\p"
	.string "Parece parte de uma carroca.$"

EryonRota03_Text_CaravanDebrisBadge:
	.string "A madeira tem um desenho\n"
	.string "que lembra um eclipse.\p"
	.string "Ha pequenos cristais presos\n"
	.string "nas rachaduras.$"

EryonRota03_EventScript_Ranger::
	lock
	faceplayer
	trainerbattle_single TRAINER_ERYON_ROUTE03_RANGER, EryonRota03_Text_TrainerChallenge, EryonRota03_Text_TrainerDefeat, EryonRota03_EventScript_TrainerVictory, FALSE
	msgbox EryonRota03_Text_TrainerAfter, MSGBOX_DEFAULT
	release
	end

EryonRota03_EventScript_TrainerVictory::
	msgbox EryonRota03_Text_TrainerAfter, MSGBOX_DEFAULT
	release
	end

EryonRota03_Text_TrainerChallenge:
	.string "RANGER LIA: A trilha fica\n"
	.string "mais dificil daqui em diante.$"

EryonRota03_Text_TrainerDefeat:
	.string "LIA: Fui derrotada!$"

EryonRota03_Text_TrainerAfter:
	.string "LIA: Boa batalha!\n"
	.string "Sua equipe esta preparada.$"
