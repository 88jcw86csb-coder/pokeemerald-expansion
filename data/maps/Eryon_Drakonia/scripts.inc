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
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonDrakonia_EventScript_SageEvidenceReported
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, EryonDrakonia_EventScript_SageManifest
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
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_NOIBAT_RESOLVED, EryonDrakonia_EventScript_ResearcherNoibat
	goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, EryonDrakonia_EventScript_ResearcherRelayOff
	msgbox EryonDrakonia_Text_Researcher, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_EclipseAgent::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_DRAKONIA_ECLIPSE_DEFEATED, EryonDrakonia_EventScript_AgentAfterBattle
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonDrakonia_EventScript_AgentBattleOffer
	msgbox EryonDrakonia_Text_AgentBefore, MSGBOX_DEFAULT
	release
	end

@ The showdown is optional, offered only after the mountain investigation.
@ Losing follows normal trainer whiteout and payment rules.
EryonDrakonia_EventScript_AgentBattleOffer::
	msgbox EryonDrakonia_Text_AgentChallenge, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonDrakonia_EventScript_AgentDecline
	closemessage
	trainerbattle_single TRAINER_ERYON_DRAKONIA_ECLIPSE, EryonDrakonia_Text_AgentIntro, EryonDrakonia_Text_AgentLoss, EryonDrakonia_EventScript_AgentVictory, FALSE
	msgbox EryonDrakonia_Text_AgentAfter, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_AgentDecline::
	closemessage
	msgbox EryonDrakonia_Text_AgentDecline, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_AgentVictory::
	msgbox EryonDrakonia_Text_AgentVictory, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_AgentAfterBattle::
	msgbox EryonDrakonia_Text_AgentAfter, MSGBOX_DEFAULT
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

@ The dragon city reacts to the Star Chart discovery without blocking exploration.
EryonDrakonia_EventScript_SanctuaryHistorian::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_GROTTO_ECLIPSE_SCOUT_DEFEATED, EryonDrakonia_EventScript_HistorianScoutVictory
	goto_if_set FLAG_ERYON_STAR_CHART_READ, EryonDrakonia_EventScript_HistorianAfter
	msgbox EryonDrakonia_Text_HistorianBefore, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_HistorianAfter::
	msgbox EryonDrakonia_Text_HistorianAfter, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_Courier::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_COURIER_DEFEATED, EryonDrakonia_EventScript_CourierEscortBeaten
	goto_if_set FLAG_ERYON_QUALIFIED, EryonDrakonia_EventScript_CourierAfter
	msgbox EryonDrakonia_Text_CourierBefore, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_CourierAfter::
	msgbox EryonDrakonia_Text_CourierAfter, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_Text_HistorianBefore:
	.string "HISTORIADOR: As runas\n"
	.string "de DRAKONIA apontam\n"
	.string "para a gruta a leste.\p"
	.string "A ECLIPSE deseja usar\n"
	.string "seu poder antigo.$"

EryonDrakonia_Text_HistorianAfter:
	.string "HISTORIADOR: A carta\n"
	.string "mostra o plano deles!\p"
	.string "Os sinais vao ate\n"
	.string "a CIDADE DA LIGA.\p"
	.string "Avise os guardioes\n"
	.string "antes do torneio.$"

EryonDrakonia_Text_CourierBefore:
	.string "MENSAGEIRA: A estrada\n"
	.string "da LIGA segue pela\n"
	.string "GRUTA DAS ESTRELAS.\p"
	.string "Toda a travessia\n"
	.string "e possivel a pe.$"

EryonDrakonia_Text_CourierAfter:
	.string "MENSAGEIRA: Voce\n"
	.string "venceu oito duelos!\p"
	.string "Os guardioes torcem\n"
	.string "pela sua vitoria.$"

@ The disguised technician reacts once the player knows the crystal network.
EryonDrakonia_EventScript_EclipseAgentChart::
	msgbox EryonDrakonia_Text_AgentChart, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_Text_AgentChart:
	.string "ECLIPSE: Voce leu\n"
	.string "a Carta Estelar?!\p"
	.string "Entao sabe que nossa\n"
	.string "rede chega ate a LIGA.\p"
	.string "Nao vai conseguir\n"
	.string "parar a transmissao!$"

