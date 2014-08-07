/****************************************************************************
** ui.h extension file, included from the uic-generated form implementation.
**
** If you want to add, delete, or rename functions or slots, use
** Qt Designer to update this file, preserving your code.
**
** You should not define a constructor or destructor in this file.
** Instead, write your code in functions called init() and destroy().
** These will automatically be called by the form's constructor and
** destructor.
*****************************************************************************/


void Form1::loadinput()
{
   #oadinput(window=1)
   from read_input import get_input
   from commands import getoutput
   if window == 1:
      from qt import QFileDialog 
      PathLineEdit=self.lineEdit_input.text().ascii()
      filename = QFileDialog.getOpenFileName(PathLineEdit,('*.txt'))
      if filename:
         self.lineEdit_input.setText(filename)
      else: 
         filename=self.lineEdit_input.text().ascii()
   else:
      filename=self.lineEdit_input.text().ascii()
   input_info=get_input(filename)
   self.lineEditDataDir.setText(input_info['dir'])
   self.lineEditDataPrefix.setText(input_info['file_prefix'])
   self.lineEditDataSuff.setText(input_info['file_suffix'])
   self.lineEditDataStart.setText(input_info['n_first_image'])
   self.lineEditDataEnd.setText(input_info['n_last_image'])
   if input_info['n_first_dark'].lower()=='none':
      self.checkBox_darks.setChecked(0)
   else:
      self.checkBox_darks.setChecked(1)
      self.lineEditDarkDir.setText(input_info['dark dir'])
      self.lineEditDarkPrefix.setText(input_info['dark_prefix'])
      self.lineEditDarkStart.setText(input_info['n_first_dark'])
      self.lineEditDarkEnd.setText(input_info['n_last_dark'])
   self.lineEdit12.setText(input_info['output directory'])
   self.lineEdit13.setText(input_info['output filename prefix'])
   if input_info['detector'].lower()=='medipix':
      self.comboBox_detector.setCurrentItem(0)
      self.checkBox_flatfield.setEnabled(1)
      try:
         flat_file=input_info['flatfield file'].lower()
         if flat_file == 'none' :
            self.checkBox_flatfield.setChecked(0)
            self.comboBox_flatfield.setEnabled(0)
         else:
            self.checkBox_flatfield.setChecked(1)
            self.comboBox_flatfield.setEnabled(1) 
            if flat_file == '8kev' :
              self.comboBox_flatfield.setCurrentItem(0)
            elif flat_file == '8kev before april 2009' :
              self.comboBox_flatfield.setCurrentItem(1)
            elif flat_file == '10kev' :
              self.comboBox_flatfield.setCurrentItem(2)
            else:
              self.comboBox_flatfield.setCurrentItem(3)
              self.lineEdit_other.setText(input_info['flatfield file'])
      except:
            self.checkBox_flatfield.setChecked(1)
            self.comboBox_flatfield.setCurrentItem(1)
   else:
      self.checkBox_flatfield.setChecked(0)
      self.checkBox_flatfield.setEnabled(0)
      self.comboBox_flatfield.setEnabled(0)
   if input_info['detector'].lower()=='princeton':
      self.comboBox_detector.setCurrentItem(1)
   if input_info['detector'].lower()=='andor 22.5micron':
      self.comboBox_detector.setCurrentItem(2)
   if input_info['detector'].lower()== 'andor 13micron': 
      self.comboBox_detector.setCurrentItem(3)
   if input_info['detector'].lower()=='andor': #andor alone is for old input files
      self.comboBox_detector.setCurrentItem(3)
   self.SetNormalizeList()
   self.lineEdit_dsd.setText(input_info['detector sample distance'])
   self.lineEdit_lambda.setText(input_info['wavelength'])
   self.lineEdit17.setText(input_info['lag time'])
   if input_info['geometry']=='saxs':
      self.radioButton3.setChecked(1)
      self.lineEdit18.setText(input_info['x direct beam'])
      self.lineEdit19.setText(input_info['y direct beam'])
   if input_info['geometry']=='gisaxs':
      self.radioButton4.setChecked(1)
      self.lineEdit18.setText(input_info['x reflected beam'])
      self.lineEdit19.setText(input_info['y reflected beam'])
      self.lineEdit20.setText(input_info['incidence angle'])
   if input_info['geometry']=='waxs':
      self.radioButton5.setChecked(1)
      self.lineEdit18.setText(input_info['x direct beam'])
      self.lineEdit19.setText(input_info['y direct beam'])
      self.checkBox_droplet.setEnabled(1)
      try:
        if input_info['dropletize'].lower()=='yes':
          self.checkBox_droplet.setChecked(1)
          self.lineEdit_0PhotADU.setText(input_info['0 Photon ADU'])
          self.lineEdit_0PhotSigma.setText(input_info['0 Photon Sigma'])
          self.lineEdit_1PhotADU.setText(input_info['1 Photon ADU'])
          self.lineEdit_1PhotSigma.setText(input_info['1 Photon Sigma'])
        else:
          self.checkBox_droplet.setChecked(0)
      except:
        self.checkBox_droplet.setChecked(0)
   self.lineEdit_firstq.setText(input_info['first q'])
   self.lineEdit27.setText(input_info['delta q'])
   self.lineEdit28.setText(input_info['step q'])
   self.lineEdit_nq.setText(input_info['number of q'])
   self.lineEdit_qTRC.setText(input_info['q for TRC'])
   self.lineEdit_plotq_TRcf.setText(input_info['q for TRC'])
   self.q_lineEdit_chi4.setText(input_info['q for TRC'])
   self.lineEdit_tolerance.setText(input_info['tolerance'])
   self.lineEdit_tolerance_2.setText(input_info['tolerance'])
   try:
      self.lineEdit_mask.setText(input_info['mask file'])
      self.lineEdit_dark.setText(input_info['dark file'])
   except:
      self.lineEdit_mask.setText(self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'mask.edf')
      self.lineEdit_dark.setText(self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'dark.edf')
   try:
      normalize=input_info['normalize'].lower()
      if normalize== 'none':
         self.comboBox_normalize.setCurrentItem(0)  
      if normalize== 'average in ccd':
         self.comboBox_normalize.setCurrentItem(1)
      if normalize== 'monitor':
         self.comboBox_normalize.setCurrentItem(2)
   except:
      self.comboBox_normalize.setCurrentItem(0)  
   self.update_text()
   outdir=input_info['output directory']
   print outdir
   if os.path.exists(outdir) is False:
      com='mkdir '+outdir
      print getoutput(com)
      if os.path.exists(outdir) is False:
         print 'cannot create output directory, please check if there is some error'
      else:
         print 'created output directory:', outdir
}


