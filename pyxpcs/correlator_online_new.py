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
import matplotlib.pylab as p
import sys, os.path, os, time, EdfFile, ytrc
from numpy.ma import mask_or
from get_edf import file_name
from read_input import *
from some_modules_new import flatfield,rad_average, dropletize, loadedf, saveedf, headeredf,headersedf
from commands import getoutput
from makemask import make_mask
from numpy import *
from threading import Thread
from IO import read_image,find_lagt
from scipy.optimize import leastsq

def dread(f,n,tot_darks,flat_field,static_corrected):
    global ccd_img, I_avg, I_avg2, I_avgs, ttdata, tread_cum, tdrop_cum, tI_avg,monitor,totsaxs,wtotmask

    ccd_img,monitor,tread,tdrop,totsaxs=read_image(f,input_info,flat_field,wtotmask,tot_darks,'none',static_corrected,totsaxs)
    tread_more=time.time()
    if q_2tcf!='none':
       ttdata[n,:]=ccd_img[index_in_q[q_2tcf-1]]
    if input_info['dropletize'].lower()== 'yes':
       for k in range(nq):
          I_avgs[k,n]=sum(ccd_img[index_in_q[k]])
    else:
       for k in range(nq):
          I_avgs[k,n]=mean(ccd_img[index_in_q[k]])
    I_avg[0,n]=I_avgs[0,n]
    I_avg2[0,n]=I_avgs[nq/2,n]
    tI_avg[0,n]= n*dt
    tread_cum+=time.time()-tread_more+tread
    tdrop_cum+=tdrop

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
    

#function plotinf
def ttplot(corf,sr,sl,norm,n, I1, I2,lag):
    global tplot_cum
    firstfile=int(input_info['n_first_image'])
    tplot=time.time()
    rchplot=int(ceil(log(n/nchannels)/log(2))+1)
    normplot=zeros((1,rcr),dtype=float32)
    
    for ir in xrange(rchplot):
       if ir==0:
           normplot[0,:nchannels]=1./arange(n-2,n-nchannels-2,-1)
       else:
           normplot[0,nchannels2*(ir+1):nchannels2*(ir+2)]=1./arange((n-1)/(2**ir)-nchannels2-1,(n-1)/(2**ir)-nchannels-1,-1)

    indt=int(nchannels+nchannels2*log(n/nchannels)/log(2))-2
    cc1=corf[0,:indt]/(sl[0,:indt]*sr[0,:indt])/normplot[0,:indt]
    cc2=corf[nq/2,:indt]/(sl[nq/2,:indt]*sr[nq/2,:indt])/normplot[0,:indt]
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
    

#function correlator
def correlator(reg,matrx):
    global datreg, corf, sl, sr, norm, tcalc_cum,sst
    tcalc=time.time()
    if nc<=nchannels:
        if nc>=2:
            for cindex in xnq:
                sr[cindex,:n]=roll(sr[cindex,:n],1)
                sr[cindex,0]=sr[cindex,1]+sst[reg][cindex]#average intensity in q for normalization right
                sst[reg][cindex]=dot(oneq[cindex],matrx[index_in_q[cindex]])/lind[cindex]
                sl[cindex,:n]+=sst[reg][cindex]#average intensity in q for normalization left 
        else:
            for cindex in xnq:
                sst[reg][cindex]=dot(oneq[cindex],matrx[index_in_q[cindex]])/lind[cindex]
        for cindex in xnq:
            corf[cindex,:n]+=dot(matrx[index_in_q[cindex]].T,datreg[reg][cindex][:,:n])/lind[cindex] #calculate a product of input data and register corf(number of q's, number of chanels)
            datreg[reg][cindex]=concatenate((reshape(matrx[index_in_q[cindex]],(lind[cindex],1)), datreg[reg][cindex][:,:nchannels-1]), axis=1) #shift register by 1
        if nc/2==nc/2.:
            for cindex in xnq:
                matrx[index_in_q[cindex]]=(datreg[reg][cindex][:,0]+datreg[reg][cindex][:,1])/2 #data for the next register from present
            correlator2(1,matrx)
    else:
        for cindex in xnq:
            sr[cindex,:nchannels]=roll(sr[cindex,:nchannels],1)
            sr[cindex,0]=sr[cindex,1]+sst[reg][cindex]#average intensity in q for normalization right
            sst[reg][cindex]=dot(oneq[cindex],matrx[index_in_q[cindex]])/lind[cindex]
            sl[cindex,:nchannels]+=sst[reg][cindex]#average intensity in q for normalization left
            corf[cindex,:nchannels]+=dot(matrx[index_in_q[cindex]].T,datreg[reg][cindex])/lind[cindex] #calculate a product of input data and register corf(number of q's, number of chanels)
            datreg[reg][cindex]=concatenate((reshape(matrx[index_in_q[cindex]],(lind[cindex],1)), datreg[reg][cindex][:,:nchannels-1]), axis=1) #shift register by 1  
        if nc/2==nc/2.:
            for cindex in xnq:
                matrx[index_in_q[cindex]]=(datreg[reg][cindex][:,0]+datreg[reg][cindex][:,1])/2 #data for the next register from present
            correlator2(1,matrx)
    tcalc_cum+=time.time()-tcalc
