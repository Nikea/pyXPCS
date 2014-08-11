#!/usr/bin/env python
################################################################################
# Copyright (c) 2014, the European Synchrotron Radiation Facility              #
# All rights reserved.                                                         #
#                                                                              #
# Redistribution and use in source and binary forms, with or without           #
# modification, are permitted provided that the following conditions are met:  #
#                                                                              #
# * Redistributions of source code must retain the above copyright notice,     #
#   this list of conditions and the following disclaimer.                      #
#                                                                              #
# * Redistributions in binary form must reproduce the above copyright notice,  #
#  this list of conditions and the following disclaimer in the documentation   #
#  and/or other materials provided with the distribution.                      #
#                                                                              #
# * Neither the name of the European Synchrotron Radiation Facility nor the    #
#   names of its contributors may be used to endorse or promote products       #
#   derived from this software without specific prior written permission.      #
#                                                                              #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"  #
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE    #
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE   #
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE    #
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR          #
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF         #
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS     #
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN      #
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)      #
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE   #
# POSSIBILITY OF SUCH DAMAGE.                                                  #
################################################################################
#multiprocessing

import matplotlib.pylab as p
import sys, os.path, os, time,EdfFile,ytrc,threading
from numpy.ma import mask_or
from get_edf import file_name
from read_input import *
from some_modules_new import flatfield,rad_average, dropletize, loadedf, saveedf, headeredf
from commands import getoutput
from makemask import make_mask
from numpy import *
from multiprocessing import Process, Queue
from mp_corr import mp_corr
from scipy.optimize import leastsq
from IO import read_image,find_lagt
##################################################################
def dread(f,n,tot_darks,flat_field,static_corrected):
    global ccd_img, I_avg, I_avg2, I_avgs, ttdata, tread_cum, tdrop_cum, tI_avg,monitor,totsaxs,wtotmask

    ccd_img,monitor,tread,tdrop,totsaxs=read_image(f,input_info,flat_field,wtotmask,tot_darks,'none',static_corrected,totsaxs)
    tread_more=time.time()
    if q_2tcf!='none':
       ttdata[n,:]=ccd_img[index_in_q[q_2tcf-1]]
    if input_info['dropletize'].lower()== 'yes':
       for k in range(nq):
          I_avgs[n,k]=sum(ccd_img[index_in_q[k]])
    else:
       for k in range(nq):
          I_avgs[n,k]=mean(ccd_img[index_in_q[k]])
    I_avg[0,n]=I_avgs[n,0]
    I_avg2[0,n]=I_avgs[n,nq/2]
    tI_avg[0,n]= n*dt
    tread_cum+=time.time()-tread_more+tread
    return

def trc(matr):
    meanmatr=mean(matr,axis=1)
    tmp,lenmatr=shape(matr)
    meanmatr.shape=1,tmp
    trcm=dot(matr,matr.T)/lenmatr/dot(meanmatr.T,meanmatr)
    return trcm

def errfunc(pa,xdata,ydata):return (pa[0]+pa[1]*xdata-ydata)/sqrt(ydata*1e-8)

def errfuncc(pc,xdata,ydata):return (pc[0]+pc[1]*xdata-ydata)/sqrt(ydata*1e-8)

def vartrc(ttc):
    pc0=[1.0,0.1]
    n,tmp=shape(ttc)
    vtmp=[]
    for it in xrange(1,n-1):
        ###for aging###  
        #ydata=diag(ttc,it)
        #xdata=arange(1,len(ydata)+1)
        #p1,success=leastsq(errfuncc,pc0,args=(xdata,ydata))
        #vtmp.append(var(ydata/(p1[0]+p1[1]*xdata)))              
        ###for aging###
        vtmp.append(var(diag(ttc,it))) 
    return vtmp

def recurf(ll):
    global l,y,v
    y[ll+1].append((y[ll][0]+y[ll][1])*0.5)
    y[ll]=[]
    v[ll+1].append(vartrc(y[ll+1][-1]))
    if l[ll+1]==1:
        recurf(ll+1)
    else:
        l[ll+1]+=1
    l[ll]=0  
    return

