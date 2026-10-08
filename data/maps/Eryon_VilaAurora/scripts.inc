@ Eryon: Professor Elya gives the one-time Riolu starter.
@ Temporary story-state variable; replace with an Eryon-specific variable during integration.
EryonVilaAurora_EventScript_ProfessorElya::
	lock
	faceplayer
	goto_if_ge VAR_BIRCH_LAB_STATE, 3, EryonVilaAurora_EventScript_ElyaAfterStarter
	msgbox EryonVilaAurora_Text_ElyaIntroduction, MSGBOX_DEFAULT
	givemon SPECIES_RIOLU, 5
	goto_if_eq VAR_RESULT, FALSE, EryonVilaAurora_EventScript_PartyFull
	setvar VAR_BIRCH_LAB_STATE, 3
	msgbox EryonVilaAurora_Text_RioluReceived, MSGBOX_DEFAULT
	release
	end

EryonVilaAurora_EventScript_PartyFull::
	msgbox EryonVilaAurora_Text_PartyFull, MSGBOX_DEFAULT
	release
	end

EryonVilaAurora_EventScript_ElyaAfterStarter::
	msgbox EryonVilaAurora_Text_ElyaAfterStarter, MSGBOX_DEFAULT
	release
	end

EryonVilaAurora_Text_ElyaIntroduction:
	.string "PROF. ELYA: Bem-vindo a Eryon!\\p"
	.string "Esta regiao guarda muitos segredos.\\p"
	.string "Riolu pode explorar esse mundo\\n"
	.string "ao seu lado. Cuide bem dele!$"

EryonVilaAurora_Text_RioluReceived:
	.string "Voce recebeu RIOLU!\\p"
	.string "A sua jornada comeca agora.$"

EryonVilaAurora_Text_PartyFull:
	.string "Sua equipe esta cheia.\\n"
	.string "Volte quando houver espaco.$"

EryonVilaAurora_Text_ElyaAfterStarter:
	.string "PROF. ELYA: O Bosque de Lumina\\n"
	.string "fica alem da Rota 01.\\p"
	.string "Explore com calma e cuide de RIOLU!$"
