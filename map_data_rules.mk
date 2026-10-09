# Eryon: generate correctly sized terrain binaries before assembling maps.
# Provisional metatile IDs; inspect tileset visuals and collision in Porymap.
ERYON_MAP_BINS := $(addprefix data/layouts/Eryon_,$(addsuffix /map.bin,BosqueDeLumina SerraDosCristais PassagemRochosa EstradaOriental ValeDosVentos EstradaDosPomares Rota04 ColinasDaNeblina TrilhaGlacial RotaDasCachoeiras))
ERYON_TERRAIN_PLANS := $(addprefix docs/eryon/,$(addsuffix _terrain_plan.txt,bosque_de_lumina serra_dos_cristais passagem_rochosa estrada_oriental vale_dos_ventos estrada_dos_pomares rota_04 colinas_da_neblina trilha_glacial rota_das_cachoeiras))
ERYON_VILLAGE_BIN := data/layouts/Eryon_VilaDosPomares/map.bin
ERYON_VILLAGE_PLAN := docs/eryon/vilas/vila_dos_pomares_village_plan.txt
ERYON_NEBLINA_BIN := data/layouts/Eryon_VilaDaNeblina/map.bin
ERYON_NEBLINA_PLAN := docs/eryon/vilas/vila_da_neblina_village_plan.txt
ERYON_CITY_BIN := data/layouts/Eryon_Neonara/map.bin
ERYON_CITY_PLAN := docs/eryon/cidades/neonara_city_plan.txt
ERYON_UMBRA_BIN := data/layouts/Eryon_Umbra/map.bin
ERYON_UMBRA_PLAN := docs/eryon/cidades/umbra_city_plan.txt
ERYON_OUTPOST_BIN := data/layouts/Eryon_PostoOriental/map.bin
ERYON_OUTPOST_PLAN := docs/eryon/vilas/posto_oriental_village_plan.txt
ERYON_REFUGE_BIN := data/layouts/Eryon_RefugioCristal/map.bin
ERYON_REFUGE_PLAN := docs/eryon/vilas/refugio_cristal_village_plan.txt
ERYON_FROSTHEIM_BIN := data/layouts/Eryon_Frostheim/map.bin
ERYON_FROSTHEIM_PLAN := docs/eryon/cidades/frostheim_city_plan.txt
ERYON_MAP_STAMP := data/layouts/.eryon_maps_generated

$(ERYON_MAP_STAMP): tools/build_eryon_map_bins.py $(ERYON_TERRAIN_PLANS) $(ERYON_VILLAGE_PLAN) $(ERYON_NEBLINA_PLAN) $(ERYON_CITY_PLAN) $(ERYON_FROSTHEIM_PLAN) $(ERYON_REFUGE_PLAN) $(ERYON_OUTPOST_PLAN) $(ERYON_UMBRA_PLAN)
	python3 tools/build_eryon_map_bins.py --wall 0x3c01 --path 0x3001 --meadow 0x3002 --stone 0x3003
	@touch $@

$(ERYON_MAP_BINS) $(ERYON_VILLAGE_BIN) $(ERYON_NEBLINA_BIN) $(ERYON_CITY_BIN) $(ERYON_FROSTHEIM_BIN) $(ERYON_REFUGE_BIN) $(ERYON_OUTPOST_BIN) $(ERYON_UMBRA_BIN): $(ERYON_MAP_STAMP)
	@test -s $@ || { echo "Missing Eryon map: $@; run make eryon-maps after removing the stamp"; exit 1; }
	@actual=$$(wc -c < "$@"); expected=4224; case "$@" in *VilaDosPomares*|*VilaDaNeblina*|*RefugioCristal*|*PostoOriental*) expected=2160;; *Neonara*|*Frostheim*|*Umbra*) expected=7168;; esac; test "$$actual" -eq "$$expected" || { echo "Wrong map size: $@ ($$actual bytes, expected $$expected)"; exit 1; }

$(DATA_ASM_BUILDDIR)/maps.o: $(ERYON_MAP_BINS) $(ERYON_VILLAGE_BIN) $(ERYON_NEBLINA_BIN) $(ERYON_CITY_BIN) $(ERYON_FROSTHEIM_BIN) $(ERYON_REFUGE_BIN) $(ERYON_OUTPOST_BIN) $(ERYON_UMBRA_BIN)

.PHONY: eryon-maps
eryon-maps: $(ERYON_MAP_BINS) $(ERYON_VILLAGE_BIN) $(ERYON_NEBLINA_BIN) $(ERYON_CITY_BIN) $(ERYON_FROSTHEIM_BIN) $(ERYON_REFUGE_BIN) $(ERYON_OUTPOST_BIN) $(ERYON_UMBRA_BIN)

# Map JSON data

# Inputs
MAPS_DIR = $(DATA_ASM_SUBDIR)/maps
LAYOUTS_DIR = $(DATA_ASM_SUBDIR)/layouts