#function plotinf
def ttplot(corfp,srp,slp,n,I1,I2):
    global tplot_cum,dt,firstfile
    tplot=time.time()
    rchplot=int(ceil(log(n/chn)/log(2))+1)
    normplot=zeros((1,rcr),dtype=float32)
    
    for ir in xrange(rchplot):
       if ir==0:
           normplot[0,:chn]=1./arange(n-2,n-chn-2,-1)
       else:
           normplot[0,chn2*(ir+1.):chn2*(ir+2.)]=1./arange((n-1)/(2**ir)-chn2-1,(n-1)/(2**ir)-chn-1,-1)

    indt=int(chn+chn2*log(n/chn)/log(2))-2
    cc1=corfp[0,:indt]/(slp[0,:indt]*srp[0,:indt])/normplot[0,:indt]
    cc2=corfp[-1,:indt]/(slp[-1,:indt]*srp[-1,:indt])/normplot[0,:indt]
    t_axis=lag[0,:indt]
    t_axis2=tI_avg[0,:n]
    t_axis2b=tI_avg[0,:n]/dt+firstfile
    lm1.set_data(t_axis,cc1)
    lm2.set_data(t_axis2,I1)
    lm1b.set_data(t_axis,cc2)
    lm2b.set_data(t_axis2b,I2)
    ax1.set_xlim(min(t_axis),max(t_axis))
    ax1.set_ylim(min(cc1),max(cc1))
    ax1b.set_ylim(min(cc2),max(cc2))
    ax2.set_xlim(min(t_axis2),max(t_axis2))
    ax2b.set_xlim(min(t_axis2b),max(t_axis2b))
    ax2.set_ylim(min(I1),max(I1))
    ax2b.set_ylim(min(I2),max(I2))
    p.draw()
    tplot_cum+=time.time()-tplot
    return 

########################READING INPUT FILE##################################    
def correlator_online_mp(fileinput='input.txt',dark_file='default',mask_file='default',plot='yes'):
   global nq, n, chn,chn2,rcr,index_in_q, lag, dt, norm, nc, I_avg, I_avg2, lm1, lm2, lm1b, lm2b, ax1,ax1b, ax2, ax2b, nq, detector, ccd_img, flat_field, tot_darks, totmask, ttdata,tcalc_cum, tplot_cum, tread_cum, tI_avg,static_corrected, firstfile, tolerance, I_avgs, xnq, Mythread,l,y,v, input_info, wtotmask,totsaxs,tI_avg,q_2tcf
   time1=time.time()
   p.rc('image',origin = 'lower')
   p.rc('image',interpolation = 'nearest')
   p.close()
   print 'multiprocessor'
   print 'reading input...'
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
   if avgt=='auto':
      lagt=[]
      lagt1=0
      for k in xrange(firstfile+40,firstfile+100):
        filename=file_name(dir+file_prefix,ext,k)
        while os.path.exists(filename) is False:
          sys.stdout.write(50*'\x08')
          sys.stdout.write('file '+filename+'still not ready')
          sys.stdout.flush()
           #rint 'file ' ,filename, 'still not ready'
          time.sleep(10)
        f=dataread(filename)
        params=f.GetHeader(0)
        if input_info['detector']=='medipix':
           lagt2=float32(float(params['time_of_frame']))
           lagt.append(lagt2-lagt1)
           lagt1=lagt2
