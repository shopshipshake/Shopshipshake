from django.db import models

# Create your models here.


class Basemodel(models.Model):
    date = models.DateField(auto_now=True, verbose_name='日期',null=True)
    Image = models.CharField(max_length=1000, verbose_name='图片链接',default=None,null=True)
    id = models.CharField(max_length=200, verbose_name='产品ID', primary_key=True)
    Title = models.CharField(max_length=100, verbose_name='商品名称(电商)',default=None,null=True)
    price = models.CharField(max_length=100, verbose_name='商品价格',default=None,null=True)
    offer_url = models.URLField(max_length=1000, verbose_name='1688商品链接',default=None,null=True)
    saledCount = models.FloatField(verbose_name='已售商品数量', default=0, null=True)
    service = models.DecimalField(verbose_name='服务能力', default=0, null=True, max_digits=3,decimal_places=2)
    huitou = models.DecimalField(verbose_name='回头率', default=0, null=True,max_digits=3,decimal_places=2)
    wwxy = models.DecimalField(verbose_name='旺旺响应', default=0, null=True,max_digits=3,decimal_places=2)
    cfmj = models.FloatField(verbose_name='厂房面积', default=0, null=True)
    zrs = models.FloatField(verbose_name='员工人数', default=0, null=True)
    num_comment = models.FloatField(verbose_name='评价数目', default=0, null=True)
    good_percent = models.DecimalField(verbose_name='好评率', default=0, null=True,max_digits=3,decimal_places=2)
    rateAverageStarLevel = models.DecimalField(verbose_name='商品评分', default=0, null=True,max_digits=2,decimal_places=1)
    weight = models.FloatField(verbose_name='重量', default=0, null=True)
    deliverySpeed=models.DecimalField(verbose_name='配送速度',default=0, null=True,max_digits=3,decimal_places=2)
    # picture=models.ImageField(upload_to="test_img/",verbose_name='商品图片',default='static/default.jpg')
    objects = models.Manager()
    class Meta:
        #定义该model不生成表
        abstract = True

    def __str__(self):
        return self.Title
    def show_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<img src='{}' style='width:50px;height:50px;'>".format(self.picture.url))
    show_image.short_description = "商品图片"


#下面所有模型类都继承basemodel
class kikuumodel(Basemodel):
    picture=models.ImageField(upload_to="kikuu_img/",verbose_name='商品图片',default='static/default.jpg')
    class Meta:
        # 修改数据库中的表名，默认表明是 子应用_子应用info
        db_table = 'kikuu'
        # 修改后台admin的显示信息
        verbose_name_plural = 'KIKUU'


class fixmodel(Basemodel):
    #注意：upload_to时图片存放的目录，即在meida/XXXX文件夹下
    picture=models.ImageField(upload_to="fix_img/",verbose_name='商品图片',default='static/default.jpg')

    class Meta:
        # 修改数据库中的表名，默认表明是 子应用_子应用info
        db_table = 'fix'
        # 修改后台admin的显示信息
        verbose_name_plural = 'FIX'


class snatchermodel(Basemodel):
    #注意：upload_to时图片存放的目录，即在meida/XXXX文件夹下
    picture=models.ImageField(upload_to="snatcher_img/",verbose_name='商品图片',default='static/default.jpg')

    class Meta:
        # 修改数据库中的表名，默认表明是 子应用_子应用info
        db_table = 'snatcher'
        # 修改后台admin的显示信息
        verbose_name_plural = 'SNATCHER'


class kilimallmodel(Basemodel):
    picture=models.ImageField(upload_to="kilimall_img/",verbose_name='商品图片',default='static/default.jpg')
    class Meta:
        # 修改数据库中的表名，默认表明是 子应用_子应用info
        db_table = 'kilimall'
        # 修改后台admin的显示信息
        verbose_name_plural = 'KILIMALL'

class valuecomodel(Basemodel):
    picture=models.ImageField(upload_to="valueco_img/",verbose_name='商品图片',default='static/default.jpg')
    class Meta:
        # 修改数据库中的表名，默认表明是 子应用_子应用info
        db_table = 'valueco'
        # 修改后台admin的显示信息
        verbose_name_plural = 'VALUECO'

