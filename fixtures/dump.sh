#!/bin/bash
python ../manage.py dumpdata eotd.faction > faction.json
python ../manage.py dumpdata eotd.skill > skill.json
python ../manage.py dumpdata eotd.skilllist > skilllist.json
python ../manage.py dumpdata eotd.unittemplate > unittemplate.json
python ../manage.py dumpdata eotd.unittemplateskill > unittemplateskill.json
python ../manage.py dumpdata eotd.unittemplateweapon > unittemplateweapon.json
python ../manage.py dumpdata eotd.unittemplateweaponlist > unittemplateweaponlist.json
python ../manage.py dumpdata eotd.injury > injury.json 
python ../manage.py dumpdata eotd.weaponList > weaponList.json
python ../manage.py dumpdata eotd.weapon > weapon.json
python ../manage.py dumpdata eotd.unittemplateskilllist > unittemplateskilllist.json

