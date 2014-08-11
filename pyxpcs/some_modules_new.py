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
from numpy import *
from get_edf import file_name
from read_input import *
from numpy.ma import masked_array,filled,masked_greater,masked_less
from commands import getoutput
import sys, os, time, EdfFile
import pylab as p
from q_pattern import qpattern
from os.path import isfile

def loadedf(filename,imgn=0):
    if isfile(filename):
        f=EdfFile.EdfFile(filename)
        return f.GetData(imgn)
    else:
        print "file ",filename," does not exist!"
        return 

def saveedf(filename,data,imgn=0):
    try:
        newf=EdfFile.EdfFile(filename)
        newf.WriteImage({},data,imgn)
        print "file is saved to ",filename
        return 
    except:
        print "file is not saved!" 
        return

def headersedf(filename,imgn=0):
    if isfile(filename):
        f=EdfFile.EdfFile(filename)
        return f.GetStaticHeader(imgn)
    else:
        print "file ",filename," does not exist!"
        return 

def headeredf(filename,imgn=0):
    if isfile(filename):
        f=EdfFile.EdfFile(filename)
        return f.GetHeader(imgn)
    else:
        print "file ",filename," does not exist!"
        return


def sum_data(files,detector,flatfield_file,normalize='none'):
   #f=files[0]
   #ext=os.path.splitext(f)[1]
   #if ext=='.gz': 
   #   readfile=EdfFile.EdfGzipFile
   #else:
   #   readfile=EdfFile.EdfFile
   #file=readfile(f)
   #header=file.GetStaticHeader(0)
   header= headersedf(files[0])
   dim1=int(header['Dim_1'])
   dim2=int(header['Dim_2'])
   nfiles=len(files)
   data=zeros((dim2,dim1),dtype=float32)
   mon=1
   for i,f in enumerate(files):
      pct= int(100.0*i/nfiles)
      sys.stdout.write(18*'\x08')
      image=asfarray(loadedf(f),dtype=float32)
      if normalize=='average in ccd':
         mon=average(image)
         image/=mon 
      if normalize=='monitor':
         header=headeredf(f)
         counters=header['counter_pos'].split(' ')
         mon=int(counters[1])
         image/=mon
      data+=image
      sys.stdout.write('read '+str(pct)+'% of files')
      sys.stdout.flush()
   avg_data=data/nfiles/flatfield(detector,flatfield_file)
   sys.stdout.write(18*'\x08')
   sys.stdout.write('read 100% of files')
   sys.stdout.flush()
   return avg_data


def auto_mask(infos,dark_file='default'):
   name= sys.argv[0]
   realname=os.path.realpath(name)
   directory=os.path.dirname(realname)
   out_dir=infos['output directory']
   out_pref=infos['output filename prefix']
   out_tot=out_dir+'/'+out_pref
   staticfile=out_tot+'static.edf'
   image=loadedf(staticfile)
   sx,sy=shape(image)
   tolerance=float32(infos['tolerance'])
   detector=infos['detector'].lower()
   if detector=='medipix':
     if sx>260:
       default_maskf=os.path.join(directory,'mask_medipix2x2.edf')
     else:
       default_maskf=os.path.join(directory,'mask_medipix.edf')
     print default_maskf
     default_mask=loadedf(default_maskf,0)
     genmask=copy(default_mask)
     if tolerance>0:
        print 'masking where dark>', tolerance
        if dark_file=='default':
           dark_file=out_tot+'dark.edf'
        dark=loadedf(dark_file)
        genmask[dark>tolerance]=1
   
   if detector=='princeton':
     default_maskf=os.path.join(directory,'mask_princeton.edf')
     dir=infos['dir']
     file_prefix=infos['file_prefix']
     ext=infos['file_suffix']
     n_file=infos['n_first_image']
     file=file_name(dir+file_prefix,ext,n_file)
     header=headeredf(file)
     fcol=int(header['col_beg'])
     lcol=int(header['col_end'])
     frow=int(header['row_beg'])
     lrow=int(header['row_end'])
     default_mask=loadedf(default_maskf)[frow:lrow+1,fcol:lcol+1]
     genmask=copy(default_mask)
   if 'andor' in detector:
     genmask=0*image
   if 'xbpm' in detector:
     genmask=0*image
   return genmask

