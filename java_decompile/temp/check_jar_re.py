import re

re_str_list = [
    "bcprov-jdk.*\.jar",
    "catalina.*\.jar",
    "tomcat.*\.jar",
    "servlet-api.*\.jar",
    "el-api.jar",
    "junit-.*\.jar",
    "ecj-.*\.jar",
    "quartz-.*\.jar",
    "commons-.*\.jar",
    "zookeeper-.*\.jar",
    "spring-.*\.jar",

]


with open('../uncompile_file', 'wb') as f:
    for item in re_str_list:
        f.write(bytes(item, encoding = "utf-8"))
        f.write(bytes("\n", encoding = "utf-8"))


re_white_package = []
with open('../uncompile_file', 'r') as f:
    for item in f:
        re_white_package.append(re.compile(item.strip()))


print(re_white_package)
for item in re_white_package:
    print(item.match("bcprov-jdk=123123123.jar"))