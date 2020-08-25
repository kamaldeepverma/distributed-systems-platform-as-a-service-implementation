import schedule,time,os,csv,json
import pandas as pd


cmd = 'echo bits2018 | sudo -S  docker ps --format "table {{.Names}}" > active_users.csv'
os.system(cmd)

users={}
df=pd.read_csv('active_users.csv')
for index,row in df.iterrows():
    users[row['NAMES']]=0

def calculate_cost():
    
    try:
        usage_time=json.loads(open("usage_time.json","r").read()) 
    except:
        usage_time={}

    cmd = 'echo bits2018 | sudo -S docker ps --format "table {{.Names}}" > active_users.csv'
    os.system(cmd)

    df=pd.read_csv('active_users.csv')
    for index,row in df.iterrows():
        user = row['NAMES']
        if usage_time.__contains__(user):
            current_usage=int(usage_time[user])
            current_usage+=10
            usage_time[user]=current_usage
        else:
            usage_time[user]=0
    
    print(usage_time)
    usage_json = json.dumps(usage_time)
    open("usage_time.json","w").write(usage_json)
	

schedule.every(5).seconds.do(calculate_cost)

if __name__ =="__main__":
    while(1):
        schedule.run_pending()
        time.sleep(1)