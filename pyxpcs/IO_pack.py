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
from time import asctime
from scipy import array
from scipy.optimize import leastsq
import scipy.io.array_import
from math import pi
from numpy import *
import re
from minimize import fitting
import pylab as Plab


#reading input parameters####################################################

def unpack(string,sep=','):
   lis=string.split(sep)
   return lis[0],float(lis[1])


def delcomments(text):
   comment=re.compile('#+.+\n')
   cleaned_text=comment.sub("",text)
   return cleaned_text
################################################################################ 

def get_input(filename='input.txt'):
   f= open(filename,'r')
   alltext=delcomments(f.read())
   allrows=alltext.split('\n')
   f.close
   separator= re.compile('\s*=\s*')
   l=[]
   for line in allrows:
      a=separator.split(line)
      if len(a)==2:
         l.append(a)
   input_par=dict(l)
   return input_par
   
###########################################################   
   
def create_input(file='input.txt'):
   f=open(file,'w')
   f.write('file='+ raw_input('filename?\n')+'\n')
   f.write('xcol='+raw_input('x data in col number...\n')+'\n')
   f.write('ycol='+raw_input('y data in col number...\n')+'\n')
   reply=raw_input('Do you want to normalize the data?(y/N)')
   if reply=='y':
      f.write('normcol='+raw_input('norm data in col number...\n')+'\n')
   else:
      f.write('normcol=none\n')
   reply=raw_input('Do you want to specify an errors column?(y/N)')
   if reply=='y':
      f.write('yerr='+raw_input('errors on data in col number...\n')+'\n')
   else:
      f.write('yerr=none\n')
   reply=raw_input('Do you want to specify a fitting x range?(Y/n)')
   if reply=='n':
      f.write('range=all\n')
      f.write('T1=0\n')
      f.write('T2=0\n')
   else:
      f.write('range='+raw_input('is it a "range in" or a "range out"?(in/out)\n')+'\n')
      f.write('T1='+raw_input('x range lower limit...\n')+'\n')
      f.write('T2='+raw_input('x range upper limit...\n')+'\n')
   print 'Now you should define a fitting function;\n the fitting parameters should be called p0,p1,...;\n if you want to define fixed parameters just call them c0,c1...'
   function= raw_input('specify the fitting function (i.e. c0+p0*x+p1*x**2)\n')
   f.write('f(x)='+ function + '\n')
   par_format=re.compile("p\d+")
   c_format=re.compile("c\d+")
   pars=set(par_format.findall(function))
   consts=set(c_format.findall(function))
   n_p= len(pars)
   n_c=len(consts)
   if n_p>=1:
      for par in pars:
         question='give me the name of the parameter '+par+'\n'
         name=raw_input(question)
         question='give me the value of the parameter '+par+'\n'
         value=raw_input(question)
         f.write(par+'='+name+', '+ value +'\n')
   if n_c>=1:
      for c in consts:
         question='give me the name of the constant '+c+'\n'
         name=raw_input(question)
         question='give me the value of the constant '+c+'\n'
         value=raw_input(question)
         f.write(c+'='+name+', '+ value +'\n')
   f.close()
   print 'The file' , file, 'has been created in this directory. Please check it'
   return file

##############################################################

def process_input(Input_par):  
   npar_max=100 
   filename=Input_par['file']
   t1=float(Input_par['T1'])
   t2=float(Input_par['T2'])
   xcol=int(Input_par['xcol'])-1
   ycol=int(Input_par['ycol'])-1
   normcol=Input_par['normcol']
   yerr=Input_par['yerr']
   range_par=(Input_par['range'])
   func=(Input_par['f(x)'])
   par_0 = []
   name_par=[]
   name_const=[]
   const_0=[]
   for i in range(npar_max):
      kconst='c'+str(i)
      kpar='p'+str(i)
      par=Input_par.get(kpar, 'none')
      const=Input_par.get(kconst, 'none')
      if (const!='none'):
         name_c,c=unpack(const)
         name_const.append(name_c)
         const_0.append(c)   
      if (par != 'none'):
         name_p,p=unpack(par)
         name_par.append(name_p)
         par_0.append(p)
   return filename,t1,t2,range_par,func,name_const,const_0,name_par,par_0,xcol,ycol,normcol,yerr

def read_data(file,xcol,ycol,normcol,yerr='none'):
   f = open(file,'r')
   text= delcomments(f.read())
   f.close()
   f = open('/tmp/data.dat','w')
   f.write(text)
   f.close()
   data = scipy.io.array_import.read_array('/tmp/data.dat')
   x = data[:,xcol]
   y = data[:,ycol]
   if yerr!='none':
      err=data[:,yerr]
   else:
      err=y*0+1.0
   if normcol!='none':
      ncol=int(normcol)-1
      norm = data[:,ncol]
      y=y/norm
   return(x,y,err)

