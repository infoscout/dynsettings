from django.test import TestCase

from dynsettings.admin.forms import BucketModelChoiceField
from dynsettings.models import Bucket


class BucketModelChoiceFieldTestCase(TestCase):
    """
    Verify class returns bucket.key when no bucket_type present
    """
    def test_bucket_model_choice(self):

        bucket = Bucket.objects.create(key='bucket_one')
        self.bucket_model_choice_field = BucketModelChoiceField(
            queryset=Bucket.objects.all()
        )
        answer = self.bucket_model_choice_field.label_from_instance(bucket)

        self.assertEqual(answer, 'bucket_one')
