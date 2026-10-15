Eryon_Lunaris_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Eryon_Lunaris_RespawnCheckpoint
	.byte 0

@ Native Eryon whiteout checkpoint. Re-entry updates the safe return town.
Eryon_Lunaris_RespawnCheckpoint:
	setrespawn HEAL_LOCATION_ERYON_LUNARIS
	end

@ Lunaris protects the ancient observatory and the seventh gym.
EryonLunaris_EventScript_Medic::
	lock
	faceplayer
	msgbox EryonLunaris_Text_Medic, MSGBOX_DEFAULT
	special HealPlayerParty
	release
	end

EryonLunaris_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonLunaris_EventScript_GymGuideClue
	msgbox EryonLunaris_Text_GymGuideBefore, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_GymGuideClue::
	msgbox EryonLunaris_Text_GymGuideClue, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_Astronomer::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_LUNAR_INKAY_RESOLVED, EryonLunaris_EventScript_AstronomerInkay
	goto_if_set FLAG_ERYON_LUNAR_ARRAY_READ, EryonLunaris_EventScript_AstronomerMoonfall
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonLunaris_EventScript_AstronomerClue
	msgbox EryonLunaris_Text_AstronomerBefore, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_AstronomerClue::
	msgbox EryonLunaris_Text_AstronomerClue, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_EclipseAnalyst::
	lock
	faceplayer
	goto_if_set FLAG_ERYON_ECLIPSE_EVIDENCE_REPORTED, EryonLunaris_EventScript_AnalystAfterReport
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, EryonLunaris_EventScript_AnalystManifest
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonLunaris_EventScript_EclipseAnalystExposed
	msgbox EryonLunaris_Text_AnalystBefore, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_EclipseAnalystExposed::
	msgbox EryonLunaris_Text_AnalystExposed, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_ObservatorySign::
	lock
	msgbox EryonLunaris_Text_ObservatorySign, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_CrystalGenerator::
	lock
	goto_if_set FLAG_ERYON_DRAGON_TRAIL_MANIFEST_READ, EryonLunaris_EventScript_GeneratorManifest
	goto_if_ge VAR_ERYON_SERRA_CLUE_FOUND, 1, EryonLunaris_EventScript_CrystalGeneratorClue
	msgbox EryonLunaris_Text_GeneratorBefore, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_CrystalGeneratorClue::
	msgbox EryonLunaris_Text_GeneratorClue, MSGBOX_DEFAULT
	release
	end

EryonLunaris_Text_Medic:
	.string "SOCORRISTA: A trilha\n"
	.string "e longa e cansativa.\p"
	.string "Vou recuperar seus\n"
	.string "Pokemon agora.$"

EryonLunaris_Text_GymGuideBefore:
	.string "GUIA: O GINASIO de\n"
	.string "LUNARIS usa PSIQUICO.\p"
	.string "Pokemon FADA tambem\n"
	.string "ajudam nos desafios.$"

EryonLunaris_Text_GymGuideClue:
	.string "GUIA: O lider investiga\n"
	.string "os sinais da ECLIPSE.\p"
	.string "O desafio do GINASIO\n"
	.string "ainda nao foi liberado.$"

EryonLunaris_Text_AstronomerBefore:
	.string "ASTRONOMA: Os cristais\n"
	.string "seguem um antigo canto.\p"
	.string "O movimento da LUA\n"
	.string "altera sua frequencia.$"

EryonLunaris_Text_AstronomerClue:
	.string "ASTRONOMA: O sinal\n"
	.string "de IGNIVAR chegou aqui!\p"
	.string "O arquivo da ALDEIA\n"
	.string "revelou uma pista.$"

EryonLunaris_Text_AnalystBefore:
	.string "TECNICO: Estou medindo\n"
	.string "a luz das estrelas.\p"
	.string "O observatorio esta\n"
	.string "sob manutencao.$"

EryonLunaris_Text_AnalystExposed:
	.string "ECLIPSE: A LUA pode\n"
	.string "ampliar nosso sinal!\p"
	.string "As caixas ja seguem\n"
	.string "para DRAKONIA.$"

