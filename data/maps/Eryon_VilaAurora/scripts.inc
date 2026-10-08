@ Eryon: Professor Elya gives the one-time Riolu starter.
@ Progress uses Eryon's own persistent variable, independent from Birch's story.
EryonVilaAurora_EventScript_ProfessorElya::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_STARTER_RECEIVED, 1, EryonVilaAurora_EventScript_ElyaAfterStarter
	msgbox EryonVilaAurora_Text_ElyaIntroduction, MSGBOX_DEFAULT
	givemon SPECIES_RIOLU, 5
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PARTY, EryonVilaAurora_EventScript_RioluToParty
	goto_if_eq VAR_RESULT, MON_GIVEN_TO_PC, EryonVilaAurora_EventScript_RioluToPC
	goto EryonVilaAurora_EventScript_PartyFull
	end

EryonVilaAurora_EventScript_RioluToParty::
	setvar VAR_ERYON_STARTER_RECEIVED, 1
	msgbox EryonVilaAurora_Text_RioluReceived, MSGBOX_DEFAULT
	goto EryonVilaAurora_EventScript_CaptureKit

EryonVilaAurora_EventScript_RioluToPC::
	setvar VAR_ERYON_STARTER_RECEIVED, 1
	msgbox EryonVilaAurora_Text_RioluSentToPC, MSGBOX_DEFAULT
	goto EryonVilaAurora_EventScript_CaptureKit
	release
	end

EryonVilaAurora_EventScript_PartyFull::
	msgbox EryonVilaAurora_Text_PartyFull, MSGBOX_DEFAULT
	release
	end

EryonVilaAurora_EventScript_ElyaAfterStarter::
	goto_if_eq VAR_ERYON_CAPTURE_KIT_RECEIVED, 0, EryonVilaAurora_EventScript_CaptureKit
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonVilaAurora_EventScript_ElyaAfterBadge
	msgbox EryonVilaAurora_Text_ElyaAfterStarter, MSGBOX_DEFAULT
	goto EryonVilaAurora_EventScript_ElyaHealOffer

@ Optional homecoming after the first badge; no additional rewards or forced travel.
EryonVilaAurora_EventScript_ElyaAfterBadge::
	msgbox EryonVilaAurora_Text_ElyaAfterBadge, MSGBOX_DEFAULT
	goto EryonVilaAurora_EventScript_ElyaHealOffer

@ The capture kit is offered again if the bag was full; no duplicate reward.
EryonVilaAurora_EventScript_CaptureKit::
	goto_if_ge VAR_ERYON_CAPTURE_KIT_RECEIVED, 1, EryonVilaAurora_EventScript_ElyaAfterStarter
	msgbox EryonVilaAurora_Text_CaptureKit, MSGBOX_DEFAULT
	giveitem ITEM_POKE_BALL, 5
	goto_if_eq VAR_RESULT, FALSE, EryonVilaAurora_EventScript_CaptureKitFull
	setvar VAR_ERYON_CAPTURE_KIT_RECEIVED, 1
	release
	end

EryonVilaAurora_EventScript_CaptureKitFull::
	msgbox EryonVilaAurora_Text_CaptureKitFull, MSGBOX_DEFAULT
	release
	end

EryonVilaAurora_Text_ElyaIntroduction:
	.string "PROF. ELYA: Bem-vindo a Eryon!\p"
	.string "Esta regiao guarda muitos segredos.\p"
	.string "Riolu pode explorar esse mundo\n"
	.string "ao seu lado. Cuide bem dele!$"

EryonVilaAurora_Text_RioluReceived:
	.string "Voce recebeu RIOLU!\p"
	.string "A sua jornada comeca agora.$"

EryonVilaAurora_Text_RioluSentToPC:
	.string "RIOLU foi enviado ao PC!$"

EryonVilaAurora_Text_PartyFull:
	.string "Sua equipe esta cheia.\n"
	.string "Volte quando houver espaco.$"

