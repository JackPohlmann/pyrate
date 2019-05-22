"""
SAIG

Class module for Solid Angle Interpolation Grid.

Make sure to grab any dependent abstractions and move them here.

Dev Notes:
-   RTTOV typical max zen_angle is 75deg (85 for some; check IASI coeff header)
    - v9 predictors *can* get up to 85deg
    - Note that extended Simulator classes should handle their own limits
-   Uses 4-pt. bilinear interpolation:
    (https://en.wikipedia.org/wiki/Bilinear_interpolation)
-   Consider using scipy.interpolate.RectBivariateSpline

+   Need to scale 

"""

import abc
import numpy as np
from math import degrees, ceil
import warnings


class interpolators:
    """Class containing interpolators."""
    @classmethod
    def fromKey(cls, key=None):
        """Returns an interpolator using a string key."""
        # Add new interpolators to this dict.
        # Could definitely be implemented better.
        interpDict = {
            'bilinear' : interpolators.bilinear
        }
        if not key:
            return interpDict
        else:
            try:
                return interpDict[key]
            except KeyError:
                raise KeyError("Unknown interpolator. \
                    Supported interpolators: {}".format(list(interpDict.keys())))

    @classmethod
    def bilinear(cls, index1, index2, dataGrid):
        """Bilinearly interpolates a value at [index1,index2] onto dataGrid."""
        dimx, dimy = dataGrid.shape[:2]
        if not (0<=index1<=dimx-1 or 0<=index2<=dimy-1):
            raise IndexError("Extrapolation not supported.")
        ix = int(index1)
        iy = int(index2)
        step1 = index1%1
        step2 = index2%2
        if (ix == index1 and iy == index2):
            return dataGrid[ix,iy]
        elif (ix == index1 or iy == index2):
            val1 = dataGrid[ix, iy]
            val2 = dataGrid[ix+ceil(step1), iy+ceil(step2)]
            return interpolators.linear(max(step1,step2), val1, val2)
        else:
            dg = dataGrid[ix:ix+2, iy:iy+2]
            x_arr = np.array([1-step1, step1])
            y_arr = np.array([1-step2, step2])
            return np.dot(x_arr, np.dot(dg, y_arr))

    @classmethod
    def linear(cls, step, val1, val2):
        """Linearly interpolate."""
        return val1 + (val2-val1) * step


class DummySAIG(abc.ABC):
    """Dummy Saig class for simple returns."""
    @abc.abstractmethod
    def get(self, arg1, arg2):
        pass


class AbstractInterpGrid(abc.ABC):
    """Abstract 2D-grid interpolation class."""
    def __init__(self, dataGrid, interpolator):
        try:
            if len(dataGrid.shape)<2 or 1 in dataGrid.shape[:2]:
                raise ValueError("Must have 2D+ dataGrid.")
        except TypeError:
            raise TypeError("dataGrid must be array-like.")
        if not callable(interpolator):
            raise TypeError("interpolator must be a function.")
            
        self._dataGrid = dataGrid
        self._interpolator = interpolator

        self.dims = self._dataGrid.shape[:2]
        try:
            self.depth = self._dataGrid.shape[3]
        except IndexError:
            self.depth = 1
        return

    @abc.abstractmethod
    def get(self, index1, index2):
        """
        Returns value at specified location [index1,index2]. If both index1 and
        index2 are integers, then dataGrid[index1,index2] is returned.
        Otherwise the value is interpolated using the specified interpolator.
        """
        if type(index1) not in (int,float) or type(index2) not in (int,float):
            raise TypeError("Indices must be int or float.")
        elif type(index1)==type(index2)==int:
            return self._dataGrid[index1, index2]
        else:
            return self._interpolator(index1, index2, self._dataGrid)


class InterpGrid(AbstractInterpGrid):
    """
    Interpolate over a regular 2D grid.

    Parameters
    ----------
    dataGrid : array_like
        2D+ data array in which the first two dimensions are indices and all
        trailing dimensions correspond to data.
    interpMode : str, optional
        String indicating interpolation mode.
        Current accepted modes are: 'bilinear'.
        Default is 'bilinear'.

    Methods
    -------
    get
    """
    def __init__(self, dataGrid, interpMode='bilinear'):
        interpolator = interpolators.fromKey(interpMode)
        super().__init__(dataGrid, interpolator)
        return
    def get(self, index1, index2):
        """Return a value interpolated onto dataGrid at [index1, index2]."""
        return super().get(index1, index2)