EryonLunaris_Text_ObservatorySign:
	.string "OBSERVATORIO LUNAR:\n"
	.string "Pesquisa de cristais.\p"
	.string "Acesso restrito na\n"
	.string "fase de manutencao.$"

EryonLunaris_Text_GeneratorBefore:
	.string "Um gerador antigo\n"
	.string "esta desligado.\p"
	.string "Uma carta celeste\n"
	.string "repousa ao lado.$"

EryonLunaris_Text_GeneratorClue:
	.string "O selo da ECLIPSE\n"
	.string "aparece no gerador.\p"
	.string "Cabos levam energia\n"
	.string "de IGNIVAR ate ca.$"

@ The Lunar observatory reacts to shipments documented later on Dragon Trail.
EryonLunaris_EventScript_AnalystManifest::
	msgbox EryonLunaris_Text_AnalystManifest, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_AnalystAfterReport::
	msgbox EryonLunaris_Text_AnalystAfterReport, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_GeneratorManifest::
	msgbox EryonLunaris_Text_GeneratorManifest, MSGBOX_DEFAULT
	release
	end

EryonLunaris_Text_AnalystManifest:
	.string "ECLIPSE: Encontrou\n"
	.string "nossa lista de cargas!\p"
	.string "Nao sabe o que\n"
	.string "esses cristais fazem.$"

EryonLunaris_Text_AnalystAfterReport:
	.string "ECLIPSE: A LIGA ja\n"
	.string "sabe das remessas?!\p"
	.string "Os chefes vao mudar\n"
	.string "o plano da operacao.$"

EryonLunaris_Text_GeneratorManifest:
	.string "O registro da trilha\n"
	.string "cita este gerador.\p"
	.string "Seu numero coincide\n"
	.string "com o manifesto.$"

@ Eryon: LYRA is the city leader, separate from the Gym guide.
EryonLunaris_EventScript_GymLeader::
	lock
	faceplayer
	goto_if_set FLAG_BADGE07_GET, EryonLunaris_EventScript_GymAfter
	goto_if_unset FLAG_BADGE06_GET, EryonLunaris_EventScript_GymNotReady
	goto EryonLunaris_EventScript_GymOffer
	end

@ Tactical badge battle — Lunaris: ace level 51, badge 7.
EryonLunaris_EventScript_GymOffer::
	msgbox EryonLunaris_Text_GymOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonLunaris_EventScript_GymDecline
	closemessage
	trainerbattle_single TRAINER_ERYON_GYM_LUNARIS, EryonLunaris_Text_GymIntro, EryonLunaris_Text_GymLoss, EryonLunaris_EventScript_GymVictory, FALSE
	msgbox EryonLunaris_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_GymVictory::
	message EryonLunaris_Text_GymBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	setflag FLAG_BADGE07_GET
	msgbox EryonLunaris_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_GymDecline::
	closemessage
	release
	end

EryonLunaris_EventScript_GymNotReady::
	msgbox EryonLunaris_Text_GymNotReady, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_GymAfter::
	msgbox EryonLunaris_Text_GymAfter, MSGBOX_DEFAULT
	release
	end

EryonLunaris_Text_GymOffer:
	.string "LYRA: Meu GINASIO\n"
	.string "treina com psiquismo.\p"
	.string "Desafiar meu time\n"
	.string "de Pokemon agora?$"

EryonLunaris_Text_GymIntro:
	.string "LYRA: Mostre sua\n"
	.string "forca e estrategia!$"

EryonLunaris_Text_GymLoss:
	.string "LYRA: Voce encontrou\n"
	.string "uma boa resposta!$"

EryonLunaris_Text_GymBadge:
	.string "Venceu o 7o GINASIO!\p"
	.string "Recebeu a INSIGNIA\n"
	.string "de numero 7!$"

EryonLunaris_Text_GymAfter:
	.string "LYRA: Bela vitoria!\p"
	.string "Siga os sinais das estrelas.$"