void Form1::makeinput()
{  
   from commands import getoutput
   import os.path
   filename=self.lineEdit_input.text().ascii()
   self.lineEdit_input.setText(os.path.realpath(filename))
   f=open(filename,'w')
   dir=os.path.realpath(self.lineEditDataDir.text().ascii())
   if dir[-1]!='/':
      dir=dir+'/'
   f.write('dir = '+ dir+'\n')
   f_prefix=self.lineEditDataPrefix.text().ascii()
   f.write('file_prefix = '+ f_prefix+'\n')
   f_suffix=self.lineEditDataSuff.text().ascii()
   f.write('file_suffix = '+ f_suffix+'\n')
   n_image=self.lineEditDataStart.text().ascii()
   f.write('n_first_image = '+ n_image+'\n')
   n_image=self.lineEditDataEnd.text().ascii()
   f.write('n_last_image = '+ n_image+'\n')
   if self.checkBox_darks.isChecked():
      dark_dir=self.lineEditDarkDir.text().ascii()
      if dark_dir=='':
         dark_dir=dir
      dark_dir=os.path.realpath(dark_dir)
      if dark_dir[-1]!='/':
         dark_dir=dark_dir+'/'
      f.write('dark dir = ' +dark_dir +'\n')
      dark_prefix=self.lineEditDarkPrefix.text().ascii()
      f.write('dark_prefix = '+ dark_prefix +'\n')
      dark1=self.lineEditDarkStart.text().ascii()
      f.write('n_first_dark = '+ dark1 + '\n')
      dark2=self.lineEditDarkEnd.text().ascii()
      f.write('n_last_dark = ' + dark2 + '\n')
   else:
      f.write('dark dir = none \n')
      f.write('dark_prefix = none \n')
      f.write('n_first_dark = none \n')
      f.write('n_last_dark = none \n')
   
   outdir=self.lineEdit12.text().ascii()
   if (outdir=='' or outdir=='none'):
      outdir='./'
   else:
      if outdir[-1]!='/':
         outdir=outdir+'/'
   if os.path.exists(outdir) is False:
      com='mkdir '+outdir
      print getoutput(com)
      if os.path.exists(outdir) is False:
         print 'cannot create output directory, please check if there is some error'
      else:
         print 'created output directory:', outdir
         outdir=os.path.realpath(outdir)
   f.write('output directory = '+ outdir + '\n')
   outprefix=self.lineEdit13.text().ascii()
   f.write('output filename prefix = '+ outprefix + '\n')
   mask_file=self.lineEdit_mask.text().ascii()
   if mask_file=='default':
      mask_file=outdir+outprefix+'mask.edf'
   self.lineEdit_mask.setText(mask_file)
   f.write('mask file = '+ mask_file + '\n')
   dark_file=self.lineEdit_dark.text().ascii()
   if dark_file=='default':
      dark_file=outdir+outprefix+'dark.edf'
   self.lineEdit_dark.setText(dark_file)
   f.write('dark file = '+ dark_file + '\n')
   detector=self.comboBox_detector.currentText().ascii().lower()
   f.write('detector = ' +detector+ '\n')
   if self.checkBox_flatfield.isChecked():
      flatfield_file=self.comboBox_flatfield.currentText().ascii()
      if flatfield_file=='other':
         flatfield_file=self.lineEdit_other.text().ascii()
   else:
      flatfield_file='none'
   f.write('flatfield file = '+flatfield_file+'\n')
   dsd=self.lineEdit_dsd.text().ascii()
   f.write('detector sample distance = '+dsd+'\n')
   lam=self.lineEdit_lambda.text().ascii()
   f.write('wavelength = '+lam+'\n')
   dt=self.lineEdit17.text().ascii()
   if dt=='':
      dt='auto'
   f.write('lag time = '+dt+'\n')
   if self.radioButton3.isChecked():
      f.write('geometry = saxs \n')
      xbeam=self.lineEdit18.text().ascii()
      ybeam=self.lineEdit19.text().ascii()
      f.write('x direct beam = ' +xbeam+'\n')
      f.write('y direct beam = ' +ybeam+'\n')
   if self.radioButton4.isChecked():
      f.write('geometry = gisaxs \n')
      xbeam=self.lineEdit18.text().ascii()
      ybeam=self.lineEdit19.text().ascii()
      f.write('x reflected beam = '+ xbeam+'\n')
      f.write('y reflected beam = ' + ybeam+'\n')
      angle=self.lineEdit20.text().ascii()
      f.write('incidence angle = '+ angle+'\n')
   if self.radioButton5.isChecked():
      f.write('geometry = waxs \n')
      xbeam=self.lineEdit18.text().ascii()
      ybeam=self.lineEdit19.text().ascii()
   if self.checkBox_droplet.isChecked():
      f.write('dropletize = yes \n')
      ZerophotADU=self.lineEdit_0PhotADU.text().ascii()
      ZerophotSigma=self.lineEdit_0PhotSigma.text().ascii()
      OnephotADU=self.lineEdit_1PhotADU.text().ascii()
      OnephotSigma=self.lineEdit_1PhotSigma.text().ascii()
   else:
      f.write('dropletize = no \n')
      ZerophotADU='none'
      ZerophotSigma='none'
      OnephotADU='none'
      OnephotSigma='none'
   f.write('0 Photon ADU = ' +ZerophotADU+'\n')
   f.write('0 Photon Sigma = ' +ZerophotSigma+'\n')
   f.write('1 Photon ADU = ' +OnephotADU+'\n')
   f.write('1 Photon Sigma = ' +OnephotSigma+'\n')
   f.write('x direct beam = ' +xbeam+'\n')
   f.write('y direct beam = ' +ybeam+'\n')
   normalize=self.comboBox_normalize.currentText().ascii().lower()
   f.write('normalize = ' +normalize+'\n')
   darkstatus=self.checkBox_darks.isChecked()
   tol=float(self.lineEdit_tolerance.text().ascii())
   if (detector=='medipix')&(darkstatus is False)&(tol>0):
     self.lineEdit_tolerance.setText('0')
     self.lineEdit_tolerance_2.setText('0')
   tol=self.lineEdit_tolerance.text().ascii()
   f.write('tolerance = '+ tol+'\n')
   q1=self.lineEdit_firstq.text().ascii()
   f.write('first q = '+ q1+'\n')
   dq=self.lineEdit27.text().ascii()
   f.write('delta q = '+ dq+'\n')
   sq=self.lineEdit28.text().ascii()
   f.write('step q = '+ sq+'\n')
   nq=self.lineEdit_nq.text().ascii()
   f.write('number of q = '+ nq+'\n')
   nq_TRC=self.lineEdit_qTRC.text().ascii()
   f.write('q for TRC = '+ nq_TRC+'\n')
   f.close()
   print 'new input file created:', filename



}


