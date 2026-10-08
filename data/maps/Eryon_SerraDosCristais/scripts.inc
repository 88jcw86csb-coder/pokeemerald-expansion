@ Eryon: the first foothills beyond the eastern trail.
EryonSerra_EventScript_Geologist::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonSerra_EventScript_GeologistBadge
	msgbox EryonSerra_Text_GeologistBefore, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_GeologistBadge::
	msgbox EryonSerra_Text_GeologistBadge, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_Explorer::
	lock
	faceplayer
	msgbox EryonSerra_Text_Explorer, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_CrystalOutcrop::
	lock
	msgbox EryonSerra_Text_CrystalOutcrop, MSGBOX_DEFAULT
	release
	end

EryonSerra_Text_GeologistBefore:
	.string "GEOLOGO: Esta serra e antiga.\p"
	.string "As pedras guardam marcas\n"
	.string "de muito antes das cidades.$"

EryonSerra_Text_GeologistBadge:
	.string "GEOLOGO: O simbolo do eclipse\n"
	.string "apareceu nos meus estudos.\p"
	.string "Alguem retirou cristais\n"
	.string "desta encosta recentemente.$"

EryonSerra_Text_Explorer:
	.string "EXPLORADORA: Nao tenha pressa.\p"
	.string "Ha caminhos escondidos\n"
	.string "entre as pedras da serra.$"

EryonSerra_Text_CrystalOutcrop:
	.string "Uma rocha foi escavada.\p"
	.string "Pequenos fragmentos brilham\n"
	.string "sob a luz do sol.$"


@ New Serra characters: scout, historian and repeatable field medic.
EryonSerra_EventScript_YoungScout::
	lock
	faceplayer
	msgbox EryonSerra_Text_YoungScout, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_Archivist::
	lock
	faceplayer
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonSerra_EventScript_ArchivistBadge
	msgbox EryonSerra_Text_ArchivistBefore, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_ArchivistBadge::
	msgbox EryonSerra_Text_ArchivistBadge, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_Medic::
	lock
	faceplayer
	msgbox EryonSerra_Text_MedicOffer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EryonSerra_EventScript_MedicDecline
	special HealPlayerParty
	msgbox EryonSerra_Text_MedicHealed, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_MedicDecline::
	msgbox EryonSerra_Text_MedicDecline, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_AbandonedCamp::
	lock
	goto_if_ge VAR_ERYON_KAEL_DEFEATED, 1, EryonSerra_EventScript_AbandonedCampBadge
	msgbox EryonSerra_Text_AbandonedCampBefore, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_AbandonedCampBadge::
	msgbox EryonSerra_Text_AbandonedCampBadge, MSGBOX_DEFAULT
	release
	end

EryonSerra_Text_YoungScout:
	.string "ESCOTEIRO: Encontrei marcas\n"
	.string "de botas perto das rochas.\p"
	.string "Nao parecem de turistas.$"

EryonSerra_Text_ArchivistBefore:
	.string "HISTORIADOR: Esta serra\n"
	.string "tem historias esquecidas.\p"
	.string "Os cristais nao sao comuns.$"

EryonSerra_Text_ArchivistBadge:
	.string "HISTORIADOR: O eclipse era\n"
	.string "um simbolo de antigas lendas.\p"
	.string "Quem busca os cristais pode\n"
	.string "estar seguindo essas lendas.$"

EryonSerra_Text_MedicOffer:
	.string "SOCORRISTA: Posso recuperar\n"
	.string "sua equipe Pokemon. Aceita?$"

EryonSerra_Text_MedicHealed:
	.string "Seus Pokemon estao bem!\n"
	.string "Cuidado nas trilhas.$"

EryonSerra_Text_MedicDecline:
	.string "Estarei aqui se precisar.$"

EryonSerra_Text_AbandonedCampBefore:
	.string "Um acampamento foi deixado\n"
	.string "as pressas entre as pedras.$"

EryonSerra_Text_AbandonedCampBadge:
	.string "Uma caixa vazia traz um\n"
	.string "simbolo de eclipse.\p"
	.string "Ha sinais de cristais que\n"
	.string "foram levados daqui.$"

EryonSerra_EventScript_EclipseScout::
	lock
	faceplayer
	trainerbattle_single TRAINER_ERYON_SERRA_ECLIPSE, EryonSerra_Text_TrainerChallenge, EryonSerra_Text_TrainerDefeat, EryonSerra_EventScript_TrainerVictory, FALSE
	msgbox EryonSerra_Text_TrainerAfter, MSGBOX_DEFAULT
	release
	end

EryonSerra_EventScript_TrainerVictory::
	msgbox EryonSerra_Text_TrainerAfter, MSGBOX_DEFAULT
	release
	end

EryonSerra_Text_TrainerChallenge:
	.string "VIGIA: Ninguem deve ver\n"
	.string "o que levamos da serra!$"

EryonSerra_Text_TrainerDefeat:
	.string "VIGIA: Fui derrotado!$"

EryonSerra_Text_TrainerAfter:
	.string "VIGIA: Voce nao deveria\n"
	.string "ter chegado tao longe.$"
