Eryon_CidadeDaLiga_MapScripts::
	.byte 0

EryonCidadeLiga_EventScript_Medic::
	lock
	faceplayer
	msgbox EryonCidadeLiga_Text_Medic, MSGBOX_DEFAULT
	special HealPlayerParty
	release
	end

EryonCidadeLiga_EventScript_Guide::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, EryonCidadeLiga_EventScript_GuideRelayOff
	msgbox EryonCidadeLiga_Text_Guide, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_Fan::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonCidadeLiga_EventScript_FanChampion
	msgbox EryonCidadeLiga_Text_Fan, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_PlazaSign::
	lock
	msgbox EryonCidadeLiga_Text_CitySign, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_Notice::
	lock
	msgbox EryonCidadeLiga_Text_Notice, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_Text_Medic:
	.string "SOCORRISTA: Bem-vindo\n"
	.string "a CIDADE DA LIGA!\p"
	.string "Vou restaurar sua\n"
	.string "equipe Pokemon.$"

EryonCidadeLiga_Text_Guide:
	.string "GUIA: O grande edificio\n"
	.string "fica no CENTRO da cidade.\p"
	.string "Primeiro, oito batalhas\n"
	.string "da CLASSIFICATORIA.$"

EryonCidadeLiga_Text_Fan:
	.string "TORCEDORA: Uma derrota\n"
	.string "zera sua sequencia.\p"
	.string "Guarde dinheiro antes\n"
	.string "de entrar na arena!$"

EryonCidadeLiga_Text_CitySign:
	.string "CIDADE DA LIGA DE ERYON.\n"
	.string "PRACA DA COMPETICAO.\p"
	.string "O edificio da LIGA\n"
	.string "fica nesta praca.$"

EryonCidadeLiga_Text_Notice:
	.string "TORNEIO DA LIGA:\n"
	.string "8 duelos consecutivos.\p"
	.string "Venca, cure sua equipe\n"
	.string "e siga para a ELITE 4.$"

@ The Eclipse plot reaches the League capital before the player enters the tournament.
@ NPC dialogue is informational: no HMs, forced combat or progression locks.
EryonCidadeLiga_EventScript_Reporter::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonCidadeLiga_EventScript_ReporterChampion
	goto_if_set FLAG_ERYON_DRAKONIA_ECLIPSE_DEFEATED, EryonCidadeLiga_EventScript_ReporterDrakonia
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonCidadeLiga_EventScript_ReporterEvidence
	msgbox EryonCidadeLiga_Text_Reporter, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_Investigator::
	lock
	faceplayer
	goto_if_unset FLAG_ERYON_GROTTO_SCOUT_REWARD_CLAIMED, EryonCidadeLiga_EventScript_InvestigatorScoutRewardCheck
EryonCidadeLiga_EventScript_InvestigatorNormal::
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonCidadeLiga_EventScript_InvestigatorEvidenceFiled
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, EryonCidadeLiga_EventScript_InvestigatorManifest
	goto_if_set FLAG_ERYON_QUALIFIED, EryonCidadeLiga_EventScript_InvestigatorQualified
	goto_if_set FLAG_ERYON_STAR_CHART_READ, EryonCidadeLiga_EventScript_InvestigatorChart
	msgbox EryonCidadeLiga_Text_InvestigatorBefore, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_InvestigatorQualified::
	msgbox EryonCidadeLiga_Text_InvestigatorAfter, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_Text_Reporter:
	.string "REPORTER: A cidade vive\n"
	.string "o grande torneio!\p"
	.string "Mas testemunhas viram\n"
	.string "agentes da ECLIPSE\n"
	.string "perto do estadio.$"

EryonCidadeLiga_Text_InvestigatorBefore:
	.string "INVESTIGADOR: A ECLIPSE\n"
	.string "procura algo na LIGA.\p"
	.string "Fique atento aos\n"
	.string "rumores nas ruas.\p"
	.string "Sua prioridade agora\n"
	.string "e a classificatoria.$"

EryonCidadeLiga_Text_InvestigatorAfter:
	.string "INVESTIGADOR: Oito\n"
	.string "vitorias confirmadas!\p"
	.string "A ECLIPSE observou\n"
	.string "todo o torneio.\p"
	.string "A investigacao ainda\n"
	.string "nao terminou.$"

@ Optional story reveal after decoding the cave chart, before qualifying.
EryonCidadeLiga_EventScript_InvestigatorChart::
	msgbox EryonCidadeLiga_Text_InvestigatorChart, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_Text_InvestigatorChart:
	.string "INVESTIGADOR: Voce\n"
	.string "achou a Carta Estelar!\p"
	.string "A rede une SOLARIS,\n"
	.string "DRAKONIA e a LIGA.\p"
	.string "Estamos vigiando os\n"
	.string "tecnicos da ECLIPSE.$"

