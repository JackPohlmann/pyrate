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
            dg = np.swapaxes(dg, 1, -1)
            x_arr = np.array([1-step1, step1])
            y_arr = np.array([1-step2, step2])
            return np.dot(x_arr, np.dot(dg, y_arr))

    @classmethod
    def linear(cls, step, val1, val2):
        """Linearly interpolate."""
        return val1 + (val2-val1) * step


class InterpGrid():
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
        # memoize
        self._memoized = {}
        return

    def get(self, index1, index2):
        """
        Returns value at specified location [index1,index2]. If both index1 and
        index2 are integers, then dataGrid[index1,index2] is returned.
        Otherwise the value is interpolated using the specified interpolator.
        """
        key = '_'.join([str(index1),str(index2)])
        try:
            out = self._memoized[key]
        except KeyError:
            if type(index1)==type(index2)==int:
                out = self._dataGrid[index1, index2]
            else:
                out = self._interpolator(index1, index2, self._dataGrid)
            self._memoized[key] = out
        return out


class SAIG(InterpGrid):
    """
    Store data with ability to interpolate over a grid indexed by solid angles.

    Parameters
    ----------
    dataGrid : array_like
        2D+ data array in which the first two dimensions are indices and all
        trailing dimensions correspond to data.
    zen_angle_range : list or tuple
        Lower and upper bounds for zenith viewing angles corresponding to the
        second dimension of dataGrid.
    az_angle_range : list or tuple
        Lower and upper bounds for azimuth viewing angles corresponding to the
        first dimension of dataGrid.
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
            self, dataGrid, zen_angle_range, az_angle_range,
            radians=False, interpMode='bilinear'):
        """Initialize solid angle interpolator object."""
        try:
            if not len(az_angle_range)==len(zen_angle_range)==2:
                raise ValueError("Incorrect range dimensions.")
        except TypeError:
            raise TypeError("Incorrect type for angle ranges. Must be list-like.")
        if radians:
            az_angle_range = tuple(map(degrees, az_angle_range))
            zen_angle_range = tuple(map(degrees, zen_angle_range))
            warnings.warn("Input angle ranges are in radians. \
                Object methods expect arguments in degrees.")

        super().__init__(dataGrid, interpMode=interpMode)
        
        self.az_angle_range = tuple(sorted(az_angle_range))
        self.zen_angle_range = tuple(sorted(zen_angle_range))
        
        # Parameters to convert angles to indices
        zen_angle_anchor = self.zen_angle_range[0]
        zen_angle_scale = \
            (self.zen_angle_range[1] - self.zen_angle_range[0]) / (self.dims[0] - 1)
        az_angle_anchor = self.az_angle_range[0]
        az_angle_scale = \
            (self.az_angle_range[1] - self.az_angle_range[0]) / (self.dims[1] - 1)

        self._anchor_scale = (
                (zen_angle_anchor, zen_angle_scale),
                (az_angle_anchor, az_angle_scale)
            )
        return

    def _convert_angle_index(self, zen_angle, az_angle):
        """Convert angles to indices."""
        zanch, zscale = self._anchor_scale[0]
        aanch, ascale = self._anchor_scale[1]
        index1 = (zen_angle - zanch) / zscale
        index2 = (az_angle - aanch) / ascale
        return index1, index2

    def get(self, zen_angle, az_angle):
        """Returns value at [index1,index2] inerpolated onto dataGrid.

        index1 and index2 correspond to the angle and zen_angle, respectively,
        and must be in degrees.
        """
        index1, index2 = self._convert_angle_index(zen_angle, az_angle)
        return super().get(index1, index2)


class dummySAIG(SAIG):
    """Dummy SAIG class when the output is constant."""
    def __init__(self, function):
        self._function = function
        self._memoized = {}
        return
    def get(self, zen_angle, az_angle):
        key = '_'.join([str(zen_angle),str(az_angle)])
        try:
            out = self._memoized[key]
        except KeyError:
            out = self._function(zen_angle, az_angle)
            self._memoized[key] = out
        return out
