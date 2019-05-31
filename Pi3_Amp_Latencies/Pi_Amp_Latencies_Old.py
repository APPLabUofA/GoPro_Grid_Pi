#import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np 
from sklearn.linear_model import LinearRegression
import mne

plt.close('all')

trials = 200;
#blocks = 1;

# # The only thing you need to change is going to be par (participant number) the rest will be dictated by dictionaries
par = "003"


# %% We will now load in the EEG data 
#### Now we will go through the EEG file and determine our latencies

# filename = 'M:\Data\GoPro_Visor\Pi_Amp_Latency_Test\\testing_visor_pi_' + par + '.vhdr' # pre-pilot
filename = 'M:\Data\GoPro_Grid\EEG_Data\\' + par + '_grid_test.vhdr' # pilot
raw = mne.io.read_raw_brainvision(filename)
df1 = mne.find_events(raw) # outputs a numpy.ndarray
df1 = np.insert(df1,0,[0],axis = 0) #shift data one row down from the top so we don't miss the first event on o
df1 = pd.DataFrame(data=df1[1:,1:], index=df1[1:,0], columns=df1[0,1:])   # change to a pandas DataFrame
df1 = df1.reset_index() 
df1.columns = ['eeg_times', 'Empty', 'Event_Type'] # name columns
df1 = df1.drop(columns='Empty') # get rid of empty column
df1['eeg_times'] = (df1['eeg_times'] - df1['eeg_times'][0]) # subtract all from start trigger
criteria_1 = df1['Event_Type'] == 253 
#criteria_2 =  df1['Event_Type'] == 255
#criteria_all = criteria_1 | criteria_2 # either/or event defined above
df1 = df1[criteria_1]
df1 = df1.reset_index() # resets index after removing events
df1 = df1.drop(columns='index')



# %% Here we extract thhe Pi times (imported as df2)
df2 = pd.read_csv((r'M:\Data\GoPro_Grid\Pi_Times\\' + str(par) + '_test.csv'), sep=',', header=None) # pilot
df2.columns = ['pi_onset_latency'] # name the coloumns
df2 = df2.apply(pd.to_numeric, args=('coerce',))  ## Convert to numeric
df2['pi_onset_latency'] = df2['pi_onset_latency'] * 1000 # subtract all from start trigger

# %% 
df2 = df2.reset_index()

# %% 
#df_GoPro = pd.read_csv(())
#df2 = df2.T # transpose for plotting purposes
#df2.columns
# %%
# Combine the two into a single dataframe ? Nah, not for now
#all_onset_latencies = pd.concat([df1.assign(dataset='df1'), df2.assign(dataset='df2')])
df3 = df1.join(df2) # join eeg_times to pi_times
df3 = df3.reset_index()
df3['Difference'] = df3['eeg_times'] - df3['pi_onset_latency']
#%%
# Plotting 
# Latency plot
plt.close('all')
# matlibplot 
plt.figure(0)
plt.plot(df3['pi_onset_latency'], df3['level_0'], 'k--', label='Pi Times')
plt.plot(df3['eeg_times'], df3['level_0'], '-.', label='EEG Times')
plt.xlabel('Latency (Miliseconds)')
plt.ylabel('Trial Number')
plt.title('Trial Number vs Pi & EEG')
legend = plt.legend(loc='upper center', shadow=True, fontsize='large')
legend.get_frame().set_facecolor('C0')
plt.show()

# Difference plot
plt.figure(1)
plt.plot(df3['Difference'], df3['level_0'], label='EEG - Pi')
legend = plt.legend(loc='upper right', shadow=True, fontsize='x-large')
plt.xlabel('Latency (Miliseconds)')
plt.ylabel('Trial Number')
plt.title('Trial Number vs Time Difference')
# plt.ylabel('Trial Count')
plt.show()

hist, bin_edges = np.histogram(df3['Difference'], bins = range(0,200,2)) #  range(0,20,2) or  range(0,100,1)
plt.bar(bin_edges[:-1], hist, width = 1)
plt.xlim(min(bin_edges), max(bin_edges))
plt.title("Raw Difference Histogram")
plt.xlabel("Milliseconds")
plt.ylabel("Elements per bin")
plt.show() 