################################################################            
#correlator2(reg,matrx)

def correlator2(reg,matrx):
    global datreg, corf, sl, sr, norm, srr, sll,sst
    condition=((reg+1)<rch and nc/2**(reg+1)==nc/2.**(reg+1))
    corn=nc/2.**reg
    if 2<=corn<=nchannels:#corn<=nchannels and corn>=2:
        for cindex in xnq:
            srr[reg][cindex,:corn-1]=roll(srr[reg][cindex,:corn-1],1)
            srr[reg][cindex,0]=srr[reg][cindex,1]+sst[reg][cindex]#average intensity in q for normalization right
            sst[reg][cindex]=dot(oneq[cindex],matrx[index_in_q[cindex]])/lind[cindex]
            sll[reg][cindex,:corn-1]+=sst[reg][cindex]#average intensity in q for normalization left
    if corn>nchannels:
        for cindex in xnq:
            srr[reg][cindex,:nchannels]=roll(srr[reg][cindex,:nchannels],1)
            srr[reg][cindex,0]=srr[reg][cindex,1]+sst[reg][cindex]#average intensity in q for normalization right
            sst[reg][cindex]=dot(oneq[cindex],matrx[index_in_q[cindex]])/lind[cindex] 
            sll[reg][cindex,:nchannels]+=sst[reg][cindex]#average intensity in q for normalization left
    if  nchannels2<corn<=nchannels:#corn<=nchannels and corn>nchannels/2:
        inb=nchannels2*(reg+1)
        ine=corn+nchannels2*reg
        sl[:,inb:ine]=sll[reg][:,nchannels2:corn]
        sr[:,inb:ine]=srr[reg][:,nchannels2:corn]
        for cindex in xnq:
            corf[cindex,inb:ine]+=dot(matrx[index_in_q[cindex]].T,datreg[reg][cindex][:,nchannels2:corn])/lind[cindex] #calculate a product of input data and register corf(number of q's, number of chanels)
            datreg[reg][cindex]=concatenate((reshape(matrx[index_in_q[cindex]],(lind[cindex],1)), datreg[reg][cindex][:,:nchannels-1]), axis=1) #shift register by 1 
        if condition:#nc/2**(reg+1)==floor(nc/2**(reg+1)):
            for cindex in xnq:
                matrx[index_in_q[cindex]]=(datreg[reg][cindex][:,0]+datreg[reg][cindex][:,1])/2 #data for the next register from present
            reg+=1
            correlator2(reg,matrx)
    elif corn>nchannels:
        inb=nchannels2*(reg+1)
        ine=nchannels2*(reg+2)
        sl[:,inb:ine]=sll[reg][:,nchannels2:nchannels]
        sr[:,inb:ine]=srr[reg][:,nchannels2:nchannels]
        for cindex in xnq:
            corf[cindex,inb:ine]+=dot(matrx[index_in_q[cindex]].T, datreg[reg][cindex][:,nchannels2:nchannels])/lind[cindex] #calculate a product of input data and register corf(number of q's, number of chanels)
            datreg[reg][cindex]=concatenate((reshape(matrx[index_in_q[cindex]],(lind[cindex],1)), datreg[reg][cindex][:,:nchannels-1]), axis=1) #shift register by 1 
        if condition:#nc/2**(reg+1)==floor(nc/2**(reg+1))
            for cindex in xnq:
                matrx[index_in_q[cindex]]=(datreg[reg][cindex][:,0]+datreg[reg][cindex][:,1])/2 #data for the next register from present"""
            reg+=1
            correlator2(reg,matrx)
    else: 
        for cindex in xnq:
            sst[reg][cindex]=dot(oneq[cindex],matrx[index_in_q[cindex]])/lind[cindex]
        for cindex in xnq:
            datreg[reg][cindex]=concatenate((reshape(matrx[index_in_q[cindex]],(lind[cindex],1)), datreg[reg][cindex][:,:nchannels-1]), axis=1) #shift register by 1 
        if condition:#nc/2**(reg+1)==floor(nc/2**(reg+1)):
            for cindex in xnq:
                 matrx[index_in_q[cindex]]=(datreg[reg][cindex][:,0]+datreg[reg][cindex][:,1])/2 #data for the next register from present"""
            reg+=1
            correlator2(reg,matrx)
           
