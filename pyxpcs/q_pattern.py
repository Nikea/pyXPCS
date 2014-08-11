#!/usr/bin/python
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
from get_edf import *
from read_input import *
import numpy.ma as ma
from numpy import *
import matplotlib.pylab as p
import EdfFile
################################################################################           
########################READING INPUT FILE##################################         
def radians(theta):
   return theta/180.0*pi
def distance(x,y):
   return(sqrt(x**2+y**2))
def theta_grid(x,y):
   tang= y/x
   ysign=y*abs(x)
   xsign=x*abs(y)
   th=arctan(tang)*180/pi
   th[(xsign<0)&(ysign>=0)]=180+th[(xsign<0)&(ysign>=0)]
   th[(ysign<0)&(xsign<0)]=180+th[(ysign<0)&(xsign<0)]
   th[(ysign<0)&(xsign==0)]=270
   th[(xsign>=0)&(ysign<0)]=360+th[(xsign>=0)&(ysign<0)]
   return(th)

def angle(x,dsd):
   return(arctan(x/dsd))

def x_component(alfa_i,alfa_f,delta):
   return(-cos(alfa_f)+cos(alfa_i))

def y_component(delta,alfa_f):
   return(cos(alfa_f)*sin(delta))

def z_component(alfa_i,alfa_f):
   return(sin(alfa_f)+sin(alfa_i))

def qpattern(input_info):
   
   dir= input_info['dir']
   file_prefix=input_info['file_prefix']
   ext = input_info['file_suffix']
   firstfile=int(input_info['n_first_image'])
   out_dir = get_dir(input_info['output directory'])
   out_prefix= get_prefix(input_info['output filename prefix'])
   
   geometry=input_info['geometry'].lower()
   wavelength=float(input_info['wavelength'])
   dsd=float(input_info['detector sample distance'])
   det=input_info['detector']
   print 'detector is =', det
   if det.lower()=='princeton':
      x_pix_size=y_pix_size=float(0.0225)
   elif det.lower()=='andor 13micron':
      x_pix_size=y_pix_size=float(0.013)
   elif det.lower()=='andor 22.5micron': 
      x_pix_size=y_pix_size=float(0.0225)
   elif det.lower()=='medipix':
      x_pix_size=y_pix_size=float(0.055)
   
   if geometry == 'gisaxs':
      #rod_geometry=input_info['rod geometry'].lower()
      rod_geometry='horiz'
      x_ref_beam=float(input_info['x reflected beam'])
      y_ref_beam=float(input_info['y reflected beam'])
      alfa= float(input_info['incidence angle'])
      if rod_geometry=='horiz':
         x_dir_beam=x_ref_beam-(2*dsd*tan(radians(alfa))/x_pix_size)
         y_dir_beam=y_ref_beam
      else:
         y_dir_beam=y_ref_beam-(2*dsd*tan(radians(alfa))/y_pix_size)
         x_dir_beam=x_ref_beam
   else:
      x_dir_beam=float(input_info['x direct beam'])
      y_dir_beam=float(input_info['y direct beam'])
   
   
   firstname=dir+file_name(file_prefix,ext,firstfile)
#This is for the ccd files
   if ext=='.edf':
      f=EdfFile.EdfFile(firstname)
   if ext=='.edf.gz': 
      f=EdfFile.EdfGzipFile(firstname)
   head=f.GetStaticHeader(0)
#      ccd_info=get_header(firstname)
   ncol=int(head['Dim_1'])
   nrows=int(head['Dim_2'])
#  if ext=='.bin':
#     ncol=nrows=256


########### CALCULATING Q PATTERN ##############################
   k=2*pi/wavelength
   
   if (geometry == 'saxs') | (geometry == 'waxs'):
      print 'saxs geometry'
      x_pix=reshape(arange(ncol)-x_dir_beam,(1,-1))
      y_pix=reshape(arange(nrows)-y_dir_beam,(-1,1))
      x_mm=x_pix*x_pix_size
      y_mm=y_pix*y_pix_size
      pix_distance=distance(x_mm,y_mm)
      theta=angle(pix_distance,dsd)
      q_tot = 2*k*sin(theta/2)
      return(q_tot)

   if geometry =='magnetic field':
      x_pix=reshape(arange(ncol)-x_dir_beam,(1,-1))
      y_pix=reshape(arange(nrows)-y_dir_beam,(-1,1))
      theta=theta_grid(x_pix,y_pix)
      return(theta)
   
   if geometry == 'gisaxs':
      print 'gisaxs geometry'
      alfa_i=radians(alfa)
      x_origin=(x_dir_beam+x_ref_beam)/2
      y_origin=(y_dir_beam+y_ref_beam)/2
      x_pix=reshape(arange(ncol)-x_origin,(1,-1))
      y_pix=reshape(arange(nrows)-y_origin,(-1,1))
      x_mm=x_pix*x_pix_size
      y_mm=y_pix*y_pix_size
      if rod_geometry=='horiz':
         alfa_f = angle(x_mm,dsd)
         delta = angle(y_mm,dsd)
      else:
         alfa_f = angle(y_mm,dsd)
         delta = angle(x_mm,dsd)
      q_x = k*x_component(alfa_i,alfa_f,delta)
      qx=zeros((nrows,ncol))
      if rod_geometry=='horiz':
         for i in range(nrows):
             qx[i,:]=q_x
      else:
         for i in range(ncol):
             qx[:,i]=transpose(q_x)
      q_y = k*y_component(delta,alfa_f)
      q_z = resize(k*z_component(alfa_i,alfa_f),(nrows,ncol))
      q_tot=sqrt(q_x**2+q_y**2+q_z**2)
      q_par=sqrt(q_x**2+q_y**2)
      return(q_par,qx,q_y,q_z,q_tot)