void Form1::change_labelsq()
{
   self.textLabel29.setText('first angle (in degrees)')
   self.textLabel30.setText('delta angle (in degrees)')
   self.textLabel31.setText('step angle (in degrees)')
   self.textLabel32.setText('no. of angle')
   self.textLabel29_2.setText('first angle (in degrees)')
   self.textLabel30_2.setText('delta angle (in degrees)')
   self.textLabel31_2.setText('step angle (in degrees)')
}

void Form1::change_labelsback()
{
   Inv_Ang=u"(\u00C5\u207B\u00B9):"
   Ang=u"(\u00C5):"
   self.textLabel16.setText('waverlength '+ Ang)
   self.textLabel29.setText('first q '+ Inv_Ang)
   self.textLabel30.setText('delta q '+Inv_Ang)
   self.textLabel31.setText('step q ' + Inv_Ang)
   self.textLabel32.setText('no. of q')
   self.textLabel29_2.setText('first q '+ Inv_Ang)
   self.textLabel30_2.setText('delta q '+Inv_Ang)
   self.textLabel31_2.setText('step q ' + Inv_Ang)
}



void Form1::user_mask()
{
  from makemask import make_mask
  import os.path
  from get_edf import file_name
  self.makeinput()
  mask_file=self.lineEdit_mask.text().ascii()
  data_file=self.lineEdit_data.text().ascii()
  if os.path.exists(data_file) is False:
     print 'static data ', data_file, "doesn't exist:using first image"
     dir=self.lineEditDataDir.text().ascii()
     prefix=self.lineEditDataPrefix.text().ascii()
     suffix=self.lineEditDataSuff.text().ascii()
     no=self.lineEditDataStart.text().ascii()
     data_file=dir+file_name(prefix,suffix,no)
  if os.path.exists(mask_file) is False:
     self.automask()
  else:
     make_mask(data_file,mask_file)
  print 'done'
  self.plot_masked()

}

