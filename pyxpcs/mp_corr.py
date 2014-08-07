from numpy import *
from time import time


###############################################################################################################
def mp_corr(iproc,nfile,chn,plot,npix_per_q,index_in_q,quc,quce,quplot):
   global datreg, nq, corf, n, nc, sl, sr, chn2, lind, srr, sll, oneq, rch, rcr, xnq, sst 
   

########################################################################################
#function correlator
   def correlator(reg,matrx):
       global datreg, corf, sl, sr, sst 
       if nc<=chn:
           if nc>=2:
               for cindex in xnq:
                   sr[cindex,:n]=roll(sr[cindex,:n],1)
                   sr[cindex,0]=sr[cindex,1]+sst[reg][cindex]#pyfmean(datreg[reg][cindex][:,0],lind[cindex])#average intensity in q for normalization right
                   sst[reg][cindex]=dot(oneq[cindex],matrx[cindex])/lind[cindex]
                   sl[cindex,:n]+=sst[reg][cindex]#pyfmean(matrx[cindex],lind[cindex])#average intensity in q for normalization left
           else:
               for cindex in xnq:
                   sst[reg][cindex]=dot(oneq[cindex],matrx[cindex])/lind[cindex]
           for cindex in xnq:
               corf[cindex,:n]+=dot(matrx[cindex],datreg[reg][cindex][:,:n])/lind[cindex] #calculate a product of input data and register corf(number of q's, number of chanels)
               datreg[reg][cindex]=concatenate((reshape(matrx[cindex],(lind[cindex],1)), datreg[reg][cindex][:,:chn-1]), axis=1) #shift register by 1
           if nc/2==nc/2.:
               for cindex in xnq:
                   matrx[cindex]=(datreg[reg][cindex][:,0]+datreg[reg][cindex][:,1])/2. #data for the next register from present  
               correlator2(1,matrx)
       else:
           for cindex in xnq:
               sr[cindex,:chn]=roll(sr[cindex,:chn],1)
               sr[cindex,0]=sr[cindex,1]+sst[reg][cindex]#pyfmean(datreg[reg][cindex][:,0],lind[cindex])#average intensity in q for normalization right
               sst[reg][cindex]=dot(oneq[cindex],matrx[cindex])/lind[cindex]
               sl[cindex,:chn]+=sst[reg][cindex]#pyfmean(matrx[cindex],lind[cindex])#average intensity in q for normalization left
               corf[cindex,:chn]+=dot(matrx[cindex],datreg[reg][cindex])/lind[cindex] #calculate a product of input data and register corf(number of q's, number of chanels)
               datreg[reg][cindex]=concatenate((reshape(matrx[cindex],(lind[cindex],1)), datreg[reg][cindex][:,:chn-1]), axis=1) #shift register by 1 
           if nc/2==nc/2.:
               for cindex in xnq:
                   matrx[cindex]=(datreg[reg][cindex][:,0]+datreg[reg][cindex][:,1])/2. #data for the next register from present
               correlator2(1,matrx)
