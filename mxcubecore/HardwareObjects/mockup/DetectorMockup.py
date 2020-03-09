from HardwareRepository.HardwareObjects.abstract.AbstractDetector import (
    AbstractDetector,
)


class DetectorMockup(AbstractDetector):
    """
    Descript. : Detector class. Contains all information about detector
                the states are 'OK', and 'BAD'
                the status is busy, exposing, ready, etc.
                the physical property is RH for pilatus, P for rayonix
    """

    def __init__(self, name):
        """
        Descript. :
        """
        AbstractDetector.__init__(self, name)

    def init(self):
        """
        Descript. :
        """
        AbstractDetector.init(self)

        # self.distance = 500
        self.temperature = 25
        self.humidity = 60
        self.actual_frame_rate = 50
        self.roi_modes_list = ("0", "C2", "C16")
        self.roi_mode = 0
        self.exposure_time_limits = [0.04, 60000]
        self.status = "ready"

        self._distance_motor_hwobj = self.getObjectByRole("detector_distance")

    def get_distance(self):
        return self._distance_motor_hwobj.get_position()

    def set_distance(self, position, timeout=None):
        self._distance_motor_hwobj.set_value(position, wait=True)

    def get_distance_limits(self):
        return [100, 1000]

    def set_roi_mode(self, roi_mode):
        self.roi_mode = roi_mode
        self.emit("detectorModeChanged", (self.roi_mode,))

    def has_shutterless(self):
        """Returns always True
        """
        return True

    def get_beam_centre(self):
        """Get approx detector centre (default to Pilatus values)"""
        xval = self.getProperty("width", 2463) / 2.0 + 0.4
        yval = self.getProperty("height", 2527) / 2.0 + 0.4
        return xval, yval

    def update_values(self):
        self.emit("detectorModeChanged", (self.roi_mode,))
        self.emit("temperatureChanged", (self.temperature, True))
        self.emit("humidityChanged", (self.humidity, True))
        self.emit("expTimeLimitsChanged", (self.exposure_time_limits,))
        self.emit("frameRateChanged", self.actual_frame_rate)
        self.emit("statusChanged", (self.status, "Ready"))

    def prepare_acquisition(self, *args, **kwargs):
        """
        Prepares detector for acquisition
        """
        return

    def last_image_saved(self):
        """
        Returns:
            str: path to last image
        """
        return

    def start_acquisition(self):
        """
        Starts acquisition
        """
        return

    def stop_acquisition(self):
        """
        Stops acquisition
        """
        return

    def wait_ready(self):
        """
        Blocks until detector is ready
        """
        return
