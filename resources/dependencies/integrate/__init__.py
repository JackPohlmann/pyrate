import multiprocessing as mp
import numpy as np
from scipy.integrate import dblquad

cucumber = None

def pickled(*args, **kwargs):
    return cucumber(*args, **kwargs)

def threaded_dblquad(iterations, *dblquad_args, threads=None):
    """Use scipy.integrate.dblquad as a backend along with the python
    multiprocessing module in order to speed up computation.
    
    Args:
    ==================== 
    iterations
        Number of iterations to run.

    KW Args:
    ==================== 
    threads: optional
        Default=None. If None, uses threads=MAX_THREADS-1 where MAX_THREADS is
        the system's maximum number of threads as specified by the 
        multiprocessing module.
    """
    # Determine threads and init the pool
    max_threads = mp.cpu_count() - 1
    threads = max_threads if not threads else threads
    threads = threads if threads <= max_threads else max_threads
    pool = mp.Pool(processes=threads)
    print('Performing double integration using {} threads...'.format(threads))
    # Init output array
    output = np.empty((iterations,))
    # Chunk and remainder sizes
    chunk = iterations//threads
    remain = iterations%threads
    # Main function
    def main(buf):
        buf *= chunk
        dout = np.empty((chunk,))
        for ii in range(chunk):
            dout[buf+ii] = dblquad(*dblquad_args, args=(buf+ii,))[0]
        return dout
    # Run the pool
    global cucumber
    cucumber = main
    chkd_out = pool.map(pickled, np.arange(threads))
    # Set values to the output
    for sec in range(threads):
        start = sec * chunk
        stop = (sec + 1) * chunk
        output[start:stop] = chkd_out[sec]
    # Clean up the remaining pieces
    rem_buf = chunk*threads
    for ii in range(remain):
        output[rem_buf+ii] = dblquad(*dblquad_args, args=(rem_buf+ii,))[0]
    # Should be finished...
    return output
    
    
