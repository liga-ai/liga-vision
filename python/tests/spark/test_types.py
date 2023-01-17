#  Copyright 2020 Rikai Authors
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import secrets
from pathlib import Path
from typing import Iterable

from pyspark.sql import DataFrame, Row, SparkSession

# Liga
from ligavision.dsl import (
    Box2d,
    Box3d,
    Image,
    Mask,
    Point,
    Segment,
    VideoStream,
    YouTubeVideo,
)

def assert_count_equal(first: Iterable, second: Iterable, msg=None):
    """Assert ``first`` has the same elements as ``second``, regardless of
    the order.
    See Also
    --------
    :py:meth:`unittest.TestCase.assertCountEqual`
    """
    from unittest import TestCase

    TestCase().assertCountEqual(first, second, msg=msg)


def _check_roundtrip(spark: SparkSession, df: DataFrame, tmp_path: Path):
    df.show()
    df.write.mode("overwrite").format("parquet").save(str(tmp_path))
    actual_df = spark.read.format("parquet").load(str(tmp_path))
    assert_count_equal(df.collect(), actual_df.collect())


def test_bbox(spark, tmp_path):
    df = spark.createDataFrame(
        [Row(Box2d(1, 2, 3, 4)), Row(Box2d(23, 33, 44, 88))], ["bbox"]
    )
    _check_roundtrip(spark, df, tmp_path)


def test_point(spark, tmpdir):
    df = spark.createDataFrame([Row(Point(1, 2, 3)), Row(Point(2, 3, 4))])
    _check_roundtrip(spark, df, tmpdir)


def test_box3d(spark, tmpdir):
    df = spark.createDataFrame([Row(Box3d(Point(1, 2, 3), 1, 2, 3, 2.5))])
    _check_roundtrip(spark, df, tmpdir)


def test_mask(spark, tmpdir):
    df = spark.createDataFrame(
        [Row(mask=Mask.from_rle([1, 10, 10], height=3, width=7))]
    )
    _check_roundtrip(spark, df, tmpdir)


def test_embedded_images(spark, tmpdir):
    df = spark.createDataFrame([Row(Image(secrets.token_bytes(128)))])
    _check_roundtrip(spark, df, tmpdir)


def test_youtubevideo(spark, tmpdir):
    df = spark.createDataFrame(
        [
            Row(YouTubeVideo("video_id")),
            Row(YouTubeVideo("other_video_id")),
        ]
    )
    _check_roundtrip(spark, df, tmpdir)


def test_videostream(spark, tmpdir):
    df = spark.createDataFrame(
        [Row(VideoStream("uri1")), Row(VideoStream("uri2"))]
    )
    _check_roundtrip(spark, df, tmpdir)


def test_segment(spark, tmpdir):
    df = spark.createDataFrame([Row(Segment(0, 10)), Row(Segment(15, -1))])
    _check_roundtrip(spark, df, tmpdir)