@ Optional evidence collected on Dragon Trail changes the capital investigation.
EryonCidadeLiga_EventScript_InvestigatorManifest::
	msgbox EryonCidadeLiga_Text_InvestigatorManifest, MSGBOX_DEFAULT
	setflag FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED
	release
	end

EryonCidadeLiga_Text_InvestigatorManifest:
	.string "INVESTIGADOR: O\n"
	.string "manifesto e a prova!\p"
	.string "A ECLIPSE enviou\n"
	.string "cristais ate DRAKONIA.\p"
	.string "Vamos seguir os\n"
	.string "agentes na LIGA.$"

EryonCidadeLiga_EventScript_InvestigatorEvidenceFiled::
	msgbox EryonCidadeLiga_Text_EvidenceFiled, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_Text_EvidenceFiled:
	.string "INVESTIGADOR: Sua prova\n"
	.string "foi registrada!\p"
	.string "Agora investigamos\n"
	.string "a ECLIPSE na LIGA.$"

@ The League capital publicly acknowledges the optional evidence quest.
EryonCidadeLiga_EventScript_ReporterEvidence::
	msgbox EryonCidadeLiga_Text_ReporterEvidence, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_Text_ReporterEvidence:
	.string "REPORTER: As provas\n"
	.string "da ECLIPSE vieram\n"
	.string "a publico na LIGA!\p"
	.string "A seguranca aumentou\n"
	.string "perto do edificio.\p"
	.string "O torneio continua,\n"
	.string "mas todos estao alertas.$"

@ The League guide acknowledges the optional Star Grotto relay shutdown.
EryonCidadeLiga_EventScript_GuideRelayOff::
	msgbox EryonCidadeLiga_Text_GuideRelayOff, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_Text_GuideRelayOff:
	.string "GUIA: O sinal estranho\n"
	.string "da gruta desapareceu!\p"
	.string "A LIGA agradece\n"
	.string "sua ajuda na regiao.\p"
	.string "O torneio acontece\n"
	.string "no edificio central.$"

@ Optional emergency supplies in the central League plaza.
@ If the bag is full, the supplies remain available.
EryonCidadeLiga_EventScript_AidStation::
	lock
	goto_if_set FLAG_ERYON_LEAGUE_CITY_AID_COLLECTED, EryonCidadeLiga_EventScript_AidEmpty
	msgbox EryonCidadeLiga_Text_AidFound, MSGBOX_DEFAULT
	giveitem ITEM_FULL_RESTORE
	goto_if_eq VAR_RESULT, FALSE, EryonCidadeLiga_EventScript_AidFull
	setflag FLAG_ERYON_LEAGUE_CITY_AID_COLLECTED
	release
	end

EryonCidadeLiga_EventScript_AidFull::
	msgbox EryonCidadeLiga_Text_AidFull, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_AidEmpty::
	msgbox EryonCidadeLiga_Text_AidEmpty, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_Text_AidFound:
	.string "POSTO DE APOIO:\p"
	.string "Um FULL RESTORE\n"
	.string "para treinadores\n"
	.string "da classificatoria!$"

EryonCidadeLiga_Text_AidFull:
	.string "Sua BOLSA esta cheia.\p"
	.string "O remedio ficara\n"
	.string "guardado no posto.$"

EryonCidadeLiga_Text_AidEmpty:
	.string "Voce ja retirou\n"
	.string "seu remedio gratuito.$"


@ Optional battle at Star Grotto is recognized in the League capital.
@ Full bags can retry. Reporting the transport manifest remains independently possible.
EryonCidadeLiga_EventScript_InvestigatorScoutRewardCheck::
	goto_if_set FLAG_ERYON_GROTTO_ECLIPSE_SCOUT_DEFEATED, EryonCidadeLiga_EventScript_InvestigatorScoutReward
	goto EryonCidadeLiga_EventScript_InvestigatorNormal

EryonCidadeLiga_EventScript_InvestigatorScoutReward::
	msgbox EryonCidadeLiga_Text_ScoutRewardOffer, MSGBOX_DEFAULT
	giveitem ITEM_RARE_CANDY
	goto_if_eq VAR_RESULT, FALSE, EryonCidadeLiga_EventScript_InvestigatorScoutRewardFull
	setflag FLAG_ERYON_GROTTO_SCOUT_REWARD_CLAIMED
	msgbox EryonCidadeLiga_Text_ScoutRewardComplete, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_InvestigatorScoutRewardFull::
	msgbox EryonCidadeLiga_Text_ScoutRewardFull, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_Text_ScoutRewardOffer:
	.string "INVESTIGADOR: Soube\n"
	.string "de sua vitoria na gruta!\p"
	.string "A LIGA reservou\n"
	.string "uma recompensa.$"