def fit_region(x,y,x1,x2,range_par,err='none'):
   if err=='none':
      err=y*0+1.0
   xlow=[]
   ylow=[]
   xhigh=[]
   yhigh=[]
   errlow=[]
   errhigh=[]
   if range_par=='all':
      return(x,y,err)
   if range_par=='out':
      for i  in range(len(x)):
         if (x[i]<x1):
            xlow.append(x[i])
            ylow.append(y[i])
            errlow.append(err[i])
         if (x[i]>x2):
            xhigh.append(x[i])
            yhigh.append(y[i])
            errhigh.append(err[i])
   if range_par=='auto':
      yend=y[0]/4
      print yend
      for i  in range(len(y)):
         if (y[i]>yend):
            xlow.append(x[i])
            ylow.append(y[i])
            errlow.append(err[i])
   if range_par=='in':
      for i  in range(len(x)):
         if ((x[i]>x1) and (x[i]<x2)):
            xlow.append(x[i])
            ylow.append(y[i])
            errlow.append(err[i])
   xnew=array(xlow+xhigh)
   ynew=array(ylow+yhigh)
   errnew=array(errlow+errhigh)
   return(xnew,ynew,errnew)

def find_baseline(x,y,xstart,xend):
    not_used,ybaselist,nn=fit_region(x,y,xstart,xend,'in')
    y_baseline=mean(ybaselist)
    return(y_baseline)

def find_contrast(x,y):
    f='p0*exp(-p1*x)+p2'
    p0=[y[0],(2/y[0]),y[-1]]
    c0=[]
    print p0
    not_used,pars,nn=fitting(x,y,f,p0,c0)
    y_contrast=pars[0]
    y_range_end=1.0/pars[1]
    return y_contrast,y_range_end

def arraytostring(array,sep= ' '):
   list_tmp=[]
   if type(array) is not list:
      lista = array.tolist()
   else:
      lista = array   
   for l in lista:
      list_tmp.append(str(l))
   return  sep.join(list_tmp)

def write_par_out(names,par,t1,t2,filename,func,const,const_names,xbase1='none',xbase2='none',fileno='none',fileout='params.out',multi='off',qval='none',file_input='input_fit.txt'):
   info=get_input(file_input)
   xcol=info['xcol']+' '
   ycol=info['ycol']+' '
   ynorm=info['normcol']+' '
   yerr=info['yerr']+' '

   f=open(fileout,'a')
   sep=' '
   f.write('#'+asctime()+'\n')
   f.write('#'+70*'-'+'\n')
   f.write('#fitted file= '+ filename +'\n')
   f.write('#fitting function= '+ func + '\n')
   f.write('#fitting range= ' + str(t1) + ':' + str(t2) + '\n')
   f.write('#baseline range= ' +str(xbase1)+':' +str(xbase2) + '\n')
   f.write('#xcol='+xcol+'\n')
   f.write('#ycol='+ycol+'\n')
   f.write('#ynorm='+ynorm+'\n')
   f.write('#yerr='+yerr+'\n')
   if const != []:
      f.write('#parameters kept fixed:\n')
      f.write('#'+sep.join(const_names)+'\n')
      if len(const)>1:
         f.write('#'+arraytostring(const)+'\n')
      else:
         f.write('#'+str(const)+'\n')
   if multi=='on':
      f.write('# ycol '+sep.join(names)+'\n')
      outpar=zeros((1,len(par)+1))
      outpar[0,0]=float(qval)
      outpar[0,1:]=par[:]
      Plab.save(f,outpar)
   else:
      f.write('#'+sep.join(names)+'\n')
      if len(par)>1:
         f.write(arraytostring(par)+'\n')
      else:
         f.write(str(par)+'\n')
      f.write(70*'*'+'\n')
   f.close()
	
def write_multi_par_out(check,names,par,t1,t2,filename,func,const,const_names,xbase1='none', xbase2='none', fileno='none',fileout='params.out',qval='none',file_input='input_fit.txt'):
   multi = 'on'
   if check==0:
      write_par_out(names,par,t1,t2,filename,func,const,const_names,xbase1,xbase2,fileno,fileout,multi,qval)
   else:
      f=open(fileout,'a')
      outpar=zeros((1,len(par)+1))
      outpar[0,0]=float(qval)
      outpar[0,1:]=par[:]
      Plab.save(f,outpar)
      f.close()




def q(x,lam,dsd,ai):
    ai=pi/180*ai
    xoffset=.73
    x=x-xoffset
    xspec=dsd*tan(ai)
    xtot=xspec+x
    af=arctan(xtot/dsd)
    q=2*pi/lam*(cos(ai)-cos(af))
    return q

def q_saxs(x,lam,dsd):
    theta=arctan(abs(x/dsd))
    q= 4*pi/lam*sin(theta/2)
    return q

def create_name(scan,filename):
    tot_name=filename.split('/')
    name=tot_name.pop()
    name_parts=name.split('_')
    name_parts[1]=str(scan).zfill(2)
#    name_parts[2]=str(scan).zfill(2)
#    name_parts[3]=str(scan)
    file='_'.join(name_parts)
    tot_name.append(file)      
    totfile='/'.join(tot_name)
    return totfile                                                                          



