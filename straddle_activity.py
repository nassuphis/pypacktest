import IPython
import pandas as pd
import duckdb as ddb
ltx = False
result_set = "result_nick_20250121_stagger_7299"

def activity(underlying,month):
    with ddb.connect() as con:
        df0 = pd.read_parquet(f"{result_set}/straddle_entry_expiry.parquet")
        con.register("df0", df0)
        df1 = con.execute(f"""
                          
            SELECT 
                Underlying, 
                str_split(straddle,'|')[3] AS month,  
                expiry_date as date,    
                'expiry' as activity,
                straddle
            FROM df0 AS expiry
            WHERE expiry.Underlying = '{underlying}' AND str_split(straddle,'|')[3]='{month}'

            UNION ALL

            SELECT 
                Underlying, 
                str_split(straddle,'|')[2] AS month,
                entry_date as date,
                'entry' as activity,
                straddle
            FROM df0 AS entry
            WHERE entry.Underlying = '{underlying}' AND str_split(straddle,'|')[2]='{month}'

            ORDER BY month, date, activity

        """).df()
        return df1
    

def show(res):
    if ltx:
        lres = res.to_latex(formatters={'date': lambda x: x.strftime('%Y-%m-%d')})
        IPython.display.display(IPython.display.Latex(lres))
    else:
        IPython.display.display(res)

    
