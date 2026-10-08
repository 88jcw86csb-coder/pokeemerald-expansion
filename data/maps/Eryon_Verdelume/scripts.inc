@ The town guide acknowledges the forest discovery without forcing progression.
EryonVerdelume_EventScript_Guide::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonVerdelume_EventScript_GuideBadge
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonVerdelume_EventScript_GuideClue
	msgbox EryonVerdelume_Text_Guide, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_EventScript_GuideBadge::
	msgbox EryonVerdelume_Text_GuideBadge, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_EventScript_GuideClue::
	msgbox EryonVerdelume_Text_GuideClue, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_Text_Guide:
	.string "Bem-vindo a Verdelume!\p"
	.string "Kael protege nosso ginasio, mas\n"
	.string "o bosque preocupa a cidade.$"

EryonVerdelume_Text_GuideBadge:
	.string "Parabens pela primeira insignia!\p"
	.string "Kael vai proteger o bosque.\n"
	.string "Sua jornada continua adiante.$"

EryonVerdelume_Text_GuideClue:
	.string "Uma marca de eclipse no bosque?\p"
	.string "Kael tambem ouviu rumores.\n"
	.string "Talvez ele saiba de algo.$"

@ A local resident introduces Kael without forcing the story forward.
EryonVerdelume_EventScript_LocalKid::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonVerdelume_EventScript_LocalKidBadge
	msgbox EryonVerdelume_Text_LocalKid, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_EventScript_LocalKidBadge::
	msgbox EryonVerdelume_Text_LocalKidBadge, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_Text_LocalKidBadge:
	.string "Voce venceu a ROSERADE do Kael!\p"
	.string "Quero treinar bastante para\n"
	.string "ser forte como voces dois.$"

EryonVerdelume_Text_LocalKid:
	.string "Kael treina Pokemon de planta!\p"
	.string "Dizem que sua ROSERADE nunca\n"
	.string "desiste de uma batalha.$"

@ Kael challenges the player after they discover the forest clue.
EryonVerdelume_EventScript_Kael::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonVerdelume_EventScript_KaelAfterBattle
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonVerdelume_EventScript_KaelClue
	msgbox EryonVerdelume_Text_KaelWelcome, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_EventScript_KaelClue::
	goto_if_ge VAR_ERYON_KAEL_BRIEFED, 1, EryonVerdelume_EventScript_KaelFollowup
	msgbox EryonVerdelume_Text_KaelClue, MSGBOX_DEFAULT
	setvar VAR_ERYON_KAEL_BRIEFED, 1
	release
	end

EryonVerdelume_EventScript_KaelFollowup::
	trainerbattle_single TRAINER_ERYON_KAEL, EryonVerdelume_Text_KaelChallenge, EryonVerdelume_Text_KaelDefeat, EryonVerdelume_EventScript_KaelVictory, FALSE
	msgbox EryonVerdelume_Text_KaelAfterBattle, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_EventScript_KaelVictory::
	setvar VAR_ERYON_KAEL_DEFEATED, 1
	message EryonVerdelume_Text_KaelBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	setflag FLAG_BADGE01_GET
	msgbox EryonVerdelume_Text_KaelAfterBattle, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_EventScript_KaelAfterBattle::
	msgbox EryonVerdelume_Text_KaelAfterBattle, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_Text_KaelWelcome:
	.string "KAEL: Cuido das trilhas que\n"
	.string "cercam Verdelume.\p"
	.string "No Bosque de Lumina,\n"
	.string "observe bem as pedras.\p"
	.string "Algo estranho aconteceu la.$"

EryonVerdelume_Text_KaelClue:
	.string "KAEL: Entao viu a marca antiga!\p"
	.string "A floresta precisa de ajuda.\n"
	.string "Vamos investigar com cuidado.$"

EryonVerdelume_Text_KaelFollowup:
	.string "KAEL: Obrigado por avisar.\p"
	.string "Ainda nao sabemos quem marcou\n"
	.string "aquelas pedras antigas.\p"
	.string "Continue explorando com calma.$"

@ A public notice changes once the player has investigated the forest.
EryonVerdelume_EventScript_ForestNotice::
	lock
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonVerdelume_EventScript_ForestNoticeClue
	msgbox EryonVerdelume_Text_ForestNotice, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_EventScript_ForestNoticeClue::
	msgbox EryonVerdelume_Text_ForestNoticeClue, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_Text_ForestNotice:
	.string "AVISO AOS VIAJANTES\p"
	.string "Luzes estranhas foram vistas\n"
	.string "no Bosque de Lumina.\p"
	.string "Explore com cuidado.$"

