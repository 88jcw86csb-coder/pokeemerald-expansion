#!/usr/bin/env python3
"""Audit the regional plan against generated map designs and approved gyms.

This does not claim any proposed map is playable in the ROM.
"""
from pathlib import Path
from eryon_world_progression import STAGES, GYMS
from eryon_gym_cities import CITIES
from eryon_villages import VILLAGES
from eryon_connector_routes import ROUTES as CONNECTORS
from eryon_new_routes import ROUTES as NEW_ROUTES

ROOT=Path(__file__).resolve().parents[1]
KNOWN_EXISTING={
    "vila_aurora", "rota_01", "rota_02", "rota_03",
    "bosque_de_lumina", "serra_dos_cristais", "passagem_rochosa",
    "estrada_oriental", "vale_dos_ventos",
}
FINAL_PLANS={"caminho_da_liga", "liga_eryon"}


def audit():
    errors=[]
    planned={name for name,_ in STAGES}
    for name in GYMS:
        if name not in CITIES:
            errors.append(f"Gym city missing from generator: {name}")
    for name,kind in STAGES:
        if kind=="gym":
            path=ROOT/"docs/eryon/cidades"/f"{name}_city_plan.txt"
        elif name in VILLAGES:
            path=ROOT/"docs/eryon/vilas"/f"{name}_village_plan.txt"
        elif name in CONNECTORS or name in NEW_ROUTES or kind in ("forest","mountain","valley","route","desert"):
            path=ROOT/"docs/eryon"/f"{name}_terrain_plan.txt"
        else:
            path=None
        if path is not None and name not in KNOWN_EXISTING and not path.is_file():
            errors.append(f"Missing concept plan: {name}: {path}")
    for name in FINAL_PLANS:
        if name not in planned:
            errors.append(f"Final stage missing: {name}")
        path=ROOT/"docs/eryon"/f"{name}_terrain_plan.txt"
        if not path.is_file():
            errors.append(f"Final map concept missing: {name}")
    return errors


if __name__=="__main__":
    errors=audit()
    if errors:
        for item in errors:
            print("ERROR:",item)
        raise SystemExit(1)
    print("Regional concept inventory: all planned map concepts found (not compiled).")
