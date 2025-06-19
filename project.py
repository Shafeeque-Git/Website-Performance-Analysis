import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Show all columns when printing the DataFrame
#pd.set_option('display.max_columns', None)

# Optionally, increase display width to avoid wrapping
#pd.set_option('display.width', 1000)



df = pd.read_csv("data-export (1) (1).csv")
print(df.head())
print(df.columns)

#removing unnamed columns
df.columns = df.iloc[0]
print(df.head())

#removing duplicate column name
df =df.drop(index=0).reset_index(drop=True)
df.columns=['channel group', 'DateHour', 'Users', 'Sessions', 'Engaged Sessions', 
            'Average enagement time per session', 'Engaged session per user', 'Events per session'
            , 'Engagement rate', 'Event count']
print(df.columns)

print(df.info())

#Column datehour dtypechange into datetime
df['DateHour'] = pd.to_datetime(df['DateHour'], format='%Y%m%d%H', errors='coerce')
print(df.info())
print(df.head(10))

#covert all columns into numeric dtype leaving Channel Group and DateHour
numeric_cols= df.columns.drop(['channel group','DateHour'])
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
print(df.info())

#adding new column for hours
df['Hour'] = df['DateHour'].dt.hour
print(df.head())
print(df[['DateHour','Hour']])


print(df.describe())

# Q1 : What patterns or trends can you observe in website sessions and users over time?
#fig, ax = plt.subplots(4, 2, figsize=(24, 24))

sns.set(style='whitegrid')
plt.figure(figsize=(10,5))
df.groupby('DateHour')[['Sessions','Users']].sum().plot()
plt.title('Sessions and Users Over Time')
plt.xlabel('DateHour')
plt.ylabel('Count')
plt.savefig("Sessions and Users Over Time.png", dpi=300)
plt.show()


# Q2 : Which marketing channel brought the highest number of users to the website,and
# how can we use this insight to improve traffic from other sources? 
plt.figure(figsize=(8,5))
sns.barplot(data=df, x='channel group', y='Users', estimator=np.sum, palette='viridis')
plt.title('Total Users by Channel')
plt.xticks(rotation=45)
plt.savefig('Total Users by Channel.png')
plt.show()


# Q3 : Which channel has the highest average engagement time and what does that tell us
# about user behaviour and content effectiveness?
plt.figure(figsize=(10,6))
sns.barplot(data=df, x='channel group', y='Average enagement time per session', estimator=np.mean, palette='magma')
plt.title('Average Engagement Time by Channel')
plt.xlabel('channel')
plt.ylabel('Average Engaged Time')
plt.xticks(rotation=45)
plt.savefig("Average Engagement Time by Channel")
plt.show()


# Q4 : How does engagement rate vary across different traffic channels?
plt.figure(figsize=(10,6))
sns.boxplot(data=df, x='channel group', y='Engagement rate', palette='coolwarm')
plt.title('Engagement Rate Distribution by Channel')
plt.xticks(rotation=45)
plt.savefig("Engagement Rate Distribution by Channel", dpi=300)
plt.show()


# Q5 : Which channels are driving more engaged sessions compared to non-engaged ones
# and what strategies can improve engagement in underperforming channels?
session_df = df.groupby('channel group')[['Sessions', 'Engaged Sessions']].sum().reset_index()
session_df['Non-Engaged'] = session_df['Sessions']-session_df['Engaged Sessions']
session_df_melted = session_df.melt(id_vars='channel group', value_vars=['Engaged Sessions', 'Non-Engaged'])
plt.figure(figsize=(8,5))
sns.barplot(data=session_df_melted, x='channel group', y='value', hue='variable')
plt.title('Engaged vs Non-Engaged Sessions')
plt.xticks(rotation=45)
plt.savefig("Engaged vs Non-Engaged.png", dpi=300)
plt.show()


# Q6 : At what hours of the day does each channel drive the most traffic?
heatmap_data = df.groupby(['Hour', 'channel group'])['Sessions'].sum().unstack().fillna(0)
plt.figure(figsize=(10,6))
sns.heatmap(heatmap_data, cmap='YlGnBu', linewidths=.5, annot=True, fmt='.0f')
plt.title('Traffic by Hour and Channel')
plt.xlabel('channel group')
plt.ylabel('Hour of Day')
plt.savefig("Traffic by Hour and Channel.png", dpi=300)
plt.show()


# Q7 : Is there any correlation between high traffic (sesions) and high engagement
# rate over time?
df_plot = df.groupby('DateHour')[['Engagement rate', 'Sessions']].mean().reset_index()
plt.figure(figsize=(10,6))
plt.plot(df_plot['DateHour'], df_plot['Engagement rate'], label='Engagement rate', color='green')
plt.plot(df_plot['DateHour'], df_plot['Sessions'], label='Sessions', color='blue')
plt.title('Engagement Rate vs Sessions Over Time')
plt.xlabel('DateHour')
plt.legend()
plt.grid(True)
plt.savefig("Engagement Rate vs Sessions Over Time.png", dpi=300)
#fig.suptitle("Charts")
plt.tight_layout()
plt.show()