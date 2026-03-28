import os
import pandas as pd
import numpy as np

def csv_filter():
    
    def get_data(filename):
        try:
            df = pd.read_csv(filename, sep = ',', index_col = 0, header = 0, na_values = ['NaN', 'N/A', 'NA'])
            df.replace(['nan','NAN', 'NaN', 'None', 'N/A', 'n/a'],np.nan)
            df['Phone'] = df['Phone'].str.lstrip("+1").str.split('x').str[0].str.replace(r'[+\-.\(\)]','',regex = True).astype(int)
            df['Date of birth'] = pd.to_datetime(df['Date of birth'], errors = ('coerce'))
            return df

        except Exception as e:
            print(f"Unable to access file: {e}")

    def load_file(df):
        try:
            print(f"Shape of the data: {df.shape[0]}rows x {df.shape[1]}columns")
            print("\nData types of each columns:")
            print(df.dtypes)
            print("\nColumns:")
            for v in df.columns:
                print(v)
            print("\nData preview:")
            print(df.head(5))
            return df

        except Exception as e:
            print(f"Data Load operation failed: {e}")

    def apply_filters(df):
        try:
            print("\nINTERACTIVE FILTER")
            print("\nAvailable columns:")
            print(df.head(5))
            print(df.dtypes)
            result = df
            count = int(input("How many filters you want to apply?: "))
            while count>0:
                col = input("Enter the name of the column you want to apply for: ")
                if col in df.columns and df[col].dtypes == "int64":
                    ch = int(input("Enter the number to be found: "))
                    result = result[result[col] == ch]
                    print("User found")
                    for index, row in result.iterrows():
                        name = row['First Name']+" "+row['Last Name']
                        print(f"Name: {name}")
                        print(f"Gender: {row['Sex']}")
                        print(f"Email: {row['Phone']}")
                        print(f"DOB: {row['Date of birth']}")
                        print(f"Job Title: {row['Job Title']}")

                elif col in df.columns and df[col].dtypes == "str":
                    while True:
                        print("1. Find values that contain")
                        print("2. Starts with")
                        print("3. Ends with")
                        print("4. Exact Value")
                        print("5. Quit")
                        op = input("Select a choice to perform operation:")

                        if op == "5":
                            break

                        if op == "1":
                            word = input("Enter the word to proceed: ")
                            result = result[result[col].str.contains(word)]  

                        elif op == "2":
                            word = input("Enter the word to proceed: ")
                            result = result[result[col].str.startswith(word)]
                    
                        elif op == "3":
                            word = input("Enter the word to proceed: ")
                            result = result[result[col].str.endswith(word)]  
                    
                        elif op == "4":
                            word = input("Enter the word to proceed: ")
                            result = result[result[col]==word]
                            
                        else:
                            print("Invalid value")
                            continue
                        break
                
                else:
                    print("Element access failed")

                count-=1
            print(result)
            return result

        except Exception as e:
            print(f"Filter apply failed: {e}")
    
    def select_columns(df):
        try:
            print("Available columns from the System:")
            i=0
            for v in df.columns:
                    print(f"{i+1}. {v}")
                    i+=1

        except Exception as e:
            print(f"Column selection failed: {e}")
        
    fn = input("Enter the filename(with .csv): ")
    path = "Week 2/Day 4/csv filter files"
    filename = os.path.join(path, fn).replace('\\','/')
    data = get_data(filename)

    if data is not None:
        data = load_file(data)
        #apply_filters(data)
        select_columns(data)
csv_filter()