void Form1::plot_masked()
{
  from get_edf import file_name
  import EdfFile
  import os.path
  self.makeinput()
  data_file=self.lineEdit_data.text().ascii()
  if os.path.exists(data_file) is False:
     self.dostatic_quick()
  data=EdfFile.EdfFile(data_file)
  data=data.GetData(0)
  mask_file=self.lineEdit_mask.text().ascii()
  print mask_file
  self.automask()
  mymask=EdfFile.EdfFile(mask_file)
  mymask=mymask.GetData(0)+mymask.GetData(1)
  print 'plotted masked data'
  if self.checkBox_zoom.isChecked():
     self.matplotlibWidget1.update_figure(0,data+1,data_file,mymask,Zoom='fixed')
  else:
     self.matplotlibWidget1.update_figure(0,data+1,data_file,mymask)
}
void Form1::plot_unmasked()
{
  self.makeinput()
  import EdfFile
  from get_edf import file_name
  data_file=self.lineEdit_data.text().ascii()
  dataread=EdfFile.EdfFile
  if os.path.exists(data_file) is True:
     data=dataread(data_file)
     data=data.GetData(0)
     if self.checkBox_zoom.isChecked():
        self.matplotlibWidget1.update_figure(1,data+1,data_file,Zoom='fixed')
     else:
        self.matplotlibWidget1.update_figure(1,data+1,data_file)
}

void Form1::update_text()
{
#  mask_file=self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'mask.edf'
  data_file=self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'static.edf'
#  dark_file=self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'dark.edf'
  qmask_file=self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'qmask.edf'
  cf_file=self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'cf.dat'
  nq=self.lineEdit_plotq_TRcf.text().ascii()
  TRcf_file=self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'2times_q_'+nq+'.edf'
  nq_chi4=self.q_lineEdit_chi4.text().ascii()
  chi4_file=self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'fitchi4_q_'+nq_chi4+'.dat'
#  self.lineEdit_mask.setText(mask_file)
  self.lineEdit_data.setText(data_file)
#  self.lineEdit_dark.setText(dark_file)
  self.lineEdit_qmask.setText(qmask_file)
  self.lineEdit_cf.setText(cf_file)
  self.lineEdit_TRcf.setText(TRcf_file)
  self.lineEdit_chi4_file.setText(chi4_file)
 

}

void Form1::dodarks()
{ 
     self.makeinput()
     print 'calculating dark...'
     from some_modules_new import sum_data
     from get_edf import file_name
     import EdfFile
     dir=self.lineEditDarkDir.text().ascii()
     prefix=self.lineEditDarkPrefix.text().ascii()
     prefix=dir+prefix
     suffix=self.lineEditDataSuff.text().ascii()
     nstart=int(self.lineEditDarkStart.text().ascii())
     nend=int(self.lineEditDarkEnd.text().ascii())

     files=[]
     for i in range(nstart,nend):
        dark_file=file_name(prefix,suffix,i)
        files.append(dark_file)
     if os.path.exists(dir) is False:
        print "dark directory doesn't exist, please check it!!!!"
     elif os.path.exists(files[0]) is False:
        print "dark prefix or numbers wrong, please check it!!!!"
     else:
        detector=self.comboBox_detector.currentText().ascii().lower()
        flatfield_file=self.comboBox_flatfield.currentText().ascii()
        if flatfield_file== 'other':
           flatfield_file=self.lineEdit_other.text().ascii()
        while os.path.exists(files[-1]) is False:
           print 'waiting for dark ', files[-1]
        dark=sum_data(files,detector,flatfield_file)
        dark_file=self.lineEdit_dark.text().ascii()
        print dark_file
        avg=EdfFile.EdfFile(dark_file)
        avg.WriteImage({},dark,0,DataType='FloatValue')
        if self.checkBox_zoom.isChecked():
           self.matplotlibWidget1.update_figure(1,dark,dark_file,logscale='nolog',Zoom='fixed')
        else:
           self.matplotlibWidget1.update_figure(1,dark,dark_file,logscale='nolog')
        print '...done'
         
}
void Form1::dostatic_quick()
{
     print 'calculating quick static...'
     self.dostatic('quick')
}
void Form1::dostatic_all()
{
     print 'calculating accurate static...'
     self.dostatic('all')
}
void Form1::dostatic()
{
     #void Form1::dostatic(mode)
     from some_modules_new import do_average
     import EdfFile
     from read_input import get_input
     
     self.makeinput()
     inputfile=self.lineEdit_input.text().ascii()
     if mode=='quick':
        data=do_average(inputfile,nstart='first',nend='nstart+20')
     if mode=='all':
        data=do_average(inputfile,nstart='first',nend='last')
     data_file=self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'rawstatic.edf'
     avg=EdfFile.EdfFile(data_file)
     avg.WriteImage({},data,0,DataType='FloatValue')
     if self.checkBox_darks.isChecked():
        dark_file=self.lineEdit_dark.text().ascii()
        if os.path.exists(dark_file) is False:
          self.dodarks()
        dark=EdfFile.EdfFile(dark_file)
        dark=dark.GetData(0)
     else:
        dark=0*data
     data_file=self.lineEdit_data.text().ascii()
     if detector!= 'medipix':
        data=data-dark
     data[data<=0]=0
     avg=EdfFile.EdfFile(data_file)
     avg.WriteImage({},data,0,DataType='FloatValue')
     if self.checkBox_zoom.isChecked():
        self.matplotlibWidget1.update_figure(1,(data+1),data_file,Zoom='fixed')
     else:
        self.matplotlibWidget1.update_figure(1,(data+1),data_file)
     print '...done'
}



