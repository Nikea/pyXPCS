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

from get_edf import file_name
import os.path, sys
from numpy import float32, average, array,asfarray,mean,where
from time import time,sleep

def read_image(f,input_info,flat_field,wtotmask,tot_darks,indices,static_corrected,totsaxs='none'):

    tread=time()
    tdrop=0
    detector=input_info['detector'].lower()
    tolerance=input_info['tolerance']
    dropletize=input_info['dropletize'].lower()
    normalize=input_info['normalize'].lower()
    ccd_img=asfarray(f.GetData(0),dtype=float32)
    if detector=='medipix':
        ccd_img/=flat_field
        if totsaxs!='none':
          totsaxs+=ccd_img
        monitor=mean(ccd_img[wtotmask])
    else:
        if totsaxs!='none':
          totsaxs+=ccd_img
        ccd_img-=tot_darks
        if tolerance>=0:
           ccd_img[ccd_img<tolerance]=0
        header=f.GetHeader(0)
        counters=header['counter_pos'].split(' ')
        monitor=int(counters[1])
    if dropletize== 'yes':
       tdrop=time()
       Onephot_adu=float(input_info['1 Photon ADU'])
       Onephot_sigma=float(input_info['1 Photon Sigma'])
       Zerophot_adu=float(input_info['0 Photon ADU'])
       Zerophot_sigma=float(input_info['0 Photon Sigma'])
       ccd_img=dropletize(ccd_img,Onephot_adu,Onephot_sigma,Zerophot_adu,Zerophot_sigma)
       tdrop=time()-tdrop
    if normalize=='monitor':
        ccd_img/=monitor
    if normalize=='average in ccd':
        ccd_img/=mean(ccd_img[wtotmask])
    
    if totsaxs=='none': #meaning that it has been called from chi4_chiara
       ccd_img[indices]*=static_corrected[indices]###Should help for the baseline!!!
       tread=time()-tread 
       return(ccd_img,tread,tdrop)
    else: #meaning that it has been called from correlator
       ccd_img*=static_corrected  ###Should help for the baseline!!!
       tread=time()-tread 
       return(ccd_img,monitor,tread,tdrop,totsaxs)

def find_lagt(avgt,input_info,dataread):
   firstfile=int(input_info['n_first_image'])
   dir= input_info['dir']   
   file_prefix=input_info['file_prefix']
   ext = input_info['file_suffix']
   detector=input_info['detector']
   if avgt=='auto':
      lagt=[]
      lagt1=0
      for k in xrange(firstfile+40,firstfile+100):
        filename=file_name(dir+file_prefix,ext,k)
        while os.path.exists(filename) is False:
          sys.stdout.write(50*'\x08')
          sys.stdout.write('file '+filename+'still not ready')
          sys.stdout.flush()
          sleep(10)
        f=dataread(filename)
        params=f.GetHeader(0)
        if detector=='medipix':
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
   else:
      dt=float32(float(input_info['lag time']))
   return(dt) 
