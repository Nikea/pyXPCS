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


void Form1::load_input()
{
   import os.path
   inputfile=self.lineEdit_input.text().ascii() 
   if os.path.exists(inputfile) is True:
      f=open(inputfile,'r')
      self.textEdit_input.setText(f.read())
      f.close()
}


void Form1::save_input()
{
   import os.path
   import shutil as s    
   inputfile=self.lineEdit_input.text().ascii()
   print 'saving file: ', inputfile     
   if os.path.exists(inputfile) is True:
     s.copyfile(inputfile,inputfile+'~')
     print 'Input file already exist, saving a backup copy as ', inputfile+'~'
   f=open(inputfile,'w')
   text= self.textEdit_input.text().ascii()
   f.write(text)
   f.close()
}

void Form1::fit()
{
   from read_input import get_input
   import os.path     
   from multi_fit import multifit
   inputfile=self.lineEdit_input.text().ascii()    
   infos=get_input(inputfile)
   infile=infos['file']
   outdir= self.lineEdit_outdir.text().ascii()
   outpref= self.lineEdit_outpref.text().ascii()
   if outdir=='auto':
     tot= os.path.abspath(infile)
     outdir=os.path.dirname(tot)   
     self.lineEdit_outdir.setText(outdir)     
   if outpref=='auto':
     tot= os.path.abspath(infile)
     outpref,suff=os.path.splitext(os.path.basename(tot))             
     self.lineEdit_outpref.setText(outpref)   
   self.lineEdit_filepars.setText(os.path.join(outdir,outpref+'_fitpar.dat'))
   self.lineEdit_filefit.setText(os.path.join(outdir,outpref+'_fitcol$ncol$.dat'))
   print 'start fitting...'     

   col=self.lineEdit_col.text().ascii()
   if self.checkBox_plot.isChecked():
      multifit(col,outdir,outpref,inputfile)
   else:
      multifit(col,outdir,outpref,inputfile,doplot='no')
}