EryonVilaAurora_Text_ElyaAfterStarter:
	.string "PROF. ELYA: O Bosque de Lumina\n"
	.string "fica alem da Rota 01.\p"
	.string "Explore com calma e cuide de RIOLU!$"

EryonVilaAurora_Text_ElyaAfterBadge:
	.string "PROF. ELYA: Sua primeira\n"
	.string "insignia! Estou orgulhosa.\p"
	.string "A marca no bosque ainda\n"
	.string "precisa ser investigada.\p"
	.string "Volte sempre que quiser\n"
	.string "conversar sobre sua jornada.$"

EryonVilaAurora_Text_CaptureKit:
	.string "PROF. ELYA: Leve estas cinco\n"
	.string "POKE BALLS para sua jornada!\p"
	.string "Observe os Pokemon de cada rota.$"

EryonVilaAurora_Text_CaptureKitFull:
	.string "PROF. ELYA: Sua bolsa esta cheia.\p"
	.string "Volte quando tiver espaco\n"
	.string "para as POKE BALLS.$"

@ The village notice introduces the route without forcing an early departure.
EryonVilaAurora_EventScript_VillageNotice::
	lock
	goto_if_ge VAR_ERYON_STARTER_RECEIVED, 1, EryonVilaAurora_EventScript_VillageNoticeAfterStarter
	msgbox EryonVilaAurora_Text_VillageNoticeBeforeStarter, MSGBOX_DEFAULT
	release
	end

EryonVilaAurora_EventScript_VillageNoticeAfterStarter::
	goto_if_ge VAR_ERYON_LUMINA_CLUE_FOUND, 1, EryonVilaAurora_EventScript_VillageNoticeAfterClue
	msgbox EryonVilaAurora_Text_VillageNoticeAfterStarter, MSGBOX_DEFAULT
	release
	end

EryonVilaAurora_EventScript_VillageNoticeAfterClue::
	msgbox EryonVilaAurora_Text_VillageNoticeAfterClue, MSGBOX_DEFAULT
	release
	end

EryonVilaAurora_Text_VillageNoticeBeforeStarter:
	.string "VILA AURORA - BOAS-VINDAS\p"
	.string "Novos treinadores devem\n"
	.string "conversar com a Prof. Elya.$"

EryonVilaAurora_Text_VillageNoticeAfterStarter:
	.string "TRILHA DA AURORA\p"
	.string "Rota 01: siga para o bosque.\n"
	.string "Prepare sua equipe antes.$"

EryonVilaAurora_Text_VillageNoticeAfterClue:
	.string "AVISO DA VILA\p"
	.string "Relatos de luzes estranhas\n"
	.string "chegaram do Bosque de Lumina.$"


@ Repeatable recovery in the starting village. The starter and capture kit
@ are handled first; this service never awards items or changes story flags.
EryonVilaAurora_EventScript_ElyaHealOffer::
	msgbox EryonVilaAurora_Text_ElyaHealOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonVilaAurora_EventScript_ElyaHealDeclined
	special HealPlayerParty
	msgbox EryonVilaAurora_Text_ElyaHealed, MSGBOX_DEFAULT
	release
	end

EryonVilaAurora_EventScript_ElyaHealDeclined::
	msgbox EryonVilaAurora_Text_ElyaHealDeclined, MSGBOX_DEFAULT
	release
	end

EryonVilaAurora_Text_ElyaHealOffer:
	.string "PROF. ELYA: Quer que eu\n"
	.string "recupere sua equipe Pokemon?$"

EryonVilaAurora_Text_ElyaHealed:
	.string "Sua equipe esta recuperada!\p"
	.string "Explore no seu proprio ritmo.$"

EryonVilaAurora_Text_ElyaHealDeclined:
	.string "Tudo bem! Pode voltar\n"
	.string "quando precisar.$"
