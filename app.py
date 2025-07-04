from faker import Faker
import random
import datetime
import csv

fake = Faker('zh_CN')  # 使用中文数据

# 全局变量
# PROJECT_STATUS = ['进行中', '已完成', '已暂停', '已取消']
PROJECT_STATUS = ['进行中']
EMPLOYEE_STATUS = ['在职', '离职']
GENDERS = ['男', '女']
DEPARTMENTS = ['技术部', '销售部', '人事部', '财务部', '市场部']
POSITIONS = {
    '技术部': ['前端工程师', '后端工程师', '测试工程师', '架构师'],
    '销售部': ['销售代表', '销售经理'],
    '人事部': ['HR专员', '人事经理'],
    '财务部': ['会计', '出纳', '财务主管'],
    '市场部': ['市场专员', '市场经理']
}
TIME_TYPES = ['开发', '测试', '会议', '培训', '出差']

# 存储主键用于关联
projects = []
employees = []

# 生成项目列表
def generate_projects(n=30):
    with open('项目列表.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', '项目名称', '项目描述', '项目状态', '开始时间', '结束时间', '项目创建时间', '项目更新时间'])

        for i in range(1, n + 1):
            start_date = fake.date_between(start_date=datetime.datetime(2013,6,6), end_date=datetime.datetime(2020,12,31))
            end_date = fake.date_between(start_date=start_date, end_date=datetime.datetime(2020,12,31)) if random.random() > 0.3 else None
            status = random.choice(PROJECT_STATUS)
            if end_date is None and status == '已完成':
                status = '进行中'

            created_at = fake.date_time_between(start_date=datetime.datetime(2013,6,6), end_date=datetime.datetime(2020,12,31))
            updated_at = fake.date_time_between(start_date=created_at, end_date=datetime.datetime(2020,12,31)) if random.random() > 0.2 else created_at

            project = {
                'ID': i,
                '项目名称': fake.catch_phrase(),
                '项目描述': fake.text(100),
                '项目状态': status,
                '开始时间': start_date,
                '结束时间': end_date,
                '项目创建时间': created_at,
                '项目更新时间': updated_at
            }
            projects.append(project)
            writer.writerow([
                project['ID'],
                project['项目名称'],
                project['项目描述'],
                project['项目状态'],
                project['开始时间'],
                project['结束时间'],
                project['项目创建时间'],
                project['项目更新时间']
            ])

