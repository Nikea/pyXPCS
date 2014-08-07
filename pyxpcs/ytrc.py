#function to save and read compressed edf for TRC
import EdfFile
from numpy import *

def read(filename):
    trcfile=EdfFile.EdfFile(filename)
    trcheader=trcfile.GetHeader(0)
    trcdata=asfarray(trcfile.GetData(0))
    trcdata=trcdata/2**16*(float(trcheader['MaxValue'])-float(trcheader['MinValue']))+float(trcheader['MinValue'])
    return trcdata


def write(filename,trcdata):
    trcfile=EdfFile.EdfFile(filename)
    maxtrc=trcdata.max() 
    mintrc=trcdata.min()
    trcdata=(trcdata-mintrc)/(maxtrc-mintrc)*2**16
    trcfile.WriteImage({'MaxValue':maxtrc,'MinValue':mintrc},trcdata,0,DataType='UnsignedShort')

#######binning the TRC##########
def rebin( a, newshape ):
    '''Rebin an array to a new shape.
    '''
    assert len(a.shape) == len(newshape)
    slices = [ slice(0,old, float(old)/new) for old,new in zip(a.shape,newshape)]
    coordinates = mgrid[slices]
    indices = coordinates.astype('i')   #choose the biggest smaller integer index
    return a[tuple(indices)]
#################################