void Form1::plot_dark()
{
  import EdfFile
  from get_edf import file_name
  self.makeinput()
  dark_file=self.lineEdit_dark.text().ascii()
  if os.path.exists(dark_file) is False:
    self.dodarks()
  dark=EdfFile.EdfFile(dark_file)
  dark=dark.GetData(0)
  if self.checkBox_zoom.isChecked():
     self.matplotlibWidget1.update_figure(1,dark,dark_file,logscale='nolog',Zoom='fixed')
  else:
     self.matplotlibWidget1.update_figure(1,dark,dark_file,logscale='nolog')
}
void Form1::correlator()
{
import os.path 
import EdfFile
import threading 
from numpy import max
self.makeinput()
self.loadinput(0)
inputfile=self.lineEdit_input.text().ascii()
staticfile=self.lineEdit_data.text().ascii()
maskfile=self.lineEdit_mask.text().ascii()
darkfile=self.lineEdit_dark.text().ascii()
qmaskfile=self.lineEdit_qmask.text().ascii()
if self.checkBox_darks.isChecked():
   if os.path.exists(darkfile) is False:
      self.dodarks()
      self.dostatic_quick()
if os.path.exists(staticfile) is False:
   self.dostatic_quick()
static=EdfFile.EdfFile(staticfile)
static=static.GetData(0)
if os.path.exists(maskfile) is False:
   print 'making mask'
   self.automask() #the user_mask is directly called in automask as there is no mask file yet
mask=EdfFile.EdfFile(maskfile)
mask=mask.GetData(0)
if shape(mask)!=shape(static):
   print 'mask and static data have different size.... please make a mask!'
   self.user_mask()
if os.path.exists(qmaskfile) is False:
   print 'making q mask'
   self.Qs()
qmask=EdfFile.EdfFile(qmaskfile)
qmask=qmask.GetData(0)
nq=int(self.lineEdit_nq.text().ascii())
if int(max(qmask)/2)!= nq:
   print 'updating qmask...'
   self.Qs()
   print '...done'
if shape(qmask)!=shape(static):
   print 'q mask and static data have different size.... calculating q mask!'
   self.Qs()
if self.checkBox_plot.isChecked():
   arg=inputfile,darkfile,maskfile
else:
   arg=inputfile,darkfile,maskfile,'no'
self.Iq()
if self.checkBox_multiproc.isChecked():
   from correlator_online_new_mp import correlator_online_mp
   tmain=threading.Thread(target=correlator_online_mp,args=(arg))
else:
   from correlator_online_new import correlator_online
   tmain=threading.Thread(target=correlator_online,args=(arg))
tmain.start()
}

void Form1::stop_correlator()
{
  import os
  import threading
  print 'ciao'
  os.spawnlp(os.P_WAIT, 'stop')

}

void Form1::change_labelsbeam()
{
   self.textLabel19.setText('X reflected beam:')
   self.textLabel20.setText('Y reflected beam:')
   self.textLabel22.setEnabled(1)
   self.lineEdit20.setEnabled(1)
}
void Form1::change_labelsbeamback()
{
   self.textLabel19.setText('X direct beam:')
   self.textLabel20.setText('Y direct beam:')
}


void Form1::plot_raw()
{
  import os.path
  import EdfFile
  self.makeinput()
  raw_file=self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'rawstatic.edf'
  if os.path.exists(raw_file) is False:
     self.dostatic_quick()
  f=EdfFile.EdfFile(raw_file)
  data=f.GetData(0)
  if self.checkBox_zoom.isChecked():
     self.matplotlibWidget1.update_figure(1,data+1,raw_file,Zoom='fixed')
  else:
     self.matplotlibWidget1.update_figure(1,data+1,raw_file)
}