# 生成员工信息
def generate_employees(n=15):
    with open('员工信息表.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['员工ID', '员工姓名', '员工性别', '员工电话', '员工邮箱', '员工状态', '员工职位', '员工部门', '员工入职时间', '员工离职时间', '备注'])

        for i in range(1, n + 1):
            dept = random.choice(DEPARTMENTS)
            position = random.choice(POSITIONS[dept])
            gender = random.choice(GENDERS)
            name = fake.name_male() if gender == '男' else fake.name_female()

            entry_date = fake.date_between(start_date=datetime.datetime(2013,6,6), end_date=datetime.datetime(2020,12,31))
            status = random.choices(EMPLOYEE_STATUS, weights=[0.8, 0.2])[0]
            leave_date = fake.date_between(start_date=entry_date, end_date=datetime.datetime(2020,12,31)) if status == '离职' else None

            employee = {
                '员工ID': i,
                '员工姓名': name,
                '员工性别': gender,
                '员工电话': fake.phone_number(),
                '员工邮箱': fake.email(),
                '员工状态': status,
                '员工职位': position,
                '员工部门': dept,
                '员工入职时间': entry_date,
                '员工离职时间': leave_date,
                '备注': fake.sentence() if random.random() > 0.7 else ''
            }
            employees.append(employee)
            writer.writerow([
                employee['员工ID'],
                employee['员工姓名'],
                employee['员工性别'],
                employee['员工电话'],
                employee['员工邮箱'],
                employee['员工状态'],
                employee['员工职位'],
                employee['员工部门'],
                employee['员工入职时间'],
                employee['员工离职时间'],
                employee['备注']
            ])

# 生成项目收入明细
def generate_income():
    with open('项目收入明细.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['收入ID', '项目ID', '收入日期', '收入金额', '收入备注'])
        income_id = 1
        for project in projects:
            if project['项目状态'] in ['进行中', '已完成']:
                # 每个项目生成 n-m 条收入记录
                num = random.randint(2000, 3000)
                for _ in range(num):
                    date = fake.date_between(start_date=project['开始时间'], end_date=project['结束时间'] or datetime.datetime(2020,12,31))
                    amount = round(random.uniform(5000, 100000), 2)
                    writer.writerow([income_id, project['ID'], date, amount, fake.sentence()])
                    income_id += 1

# 生成项目支出明细
def generate_expense():
    with open('项目支出明细.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['支出ID', '项目ID', '支出日期', '支出金额', '支出备注'])
        expense_id = 1
        for project in projects:
            if project['项目状态'] in ['进行中', '已完成']:
                num = random.randint(50, 10000)
                for _ in range(num):
                    date = fake.date_between(start_date=project['开始时间'], end_date=project['结束时间'] or datetime.datetime(2020,12,31))
                    amount = round(random.uniform(2000, 5000000), 0)
                    writer.writerow([expense_id, project['ID'], date, amount, fake.sentence()])
                    expense_id += 1

# 生成员工工资明细
def generate_salary():
    with open('员工工资明细.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # 只写部分关键字段（太多字段了，可按需扩展）
        writer.writerow(
            ['工资ID', '员工ID',
             '本月工时', '本月时薪', '本月销售额度', '本月销售提成比例', '本月销售提成额度',
             '本月项目补助', '本月住房补助', '本月交通补助', '本月通讯补助', '本月伙食补助', '本月高温补助', '本月取暖补助', '本月其他补助',
             '本月单位养老保险金额', '本月个人养老保险金额', '本月单位医疗保险金额', '本月个人医疗保险金额',
             '本月单位失业保险金额', '本月个人失业保险金额',
             '本月单位工伤保险金额', '本月单位生育保险金额', '本月单位公积金金额', '本月个人住房公积金金额',
             '本月工资日期', '本月工资金额', '本月总投入金额', '创建日期', '备注'])
        salary_id = 1
        for emp in employees:
            if emp['员工状态'] == '在职':
                hours = round(random.uniform(136, 200), 0)
                hourly_rate = random.choice([50, 80, 100, 150, 200])
                sales = 0
                if emp['员工部门'] == '销售部':
                    sales = round(random.uniform(0, 300000), 0)
                    commission_rate = 0.03
                    commission = sales * commission_rate
                else:
                    commission = 0
                    commission_rate = 0

                # 特殊人才时薪为 255、600 元
                hourly_rate = (600.0 if random.random() < 0.001 else 225.0) if random.random() < 0.002 else hourly_rate
                base_salary = float(hours * hourly_rate)
                base_salary_unit = 30000 if base_salary > 30000 else base_salary
                # 本月单位养老保险金额
                unit_1 = round(base_salary_unit * 0.20, 0)
                # 本月个人养老保险金额
                personal_1 = round(base_salary_unit * 0.08, 0)
                # 本月单位医疗保险金额
                unit_2 = round(base_salary_unit * 0.09, 0)
                # 本月个人医疗保险金额
                personal_2 = round(base_salary_unit * 0.02, 0)
                # 本月单位失业保险金额
                unit_3 = round(base_salary_unit * 0.02, 0)
                # 本月个人失业保险金额
                personal_3 = round(base_salary_unit * 0.01, 0)
                # 本月单位工伤保险金额
                unit_4 = round(base_salary_unit * 0.01, 0)
                # 本月单位生育保险金额
                unit_5 = round(base_salary_unit * 0.09, 0)
                # 本月单位公积金金额
                unit_6 = round(base_salary_unit * 0.12, 0)
                # 本月个人住房公积金金额
                personal_6 = round(base_salary_unit * 0.12, 0)
                # 补贴等
                total_salary = base_salary + commission

                pay_date = fake.date_this_month()
                created = fake.date_time_this_month()

                writer.writerow([
                    salary_id,
                    emp['员工ID'],
                    hours,
                    hourly_rate,
                    # 本月销售额度
                    sales,
                    # 本月销售提成比例
                    0.03,
                    # 本月销售提成额度
                    commission_rate,
                    # 本月项目补助
                    500,
                    # 本月住房补助
                    1500,
                    # 本月交通补助
                    500,
                    # 本月通讯补助
                    500,
                    # 本月伙食补助
                    1000,
                    # 本月高温补助
                    500,
                    # 本月取暖补助
                    500,
                    # 本月其他补助
                    0,
                    # 本月单位养老保险金额
                    unit_1,
                    # 本月个人养老保险金额
                    personal_1,
                    # 本月单位医疗保险金额
                    unit_2,
                    # 本月个人医疗保险金额
                    personal_2,
                    # 本月单位失业保险金额
                    unit_3,
                    # 本月个人失业保险金额
                    personal_3,
                    # 本月单位工伤保险金额
                    unit_4,
                    # 本月单位生育保险金额
                    unit_5,
                    # 本月单位公积金金额
                    unit_6,
                    # 本月个人住房公积金金额
                    personal_6,
                    # 本月工资日期
                    pay_date,
                    # 本月工资金额
                    total_salary,
                    # 本月总投入金额
                    total_salary + unit_1 + unit_2 + unit_3 + unit_4 + unit_5 + personal_1 + personal_2 + personal_3 + personal_6,
                    # 创建日期
                    created,
                    # 备注
                    fake.sentence() if random.random() > 0.6 else ''
                ])
                salary_id += 1

# 执行生成
if __name__ == '__main__':
    generate_projects(10)
    generate_employees(10000)
    generate_income()
    generate_expense()
    generate_salary()
    print("✅ 所有测试数据生成完成！")