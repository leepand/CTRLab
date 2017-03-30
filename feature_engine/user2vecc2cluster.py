'''Items2vec pre-train: process categorical features'''
import time
start =time.clock()
fo = open( './pretraindata/item2vectors.libsvm', 'w' )
fw = open( './pretraindata/item2vectors.words', 'w' )
is_first_line=True
n=0
items2row={}
for l in open( './pretraindata/Itemsvectors.txt' ):
    if is_first_line:
        is_first_line=False
        continue
    arr = l.split(' ')    
    if arr[0] == 'p______':
        fo.write('1')
        fw.write(arr[0])
        items2row[n]=arr[0]
        
    else:
        #assert arr[0] == 0
        fo.write('0')
        fw.write(arr[0])
        items2row[n]=arr[0]
        n=n+1
    
    for i in range( 1,len(arr)-1 ):
        #print arr[i]
        fo.write( ' %d:%s' % (i,(arr[i].strip())))
    fo.write('\n')
    fw.write('\n')
fo.close()
fw.close()
print 'done!'
end = time.clock()
print('Running time: %s Seconds'%(end-start))#其中end-start就是程序运行的时间，单位是秒。
#也可以使用https://github.com/mblondel/svmlight-loader  把sklearn.datasets替换成svmlight-loader即可，不过要在lunix下
from sklearn.datasets import load_svmlight_file
import kmc2
import time
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.cluster import k_means
start =time.clock()
#X_train, y_train = load_svmlight_file("./weibo_sparase10w.txt")
X_train, y_train = load_svmlight_file("./pretraindata/item2vectors.libsvm")
#根据聚类的中心点计算每个新的向量归属的类别
start =time.clock()
seeding = kmc2.kmc2(X_train, 100)  # Run k-MC2 with k=5
cluster_assignments = -np.ones(X_train.shape[0], dtype=np.int32)
dists = euclidean_distances(X_train, seeding, squared=True)
np.argmin(dists, axis=1, out=cluster_assignments)
#print type(cluster_assignments)
#print cluster_assignments.size
f1 = open('./pretraindata/items2cluster.txt','w')
for i in range(cluster_assignments.size):
    #print cluster_assignments[i]
    item=items2row[i]
    f1.write(str(item)+' '+str(cluster_assignments[i])+'\n')
f1.close()
end = time.clock()
print('Running time: %s Seconds'%(end-start))#其中end-start就是程序运行的时间，单位是秒。