void Form1::plot_cf()
{
  import pylab as p
  file=self.lineEdit_cf.text().ascii()
  f=open(file,'r')
  title= f.readline()
  qlist=title.split(': ')[-1]
  qs=qlist.split(' ')
  f.close()
  hold=False
  nq=self.lineEdit_plotq.text().ascii()
  if nq.lower()=='all':
     firstq=int(1)
     lastq=len(qs)+1
  elif nq.find(':')!=-1:
     limits=nq.split(':')
     firstq=int(limits[0])
     lastq=int(limits[1])+1
  else:
     firstq=int(nq)
     lastq=int(nq)+1
  if self.checkBox_hold.isChecked():
     hold=True
  styles = ['o', '^', 'v', '<', '>', 's', '+']
  colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
  symbols=[]
  for style in styles:
     for color in colors:
         symbols.append(color+style)  
  for i in range(firstq,lastq):
    x,y=p.load(file,usecols=(0,i),unpack=True)
    symbol=symbols[i-firstq]+'-'
    label=r'$%s:\hspace{1} q=%5.4f \hspace{1} \AA^{-1}$' % (i,float(qs[i-1]))
    markers=self.matplotlibWidget_cf.update_plot(x,y,hold,label,symbol)
}


void Form1::del_cf()
{
  import pylab as p
  file=self.lineEdit_cf.text().ascii()
  nq=self.lineEdit_plotq.text().ascii()
  if nq.lower()=='all':
      self.matplotlibWidget_cf.cla() 
  else:
    if nq.find(':')!=-1:
      limits=nq.split(':')
      firstq=int(limits[0])
      lastq=int(limits[1])+1
    else:
      firstq=int(nq)
      lastq=int(nq)+1
    for i in range(firstq,lastq):
      x,y=p.load(file,usecols=(0,i),unpack=True)
      self.matplotlibWidget_cf.remove_plot(x,y)

}


void Form1::plot_TRcf()
{
  import ytrc
  import os.path
  self.update_text()
  file=self.lineEdit_TRcf.text().ascii()
  if os.path.exists(file) is False:
     print 'file ', file, "doesn't exist"
  else:
    zmin=self.lineEdit_zmin.text().ascii()
    zmax=self.lineEdit_zmax.text().ascii()
    data=  ytrc.read(file)
    datadim=sqrt(size(data))
    while datadim>8000:
       newdim=int(datadim/2)
       data=ytrc.rebin(data,(newdim,newdim))
       datadim=sqrt(size(data))
    if zmin!='auto':
       zmin=float(zmin)
    else:
       self.lineEdit_zmin.setText(str(amin(log(data))))
    if zmax!='auto':
       zmax=float(zmax)
    else:
       self.lineEdit_zmax.setText(str(amax(log(data))))
    self.matplotlibWidget_TRC.update_figure(1,data,file,logscale='log',zmax=zmax,zmin=zmin)
}


void Form1::calc_TRCF()
{
  import thread
  from some_modules_new import TRCF
  self.update_text()
  outfile=self.lineEdit_TRcf.text().ascii()
  nq=int(lineEdit_plotq_TRcf.text().ascii())
  thread.start_new_thread(TRCF(nq,outfile))
}


void Form1::Qs()
{
   from read_input import get_input
   from q_pattern import qpattern
   import pylab as p
   import EdfFile
   
   self.makeinput()
   input_file=self.lineEdit_input.text().ascii()
   input_info=get_input(input_file)
   qtot=qpattern(input_info)
   geometry=input_info['geometry']
   if geometry == 'gisaxs':
      qtot=qtot[1]
   firstq=float(input_info['first q'])
   deltaq=float(input_info['delta q'])
   stepq=float(input_info['step q'])
   nq=int(input_info['number of q'])
   lastq=firstq+nq*(stepq+deltaq)
   qvalues=arange(firstq,lastq,stepq+deltaq)
   if len(qvalues)>nq:
     qvalues.resize((nq,))
   qaxis_list=[]
   I=[]
   static_file=self.lineEdit_data.text().ascii()
   if os.path.exists(static_file) is False:
      self.dostatic_quick()
   static=EdfFile.EdfFile(static_file)
   static_data=static.GetData(0)
   mask_file=self.lineEdit_mask.text().ascii()
   if os.path.exists(mask_file) is False:
      self.user_mask()
   tot=EdfFile.EdfFile(mask_file)
   if tot.GetNumImages()!=2:
      self.automask()
      tot=EdfFile.EdfFile(mask_file)
   totmask=tot.GetData(0)+tot.GetData(1)
   fileq=self.lineEdit_qmask.text().ascii()
   file=EdfFile.EdfFile(fileq)
   qvalue=firstq
   firsttime=0
   qsave=0*static_data
   n=0
   for el,q in enumerate(qvalues):
      ind=where((qtot>=q)&(qtot<=q+deltaq)&(totmask==0))
      npixel=len(ind[0])
      #This is to reject q-rings that have no pixels (e.g. behind the beamstop or outside the ccd range, it permits to put in the input firstq=0 and an arbitrary high number of qs)
      if npixel!=0:
         n+=2
         if firsttime==0:
            firstq=q
            self.lineEdit_firstq.setText(str(firstq))
         qsave[ind]=n
         firsttime=1
         qval=q+deltaq/2
         qaxis_list.append(qval)
         I.append(p.average(static_data[ind]))
   file.WriteImage({},qsave,0)
   outfile=self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'1Dstatic.dat'
   f=open(outfile,'w')
   f.write('#q (1/Ang) I(q) (a.u.) \n')
   qaxis=array(qaxis_list)
   I_q=array(I)
   tosave=transpose(array([qaxis,I_q]))
   p.save(f,tosave)
   f.close()

   nq=len(qaxis_list)
   self.lineEdit_nq.setText(str(nq))
   qsave[qsave==0]=1
   qsave[qsave>=2]=0
   if self.checkBox_zoom.isChecked():
      self.matplotlibWidget1.update_figure(0,static_data+1,fileq,qsave+totmask,Zoom='fixed')
   else:
      self.matplotlibWidget1.update_figure(0,static_data+1,fileq,qsave+totmask)
   self.makeinput()
}