#        if (input_info['detector']=='princeton' or input_info['detector']=='andor'):
        else:
           counters=params['counter_mne'].split(' ')
           lagt_ind=counters.index('ccdtavg')
           values=params['counter_pos'].split(' ')
           lagt.append(float32(float(values[lagt_ind])))
      del lagt[0]    
      dt=average(array(lagt,dtype=float32))
      print 'lag time =', dt 
   else:
      dt=float32(float(input_info['lag time']))
   q_2tcf=(input_info['q for TRC']).lower()
   if q_2tcf!='none':
      q_2tcf=int(q_2tcf)
   
   out_dir=get_dir(input_info['output directory'])
   out_prefix=get_prefix(input_info['output filename prefix'])
   out_tot=out_dir+out_prefix
   ##end processing input file#####  
   firstname=dir+file_name(file_prefix,ext,firstfile)
   f=dataread(firstname)
   ccd_info=f.GetStaticHeader(0)
   ncol=int(ccd_info['Dim_1'])
   nrows=int(ccd_info['Dim_2'])
   
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
      tot_darks=asfarray(dark.GetData(0),dtype=float32)
   
   toplot=static_data+.001 #to avoid zeros in plotting logarithm###
   print '...done'
   print '...reading q mask'
   if mask_file=='default':
      mask_file=out_tot+'mask.edf'
   print 'using mask file:', mask_file
   tot=EdfFile.EdfFile(mask_file)
   totmask=float32(tot.GetData(0)+tot.GetData(1))
   wtotmask=where(totmask==0)

   p.ion()
   fileq=out_tot+'qmask.edf'
   file=EdfFile.EdfFile(fileq)
   q=file.GetData(0)
   maxval=int(amax(q)+2)
   detector=input_info['detector']
   flatfield_file=input_info['flatfield file']
   if detector=='medipix':
      flat_field=flatfield(detector,flatfield_file)
   else:
      flat_field=1.0
   print '...done'
   if geometry=='saxs':
      print '...correcting static for baseline'
      xbeam=int(input_info['x direct beam'])
      ybeam=int(input_info['y direct beam'])
      static_data=rad_average(static_data,totmask,xbeam,ybeam)

   qaxis_list=[]
   npix_per_q=[]
   oneq=[]
   index_in_q=[]
   firstq=float32(float(input_info['first q']))
   deltaq=float32(float(input_info['delta q']))
   stepq=float32(float(input_info['step q']))
   qvalue=firstq+deltaq/2
   static_corrected=ones(shape(static_data),dtype=float32)
   q*=abs(totmask-1)
   total_pixels=0
   for i in range(2,maxval,2):
      indices=where(q==i)
      index_in_q.append(indices)#gives the indices of pixels that are not masked at this q
      if geometry=='saxs':
         static_corrected[indices]=mean(static_data[indices])/static_data[indices]
      npixel=len(static_data[indices])
      npix_per_q.append(npixel)
      oneq.append(ones((1,npixel)))
      qaxis_list.append(qvalue)
      qvalue+=deltaq+stepq
      total_pixels+=npixel
   print '...done'
   nq=len(npix_per_q)
   xnq=xrange(nq)
   ncores=1
   ncores=min(ncores,nq)
   tmp_pix=0
   q_sec=[]
   if nq==1:
      q_sec.append(0)
   elif ncores>=nq:
      q_sec=range(1,nq)
   else:
      for ii in xnq:
          if tmp_pix<total_pixels/(ncores):
             tmp_pix+=npix_per_q[ii]
             if ii== nq-1:
                 q_sec.append(ii)
          else:
              q_sec.append(ii)
              tmp_pix=0+npix_per_q[ii]
   ncores=len(q_sec)
   tmpdat=loadtxt(out_tot+'1Dstatic.dat')
   qaxis=tmpdat[:,0]
   I_q=tmpdat[:,1]
   del tmpdat





   ##FINISHED INITIALIZING PART OF THE CODE######
   ##START MAIN PART FOR CORRELATION#####
   chn=16.
   chn2=chn/2
   nfile=lastfile-firstfile
   rch=int(ceil(log(nfile/chn)/log(2))+1)
   ###2time
   if q_2tcf!='none':
         ttdata=zeros((nfile,npix_per_q[q_2tcf-1]),dtype=float32)
   ###2time
   rcr=chn+chn2*ceil(log(nfile/chn)/log(2))
   lag=zeros((1,rcr),dtype=float32)
   data_shape=p.shape(toplot)
   smatr=zeros(data_shape,dtype=float32)
   matr=zeros(data_shape,dtype=float32)
   norm=zeros((1,rcr),dtype=float32)
   for ir in xrange(rch):
    if ir==0:
        lag[0,:chn]=dt*arange(1,chn+1,1)
        norm[0,:chn]=1./arange(nfile-2,nfile-chn-2,-1)
    else:
        lag[0,chn2*(ir+1):chn2*(ir+2)]=(dt*2**ir)*arange(1+chn2,chn+1)
        norm[0,chn2*(ir+1):chn2*(ir+2)]=1./arange((nfile-1)/(2**ir)-chn2-1,(nfile-1)/(2**ir)-chn-1,-1)
   #END of declaring and initializing variables####
   #READING FILES 
   filenames=[]
   for k in xrange(firstfile,lastfile):
       filenames.append(file_name(file_prefix,ext,k))
   n=0
   if plot!='no':
      ax1=p.axes([0.11, 0.08, 0.75, 0.57])
      ax1.set_xlabel('t [sec]')
      ax1.set_ylabel('g^2(q,t)')
      ax1b=p.twinx(ax1)
      ax1b.yaxis.tick_right()
      ax2=p.axes([0.11, 0.73, 0.75, 0.19])
      ax2.xaxis.tick_bottom()
      ax2.set_xlabel('t [sec]')
      ax2.set_ylabel('I(q,t) [a.u.]')

      ax2b=p.gcf().add_axes(ax2.get_position(),frameon=False)
      ax2b.xaxis.tick_top()
      ax2b.yaxis.tick_right()
      ax2b.xaxis.set_label_position('top')
      ax2b.set_xlabel('Image no.')
      label1='q= %2.1e 1/Ang' % qaxis_list[0]
      label2='q= %2.1e 1/Ang' % qaxis_list[nq/2]
      lm1,=ax1.semilogx((1,),(1,),'ro-',label=label1)
      lm1b,=ax1b.semilogx((1,),(1,),'bo-',label=label2)
      ax1.legend(loc='lower left')
      ax1b.legend(loc=(0.02,0.1))
      lm2,=ax2.plot((1,),(1,),'r-')
      lm2b,=ax2b.plot((1,),(1,),'b-')
      p.setp(ax1.get_yticklabels(), color='r')
      p.setp(ax1b.get_yticklabels(), color='b')
      p.setp(ax2.get_yticklabels(), color='r')
      p.setp(ax2b.get_yticklabels(), color='b')
   tplot_cum=0
   tread_cum=0
   tcalc_cum=0
   tqueue_cum=0	
   I_avg=zeros((1,nfile),float32)
   I_avg2=zeros((1,nfile),float32)
   I_avgs=zeros((nfile,nq),float32)
   tI_avg=zeros((1,nfile),float32)
   mon=zeros((1,nfile),int16)
   
   detector=input_info['detector'].lower()
   Mythread=threading.Thread
   checkfile=os.path.exists
   n=0
   totsaxs=0*static_data
   goodsize=os.path.getsize(dir+filenames[n])
   nnfile=nfile-1
   #if plot!='no':
   #   tmpf=lambda x : True 
   #   thplot=Process(target=tmpf,args=([0]))   
   #   thplot.start()
