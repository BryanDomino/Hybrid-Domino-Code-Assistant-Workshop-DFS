df = pd.read_csv("/mnt/data/app_data.csv", parse_dates=['datetime'])

import datetime

df_today = df.loc[df["datetime"] > (df["datetime"].iloc[-1] - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')]

df_week = df.loc[df["datetime"] > (df["datetime"].iloc[-1] - datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')]
df_today.head()

def vertical_stack(df, columns, index_col, stack_id, value_id):
    df_out = pd.DataFrame(columns=[index_col, stack_id, value_id])
    temp = pd.DataFrame(columns=[index_col, stack_id, value_id])
    
    for c in columns:
        temp[index_col] = df[index_col]
        temp[stack_id] = c
        temp[value_id] = df[c]
        df_out = pd.concat([df_out, temp])
    
    return df_out


columns = ['CCGT', 'OIL', 'COAL', 'NUCLEAR', 'WIND', 'PS', 'NPSHYD', 'OCGT', 'OTHER', 'INTFR', 'INTIRL', 'INTNED', 'INTEW', 'BIOMASS', 'INTEM']
index_col = 'datetime'
stack_id = 'Source'
value_id = 'Production (MW)'

# 
df_today = vertical_stack(df_today, columns, index_col, stack_id, value_id)
df_today["datetime"] = df_today["datetime"].astype(str)

df_week = vertical_stack(df_week, columns, index_col, stack_id, value_id)
df_week["datetime"] = df_week["datetime"].astype(str)