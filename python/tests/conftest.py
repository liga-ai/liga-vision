import pytest

from pyspark.sql import SparkSession

from ligavision.types.vision import Image
from ligavision import init_spark


@pytest.fixture(scope="session")
def two_flickr_images() -> list:
    return [
        Image.read(uri)
        for uri in [
            "http://farm2.staticflickr.com/1129/4726871278_4dd241a03a_z.jpg",
            "http://farm4.staticflickr.com/3726/9457732891_87c6512b62_z.jpg",
        ]
    ]

@pytest.fixture(scope="module")
def spark(tmp_path_factory) -> SparkSession:
    warehouse_path = tmp_path_factory.mktemp("warehouse")
    return init_spark(jar_type="local")