EryonVerdelume_Text_ForestNoticeClue:
	.string "AVISO AOS VIAJANTES\p"
	.string "A antiga marca de eclipse\n"
	.string "esta sendo investigada.\p"
	.string "Informe Kael sobre pistas.$"

@ The town botanist offers optional worldbuilding after the forest investigation.
EryonVerdelume_EventScript_Botanist::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonVerdelume_EventScript_BotanistAfterBadge
	goto_if_ge VAR_ERYON_KAEL_BRIEFED, 1, EryonVerdelume_EventScript_BotanistAfterKael
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonVerdelume_EventScript_BotanistAfterClue
	msgbox EryonVerdelume_Text_BotanistWelcome, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_EventScript_BotanistAfterBadge::
	msgbox EryonVerdelume_Text_BotanistAfterBadge, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_EventScript_BotanistAfterClue::
	msgbox EryonVerdelume_Text_BotanistAfterClue, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_EventScript_BotanistAfterKael::
	msgbox EryonVerdelume_Text_BotanistAfterKael, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_Text_BotanistAfterBadge:
	.string "BOTANICA: Depois da batalha,\n"
	.string "comparei amostras do bosque.\p"
	.string "As flores proximas a marca\n"
	.string "florescem fora de epoca.\p"
	.string "Alguem pode estar alterando\n"
	.string "a energia daquela floresta.\p"
	.string "Volte ao bosque e observe\n"
	.string "as pedras com atencao.$"

EryonVerdelume_Text_BotanistWelcome:
	.string "Estudo as plantas do bosque.\p"
	.string "Algumas flores se fecham\n"
	.string "quando as luzes aparecem.$"

EryonVerdelume_Text_BotanistAfterClue:
	.string "Uma marca antiga nas pedras?\p"
	.string "Talvez a luz e as flores\n"
	.string "estejam relacionadas.$"

EryonVerdelume_Text_BotanistAfterKael:
	.string "Kael vai investigar? Que bom!\p"
	.string "Enquanto isso, vou comparar\n"
	.string "as flores das duas trilhas.$"

EryonVerdelume_Text_KaelChallenge:
	.string "KAEL: Quero ver o que aprendeu\n"
	.string "em sua viagem pelo bosque!$"

EryonVerdelume_Text_KaelDefeat:
	.string "KAEL: Sua coragem me surpreendeu!$"

EryonVerdelume_Text_KaelAfterBattle:
	.string "KAEL: Foi uma bela batalha!\p"
	.string "Um mensageiro viu carrocas\n"
	.string "seguindo a trilha do leste.\p"
	.string "Dizem que levam cristais\n"
	.string "marcados com um eclipse.\p"
	.string "Nao persiga ninguem sozinho.\n"
	.string "Investigue as pistas primeiro.$"

EryonVerdelume_Text_KaelBadge:
	.string "KAEL: Voce conquistou a primeira\n"
	.string "insignia da regiao de Eryon!$"


@ Free, repeatable healing in Verdelume for early-game exploration.
@ This service is optional and does not change story progress.
EryonVerdelume_EventScript_FieldMedic::
	lock
	faceplayer
	msgbox EryonVerdelume_Text_FieldMedicWelcome, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonVerdelume_EventScript_FieldMedicDecline
	special HealPlayerParty
	msgbox EryonVerdelume_Text_FieldMedicHealed, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_EventScript_FieldMedicDecline::
	msgbox EryonVerdelume_Text_FieldMedicDecline, MSGBOX_DEFAULT
	release
	end

EryonVerdelume_Text_FieldMedicWelcome:
	.string "SOCORRISTA: Suas viagens pelo\n"
	.string "bosque podem ser cansativas.\p"
	.string "Quer que eu cuide da sua\n"
	.string "equipe Pokemon?$"

EryonVerdelume_Text_FieldMedicHealed:
	.string "Pronto! Seus Pokemon estao\n"
	.string "descansados e saudaveis.\p"
	.string "Boa sorte na sua jornada!$"

EryonVerdelume_Text_FieldMedicDecline:
	.string "Tudo bem! Volte se precisar\n"
	.string "de ajuda com sua equipe.$"
