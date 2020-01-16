# ------- main module ------
# Данный файл не изменяем!!!

try:
    from customEval import *
except:
    print("unable to import customEval")
    grade(0)
    exit()
    
# checking code
main()
