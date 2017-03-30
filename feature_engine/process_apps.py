####process app data
from util import  run_cmd
from collections import defaultdict
data = defaultdict(dict)
keys = []
fo_app=open('./transform_data/app/user_app_content.txt','w')
fo_app_only=open('./transform_data/app/user_app_content_only.txt','w')
for line in open('./data/app.txt'):
    if not line:
        continue
    items = line.split()
    key = items[0]
    keys.append(key)
    for i, item in enumerate(items[1:3]):
        data[key][i] = data[key].get(i, []) + [item]
appuserid2row={}
nn=0
for key in sorted(list(set(keys)), key=keys.index):
    value = data[key]
    #print key,
    fo_app.write(str(key)+' ')
    appuserid2row[nn]=key
    for i in sorted(value.keys()):
        vs = list(set(value[i]))
        vs.sort(key=value[i].index)
        #print ' '.join(vs),
        fo_app.write(' '.join(vs)+' ')
        fo_app_only.write(' '.join(vs)+' ')
    fo_app.write('\n')
    fo_app_only.write('\n')
    nn=nn+1
    #print
fo_app.close()
fo_app_only.close()
####transfer apps info to sparse features using doc2vecc 
def run_cmd(cmd):
    print (cmd)
    os.system(cmd)
#####注意和search的转换的不同！search用的局部ref，只针对语义级，app用的全局ref，针对feature的交叉合并
#run_cmd('time GLOG_log_dir="." ./article2vec.bin -method cluster -input user_app_content_only.txt -ref items2cluster.txt -nclasses 100 -output app_doclevel_vectors.txt -oformat xgboost')
######与userID进行合并
fo_app=open('./transform_data/app/userid_app_doclevel_vectors.txt','w')
for i,line in enumerate(open('./transform_data/app/app_doclevel_vectors.txt')):
    if line.strip()== 'NULL':
        continue
    fo_app.write(str(appuserid2row[i])+' '+line.strip()+'\n')
    #print i,line
fo_app.close()