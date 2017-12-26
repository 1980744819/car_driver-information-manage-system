# car_driver information manage system
## 需求文件

>运行平台 windows   
python3  版本：3.6.1  
MSSQL server 2017  
Flask (0.12.2)  
Flask-Bootstrap (3.3.7.1)  
Flask-Login (0.4.1)  
Flask-Migrate (2.1.1)  
Flask-Moment (0.5.2)  
Flask-MySQL (1.4.0)  
Flask-Script (2.0.6)  
Flask-SQLAlchemy (2.3.2)  
Flask-WTF (0.14.2)  
pymssql (2.1.3)  
virtualenv (15.1.0)  
Jinja2 (2.10)  
WTForms (2.1)  

## 简介

### 课程设计要求

 实践环节要求学生能够独立按预定题目开发出功能完善的小型管理信息系统。  
1. 握管理信息系统的开发方法学、各阶段的步骤、基本技术与方法；  
1. 要求规范化完成系统设计、实施与转换、调试、运行、管理与维护等阶段；  
1. 能够编写开发过程各阶段的主要文档；   
1. 要求提交系统说明书、用户手册、设计报告；  
1. B/S结构，SQL Server数据库  
1. 要求提交开发源代码  
1. 实践环节终了要求进行系统功能演示。  


数据库课程设计题目
### 题目：
>    实践内容30运输企业车辆信息管理系统
建立一套运输企业车辆信息管理系统，实现司机、车辆信息的系统化管理。  
*功能包括:*  
（1）用户管理：注册用户，设定权限，登录系统；  
（2）司机基本信息（驾照信息）的录入、查询、修改  
（3）车辆基本信息、驾照信息的录入、查询、修改  
（4）车辆维修信息的录入、查询、修改  

### 开发简介

* 基于flask实现的车辆信息管理系统
* UI框架使用bootstrap进行美化
* 数据库使用microsoft SQL server
* html使用jinja2模板引擎渲染
* 数据库仓库迁移使用flask-Migrate
* Flask-Moment 本地化时间和日期
* Flask-AQLAlchemy 管理数据库
* python shell 命令行启动与管理
* Flask-Login 认证用户
* Flask-WTF 渲染表单

#### 数据库table

* User  
  | 列| id | user_id | nick_name | password |
  |:--|:----|:---------|:---------|:---------|
  |说明 | 主键|用户编号 | 昵称 |密码 |
  | 类型|Integer |String(10) |Unicode(32) |String(32) |  

*Admin  
  |列 | id | admin_id |  
  |:-|:----|:----------|  
  |说明 | 主键 |用户编号|
  | 类型|Integer|String(10)

*DriverInfo
 |列|id| driver_id| license_id|real_name |
 |:-|:-|:-|:-|:-|
 | 说明|主键 |用户编号 |驾照编号 |真实姓名 |
 | 类型|Integar |String(10) |String(20) |Unicode(32) |

*CarInfo
 | 列|id |car_id |bought_time |car_type |driver_id |
 |:- |:- |:- |:- |:- |:- |
 | 说明|主键 |车辆编号 |购买日期(年/月) |车辆型号 |驾驶人编号 |
 | 类型|Integar |String(32) |String(10) |String(32) |String(10) |

*RepairRecord
| 列|id |car_id |broken_time |fee |is_fixed|
|:-|:-|:-|:-|:-|:-|
|说明|主键|车辆编号|损坏时间|花费|是否修好|
|类型|Integar|String(32)|String(10)|Integar|Boolean|

* 各个表格时间的关系

    *    User.user_id => Admin.admin_id => DriverInfo.driver_id => CarInfo.driver_id  
    *    CarInfo.car_id => RepairRecord.car_id  



#### 项目文件结构

[文件结构树位于tree.txt文件夹](./tree.txt)

#### 运行

进入app文件夹(包含run.py的文件夹)
>python3 run.py runserver

运行服务器  
本地浏览器访问127.0.0.1:5000即可访问主页面

                