@ The mountain shipment evidence reaches the dragon sanctuary.
EryonDrakonia_EventScript_SageManifest::
	msgbox EryonDrakonia_Text_SageManifest, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_Text_SageManifest:
	.string "ANCIA: Voce trouxe\n"
	.string "o manifesto da trilha!\p"
	.string "As cargas da ECLIPSE\n"
	.string "vinham de LUNARIS.\p"
	.string "Vou alertar os\n"
	.string "guardioes do santuario.$"

@ Authorities at the League inform Drakonia after the player files the evidence.
EryonDrakonia_EventScript_SageEvidenceReported::
	msgbox EryonDrakonia_Text_SageEvidenceReported, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_Text_SageEvidenceReported:
	.string "ANCIA: A LIGA recebeu\n"
	.string "seu manifesto ECLIPSE!\p"
	.string "Os guardioes reforcaram\n"
	.string "a vigia do santuario.\p"
	.string "Agora podemos estudar\n"
	.string "os cristais com calma.$"

@ The sanctuary's measurements respond to the disabled cave transmitter.
EryonDrakonia_EventScript_ResearcherRelayOff::
	msgbox EryonDrakonia_Text_ResearcherRelayOff, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_Text_ResearcherRelayOff:
	.string "PESQUISADOR: O pulso\n"
	.string "da gruta desapareceu!\p"
	.string "Agora os cristais\n"
	.string "voltam ao ritmo normal.\p"
	.string "A ECLIPSE perdeu uma\n"
	.string "parte da sua rede.$"


@ After the cave confrontation, the formerly isolated historian connects the event to the sanctuary.
EryonDrakonia_EventScript_HistorianScoutVictory::
	msgbox EryonDrakonia_Text_HistorianScoutVictory, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_Text_HistorianScoutVictory:
	.string "HISTORIADOR: Um agente\n"
	.string "da ECLIPSE caiu na gruta!\p"
	.string "Os guardioes agora\n"
	.string "podem proteger as runas.\p"
	.string "Leve sua vitoria\n"
	.string "a Cidade da Liga.$"


@ Optional crystal shipment depot on Drakonia's southeast plateau.
@ No forced battle; winning against the commander unlocks supplies.
EryonDrakonia_EventScript_EclipseDepot::
	lock
	goto_if_set FLAG_ERYON_DRAKONIA_DEPOT_SUPPLIES_TAKEN, EryonDrakonia_EventScript_DepotEmpty
	goto_if_unset FLAG_ERYON_DRAKONIA_ECLIPSE_DEFEATED, EryonDrakonia_EventScript_DepotSealed
	msgbox EryonDrakonia_Text_DepotOpen, MSGBOX_DEFAULT
	giveitem ITEM_MAX_REVIVE
	goto_if_eq VAR_RESULT, FALSE, EryonDrakonia_EventScript_DepotBagFull
	setflag FLAG_ERYON_DRAKONIA_DEPOT_SUPPLIES_TAKEN
	release
	end

EryonDrakonia_EventScript_DepotSealed::
	msgbox EryonDrakonia_Text_DepotSealed, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_DepotBagFull::
	msgbox EryonDrakonia_Text_DepotBagFull, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_DepotEmpty::
	msgbox EryonDrakonia_Text_DepotEmpty, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_Text_AgentChallenge:
	.string "ECLIPSE: Os cristais\n"
	.string "do santuario sao nossos!\p"
	.string "Quer enfrentar o\n"
	.string "comandante da operacao?$"

EryonDrakonia_Text_AgentIntro:
	.string "ECLIPSE: O poder das\n"
	.string "runas nao sera seu!$"

EryonDrakonia_Text_AgentLoss:
	.string "ECLIPSE: Nao esperava\n"
	.string "perder aqui!$"

EryonDrakonia_Text_AgentVictory:
	.string "ECLIPSE: Meu posto\n"
	.string "caiu em DRAKONIA!\p"
	.string "O deposito no sudeste\n"
	.string "esta abandonado.$"

EryonDrakonia_Text_AgentDecline:
	.string "ECLIPSE: Entao saia\n"
	.string "do meu caminho.$"

EryonDrakonia_Text_AgentAfter:
	.string "ECLIPSE: Recolhemos\n"
	.string "o que restou.\p"
	.string "Va ao deposito se\n"
	.string "quiser. Nos recuamos.$"

EryonDrakonia_Text_DepotSealed:
	.string "DEPOSITO DA ECLIPSE:\p"
	.string "Caixas lacradas pelo\n"
	.string "comandante de DRAKONIA.$"

