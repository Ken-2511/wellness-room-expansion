import numpy as np
import colour

def RGB2CCT(RGB):
    # Assuming sRGB encoded colour values.
    # RGB = np.array([255.0, 235.0, 12.0])

    # Conversion to tristimulus values.
    XYZ = colour.sRGB_to_XYZ(RGB / 255)

    # Conversion to chromaticity coordinates.
    xy = colour.XYZ_to_xy(XYZ)

    # Conversion to correlated colour temperature in K.
    CCT = colour.xy_to_CCT(xy, 'hernandez1999')
    print(CCT)

# 3557.10272422
