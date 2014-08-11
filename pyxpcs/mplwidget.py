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
import sys, os, random, matplotlib
from PyQt4 import QtGui, QtCore
from numpy import *
import numpy.ma as ma
matplotlib.rc('image',origin = 'lower')
matplotlib.rc('image',interpolation = 'nearest')
matplotlib.rc('legend',numpoints = 1)
matplotlib.rc('legend',fontsize = 11)
from matplotlib import pylab
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector,Cursor


class MplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    global symbols
    styles = ['o', '^', 'v', '<', '>', 's', '+']
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    symbols=[]
    for style in styles:
       for color in colors:
          symbols.append(color+style+'-')

    def __init__(self, parent=None, name=None, width=5, height=4, dpi=100, bgcolor=None):
	self.parent = parent
	if self.parent:
		bgc = parent.backgroundBrush().color()
		bgcolor = float(bgc.red())/255.0, float(bgc.green())/255.0, float(bgc.blue())/255.0
		#bgcolor = "#%02X%02X%02X" % (bgc.red(), bgc.green(), bgc.blue())

        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=bgcolor, edgecolor=bgcolor)
        self.axes = self.fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        FigureCanvas.__init__(self, self.fig)
#        self.reparent(parent, QPoint(0, 0))

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

###################################################################



class MplWidget(QtGui.QWidget):
    """Widget defined in Qt Designer"""
    def __init__(self, parent = None):
        # initialization of Qt MainWindow widget
        QtGui.QWidget.__init__(self, parent)
        # set the canvas to the Matplotlib widget
        self.canvas = MplCanvas()
        # create a vertical box layout
        self.vbl = QtGui.QVBoxLayout()
        # add mpl widget to the vertical box
        self.vbl.addWidget(self.canvas)
        # set the layout to the vertical box
        self.setLayout(self.vbl)

