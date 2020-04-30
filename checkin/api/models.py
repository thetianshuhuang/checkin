from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class UserToken(models.Model):
    """Access tokens for each user

    This token is necessary in order to create
    new Programs. This token cannot be used to send records.
    """

    # Owner (user)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Actual token
    api_token = models.TextField(blank=False, null=False)

    # Description
    desc = models.TextField()


class Program(models.Model):
    """Program; consists of a set of records."""

    # Owner (user)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Record token
    api_token = models.TextField(null=True)
    # View access token
    access_token = models.TextField(null=True)

    # Name
    name = models.TextField(null=True)

    # Start time; NULL if not started
    start = models.FloatField(null=True)
    # End time; NULL if not done
    end = models.FloatField(null=True)


class Record(models.Model):
    """Task, Error, Warning, or Info Record"""

    # Program ID
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    # UUID corresponding to this record
    record_id = models.CharField(max_length=50)

    # UUID corresponding to record's parent. If this is the root record, the
    # UUID will be the program ID.
    parent = models.CharField(max_length=50, null=True)

    # Record name. For errors, this corresponds to the error name.
    name = models.TextField(null=True)
    # Record description. For errors, this corresponds to the traceback.
    desc = models.TextField(null=True)

    # Source node ID.
    node_id = models.CharField(max_length=50, null=True)

    # Record type: TASK, ERR, WARN, INFO, META
    type = models.CharField(max_length=10, null=True)

    # Start Time (POSIX time); NULL if task not started
    start = models.FloatField(null=True)

    # End Time (POSIX time); NULL if task not complete
    end = models.FloatField(null=True)

    # Time last updated (POSIX time);
    updated = models.FloatField(null=True)

    # Additional metadata (JSON)
    meta = models.TextField(null=True)


class QueuedRecord(Record):
    """Queued records for a client -- records that a front end client hasn't
    yet recieved and rendered
    """

    # Identical to Record; many fields may be null


admin.site.register(Program)
admin.site.register(Record)
admin.site.register(UserToken)