EryonCidadeLiga_Text_ScoutRewardComplete:
	.string "INVESTIGADOR: Otimo!\p"
	.string "A ECLIPSE perdeu\n"
	.string "mais um agente.$"

EryonCidadeLiga_Text_ScoutRewardFull:
	.string "INVESTIGADOR: Sua\n"
	.string "BOLSA esta cheia!\p"
	.string "Volte para receber\n"
	.string "a recompensa.$"


@ News from the Dragon sanctuary reaches the League capital.
EryonCidadeLiga_EventScript_ReporterDrakonia::
	msgbox EryonCidadeLiga_Text_ReporterDrakonia, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_Text_ReporterDrakonia:
	.string "REPORTER: Ultimas\n"
	.string "noticias de DRAKONIA!\p"
	.string "O comandante ECLIPSE\n"
	.string "perdeu um duelo Pokemon.\p"
	.string "Mesmo com essa vitoria,\n"
	.string "a LIGA continua alerta.$"


@ Optional Kalos encounter at the new civic garden.
@ The restored Star Grotto relay stops Eclipse interference with Pokemon.
@ Capturing or defeating Espurr resolves the encounter, escape permits a retry.
EryonCidadeLiga_EventScript_ParkEspurr::
	lock
	goto_if_set FLAG_ERYON_LEAGUE_PARK_ESPURR_RESOLVED, EryonCidadeLiga_EventScript_ParkEspurrQuiet
	goto_if_unset FLAG_ERYON_STAR_GROTTO_RELAY_DISABLED, EryonCidadeLiga_EventScript_ParkEspurrDisturbed
	msgbox EryonCidadeLiga_Text_ParkEspurrPrompt, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonCidadeLiga_EventScript_ParkLeave
	closemessage
	setwildbattle SPECIES_ESPURR, 47
	waitse
	playmoncry SPECIES_ESPURR, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, EryonCidadeLiga_EventScript_ParkEspurrResolved
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, EryonCidadeLiga_EventScript_ParkEspurrResolved
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, EryonCidadeLiga_EventScript_ParkEspurrEscaped
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, EryonCidadeLiga_EventScript_ParkEspurrEscaped
	release
	end

EryonCidadeLiga_EventScript_ParkEspurrResolved::
	setflag FLAG_ERYON_LEAGUE_PARK_ESPURR_RESOLVED
	msgbox EryonCidadeLiga_Text_ParkEspurrResolved, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_ParkEspurrDisturbed::
	msgbox EryonCidadeLiga_Text_ParkEspurrDisturbed, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_ParkEspurrEscaped::
	msgbox EryonCidadeLiga_Text_ParkEspurrEscaped, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_ParkEspurrQuiet::
	msgbox EryonCidadeLiga_Text_ParkEspurrQuiet, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_ParkLeave::
	closemessage
	release
	end

@ The public botanist observes the garden and provides a single research reward.
@ A full bag never consumes the Dawn Stone reward.
EryonCidadeLiga_EventScript_ParkBotanist::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_LEAGUE_PARK_REWARD_CLAIMED, EryonCidadeLiga_EventScript_ParkRewardDone
	goto_if_unset FLAG_ERYON_LEAGUE_PARK_ESPURR_RESOLVED, EryonCidadeLiga_EventScript_ParkResearchPending
	msgbox EryonCidadeLiga_Text_ParkResearchReward, MSGBOX_DEFAULT
	giveitem ITEM_DAWN_STONE
	goto_if_eq VAR_RESULT, FALSE, EryonCidadeLiga_EventScript_ParkBagFull
	setflag FLAG_ERYON_LEAGUE_PARK_REWARD_CLAIMED
	msgbox EryonCidadeLiga_Text_ParkRewardThankYou, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_ParkResearchPending::
	msgbox EryonCidadeLiga_Text_ParkResearchPending, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_ParkBagFull::
	msgbox EryonCidadeLiga_Text_ParkBagFull, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_ParkRewardDone::
	msgbox EryonCidadeLiga_Text_ParkRewardDone, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_Text_ParkEspurrDisturbed:
	.string "JARDIM DA LIGA:\p"
	.string "Uma interferencia\n"
	.string "assusta os Pokemon.\p"
	.string "Investigue o sinal\n"
	.string "na GRUTA DAS ESTRELAS.$"

EryonCidadeLiga_Text_ParkEspurrPrompt:
	.string "Um ESPURR observa\n"
	.string "voce entre as flores!\p"
	.string "Investigar o jardim?$"

