import datetime
import os
import pandas
from collections import namedtuple
from common.file_management import fetch, write_df

DatasetInfo = namedtuple('DatasetInfo', ['name', 'urlinfos', 'main_file', 'source'])
UrlInfo = namedtuple('UrlInfo', ['url', 'filenames', 'uncompress'])

EMPLOYEE_SALARIES_CONFIG = DatasetInfo(
    name='employee_salaries',
    urlinfos=(
        UrlInfo(
            url="https://data.montgomerycountymd.gov/api/views/"
                "xj3h-s2i7/rows.csv?accessType=DOWNLOAD",
            filenames=("rows.csv",),
            uncompress=False
        ),
    ),
    main_file="employee_salaries.csv",
    source="https://catalog.data.gov/dataset/employee-salaries-2016"
)


def get_employee_salaries_df(save=True):
    data_dir = fetch(EMPLOYEE_SALARIES_CONFIG)
    file = os.listdir(data_dir[0])[0]
    csv_path = os.path.join(data_dir[0], file)
    df = pandas.read_csv(csv_path)
    df['Year First Hired'] = [datetime.datetime.strptime(d, '%m/%d/%Y').year for d in df['Date First Hired']]
    write_df(save, df, data_dir[1], EMPLOYEE_SALARIES_CONFIG.main_file)
    return df
