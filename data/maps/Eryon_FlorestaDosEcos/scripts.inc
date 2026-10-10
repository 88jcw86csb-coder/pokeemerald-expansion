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
