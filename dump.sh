#!/bin/bash
# Dump Umpire of the Dead fixtures
python manage.py dumpdata eotd.faction > fixtures/faction.json
python manage.py dumpdata eotd.injury > fixtures/injury.json
python manage.py dumpdata eotd.skill > fixtures/skill.json
python manage.py dumpdata eotd.skilllist > fixtures/skilllist.json
python manage.py dumpdata eotd.unittemplate > fixtures/unittemplate.json
python manage.py dumpdata eotd.unittemplateskill > fixtures/unittemplateskill.json
python manage.py dumpdata eotd.unittemplateskilllist > fixtures/unittemplateskilllist.json
python manage.py dumpdata eotd.unittemplateweapon > fixtures/unittemplateweapon.json
python manage.py dumpdata eotd.unittemplateweaponlist > fixtures/unittemplateweaponlist.json
python manage.py dumpdata eotd.weapon > fixtures/weapon.json
python manage.py dumpdata eotd.weaponList > fixtures/weaponList.json
