import pandas as pd
import numpy as np
from datetime import datetime
import os
import matplotlib.pylab as plt

def sales_analytics():

    filename = "Week 2/Day 5/sales analytics files/sales_dataset.csv"
    fnn = "Week 2/Day 5/sales analytics files/sales_dashboard.xlsx"

    def get_data(filename):
        try:
            df = pd.read_csv(filename, sep =',', header = 0, na_values = ['nan','NaN','N/A', 'NA'])
            df.replace(['nan','NaN','NAN','None','N/A','NA'],np.nan)
            return df

        except Exception as e:
            print(f"Unable to get data: {e}")

    def load_prepare_data(df):
        try:
            df['date'] = pd.to_datetime(df['date'], errors = 'coerce')
            df['revenue'] = df['price']*df['quantity']
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month_name()
            df['quarter'] = 'Q' + df['date'].dt.quarter.astype(str)
            print("Updated Dataframe:")
            print(df)
            return df

        except Exception as e:
            print(f"Data load failed: {e}")

    def advanced_filter(df):
        try:
            filter_df = df
            p_found = False
            c_found = False
            print(df)
            print(" ")
            while True:
                print("INTERACTIVE FILTER")
                print("1. Date Range")
                print("2. Product/Category")
                print("3. Revenue Range")
                print("4. Region based")
                print("5. Quit")

                ch = input("Enter a valid choice from (1-5): ")

                if ch == "1":
                    start = input("Enter start date(YYYY-MM-DD): ")
                    end = input("Enter end date(YYYY-MM-DD): ")
                    start_date = pd.to_datetime(start, errors = 'coerce')
                    end_date = pd.to_datetime(end, errors = 'coerce')
                    print("Data Based on Date range:")
                    filter_df = filter_df.query('date >= @start_date and date <= @end_date')
                    print(filter_df)

                elif ch == "2":
                    print("Do you want to filter based on Product or Category?")
                    pc = input("For Product type 'P', for Category type 'C', to quit press 'Q': ")
                    if pc.upper() == 'P':
                        p = input("Enter the product name: ")
                        filter_df= filter_df.query('product == @p')
                        print(filter_df)
                        p_found = True
                    elif pc.upper() == 'C':
                        c = input("Enter the Category: ")
                        filter_df = filter_df.query('category == @c')
                        print(filter_df)
                    else:
                        print("Invalid choice")

                elif ch == "3":
                    s = int(input("Starting range: "))
                    e = int(input("Ending range: "))
                    r = filter_df.query('revenue>=@s and revenue<=@e')
                    filter_df = r.sort_values(['revenue'], ascending = True)
                    print(filter_df)

                elif ch == '4':
                    re = input("Enter the region: ")
                    re = re.title()
                    filter_df = filter_df.query('region == @re')
                    print(filter_df)

                elif ch == '5':
                    print('Quitting')
                    break
                else:
                    print("Invalid choice")

            return filter_df

        except Exception as e:
            print(f"Advanced filter failed: {e}")

    def multidimensional_analysis(df):
        try:
            reg_df = df.groupby('region')[['price','quantity']].sum()
            prod_df = df.groupby('product')[['price', 'quantity']].sum()
            quarter_df = df.groupby('quarter')[['price','quantity']].sum()
            rev_df = df.groupby('quarter')[['revenue']].sum()
            ind_df = df.groupby('salesperson')[['revenue']].max()

            print("\nRegion based sales:\n")
            print(reg_df)
            print("\nProduct based sales:\n")
            print(prod_df)
            print("\nSales distribution based on quarters:\n")
            print(quarter_df)
            print("\nRevenue for Quarters:\n")
            print(rev_df)
            print("\nTop sales person by revenue:")
            print(ind_df)

            while True:
                print("Analysis options:")
                print("1. Region x Product performance")
                print("2. Month x Category trends")
                print("3. Salesperson x Region results")
                print("4. Quit")

                ch = input("Enter the choice between 1-5: ")

                if ch == "1":
                    pv = df.pivot_table(index = 'region', columns = 'product', values = 'revenue', aggfunc = 'sum')
                    print("\nRegion x Product performance: \n")
                    print(pv)

                elif ch == "2":
                    pv = df.pivot_table(index = 'month', columns = 'category', values = 'revenue', aggfunc = 'sum')
                    print("\nMonth x Category performance: \n")
                    print(pv)
                
                elif ch == "3":
                    pv = df.pivot_table(index = 'salesperson', columns = 'region', values = 'revenue', aggfunc = 'sum')
                    print("\nSalesperson x Region results: \n")
                    print(pv)

                elif ch == "4":
                    print("Quitting")
                    break

                else:
                    print("Invalid choice")
            
            return pv
        
        except Exception as e:
            print(f"Multi dimensional analysis failed: {e}")

    def time_series_analysis(df):
        try: 
            weekly = df.resample('W', on='date').agg({'price': 'sum', 'quantity':'sum'})
            print("Weekly Analysis:")
            print(weekly)
            daily = df.resample('D', on='date').agg({'price': 'sum', 'quantity':'sum'})
            print("Daily Analysis:")
            print(daily)
            quarterly = df.resample('QE', on='date').agg({'price': 'sum', 'quantity': 'sum'})
            print("Quarterly Analysis:")
            print(quarterly)

            df_ind = df.set_index('date').sort_index()
            df_sales = df_ind.resample('D')[['quantity', 'price']].sum()
            rolling_avg_weekly = df_ind[['price','quantity']].rolling(window= '7D').mean()
            print("Weekly average on growth:")
            print(rolling_avg_weekly.head(10))

            rolling_avg_monthly = df_sales['quantity'].rolling(window = 30, min_periods = 1).mean().sort_values(ascending = False)
            print("Monthly average on growth:")
            print(rolling_avg_monthly.head(10))

            rolling_avg_weekly.plot(title = 'Weekly sales', fig = (10,5), kind = 'hist', bins = 10, edgecolor = 'black' )
            plt.xlabel('price')
            plt.ylabel('quantity')
            plt.show()

            rolling_avg_monthly.plot(title = 'Daily sales', fig = (10,5))
            plt.ylabel('quantity')
            plt.show()

            return rolling_avg_weekly, rolling_avg_monthly

        except Exception as e:
            print(f"Time series Analysis failed: {e}")

    def comparative_analysis(df):
            try:
                print("Monthly Sales Report:")
                monthly_sales = df.resample('ME', on='date')['quantity'].sum().to_frame()
                monthly_sales['last_month'] = monthly_sales['quantity'].shift(1)
                monthly_sales['MoM sales'] = ((monthly_sales['quantity']- monthly_sales['last_month'])/monthly_sales['last_month'])*100
                print(monthly_sales)

                print("Weekly Sales Report:")
                weekly_sales = df.resample('W', on = 'date')['quantity'].sum().to_frame()
                weekly_sales['weekend'] = weekly_sales['quantity'].shift(1)
                weekly_sales['WoW sales'] = ((weekly_sales['quantity']-weekly_sales['weekend'])/weekly_sales['weekend'])*100
                print(weekly_sales)

                print("Quarterly Sales Report:")
                quarterly_sales = df.resample('QE', on = 'date')['quantity'].sum().to_frame()
                quarterly_sales['last_quarter'] = quarterly_sales['quantity'].shift(4)
                quarterly_sales['QoQ Sales'] = ((quarterly_sales['quantity']-quarterly_sales['last_quarter'])/quarterly_sales['last_quarter'])*100
                print(quarterly_sales)

                return monthly_sales,weekly_sales,quarterly_sales

            except Exception as e:
                print(f"Time Analysis failed: {e}")

    

    def export_sheets(df,filter_df,pv,rolling_avg_weekly, rolling_avg_monthly,monthly_sales,weekly_sales,quarterly_sales,fnn):
        try:
            with pd.ExcelWriter(fnn, engine = "openpyxl") as writer:
                df.to_excel(writer, sheet_name = 'Source Data',index = True)
                filter_df.to_excel(writer, sheet_name = 'Filtered Data', index = True)
                pv.to_excel(writer, sheet_name = 'Pivot Tables', index = True)
                rolling_avg_weekly.to_excel(writer, sheet_name = 'Weekly rollimg average', index = True)
                rolling_avg_monthly.to_excel(writer, sheet_name = 'Monthly rolling average', index = True)
                monthly_sales.to_excel(writer, sheet_name = 'Monthly growth rate', index = True)
                weekly_sales.to_excel(writer, sheet_name = 'Weekly growth rate', index = True)
                quarterly_sales.to_excel(writer, sheet_name = 'Quarterly growth rate', index = True)

            print(f"Data has been successfully exported to the path: {fnn}")
        
        except Exception as e:
            print(f"Data Export failed: {e}")
            
            

    piv = None
    filters = None
    raw = None
    ram = None
    mom = None
    wow = None
    qoq = None

    data = get_data(filename)

    if data is None:
        print("Failed to load initial data")
        return
    
    while True:
        print("SALES ANALYTICS SYSTEM")
        print("1. Load Data")
        print("2. Apply advanced filter")
        print("3. MultiDimensional Analysis")
        print("4. Time series analysis")
        print("5. Comparative Analysis")
        print("6. Export data")
        print("7. Quit")

        ch = input("Enter a choice between 1-7: ")
        if ch == "1":
            data = load_prepare_data(data)
        elif ch == "2":
            filters= advanced_filter(data)
        elif ch == "3":
            piv = multidimensional_analysis(data)
        elif ch == "4":
            raw,ram=time_series_analysis(data)
        elif ch == "5":
            mom, wow, qoq = comparative_analysis(data)
        elif ch == "6":
            export_sheets(data,filters,piv,raw,ram,mom,wow,qoq,fnn)




sales_analytics()