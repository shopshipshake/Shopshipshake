# E-Commercial-DataCrawl

简介：
本项目用于 服务电商运营部门选品，并利用Django框架搭建后台管理系统。数据库将存储所有爬取到的数据并通过后台管理系统可视化。使用人员可以通过后台管理系统通过筛选选出理想的商品。这个功能将有效提高选品的效率，并赋能于公司其他部门。


配置环境：
需要python3以上版本。

所需要的包：requests，selenium，pymysql，threading，lxml， oss2， goto

Django版本: 2.2 （根据需求以及兼容性适当做出些修改）

goto安装不上可以安装goto-statement

当前已有爬虫代码的南非独立站：KIKUU, FIX, JJHOUSE, SNATCHER, LOVELYWHOLE, KILIMALL, DEAL-HUB, VALUECO, JUMIA, BIDORBUY, ACKERMANS, CJDROPSHIPPING, MRP, ZANDO, YELLOWSUBTRADING d等（不排除这些网站会更新而导致代码没法用的情况）。

如果该网站是基于shopify建站，则可通过 https://github.com/lagenar/shopify-scraper.git 内的代码完成爬取。不需要重新编写爬虫代码。所有的爬虫代码在crawl/stage1 里面呈现。

爬虫代码分为三个阶段。第一阶段是爬取南非独立站，我们获得每个商品独立的ID，标题，价格，和最重要的图片链接。ID作为唯一的标识符，可以用作去重的标准。

第二阶段通过调取1688api: https://open.1688.com/api/apiTool.htm?ns=com.alibaba.linkplus&n=alibaba.cross.similar.offer.search&v=1 ，从而通过图片获取相关供应商的信息。可以按照公司的需求选取销量优先还是价格低廉优先。

第三阶段：当拥有1688供应商的链接后，通过爬取每个供应商页面的相关信息作为选取商品的标准。代码中选取的标准为：已售商品数量、服务能力、回头率、旺旺响应、厂房面积、员工人数、评价数目、好评率、商品评分、重量、配送速度。

操作方法：
先run任意一个drive

关于电商选品的内容以及其他电商相关内容，欢迎关注ShopShipShake语雀：https://shopshipshake.yuque.com/shopshipshake/commerce_events/niprt0

Project Owner: Alvin Rong

Main Contributor: Chenchuhui Hu, Chenyun Zhang, Alvin Rong, Ruiqing Shi
