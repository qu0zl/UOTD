from django.contrib import admin
from eotd.models import Campaign, Unit, UnitTemplate, Team, Faction, Weapon, UnitTemplateWeapon, UnitTemplateWeaponList, UnitWeapon, WeaponList, Skill, SkillList

class UnitTemplateWeaponInline(admin.TabularInline):
    model = UnitTemplateWeapon
    extra = 1
class UnitTemplateWeaponListInline(admin.TabularInline):
    model = UnitTemplateWeaponList
    extra = 1
class UnitTemplateAdmin(admin.ModelAdmin):
    inlines = (UnitTemplateWeaponInline, UnitTemplateWeaponListInline)

# If I wanted both ends of the template weapon manytomany to be able to be editable in the admin interface
# then I would also define and register the below admin class
#class WeaponAdmin(admin.ModelAdmin):
#    inlines = (UnitTemplateWeaponInline,)

class UnitWeaponInline(admin.TabularInline):
    model = UnitWeapon
    extra = 1

class UnitAdmin(admin.ModelAdmin):
    inlines = (UnitWeaponInline,)

#class WeaponListInline(admin.TabularInline):
#    model = Weapon
#    extra = 1

#class WeaponListAdmin(admin.ModelAdmin):
#    inlines = (WeaponListInline,)

admin.site.register(Campaign)
admin.site.register(UnitTemplate, UnitTemplateAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Team)
admin.site.register(Faction)
admin.site.register(Weapon)
#admin.site.register(WeaponList, WeaponListAdmin)
admin.site.register(WeaponList)
admin.site.register(Skill)
admin.site.register(SkillList)
