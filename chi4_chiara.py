#!/usr/bin/env python
import matplotlib.pylab as p
import os.path, os, sys, time, EdfFile, ytrc
from numpy.ma import mask_or
from get_edf import file_name
from read_input import *
from some_modules_new import flatfield, rad_average, dropletize
from commands import getoutput
from makemask import make_mask
from numpy import *
from multiprocessing import Process, Queue
from scipy.optimize import leastsq
from IO import find_lagt,read_image

def dtrc(ccd_img,nc):
    global ttdata,ttmint,tcalc_cum
    tcalc=time.time() 
    tmpx=float32(ccd_img[indices])#*static_corrected)
    for i in lnum:
        ib=0
        lind2=npixel/2**i
        for ii in xrange(2**i):
            ie=ib+lind2
            ttdata[i][ii][nc,:]=tmpx[ib:ie]
            ttmint[i][ii][0,nc]=mean(tmpx[ib:ie])
            ib=ib+lind2
    tcalc_cum+=time.time()-tcalc
#error function for fitting
def errfunc(pa,xdata,ydata):return (pa[0]+pa[1]*xdata-ydata)/sqrt(ydata*1e-8)

def errfuncc(pc,xdata,ydata):return (pc[0]+pc[1]*xdata-ydata)/sqrt(ydata*1e-8)

def mydot(qu,ttdatap,ttmintp,lindp,i,n):
    v=[]
    for ii in xrange(2**i):
        ttc=dot(ttdatap[ii],ttdatap[ii].T)/lindp/dot(ttmintp[ii].T,ttmintp[ii])#-1
        vtmp=[]
        for it in xrange(1,n-1):
            vtmp.append(var(diag(ttc,it)))#classical way 
        v.append(vtmp)
    qu.put(mean(v,0))






########################READING INPUT FILE##################################    
def chi4(q_chi4='default',fileinput='input.txt',dark_file='default',mask_file='default',):
   global detector, flat_field, tread_cum, indices, static_corrected, lnum, npixel, ttdata, ttmint, tcalc_cum, tot_darks, tolerance, ccd_img,totmask,tdrop_cum, input_info
   time1=time.time()
   print 'reading input...'
   print fileinput
   input_info=get_input(fileinput)
   ##processing input file#####
   dir= input_info['dir']
   dir_dark= input_info['dark dir']
   if dir_dark=='none':
      dir_dark=dir
   file_prefix=input_info['file_prefix']
   ext = input_info['file_suffix']
# New version has capabilities of reading also .gz files
   if ext == '.edf.gz':
     dataread=EdfFile.EdfGzipFile
   else:
     dataread=EdfFile.EdfFile
   
   firstfile=int(input_info['n_first_image'])
   lastfile=int(input_info['n_last_image'])+1
   firstdark=input_info['n_first_dark']
   if firstdark.lower() != 'none':
      firstdark=int(input_info['n_first_dark'])
      lastdark=int(input_info['n_last_dark'])+1
   geometry=input_info['geometry'].lower()
   tolerance=float32(float(input_info['tolerance']))
   avgt = input_info['lag time'].lower()
   dt=find_lagt(avgt,input_info,dataread)
#####End of stuff for extracting the lag time automatically############3
   if q_chi4=='default':
      q_2tcf=(input_info['q for TRC']).lower()
      if q_2tcf!='none':
         q_2tcf=int(q_2tcf)
   else:
      q_2tcf=q_chi4 
   
   out_dir=get_dir(input_info['output directory'])
   if os.path.exists(out_dir) is False:
      com='mkdir '+out_dir
      print getoutput(com)
   out_prefix=get_prefix(input_info['output filename prefix'])
   print out_prefix
   out_tot=out_dir+out_prefix
   print '...done'
   ##end processing input file#####  

   firstname=dir+file_name(file_prefix,ext,firstfile)
   f=dataread(firstname)
   ccd_info=f.GetStaticHeader(0)
   ncol=int(ccd_info['Dim_1'])
   nrows=int(ccd_info['Dim_2'])
#reading static data and dark   
   static=out_tot+'static.edf'
   static=EdfFile.EdfFile(static)
   static_data=asfarray(static.GetData(0),dtype=float32)
   if input_info['n_first_dark'].lower()=='none':
      print 'not using darks'
      tot_darks=0*static_data
   else:
      print 'using darks'
      if dark_file=='default': 
         dark_file=out_tot+'dark.edf'
      print 'using dark file:', dark_file
      dark=EdfFile.EdfFile(dark_file)
      tot_darks=asfarray(dark.GetData(0),dtype=float64)
