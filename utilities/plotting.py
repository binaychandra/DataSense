import pandas as pd
import sqlite3

def badges_get_pillar_dougnutdata():
    con = sqlite3.connect("database.db")
    df = pd.read_sql_query(f"SELECT * from badges", con)
    sdf = df.drop_duplicates()[['GUI', 'Pillar']]
    sdf = sdf[(sdf.Pillar.notna()) | (sdf.Pillar != 'null')]
    pillar_dist = sdf.groupby('Pillar').count().reset_index().rename(columns={'GUI':'cnt_gui'})
    sum_validrecords = pillar_dist.cnt_gui.sum()
    pillar_dist['pct_gui'] = pillar_dist['cnt_gui'] / sum_validrecords
    badges_pillar_doughnut_json = pillar_dist.to_json(orient='records')
    return badges_pillar_doughnut_json

def badges_get_badgecompletion_monthwise():
    df = pd.DataFrame(
                        {
                        'Month':['Nov-23', 'Dec-23', 'Jan-23', 'Feb-23', 'Mar-23', 'Apr-23', 'May-23', 'Jun-23'],
                        'cnt_gui_badgeinitiated':[45,40,30,56, 50,32,37,25],
                        'cnt_gui_badgeawarded':  [23,34,38,40, 31, 40,23,28],
                        },
                      )
    print(df)
    badgecompletion_monthwise_json = df.to_json(orient='records')
    return badgecompletion_monthwise_json

def get_validation_json(table_name, run_required=False):
    ## Dummy data for workforce
    con = sqlite3.connect("database.db")
    validation_df = pd.read_sql_query(f"SELECT * from {table_name}_validation", con)
    json_data = validation_df.to_json(orient='records')
    return json_data

def get_wfrankwise_countmom(df=None):
    data = [
        ('Jan', 9, 15, 3, 30, 25, 23, 110),
        ('Feb', 7, 14, 2, 32, 40, 35, 106),
        ('Mar', 6, 13, 4, 36, 34, 20, 105),
        ('Apr', 8, 15, 3, 21, 30, 25, 112),
        ('May', 9, 19, 4, 25, 35, 30, 121),
        ('Jun', 7, 14, 3, 20, 25, 35, 113),
        ('Jul', 10, 11, 3, 41, 27, 25, 113)
    ]
    columns = ['Month', 'Director', 'Manager', 'Partner', 'Senior', 'SeniorManager', 'Staff', 'Grand Total']
    df = pd.DataFrame(data, columns=columns)
    json_df = df.to_json(orient='records')

    return json_df

def get_lst_topdepartment():
    lst_dept = [
        'D&A-BI&R-FS-GDS_S-BLR (138)',
        'D&A-BI&R-FS-GDS_NS-CCU (128)',
        'IntA-IntAut-NF-GDS_S-BLR (88)',
        'IntA-IntAut-NF-GDS_NS-GGN (75)',
        'D&A-BI&R-FS-GDS_NS-HYD (70)',
        'D&A-InMg-FS-GDS_S-BLR (70)',
        'INTA-INTAUT-NF (67)',
        'D&A-BI&R-FS-GDS_S-COK-L (59)',
        'D&A-BI&R-FS-GDS_S-MAA (58)',
        'D&A-InMg-NF-GDS_S-BLR (49)'
    ]
    return lst_dept

def get_wfrankwise_count():

    #write the logic to create pandas dataframe like below
    data = {
        "Rank": [
            "Contractor",
            "Director(Exec./Asst.)",
            "Manager",
            "null",
            "Senior",
            "Senior Manager",
            "Staff/Intern"
        ],
        "count_rank": [10, 10, 253, 322, 1391, 92, 1020]
    }

    df = pd.DataFrame(data)
    json_rankwise_count = df.to_json(orient='records')
    return json_rankwise_count


def get_topfive_badgetitle():
    lstbadges = [
        'Agile Learning Badge (479)',
        'Data Integration Bronze Badge (362)',
        'Data Integration Learning Badge (339)',
        'Data Visualization Bronze Badge (306)',
        'Data Visualization Learning Badge (295)',
        'Cloud Learning Badge (291)',
        'Robotic Process Automation Learning Badge (212)',
        'Robotic Process Automation Bronze Badge (191)',
        'Data Visualization Bronze Learning Badge (166)',
        'Data Science Learning Badge (165)'
    ]
    return lstbadges