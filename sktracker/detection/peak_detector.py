def peak_detector(data_iterator,
                  metadata,
                  parameters=None,
                  parallel=True,
                  verbose=True,
                  show_progress=False):
    """Gaussian peak detection described in Segré et al. Nature Methods, (2008).

    Parameters
    ----------
    data_iterator : python iterator
        To iterate over data.
    metadata : dict
        Metadata to scale detected peaks

    shape_label : tuple (default: ('t', 'z', 'x', 'y'))
        Label for each array dimension. Used in returned peaks array.
    parallel : bool (default: True)
        Used several processes at once (greatly imrpove speed on multi core machines).
    show_progress : bool (default: False)
        Print progress bar during detection.
    verbose : bool (default: True)
        Display informations during detection.
    **detection_parameters : dict
        dict which contains gaussian detection algorithm parameters:
            - w_s: int, optional
                Width of the sliding window over which the hypothesis ratio
                is computed :math:`w_s` in the article. It should be wide enough
                to contain some background to allow a proper noise evaluation.
            - peak_radius: float, optional
                Typical radius of the peaks to detect. It must be higher than one
                (as peaks less that a pixel wide would yield bogus results
            - threshold: float, optional
                Criterium for a positive detection (i.e. the null hypothesis is false).
                Corresponds to the :mat:`\chi^2` parameter in the Constant False
                Alarm Rate section of the article supplementary text (p. 12).
                A higher `threshold` corresponds to a more stringent test.
                According to the authors, this parameters needs to be adjusted
                once for a given data set.
            - max_peaks : int, optional
                Deflation loop will stop if detected peaks is higher than max_peaks.

    Returns
    -------
    `pandas.DataFrame` array is returned. Each `stacks` lines contains contains
    peaks detected for each frames. Multi dimensional informations are present in
    columns.
    """
