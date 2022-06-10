import pathlib,sqlite3,datetime
from datetime import date,datetime
today=date.today()
now = datetime.now().time()
c_year,c_month,c_day=str(today).split('-')
c_hour,c_min,c_sec=str(now).split(':')
d2 = datetime(int(c_year),int(c_month),int(c_day))


data_path=pathlib.Path(__file__).parent.absolute().joinpath('Databases')     
conn = sqlite3.connect(f"{data_path}/Student_info.db")
cur = conn.cursor()
std_roll_number=36
cur.execute(f'Select Sign_Name,Test_Completed,Start_Date,End_Date FROM Student_Tests where ID == {std_roll_number};')
passw2=cur.fetchall()
conn.close()
for details in passw2:
    text=details[2]
    start=text.split(' ')
    text2=start[0]
    year,month,day=text2.split('-')
    
    d1=datetime(int(year),int(month),int(day))
    text3=start[1]
    hr,min=text3.split(':')


    
    
    

    etext=details[3]
    end=etext.split(' ')
    text2=end[0]
    year,month,day=text2.split('-')
    c_year,c_month,c_day=str(today).split('-')
    d1=datetime(int(year),int(month),int(day))
    text3=start[1]
    hr,min=text3.split(':')
    


