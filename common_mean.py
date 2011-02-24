#!/usr/bin/env python
import sys,pmagplotlib,pmag,exceptions
def main():
    """
    NAME
       common_mean.py

    DESCRIPTION
       calculates bootstrap statistics to test for common mean

    INPUT FORMAT
       takes dec/inc as first two columns in two space delimited files
   
    SYNTAX
       common_mean.py [command line options]
    
    OPTIONS
       -h prints help message and quits
       -f FILE, input file 
       -f2 FILE, optional second file to compare with first file
       -dir D I, optional direction to compare with input file
    NOTES
       must have either F2 OR dir but not both
     

    """
    D1,D2,d,i,file2=[],[],"","",""
    if '-h' in sys.argv: # check if help is needed
        print main.__doc__
        sys.exit() # graceful quit
    if '-f' in sys.argv:
        ind=sys.argv.index('-f')
        file1=sys.argv[ind+1]
    if '-f2' in sys.argv:
        ind=sys.argv.index('-f2')
        file2=sys.argv[ind+1]
    if '-dir' in sys.argv:
        ind=sys.argv.index('-dir')
        d=float(sys.argv[ind+1])
        i=float(sys.argv[ind+2])
    f=open(file1,'rU')
    for line in f.readlines():
        rec=line.split()
        Dec,Inc=float(rec[0]),float(rec[1]) 
        D1.append([Dec,Inc])
    f.close()
    if file2!="":
        f=open(file2,'rU')
        for line in f.readlines():
            rec=line.split()
            Dec,Inc=float(rec[0]),float(rec[1]) 
            D2.append([Dec,Inc])
        f.close()
#
    counter,NumSims=0,1000
#
# get bootstrapped means for first data set
#
    print "Doing first set of directions, please be patient.."
    BDI1=pmag.di_boot(D1)
#
#   convert to cartesian coordinates X1,X2, Y1,Y2 and Z1, Z2
#
    if d=="": # repeat for second data set
        BDI2=pmag.di_boot(D2)
    else:
        BDI2=[]
# set up plots
    CDF={'X':1,'Y':2,'Z':3}
    pmagplotlib.plot_init(CDF['X'],4,4)
    pmagplotlib.plot_init(CDF['Y'],4,4)
    pmagplotlib.plot_init(CDF['Z'],4,4)
# draw the cdfs
    pmagplotlib.plotCOM(CDF,BDI1,BDI2,[d,i])
    pmagplotlib.drawFIGS(CDF)
    try:
        raw_input("Return to save plots - <cntl-D> to quit")
    except:
       print "\n Good bye\n"
       sys.exit()
    files={}
    files['X']='CD_X.svg'
    files['Y']='CD_Y.svg'
    files['Z']='CD_Z.svg'
    pmagplotlib.saveP(CDF,files)
 
main()

