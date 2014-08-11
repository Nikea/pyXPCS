#!/usr/bin/python
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
import re
################################################################################ 
def delcomments(text):
   comment=re.compile('#+.+\n')
   cleaned_text=comment.sub("\n",text)
   return cleaned_text.split('\n')
################################################################################ 
def get_input(filename='input.txt'):
   f= open(filename,'r')
   allrows=delcomments(f.read())
   f.close
   separator= re.compile('\s*=\s*')
   l=[]
   for line in allrows:
      line=line.strip()
      a=separator.split(line)
      if len(a)==2:
         l.append(a)
   input_par=dict(l)
   return input_par
   
def get_dir(dirname):
   dir=dirname.strip()
   if dir.lower() == '':
      dir='./'
   else:
      if dir[-1]!='/':   
         dir=dir+'/'
   return dir

def get_prefix(name):
   name=name.strip()
   if name.lower() == 'none':
      name=''
   #else:
   #   if name[-1]!='_':   
   # #     name=name+'_'
   return name

def get_suffix(name):
   name=name.strip()
   if name.lower() == 'none':
      name=''
   else:
      if name[0]!='_':   
         name='_'+name
   return name

def create_input():
    print 'creating input file....'
    f=open('input.txt','w')
    datadir = raw_input('give the directory where data are:')
    f.write('dir = '+datadir+'\n')
    darkdir = raw_input("give the directory where darks are (type nothing if it is the same of data, or if you don't have darks:")
    if darkdir=='':
       darkdir ='none'
    f.write('dark dir = '+darkdir+'\n')
    file_prefix=raw_input('prefix of files (i.e. bla_bla_):')
    f.write('file_prefix = '+file_prefix+'\n')
    file_suffix=raw_input('suffix of files (default .edf):')
    if file_suffix=='':
       file_suffix='.edf'
    f.write('file_suffix = '+file_suffix+'\n')
    firstfile=raw_input('number of first data file:')
    f.write('n_first_image = '+firstfile+'\n')
    lastfile=raw_input('number of last data file:')
    f.write('n_last_image = '+lastfile+'\n')
    firstdark=raw_input("number of first dark file (type nothing if you don't have darks):")
    if firstdark=='':
       firstdark='none'
    f.write('n_first_dark = '+firstdark+'\n')
    if firstdark.lower()!='none':
       lastdark=raw_input('number of last dark file:')
       dark_prefix=raw_input('prefix of darks (type nothing if it is the same as files):')
       if dark_prefix=='':
          dark_prefix='none'
       f.write('dark_prefix = '+dark_prefix+'\n')
    else:
       lastdark='none'
       dark_prefix='none'
    f.write('n_last_dark = '+lastdark + '\n')
    f.write('dark_prefix = '+dark_prefix+'\n')
    outdir = raw_input("give the directory where to save output (type nothing if here):")
    if outdir=='':
       outdir='./'
    f.write('output directory = '+outdir+'\n')
    outfile=raw_input('prefix of output files (i.e. cf-sample1_):')
    f.write('output filename prefix = '+outfile+'\n')
    detector=raw_input('which detector are you using? (medipix or princeton):')
    f.write('detector  = '+ detector + '\n')
    wavelength=raw_input('wavelength? (in angstrom):')
    f.write('wavelength  = '+ wavelength + '\n')
    dsd=raw_input('detector sample distance? (in mm):')
    f.write('detector sample distance = '+ dsd + '\n')
    lag_time = raw_input("time between images? (if you type 'none' I'll take it from ccd images ==> coming soon...not yet implemented):")
    f.write('lag time = '+ lag_time + '\n')
    geometry= raw_input('gisaxs or saxs?')
    f.write('geometry  = '+ geometry + '\n')
    if geometry.lower()=='gisaxs':
       rod_geom=raw_input('is the roi horizontal or vertical? h/V')
       if rod_geom.lower()=='h':
          rod_geom='horiz'
       else:
          rod_geom='vertical'
       f.write('rod geometry = '+ rod_geom + '\n')
       incident_angle=raw_input('incident angle in degrees')
       f.write('incident angle = '+ incident_angle + '\n')
       xbeam = raw_input('x reflected beam?')
       f.write('x reflected beam = '+ xbeam + '\n')
       ybeam = raw_input('y reflected beam?')
       f.write('y reflected beam = '+ ybeam + '\n')
    if geometry.lower()=='saxs':
       xbeam = raw_input('x direct beam?:')
       f.write('x direct beam = '+ xbeam + '\n')
       ybeam = raw_input('y direct beam?:')
       f.write('y direct beam = '+ ybeam + '\n')
    f.write('region of interest = none \n')
#    f.write('rois to mask = none \n')
    f.write('tolerance = -1 \n')
    firstq= raw_input ("first q (angstrom-1) (put 0 if you don't know):")
    f.write('first q = '+ firstq + '\n')
    deltaq= raw_input ('delta q (angstrom-1):')
    f.write('delta q = '+deltaq + '\n')
    stepq= raw_input ('step q (angstrom-1):')
    f.write('step q = '+ stepq + '\n')
    nq = raw_input ('how many qs?:')
    f.write('number of q = '+ nq + '\n')
    f.close()
    print '...done'