########################################################################

########################READING INPUT FILE##################################    
def correlator_online(fileinput='input.txt',dark_file='default',mask_file='default',plot='yes'):
   global datreg, nq, corf, n, sl, sr, nchannels, nchannels2, index_in_q, lind, dt, norm, srr, sll, nc, oneq, I_avg, I_avg2, lm1, lm2, lm1b, lm2b, ax1,ax1b, ax2, ax2b, ccd_img, ttdata,tcalc_cum, tplot_cum, tread_cum, tdrop_cum, tI_avg,q_2tcf, I_avgs, rch, rcr,totsaxs,input_info,l,y,v, sst, xnq, wtotmask

   time1=time.time()
   p.rc('image',origin = 'lower')
   p.rc('image',interpolation = 'nearest')
   
   print 'reading input...'
   input_info=get_input(fileinput)
##########################processing input file###############################
   dir= input_info['dir']
   dir_dark= input_info['dark dir']
   if dir_dark=='none':
      dir_dark=dir
   file_prefix=input_info['file_prefix']
   ext = input_info['file_suffix']
#####New version has capabilities of reading also .gz files####
   if ext == '.edf.gz':
     dataread=EdfFile.EdfGzipFile
   else:
     dataread=EdfFile.EdfFile
##################################################
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
   print 'lag time =', dt 
   q_2tcf=(input_info['q for TRC']).lower()
   if q_2tcf!='none':
      q_2tcf=int(q_2tcf)
   
   out_dir=get_dir(input_info['output directory'])
   out_prefix=get_prefix(input_info['output filename prefix'])
   out_tot=out_dir+out_prefix
   print '...done'
