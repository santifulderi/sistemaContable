from django.contrib import admin
from appSistemaContable.models import Usuario, Asiento, CuentaAsiento, Cuentas, Tareas, PerfilesTareas, TipoPerfiles

admin.site.register(Usuario)


class AsientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'descripcion')
    search_fields = ('descripcion', )
    date_hierarchy = 'fecha'


class CuentaAsientoAdmin(admin.ModelAdmin):
    list_display = ('id_cuenta', 'id_asiento', 'debe', 'haber', 'saldo')
    # search_fields = ()


class CuentasAdmin(admin.ModelAdmin):
    list_display = ('cuenta', 'codigo', 'tipo', 'recibe_saldo', 'saldo_actual')
    search_fields = ('cuenta', 'codigo', 'tipo')


class TipoPerfilesAdmin(admin.ModelAdmin):
    list_display = ('perfil', )


class PerfilesTareasAdmin(admin.ModelAdmin):
    list_display = ('id_tipo_perfil', 'id_tarea')


class TareasAdmin(admin.ModelAdmin):
    list_display = ('tarea', )


admin.site.register(Asiento, AsientoAdmin)

admin.site.register(CuentaAsiento, CuentaAsientoAdmin)

admin.site.register(Cuentas, CuentasAdmin)

admin.site.register(TipoPerfiles, TipoPerfilesAdmin)

admin.site.register(PerfilesTareas, PerfilesTareasAdmin)

admin.site.register(Tareas, TareasAdmin)
