import pyrate.core
import pyrate.core.keys as pk


# Keys
pix_key = pk.pix_key


def run():
    print('Finalizing pixel...')
    pyrate.core.HDSTRUCT['last'].append(__name__)
    # Grab the data
    bg = pyrate.core.HDSTRUCT[pk.bg_key]
    targ = pyrate.core.HDSTRUCT[pk.targ_key]
    proj = pyrate.core.HDSTRUCT[pk.proj_key]
    upwell = pyrate.core.HDSTRUCT[pk.up_key]
    tau = pyrate.core.HDSTRUCT[pk.tau_key]

    # Make the new SAIG
    def pixelOutput(zen, az):
        coverage = proj.get(zen,az)
        emitted = targ.get(zen,az) * coverage + bg.get(zen,az) * (1-coverage)
        return tau.get(zen,az) * emitted + upwell.get(zen,az)
    pixelSAIG = pyrate.core.saig.dummySAIG(pixelOutput)
    pyrate.core.HDSTRUCT[pix_key] = pixelSAIG

    return
