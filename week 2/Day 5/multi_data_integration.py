import pandas as pd
import numpy as np

def multi_src():

    emp = "Python-practice/week 2/Day 5/Multi source files/employees.csv"
    sal = "Python-practice/week 2/Day 5/Multi source files/salaries.csv"
    perf = "Python-practice/week 2/Day 5/Multi source files/performance.csv"
    dept = "Python-practice/week 2/Day 5/Multi source files/departments.csv"
    db = "Python-practice/week 2/Day 5/Multi source files/Dashboard.xlsx"

    def load_multiple_data():
        try:
            employee = pd.read_csv(emp, sep = ',', header = 0, na_values = ['NaN', 'nan', 'N/A', 'NA'])
            employee.replace(['NaN', 'NAN', 'None', 'none', 'NA', 'N/A', 'nan'], np.nan)
            salary = pd.read_csv(sal, sep = ',', header = 0, na_values = ['NaN', 'nan', 'N/A', 'NA'])
            salary.replace(['NaN', 'NAN', 'None', 'none', 'NA', 'N/A', 'nan'], np.nan)
            performance = pd.read_csv(perf, sep = ',', header = 0, na_values = ['NaN', 'nan', 'N/A', 'NA'])
            performance.replace(['NaN', 'NAN', 'None', 'none', 'NA', 'N/A', 'nan'], np.nan)
            department = pd.read_csv(dept, sep = ',', header = 0, na_values = ['NaN', 'nan', 'N/A', 'NA'])
            department.replace(['NaN', 'NAN', 'None', 'none', 'NA', 'N/A', 'nan'], np.nan)

            dept_with_no_id = employee['dept_id']
            empty_dept = department[~department['dept_id'].isin(dept_with_no_id)]

            df = pd.merge(employee, department, on='dept_id', how= 'outer')
            df = pd.merge(df, performance, on='emp_id', how = 'outer')
            df = pd.merge(df, salary, on='emp_id', how='outer')

            df['emp_id'] = df['emp_id'].astype('Int64')
            df['hire_date'] = pd.to_datetime(df['hire_date'])
            df['year'] = pd.to_datetime(df['year'], format = '%Y').dt.to_period('Y')

            df.replace(['NaN', 'NAN', 'None', 'none', 'NA', 'N/A', 'nan', 'NaT', 'nat', 'NAT','<NA>'], np.nan)
            print(df)
            return df, empty_dept

        except Exception as e:
            print(f'Unable to load data: {e}')

    def validate_data(df, emp):
        try:
            print("Empty departments:")
            print(emp)
            print("Number of null values in the dataframe(columnwise):\n")
            print(df.isna().sum())
            print(f"\nNumber of duplicates in the dataframe: {df.duplicated().sum()}")
            updated_df = df.dropna()
            updated_df = updated_df.drop_duplicates()
            print("\nUpdated Dataframe:")
            print(updated_df)
            print("Complexities after removing duplicates and nulls:")
            print("\nNull Report:")
            print(updated_df.isna().sum())
            print(f"\nNumber of duplicates in the dataframe: {updated_df.duplicated().sum()}")
            return updated_df

        except Exception as e:
            print(f"data validation failed: {e}")

    def merge_all_data(df):
        try:
            print("Consolidated Dataframe:")
            print(df)
            df['compensation'] = df['base_salary'] + df['bonus']
            df['YoE'] = df.groupby('emp_id')['year'].transform('count')
            df['dept_size'] = df.groupby(['dept_id','year'])['emp_id'].transform('count')
            print("Updates made in Data: Added compensation, YoE, dept_size columns\n")
            print(df)
            return df

        except Exception as e:
            print(f"Data merge failed: {e}")

    def cross_tabulate(df):
        try:
            print("Department x Location employee counts\n")
            dl = df.pivot_table(index = 'dept_name', columns = 'location', values = 'dept_size', aggfunc = 'count')
            print(dl)
            print("Department x Performance rating\n")
            dp = df.pivot_table(index = 'dept_name', columns = 'location', values = 'rating', aggfunc = 'mean').round(2)
            print(dp)
            print("Location x Salary ranges\n")
            ls = df.pivot_table(index = 'dept_name', columns = 'location', values = 'base_salary', aggfunc = 'mean').round(2)
            print(ls)
            return dl, dp, ls

        except Exception as e:
            print(f"Cross tabulation failed: {e}")

    def hierarchial_analysis(df):
        try:
            print("Department ID validation")
            print(df.groupby('dept_name')['dept_size'].agg(['count', 'sum', 'max', 'min']))
            print("\nDepartment based Rating")
            print(df.groupby('dept_name')['rating'].agg(['max','min','mean']).round(1))
            print("\nDepartment based salary dstr.")
            print(df.groupby('dept_name')['base_salary'].agg(['max','min','mean']).round(2))
            print("\nYear based salary dstr.")
            print(df.groupby('year')['base_salary'].agg(['max','min','mean']).round(2))
            print("\nYear based employee count")
            print(df.groupby('year')['emp_id'].agg('count'))
            print("\nYear based rating statistics")
            print(df.groupby('year')['rating'].agg(['max','min','mean']).round(1))
            print("\nLocation based Employee count")
            print(df.groupby('location')['emp_id'].agg('count'))
            print("\nLocation based salary dstr.")
            print(df.groupby('location')['base_salary'].agg(['max','min','mean']).round(2))
            print("\nLocation based performers")
            print(df.groupby('location')['rating'].agg(['max','min','mean']).round(1))

        except Exception as e:
            print(f"Hirarchial analysis failed: {e}")

    def export_excel(db,df, dl, dp, ls):
        try:
            with pd.ExcelWriter(db, engine = 'openpyxl') as writer:
                df.to_excel(writer, sheet_name = 'Final Data', index=False)
                dl.to_excel(writer, sheet_name = 'DepartmentxLocation', index = True)
                dp.to_excel(writer, sheet_name = 'DepartmentxPerformance', index = True)
                ls.to_excel(writer, sheet_name = 'LocationxSalary', index = True)
            print(f"Data Successfully loaded to path: {db}")

        except Exception as e:
            print(f"Export failed: {e}")

    dl = None
    dp = None
    ls = None
    data, empty_dept = load_multiple_data()

    if data is None:
        print("Unable to retreive data")
        return
    
    while True:
        print("Multi-Data Integration System")
        print("1. Load Data")
        print("2. Validate Data")
        print("3. Merge All Data")
        print("4. Cross Tabulate Data")
        print("5. Hierarchial Analysis")
        print("6. Export Data")
        print("7. Quit")

        ch = input("Enter a valid choice from 1-7: ")

        if ch == "1":
            load_multiple_data()
        elif ch == "2":
            data = validate_data(data, empty_dept)
        elif ch == "3":
            data = merge_all_data(data)
        elif ch == "4":
            dl,dp,ls = cross_tabulate(data)
        elif ch == "5":
            hierarchial_analysis(data)
        elif ch == "6":
            export_excel(db,data,dl,dp,ls)
        elif ch == "7":
            print("Quitting....")
            break
        else:
            print("Invalid choice")


multi_src()