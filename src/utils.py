def ok(*args):
  print("\u001b[32m[+]\u001b[0m", *args)

def error(*args):
  print("\u001b[31m[-]\u001b[0m", *args)

def print_header():
  print(''' (   (                                                 
 )\ ))\ )         )                          )         
(()/(()/(      ( /(  (  (         (       ( /(    (    
 /(_))(_))(    )\())))\ )(   (   ))\`  )  )\())(  )(   
(_))(_))  )\ )(_))//((_|()\  )\ /((_)(/( (_))/ )\(()\  
| _ \_ _|_(_/(| |_(_))  ((_)((_|_))((_)_\| |_ ((_)((_) 
|  _/| || ' \))  _/ -_)| '_/ _|/ -_) '_ \)  _/ _ \ '_| 
|_| |___|_||_| \__\___||_| \__|\___| .__/ \__\___/_|   
                                   |_|                 ''')
  ok("Starting up")