###############################################################            
#correlator2(reg,matrx)

   def correlator2(reg,matrx):
       global datreg, corf, sl, sr, srr, sll, sst
       condition=((reg+1)<rch and nc/2**(reg+1)==nc/2.**(reg+1))
       corn=nc/2**reg
       if 2<=corn<=chn:#corn<=chn and corn>=2:
           for cindex in xnq:
               srr[reg][cindex,:corn-1]=roll(srr[reg][cindex,:corn-1],1)
               srr[reg][cindex,0]=srr[reg][cindex,1]+sst[reg][cindex]#pyfmean(datreg[reg][cindex][:,0],lind[cindex])#average intensity in q for normalization right
               sst[reg][cindex]=dot(oneq[cindex],matrx[cindex])/lind[cindex]
               sll[reg][cindex,:corn-1]+=sst[reg][cindex]#pyfmean(matrx[cindex],lind[cindex])#average intensity in q for normalization left
       if corn>chn:
           for cindex in xnq:
               srr[reg][cindex,:chn]=roll(srr[reg][cindex,:chn],1)
               srr[reg][cindex,0]=srr[reg][cindex,1]+sst[reg][cindex]#pyfmean(datreg[reg][cindex][:,0],lind[cindex]) #average intensity in q for normalization right
               sst[reg][cindex]=dot(oneq[cindex],matrx[cindex])/lind[cindex]
               sll[reg][cindex,:chn]+=sst[reg][cindex]#pyfmean(matrx[cindex],lind[cindex])#average intensity in q for normalization left
       if  chn2<corn<=chn:#corn<=chn and corn>chn/2:
           inb=chn2*(reg+1)
           ine=corn+chn2*reg
           sl[:,inb:ine]=sll[reg][:,chn2:corn]
           sr[:,inb:ine]=srr[reg][:,chn2:corn]
           for cindex in xnq:
               corf[cindex,inb:ine]+=dot(matrx[cindex],datreg[reg][cindex][:,chn2:corn])/lind[cindex] #calculate a product of input data and register corf(number of q's, number of chanels)
               datreg[reg][cindex]=concatenate((reshape(matrx[cindex],(lind[cindex],1)), datreg[reg][cindex][:,:chn-1]), axis=1) #shift register by 1 
           if condition:#nc/2**(reg+1)==floor(nc/2**(reg+1)):
               for cindex in xnq:
                   matrx[cindex]=(datreg[reg][cindex][:,0]+datreg[reg][cindex][:,1])/2. #data for the next register from present
               reg+=1
               correlator2(reg,matrx)
       elif corn>chn:
           inb=chn2*(reg+1)
           ine=chn2*(reg+2)
           sl[:,inb:ine]=sll[reg][:,chn2:chn]
           sr[:,inb:ine]=srr[reg][:,chn2:chn]
           for cindex in xnq:
               corf[cindex,inb:ine]+=dot(matrx[cindex], datreg[reg][cindex][:,chn2:chn])/lind[cindex] #calculate a product of input data and register corf(number of q's, number of chanels)
               datreg[reg][cindex]=concatenate((reshape(matrx[cindex],(lind[cindex],1)), datreg[reg][cindex][:,:chn-1]), axis=1) #shift register by 1 
           if condition:#nc/2**(reg+1)==floor(nc/2**(reg+1))
               for cindex in xnq:
                   matrx[cindex]=(datreg[reg][cindex][:,0]+datreg[reg][cindex][:,1])/2. #data for the next register from present"""
               reg+=1
               correlator2(reg,matrx)
       else: 
           for cindex in xnq:
               sst[reg][cindex]=dot(oneq[cindex],matrx[cindex])/lind[cindex]
           for cindex in xnq:
               datreg[reg][cindex]=concatenate((reshape(matrx[cindex],(lind[cindex],1)), datreg[reg][cindex][:,:chn-1]), axis=1) #shift register by 1
           if condition:#nc/2**(reg+1)==floor(nc/2**(reg+1)):
               for cindex in xnq:
                    matrx[cindex]=(datreg[reg][cindex][:,0]+datreg[reg][cindex][:,1])/2. #data for the next register from present"""
               reg+=1
               correlator2(reg,matrx)
#####################################################################################################################

##FINISHED INITIALIZING PART OF THE CODE######
   ##START MAIN PART FOR CORRELATION#####
   tcalc=time()
   chn2=chn/2
   datregt=[]
   datreg=[]
   nq=len(index_in_q)
   xnq=xrange(nq)
   rch=int(ceil(log(nfile/chn)/log(2))+1)
   for ir in xrange(rch):
       for iq in xnq:
           datregt.append(zeros((npix_per_q[iq],chn),dtype=float32))
       datreg.append(datregt)
       datregt=[]
   del datregt
   oneq=[]
   for iq in xnq:
       oneq.append(ones((1,npix_per_q[iq])))

   rcr=chn+chn2*ceil(log(nfile/chn)/log(2))
   corf=zeros((nq,rcr),dtype=float32)
   sl=zeros((nq,rcr),dtype=float32)
   sr=zeros((nq,rcr),dtype=float32)
   sll=[]
   srr=[]
   sst=[]

   for ir in xrange(rch):
      sll.append(zeros((nq,chn),dtype=float32))
      srr.append(zeros((nq,chn),dtype=float32))
      sst.append(arange(nq)*0.0) 

   #END of declaring and initializing variables####
   n=0
   nc=0
   lind=npix_per_q
   nnfile=nfile-1
   while n<nnfile:
       nc=n+1
       if (nc%chn==0 and iproc==0):
          if plot!='no': 
              quplot.put([corf[[0,-1],:],sr[[0,-1],:],sl[[0,-1],:]])
       correlator(0,quc.get())
       n+=1   
   #END OF MAIN LOOP
   quc.close()
   tcalc=time()-tcalc
   quce.put([corf,sl,sr,tcalc])
