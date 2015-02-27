
from collections import namedtuple
from contextlib import contextmanager

from pygenie.lib import *
from pygenie.lib.params._par_type import Parameter

class MeasurementTime(object):

    def __init__(self, live, real):
        self.live = live
        self.real = real

    def serialize(self):
        return {
            "live": self.live,
            "real": self.real
        }

class EnergycalibrationManager(object):

    POLYNOMIAL_CALIBRATION = b"POLY"
    """
    Value of ``EnergyCalibration.TYPE`` parameter which signifies
    polynomial calibration (that we are able to serialize.
    """

    def __init__(self, pygenie):
        super().__init__()
        self.pygenie = pygenie

    @property
    def type(self):
        """
        Calibration type used.
        """
        return self.pygenie.get_param(EnergyCalibration.TYPE)

    @property
    def unit(self):
        """
        Unit (eg. kev) in to which energy is calibrated
        """
        return self.pygenie.get_param(EnergyCalibration.UNIT)

    def get_calibration_coefficients(self):
        """
        If this uses polynomial calibration will return
        numpy array containing polynomial coefficients.
        This polynomial is in format compatible with ``np.polyval``
        call.
        """
        return get_calibration(self.pygenie.dsc)

    def serialize(self):
        serialized_dict = {
            "type" : self.type,
            "unit": self.unit,
        }
        if serialized_dict['type'] == self.POLYNOMIAL_CALIBRATION:
            serialized_dict.update({
                "energy_calibration": list(self.get_calibration_coefficients())
            })
        return serialized_dict

@contextmanager
def open_cam_source(file_name, source_type, open_mode=OpenFlags.ReadOnly, verify_hardware=False, shell_ptr=b""):
    pygenie = PYGenieObj()
    try:
        pygenie.open(file_name, source_type, open_mode, verify_hardware, shell_ptr)
        yield pygenie
    finally:
        pygenie.close()

