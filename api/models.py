from django.db import models

# Django internal tables - KEEP MANAGED = FALSE
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)
    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)

class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)

class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)

class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_migrations'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_session'

# YOUR CUSTOM TABLES - MANAGED = TRUE
class Locations(models.Model):
    location_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(unique=True, max_length=100)
    class Meta:
        managed = True
        db_table = 'locations'

class EventOrganizers(models.Model):
    organizer_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=150)
    organization_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(unique=True, max_length=150)
    created_at = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'event_organizers'

class UserProfiles(models.Model):
    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=150)
    email = models.CharField(unique=True, max_length=150)
    role = models.CharField(max_length=50)
    assigned_location = models.ForeignKey(Locations, models.DO_NOTHING, blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'user_profiles'

class Bookings(models.Model):
    booking_id = models.AutoField(primary_key=True)
    location = models.ForeignKey(Locations, models.DO_NOTHING, blank=True, null=True)
    organizer = models.ForeignKey(EventOrganizers, models.DO_NOTHING, blank=True, null=True)
    approved_by = models.ForeignKey(UserProfiles, models.DO_NOTHING, db_column='approved_by', blank=True, null=True)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, blank=True, null=True)
    compliance_document = models.FileField(upload_to='compliance/', null=True, blank=True)
    class Meta:
        managed = True
        db_table = 'bookings'
