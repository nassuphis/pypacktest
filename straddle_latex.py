import IPython
import straddle_activity as straddle

result_set = None

def set(rs):
    global result_set 
    result_set = rs.replace("_", "\\_")
    straddle.result_set = rs
    
def get():
    return  result_set


def activity(ul,month):
    res=straddle.activity(ul,month)
    count = res["activity"].value_counts()
    lres = res.to_latex(formatters={
        'Underlying': lambda x: f'\\texttt{{{x}}}',
        'month': lambda x: f'\\texttt{{{x}}}',
        'date': lambda x: x.strftime('%Y-%m-%d'),
        'activity': lambda x: f'\\texttt{{{x}}}',
        'straddle': lambda x: f'\\texttt{{{x}}}'
    })
    print("\\noindent")
    print(lres)
    print("\n")
    print("\\vskip 1mm")
    print("\n")
    print(f"entries: {count.get('entry',0)},")
    print(f"expiries: {count.get('expiry',0)}\n")
    print("\\vskip 5mm")

def out_activity(month):
    res=straddle.out_activity(month)
    count = res["activity"].value_counts()
    lres = res.to_latex(formatters={
        'Underlying': lambda x: f'\\texttt{{{x}}}',
        'month': lambda x: f'\\texttt{{{x}}}',
        'date': lambda x: x.strftime('%Y-%m-%d'),
        'activity': lambda x: f'\\texttt{{{x}}}',
        'straddle': lambda x: f'\\texttt{{{x}}}'
    },
    longtable=True,
    index=False,
    column_format='p{3cm} p{1.25cm} p{1.75cm} p{1cm} p{5cm}'
    )
    print("\\noindent")
    print(lres)
    print("\n")
    print("\\vskip 1mm")
    print("\n")
    print(f"entries: {count.get('entry',0)},")
    print(f"expiries: {count.get('expiry',0)}\n")
    print("\\vskip 5mm")

def out_hi(df):

    df_hi = df.copy()

    for index, row in df.iterrows():
        straddle = row["straddle"].split("|")
        ntr = straddle[1]
        xpr = straddle[2]
        ntrym = row["entry_date"].strftime('%Y-%m')
        xprym = row["expiry_date"].strftime('%Y-%m')
        ntrymd = row["entry_date"].strftime('%Y-%m-%d')
        xprymd = row["expiry_date"].strftime('%Y-%m-%d')

        if ntr != ntrym: 
            df_hi.at[index, "entry_date"] = f"\\cellcolor{{red}}{ntrymd}"
        else:
            df_hi.at[index, "entry_date"] = f"\\cellcolor{{white}}{ntrymd}"

        if xpr != xprym: 
            df_hi.at[index, "expiry_date"] = f"\\cellcolor{{red}}{xprymd}"
        else:
            df_hi.at[index, "expiry_date"] = f"\\cellcolor{{white}}{xprymd}"

    return df_hi

def out_backtest(month):
    res=straddle.out_backtest(month)
    res=out_hi(res)
    res.rename(columns=lambda x: x.replace("_", "\\_"),inplace=True)
    lres = res.to_latex(formatters={
        res.columns[0]: lambda x: f'\\texttt{{{x}}}',
        res.columns[1]: lambda x: x,
        res.columns[2]: lambda x: x,
        res.columns[3]: lambda x: f'\\texttt{{{x}}}'
    },
    longtable=True,
    index=False,
    column_format='p{3cm} p{1.75cm} p{1.75cm} p{6cm}'
    )
    print("\\noindent")
    print(lres)
    print("\n")
    print("\\vskip 1mm")
    print("\n")
    print(f"rows: {res.shape[0]},")
    print("\n")
    print("\\vskip 5mm")

def asset_entry(asset,month):
    res=straddle.asset_entry(asset,month)
    res.rename(columns=lambda x: x.replace("_", "\\_"),inplace=True)
    lres = res.to_latex(formatters={
        res.columns[0]: lambda x: f'\\texttt{{{x}}}', # asset
        res.columns[1]: lambda x: f'\\texttt{{{x}}}', # month
        res.columns[2]: lambda x: f'\\texttt{{{x}}}', # straddle
        res.columns[3]: lambda x: x.strftime('%Y-%m-%d'), # entry
        res.columns[4]: lambda x: f'\\texttt{{{round(x,2)}}}', # vol
        res.columns[5]: lambda x: f'\\texttt{{{round(x,2)}}}', # strike
        res.columns[6]: lambda x: f'\\texttt{{{round(x,4)}}}', # mv
    },
    index=False,
    column_format='p{3cm} p{1.5cm} p{6cm} p{1.75cm} p{1.25cm} p{1.25cm} p{1.25cm} '
    )
    print("\\noindent")
    print(lres)
    print("\n")
    print("\\vskip 1mm")
    print("\n")
    print(f"rows: {res.shape[0]}")
    print("\n")
    print("\\vskip 5mm")




    
