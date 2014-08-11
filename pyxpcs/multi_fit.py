#!/usr/bin/env python
# Licensed as BSD by Yuriy Chushkin of the ESRF on 2014-08-06
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
import sys
from time import sleep
from IO_pack import *
from minimize import fitting
from array import *
#from scipy import *
from scipy.optimize import leastsq
import pylab as Plab
from commands import getoutput
from Numeric import argmin,argmax
import os.path


#look for input file#########################################################

def multifit(lastcol,outdir,outpref,inputfile='input_fit.txt',doplot='yes'):
   ndataset=int(lastcol)
   if os.path.exists(inputfile) is False:
      reply=raw_input('I need an input file, do you want me to create it?(Y/n)')
      print reply
      if reply=='n':
         exit()
      else:
         print 'creating an input file'
         inputfile= create_input(inputfile)
         f=open(inputfile,'r')
         text=f.read()
         print text
         test = raw_input('Is it ok?(Y/n)')
         if test == 'n':
           print 'Please correct it and launch the program again'
           exit()
#reading input parameters####################################################
   Input_par=get_input(inputfile)
   pars = process_input(Input_par)
   filename=pars[0]
   t1=float(pars[1])
   t2=float(pars[2])
   range_par=pars[3]
   func=pars[4]
   name_const=pars[5]
   const_0=pars[6]
   name_par=pars[7]
   par_0=pars[8]
   xcol=pars[9]
   ycol=pars[10]
   normcol=pars[11]
   #yerr=pars[12]
#input parameters read####################################################
   g=open(filename,'r')
   title=g.readline()
   g.close()
   qs=title.split(' ')
   if doplot=='yes':
      Plab.ion()
      Plab.figure(1)
      axdata=Plab.axes()
      axdata.set_xlabel('t [sec]')
      axdata.set_ylabel('g^2(q,t)')
      ldata1,=axdata.semilogx((1,),(1,),'ko',label='all range')
      axdata.hold(True)
      ldata2,=axdata.semilogx((1,),(1,),'r^',label='fitting range')
      ldata3,=axdata.semilogx((1,),(1,),'k-',label='fit')
      axdata.legend(loc='lower left')
      Plab.draw()
      npars=len(name_par)
      parplot=zeros((ndataset-ycol,npars),dtype=float32)
      n=tuple(range(1,npars+1))
      Plab.figure(2)
      ncols=(1+npars)/2
      nrows=npars/ncols+npars%ncols
      ax=range(npars)
      lpars=range(npars)
      for k in range(npars):
          s=str(ncols)+str(nrows)+str(k+1)
          ax[k]=Plab.subplot(s)
          ax[k].set_xlabel('q [1/Ang]')
          ax[k].set_ylabel(name_par[k])
          ax[k].set_title(name_par[k])
          lpars[k],=ax[k].plot((1,),(1,),'ro-')
      Plab.draw()
      raw_input('Adjust positioning and size of figures, then press RETURN...')
   
   for i in range(ycol,ndataset):
     check=i-ycol
     print 'reading file ', filename, ' ...', 'col no. ', i+1
     x,y,not_used=read_data(filename,xcol,i,normcol)
     print 'read'
     if range_par=='in':
        print 'including data in the range ', t1, ':', t2
     if range_par=='out':
        print 'excluding data in the range ', t1, ':', t2
     if range_par=='all':
        t1=Plab.min(x)
        t2=Plab.max(x)
        print 'using all x-range to fit:[',t1,'-',t2,']'
     xfit,yfit,not_used=fit_region(x,y,t1,t2,range_par)
     y_out,p,f= fitting(xfit,yfit,func,par_0,const_0)
#writing results#################################################
     file_par_out=os.path.join(outdir,outpref+'_fitpar.dat')
     file_data_out=os.path.join(outdir,outpref+'_fitcol'+str(i+1)+'.dat')
     write_multi_par_out(check,name_par,p,t1,t2,filename,func,const_0,name_const,fileout=file_par_out,qval=qs[i+1],file_input=inputfile)
     ytheo=eval(f)
     mat=zeros((len(x),3),dtype=float32)
     mat[:,0]=x
     mat[:,1]=y
     mat[:,2]=ytheo
     fi=open(file_data_out,'w')
     fi.write('# x y fit')
     Plab.save(fi,mat)
     fi.close()
     print 'output written on files ', file_par_out,' and ', file_data_out
#some plots#####################################################
     if doplot=='yes':
       Plab.figure(1)
       ldata1.set_data(x,y)
       ldata2.set_data(xfit,yfit)
       ldata3.set_data(x,ytheo)
       axdata.set_xlim(Plab.min(x),Plab.max(x))
       axdata.set_ylim(Plab.min(y),Plab.max(y))
       Plab.draw()
       q=qs[2:i+2]
       parplot[i-1,:]=p
       q=Plab.transpose(q)
       Plab.figure(2)
       for k in range(npars):
         lpars[k].set_data(q,parplot[:i,k])
         xmin=float(q[0])
         xmax=float(q[-1])
         ax[k].set_xlim(0.9*xmin,1.1*xmax)
         ax[k].set_ylim(0.9*Plab.min(parplot[:i,k]),1.1*Plab.max(parplot[:i,k]))
       Plab.draw()
   if doplot=='yes':
      raw_input( "Press a RETURN to close figures...")
      Plab.close('all')
