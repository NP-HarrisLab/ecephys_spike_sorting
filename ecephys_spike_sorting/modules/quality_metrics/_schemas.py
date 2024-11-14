from marshmallow import INCLUDE, Schema
from marshmallow.fields import Boolean, Float, Int, Nested, String

from ...common.schemas import (
    ClusterMetricsFile,
    Directories,
    EphysParams,
    WaveformMetricsFile,
)


class QualityMetricsParams(Schema):
    class Meta:
        unknown = INCLUDE

    isi_threshold = Float(
        required=False,
        missing=0.0015,
        help="Maximum time (in seconds) for ISI violation",
    )
    min_isi = Float(
        required=False, missing=0.00, help="Minimum time (in seconds) for ISI violation"
    )
    tbin_sec = Float(
        required=False,
        missing=0.001,
        help="time bin in seconds for ccg in contam_rate calculation",
    )
    max_radius_um = Int(
        required=False,
        missing=68,
        help="Maximum radius for computing PC metrics, in um",
    )
    max_spikes_for_unit = Int(
        required=False,
        missing=500,
        help="Number of spikes to subsample for computing PC metrics",
    )
    max_spikes_for_nn = Int(
        required=False,
        missing=10000,
        help="Further subsampling for NearestNeighbor calculation",
    )
    n_neighbors = Int(
        required=False,
        missing=4,
        help="Number of neighbors to use for NearestNeighbor calculation",
    )
    n_silhouette = Int(
        required=False,
        missing=10000,
        help="Number of spikes to use for calculating silhouette score",
    )

    drift_metrics_min_spikes_per_interval = Int(
        required=False, missing=10, help="Minimum number of spikes for computing depth"
    )
    drift_metrics_interval_s = Float(
        required=False,
        missing=100,
        help="Interval length is seconds for computing spike depth",
    )
    include_pcs = Boolean(
        required=False,
        missing=True,
        help="Set to false if features were not saved with Phy output",
    )
    include_ibl = Boolean(
        required=False,
        missing=True,
        help="Set to false if features were not saved with Phy output",
    )


class InputParameters(Schema):
    class Meta:
        unknown = INCLUDE

    quality_metrics_params = Nested(QualityMetricsParams)
    ephys_params = Nested(EphysParams)
    directories = Nested(Directories)
    waveform_metrics = Nested(WaveformMetricsFile)
    cluster_metrics = Nested(ClusterMetricsFile)


class OutputSchema(Schema):
    class Meta:
        unknown = INCLUDE

    input_parameters = Nested(
        InputParameters,
        description=("Input parameters the module " "was run with"),
        required=False,
    )


class OutputParameters(OutputSchema):
    class Meta:
        unknown = INCLUDE

    execution_time = Float()
    quality_metrics_output_file = String()


class QualityMetricsSchema(Schema):
    class Meta:
        unknown = INCLUDE

    input = Nested(InputParameters, required=True)
    output = Nested(OutputParameters, required=True)
