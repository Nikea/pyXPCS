from sys import argv
from numpy import *
#import EdfFile
from some_modules_new import loadedf, saveedf, headersedf, headeredf
import matplotlib.mlab
from matplotlib.nxutils import points_inside_poly
import matplotlib.pylab as p
import os.path
from numpy.ma import masked_array
#from commands import getoutput 

MASK_FIGURE_ID = 2

def make_mask(data_file,mask_file='none'):
   global key, x, y,lc,data,im,xy,mymask,xx,yy,px,lx,lm,default_mask,maskfig
   # determine if a point is inside a given polygon or not
   # Polygon is a list of (x,y) pairs.
      
   
   #read input parameters
   print "masking the edf file"
   print "use mouse to select a region"
   print "m - to mask selected region"
   print "u - to unmask selected region"
   print "a - to cancel selected region"
   print "w - to save mask and exit"
   #print "e - to exit"
   
   data=loadedf(data_file)
   lx,ly=shape(data)
   if os.path.exists(mask_file) is True:
      mymask=loadedf(mask_file,0)
      automask=loadedf(mask_file,1)
      if shape(mymask)!=shape(data):
         mymask=zeros((lx,ly))
   else:
      mymask=zeros((lx,ly))
      automask=zeros((lx,ly))

   #points=[]
   #for i in range(lx):
   #    for j in range(ly):
   #     points.append([i,j]) 
   
   x, y = meshgrid(arange(lx), arange(ly))
   x, y = x.flatten(), y.flatten()
   points = vstack((x,y)).T

   key=[]
   x=0
   y=0
   xy=[]
   xx=[]
   yy=[]
   print "Make Mask"
  
   def on_click(event):
       print "On click"
       global key, x, y,lc,data,im,xy,mymask,xx,yy,px,lx,lm,default_mask,maskfig
       if not event.inaxes: 
           xy=[]
           return
       x,y=int(event.xdata), int(event.ydata)
       xx.append([x])
       yy.append([y])
       xy.append([y,x])
       lc.set_data(xx,yy)
       p.draw()
   def on_click_key(event):
       global key, x, y,lc,data,im,xy,mymask,xx,yy,px,lx,lm,default_mask,maskfig
       key=event.key
       if not event.inaxes: 
          xy=[]
          return
       if key=='a':
          xx=[]
          yy=[]
          xy=[]  
          x=0
          y=0
          lc.set_data(xx,yy)
          lm.set_data(xx,yy)
          p.draw()
       if key=='m':
           #print 'masking'
           xx.append(xx[0])#xx[-1]=xx[0]
           yy.append(yy[0])#yy[-1]=yy[0]
           xy.append(xy[0])#xy[-1]=xy[0]
           ind=points_inside_poly(points,xy).reshape(lx,ly).T
           mymask[ind]=1
           data=masked_array(data,mymask+automask)
           im.set_data(data)
           xx=[]
           yy=[]
           xy=[] 
           lc.set_data(xx,yy)
           lm.set_data(xx,yy)
           p.draw()
           x=0
           y=0 
           print "key m pressed"
       if key=='u': 
           xx.append(xx[0])#xx[-1]=xx[0]
           yy.append(yy[0])#yy[-1]=yy[0]
           xy.append(xy[0])#xy[-1]=xy[0]
           ind=points_inside_poly(points,xy).reshape(lx,ly).T
           mymask[ind]=0
           data=masked_array(data,mymask+automask)
           im.set_data(data)
           xx=[]
           yy=[]
           xy=[] 
           lc.set_data(xx,yy)
           lm.set_data(xx,yy)
           p.draw()
           x=0
           y=0
           print "key u pressed"
       if key=='r':
          mymask=0*mymask
          mymask=mymask.reshape(lx,ly)
          data=masked_array(data,mymask+automask)
          im.set_data(data)
          xx=[]
          yy=[]
          xy=[] 
          lc.set_data(xx,yy)
          lm.set_data(xx,yy)
          p.draw()
          x=0
          y=0 
          print "key r pressed"
       if key=='w':
          p.close()
          saveedf(mask_file,mymask,0)
          saveedf(mask_file,automask,1)
          print "key w pressed, CLOSING"
          return
   
   def on_move(event):
       #print"On move"
       global lm,x,y
       if not event.inaxes: return
       xm,ym=int(event.xdata), int(event.ydata)
       # update the line positions
       if x!=0: 
           lm.set_data((x,xm),(y,ym))
           p.draw()
   p.rc('image',origin = 'lower')
   p.rc('image',interpolation = 'nearest')
   p.figure()
   px=p.subplot(111)
   data=p.log(data+1)
   im=p.imshow(masked_array(data,mymask+automask))
   p.title("Select a ROI. Press m to mask or u to unmask it \n w to write mask and exit")
   lc,=px.plot((0,0),(0,0),'-+m',linewidth=1,markersize=8,markeredgewidth=1)
   lm,=px.plot((0,0),(0,0),'-+m',linewidth=1,markersize=8,markeredgewidth=1)
   px.set_xlim(0,ly)
   px.set_ylim(0,lx)
   #p.ion()
   cidb=p.connect('button_press_event',on_click)
   cidk=p.connect('key_press_event',on_click_key)
   cidm=p.connect('motion_notify_event',on_move)
   p.show()
