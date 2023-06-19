from django.test import TransactionTestCase
from django.core.management import call_command
from io import StringIO
import logging
from metering.models import MeterPoint, Meter, MeterReading

logger = logging.getLogger(__name__)


class TestD0010FileProcessing(TransactionTestCase):
    def command(self, path):
        out = StringIO()
        call_command(
            "d0010",
            path,
            stdout=out,
            stderr=StringIO(),
        )
        return out.getvalue()

    def test_calling_command_with_valid_file_creates_expected_data(self):
        path = "flows/samples/d0010.txt"

        self.command(path)

        self.assertEqual(11, len(MeterPoint.objects.all()))
        self.assertEqual(11, len(Meter.objects.all()))
        self.assertEqual(11, len(MeterReading.objects.all()))

    def test_calling_command_with_invalid_file_logs_unrecognised_flow_type_error(self):
        path = "flows/samples/invalid_file.txt"
        self.command(path)

        with self.assertLogs("", level="INFO") as log:
            self.command(path)
        self.assertEqual(
            log.output[-2][-29:],
            f"is an unrecognised flow type.",
        )

    def test_calling_command_with_invalid_path_logs_file_not_found_error(self):
        path = "invalid/path"
        with self.assertLogs("", level="CRITICAL") as log:
            self.command(path)
        self.assertEqual(
            log.output[0],
            f"CRITICAL:flows.management.commands.d0010:No file found in path: {path}",
        )

    def test_calling_command_with_same_data_does_not_create_duplicates(self):
        path = "flows/samples/d0010.txt"

        self.command(path)

        meter_points = MeterPoint.objects.all()
        meters = Meter.objects.all()
        meter_readings = MeterReading.objects.all()

        self.command(path)
        self.assertEqual(len(meter_points), len(MeterPoint.objects.all()))
        self.assertEqual(len(meters), len(Meter.objects.all()))
        self.assertEqual(len(meter_readings), len(MeterReading.objects.all()))