##################end processing input file###################################  
   firstname=dir+file_name(file_prefix,ext,firstfile)
   f=dataread(firstname)
   ccd_info=f.GetStaticHeader(0)
   ncol=int(ccd_info['Dim_1'])
   nrows=int(ccd_info['Dim_2'])
   
   static=out_tot+'static.edf'
   static_data=asfarray(loadedf(static),dtype=float32)
   if input_info['n_first_dark'].lower()=='none':
      print 'not using darks'
      tot_darks=0*static_data
   else:
      print 'using darks'
      if dark_file=='default': 
         dark_file=out_tot+'dark.edf'
      print 'using dark file:', dark_file
      tot_darks=asfarray(loadedf(dark_file),dtype=float32)
   toplot=static_data+.001 #to avoid zeros in plotting logarithm###
   print '...done'
   print '...reading mask'
   if mask_file=='default':
      mask_file=out_tot+'mask.edf'
   print 'using mask file:', mask_file
   totmask=loadedf(mask_file,0)+loadedf(mask_file,1)
   wtotmask=where(totmask==0)
   p.ion()
   fileq=out_tot+'qmask.edf'
   q=loadedf(fileq)
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
   print '...done'
   nq=len(npix_per_q)
   xnq=xrange(nq)
   tmpdat=loadtxt(out_tot+'1Dstatic.dat')
   qaxis=tmpdat[:,0]
   I_q=tmpdat[:,1]
   del tmpdat



   ##FINISHED INITIALIZING PART OF THE CODE######
   ##START MAIN PART FOR CORRELATION#####
   nchannels=16.
   nchannels2=nchannels/2
   nfile=lastfile-firstfile
   datregt=[]
   datreg=[]
   rch=int(ceil(log(nfile/nchannels)/log(2))+1)
   ###2time
   if q_2tcf!='none':
         ttdata=zeros((nfile,npix_per_q[q_2tcf-1]),dtype=float32)
   ###2time
   for ir in xrange(rch):
       for iq in xnq:
           datregt.append(zeros((npix_per_q[iq],nchannels),dtype=float32))
       datreg.append(datregt)
       datregt=[]
   del datregt
   rcr=nchannels+nchannels2*ceil(log(nfile/nchannels)/log(2))
   corf=zeros((nq,rcr),dtype=float32)
   lag=zeros((1,rcr),dtype=float32)
   data_shape=p.shape(toplot)
   smatr=zeros(data_shape,dtype=float32)
   matr=zeros(data_shape,dtype=float32)
   sl=zeros((nq,rcr),dtype=float32)
   sr=zeros((nq,rcr),dtype=float32)
   norm=zeros((1,rcr),dtype=float32)
   sll=[]
   srr=[]
   sst=[]

   for ir in xrange(rch):
       if ir==0:
           lag[0,:nchannels]=dt*arange(1,nchannels+1,1)
           norm[0,:nchannels]=1./arange(nfile-2,nfile-nchannels-2,-1)
       else:
           lag[0,nchannels2*(ir+1):nchannels2*(ir+2)]=(dt*2**ir)*arange(1+nchannels2,nchannels+1)
           norm[0,nchannels2*(ir+1):nchannels2*(ir+2)]=1./arange((nfile-1)/(2**ir)-nchannels2-1,(nfile-1)/(2**ir)-nchannels-1,-1)
       sll.append(zeros((nq,nchannels),dtype=float32))
       srr.append(zeros((nq,nchannels),dtype=float32))
       sst.append(arange(nq)*0.0)

   #END of declaring and initializing variables####
   #READING FILES 
   filenames=[]
   for k in xrange(firstfile,lastfile):
       filenames.append(file_name(file_prefix,ext,k))
   n=0
   lind=npix_per_q
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
   tdrop_cum=0
   tcalc_cum=0
   I_avg=zeros((1,nfile),float32)
   I_avg2=zeros((1,nfile),float32)
   I_avgs=zeros((nq,nfile),float32)
   tI_avg=zeros((1,nfile),float32)
   mon=zeros((1,nfile),int)
   totsaxs=0*static_data
   
   detector=input_info['detector'].lower()
   Mythread=Thread
   #Mythread=Process
   checkfile=os.path.exists
   n=0
   firstdata=dir+filenames[n]
   f=dataread(firstdata)
   dread(f,n,tot_darks,flat_field,static_corrected)
   goodsize=os.path.getsize(dir+filenames[n])
   nnfile=nfile-1
   stop=0
   if input_info['normalize'].lower()!= 'none':
      print "normalizing to ", input_info['normalize']
   else:
      print "not normalizing"
   while n<nnfile:
       #nc=n+1.
       nc=n+1 
       ccd_imgn=ccd_img
       file=filenames[n+1]
       tempfile=dir+file
       wait=0
       t0=time.time()
       while checkfile(tempfile) is False:
          p.draw()
          sys.stdout.write(50*'\x08')
          sys.stdout.write('waiting for file'+ file+'...')
          sys.stdout.flush()
          t1=time.time()
          wait+=t1-t0
          time.sleep(1)
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
       if ext=='.edf': #cannot do the check for gz files as their size are not to be equal.
          filesize=os.path.getsize(tempfile)
          while filesize!=goodsize:
             sys.stdout.write(50*'\x08')
             sys.stdout.write('file '+ file+'still not ready...')
             sys.stdout.flush()
             time.sleep(2)
             filesize=os.path.getsize(tempfile)
       tmf=dataread(tempfile)
       thrd=Mythread(target=dread,args=([tmf,n+1,tot_darks,flat_field,static_corrected]))
       thcor=Mythread(target=correlator,args=([0,ccd_imgn]))
       mon[0,n]= monitor
    #for plot. TO be faster, I only updated plot each nchannels files.
       if nc%nchannels==0:
          pct=float32(n)/float32(nfile)*100
          sys.stdout.write(50*'\x08')
          sys.stdout.write('read '+str(int(pct))+'% of files'+32*' ')
          sys.stdout.flush()
          if plot!='no':
            ttplot(corf,sr,sl,norm,n+1, I_avg[0,:n+1], I_avg2[0,:n+1],lag) 
            #thplot.join()
            #thplot=Mythread(target=ttplot,args=([corf,sr,sl,norm,n+1, I_avg[0,:n+1], I_avg2[0,:n+1]]))
            #thplot.start()
       thrd.start()
       thcor.start()
       thrd.join()
       thcor.join() 
       n+=1   
   #END OF MAIN LOOP
   #calculate 2 times correlation function
   sys.stdout.write(50*'\x08')
   sys.stdout.flush()
   print "read 100% of files"
   #calculate correlation functions
   if stop==1:
     print nfile, shape(I_avgs)
     tI_avg=tI_avg[:,:nfile] 
     mon=mon[:,:nfile]
     I_avgs=I_avgs[:,:nfile]
     rch=int(ceil(log(nfile/nchannels)/log(2))+1)
     for ir in xrange(rch):
       if ir==0:
         norm[0,:nchannels]=1./arange(nfile-2,nfile-nchannels-2,-1)
       else:
         norm[0,nchannels2*(ir+1):nchannels2*(ir+2)]=1./arange((nfile-1)/(2**ir)-nchannels2-1,(nfile-1)/(2**ir)-nchannels-1,-1)
   indt=int(nchannels+nchannels2*log(nfile/nchannels)/log(2))-2
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
   traces[:,3:]=transpose(I_avgs[:,:])
   savetxt(f,traces)
   f.close()
   del traces 
   static=out_tot+'static.edf'
   totsaxs=totsaxs/nfile-tot_darks
   totsaxs[totsaxs<=0]=0
   saveedf(static,totsaxs)
   del static
   del totsaxs
   del tot_darks 
   print 'correlation functions are saved to ', out_tot+'cf.dat'
   print 'traces are saved to ', out_tot+'trace.dat'
   if input_info['normalize'].lower()!= 'none':
      print "data normalized to ", input_info['normalize']
   else:
      print "data not normalized"
   if input_info['dropletize'].lower()=='yes':
      print   "data dropletized: !!!!CAUTION this is valid only for andor 13 micron and dark subtracted images (adu per photon = 1930 +/- 100, zero photon = 0 +/- 200)"
   #if plot!='no':
   #   p.hold(True)
   #   raw_input('Press enter to close window')
   #   p.close()
   p.hold(True)
   p.close()

   if q_2tcf!='none':
      print "calculating time resolved cf and chi4..."
      if nfile>6000:  #this is for 4 GB RAM PC
         nfile=6000
         n=6000
   if q_2tcf!='none':
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
   if plot!='no':
      print 'elapsed time for plotting', tplot_cum
   print 'elapsed time for reading', tread_cum-tdrop_cum
   if input_info['dropletize'].lower()=='yes':
      print 'elapsed time for dropletizing', tdrop_cum
   print 'elapsed time for correlating', tcalc_cum
   print 'calculations have finished:)'
