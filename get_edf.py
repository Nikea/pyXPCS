#!/usr/bin/python
from numpy import *
from struct import unpack
from string import join,zfill
from one_space import one_space
import re, os.path
from time import sleep
from commands import getoutput
from read_input import get_input

################################################################################           
def file_name(file_prefix,ext,number):
   number=int(number)
   if number<10000:
      n=str(number).zfill(4)
   else:
      n=str(number)
   filename=file_prefix+n+ext
   return filename
##############################################################################

def byteunits(n,typ):
   """ it simply convert dimensions from pixels to bytes"""
   if typ=='Int16':
      byteperpixel=2
   else:
      byteperpixel=4
   n_byte= byteperpixel*n
   return n_byte
##############################################################################

def get_header(file):
   """open the edf file to extract the header and pass it to get_header_f"""
#   filetest=getoutput("ls "+ file)
   filetest=os.path.exists(file)
   while filetest is False:
      print 'waiting for file ', file.split('/')[-1], ' ...'
      sleep(2)
#      filetest=getoutput("ls "+ file)
      filetest=os.path.exists(file)
   f = open(file,'rb')
   header = f.read(1024)
   f.close()
   return get_header_f(header)

##############################################################################

def get_header_f(string):
   """Reads the header of the edf file and extract the important parameters into a dictionary"""
   p= re.compile('\s*=\s*')
   sep=re.compile('\s*;\n')
   l=[]
#   for line in string.split(' ;\n'):
   for line in sep.split(string):
      a=p.split(line)
      if len(a)==2: # to skip the lines that cannot be splitted (i.e. the first one)
         l.append(a)
   params=dict(l)
#   labels=params['counter_mne'].split()
#   counters=params['counter_pos'].split()
#   for i,el in enumerate(labels): # this is to split the informations contained in counter_pos, i.e mon, ccdtavg...)
#      l.append([el,counters[i]])
#   params=dict(l)
#   del params['counter_mne']
#   del params['counter_pos']
   return params
##############################################################################
def get_roi(ccd,roi,ncol,nrows,typ,f1,f2):
   roi=roi.split(',')
   if roi[2]=='noxpixels':
      roi[2]=ncol
   if roi[3]=='noypixels':
      roi[3]=nrows
   cs=int(roi[0])-1  # ccd indexes start from 1, while python start from 0!!!!
   ce=int(roi[2])
   csbyte=byteunits(cs,typ)
   cebyte=byteunits(ce,typ)
   ncolbyte=byteunits(ncol,typ)
   rs=int(roi[1])-1
   re=int(roi[3])
   newnrows=re-rs
   newncol=ce-cs
   newdim=newncol*newnrows
   slice= []
   for i in arange(rs,re,1):
      start=i*ncolbyte+csbyte
      end=i*ncolbyte+cebyte
      slice.append(ccd[start:end])
   rslice = join(slice,'')
   format=f1+newdim*f2
   c=array(unpack(format,rslice))
   ccdimage=reshape(c,(newnrows,newncol))
   return ccdimage 
##############################################################################
def get_ccd(file,roi='none',avgt='none'):
   infos=get_input() 
   filetest=os.path.exists(file)
   while filetest is False:
      print 'waiting for file ', file.split('/')[-1], ' ...'
      sleep(2)
      filetest=os.path.exists(file)
   f = open(file,'r')
   header = f.read(1024)
   ccd=f.read()
   f.close()

   param = get_header_f(header)
   byte_order= param['ByteOrder']
   data_type= param['DataType']
   ncol=int(param['Dim_1']) #in pixel units
   nrows=int(param['Dim_2']) # in pixel units
   dim=ncol*nrows
#   I_mon=int(param['mon'])
   I_mon=1
   if avgt=='none':
#   t=float(param['sec']) # for old files
      #t=float(param['ccdtavg']) # for new files
      detector=infos['detector'].lower()
      if detector=='medipix': 
         t=float(param['time_of_frame']) # for new files
      if (detector=='princeton' or detector=='andor'): 
         t=float(param['time_of_day']) # for new files
   else:
      t=float(avgt) # for the medipix we have to give the time for the moment
   if byte_order=='HighByteFirst':
      f1=">"
   else:
      f1="<"
   if data_type=='UnsignedShort':
      f2="H"
      typ="Int16"
   else:
      f2="L"
      typ="Int32"
   format=f1+dim*f2
   if roi=='none':
      c= array(unpack(format, ccd))
      ccdimage=reshape(c,(nrows,ncol))
   else:
        ccdimage=get_roi(ccd,roi,ncol,nrows,typ,f1,f2)
   result= [ccdimage,I_mon,t]
   return result

def get_medipix(file,roi='none'):
   f = open(file,'r')
   if roi=='none':
      ccd=f.read()
      f.close()
      dim=256*256
      format='<'+dim*'H'
      typ='Int16'
      c= array(unpack(format, ccd))
      ccdimage=reshape(c,(256,256))
      result=ccdimage
   else:
      print "not yet implemented"
      result='none'
   return result