######################multiprocessing#######################################################
   qur=[]  
   qure=[]  
   pcorr=[]
   for i in xrange(ncores):
       qur.append(Queue())
       qure.append(Queue())
   #qur.append(Queue())
   quplot=Queue() 
   for i in xrange(ncores):
       if i==0:
           q_beg=0
       else:
           q_beg=q_sec[i-1]
       q_end=q_sec[i]
       if i==ncores-1:
           q_end=nq
       pcorr.append(Process(target=mp_corr, args=(i,nfile,chn,plot,npix_per_q[q_beg:q_end],index_in_q[q_beg:q_end],qur[i],qure[i],quplot)))
   for i in xrange(ncores):
       pcorr[i].start()

   n=0
   nc=0
   nnfile=nfile-1
   if input_info['normalize'].lower()!= 'none':
     normalize=input_info['normalize'] 
     print "normalizing to ", input_info['normalize']
   else:
     print "not normalizing"
   while n<nnfile:
       tread=time.time()
       nc=n+1
       file=filenames[n]
       tmf=dir+file
       wait=0
       t0=time.time()
       stop=0
       while checkfile(tmf) is False:
          p.draw()
          sys.stdout.write(50*'\x08')
          sys.stdout.write('waiting for file'+ file+'...')
          sys.stdout.flush()
          t1=time.time()
          wait+=t1-t0
          time.sleep(dt)
          t0=t1
          if wait>10*dt:
            print nfile 
            ans=raw_input('\n will this file ever arrive? (y/N)')
            if ans.lower()=='y':
               print '\n keep waiting...\n'
               time.sleep(3*dt)
               wait=0
            else:
               stop=1
               nfile=n+1 
               break
       if stop==1:
         break
       if ext=='.edf':
          filesize=os.path.getsize(tmf)
          while filesize!=goodsize:
             sys.stdout.write(50*'\x08')
             sys.stdout.write('file '+ file+'still not ready...')
             sys.stdout.flush()
             time.sleep(dt)
             filesize=os.path.getsize(tmf)
       f=dataread(tmf)
       dread(f,n,tot_darks,flat_field,static_corrected)
       mon[0,n]=monitor
    #for plot. TO be faster, I only updated plot each chn files.
       jj=0
       tmp_put=[]
       tqueue=time.time()
       for i in xnq:
           if i <q_sec[jj]:
               tmp_put.append(ccd_img[index_in_q[i]])
           elif i==nq-1:
               tmp_put.append(ccd_img[index_in_q[i]])
               qur[jj].put(tmp_put)
           else:
               qur[jj].put(tmp_put)
               tmp_put=[]
               tmp_put.append(ccd_img[index_in_q[i]])  
               jj+=1  
       tqueue_cum+=time.time()-tqueue
       if nc%chn==0:
           pct=100.0*n/nfile
           sys.stdout.write(50*'\x08')
           sys.stdout.write('read '+str(int(pct))+'% of files'+32*' ')
           sys.stdout.flush()
           if plot!='no':
              #thplot.join()
              xx=quplot.get()
              ttplot(xx[0],xx[1],xx[2],n+1,I_avg[0,:n+1],I_avg2[0,:n+1])
              #thplot=Process(target=ttplot,args=([xx[0],xx[1],xx[2],n+1,I_avg[0,:n+1],I_avg2[0,:n+1]]))
              #thplot.start()
              #thplot.join()
       n+=1
   #if plot!='no':
      #thplot.join()  
   sys.stdout.write(50*'\x08')
   sys.stdout.flush()
   print "read 100% of files"