EryonDrakonia_Text_DepotOpen:
	.string "As caixas abandonadas\n"
	.string "contem suprimentos!\p"
	.string "Um MAX REVIVE esta\n"
	.string "no fundo do deposito.$"

EryonDrakonia_Text_DepotBagFull:
	.string "A BOLSA esta cheia!\p"
	.string "O remedio pode ser\n"
	.string "retirado depois.$"

EryonDrakonia_Text_DepotEmpty:
	.string "As caixas foram\n"
	.string "revistadas. Estao vazias.$"


@ The dragon sanctuary is alerted to the stopped Eclipse shipments.
EryonDrakonia_EventScript_CourierEscortBeaten::
	msgbox EryonDrakonia_Text_CourierEscortBeaten, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_Text_CourierEscortBeaten:
	.string "MENSAGEIRO: Recebemos\n"
	.string "a noticia da escolta!\p"
	.string "A ECLIPSE perdeu sua\n"
	.string "carga na trilha oeste.\p"
	.string "Os guardioes do pico\n"
	.string "ja estao avisados.$"


@ The dragon sanctuary receives ecological findings from the northern cliff.
EryonDrakonia_EventScript_ResearcherNoibat::
	msgbox EryonDrakonia_Text_ResearcherNoibat, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_Text_ResearcherNoibat:
	.string "PESQUISADOR: Um NOIBAT\n"
	.string "foi observado na trilha!\p"
	.string "O eco das asas ajuda\n"
	.string "a localizar cristais.\p"
	.string "O santuario ira\n"
	.string "proteger esse habitat.$"


@ Ancient dragon sanctuary: optional Kalos-compatible Axew encounter.
@ Defeating the local Eclipse commander calms the shrine enough to approach.
@ Catch/defeat is saved; fleeing or teleporting does not consume the encounter.
EryonDrakonia_EventScript_AxewShrine::
	lock
	goto_if_set FLAG_ERYON_DRAKONIA_AXEW_RESOLVED, EryonDrakonia_EventScript_AxewShrineQuiet
	goto_if_unset FLAG_ERYON_DRAKONIA_ECLIPSE_DEFEATED, EryonDrakonia_EventScript_AxewShrineDisturbed
	msgbox EryonDrakonia_Text_AxewShrineOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonDrakonia_EventScript_AxewShrineLeave
	closemessage
	setwildbattle SPECIES_AXEW, 42
	waitse
	playmoncry SPECIES_AXEW, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, EryonDrakonia_EventScript_AxewShrineResolved
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, EryonDrakonia_EventScript_AxewShrineResolved
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, EryonDrakonia_EventScript_AxewShrineEscaped
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, EryonDrakonia_EventScript_AxewShrineEscaped
	release
	end

EryonDrakonia_EventScript_AxewShrineResolved::
	setflag FLAG_ERYON_DRAKONIA_AXEW_RESOLVED
	msgbox EryonDrakonia_Text_AxewShrineResolved, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_AxewShrineDisturbed::
	msgbox EryonDrakonia_Text_AxewShrineDisturbed, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_AxewShrineEscaped::
	msgbox EryonDrakonia_Text_AxewShrineEscaped, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_AxewShrineQuiet::
	msgbox EryonDrakonia_Text_AxewShrineQuiet, MSGBOX_DEFAULT
	release
	end

EryonDrakonia_EventScript_AxewShrineLeave::
	closemessage
	release
	end

EryonDrakonia_Text_AxewShrineOffer:
	.string "Um pequeno dragao\n"
	.string "surge das ruinas!\p"
	.string "E um AXEW selvagem!\p"
	.string "Aproximar-se dele?$"

EryonDrakonia_Text_AxewShrineDisturbed:
	.string "RUINAS DOS DRAGOES:\p"
	.string "Cristais da ECLIPSE\n"
	.string "assustam os Pokemon.\p"
	.string "Derrote o comandante\n"
	.string "para acalmar a area.$"

EryonDrakonia_Text_AxewShrineEscaped:
	.string "AXEW correu para\n"
	.string "tras de uma pedra!\p"
	.string "Ele pode voltar\n"
	.string "em outra visita.$"

EryonDrakonia_Text_AxewShrineResolved:
	.string "O encontro terminou.\p"
	.string "O santuario agora\n"
	.string "descansa em silencio.$"

EryonDrakonia_Text_AxewShrineQuiet:
	.string "As ruinas estao\n"
	.string "quietas novamente.\p"
	.string "Nao ha Pokemon\n"
	.string "aqui por enquanto.$"
