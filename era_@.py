#importing pandas library
import pandas as pd
#importing time library for calculating total runtime
#import datafr
#importing decimal library

#main function containing all functionality
def annexure_1(df, date1,date2,artm1,artm2):

    df=df[df['Era']!='NA']
    #radio_list = df['Radio'].unique().tolist()
    year_list =sorted(df['Era'].dropna().unique().tolist())
    year_list = year_list[::-1]
    #print(year_list)
    language_list = df['Language'].dropna().unique().tolist()
    #print(language_list)
    radio_list = df['Radio'].unique().tolist()
    #datafr.listname=len(radio_list)
    #print(radio_list)
    #df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    #print(df)
    date_list = sorted(df['Date'].unique().tolist())
    #print(date_list)
    result = pd.DataFrame()
    
    length = len(language_list)
    
    for radio in radio_list:
        
        radio_df = df.loc[df['Radio'] == radio]
        
        #creating main df
        #print("\nName of Radio:",radio)
        perc_sum = []
        radio_list_same = []
        for i in range (0,length) :
            radio_list_same.append(radio)
            perc_sum.append(0)
        data_frame_1 = pd.DataFrame()
        data_frame_1['Radio'] = [' '.join(['No. of Playouts', radio]) for radio in radio_list_same]
        data_frame_1['Language'] = language_list
        data_frame_2 = pd.DataFrame()
        data_frame_2['Radio'] = [' '.join(['Percentage of Playouts', radio]) for radio in radio_list_same]
        data_frame_2['Language'] = language_list
        data_frame_3 = pd.DataFrame()
        data_frame_3['Radio'] = [' '.join(['No. of Songs', radio]) for radio in radio_list_same]
        data_frame_3['Language'] = language_list

        
        #adding different constraints on input
        
        if(date1 == "" or date1>date_list[len(date_list)-1]):
            date1 = date_list[0]
        if(date2 == "" or date2<date_list[0]):
            date2 = date_list[-1]

        
        #radio_df.to_excel('x.xlsx')
        #defining dataframes for start and end dates
        date_df = radio_df.loc[(radio_df['Date'] >= date1) & (radio_df['Date'] <= date2) ]
        #print(date_df)
        #print(date1,date2)
        
        #defining data frame according time defined
        if(artm1<=artm2):
            air_df = date_df.loc[(date_df['Air Time'] >= artm1) & (date_df['Air Time'] <= artm2)]
        else:
            da1 = date_df.loc[(date_df['Date'] >= date1) & (date_df['Air Time'] >= pd.to_datetime(artm1, format="%H:%M:%S").time())]
            da2 = date_df.loc[(date_df['Date'] != date1) & (date_df['Air Time'] <= pd.to_datetime(artm2, format="%H:%M:%S").time())]
            air_df=da1.append(da2)
        #print(air_df)
        language_total_list = []
        for language in language_list:
            language_df = air_df.loc[air_df['Language'] == language]
            language_total = language_df.shape[0]
            #print("Total playouts ", language, " songs: ",language_total)
            language_total_list.append(language_total)
        language_total_sum = sum(language_total_list)
        #print(language_total_list)
        
        language_total_list2 = []
        for language in language_list:
            language_df_2 = air_df.loc[air_df['Language'] == language]
            song_df_total = language_df_2['Account/Song Title'].unique()
            language_total2 = song_df_total.shape[0]
            #print("Total playouts ", language, " songs: ",language_total)
            language_total_list2.append(language_total2)
        language_total_sum2 = sum(language_total_list2)
        #print(language_total_list)
                
        for year in year_list:
            #sum to calculate total playouts in that in that radio
            #sum_year = 0
            year_df = air_df.loc[air_df['Era'] == year ]
            #print(year_df)
            #print("Number of songs of " , year)
            
            
            no_of_songs_list = []
            no_of_songs1_list = []
            
            per_song_list = []
                                               
            for language in language_list:
                language_year_df = year_df.loc[year_df['Language'] == language]
                song_df = language_year_df['Account/Song Title'].unique()
                #print(song_df)
                no_of_songs1 = song_df.shape[0]
                #print(no_of_songs1)
                no_of_songs = language_year_df.shape[0]
                #to find the total playouts in that year
                #sum_year = sum_year + no_of_songs
                #print(language_year_df)
                #print(language , " : " , no_of_songs)
                no_of_songs_list.append(no_of_songs)
                no_of_songs1_list.append(no_of_songs1)
            data_frame_3[year] = no_of_songs1_list
            data_frame_1[year] = no_of_songs_list
            #print(no_of_songs1_list,no_of_songs_list)
            #print(sum_year)
            
            for i in range (0,length) :
                if(language_total_sum == 0):
                    per_song_list.append(0)
                else:
                    per_song_list.append(round((no_of_songs_list[i]/language_total_sum)*100,2))
                perc_sum[i] = perc_sum[i] + per_song_list[i]
            per_song_list=[str(x)+'%' for x in per_song_list]
            data_frame_2[year] = per_song_list
        for i in range(len(perc_sum)):
            perc_sum[i] = round(perc_sum[i],1)
        data_frame_1['Total'] = language_total_list
        data_frame_3['Total'] = language_total_list2
        perc_sum=[str(x)+'%' for x in perc_sum]
        data_frame_2['Total'] = perc_sum
        pd.set_option('display.max_columns', 8)
        frames_tosort = [data_frame_3,data_frame_1,data_frame_2]
        resultx = pd.concat(frames_tosort)
        #print(resultx)
        #resultx = resultx.groupby(["Language"])
        resultx['Language'] = pd.Categorical(resultx['Language'], ["Hindi", "Punjabi", "Bengali"])
        resultx = (resultx.sort_values('Language'))
        
        #resultx = resultx.sort_values(["Language"],ascending=False)
        frames = [result,resultx]
        result = pd.concat(frames)
        #print(result.sort_values(["Language"]))
        #display(data_frame_1)
        #display(data_frame_2)
    #datafr.download_era=[]
    #datafr.download_era.append(result)
    #result.to_excel('out.xlsx')
    print(result)
    
    #print(result.loc["No. of Songs CITY DELHI":"No. of Playouts CITY DELHI", "2018s":"2015s"])

df = pd.read_excel('Dataframe.xlsx' , sheet_name = 'Sheet1')
annexure_1(df,'2019-02-22','2019-02-28','07:00:00','21:00:00')