void Form1::plotQmask()
{ 
   import EdfFile 
   static_file=self.lineEdit_data.text().ascii()
   if os.path.exists(static_file) is False:
      self.dostatic_quick()
   static=EdfFile.EdfFile(static_file)
   static_data=static.GetData(0)
   mask_file=self.lineEdit_mask.text().ascii()
   if os.path.exists(mask_file) is False:
      self.user_mask()
   tot=EdfFile.EdfFile(mask_file)
   if tot.GetNumImages()!=2:
      self.automask()
      tot=EdfFile.EdfFile(mask_file)
   totmask=tot.GetData(0)+tot.GetData(1)
   fileq=self.lineEdit_qmask.text().ascii()
   if os.path.exists(fileq) is False:
      self.Qs()
   file=EdfFile.EdfFile(fileq)
   q=file.GetData(0)
   q[q==0]=1
   q[q>=2]=0
   if self.checkBox_zoom.isChecked():
      self.matplotlibWidget1.update_figure(0,static_data+1,fileq,q+totmask,Zoom='fixed')
   else:
      self.matplotlibWidget1.update_figure(0,static_data+1,fileq,q+totmask,)
}


void Form1::Iq()
{
   from pylab import load
   import EdfFile 
   from read_input import get_input
   from q_pattern import qpattern

   self.makeinput()
   input_file=self.lineEdit_input.text().ascii()
   input_info=get_input(input_file)
   qtot=qpattern(input_info)
   geometry=input_info['geometry']
   if geometry == 'gisaxs':
      qtot=qtot[1]
   wavelength=float(self.lineEdit_lambda.text().ascii())
   distance=float(self.lineEdit_dsd.text().ascii())
   detector=self.comboBox_detector.currentText().ascii().lower()
   if detector == 'princeton' or detector == 'andor 22.5micron':
      pix_size=0.0225      
   if detector == 'medipix':
      pix_size=0.055      
   if detector == 'andor 13micron' or detector == 'andor':
      pix_size=0.013      
   deltaq=4*pi/wavelength*sin(arctan(2*pix_size/distance)/2)
   static_file=self.lineEdit_data.text().ascii()
   if os.path.exists(static_file) is False:
      self.dostatic_quick()
   static=EdfFile.EdfFile(static_file)
   static_data=static.GetData(0)
   mask_file=self.lineEdit_mask.text().ascii()
   if os.path.exists(mask_file) is False:
      self.user_mask()
   tot=EdfFile.EdfFile(mask_file)
   if tot.GetNumImages()!=2:
      self.automask()
      tot=EdfFile.EdfFile(mask_file)
   totmask=tot.GetData(0)+tot.GetData(1)

   q=qtot[totmask==0]
   indq=argsort(q)
   q=q[indq]
   qr=arange(min(q),max(q)+deltaq,deltaq)
   m=static_data[totmask==0]
   m=m[indq]
   lqv=len(qr)
   
   radi=zeros((lqv,2))
   ini=0
   hh,bins=histogram(q,lqv,new=True)
   radi[:,0]=bins[:-1]+deltaq/2
   for i in xrange(lqv):
      radi[i,1]=mean(m[ini:ini+hh[i]])
      ini=ini+hh[i]
   outfile=self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'1Dstatic_fine.dat'
   savetxt(outfile,radi)
   outfile=self.lineEdit12.text().ascii()+'/'+self.lineEdit13.text().ascii()+'1Dstatic.dat'
   x_cf,y_cf= load(outfile,unpack=True)
   radi=transpose(radi)
   self.matplotlibWidget1.update_plotlog(x_cf,y_cf,radi[0],radi[1])
}


void Form1::automask()
{
 import EdfFile
 from read_input import get_input
 from some_modules_new import auto_mask
 from time import sleep
 filename=self.lineEdit_input.text().ascii()
 self.makeinput()
 input_info=get_input(filename)
 tolerance=float(input_info['tolerance'])
 print 'tolearance = ', tolerance
 datafile=self.lineEdit_data.text().ascii()
 if os.path.exists(datafile) is False:
    self.dostatic_quick()
 data=EdfFile.EdfFile(datafile)
 if tolerance>=0:
   detector=self.comboBox_detector.currentText().ascii().lower()
   treshold_mask=auto_mask(input_info,dark_file=self.lineEdit_dark.text().ascii())
 else:
     print 'using only user mask'
     treshold_mask=zeros(shape(data.GetData(0)),dtype=int)
 mask_file=self.lineEdit_mask.text().ascii()
 print mask_file
 if os.path.exists(mask_file) is False:
   print 'make user mask'
   tot=EdfFile.EdfFile(mask_file)
   usermask=0*treshold_mask
   tot.WriteImage({},usermask,0)
   tot.WriteImage({},treshold_mask,1)
   del tot
   self.user_mask()
 else: 
   tot=EdfFile.EdfFile(mask_file)
   usermask=tot.GetData(0)
   tot.WriteImage({},usermask,0)
   tot.WriteImage({},treshold_mask,1)
   del tot
}


