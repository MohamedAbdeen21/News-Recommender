from sklearn.feature_extraction.text import TfidfVectorizer
# from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
# from matplotlib import pyplot as plt
# from datetime import date

# import json
import requests
import pandas as pd

d = "http://api:8000/users_history/"
req = requests.get(d)

j_data = req.json()

if j_data != []:
    
    cookie_id = []
    text = []
    url = []
    for i in j_data:
        cookie_id.append(i['cookie_id'])
        text.append(i['text'])
        url.append(i['url'])

features_temp = pd.DataFrame({"cookie_id":cookie_id, "url": url, "text": text})

def get_features(df):
    c = df['cookie_id'].to_list()
    t = df['text'].to_list()
    u = df['url'].to_list()
    history_url = []
    feature = []
    temp = ''
    h_temp = ''
    for i in list(df['cookie_id'].unique()):
        count = 0
        for x in c:
            if i == x:
                temp = temp + t[count] + ' '
                h_temp = h_temp + u[count] + ' '
            count += 1
        feature.append(temp)
        history_url.append(h_temp)
        temp = ''
        h_temp = ''
    return pd.DataFrame({'cookie_id':list(df['cookie_id'].unique()), 'feature': feature, 'history_url':history_url})
        
features = get_features(features_temp)
#Get users with all the articles read
#features = pd.read_csv('/media/alnaggar/F47C61617C611F9A/PBL Data/features.csv', low_memory=False)

cvec = TfidfVectorizer(stop_words = "english")

#Extract Features
count_matrix = cvec.fit_transform(features["feature"])

#Cmoputing Cosine similarity socre
cosine_sim = cosine_similarity(count_matrix)

#creating groups of similar users using hierarichal clustering
cluster = AgglomerativeClustering()

y = cluster.fit_predict(cosine_sim)

#Return a data frame with each user group
users_group = pd.DataFrame({'user':features.cookie_id, 'group': y, 'feature':features.feature, 'history_url': features.history_url})
users_group.to_csv('./users_group.csv', index = False)


#uncomment this to see groups graph
#plt.scatter(x= cosine_sim[:,0], y = cosine_sim[:,1], c= y, cmap='rainbow' )
#plt.show()

x = 0
while(x < len(users_group['user'].to_list())):
    uu = "http://api:8000/update_group/{}/{}".format(users_group['user'].loc[x], users_group['group'].loc[x])
    req_1 = requests.patch(uu)
    x +=1
x = 0
cookie_id = []
text = []
url = []