class PYGenieObj(object):

    ABSOLUTE_TIME_PARAMETERS = {
        "X_ASTIME"
    }

    def __init__(self, autoconvert_absolute_dates=False):
        """

        :param bool autoconvert_absolute_dates: If set to True this object will attempt
                                                to automaticall convert datetime
                                                parameters that
                                                contain absolute intervals to datetime
                                                objects.
        :return:
        """
        super().__init__()
        self.dsc = None
        self.autoconvert_absolute_dates = autoconvert_absolute_dates

    def open(self, file_name, source_type, open_mode=OpenFlags.ReadOnly, verify_hardware=False, shell_ptr=b""):
        """
        Creates and opens a data source.
        Parameters are just like on SadOpenDataSource function.

        :param str file_name: It can be str, bytes or pathlib.Path object. File or datasource to open.
        :param SourceType esource_type: A source type. Specific types depend on the
                                        Library used. Example valid values are:
                                        ``SourceType.NativeSpect`` or ``SourceType.Detector``.
                                        All other constants from header file are accepted,
                                        and are avilable from SourceType without
                                        ``CIF_`` prefix.
        :param OpenFlags open_mode: Open method all constants prefixed with ``ACC_`` are avilable
                                    from this enum. Example valid value
                                    ``SourceType.ReadOnly``.
        :param bool verify_hardware: See  SadOpenDataSource.
        :param bytes shell_ptr:
        :return: None
        """
        self.dsc = create_vdm_connection()
        open_source(self.dsc, file_name, source_type, open_mode, verify_hardware, shell_ptr)


    def close(self):
        """
        Closes the VDM connection. Called automatically on deletion of this object.
        """
        if self.dsc is not None:
            self.flush()
            delete_vdm_connection(self.dsc)
            self.dsc = None

    def flush(self):
        flush(self.dsc)

    def convert_cam_interval_to_datetime(self, interval):
        return convert_interval_to_absolute_date(interval)

    def get_param(self, param, entry=1, record=1):
        """

        Gets a parameter.

        Following type conversions are used:

        * T parameters are converted to byte instances.
        * F parameters are converted to floats.
        * X parameters (datetime) are converted to floats, to convert them to
          datetime use :meth:`convert_cam_interval_to_datetime` (or select:
          ``autoconvert_absolute_dates`` on ``__init__``.)
        * L parameters are converted to int instances.


        :param Parameter param: Parameter to get. This can be either a string (with name
                                of the constant). Or a Parameter instance.
                                Parameters can be obtained from: a PARAM_GENERATOR instance
                                (for example ``PARAM_GENERATOR.T_STITLE``), or from
                                various enums that contain human-readable parameter
                                names, see: :class:`EnergyCalibration`,
                                :class:`SampleDescription`, :class:`ParamAlias`.
        :param int entry: As defined in SadGetParam (yes when I use this form, it means I have no clue)
        :param int record: As defined in SadGetParam

        :return: Parameter value
        """
        value =  get_parameter(self.dsc, param, entry, record)
        if self.autoconvert_absolute_dates and param.name in self.ABSOLUTE_TIME_PARAMETERS:
            value = self.convert_cam_interval_to_datetime(value)
        return value

    def set_param(self, param, value,  entry=1, record=1):
        """
        Sets a parameter. See :meth:`get_param` for description of parameters.

        Data is flushed to the data soure when this object is closed, deleted
        or when call to :meth:`flush` is issued.

        :param value: Value to be set
        """
        set_parameter(self.dsc, param, value, entry, record)

    def get_spectrum(self, channel_from=None, channel_to=None, spectrum_type=SpectrumType.LONG_DATA):
        """
        Returns spectrum from data source as a numpy array.

        Depending on value of ``spectrum_type``,
        either a numpy array containing dtype=np.uint32 (default) entries, or
        a numpy array containing dtype=np.float32.
        :param int channel_from:
        :param int channel_to:
        :param SpectrumType spectrum_type:

        :return: Numpy array containing spectrum channels.
        """
        if channel_from is None:
            channel_from = 0
        if channel_to is None:
            channel_to = self.channel_count
        return get_spectrum(self.dsc, channel_from, channel_to, spectrum_type)

    def __getitem__(self, item):
        """
        Equicalent to:  ``self.get_spectrum(item.start, item.stop)
        :param slice item:
        """
        if not isinstance(item, slice):
            raise ValueError("Pass a slice object")

        if item.step is not None:
            raise ValueError("Step is not supported")
        return self.get_spectrum(item.start, item.stop)

    @property
    def channel_count(self):
        """
        Return number of channels in the detector
        :return:
        """
        return self.get_param(ParamAlias.NUMBER_OF_CHANNELS)

    @property
    def measurement_time(self):
        """
        Returns tuple containing both live and real measurement times.
        """
        return MeasurementTime(
            self.get_param(ParamAlias.TIME_LIVE),
            self.get_param(ParamAlias.TIME_REAL),
        )

    @property
    def title(self):
        return self.get_param(SampleDescription.TITLE)

    @title.setter
    def title(self, value):
        if isinstance(value, str):
            value = value.encode('ascii')
        self.set_param(SampleDescription.TITLE, value)
        self.flush() # Since getter would still return stale value

    @property
    def sample_id(self):
        return self.get_param(SampleDescription.ID)

    @sample_id.setter
    def sample_id(self, value):
        if isinstance(value, str):
            value = value.encode('ascii')
        self.set_param(SampleDescription.ID, value)
        self.flush() # Since getter would still return stale value

    @property
    def energy_calibration(self):
        return EnergycalibrationManager(self)

    def get_description(self, part=0):
        """
        CAM files can contain four parts of description (each 64 bytes long).
        This returns each part
        :param int part: Zero indexed part index
        """
        return self.get_param(SampleDescription.DESCRIPTION[part+1])

    def set_description(self, value, part=0):
        """
        Sets description part.
        """
        if isinstance(value, str):
            value = value.encode('ascii')
        self.set_param(SampleDescription.DESCRIPTION[part+1], value)

    @property
    def measurement_start_time(self):
        """
        Datetime instance containing time when measurement was started.
        """
        return self.convert_cam_interval_to_datetime(
            get_parameter(self.dsc, SampleDescription.MEASURE_START_TIME)
        )

    def serialize(self, convert_absolute_datetime_params=False, additional_metadata = None):
        """
        Returns a dictionary (that can be immediately serialized to JSON)

        (Format should be self-evident).

        :param bool convert_absolute_datetime_params:  if true --- we will convert absolute datetimes and present them
                                                       as strings.

        :return: dict
        """

        additional_metadata = {} if additional_metadata is None else additional_metadata
        # param_list = [] if param_list is None else param_list

        serialized_dict = {
            "metadata": additional_metadata,
            "channel_count": self.channel_count,
            "measurment_start_time": self.measurement_start_time,
            "measurement_time" : self.measurement_time,
            "spectrum": self[:],
            "sample_id": self.sample_id,
            "title": self.title,
            "description": [],
            "energy_calibration": self.energy_calibration.serialize(),
            "params": []
        }

        # for param_list

        for ii in range(4):
            serialized_dict['description'].append(self.get_description(ii))

        return serialized_dict

    def __del__(self):
        self.close()