EryonCidadeLiga_Text_ParkEspurrResolved:
	.string "O jardim esta calmo.\p"
	.string "A pesquisa sobre\n"
	.string "ESPURR foi concluida.$"

EryonCidadeLiga_Text_ParkEspurrEscaped:
	.string "ESPURR desapareceu\n"
	.string "entre os arbustos!\p"
	.string "Talvez retorne depois.$"

EryonCidadeLiga_Text_ParkEspurrQuiet:
	.string "As flores se movem\n"
	.string "com o vento da LIGA.\p"
	.string "Nenhum Pokemon aparece.$"

EryonCidadeLiga_Text_ParkResearchPending:
	.string "BOTANICA: Os ESPURR\n"
	.string "sentem os cristais.\p"
	.string "Quando a interferencia\n"
	.string "cessar, observe o jardim.$"

EryonCidadeLiga_Text_ParkResearchReward:
	.string "BOTANICA: Obrigada\n"
	.string "por estudar ESPURR!\p"
	.string "Receba esta pedra\n"
	.string "da nossa pesquisa.$"

EryonCidadeLiga_Text_ParkRewardThankYou:
	.string "BOTANICA: A LIGA\n"
	.string "protege os Pokemon\n"
	.string "e a natureza da regiao.$"

EryonCidadeLiga_Text_ParkBagFull:
	.string "BOTANICA: Sua BOLSA\n"
	.string "esta cheia!\p"
	.string "Guardo a recompensa\n"
	.string "ate voce retornar.$"

EryonCidadeLiga_Text_ParkRewardDone:
	.string "BOTANICA: Nossa\n"
	.string "pesquisa continua!\p"
	.string "Visite o jardim\n"
	.string "sempre que quiser.$"


@ The capital celebrates the new champion without overwriting Eclipse investigation.
EryonCidadeLiga_EventScript_FanChampion::
	msgbox EryonCidadeLiga_Text_FanChampion, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_ReporterChampion::
	msgbox EryonCidadeLiga_Text_ReporterChampion, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_Text_FanChampion:
	.string "TORCEDORA: ERYON tem\n"
	.string "um novo CAMPEAO!\p"
	.string "O torneio no predio\n"
	.string "central foi historico.$"

EryonCidadeLiga_Text_ReporterChampion:
	.string "REPORTER: A regiao\n"
	.string "celebra seu CAMPEAO!\p"
	.string "Oito classificatorias,\n"
	.string "quatro membros da ELITE\n"
	.string "e uma vitoria final!\p"
	.string "O trabalho contra a\n"
	.string "ECLIPSE ainda continua.$"

@ League capital research delegate carries the consequences of the Serra relay.
@ This is optional and never alters the eight-qualifier tournament rules.
EryonCidadeLiga_EventScript_ResonanceDelegate::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_CHAMPION_CROWNED, EryonCidadeLiga_EventScript_ResonanceDelegateChampion
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonCidadeLiga_EventScript_ResonanceDelegateFiled
	goto_if_set FLAG_ERYON_SERRA_ECLIPSE_SIGNAL_DISABLED, EryonCidadeLiga_EventScript_ResonanceDelegateQuiet
	msgbox EryonCidadeLiga_Text_ResonanceDelegateBefore, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_ResonanceDelegateQuiet::
	msgbox EryonCidadeLiga_Text_ResonanceDelegateQuiet, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_ResonanceDelegateFiled::
	msgbox EryonCidadeLiga_Text_ResonanceDelegateFiled, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_ResonanceDelegateChampion::
	msgbox EryonCidadeLiga_Text_ResonanceDelegateChampion, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_Text_ResonanceDelegateBefore:
	.string "PESQUISADORA: A LIGA\n"
	.string "recebe ecos estranhos.\p"
	.string "O sinal vem da SERRA.\n"
	.string "Nao ignore as pistas.$"

EryonCidadeLiga_Text_ResonanceDelegateQuiet:
	.string "PESQUISADORA: A SERRA\n"
	.string "ja nao transmite!\p"
	.string "Mas a ECLIPSE possui\n"
	.string "mais de um terminal.\p"
	.string "Traga suas provas ao\n"
	.string "investigador da praca.$"

EryonCidadeLiga_Text_ResonanceDelegateFiled:
	.string "PESQUISADORA: Os dados\n"
	.string "foram entregues a LIGA!\p"
	.string "Podemos proteger a\n"
	.string "arena e os treinadores.$"

EryonCidadeLiga_Text_ResonanceDelegateChampion:
	.string "PESQUISADORA: Venceu\n"
	.string "a LIGA e ajudou ERYON!\p"
	.string "As cidades agora\n"
	.string "compartilham os estudos.$"
