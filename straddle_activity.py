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
    

def out_activity(month):
    with ddb.connect() as con:
        df0 = pd.read_parquet(f"{result_set}/straddle_entry_expiry.parquet")
        con.register("df0", df0)
        df1 = con.execute(f"""
                          
            WITH union_table AS (
                SELECT 
                    Underlying, 
                    str_split(straddle, '|')[3] AS month,  
                    expiry_date AS date,    
                    'expiry' AS activity,
                    straddle
                FROM df0 AS expiry
                WHERE str_split(straddle, '|')[3] = '{month}'

                UNION ALL

                SELECT 
                    Underlying, 
                    str_split(straddle, '|')[2] AS month,
                    entry_date AS date,
                    'entry' AS activity,
                    straddle
                FROM df0 AS entry
                WHERE str_split(straddle, '|')[2] = '{month}'
            )
            SELECT *
            FROM union_table
            WHERE strftime('%Y-%m', date) != month
            ORDER BY Underlying, month, date, activity;

        """).df()
        return df1

def out_backtest(month):
    with ddb.connect() as con:
        bktst = pd.read_parquet(f"{result_set}/backtest.parquet")
        con.register("bktst", bktst)
        df1 = con.execute(f"""
        SELECT 
            Underlying, 
            expiry_date,
            entry_date,                  
            straddle
        FROM bktst
        WHERE 
            date = entry_date AND
            (
              str_split(straddle, '|')[2] = '{month}' 
              OR
              str_split(straddle, '|')[3] = '{month}'             
            )
        """).df()
        con.register("df1", df1)
        df2 = con.execute(f"""
        SELECT 
            Underlying, 
            entry_date,      
            expiry_date,           
            straddle
        FROM df1
        WHERE 
        strftime('%Y-%m', entry_date)!=str_split(straddle, '|')[2]
        OR 
        strftime('%Y-%m', expiry_date)!=str_split(straddle, '|')[3]
        """).df()
        return df2

def show(res):
    IPython.display.display(res)



    
