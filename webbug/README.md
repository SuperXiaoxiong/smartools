# webbug Instructions

用作信息收集

## Introduction  
1. [freebuf 窥探用户隐私的幕后之眼 – Web Bugs](http://www.freebuf.com/articles/web/23079.html)  
2. [http://www.irongeek.com/i.php?page=security/webbugs](http://www.irongeek.com/i.php?page=security/webbugs)

## now

163 网页，手机客户端，outlook 网页，手机客户端均没有做防御  
目前收集 ip , port, os, encode, lang, useragent  

## technical Points

### basis

 ```webbug.php```受访页面，记录信息，大数据服务社会，让生活更美好

 ```db.sql``` 数据库写入语句

### Expand

#### apache重定向	

1. 开启apache rewrite模块，只需要将httpd.conf配置文件中#LoadModule rewrite_module modules/mod_rewrite.so 前面的#号去掉就行

2. 在DocumentRoot里添加重定向

		DocumentRoot "/var/www"
		<Directory "/var/www">
		......
		RewriteEngine On
    	Redirect /webbug/webbug.bmp /webbug/webbug.php
		......
		</Directory>

3. 重启服务器

		sudo /usr/local/apache2/bin/apachectl restart

## TODO:  
1. **google图片检测代理？？？？**
2. 集合使用webrtc收集内网ip  
3. apache服务器上设置，重定向 ，绕过图片检测                      #ok
4. 提高网站安全性 
