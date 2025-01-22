import straddle_activity as stre

rs1 = "result_nick_20250115_prod_0024"
rs2 = "result_nick_20250121_stagger_7299"

stre.result_set = rs1

print(stre.entry_date("GBPUSD Curncy","2024-12"))

print(stre.expiry_date("GBPUSD Curncy","2024-12"))

print(stre.expiry_date("SX5E Index","2024-12"))

print(stre.entry_date("SX5E Index","2024-12"))

