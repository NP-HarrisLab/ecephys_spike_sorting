import glob
import os
import warnings

import numpy as np
import pandas as pd
import xarray as xr

from ...common.epoch import Epoch
from ...common.utils import printProgressBar
from .waveform_metrics import calculate_waveform_metrics_from_avg


def metrics_from_file(
    mean_waveform_fullpath,
    snr_fullpath,
    clus_fullpath,
    spike_times,
    spike_clusters,
    templates,
    channel_map,
    bit_volts,
    sample_rate,
    site_spacing,
    w_inv,
    site_x,
    site_y,
    params,
):
    """
    Load C_waves output and call waveform_metrics for each cluster
    Does not support epochs, since waveforms are already averaged

    Inputs:
    -------
    mean_wavefrom_fullpath: path to the mean waveforms npy file
    snr_fullpath: path to snr npy file
    clus_fullpath: path to clus_Table (contains peak channels)
    spike_times : spike times (in samples)
    spike_clusters : cluster IDs for each spike time []
    clusterIDs : all unique cluster ids
    cluster_quality : 'noise' or 'good'
    sample_rate : Hz
    site_spacing : um (now unused)
    w_inv : inverse of the whitening matrix used in KS2
    site_x, site_y: x and y coordinates of all channels, in um

    Outputs:
    -------
    mean_waveforms : numpy array with dims :
     - 1 : clusterID
     - 2 : epochs
     - 3 : mean (0) or std (1)
     - 4 : channels
     - 5 : samples
    spike_count : numpy array with dims :
     - 1 : clusterID
     - 2 : epoch (last is entire dataset)
    dimCoords : list of coordinates for each dimension
    dimLabels : list of labels for each dimension
    metrics : DataFrame with waveform metrics

    Parameters:
    ----------
    samples_per_spike : number of samples in extracted spikes
    pre_samples : number of samples prior to peak
    num_epochs : number of epochs to calculate mean waveforms
    spikes_per_epoch : max number of spikes to generate average for epoch

    """

    # #############################################

    samples_per_spike = params["samples_per_spike"]
    pre_samples = params["pre_samples"]
    spikes_per_epoch = params["spikes_per_epoch"]
    upsampling_factor = params["upsampling_factor"]
    spread_threshold = params["spread_threshold"]
    site_range = params["site_range"]
    nAP = params["nAP"]

    # #############################################

    metrics = pd.DataFrame()

    cluster_ids = np.arange(np.max(spike_clusters) + 1)
    total_units = len(cluster_ids)

    mean_waveforms = np.load(mean_waveform_fullpath)
    snr_array = np.load(snr_fullpath)
    clus_table = np.load(clus_fullpath)
    peak_channels = clus_table[:, 1]

    # peak channels were estimated from the unwhitened templates, but the
    # actual peak channel is sometimes offset (due to drift, or other effects)
    # For any unit that has spikes and a calculable mean waveform, update the
    # estimated peak channel with the measured one.

    if mean_waveforms.shape[1] > nAP:
        # remove digital channel
        mean_waveforms = mean_waveforms[:, 0:nAP, :]
    vpp_allchan = np.amax(mean_waveforms, 2) - np.amin(mean_waveforms, 2)
    vpp_val = np.amax(vpp_allchan, 1)
    meas_pkchan = np.argmax(vpp_allchan, 1)
    vpp_nonzero = vpp_val > 0
    peak_channels[vpp_nonzero] = meas_pkchan[vpp_nonzero]

    for cluster_idx, cluster_id in enumerate(cluster_ids):

        printProgressBar(cluster_idx + 1, total_units)

        snr = snr_array[cluster_idx, 0]
        nSpike = snr_array[cluster_idx, 1]
        # if at least one spike, calculate metrics and concatenate to existing dataframe
        if nSpike > 0:
            metrics = pd.concat(
                [
                    metrics,
                    calculate_waveform_metrics_from_avg(
                        mean_waveforms[cluster_idx, :],
                        snr,
                        cluster_id,
                        peak_channels[cluster_idx],
                        channel_map,
                        sample_rate,
                        upsampling_factor,
                        spread_threshold,
                        site_range,
                        site_x,
                        site_y,
                    ),
                ]
            )

    return metrics


def generateDimLabels(
    good_clusters, num_epochs, pre_samples, total_samples, num_channels, sample_rate
):
    """Generate dimension labels and coordinates for the xarray"""

    dimCoords = []
    dimLabels = []

    dimCoords.append(good_clusters)
    dimLabels.append("clusterID")

    dim1Coords = [str(i) for i in range(0, num_epochs)]
    dim1Coords.append("all")
    dimCoords.append(dim1Coords)
    dimLabels.append("epoch")

    dimCoords.append(["mean", "std"])
    dimLabels.append("mean or std")

    dimCoords.append(range(0, num_channels))
    dimLabels.append("channel")

    dimCoords.append(
        np.linspace(-pre_samples, total_samples - pre_samples, total_samples)
        / sample_rate
    )
    dimLabels.append("time")

    return dimCoords, dimLabels


def writeDataAsXarray(mean_waveforms, spike_count, dimCoords, dimLabels, output_file):
    """Saves mean waveforms as xarray"""

    waveform_array = xr.DataArray(mean_waveforms, coords=dimCoords, dims=dimLabels)

    spike_count_array = xr.DataArray(
        spike_count, coords=dimCoords[:2], dims=dimLabels[:2]
    )

    ds = xr.Dataset({"waveforms": waveform_array, "spike_count": spike_count_array})

    ds.to_netcdf(output_file)


def writeDataAsNpy(waveforms, output_file):
    """Saves mean waveforms as xarray"""

    mean_waveforms = waveforms[:, -1, 0, :, :]  # extract overall mean

    np.save(output_file, mean_waveforms)