# Outputs
MAPS_OUTDIR := $(MAPS_DIR)
LAYOUTS_OUTDIR := $(LAYOUTS_DIR)
INCLUDECONSTS_OUTDIR := include/constants

AUTO_GEN_TARGETS += $(INCLUDECONSTS_OUTDIR)/map_groups.h
AUTO_GEN_TARGETS += $(INCLUDECONSTS_OUTDIR)/layouts.h
AUTO_GEN_TARGETS += $(INCLUDECONSTS_OUTDIR)/map_event_ids.h
AUTO_GEN_TARGETS += $(DATA_SRC_SUBDIR)/map_group_count.h

MAP_DIRS := $(dir $(wildcard $(MAPS_DIR)/*/map.json))
MAP_CONNECTIONS := $(patsubst $(MAPS_DIR)/%/,$(MAPS_DIR)/%/connections.inc,$(MAP_DIRS))
MAP_EVENTS := $(patsubst $(MAPS_DIR)/%/,$(MAPS_DIR)/%/events.inc,$(MAP_DIRS))
MAP_HEADERS := $(patsubst $(MAPS_DIR)/%/,$(MAPS_DIR)/%/header.inc,$(MAP_DIRS))
MAP_JSONS := $(patsubst $(MAPS_DIR)/%/,$(MAPS_DIR)/%/map.json,$(MAP_DIRS))

$(DATA_ASM_BUILDDIR)/maps.o: $(DATA_ASM_SUBDIR)/maps.s $(LAYOUTS_DIR)/layouts.inc $(LAYOUTS_DIR)/layouts_table.inc $(MAPS_DIR)/headers.inc $(MAPS_DIR)/groups.inc $(MAPS_DIR)/connections.inc $(MAP_CONNECTIONS) $(MAP_HEADERS)
	$(PREPROC) -s $< charmap.txt | $(CPP) $(CPPFLAGS) -I include - | $(PREPROC) -ie $< charmap.txt | $(AS) $(ASFLAGS) -o $@
$(DATA_ASM_BUILDDIR)/map_events.o: $(DATA_ASM_SUBDIR)/map_events.s $(MAPS_DIR)/events.inc $(MAP_EVENTS)
	$(PREPROC) -s $< charmap.txt | $(CPP) $(CPPFLAGS) -I include - | $(PREPROC) -ie $< charmap.txt | $(AS) $(ASFLAGS) -o $@

$(MAPS_OUTDIR)/%/header.inc $(MAPS_OUTDIR)/%/events.inc $(MAPS_OUTDIR)/%/connections.inc: $(MAPS_DIR)/%/map.json $(INCLUDECONSTS_OUTDIR)/map_groups.h $(MAPJSON)
	$(MAPJSON) map emerald $< $(LAYOUTS_DIR)/layouts.json $(@D)


$(MAPS_OUTDIR)/connections.inc $(MAPS_OUTDIR)/groups.inc $(MAPS_OUTDIR)/events.inc $(MAPS_OUTDIR)/headers.inc $(INCLUDECONSTS_OUTDIR)/map_groups.h $(DATA_SRC_SUBDIR)/map_group_count.h: $(MAPS_DIR)/map_groups.json $(MAP_JSONS) .map_version $(MAPJSON)
	@$(MAPJSON) groups $(MAP_VERSION) $(filter %.json,$^) $(MAPS_OUTDIR) $(INCLUDECONSTS_OUTDIR)
	@echo "$(MAPJSON) groups $(MAP_VERSION) $(MAPS_DIR)/map_groups.json <MAP_JSONS> $(MAPS_OUTDIR) $(INCLUDECONSTS_OUTDIR)"

$(LAYOUTS_OUTDIR)/layouts.inc $(LAYOUTS_OUTDIR)/layouts_table.inc $(INCLUDECONSTS_OUTDIR)/layouts.h: $(LAYOUTS_DIR)/layouts.json .map_version $(MAPJSON)
	$(MAPJSON) layouts $(MAP_VERSION) $< $(LAYOUTS_OUTDIR) $(INCLUDECONSTS_OUTDIR)

# Generate constants for map events, which depend on data that's distributed across the map.json files.
# There's a lot of map.json files, so we print an abbreviated output with echo.
$(INCLUDECONSTS_OUTDIR)/map_event_ids.h: $(MAP_JSONS) $(MAPJSON)
	@$(MAPJSON) event_constants emerald $(MAP_JSONS) $(INCLUDECONSTS_OUTDIR)/map_event_ids.h
	@echo "$(MAPJSON) event_constants emerald <MAP_JSONS> $(INCLUDECONSTS_OUTDIR)/map_event_ids.h"

.map_version : FORCE
	@(echo "$(MAP_VERSION)" | cmp $@ -) || echo "$(MAP_VERSION)" > .map_version

FORCE:
.PHONY : FORCE
