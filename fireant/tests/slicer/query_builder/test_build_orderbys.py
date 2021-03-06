from unittest import TestCase

import fireant as f
from pypika import Order
from ..mocks import slicer


class QueryBuilderOrderTests(TestCase):
    maxDiff = None

    def test_build_query_order_by_dimension(self):
        queries = slicer.data \
            .widget(f.DataTablesJS(slicer.metrics.votes)) \
            .dimension(slicer.dimensions.timestamp) \
            .orderby(slicer.dimensions.timestamp) \
            .queries

        self.assertEqual(len(queries), 1)

        self.assertEqual('SELECT '
                         'TRUNC("timestamp",\'DD\') "$d$timestamp",'
                         'SUM("votes") "$m$votes" '
                         'FROM "politics"."politician" '
                         'GROUP BY "$d$timestamp" '
                         'ORDER BY "$d$timestamp"', str(queries[0]))

    def test_build_query_order_by_dimension_display(self):
        queries = slicer.data \
            .widget(f.DataTablesJS(slicer.metrics.votes)) \
            .dimension(slicer.dimensions.candidate) \
            .orderby(slicer.dimensions.candidate_display) \
            .queries

        self.assertEqual(len(queries), 1)

        self.assertEqual('SELECT '
                         '"candidate_id" "$d$candidate",'
                         '"candidate_name" "$d$candidate_display",'
                         'SUM("votes") "$m$votes" '
                         'FROM "politics"."politician" '
                         'GROUP BY "$d$candidate","$d$candidate_display" '
                         'ORDER BY "$d$candidate_display"', str(queries[0]))

    def test_build_query_order_by_dimension_asc(self):
        queries = slicer.data \
            .widget(f.DataTablesJS(slicer.metrics.votes)) \
            .dimension(slicer.dimensions.timestamp) \
            .orderby(slicer.dimensions.timestamp, orientation=Order.asc) \
            .queries

        self.assertEqual(len(queries), 1)

        self.assertEqual('SELECT '
                         'TRUNC("timestamp",\'DD\') "$d$timestamp",'
                         'SUM("votes") "$m$votes" '
                         'FROM "politics"."politician" '
                         'GROUP BY "$d$timestamp" '
                         'ORDER BY "$d$timestamp" ASC', str(queries[0]))

    def test_build_query_order_by_dimension_desc(self):
        queries = slicer.data \
            .widget(f.DataTablesJS(slicer.metrics.votes)) \
            .dimension(slicer.dimensions.timestamp) \
            .orderby(slicer.dimensions.timestamp, orientation=Order.desc) \
            .queries

        self.assertEqual(len(queries), 1)

        self.assertEqual('SELECT '
                         'TRUNC("timestamp",\'DD\') "$d$timestamp",'
                         'SUM("votes") "$m$votes" '
                         'FROM "politics"."politician" '
                         'GROUP BY "$d$timestamp" '
                         'ORDER BY "$d$timestamp" DESC', str(queries[0]))

    def test_build_query_order_by_metric(self):
        queries = slicer.data \
            .widget(f.DataTablesJS(slicer.metrics.votes)) \
            .dimension(slicer.dimensions.timestamp) \
            .orderby(slicer.metrics.votes) \
            .queries

        self.assertEqual(len(queries), 1)

        self.assertEqual('SELECT '
                         'TRUNC("timestamp",\'DD\') "$d$timestamp",'
                         'SUM("votes") "$m$votes" '
                         'FROM "politics"."politician" '
                         'GROUP BY "$d$timestamp" '
                         'ORDER BY "$m$votes"', str(queries[0]))

    def test_build_query_order_by_metric_asc(self):
        queries = slicer.data \
            .widget(f.DataTablesJS(slicer.metrics.votes)) \
            .dimension(slicer.dimensions.timestamp) \
            .orderby(slicer.metrics.votes, orientation=Order.asc) \
            .queries

        self.assertEqual(len(queries), 1)

        self.assertEqual('SELECT '
                         'TRUNC("timestamp",\'DD\') "$d$timestamp",'
                         'SUM("votes") "$m$votes" '
                         'FROM "politics"."politician" '
                         'GROUP BY "$d$timestamp" '
                         'ORDER BY "$m$votes" ASC', str(queries[0]))

    def test_build_query_order_by_metric_desc(self):
        queries = slicer.data \
            .widget(f.DataTablesJS(slicer.metrics.votes)) \
            .dimension(slicer.dimensions.timestamp) \
            .orderby(slicer.metrics.votes, orientation=Order.desc) \
            .queries

        self.assertEqual(len(queries), 1)

        self.assertEqual('SELECT '
                         'TRUNC("timestamp",\'DD\') "$d$timestamp",'
                         'SUM("votes") "$m$votes" '
                         'FROM "politics"."politician" '
                         'GROUP BY "$d$timestamp" '
                         'ORDER BY "$m$votes" DESC', str(queries[0]))

    def test_build_query_order_by_multiple_dimensions(self):
        queries = slicer.data \
            .widget(f.DataTablesJS(slicer.metrics.votes)) \
            .dimension(slicer.dimensions.timestamp, slicer.dimensions.candidate) \
            .orderby(slicer.dimensions.timestamp) \
            .orderby(slicer.dimensions.candidate) \
            .queries

        self.assertEqual(len(queries), 1)

        self.assertEqual('SELECT '
                         'TRUNC("timestamp",\'DD\') "$d$timestamp",'
                         '"candidate_id" "$d$candidate",'
                         '"candidate_name" "$d$candidate_display",'
                         'SUM("votes") "$m$votes" '
                         'FROM "politics"."politician" '
                         'GROUP BY "$d$timestamp","$d$candidate","$d$candidate_display" '
                         'ORDER BY "$d$timestamp","$d$candidate"', str(queries[0]))

    def test_build_query_order_by_multiple_dimensions_with_different_orientations(self):
        queries = slicer.data \
            .widget(f.DataTablesJS(slicer.metrics.votes)) \
            .dimension(slicer.dimensions.timestamp, slicer.dimensions.candidate) \
            .orderby(slicer.dimensions.timestamp, orientation=Order.desc) \
            .orderby(slicer.dimensions.candidate, orientation=Order.asc) \
            .queries

        self.assertEqual(len(queries), 1)

        self.assertEqual('SELECT '
                         'TRUNC("timestamp",\'DD\') "$d$timestamp",'
                         '"candidate_id" "$d$candidate",'
                         '"candidate_name" "$d$candidate_display",'
                         'SUM("votes") "$m$votes" '
                         'FROM "politics"."politician" '
                         'GROUP BY "$d$timestamp","$d$candidate","$d$candidate_display" '
                         'ORDER BY "$d$timestamp" DESC,"$d$candidate" ASC', str(queries[0]))

    def test_build_query_order_by_metrics_and_dimensions(self):
        queries = slicer.data \
            .widget(f.DataTablesJS(slicer.metrics.votes)) \
            .dimension(slicer.dimensions.timestamp) \
            .orderby(slicer.dimensions.timestamp) \
            .orderby(slicer.metrics.votes) \
            .queries

        self.assertEqual(len(queries), 1)

        self.assertEqual('SELECT '
                         'TRUNC("timestamp",\'DD\') "$d$timestamp",'
                         'SUM("votes") "$m$votes" '
                         'FROM "politics"."politician" '
                         'GROUP BY "$d$timestamp" '
                         'ORDER BY "$d$timestamp","$m$votes"', str(queries[0]))

    def test_build_query_order_by_metrics_and_dimensions_with_different_orientations(self):
        queries = slicer.data \
            .widget(f.DataTablesJS(slicer.metrics.votes)) \
            .dimension(slicer.dimensions.timestamp) \
            .orderby(slicer.dimensions.timestamp, orientation=Order.asc) \
            .orderby(slicer.metrics.votes, orientation=Order.desc) \
            .queries

        self.assertEqual(len(queries), 1)

        self.assertEqual('SELECT '
                         'TRUNC("timestamp",\'DD\') "$d$timestamp",'
                         'SUM("votes") "$m$votes" '
                         'FROM "politics"."politician" '
                         'GROUP BY "$d$timestamp" '
                         'ORDER BY "$d$timestamp" ASC,"$m$votes" DESC', str(queries[0]))

    def test_build_query_order_by_metric_not_in_widget(self):
        queries = slicer.data \
            .widget(f.DataTablesJS(slicer.metrics.votes)) \
            .dimension(slicer.dimensions.timestamp) \
            .orderby(slicer.metrics.wins) \
            .queries

        self.assertEqual(len(queries), 1)

        self.assertEqual('SELECT '
                         'TRUNC("timestamp",\'DD\') "$d$timestamp",'
                         'SUM("votes") "$m$votes",'
                         'SUM("is_winner") "$m$wins" '
                         'FROM "politics"."politician" '
                         'GROUP BY "$d$timestamp" '
                         'ORDER BY "$m$wins"', str(queries[0]))
