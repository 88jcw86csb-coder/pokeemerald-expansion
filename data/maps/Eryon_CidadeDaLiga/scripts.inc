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
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonCidadeLiga_EventScript_ReporterEvidence
	msgbox EryonCidadeLiga_Text_Reporter, MSGBOX_DEFAULT
	release
	end

EryonCidadeLiga_EventScript_Investigator::
	lock
	faceplayer
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
