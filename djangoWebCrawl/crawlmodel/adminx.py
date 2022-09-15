import xadmin
from .models import kikuumodel, snatchermodel, fixmodel, jjshousemodel, lovelywholesalemodel, \
    wholesale7model, kilimallmodel, dealhubmodel, valuecomodel, jumiamodel, bidorbuymodel, ackermansmodel, \
    cjdropshippingmodel, mrpmodel,zandomodel, yellowsubtradingmodel

from import_export import resources
from .views import TestView
from xadmin.views import BaseAdminPlugin, ListAdminView


class GlobalSettings(object):
    site_title = "电商数据平台"
    site_footer = "ShopShipShake"

    # menu_style="accordion"

    def get_site_menu(self):
        return [
            {
                'title': '功能子键',
                'icon': 'fa fa-th-large',
                'menus': (
                    {

                        'title': '测试菜单',
                        'url': '/xadmin/test_view',
                        'icon': 'fa fa-gears',
                    },
                )
            }
        ]


class BaseSettings(object):
    # 开启皮肤选项
    enable_themes = True
    use_bootswatch = True


############下面为资源类，负责导入导出模块的定义######################
class kikuuResource(resources.ModelResource):
    class Meta:
        model = kikuumodel


class fixResource(resources.ModelResource):
    class Meta:
        model = fixmodel


class snatcherResource(resources.ModelResource):
    class Meta:
        model = snatchermodel


class kilimallResource(resources.ModelResource):
    class Meta:
        model = kilimallmodel


class dealhubResource(resources.ModelResource):
    class Meta:
        model = dealhubmodel


class valuecoResource(resources.ModelResource):
    class Meta:
        model = valuecomodel


class jumiaResource(resources.ModelResource):
    class Meta:
        model = jumiamodel


class jjshouseResource(resources.ModelResource):
    class Meta:
        model = jjshousemodel


class lovelywholesaleResource(resources.ModelResource):
    class Meta:
        model = lovelywholesalemodel


class wholesale7Resource(resources.ModelResource):
    class Meta:
        model = wholesale7model


class bidorbuyResource(resources.ModelResource):
    class Meta:
        model = bidorbuymodel


class ackermansResource(resources.ModelResource):
    class Meta:
        model = ackermansmodel


class cjdropshippingResource(resources.ModelResource):
    class Meta:
        model = cjdropshippingmodel


class mrpResource(resources.ModelResource):
    class Meta:
        model = mrpmodel

class zandoResource(resources.ModelResource):
    class Meta:
        model = zandomodel

class yellowsubtradingResource(resources.ModelResource):
    class Meta:
        model = yellowsubtradingmodel
#######################下述为后台类，负责后台配置###############################################
class baseAdmin(object):
    # 展示的数据列名
    list_display = ['show_image', 'Title', 'price', 'offer_url', 'huitou',
                    'saledCount', 'wwxy', 'service', 'cfmj', 'zrs', 'num_comment', 'good_percent',
                    'rateAverageStarLevel', 'weight', 'deliverySpeed', 'date']
    # 可供搜素的属性
    search_fields = ['id', 'Title', 'offer_url', 'huitou', 'date', 'Image']

    # 可供过滤的属性
    list_filter = ['huitou', 'saledCount', 'service', 'wwxy', 'cfmj', 'zrs', 'num_comment', 'good_percent',
                   'rateAverageStarLevel',
                   'deliverySpeed', 'date']
    # 可跳转的链接
    # list_display_links = ("Title", "offer_url", )

    redirect = True

    # 可供用户编辑的属性
    list_editable = []

    # 当前模型小图标
    model_icon = 'fa fa-bullseye'


class KikuuAdmin(baseAdmin):
    # import_export_args = {'import_resource_class': kikuuResource, 'export_resource_class': kikuuResource}
    import_export_args = {'import_resource_class': kikuuResource}


class fixAdmin(baseAdmin):
    # import_export_args = {'import_resource_class': kikuuResource, 'export_resource_class': kikuuResource}
    import_export_args = {'import_resource_class': fixResource}


class snatcherAdmin(baseAdmin):
    # import_export_args = {'import_resource_class': kikuuResource, 'export_resource_class': kikuuResource}
    import_export_args = {'import_resource_class': snatcherResource}


class kilimallAdmin(baseAdmin):
    import_export_args = {'import_resource_class': kilimallResource}


class dealhubAdmin(baseAdmin):
    import_export_args = {'import_resource_class': dealhubResource}


class valuecoAdmin(baseAdmin):
    import_export_args = {'import_resource_class': valuecoResource}


class jumiaAdmin(baseAdmin):
    import_export_args = {'import_resource_class': jumiaResource}


class jjshouseAdmin(baseAdmin):
    import_export_args = {'import_resource_class': jjshouseResource}


class lovelywholesaleAdmin(baseAdmin):
    import_export_args = {'import_resource_class': lovelywholesaleResource}


class wholesale7Admin(baseAdmin):
    import_export_args = {'import_resource_class': wholesale7Resource}


class bidorbuyAdmin(baseAdmin):
    import_export_args = {'import_resource_class': bidorbuyResource}


class ackermansAdmin(baseAdmin):
    import_export_args = {'import_resource_class': ackermansResource}


class cjdropshippingAdmin(baseAdmin):
    import_export_args = {'import_resource_class': cjdropshippingResource}


class mrpAdmin(baseAdmin):
    import_export_args = {'import_resource_class': mrpResource}


class zandoAdmin(baseAdmin):
    import_export_args = {'import_resource_class': zandoResource}


class yellowsubtradingAdmin(baseAdmin):
    import_export_args = {'import_resource_class': yellowsubtradingResource}

xadmin.site.register(kikuumodel, KikuuAdmin)
xadmin.site.register(fixmodel, fixAdmin)
xadmin.site.register(jjshousemodel, jjshouseAdmin)
xadmin.site.register(snatchermodel, snatcherAdmin)
xadmin.site.register(lovelywholesalemodel, lovelywholesaleAdmin)
xadmin.site.register(wholesale7model, wholesale7Admin)
xadmin.site.register(kilimallmodel, kilimallAdmin)
xadmin.site.register(dealhubmodel, dealhubAdmin)
xadmin.site.register(valuecomodel, valuecoAdmin)
xadmin.site.register(jumiamodel, jumiaAdmin)
xadmin.site.register(bidorbuymodel, bidorbuyAdmin)
xadmin.site.register(ackermansmodel, ackermansAdmin)
xadmin.site.register(cjdropshippingmodel, cjdropshippingAdmin)
xadmin.site.register(mrpmodel, mrpAdmin)
xadmin.site.register(zandomodel, zandoAdmin)
xadmin.site.register(yellowsubtradingmodel, yellowsubtradingAdmin)
xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)

xadmin.site.register_view(r'test_view/$', TestView, name='test')