void Form1::clear_cf()
{
  self.matplotlibWidget_cf.cla()
}


void Form1::chi4()
{
  from chi4_chiara import chi4
  import pylab as p
  import threading 
  self.update_text()
  inputfile=self.lineEdit_input.text().ascii()
  q_chi4=int(self.q_lineEdit_chi4.text().ascii())
  print '...calculating chi4'
  mask_file=self.lineEdit_mask.text().ascii()
  dark_file=self.lineEdit_dark.text().ascii()
  arg=q_chi4,inputfile,dark_file,mask_file
  tchi4=threading.Thread(target=chi4,args=(arg))
  tchi4.start()
#  tchi4.join()
  print 'plotting'
#  chi4(q_chi4,fileinput=inputfile,mask_file=mask_file,dark_file=dark_file)
  self.plot_chi4()
}


void Form1::plot_chi4()
{
  import pylab as p
  import os.path
  
  self.update_text()
  chi4_file=self.lineEdit_chi4_file.text().ascii()
  if os.path.exists(chi4_file) is False:
     print 'chi4 file ', chi4_file, "doesn't exist"
  else:
     x,y=p.load(chi4_file,usecols=(0,1),unpack=True)
     hold=False 
     if self.checkBox_hold_chi4.isChecked():
        hold=True
     self.matplotlibWidget_chi4.update_plot(x,y,hold,label='chi4',symbol='ro-')
}


void Form1::fit()
{
  import os
  import threading
  tmain=threading.Thread(target=os.spawnlp,args=(os.P_WAIT,'PYFIT'))
  tmain.start()

#  os.spawnlp(os.P_WAIT, 'multifit_gui')
}


void Form1::activate_flatfield()
{
   detector=self.comboBox_detector.currentText().ascii().lower()
   if detector!='medipix':	   
      self.checkBox_flatfield.setEnabled(0)
      self.comboBox_flatfield.setEnabled(0)
   else:
      self.checkBox_flatfield.setEnabled(1)
      self.checkBox_flatfield.setChecked(1)
      self.comboBox_flatfield.setEnabled(1)
      self.comboBox_flatfield.setCurrentItem(0)
}

void  Form1::Loadflatfield()
{
   from qt import QFileDialog 
   PathLineEdit = "./"
   flatfield_file = QFileDialog.getOpenFileName(PathLineEdit,('*.edf'))
   self.lineEdit_other.setText(flatfield_file)


void Form1::activateLoad()
{
   flatfield_file=self.comboBox_flatfield.currentText().ascii().lower()
   if flatfield_file=='other':
      self.Loadflatfield()
      self.lineEdit_other.setEnabled(1)
   else:
      self.lineEdit_other.clear()
      self.lineEdit_other.setEnabled(0)
}

void  Form1::LoadDataDir()
{
   from qt import QFileDialog 
   PathLineEdit = "./"
   dir = QFileDialog.getExistingDirectory(PathLineEdit)
   if dir:
      self.lineEditDataDir.setText(dir)
}
void  Form1::LoadDarkDir()
{
   from qt import QFileDialog 
   PathLineEdit = self.lineEditDataDir.text().ascii()
   dir = QFileDialog.getExistingDirectory(PathLineEdit)
   if dir:
      self.lineEditDarkDir.setText(dir)
}

void  Form1::LoadOutDir()
{
   from qt import QFileDialog 
   PathLineEdit = "./"
   dir = QFileDialog.getExistingDirectory(PathLineEdit)
   if dir:
      self.lineEdit12.setText(dir)
}

void  Form1::LoadMaskFile()
{
   from qt import QFileDialog 
   PathLineEdit = self.lineEdit_mask.text().ascii()
   filename = QFileDialog.getOpenFileName(PathLineEdit,('*.edf'))
   if filename:
      self.lineEdit_mask.setText(filename)
}

void  Form1::LoadDarkFile()
{
   from qt import QFileDialog 
   PathLineEdit = self.lineEdit_dark.text().ascii()
   filename = QFileDialog.getOpenFileName(PathLineEdit,('*.edf'))
   if filename:
      self.lineEdit_dark.setText(filename)
}


void Form1::SetNormalizeList()
{
   self.comboBox_normalize.clear()
   self.comboBox_normalize.insertItem(self.__tr("None"))
   self.comboBox_normalize.insertItem(self.__tr("Average in CCD"))
   detector=self.comboBox_detector.currentText().ascii().lower()
   if detector!='medipix':
      self.comboBox_normalize.insertItem(self.__tr("Monitor"))

}