def  flatfield(detector,flatfield_file):
     name= sys.argv[0]
     realname=os.path.realpath(name)
     directory=os.path.dirname(realname)
     if detector=='medipix':
        if flatfield_file=='none':
           flat_field=1.0
        else:
           if flatfield_file== '8keV before april 2009':
             file='flatfield_medipix_8keV_thl6590_beforeApril2009.edf'
             flatfile=os.path.join(directory,file)  
           elif flatfield_file== '8keV':
             file='flatfield_medipix_8keV-27April09.edf'
             flatfile=os.path.join(directory,file) 
           elif flatfield_file== '8keV 2x2':
             file='flatfield_medipix2x2.edf'
             flatfile=os.path.join(directory,file)
           elif flatfield_file== '10keV':
             file='flatfield_medipix_10keV-27April09.edf'
             flatfile=os.path.join(directory,file)  
           else:
             flatfile=flatfield_file
           flat_field=asfarray(loadedf(flatfile),dtype=float32)
        print 'flatfield=', flatfield_file
     else:
        flat_field=1.0
     return flat_field

def rad_average(saxs,mask,cx,cy):
    dim1,dim2=shape(saxs)
    [X,Y]=mgrid[1-cy:dim1+1-cy,1-cx:dim2+1-cx]
    q=float32(sqrt(X**2+Y**2))
    q[mask!=0]=0
    q=ravel(q)
    saxs=ravel(saxs)
    qm=xrange(int(q.max()+1))
    qr=range(len(qm))
    for i in qm:
        qr[i]=[]
        
    xlenq=xrange(len(q))
    for i in xlenq:
        qr[int(q[i])].append(i)
    for i in qr:
        saxs[i]=mean(saxs[i])
    return reshape(saxs,(dim1,dim2))

def dropletize(data,adu_phot,thl_phot,adu_zero,thl_zero):
    import numpy as n
    drop_data=n.zeros(n.shape(data),dtype=float32)
    normdata=data/float(adu_phot)
    thl_rel=thl_phot/float(adu_phot)
    lenx,leny=shape(normdata)
    ind1phot=where((data<=adu_phot+thl_phot)&(data>=adu_phot-thl_phot))
    ind0phot=where((data<=adu_zero+thl_zero))
    indshit=where((data>adu_phot+thl_phot))
    drop_data[ind1phot]=1
    drop_data[ind0phot]=0
    drop_data[indshit]=0
    normdata[ind0phot]=0
    normdata[ind1phot]=0
    normdata[indshit]=0
    lost_phot=[]
    for k in arange(9,0,-1):
      down=k/10.
      indx,indy=where((normdata>=down)&(normdata<=1-thl_rel))
      for i in range(len(indx)):
        x=indx[i]
        y=indy[i]
        if (x==0)&(y==0):
           ind_shared=[(x,y),(x+1,y),(x,y+1)]
           shared=array([normdata[x,y],normdata[x+1,y],normdata[x,y+1]])
        elif (x==0)&(y==leny-1):
           ind_shared=[(x,y),(x+1,y),(x,y-1)]
           shared=array([normdata[x,y],normdata[x+1,y],normdata[x,y-1]])
        elif (x==lenx-1)&(y==leny-1):
           ind_shared=[(x,y),(x-1,y),(x,y-1)]
           shared=array([normdata[x,y],normdata[x-1,y],normdata[x,y-1]])
        elif (x==lenx-1)&(y==0):
           ind_shared=[(x,y),(x-1,y),(x,y+1)]
           shared=array([normdata[x,y],normdata[x-1,y],normdata[x,y+1]])
        elif (x==0):
           ind_shared=[(x,y),(x+1,y),(x,y+1),(x,y-1)]
           shared=array([normdata[x,y],normdata[x+1,y],normdata[x,y+1],normdata[x,y-1]])
        elif (x==lenx-1):
           ind_shared=[(x,y),(x-1,y),(x,y+1),(x,y-1)]
           shared=array([normdata[x,y],normdata[x-1,y],normdata[x,y+1],normdata[x,y-1]])
        elif (y==0):
           ind_shared=[(x,y),(x-1,y),(x+1,y),(x,y+1)]
           shared=array([normdata[x,y],normdata[x-1,y],normdata[x+1,y],normdata[x,y+1]])
        elif (y==leny-1):
           ind_shared=[(x,y),(x-1,y),(x+1,y),(x,y-1)]
           shared=array([normdata[x,y],normdata[x-1,y],normdata[x+1,y],normdata[x,y-1]])
        else:
           ind_shared=[(x,y),(x-1,y),(x+1,y),(x,y+1),(x,y-1)]
           shared=array([normdata[x,y],normdata[x-1,y],normdata[x+1,y],normdata[x,y+1],normdata[x,y-1]])
        tot=sum(shared)
        imax=argmax(shared)
        if (tot<1+thl_rel)&(tot>0.25):
          for j in range(len(shared)):
             normdata[ind_shared[j]]=0
          drop_data[ind_shared[imax]]=1
        elif tot>1+thl_rel:
          drop_data[ind_shared[imax]]=1
          shared[imax]=0
          imax=argmax(shared)
          val=normdata[ind_shared[imax]]
          for j in range(len(shared)):
             normdata[ind_shared[j]]=0
          newval=min(val,tot-1)
          normdata[ind_shared[imax]]=newval
        else:
          for j in range(len(shared)):
             normdata[ind_shared[j]]=0
    ind1phot=where((normdata<=1+thl_rel)&(normdata>=0.7))
    ind0phot=where((normdata<=0.1))
    drop_data[ind1phot]=1
    normdata[ind1phot]=0
    normdata[ind0phot]=0
    lost,list=where(normdata!=0)
    return drop_data

