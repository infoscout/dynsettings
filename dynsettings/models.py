from django.conf import settings
from django.db import models
from django.db.utils import DatabaseError


DATA_TYPES = (
    ('STRING','String'),
    ('INTEGER','Integer'),
    ('FLOAT','Float'),
    ('DECIMAL','Decimal'),
    ('BOOLEAN','Boolean'),
)
    
class Setting(models.Model):
        
    key = models.CharField(max_length=32, primary_key=True)
    value = models.CharField(max_length=255, blank=True)
    help_text = models.CharField(max_length=255, blank=True, null=True)
    data_type = models.CharField(max_length=20, choices=DATA_TYPES, blank=False)
    
    def __nonzero__(self):
        return self.key is not None

    def save(self):
        # Save and reset cache
        super(Setting, self).save()
        SettingCache.reset()
        
    def __unicode__(self):
        return self.key


class Bucket(models.Model):
    key = models.CharField(max_length=16, primary_key=True)
    desc = models.CharField(max_length=255, blank=True, null=True)
    bucket_type = models.CharField(max_length=32, blank=True)
    probability = models.IntegerField(default=0, help_text="Used for other apps that may choose random buckets")
    
    def __unicode__(self):
        return self.key
    
    
class BucketSetting(models.Model):
    bucket = models.ForeignKey(Bucket)
    setting = models.ForeignKey(Setting)
    value = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = (('bucket','setting'))

    def save(self, force_insert=False, force_update=False, using=None):
        # Save and reset cache
        super(BucketSetting, self).save(force_insert, force_update, using)
        SettingCache.reset()
        
        
class SettingCache():
    """ Static class used to load and provide values """
    
    _values = {}
    _loaded = False
    
    valuedict = {}

    @classmethod
    def get_value(cls, key, bucket=None):
        if not cls._loaded: 
            result = cls.load()
            
            # If failed, could not find value from database
            # Since it may be running syncdb, return default value
            if not result:
                value = cls.import_dynsetting(key)
                return value.default_value
                
        # Dynamically add new value to db and reset cache
        if key not in cls._values:
            cls.add_key(key)
            cls.load()
            
        # First try and pull bucket
        if bucket and bucket.key in cls._values[key]:
            return cls._values[key][bucket.key]
        else:
            return cls._values[key]['default']

        
    @classmethod
    def import_dynsetting(cls, key):
        """
        Iterates through installed apps and 
        returns Dynsetting Value based on key
        """
        
        for installed_app in settings.INSTALLED_APPS:

            try:
                import_name = "%s.dynsettings" % installed_app
                x = __import__(import_name, fromlist=[key])

                if hasattr(x, key):
                    value = getattr(x, key)
                    return value
            
            except ImportError,e :
                
                if "No module named dynsettings" in str(e):
                    continue

                # Reimport which fires error with complete ImportError msg
                x = __import__(import_name, fromlist=[key])


    @classmethod
    def add_key(cls, key):
        """
        Adds any new dynsettings values found to the db
        """
        
        # Save and clear cache
        value = cls.import_dynsetting(key)
        value.set()

        cls._loaded = False
        cls._values = {}

       
    @classmethod
    def load(cls):
        """ 
        Loads all dynsettings into local 
        self._value dict
        """
        
        try:
            setting_records = list(Setting.objects.all())        
        except DatabaseError, e:
            return False
        
        for setting_record in setting_records:
            key = setting_record.key
            value = setting_record.value
            
            # maybe type convert here intead of later?
            cls._values[key] = {'default': value}
            
        # Add bucket settings to dict
        bucket_settings = BucketSetting.objects.all()
        for bucket_setting in bucket_settings:
            key = bucket_setting.setting.key
            value = bucket_setting.value
            bucket_key = bucket_setting.bucket.key
            
            cls._values[key][bucket_key] = value
            
        cls._loaded = True
    
    @classmethod
    def reset(cls):
        cls._loaded = False
        cls._values = {}