#End of reading static data and dark      
   print '...done'
   print '...reading q mask'
   if mask_file=='default':
      mask_file=out_tot+'mask.edf'
   print 'using mask file:', mask_file
   tot=EdfFile.EdfFile(mask_file)
   mask1=tot.GetData(0)
   mask2=tot.GetData(1)
   totmask=float32(mask1+mask2)

   fileq=out_tot+'qmask.edf'
   file=EdfFile.EdfFile(fileq)
   q=file.GetData(0)
   maxval=int(amax(q)+2)
   detector=input_info['detector']
   if detector=='medipix':
      flatfield_file=input_info['flatfield file']
      flat_field=flatfield(detector, flatfield_file)

   print '...done'
   if geometry=='saxs':
      print '...correcting static for baseline'
      xbeam=int(input_info['x direct beam'])
      ybeam=int(input_info['y direct beam'])
      static_data=rad_average(static_data,totmask,xbeam,ybeam)

   static_corrected=ones(shape(static_data),dtype=float64)
   print '...done'
   
   q_2times=file.GetData(0)
   q_2times[q_2times!=2*q_2tcf]=1
   q_2times[q_2times==2*q_2tcf]=0
   pixels=get_pixelsq(static_data,totmask+q_2times)
   npixel=len(pixels)
   indices=where(q_2times+totmask==0)
   if geometry=='saxs':
      static_corrected=mean(static_data[indices])/static_data[indices]
   else:
      static_corrected=static_corrected[indices]


   lnum=xrange(5)
   filen=lastfile-firstfile
   ###2time
   ttdata=[[],[],[],[],[]]
   ttmint=[[],[],[],[],[]]
   for i in lnum:
       for ii in xrange(2**i):
           ttdata[i].append(zeros((filen,int(npixel/(2**i))),float32))
           ttmint[i].append(zeros((1,filen),float32))
   ###2time

   ccd_img=zeros((ncol,nrows),dtype=float64)
   filenames=[]
   for k in xrange(firstfile,lastfile):
       filenames.append(file_name(file_prefix,ext,k))
   n=0
   tread_cum=0
   tcalc_cum=0
   tdrop_cum=0
 
   detector=input_info['detector'].lower()
   #START OF MAIN LOOP
   checkfile=os.path.exists
   goodsize=os.path.getsize(dir+filenames[n])


   while n<filen:
       #ccd_imgn=ccd_img
       file=filenames[n]
       tmf=dir+file
       while checkfile(tmf) is False:
           print 'waiting for file ', file, '...'
           time.sleep(3*dt)
       if ext != '.edf.gz':
          filesize=os.path.getsize(tmf)
          while filesize!=goodsize:
              print 'file ', file, 'still not ready...'
              print filesize
              time.sleep(2*dt)
              filesize=os.path.getsize(tmf)

       f=dataread(dir+file)
       ccd_img,tread,tdrop = read_image(f,input_info,flat_field,totmask,tot_darks,indices,static_corrected)
       tread_cum+=tread
       tdrop_cum+=tdrop

       dtrc(ccd_img,n) 
       n+=1
       pct=float32(n*100.0/filen)
       sys.stdout.write(18*'\x08')
       sys.stdout.write('read '+str(int(pct))+'% of files')
       sys.stdout.flush()
   sys.stdout.write(18*'\x08')
   sys.stdout.flush()
   print "read 100% of files"
   #END OF MAIN LOOP
   print 'elapsed time for the loop', time.time()-time1
   ttc=zeros((n,n),float32)
   vm=[]
   number=0.0
   print 'start calculation of ttcf'
   tcalc_cum0=time.time()
   qu=range(5)
   pp=range(5)
   for i in lnum:
       qu[i]=Queue()
       pp[i]=Process(target=mydot, args=(qu[i],ttdata[i],ttmint[i],floor(npixel/2**i),i,n))
       pp[i].start()
   for i in lnum:
       vm.append(qu[i].get())
   for i in lnum:
       pp[i].join()
   tcalc_cum=time.time()-tcalc_cum0
   print 'finish calculating'    
   del ttdata
   del ttmint
   del ttc
   vm=array(vm,dtype=float32)
   npixel=float32(npixel)
   N=array([[1],[2],[4],[8],[16]])/npixel
   z=concatenate((N,vm),1).T 
   f=out_tot+'chi4_q_'+str(q_2tcf)+'.dat'
   savetxt(f,z)

   print 'file is saved to '+out_tot+'chi4_q_'+str(q_2tcf)+'.dat'
   print 'number of pixels ',npixel 
   print 'elapsed time', time.time()-time1
   print 'elapsed time for reading', tread_cum-tdrop_cum
   if input_info['dropletize'].lower()=='yes':
      print 'elapsed time for dropletizing', tdrop_cum
   print 'elapsed time for correlate', tcalc_cum
   p0=[0.0,1.0]

   data=loadtxt(f)
  
   it=range(len(data[1:,0]))
   p1=zeros((len(data[1:,0]),len(p0)+1))
   p1[:,0]=(asfarray(it,dtype=float32)+1.0)*dt 
   xdata=data[0,:]
   for i in it:
      ydata=data[i+1,:]
      p1[i,1:],success=leastsq(errfunc,p0,args=(xdata,ydata))
   print time.time()-time1
   outfile=out_tot+'fitchi4_q_'+str(q_2tcf)+'.dat'
   savetxt(outfile,p1)
   print 'file is saved to '+outfile
