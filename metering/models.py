# TODO: Implement registers.


from typing import Any
from django.db import models

# Models:
from flows.models import Flow


class MeterPoint(models.Model):
    """
    A class representing a meter point with an MPAN.
    """

    # TODO: Field formatting and validation should match the JXXXX code. Check all field constraints and consider appropriate primary keys.
    profile_type = models.CharField(max_length=2, blank=False, null=False)
    meter_time_switch_code = models.CharField(max_length=3, blank=False, null=False)
    line_loss_factor = models.CharField(max_length=3, blank=False, null=False)
    distributor_id = models.CharField(max_length=2, blank=False, null=False)
    meter_point_id = models.CharField(max_length=8, blank=False, null=False)

    # TODO: Implement check_digit logicfor MPAN.
    check_digit = models.CharField(max_length=3, blank=False, null=False)

    # TODO: Do we want to use the unique identifier as the pm for the MeterPoint? If so, this might have certain implications.
    unique_identifier = models.CharField(
        editable=False, max_length=13, blank=False, null=False
    )
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("distributor_id", "meter_point_id", "check_digit")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.unique_identifier = (
            f"{self.distributor_id}{self.meter_point_id}{self.check_digit}"
        )

    def __str__(self) -> str:
        return self.unique_identifier


class Meter(models.Model):
    """
    A class representing a meter.
    """

    meter_point = models.ForeignKey(
        MeterPoint, on_delete=models.CASCADE, blank=False, null=False
    )
    serial_number = models.CharField(
        max_length=10, unique=True, primary_key=True, blank=False, null=False
    )
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.serial_number


class MeterReading(models.Model):
    """
    A class representing a meter reading.

    """

    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, blank=False, null=False)
    reading = models.DecimalField(decimal_places=1, max_digits=10, default=0.0)
    time_of_reading = models.DateTimeField(auto_now_add=True)

    # TODO: Enforce choices from valid set obtained from docs.
    type = models.CharField(max_length=1, blank=False, null=False)

    # TODO: Enforce choices from valid set obtained from docs.
    method = models.CharField(max_length=1, blank=False, null=False)

    class Meta:
        ordering = ["meter", "-time_of_reading"]
        verbose_name = "Meter Reading"
        unique_together = ("meter", "time_of_reading")

    def __str__(self) -> str:
        return f"{self.meter.serial_number} @ {str(self.time_of_reading)}"
