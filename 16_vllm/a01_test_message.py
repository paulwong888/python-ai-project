json_output_message = """
将下面的内容转为json格式

员工ID,姓名,部门,职位,入职日期,薪资,绩效评级,直属上级ID,项目参与情况
1001,张三,研发部,高级工程师,2018-05-12,15000,A,2001,"项目A,项目C"
1002,李四,市场部,市场专员,2020-03-15,9500,B,2002,"项目B"
1003,王五,研发部,工程师,2019-11-20,12000,B,1001,"项目A,项目D"
1004,赵六,财务部,会计,2017-08-05,11000,A,2003,"项目C"
"""

text_to_sql_message = """
创建产品表
cursor.execute('''
CREATE TABLE products (
product_id INTEGER PRIMARY KEY,
product_name TEXT NOT NULL,
category TEXT NOT NULL,
unit_price REAL NOT NULL,
cost_price REAL NOT NULL,
current_stock INTEGER NOT NULL,
min_stock_level INTEGER NOT NULL
)
''')

创建进货表
cursor.execute('''
CREATE TABLE purchases (
purchase_id INTEGER PRIMARY KEY,
product_id INTEGER NOT NULL,
supplier_id INTEGER NOT NULL,
purchase_date TEXT NOT NULL,
quantity INTEGER NOT NULL,
unit_cost REAL NOT NULL,
total_cost REAL NOT NULL,
FOREIGN KEY (product_id) REFERENCES products (product_id),
FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id)
)
''')

创建销售表
cursor.execute('''
CREATE TABLE sales (
sale_id INTEGER PRIMARY KEY,
product_id INTEGER NOT NULL,
customer_id INTEGER,
sale_date TEXT NOT NULL,
quantity INTEGER NOT NULL,
unit_price REAL NOT NULL,
total_price REAL NOT NULL,
FOREIGN KEY (product_id) REFERENCES products (product_id)
)
''')

创建供应商表
cursor.execute('''
CREATE TABLE suppliers (
supplier_id INTEGER PRIMARY KEY,
supplier_name TEXT NOT NULL,
contact_person TEXT,
phone TEXT,
email TEXT,
address TEXT
)
''')

创建客户表
cursor.execute('''
CREATE TABLE customers (
customer_id INTEGER PRIMARY KEY,
customer_name TEXT NOT NULL,
contact_person TEXT,
phone TEXT,
email TEXT,
address TEXT
)
''')

生成随机数据
供应商数据
suppliers_data = [
(1, '北京供应有限公司', '张三', '13800000001', 'supplier1@example.com', '北京市海淀区'),
(2, '上海优质货源公司', '李四', '13800000002', 'supplier2@example.com', '上海市浦东新区'),
(3, '广州原材料供应商', '王五', '13800000003', 'supplier3@example.com', '广州市天河区'),
(4, '深圳电子零件公司', '赵六', '13800000004', 'supplier4@example.com', '深圳市南山区'),
(5, '杭州科技供应链', '钱七', '13800000005', 'supplier5@example.com', '杭州市西湖区')
]

客户数据
customers_data = [
(1, '第一商场', '陈一', '13900000001', 'customer1@example.com', '北京市朝阳区'),
(2, '二号连锁超市', '刘二', '13900000002', 'customer2@example.com', '上海市静安区'),
(3, '三星电子经销商', '孙三', '13900000003', 'customer3@example.com', '广州市越秀区'),
(4, '四方百货公司', '周四', '13900000004', 'customer4@example.com', '深圳市福田区'),
(5, '五洲商贸中心', '吴五', '13900000005', 'customer5@example.com', '杭州市拱墅区'),
(6, '六合连锁店', '郑六', '13900000006', 'customer6@example.com', '成都市锦江区'),
(7, '七彩电器城', '王七', '13900000007', 'customer7@example.com', '重庆市渝中区'),
(8, '八方食品公司', '冯八', '13900000008', 'customer8@example.com', '武汉市江汉区')
]

产品数据
products_data = [
(1, '笔记本电脑A型', '电子产品', 5999.00, 4500.00, 50, 10),
(2, '智能手机X1', '电子产品', 3999.00, 2800.00, 120, 20),
(3, '办公桌椅套装', '办公家具', 1299.00, 800.00, 30, 5),
(4, '激光打印机P3', '办公设备', 1599.00, 1100.00, 25, 8),
(5, '液晶显示器27寸', '电子产品', 1299.00, 900.00, 60, 15),
(6, '机械键盘K8', '电子配件', 399.00, 250.00, 100, 30),
(7, '无线鼠标M2', '电子配件', 199.00, 120.00, 150, 40),
(8, '移动硬盘1TB', '存储设备', 499.00, 350.00, 80, 20),
(9, '办公文件柜', '办公家具', 899.00, 600.00, 15, 5),
(10, '投影仪H1', '办公设备', 2999.00, 2200.00, 10, 3),
(11, '复印纸A4', '办公耗材', 39.90, 25.00, 500, 100),
(12, '墨盒套装', '办公耗材', 299.00, 180.00, 70, 20),
(13, '电脑包', '配件', 199.00, 120.00, 90, 30),
(14, 'USB集线器', '电子配件', 99.00, 60.00, 120, 40),
(15, '无线耳机', '电子配件', 599.00, 400.00, 85, 25)
]

找出所有库存低于最小库存水平的产品，直接给出SQL语句，不需要解释
对比各产品的进货量和销售量，找出库存周转率最高的5种产品，直接给出sql语句，不要解释
查询所有单价超过1000元的产品及其类别，直接给出sql语句，不要解释
分析每种产品在不同月份的销售情况，并计算同比增长率，直接给出sql语句，不要解释
"""

