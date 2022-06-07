import pandas as pd
df_flux = pd.read_csv("D:/Research/GSU/Research1_xray_flux/fixed_all_xrs_relative.csv")
df = pd.read_csv("D:/Research/GSU/Research1_xray_flux/sdo_era_goes_flares_integrated_all_CME.csv")

# 1) delete low quality X-ray flux
df_flux['B_filtered'] = df_flux['B_AVG'].where(df_flux['B_AVG']>1*10**(-9), None)

# 2) filtering out flaring interval ( from s.t to e.t )
for i in range(len(df['start_time'])):
    df_flux.loc[df_flux['Timestamp'].between(df['start_time'][i], df['end_time'][i]), 'B_filtered'] = None 
    print('\r{0}'.format((i/14411)*100),end='')


df_flux.to_csv("D:/Research/GSU/Research1_xray_flux/fixed_all_xrs_relative.csv")