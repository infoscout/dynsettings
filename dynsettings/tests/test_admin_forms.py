from django.test import TestCase

from dynsettings.admin.forms import BucketModelChoiceField
from dynsettings.models import Bucket


class BucketModelChoiceFieldTestCase(TestCase):

    def test_bucket_model_choice(self):
        bucket = Bucket.objects.create(key='bucket_one')

        self.bucket_modelchoicefield = BucketModelChoiceField(
            queryset=Bucket.objects.all()
        )
        answer = self.bucket_modelchoicefield.label_from_instance(bucket)

        self.assertEqual(answer, 'bucket_one')
