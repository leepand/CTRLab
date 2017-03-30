'''Feature Engineering'''
from util import  run_cmd
##process search data
import jieba
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
###load events
def load_user_events(fname):
    user_drive_event={}
    for line in open(fname):
        uid,Province,City,target_drive,target_buy=line.strip().split()
        user_drive_event[uid]=int(target_drive)
        #print uid,Province,City,target_drive,target_buy
    return user_drive_event
user_drive_event=load_user_events('./data/event.txt')
search_behaviour={}
behaviour_space={}
behaviour_uniq=[]
for l in open( './data/search.txt' ):
    userid=l.split('\t')[0]
    behaviour_id=l.split('\t')[4]
    search_content=l.split('\t')[5]
    clsname=str(l.split('\t')[1]).strip()
    #print userid
    if userid  in search_behaviour:       
        search_behaviour[str(userid)]+=str(search_content)
    else:
        search_behaviour[str(userid)]=str(search_content)
    if userid in behaviour_space:
        behaviour_id_list=[]
        if behaviour_id in behaviour_id_list:
            behaviour_id_list.append(str(behaviour_id))
        else:
            behaviour_id_list=str(behaviour_id)
        behaviour_space[str(userid)].append(str(behaviour_id))
    else:
        behaviour_space[str(userid)]=[str(behaviour_id)]
    if behaviour_id in behaviour_uniq:
        behaviour_uniq=behaviour_uniq
    else:
        behaviour_uniq.append(behaviour_id)

f_content=open('./transform_data/user_search_content.txt','w')
f_content_only=open('./transform_data/user_search_content_only.txt','w')
n=0
userid2row={}
for userid,content in search_behaviour.iteritems():
    if userid in user_drive_event:
        user_targer=user_drive_event[userid]
    else:
        user_targer=0
    f_content.write(str(n)+' '+str(userid)+' '+str(user_targer)+' '+str(' '.join(jieba.lcut(content.decode('utf-8'))))+'\n')
    f_content_only.write(str(' '.join(jieba.lcut(content.decode('utf-8'))))+'\n')
    userid2row[n]=userid
    n=n+1
f_content_only.close()
f_content.close()

####process search data
run_cmd('GLOG_log_dir="." ./article2vec.bin -method cluster -input user_search_content_only.txt -ref clustering/text_class_w2v_cluster.txt -nclasses 100 -output search_vectors.txt -oformat xgboost')
fo_search=open('./transform_data/userid_search_vectors2.txt','w')
for i,line in enumerate(open('./transform_data/search_vectors.txt')):
    if line.strip()== 'NULL':
        continue
    fo_search.write(str(userid2row[i])+' '+line.strip()+'\n')
    #print i,line
fo_search.close()