EryonLunaris_Text_GymNotReady:
	.string "LYRA: Primeiro,\n"
	.string "conquiste a INSIGNIA\n"
	.string "do GINASIO anterior.$"

@ Scholar connects evidence from the valley archive to the existing seventh Gym.
@ Badge checks remain read-only here; the leader battle is unchanged.
EryonLunaris_EventScript_ObservatoryScholar::
	lock
	faceplayer
	goto_if_set FLAG_BADGE07_GET, EryonLunaris_EventScript_ScholarAfterBadge
	goto_if_set FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED, EryonLunaris_EventScript_ScholarConfirmed
	goto_if_set FLAG_ERYON_ECHO_TRACE_RECORDED, EryonLunaris_EventScript_ScholarPending
	msgbox EryonLunaris_Text_ScholarWaiting, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_ScholarPending::
	msgbox EryonLunaris_Text_ScholarPending, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_ScholarConfirmed::
	msgbox EryonLunaris_Text_ScholarConfirmed, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_ScholarAfterBadge::
	goto_if_set FLAG_ERYON_ECHO_ARCHIVE_REWARD_CLAIMED, EryonLunaris_EventScript_ScholarArchiveAndBadge
	msgbox EryonLunaris_Text_ScholarAfterBadge, MSGBOX_DEFAULT
	release
	end

EryonLunaris_Text_ScholarWaiting:
	.string "PESQUISADORA: Nosso\n"
	.string "telescopio ouve ecos!\p"
	.string "Registre a frequencia\n"
	.string "no VALE DOS ECOS.$"

EryonLunaris_Text_ScholarPending:
	.string "PESQUISADORA: Trouxe\n"
	.string "dados do VALE DOS ECOS!\p"
	.string "O ARQUIVO DA ALDEIA\n"
	.string "pode separar os sons.$"

EryonLunaris_Text_ScholarConfirmed:
	.string "PESQUISADORA: O arquivo\n"
	.string "confirmou a ECLIPSE!\p"
	.string "O sinal sai daqui\n"
	.string "para a TRILHA DOS DRAGOES.$"

EryonLunaris_Text_ScholarAfterBadge:
	.string "PESQUISADORA: Sua 7a\n"
	.string "INSIGNIA mostra coragem!\p"
	.string "Os ecos continuam\n"
	.string "ate DRAKONIA.$"

@ The scholar acknowledges both the optional echo archive and seventh badge.
EryonLunaris_EventScript_ScholarArchiveAndBadge:
	msgbox EryonLunaris_Text_ScholarArchiveAndBadge, MSGBOX_DEFAULT
	release
	end

EryonLunaris_Text_ScholarArchiveAndBadge:
	.string "PESQUISADORA: O arquivo\n"
	.string "e sua 7a INSIGNIA!\p"
	.string "O canto antigo foi\n"
	.string "distorcido pela ECLIPSE.\p"
	.string "Compare as cargas na\n"
	.string "TRILHA DOS DRAGOES.$"

@ Lunaris astronomer recognizes the southern lunar sanctuary and wildlife.
EryonLunaris_EventScript_AstronomerMoonfall::
	msgbox EryonLunaris_Text_AstronomerMoonfall, MSGBOX_DEFAULT
	release
	end

EryonLunaris_EventScript_AstronomerInkay::
	msgbox EryonLunaris_Text_AstronomerInkay, MSGBOX_DEFAULT
	release
	end

EryonLunaris_Text_AstronomerMoonfall:
	.string "ASTRONOMA: O receptor\n"
	.string "na TRILHA LUNAR liga\n"
	.string "a ALDEIA a LUNARIS.\p"
	.string "A ECLIPSE alterou\n"
	.string "aquele sinal antigo.$"

EryonLunaris_Text_AstronomerInkay:
	.string "ASTRONOMA: O INKAY\n"
	.string "do santuario voltou\n"
	.string "a ter tranquilidade!\p"
	.string "A LUA ilumina agora\n"
	.string "os cristais naturais.$"
