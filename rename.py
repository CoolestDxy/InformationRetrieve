import os
path = "newcorpus/"
filename_list = os.listdir(path)
# a = 76
# for i in filename_list:
#     n=str(a)+'.'+i+'.txt'
#     os.rename(path+i,path+n)
#     a+=1
for i in filename_list:
    used_name = path + i
    with open(used_name,'r',encoding='utf-8')as f:
        c=''.join(i.split('.')[1:-1])+f.read()
    with open(path+i, 'w+', encoding='utf-8')as f:
        f.write(c)
