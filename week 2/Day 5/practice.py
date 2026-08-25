import pandas as pd


def practice():
#     df = pd.DataFrame({
#     'product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Webcam'],
#     'price': [1200, 25, 75, 300, 150],
#     'quantity': [5, 50, 30, 10, 20],
#     'category': ['Electronics', 'Accessories', 'Accessories', 'Electronics', 'Electronics']
#     })

# # YOUR TASKS:
# # 1. Use .query() to find products with price > 100
#     p = df.query('price>100')
#     print(p)
# # 2. Use .query() to find Accessories with quantity > 25
#     q = df.query('quantity > 25')
#     print(q)
# # 3. Use .query() to find products where price * quantity > 1000
#     df['prod'] = df['price']*df['quantity']
#     pq = df.query('prod>1000')
#     print(pq)
# # 4. Use variable in query to find products above average price
#     avg = df['price'].sum()/len(df)
#     a = df.query('price>@avg')
#     print(a)

#     df = pd.DataFrame({
#     'name': ['Alice Johnson', 'Bob Smith', 'Charlie Anderson', 'Diana Johnson'],
#     'email': ['alice@company.com', 'bob@example.org', 'charlie@company.com', 'diana@other.net'],
#     'phone': ['555-1234', '555-5678', '555-9012', '555-3456']
#     })

# # YOUR TASKS:
# # 1. Find names containing 'Johnson'
#     n = df['name'].str.contains('Johnson')
#     print(n)
# # 2. Find emails ending with '.com'
#     p =df['email'].str.endswith('.com')
#     print(p)
# # 3. Find phone numbers starting with '555-5'
#     c = df['phone'].str.startswith('555-5')
#     print(c)
# # 4. Find names starting with 'A' OR 'D'
#     d = df['name'].str.startswith(('A','D'))
#     print(d)

#     df = pd.DataFrame({
#     'department': ['Sales', 'Sales', 'Engineering', 'Engineering', 'Sales', 'HR'],
#     'employee': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'],
#     'salary': [50000, 60000, 75000, 80000, 55000, 58000],
#     'years': [3, 5, 7, 10, 4, 6]
#     })

# # YOUR TASKS:
# # 1. Calculate average salary by department
#     dept = df.groupby('department')['salary'].mean()
#     print(dept)
# # 2. Count employees per department
#     emp = df.groupby('department')['employee'].count()
#     print(emp)
# # 3. Find min and max years of experience per department
#     exp = df.groupby('department')['years'].agg(['max','min'])
#     print(exp)
# # 4. Calculate total salary cost per department
#     sal = df.groupby('department')['salary'].sum()
#     print(sal)

#     print("complex aggregations")

#     # YOUR TASKS:
# # 1. Group by department and show sum, mean, count for salary
#     cou = df.groupby('department')['salary'].agg(['sum','mean','count'])
#     print(cou)
# # 2. Add a column showing each employee's salary as % of department total
#     df['percent'] = ((df['salary']/df.groupby('department')['salary'].transform(sum))*100).round(2)
#     print(df)
# # 3. Filter to keep only departments with more than 1 employee
#     dep = df.groupby('department').filter(lambda x: len(x)>1)
#     print(dep)
# # 4. Create a summary showing department, employee count, and avg salary
#     summary = df.groupby('department').agg({'employee': 'count', 'salary': 'mean'})
#     summ = df.groupby('department').agg(employee_count = ('employee','count'), avg_salary = ('salary','mean'))
#     print(summary)
#     print(summ)

#     employees = pd.DataFrame({
#     'emp_id': [1, 2, 3, 4, 5],
#     'name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve'],
#     'dept_id': [10, 20, 10, 30, 20]
#     })

#     departments = pd.DataFrame({
#     'dept_id': [10, 20, 30],
#     'dept_name': ['Sales', 'Engineering', 'HR'],
#     'location': ['Boston', 'NYC', 'Chicago']
#     })

# # YOUR TASKS:
# # 1. Inner join employees and departments
#     inner = pd.merge(employees,departments,on = 'dept_id', how = 'inner')
#     print(inner)
# # 2. Left join to keep all employees
#     left = pd.merge(employees,departments,on='dept_id',how='left')
#     print(left)
# # 3. Add department name and location to employees
#     emp = pd.merge(employees,departments,on = 'dept_id', how = 'left')
#     print(emp)
# # 4. Find employees without a valid department (if any)
#     valid = pd.merge(employees, departments, on = 'dept_id', how = 'left', indicator =True)
#     orphan = valid[valid['_merge'] == 'left_only']
#     print(orphan)

    df = pd.DataFrame({
    'month': ['Jan', 'Jan', 'Feb', 'Feb', 'Mar', 'Mar'],
    'product': ['A', 'B', 'A', 'B', 'A', 'B'],
    'sales': [100, 150, 120, 160, 140, 170]
})

# YOUR TASKS:
# 1. Create pivot table with months as rows, products as columns
    pi = df.pivot_table(index = 'month',columns = 'product', values = 'sales')
    print(pi)
# 2. Add row and column totals
    piv = df.pivot_table(index ='month',columns = 'product', values = 'sales', aggfunc = 'sum')
    print(piv)
# 3. Melt the pivoted table back to long format
    pivo = pd.DataFrame({
        'product': ['A', 'B'],
        'Jan': [100, 150],
        'Feb': [120, 160],
        'Mar': [140, 170]
    })
    melt = pivo.melt(id_vars='product',var_name='month',value_name='sales')
    print(melt)
# 4. Calculate total sales per month
    addi = melt.groupby('month')['sales'].sum()
    print(addi)


practice()