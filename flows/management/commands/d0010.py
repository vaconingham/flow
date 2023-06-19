# TODO: For brevity, not every data point has been implemented.
# TODO: Created objects require further enrichment.
# TODO: We might want to create a command for getting file from the web.

import datetime
from django.utils import timezone
from sys import stdout
from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
import logging
from django.db import IntegrityError
from django.db import transaction

# Models:
from metering.models import MeterReading, Meter, MeterPoint

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """A command for processing D0010 flow files."""

    help = "Processes D0010 flow files. Extracts data and creates entries in the database for meter points, meters, and meter readings."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "paths",
            nargs="+",
            type=str,
            help="The path to the flow file.",
        )

    def handle(self, *args: Any, **options: Any) -> str | None:
        paths = options["paths"]

        logger.info("Running python manage.py d0010")

        try:
            for path in paths:
                processFile(path)

        except CommandError as e:
            logger.critical(e)

        except Exception as e:
            logger.critical(e)


@transaction.atomic
def processFile(path: str) -> None:
    """Creates meter points, meters, and meter readings with data extracted from D0010 flow files."""

    try:
        with open(path, "r") as file:
            lines = file.readlines()

        logger.info(f"Started processing {path}")
        for line in lines:
            # We're assuming here that D0010 files will only ever have the
            # following flow values.
            values = [str(value).strip() for value in line.split("|")]
            flow = values[0]
            if flow == "026":
                # Create meter point with a valid MPAN.
                core = values[1]
                meter_point, meter_point_created = MeterPoint.objects.get_or_create(
                    # TODO: Get MPAN top-line data
                    profile_type="00",
                    meter_time_switch_code="000",
                    line_loss_factor="000",
                    distributor_id=core[0:2],
                    meter_point_id=core[2:10],
                    check_digit=core[10:13],
                )

                if meter_point_created:
                    logger.info(
                        f"New meter point created with unique identifier {meter_point.unique_identifier}"
                    )

            elif flow == "028":
                # Create meter.
                meter, meter_created = Meter.objects.get_or_create(
                    meter_point=meter_point,
                    serial_number=values[1],
                )

                if meter_created:
                    logger.info(
                        f"New meter created with serial number {meter.serial_number}"
                    )

                # Create meter reading.
                meter_reading = MeterReading.objects.create(
                    meter=meter,
                    type=values[2],
                )

            elif flow == "030":
                # Populate meter reading.
                time_of_reading = datetime.datetime.fromtimestamp(
                    float(values[2]) / 1000, timezone.utc
                )
                meter_reading.time_of_reading = time_of_reading
                meter_reading.reading = values[3]
                meter_reading.method = values[7]
                meter_reading.save()

                logger.info(
                    f"New meter reading created for meter {meter_reading.meter}"
                )

            else:
                logger.warning(f"{flow} is an unrecognised flow type.")

    except FileNotFoundError as e:
        logger.critical(f"No file found in path: {path}")

    except IntegrityError as e:
        logger.warning(
            f"Meter readings with the same meter and timestamp already exist."
        )

    except Exception as e:
        logger.critical(e)

    else:
        logger.info("The file was successfully processed.")
