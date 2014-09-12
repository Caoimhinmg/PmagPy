#!/usr/bin/env python
import pmag,sys,numpy,exceptions
#
def main():
    """
    NAME
        igrf.py

    DESCRIPTION
        This program calculates igrf field values 
    using the routine of Malin and  Barraclough (1981) 
    based on d/igrfs from 1900 to 2010.
    between 1900 and 1000BCE, it uses CALS3K.4 or ARCH3K.1 
    Prior to 1000BCE, it uses CALS10k-4b
    Calculates reference field vector at  specified location and time.

  
    SYNTAX
       igrf.py [-h] [-i] -f FILE  [< filename]

    OPTIONS:
       -h prints help message and quits
       -i for interactive data entry
       -f FILE  specify file name with input data 
       -F FILE  specify output file name
       -ages MIN MAX INCR: specify age minimum in years (+/- AD), maximum and increment, default is line by line
       -loc LAT LON;  specify location, default is line by line
       -alt ALT;  specify altitude in km, default is sealevel (0)
       -plt; make a plot of the time series
       -fmt [pdf,jpg,eps,svg]  specify format for output figure  (default is svg)
       -mod [arch3k,cals3k,cals10k] specify model for 3ka to 1900 AD, default is cals10k
       -dip; plot dipole moment variations only    (only for last 3k years)
    INPUT FORMAT 
      interactive entry:
           date: decimal year
           alt:  altitude in km
           lat: positive north
           lon: positive east
       for file entry:
           space delimited string: date  alt   lat long

    OUTPUT  FORMAT
        Declination Inclination Intensity (nT) date alt lat long
    """
    lat,lon,agemin,agemax,dip,plt,fmt=0,0,'','',0,0,'svg'
    if '-fmt' in sys.argv:
        ind=sys.argv.index('-fmt')
        fmt=sys.argv[ind+1]
    if len(sys.argv)!=0 and '-h' in sys.argv:
        print main.__doc__
        sys.exit()
    if '-mod' in sys.argv:
        ind=sys.argv.index('-mod')
        mod=sys.argv[ind+1]
    else: mod=''
    if '-loc' not in sys.argv and '-f' not in sys.argv and '-ages' not in sys.argv: input=numpy.loadtxt(sys.stdin,dtype=numpy.float)
    if '-dip' in sys.argv: dip=1
    if '-loc' in sys.argv:
        ind=sys.argv.index('-loc')
        lat=float(sys.argv[ind+1])
        lon=float(sys.argv[ind+2])
    if '-alt' in sys.argv:
        ind=sys.argv.index('-alt')
        alt=float(sys.argv[ind+1])
    else: alt=0
    if '-f' in sys.argv:
        ind=sys.argv.index('-f')
        file=sys.argv[ind+1]
        input=numpy.loadtxt(file)
        print file,' read in'
    if '-ages' in sys.argv:
        ind=sys.argv.index('-ages')
        agemin=float(sys.argv[ind+1])
        agemax=float(sys.argv[ind+2])
        ageincr=float(sys.argv[ind+3])
        if '-dip' not in sys.argv: 
            if '-loc' not in sys.argv:
                print "must specify lat/lon if using age range option and not -dip"
                sys.exit()
            ages=numpy.arange(agemin,agemax,ageincr)
            lats=numpy.ones(len(ages))*lat
            lons=numpy.ones(len(ages))*lon
            alts=numpy.ones(len(ages))*alt
            input=numpy.array([ages,alts,lats,lons]).transpose()
    if '-i' in sys.argv:
        while 1:
          try:
            line=[]
            line.append(float(raw_input("Decimal year: <cntrl-D to quit> ")))
            alt=raw_input("Elevation in km [0] ")
            if alt=="":alt="0"
            line.append(float(alt))
            line.append(float(raw_input("Latitude (positive north) ")))
            line.append(float(raw_input("Longitude (positive east) ")))
            if mod=='':
                x,y,z,f=pmag.doigrf(line[3]%360.,line[2],line[1],line[0])
            else:
                x,y,z,f=pmag.doigrf(line[3]%360.,line[2],line[1],line[0],mod=mod)
            Dir=pmag.cart2dir((x,y,z))
            print '%8.2 %8.2 %8.0f'%(Dir[0],Dir[1],f)           
          except EOFError:
            print "\n Good-bye\n"
            sys.exit()
    if '-F' in sys.argv:
        ind=sys.argv.index('-F')
        outfile=sys.argv[ind+1]
        out=open(outfile,'w')
    else:outfile=""
    if '-plt' in sys.argv or '-dip' in sys.argv:
        plt=1
        import matplotlib
        matplotlib.use("TkAgg")
        import pylab
        pylab.ion()
        if '-M' not in sys.argv:
            fig=pylab.figure(num=1,figsize=(7,9))
        else:
            fig=pylab.figure(num=1,figsize=(7,3))
        Ages,Decs,Incs,Ints,VADMs=[],[],[],[],[]
    if dip:
        if mod=="":
            years,models=pmag.doigrf(0,0,0,0,models=1) # gets igrf11 coefficients
            years=years[0:-2] # peel off sec variation
            models=models[0:-2] # peel off sec variation
        else:
            years,models=pmag.doigrf(0,0,0,0,models=1,mod=mod)
        Bs=models.transpose()[0]
        VADMs=pmag.b_vdm(abs(Bs*1e-9),0)*1e-21
        Ys,Ms=[],[]
        if agemin=="":
            agemin,agemax=years[0],years[-1]
            if mod=='cals10k':agemin=-8000 
        for k in range(len(years)):
            if float(years[k])>float(agemin) and float(years[k])<float(agemax):
                Ys.append(years[k])
                Ms.append(VADMs[k])
        pylab.plot(Ys,Ms)
        pylab.ylabel('Dipole Moment (ZAm$^2$)')
        pylab.xlabel('Years')
        pylab.title(mod)
        pylab.draw()
        raw_input()
        sys.exit()
    for line in input:
        if mod=='':
            x,y,z,f=pmag.doigrf(line[3]%360.,line[2],line[1],line[0])
        else:
            x,y,z,f=pmag.doigrf(line[3]%360.,line[2],line[1],line[0],mod=mod)
        Dir=pmag.cart2dir((x,y,z))
        if outfile!="":
            out.write('%8.2f %8.2f %8.0f %7.1f %7.1f %7.1f %7.1f\n'%(Dir[0],Dir[1],f,line[0],line[1],line[2],line[3]))           
        elif plt:
            Ages.append(line[0])
            if Dir[0]>180: Dir[0]=Dir[0]-360.0
            Decs.append(Dir[0])
            Incs.append(Dir[1])
            Ints.append(f*1e-3)
            VADMs.append(pmag.b_vdm(f*1e-9,line[2])*1e-21)
        else:
            print '%8.2f %8.2f %8.0f %7.1f %7.1f %7.1f %7.1f'%(Dir[0],Dir[1],f,line[0],line[1],line[2],line[3])           
    if plt:
        fig.add_subplot(411)
        pylab.plot(Ages,Decs)
        pylab.ylabel('Declination ($^{\circ}$)')
        fig.add_subplot(412)
        pylab.plot(Ages,Incs)
        pylab.ylabel('Inclination ($^{\circ}$)')
        fig.add_subplot(413)
        pylab.plot(Ages,Ints)
        pylab.ylabel('Intensity ($\mu$T)')
        fig.add_subplot(414)
        pylab.plot(Ages,VADMs)
        pylab.ylabel('VADMs (ZAm$^2$)')
        pylab.xlabel('Ages')
        pylab.draw()
        ans=raw_input("S[a]ve to save figure, <Return>  to quit  ")
        if ans=='a':
            pylab.savefig('igrf.'+fmt)
            print 'Figure saved as: ','igrf.'+fmt
        sys.exit()
main()

