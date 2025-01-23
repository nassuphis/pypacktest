# %%
from IPython.display import display
import straddle_activity as stre
rs1 = "result_nick_20250115_prod_0024"
rs2 = "result_nick_20250121_stagger_7299"
stre.result_set = rs1
# %%
display(stre.activity("SX5E Index","2024-12").to_latex)
# %%
display(stre.activity("GBPUSD Curncy","2024-12").to_latex)