####################################################################

    def line_select_callback(self,event1, event2):
       'event1 and event2 are the press and release events'
       x1, y1 = event1.xdata, event1.ydata
       x2, y2 = event2.xdata, event2.ydata
       if x1*y1!=x2*y2:
          xmin=min(x1,x2)
          xmax=max(x1,x2)
          ymin=min(y1,y2)
          ymax=max(y1,y2)
          zoom=array([xmin,xmax,ymin,ymax])
          self.axes.axis(zoom)
          matplotlib.rc('image',origin = 'lower')

    def on_move(self,event):
       global text1,image, title,fname
       #get the x and y pixel coords
       self.canvas.axes.set_title(fname)
       if event.inaxes is not None:
          x=int(event.xdata)
          y=int(event.ydata)
          if type(image) is ma.masked_array:
             if image.mask[y,x]:
                lab= 'data coords: %d,%d \nMasked pixel' % (x, y)
             else:
                lab= 'data coords: %d,%d \nInt: %3.1f' % (x, y,image[y,x])
          else:
             lab= 'data coords: %d,%d \nInt: %3.1f' % (x, y,image[y,x])
          text1.set_text(lab)
       else:
          self.canvas.axes.set_title(fname)
          text1.set_text(' ')
       self.canvas.draw()

    ################################ 
    def on_movel(self,event):
       global text1,image, title,fname
       #get the x and y pixel coords
       self.canvas.axes.set_title(fname)
       if not event.inaxes:
           text1.set_text(' ')
           return
       x,y=float(event.xdata),float(event.ydata) 
       lab= 'data coords: x=%.4f, y=%.4f' % (x, y) 
       text1.set_text(lab)
       self.canvas.draw()
       text1.set_text(' ')
    ##################################
    def sizeHint(self):
        w = self.canvas.fig.get_figwidth()
        h = self.canvas.fig.get_figheight()
        return QtCore.QSize(w, h)

    def minimumSizeHint(self):
        return QtCore.QSize(10, 10)

    def update_figure(self,n,data,filename,mymask='none',logscale='log',Zoom='auto',zmax='auto',zmin='auto'):
        from numpy.ma import masked_array
        global text1,image,cid,title,fname
        try:
            self.canvas.fig.canvas.mpl_disconnect(cid)
        except: pass
        fname=filename
        if Zoom=='fixed':
           axis_zoom=self.canvas.axes.axis()
        text1=self.canvas.fig.text(0,0,'')
        self.canvas.axes.set_xscale('linear')
        self.canvas.axes.set_yscale('linear')
        if logscale=='log':
           data=log(data)
        if n==0:
           image=masked_array(data,mask=mymask)
        if n==1:
           image=data
        cid = self.canvas.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        if ((zmax!='auto')&(zmin!='auto')):
           print 'rescaling all'
           a=self.canvas.axes.imshow(image, vmax=zmax,vmin=zmin)
        elif zmin!='auto':
           a=self.canvas.axes.imshow(image, vmin=zmin)
        elif zmax!='auto':
           a=self.canvas.axes.imshow(image, vmin=zmax)
        else:
           a=self.canvas.axes.imshow(image)
        if Zoom=='fixed':
           a=self.canvas.axes.axis(axis_zoom)
        LS=RectangleSelector(self.canvas.axes, self.line_select_callback,drawtype='box',rectprops=dict(edgecolor = 'black',
                   alpha=0.5, fill=False),lineprops = dict(color='black', linestyle='-',linewidth = 10, alpha=0.5))
        self.canvas.axes.set_title(filename)
        self.canvas.draw()
        fname=filename


    def update_plot(self,cf_data,hold,firstq,lastq,qs,filename,ylabel):
        #styles = ['o', '^', 'v', '<', '>', 's', '+']
        #colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        #symbols=[]
        #for style in styles:
        #   for color in colors:
        #      symbols.append(color+style+'-')
        self.canvas.axes.hold(hold)
        for i in range(firstq,lastq):
            label=r'$%s:\hspace{1} q=%5.4f \hspace{1} \AA^{-1}$' % (i,float(qs[i-1]))
            self.canvas.axes.semilogx(cf_data[:,0],cf_data[:,i],symbols[i], label=label)
        labels = [line.get_label() for line in self.canvas.axes.lines]
        self.canvas.axes.set_xlabel("t (s)") 
        self.canvas.axes.set_ylabel(ylabel)
        self.canvas.axes.legend(self.canvas.axes.lines, labels, 'best')
        leg= self.canvas.fig.gca().get_legend()
        leg.draw_frame(False)
        self.canvas.axes.set_title(filename) 
        self.canvas.draw()

    def update_plotlog(self,x1,y1,x2,y2):
        global text1,image,title,fname,cid
        try:
            self.fig.canvas.mpl_disconnect(cid)
        except: pass
        text1=self.canvas.fig.text(0,0,'')
        self.canvas.axes.set_title('I(q)')
        bgcolor='None'
        axis_zoom=self.canvas.axes.axis()
        self.canvas.axes.axis('tight')
        if len(shape(x1))==0:
           self.canvas.axes.loglog((x1,),(y1,),'ro',x2,y2,'b-')
        else:
           self.canvas.axes.loglog(x1,y1,'ro',x2,y2,'b-')
        self.canvas.draw()
        self.canvas.axes.set_xlabel("Q (1/A)") 
        self.canvas.axes.set_ylabel("I(q) (arb.u.)")
        fname='I(q)'
        cid = self.canvas.fig.canvas.mpl_connect('motion_notify_event', self.on_movel)


    def remove_plot(self,y):
        ry=range(len(y[0,:]))  
        for i in ry:
          for line in self.canvas.axes.lines:
            if average(y[:,i]-line.get_ydata())==0:
              self.canvas.axes.lines.remove(line)
        if self.canvas.axes.lines!=[]:
            labels = [line.get_label() for line in self.canvas.axes.lines]
            self.canvas.axes.legend(self.canvas.axes.lines, labels, 'best')
            leg= self.canvas.fig.gca().get_legend()
            leg.draw_frame(False)
        else:
            labels = []
            self.canvas.axes.legend_= None
        self.canvas.draw()

    def cla(self):
        self.canvas.axes.lines=[]
        labels = []
        self.canvas.axes.legend_= None
        self.canvas.draw()