def do_average(fileinput,nstart='first',nend='last'):
    nstart=str(nstart)
    nend=str(nend)
    info=get_input(fileinput)
    dir= info['dir']
    prefix=info['file_prefix']
    prefix=dir+prefix
    ext = info['file_suffix']
    #if ext=='.edf.gz':
    #    dataread=EdfFile.EdfGzipFile
    #else:
    #    dataread=EdfFile.EdfFile
    files=[]
    if nstart=='first':
       nstart=int(info['n_first_image'])
    else:
       nstart=int(nstart)
    if nend=='last':
       nend=int(info['n_last_image'])
    elif 'nstart' in nend:
       nend=int(nend.split('+')[-1])+nstart 
    else:
       nend=int(nend)
    for i in range(nstart,nend+1):
        data_file=file_name(prefix,ext,i)
        files.append(data_file)
    if os.path.exists(dir) is False:
        print "data directory doesn't exist, please check it!!!!"
    elif os.path.exists(files[0]) is False:
        print files[0]
        print "data prefix or numbers wrong, please check it!!!!"
    else:
        detector=info['detector']
        flatfield_file=info['flatfield file']
        while os.path.exists(files[-1]) is False:
           print 'waiting for file ', files[-1]
        data=sum_data(files,detector,flatfield_file)
        return data

def time_resolved_static(inputfile, nfile_per_group=100):
    
   input_info=get_input(inputfile)
   firstfile=int(input_info['n_first_image'])
   lastfile=int(input_info['n_last_image'])+1
   nq=int(input_info['number of q'])
   nfile=lastfile-firstfile
   ncols=nfile/nfile_per_group
   nstart=firstfile
   nend=firstfile+nfile_per_group
   avg=do_average(inputfile,nstart,nend)
   int_q=Iq(inputfile,avg)
   nq= shape(int_q)[0]
   int_matrix=zeros((nq,ncols+1))
   int_matrix[:,0:2]=int_q 
   title='#q Ang-1'
   for k in xrange(1,ncols):
      nstart+=nfile_per_group
      nend+=nfile_per_group 
      nend=min(nend,lastfile)
      titleline=' '+str(nstart)+'to'+str(nend)
      title+=titleline
      avg=do_average(inputfile,nstart,nend)
      print nstart, nend
      int_q=Iq(inputfile,avg)
      int_matrix[:,k+1]=int_q[:,1]
   outdir=input_info['output directory']
   outpref=input_info['output filename prefix']
   outfile=outpref+'_trsaxs.dat'
   output=os.path.join(outdir,outfile)
   f=open(output,'w')
   f.write(title)
   savetxt(f,int_matrix)
   f.close() 
   print 'skipped files from', nend, 'to', lastfile
   print 'output in', output


def Iq(input_file,avg):
   info=get_input(input_file)
   qtot=qpattern(info)
   geometry=info['geometry']
   if geometry == 'gisaxs':
      qtot=qtot[1]
   wavelength=float(info['wavelength'])
   distance=float(info['detector sample distance'])
   detector=info['detector']
   if detector == 'princeton' or detector == 'andor 22.5micron':
      pix_size=0.0225
   if detector == 'medipix':
      pix_size=0.055
   if detector == 'andor 13micron' or detector == 'andor':
      pix_size=0.013
   if detector=='xbpm':
      pix_size=0.001
   deltaq=4*pi/wavelength*sin(arctan(2*pix_size/distance)/2)
   mask_file=info['mask file']
   tot=EdfFile.EdfFile(mask_file)
   totmask=tot.GetData(0)+tot.GetData(1)

   q=qtot[totmask==0]
   indq=argsort(q)
   q=q[indq]
   qr=arange(min(q),max(q)+deltaq,deltaq)
   m=avg[totmask==0]
   m=m[indq]
   lqv=len(qr)

   radi=zeros((lqv,2))
   ini=0
   hh,bins=histogram(q,lqv,new=True)
   radi[:,0]=bins[:-1]+deltaq/2
   for i in xrange(lqv):
      radi[i,1]=mean(m[ini:ini+hh[i]])
      ini=ini+hh[i]
   return radi
