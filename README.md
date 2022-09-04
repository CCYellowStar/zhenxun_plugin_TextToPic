# zhenxun_plugin_TextToPic
使用[wenxinApi](https://wenxin.baidu.com/moduleApi/ernieVilg)以文字描述生成各种风格图片的真寻插件  

效果如下：  
![image](https://user-images.githubusercontent.com/47291058/188303503-c1c742e6-f02c-4279-acf9-ce75db624902.png)  
一次生成6张，生成时间在30秒到2分钟，如果在群聊状态会自动合并为转发消息  

## 安装方法  
先安装wenxin官方模块  
在真寻虚拟环境下`pip install wenxin-api`  
然后将`release`里的发行压缩包里的插件文件放到真寻第三方插件目录（没有手动指定就放到`extensive_plugin`）  
第一次安装请先运行一次机器人，插件加载完后关闭，然后在`config.yaml`里刚生成的  ![image](https://user-images.githubusercontent.com/47291058/188303838-dee6e862-9641-467d-8459-e5f2fb3cbc02.png)  
填入从https://wenxin.baidu.com/moduleApi/key 获取的ak和sk  
每个手机号绑定的账号每天只有50次的普通用户调用上限！


## 使用方法
使用指令为 `以文生图 图片风格 图片描述` 风格可以是：油画、水彩、卡通、粉笔画、儿童画、蜡笔画  
