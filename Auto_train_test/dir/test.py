import os
l=os.listdir('D:\\Virtual_Sign_Language_Avatar\\Auto_train_test\\videos\\Computer\\')
li=[x.split('.')[0] for x in l]
print(li)
       