class dealhubmodel(Basemodel):
    picture=models.ImageField(upload_to="dealhub_img/",verbose_name='商品图片',default='static/default.jpg')
    class Meta:
        # 修改数据库中的表名，默认表明是 子应用_子应用info
        db_table = 'dealhub'
        # 修改后台admin的显示信息
        verbose_name_plural = 'DEALHUB'

class jumiamodel(Basemodel):
    picture=models.ImageField(upload_to="jumia_img/",verbose_name='商品图片',default='static/default.jpg')
    class Meta:
        # 修改数据库中的表名，默认表明是 子应用_子应用info
        db_table = 'jumia'
        # 修改后台admin的显示信息
        verbose_name_plural = 'JUMIA'

class jjshousemodel(Basemodel):
    picture=models.ImageField(upload_to="jjshouse_img/",verbose_name='商品图片',default='static/default.jpg')
    class Meta:
        # 修改数据库中的表名，默认表明是 子应用_子应用info
        db_table = 'jjshouse'
        # 修改后台admin的显示信息
        verbose_name_plural = 'JJSHOUSE'


class lovelywholesalemodel(Basemodel):
    picture=models.ImageField(upload_to="lovelywholesale_img/",verbose_name='商品图片',default='static/default.jpg')

    class Meta:
        # 修改数据库中的表名，默认表明是 子应用_子应用info
        db_table = 'lovelywholesale'
        # 修改后台admin的显示信息
        verbose_name_plural = 'LOVELYWHOLE'


class wholesale7model(Basemodel):
    picture=models.ImageField(upload_to="wholesale7_img/",verbose_name='商品图片',default='static/default.jpg',null=True)

    class Meta:
        # 修改数据库中的表名，默认表明是 子应用_子应用info
        db_table = 'wholesale7'
        # 修改后台admin的显示信息
        verbose_name_plural = 'WHOLESALE7'


class bidorbuymodel(Basemodel):
    picture=models.ImageField(upload_to="bidorbuy_img/",verbose_name='商品图片',default='static/default.jpg',null=True)

    class Meta:
        # 修改数据库中的表名，默认表明是 子应用_子应用info
        db_table = 'bidorbuy'
        # 修改后台admin的显示信息
        verbose_name_plural = 'BIDORBUY'


class ackermansmodel(Basemodel):
    picture=models.ImageField(upload_to="ackermans_img/",verbose_name='商品图片',default='static/default.jpg',null=True)

    class Meta:
        db_table = 'ackermans'
        verbose_name_plural = 'ACKERMANS'


class cjdropshippingmodel(Basemodel):
    picture=models.ImageField(upload_to="cjdropshipping_img/",verbose_name='商品图片',default='static/default.jpg',null=True)

    class Meta:
        db_table = 'cjdropshipping'
        verbose_name_plural = 'CJDROPSHOPPING'


class mrpmodel(Basemodel):
    picture=models.ImageField(upload_to="mrpmodel_img/",verbose_name='商品图片',default='static/default.jpg',null=True)

    class Meta:
        db_table = 'mrp'
        verbose_name_plural = 'MRP'


class zandomodel(Basemodel):
    picture=models.ImageField(upload_to="zandomodel_img/",verbose_name='商品图片',default='static/default.jpg',null=True)

    class Meta:
        db_table = 'zando'
        verbose_name_plural = 'ZANDO'


class yellowsubtradingmodel(Basemodel):
    picture=models.ImageField(upload_to="yellowsubtradingmodel_img/",verbose_name='商品图片',default='static/default.jpg',null=True)

    class Meta:
        db_table = 'yellowsubtrading'
        verbose_name_plural = 'YELLOW SUBTRADING'

class settingmodel(models.Model):
    name=models.CharField(max_length=100,verbose_name='电商名称',primary_key=True)
    hour=models.IntegerField(verbose_name='小时',default=0)
    minute=models.IntegerField(verbose_name='分钟',default=0)
    objects=models.Manager()
    def __str__(self):
        return self.name
    class Meta:
        # 修改数据库中的表名，默认表明是 子应用_子应用info
        db_table = 'setting'
        # 修改后台admin的显示信息
        verbose_name_plural = '配置数据'























