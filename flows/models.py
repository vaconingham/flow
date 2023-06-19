from typing import Any
from django.db import models


class Flow(models.Model):
    """
    A class representing flow files.
    """

    # TODO: Field formatting and validation should match the JXXXX code.
    reference = models.CharField(max_length=5, blank=False, null=False)
    name = models.CharField(max_length=64, blank=False, null=False)
    version = models.CharField(max_length=3, blank=False, null=False)

    # TODO: Enforce with choices list obtained from docs.
    status = models.CharField(max_length=64, blank=False, null=False)
    description = models.CharField(max_length=256, blank=False, null=False)
    ownership = models.CharField(max_length=64, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