###############################################################################################
   from_proc=[]
   for i in xrange(ncores):
       from_proc.append(qure[i].get())
       pcorr[i].join()
       qure[i].close
       
#############################################################################################
   #END OF MAIN LOOP
   #calculate 2 times correlation function
   print "saving results..."
   if stop==1:
     tI_avg=tI_avg[:,:nfile] 
     mon=mon[:,:nfile]
     I_avgs=I_avgs[:nfile,:]
     rch=int(ceil(log(nfile/nchannels)/log(2))+1)
     for ir in xrange(rch):
       if ir==0:
         norm[0,:nchannels]=1./arange(nfile-2,nfile-nchannels-2,-1)
       else:
         norm[0,nchannels2*(ir+1):nchannels2*(ir+2)]=1./arange((nfile-1)/(2**ir)-nchannels2-1,(nfile-1)/(2**ir)-nchannels-1,-1)
   
   #calculate correlation functions
   corf=from_proc[0][0]
   sl=from_proc[0][1]
   sr=from_proc[0][2]
   tcalc_cum=from_proc[0][3]
   for i in xrange(1,ncores):
       corf=concatenate((corf,from_proc[i][0]),axis=0)
       sl=concatenate((sl,from_proc[i][1]),axis=0)
       sr=concatenate((sr,from_proc[i][2]),axis=0)
       tcalc_cum=max(tcalc_cum,from_proc[i][3])

   indt=int(chn+chn2*log(nfile/chn)/log(2))-2
   cc=zeros((indt,nq+1),float32)
   q_title='#q values:'
   trace_title='#file_no. ,   time, monitor,  q values:'
   for cindex in xnq:
       q_title=q_title+' '+str(qaxis_list[cindex])
       trace_title=trace_title+' '+str(qaxis_list[cindex])
       cc[:,cindex+1]=corf[cindex,:indt]/(sl[cindex,:indt]*sr[cindex,:indt])/\
       norm[0,:indt]
   cc[:,0]=lag[0,:indt]
   q_title=q_title+'\n'
   trace_title=trace_title+'\n'
   del indt
   f=open(out_tot+'cf.dat','w')
   f.write(q_title)
   savetxt(f, cc)
   f.close()
   del cc 
   f=open(out_tot+'trace.dat','w')
   f.write(trace_title)
   traces=zeros((nfile,nq+3),float32)
   traces[:,0]=tI_avg/dt+firstfile
   traces[:,1]=tI_avg
   traces[:,2]=mon
   traces[:,3:]=I_avgs
   savetxt(f,traces)
   f.close()
   del traces
   static=out_tot+'static.edf'
   static=EdfFile.EdfFile(static)
   totsaxs=totsaxs/n-tot_darks
   totsaxs[totsaxs<=0]=0
   static.WriteImage({},totsaxs,0)
   del static
   print 'correlation functions are saved to ', out_tot+'cf.dat'
   print 'traces are saved to ', out_tot+'trace.dat'
   if plot!='no':
      p.hold(True)
      p.close()
   if q_2tcf!='none':
      print "calculating time resolved cf and chi4..."
      if nfile>6000:  #this is for 4 GB RAM PC
         nfile=6000
         n=6000
      lind2=npix_per_q[q_2tcf-1]/16
      l=arange(5)*0
      y=[]
      v=[]
      for i in range(5):
         y.append([])
         v.append([])
      ib=0
      for i in xrange(16):
         sys.stdout.write(50*'\x08')
         sys.stdout.write('done '+str(int(i/16.*100))+'% of data'+32*' ')
         sys.stdout.flush()
         ie=ib+lind2
         y[0].append(trc(ttdata[:n-1,ib:ie]))
         v[0].append(vartrc(y[0][-1]))
         if l[0]==1:
            recurf(0)
         else:
            l[0]+=1
         ib+=lind2
      vm=[]
      for i in range(4,-1,-1):
         vm.append(mean(v[i],0))
      vm=array(vm)
      del ttdata
      del v
      sys.stdout.write(50*'\x08')
      sys.stdout.flush()
      file_2times=out_tot+'2times_q_'+str(q_2tcf)+'.edf'
      ytrc.write(file_2times,y[4][0])
      print 'Time resolved CF is saved to '+ out_tot+'2times_q_'+str(q_2tcf)+'.edf'
      N=array([[1],[2],[4],[8],[16]])/float(npix_per_q[q_2tcf-1])
      data=concatenate((N,vm),1).T
      #print 'number of pixels ',lind[ttcf_par] 
      #print 'q value=', qv[ttcf_par]
      p0=[0.0,1.0]
      it=range(len(data[1:,0]))
      p1=zeros((len(data[1:,0]),len(p0)+1))
      p1[:,0]=(asfarray(it)+1.0)*dt 
      xdata=data[0,:]
      for i in it:
         ydata=data[i+1,:]
         p1[i,1:],success=leastsq(errfunc,p0,args=(xdata,ydata))
      outfile=out_tot+'fitchi4_q_'+str(q_2tcf)+'.dat'
      f=open(outfile,'w')
      f.write("#time chi4 error q value:"+str(qaxis_list[q_2tcf-1])+"\n")
      savetxt(f,p1)
      f.close()
      print 'file is saved to '+outfile
   print "saving results..."
   time2=time.time()
   print 'elapsed time', time2-time1
   print 'elapsed time for plotting', tplot_cum
   print 'elapsed time for reading', tread_cum
   print 'elapsed time for correlating', tcalc_cum
   print 'elapsed time for queueing', tqueue_cum
   print 'used ncores=', ncores
