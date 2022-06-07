
import pandas as pd

df = pd.read_csv("D:/Research/GSU/Research1_xray_flux/sdo_era_goes_flares_integrated_all_CME.csv")
df_flux = pd.read_csv("D:/Research/GSU/Research1_xray_flux/fixed_all_xrs_relative.csv")

# 1] Data preprocessing

# 1) Change goes_class into numeric value.
value_list = []
for value in df["goes_class"]:
    #print(value)
    if 'X' in value:
        value_list.append(float(value[1:])*1e-4)
    elif 'M' in value:
        value_list.append(float(value[1:])*1e-5)
    elif 'C' in value:
        value_list.append(float(value[1:])*1e-6)
    elif 'B' in value:
        value_list.append(float(value[1:])*1e-7)
    elif 'A' in value:
        value_list.append(float(value[1:])*1e-8)

df["goes_class_num"] = value_list

# change start_time, peak_time, Timestamp to time value. 
df['start_time']=pd.to_datetime(df['start_time'])
df['peak_time']=pd.to_datetime(df['peak_time'])
df['end_time']=pd.to_datetime(df['end_time'])
df_flux['Timestamp']=pd.to_datetime(df_flux['Timestamp'])

# 2) Add start_time_bf24 (start_time 24hours ago).
import datetime
df['start_time_bf24'] = df['start_time'] - datetime.timedelta(days=1)


# 2] Creating Background X-ray flux and Relative X-ray increase

# 1) Defining background X-ray flux (less than X-ray flux at start time)

avg_background_st = []
num_iteration=0
for i in range(len(df['start_time_bf24'])):
    print('\r{0}'.format((i/14411)*100),end='')
    
    # from start time - 24 hours to start time
    condition = df_flux['Timestamp'].between(df['start_time_bf24'][i], df['start_time'][i])
    df_new = df_flux.loc[condition, 'B_filtered']
        
    # less than X-ray flux at start time will be background
    condition_st = df_flux['Timestamp'] == df['start_time'][i]
    total_st = df_new.where(df_new<float(df_flux.loc[condition_st,'B_AVG']), None).sum()
    count_st = df_new.where(df_new<float(df_flux.loc[condition_st,'B_AVG']), None).count()
    avg_background_st.append(total_st/count_st)

df['Background_X-ray_flux']=avg_background_st

# relative X-ray flux
df['relative_X-ray_flux_increase'] = df['goes_class_num']/df['Background_X-ray_flux']

# Save files
df.to_csv("D:/Research/GSU/Research1_xray_flux/sdo_era_goes_flares_integrated_all_CME.csv")