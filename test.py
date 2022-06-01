import subprocess,sys
pass1=subprocess.check_output([sys.executable, "test_time.py"])
temp=str(pass1)
temp=temp.replace('b',"")
temp2=temp.split('\\r\\n')
print(temp2)