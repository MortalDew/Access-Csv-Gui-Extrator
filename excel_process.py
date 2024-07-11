import glob
import csv
import pandas as pd
import xlsxwriter
from dask import dataframe as df1
#test-access-db
def type_previw(name, true_types:bool):
    for filename in glob.glob(name + "/*.csv"):
        if (true_types):
            with open(filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter = ',')
                list_of_column_names = []
                for row in csv_reader:
                    list_of_column_names.append(row)
                    break
                return list_of_column_names[0]
        else:
            return [
                    "LandType", "LandCode", "Username",
                    "SOATO", "Area_ga", "Forma22",
                    "Oblast", "Rayon", "R_zem",
                    "Shape_Length", "Shape_Area",
                ],

def excel_process(name, list):
    # print(list)
    for filename in glob.glob(name + "/*.csv"):
        dask_df = df1.read_csv(
            filename, 
            delimiter = ',',
            usecols=[
                "LandType", "LandCode", "Username",
                "SOATO", "Area_ga", "Forma22",
                "Oblast", "Rayon", "R_zem",
                "Shape_Length", "Shape_Area",
            ],
            dtype={
                'Forma22': 'float64', 'R_zem': 'float64',

            }
        )
        # print(dask_df.head(3))
        categories = type_previw(name, False)[0]

        # print(categories)

        index_chosen, column_chosen, value_chosen = [], [], []

        
        for data in list:
            # print(data)
            if (data[1] == 0):
                index_chosen.append(data[0])
            if (data[1] == 1):
                column_chosen.append(data[0])

        value_chosen = [4]

        index_arr, column_arr, value_arr = [], [], []
        
        for i in range (len(index_chosen)):
            index_arr.append(categories[index_chosen[i]])
        for i in range (len(column_chosen)):
            column_arr.append(categories[column_chosen[i]])
        for i in range (len(value_chosen)):
            value_arr.append(categories[value_chosen[i]]) 

        # print("sorted")
        # print(index_arr)
        # print(column_arr)
        # print(value_arr)

        if (not index_arr or not column_arr):
            return False

        pandas_df = dask_df.compute()

        save=pandas_df.pivot_table(
            index = index_arr,
            columns = column_arr,
            values=value_arr,
            aggfunc = ['sum','count'],
            fill_value="",
            margins=True
        )

        with pd.ExcelWriter(name + ".xlsx", engine="xlsxwriter") as writer:
            print("table create")
            save.to_excel(writer, sheet_name='Отчет')
            writer.sheets['Отчет'].set_column(0, 1, 25)
        return True


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
if __name__ == "__main__":
    excel_process('DKR', [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])
    # type_previw("DKR")
    # first_row_previw("DKR")