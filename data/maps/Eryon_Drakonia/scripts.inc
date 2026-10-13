Eryon_Drakonia_MapScripts::
	.byte 0

@ Eighth gym city: dragon sanctuary and Eclipse transmission terminus.
EryonDrakonia_EventScript_Caretaker::
	lock
	faceplayer
	msgbox EryonDrakonia_Text_Caretaker, MSGBOX_DEFAULT
	special HealPlayerParty
	release
	end

EryonDrakonia_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonDrakonia_EventScript_GymGuideInformed
	msgbox EryonDrakonia_Text_GymGuideBefore, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_GymGuideInformed::
	msgbox EryonDrakonia_Text_GymGuideInformed, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_Sage::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_STAR_CHART_READ, EryonDrakonia_EventScript_SageAfterChart
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonDrakonia_EventScript_SageClue
	msgbox EryonDrakonia_Text_SageBefore, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_SageClue::
	msgbox EryonDrakonia_Text_SageClue, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_SageAfterChart::
	msgbox EryonDrakonia_Text_SageAfterChart, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_RuneResearcher::
	lock
	faceplayer
	msgbox EryonDrakonia_Text_Researcher, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_EclipseAgent::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonDrakonia_EventScript_EclipseAgentExposed
	msgbox EryonDrakonia_Text_AgentBefore, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_EclipseAgentExposed::
	msgbox EryonDrakonia_Text_AgentExposed, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_SanctuaryMarker::
	lock
	msgbox EryonDrakonia_Text_Sanctuary, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_LeagueNotice::
	lock
	msgbox EryonDrakonia_Text_League, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_Text_Caretaker:
	.string "SOCORRISTA: Voce chegou\n"
	.string "ao alto da montanha!\p"
	.string "Vou curar sua equipe\n"
	.string "antes de explorar.$"

EryonDrakonia_Text_GymGuideBefore:
	.string "GUIA: DRAKONIA e a\n"
	.string "cidade do oitavo GINASIO.\p"
	.string "Aqui treinamos Pokemon\n"
	.string "do tipo DRAGAO.$"

EryonDrakonia_Text_GymGuideInformed:
	.string "GUIA: O lider protege\n"
	.string "o santuario sagrado.\p"
	.string "O desafio ainda esta\n"
	.string "suspenso pela ECLIPSE.$"

EryonDrakonia_Text_SageBefore:
	.string "ANCIA: O santuario\n"
	.string "guarda um canto antigo.\p"
	.string "Os dragoes escutam\n"
	.string "o som da montanha.$"

EryonDrakonia_Text_SageClue:
	.string "ANCIA: A ECLIPSE quer\n"
	.string "usar nosso santuario!\p"
	.string "Os cristais ecoam de\n"
	.string "SOLARIS ate DRAKONIA.$"

EryonDrakonia_Text_Researcher:
	.string "PESQUISADOR: As runas\n"
	.string "registram a energia.\p"
	.string "O ultimo pulso veio\n"
	.string "pela VILA DO PICO.$"

EryonDrakonia_Text_AgentBefore:
	.string "TECNICO: Estou vendo\n"
	.string "a rede de energia.\p"
	.string "Nao preciso da ajuda\n"
	.string "de um treinador.$"

EryonDrakonia_Text_AgentExposed:
	.string "ECLIPSE: Nosso plano\n"
	.string "chegou a DRAKONIA!\p"
	.string "O santuario e a chave\n"
	.string "para ativar a rede.$"

EryonDrakonia_Text_Sanctuary:
	.string "SANTUARIO DOS DRAGOES:\n"
	.string "entrada em manutencao.\p"
	.string "Os guardioes estudam\n"
	.string "as pedras antigas.$"

EryonDrakonia_Text_League:
	.string "LESTE: GRUTA DAS ESTRELAS.\n"
	.string "Depois, CAMINHO DA LIGA.\p"
	.string "Travessia a pe;\n"
	.string "nenhuma HM e exigida.$"

EryonDrakonia_Text_SageAfterChart:
	.string "ANCIA: Voce decifrou\n"
	.string "a carta das estrelas!\p"
	.string "Os cristais de ERYON\n"
	.string "nao devem ser forjados.$"