# %% ##Linear Transform
df4 = df3.copy() # copy DataFrame 
df4 = df4.values # convert from Pandas DataFrame to a numpy structure
df4 = np.append(df4, np.zeros((trials,3)), axis=1)


# %% ## ## LinearRegression().fit(X, y) X=Training data (eeg_times), y=Target Values (pi_onset_latency)
reg =  LinearRegression().fit(df4[:,1].reshape(-1,1), df4[:,5].reshape(-1,1))
reg.score(df4[:,1].reshape(-1,1), df4[:,5].reshape(-1,1))

df4[:,6] = reg.intercept_ + df4[:,1]*reg.coef_
df4[:,7] = df4[:,5]-df4[:,6]
sum(df4[:,6])
#histogram showing distribution variability
hist, bin_edges = np.histogram(df4[:,6], bins = range(0,20,1))
plt.bar(bin_edges[:-1], hist, width = 1)
plt.xlim(min(bin_edges), max(bin_edges))
plt.show() 
# 1:eeg_times, 2:eeg_trig, 3:index, 4:pi times, 5:difference, 6:transformed difference, 7:difference between original difference and transformed difference
# %% ## Transformed Difference plot
plt.figure(2)
plt.plot(df4[:,6], df4[:,0], label='EEG - Pi')
#plt.plot(df4[:,10], df4[:,0]) #plot the magnitude of the difference 
#plt.plot(df3['Difference'], df3['level_0'], label='EEG - Pi') # plot untransformed
legend = plt.legend(loc='upper center', shadow=True, fontsize='large')
legend.get_frame().set_facecolor('C0')
plt.xlabel('Latency (miliseconds)')
plt.ylabel('Trial Number')
plt.title('Trial Number vs Transformed Difference')
#plt.xlim([-0.001, 0, 0.001])
plt.show()

# %% Construct a Regression from only the start and stop (red lights)
df5 = np.array([[0,0],[199,402090]]) # pi_times first and last
#['trial','pi_frame']
df6 = np.array([[0,0],[199,402086]]) # eeg first & last
#['trial','eeg_times']

plt.figure(3)
plt.plot(df5[:,1], df5[:,0], 'k--', label='Pi Times')
plt.plot(df6[:,1], df6[:,0], '-.', label='EEG Times')
plt.xlabel('Latency (Miliseconds)')
plt.ylabel('Trial Number')
plt.title('Trial Number vs Pi & EEG')
legend = plt.legend(loc='upper center', shadow=True, fontsize='large')
legend.get_frame().set_facecolor('C0')
plt.show()

reg2 = LinearRegression().fit(df5[:,1].reshape(-1,1), df6[:,1].reshape(-1,1)) #independent varible is the pi times - we are predicting the eeg times
reg2.score(df4[:,1].reshape(-1,1), df4[:,5].reshape(-1,1))
reg2.intercept_ 
reg2.coef_
reg.intercept_ + df6[:,1]*reg.coef_

df6 = np.append(df6, np.zeros((trials,2)), axis=1)

df4[:,8] = reg2.intercept_ + df4[:,4]*reg2.coef_
df4[:,7] = df4[:,5]-df4[:,6]
df4[:,10] = df4[:,8] - df4[:,1] # Difference between transformed and actual EEG times
df4[:,10] = abs(np.around(df4[:,10]))
df4[:,9]=df4[:,4]