class SAIG(InterpGrid):
    """
    Store data with ability to interpolate over a grid indexed by solid angles.

    Parameters
    ----------
    dataGrid : array_like
        2D+ data array in which the first two dimensions are indices and all
        trailing dimensions correspond to data.
    anglerange : list or tuple
        Lower and upper bounds for viewing angles corresponding to the first
        dimension of dataGrid.
    zenanglerange : list or tuple
        Lower and upper bounds for zenith viewing angles corresponding to the
        second dimension of dataGrid.
    radians : bool, optional
        Indicates if the angle ranges are in radians. If True, converts input 
        ranges to degrees.
        Default is False.
    interpMode : string, optional
        Sets the internal interpolation mode according to keys in the dict
        returned by interpolators.fromKey()

    Methods
    -------
    get
    """

    def __init__(
            self, dataGrid, angle_range, zen_angle_range,
            radians=False, interpMode='bilinear'):
        """Initialize solid angle interpolator object."""
        try:
            if not len(angle_range)==len(zen_angle_range)==2:
                raise ValueError("Incorrect range dimensions.")
        except TypeError:
            raise TypeError("Incorrect type for angle ranges. Must be list-like.")
        if radians:
            angle_range = tuple(map(degrees, angle_range))
            zen_angle_range = tuple(map(degrees, zen_angle_range))
            warnings.warn("Input angle ranges are in radians. \
                Object methods expect arguments in degrees.")

        super().__init__(dataGrid, interpMode=interpMode)
        
        self.angle_range = tuple(sorted(angle_range))
        self.zen_angle_range = tuple(sorted(zen_angle_range))
        
        # Parameters to convert angles to indices
        angle_anchor = self.angle_range[0]
        angle_scale = \
            (self.angle_range[1] - self.angle_range[0]) / (self.dims[0] - 1)
        zen_angle_anchor = self.zen_angle_range[0]
        zen_angle_scale = \
            (self.zen_angle_range[1] - self.zen_angle_range[0]) / (self.dims[1] - 1)

        self._anchor_scale = (
                (angle_anchor, angle_scale),
                (zen_angle_anchor, zen_angle_scale)
            )
        return

    def _convert_angle_index(self, angle, zen_angle):
        """Convert angles to indices."""
        aanch, ascale = self._anchor_scale[0]
        zanch, zscale = self._anchor_scale[1]
        index1 = (angle - aanch) / ascale
        index2 = (zen_angle - zanch) / zscale
        return index1, index2

    def get(self, angle, zen_angle):
        """Returns value at [index1,index2] inerpolated onto dataGrid.

        index1 and index2 correspond to the angle and zen_angle, respectively,
        and must be in degrees.
        """
        index1, index2 = self._convert_angle_index(angle, zen_angle)
        return super().get(index1, index2)

    @classmethod
    def combine(cls, saiglist, angle_range=None, zen_angle_range=None):
        """
        Combine an arbitrary list of SAIGs into a single SAIG.

        Parameters
        ----------
        saiglist : list of SAIGs
            List of SAIGs to combine. Order is irrelevant.
        angle_range : list, optional
            List of min and max angle (order irrelevant) over which to 
            combine the SAIGs.
            Default is calculated by the lowest and highest values in 
            the SAIG list.
        zen_angle_range : list, optional
            List of min and max zenith angle (order irrelevant) over which to
            combine the SAIGs.
            Default is calculated by the lowest and highest values in 
            the SAIG list.

        Notes
        -----
        Uses linear average of retrieved radiance vectors. This does not scale
        or process the vectors in any way.
        """
        ascale = []
        zscale = []
        depth_test = saiglist[0].depth
        amin, amax = saiglist[0].angle_range
        zmin, zmax = saiglist[0].zen_angle_range
        # Find the highest resolutions and ensure compatibility
        for saig in saiglist:
            assert saig.depth == depth_test, "Incompatible SAIG data."
            tmp = saig._anchor_scale
            tamin, tamax = saig.angle_range
            tzmin, tzmax = saig.zen_angle_range
            amin = min(amin,tamin)
            amax = max(amax,tamax)
            zmin = min(zmin,tzmin)
            zmax = max(zmax,tzmax)
            ascale.append(tmp[0][1])
            zscale.append(tmp[1][1])
        ascale = min(ascale)
        zscale = min(zscale)
        # Setup for new SAIG
        if angle_range:
            # If the min [zen]angle is greater than the min range, it is changed
            angler = list(sorted(angle_range))
            angler[0] = max(angler[0],amin)
        else:
            angler = [amin,amax]
        if zen_angle_range:
            zangler = list(sorted(zen_angle_range))
            zangler[0] = max(zangler[0],zmin)
        else:
            zangler = [zmin,zmax]
        if angler[0]>amax or zangler[0]>zmax:
            raise IndexError("Incompatible combination instructions. \
                Please check the input ranges against desired SAIGs.")
        dim1 = ceil((angler[1]-angler[0]) / ascale)
        dim2 = ceil((zangler[1]-zangler[0]) / zscale)
        ai2a = lambda i: (i * ascale) + angler[0]
        zi2a = lambda i: (i * zscale) + zangler[0]
        angler[1] = ai2a(dim1-1)
        zangler[1] = zi2a(dim2-1)
        # Ensure that the angle ranges are valid. Tweak them if not.
        # This will be skipped nicely if the ranges are defaulted
        speak_up_a = False
        while angler[1] > amax:
            speak_up_a = True
            dim1 -= 1
            angler[1] = ai2a(dim1-1)
        if speak_up_a:
            warnings.warn("Angle range maximum changed to {:1.2f}...degrees.".format(angler[1]))
        speak_up_z = False
        while zangler[1] > zmax:
            speak_up_z = True
            dim2 -= 1
            zangler[1] = zi2a(dim2-1)
        if speak_up_z:
            warnings.warn("Zenith angle range maximum changed to {:1.2f}...degrees.".format(zangler[1]))
        # Compute the output data
        dataGrid = np.empty((dim1,dim2,depth_test))
        for ii in range(dim1):
            for jj in range(dim2):
                count = 0
                tmp = np.zeros(depth_test)
                angle = ai2a(ii)
                zangle = zi2a(ii)
                for saig in saiglist:
                    try:
                        tmp += saig.get(angle,zangle)
                        count += 1
                    except IndexError:
                        continue
                dataGrid[ii,jj] = tmp / count
        return SAIG(dataGrid, angler, zangler)