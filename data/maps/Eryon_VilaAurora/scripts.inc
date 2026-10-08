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
	release
	end

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
	msgbox EryonVilaAurora_Text_ElyaAfterStarter, MSGBOX_DEFAULT
	release
	end

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

EryonVilaAurora_Text_CaptureKit:
	.string "PROF. ELYA: Leve estas cinco\\n"
	.string "POKE BALLS para sua jornada!\\p"
	.string "Observe os Pokemon de cada rota.$"

EryonVilaAurora_Text_CaptureKitFull:
	.string "PROF. ELYA: Sua bolsa esta cheia.\\p"
	.string "Volte quando tiver espaco\\n"
	.string "para as POKE BALLS.$"