coding_message = """
编写一个 Python 程序，显示一个球在旋转的六边形内弹跳。
小球应受到重力和摩擦力的影响，而且必须真实地从旋转的墙壁上弹起
"""

gl_message = """
抽一副扑克牌中的一张，告诉你是红色的，这张牌是方块A的概率是多少？
"""

ji_tu_tong_long_message = """
一个动物园里有牛、鸵鸟和蛇，一共有75只动物。
牛、鸵鸟和蛇的腿共有176条，牛角和鸵鸟头与蛇头加起来一共98个。
求有多少头牛、多少只鸵鸟和多少条蛇？
"""

planning_message = """
A带着12块钱去超市买饮料。饮料分为大瓶和小瓶。
其中大瓶(500毫升)3块钱，小瓶(100毫升)1块钱。
喝完之后的空瓶可以继续换饮料，3个大空瓶可以换1个大瓶饮料，
1个大空瓶可以换1个小瓶饮料，4个小空瓶可以换1个小瓶的饮料，5个小空瓶可以换1个大瓶的饮料。
问A最多可以喝多少毫升饮料。
"""

for_number_add_message = """
四个数的和是21，这四个数两两相乘得到的六个积分别是15、18、21、30、35和42。
请求出这四个数分别是多少。
"""

logic_predict_message = """
农夫带着一只老虎、一只羊、一条蛇、一只鸡和一筐苹果要过河。
农夫的船一次只能载农夫和一样东西过河。
已知农夫不在的时候，老虎和羊在一起的话，老虎会吃掉羊，如果鸡也在的话，鸡会阻止老虎吃羊；
农夫不在的时候，蛇和鸡在一起的话，蛇会吃掉鸡，如果老虎也在的话，老虎会阻止蛇吃鸡；
农夫不在的时候羊和苹果在一起的话，羊会吃掉苹果，如果蛇也在的话，蛇会阻止羊吃苹果；
老虎不吃鸡(鸡太小不够老虎塞牙缝的)，蛇不吃苹果(蛇不吃素)。
请问农夫如何才能将老虎、羊、蛇、鸡和苹果安全送到对岸？
"""