hist, bin_edges = np.histogram(df4[:,10], bins = range(0,200,1))
plt.bar(bin_edges[:-1], hist, width = 1)
plt.xlim(min(bin_edges), max(bin_edges))
plt.title("2-Point Transform Difference Histogram")
plt.xlabel("Milliseconds")
plt.ylabel("Elements per bin")
plt.show() 
# %% Construct a Regression from several calibration flashes at the start and end (10 each)
df5 = np.array([[0,0],[0,0],[1,2020],[2,4022],[3,6040],[4,8044],[5,10060],[6,12065],[7,14080],[8,16087],[9,18100],[190,383880],[191,385900],[192,388003],[193,390020],[194,392026],[195,394040],[196,396060],[197,398064],[198,400080],[199,402090]]) # pi_times first and last
df5 = pd.DataFrame(data=df5[1:,1:], index=df5[1:,0], columns=df5[0,1:])
#['trial','pi_frame']
df6 = np.array([[0,0],[0,0],[1,2010],[2,4022],[3,6033],[4,8044],[5,10055],[6,12065],[7,14075],[8,16087],[9,18098],[190,383738],[191,385886],[192,387908],[193,390017],[194,392029],[195,394040],[196,396051],[197,398067],[198,400078],[199,402090]])
df6 = pd.DataFrame(data=df6[1:,1:], index=df6[1:,0], columns=df6[0,1:])

#['trial','eeg_times']

# extract the 10 first and last events for calibrating 
#x = df4[0:10,3:5]
#y = df4[190:-1,3:5]
#x[:,1] = np.around(x[:,1])
#x.astype(int)
#y[:,1] = np.around(y[:,1])
#y.astype(int)
#np.concatenate(x,y)

plt.figure(3)
plt.plot(df5[:,1], df5[:,0], 'k--', label='Pi Times')
plt.plot(df6[:,1], df6[:,0],  'k--', label='EEG Times')
plt.xlabel('Latency (Miliseconds)')
plt.ylabel('Trial Number')
plt.title('Trial Number vs Pi & EEG')
legend = plt.legend(loc='upper center', shadow=True, fontsize='large')
legend.get_frame().set_facecolor('C0')
plt.show()

df7 = df5.join(df6) # join eeg_times to pi_times
df3 = df3.reset_index()
df3['Difference'] = df3['eeg_times'] - df3['pi_onset_latency']

df4[:,7] = df4[:,5]-df4[:,6] # difference across all 20 points
hist, bin_edges = np.histogram(df4[:,7], bins = range(0,150,1))
plt.bar(bin_edges[:-1], hist, width = 1)
plt.xlim(min(bin_edges), max(bin_edges))
plt.title("10 Point Regression Difference Histogram")
plt.xlabel("Milliseconds")
plt.ylabel("Elements per bin")
plt.show() 

plt.figure(4)
plt.scatter(df5[:,1], df5[:,0],color='r',s=40)
plt.scatter(df6[:,1], df6[:,0],color='b',s=40)
plt.xlim(0,20000)
plt.ylim(0,10)
plt.show()

plt.figure(4)
plt.scatter(df5[:,1], df5[:,0],color='r',s=40)
plt.scatter(df6[:,1], df6[:,0],color='b',s=40)
plt.xlim(380000,404000)
plt.ylim(189,201)
plt.show()

plt.figure(4)
plt.scatter(df5[:,1], df5[:,0],color='r',s=3)
plt.scatter(df6[:,1], df6[:,0],color='b',s=3)
plt.show()
#reg.intercept_ + df6[:,1]*reg.coef_

q = (x[:,1]).astype(int)
df4[:,10] = df4[:,8] - df4[:,1] # Difference between transformed and actual EEG times

df6 = np.append(df6, np.zeros((20,2)), axis=1)
reg3 = LinearRegression().fit(df5[:,1].reshape(-1,1), df6[:,1].reshape(-1,1)) #independent varible is the pi times - we are predicting the eeg times
reg3.score(df4[:,1].reshape(-1,1), df4[:,5].reshape(-1,1))
reg3.intercept_ 
reg3.coef_

df6[:,3] = reg3.intercept_ + df4[:,4]*reg3.coef_

df4[:,10] = df4[:,8] - df4[:,1]
df4[:,9]=df4[:,4]
sum(abs(df4[:,10]))
sum(abs(df4[:,5]))

# Try taking out rows that have variable greater than ~15 and compare wide tailed Regression before and after



sum(abs(df4[:,5])) # Raw data -  difference variance
sum(abs(df4[:,10])) # 2-point transform - difference vairance
sum(abs(df4[:,10])) # Long Tail transform - difference vairance


