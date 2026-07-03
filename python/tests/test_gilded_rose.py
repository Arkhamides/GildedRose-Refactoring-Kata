# -*- coding: utf-8 -*-
import unittest

from gilded_rose import (
    Item,
    GildedRose,
    AGED_BRIE,
    SULFURAS,
    BACKSTAGE_PASSES,
    CONJURED_MANA_CAKE as CONJURED,
)


class GildedRoseTest(unittest.TestCase):
    def update_quality(self, item):
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        return item

    # Normal item
    def test_normal_item_quality_decreases_by_one_before_sell_date(self):
        item = self.update_quality(Item("foo", 5, 10))
        self.assertEqual(9, item.quality)
        self.assertEqual(4, item.sell_in)

    def test_normal_item_quality_decreases_by_two_after_sell_date(self):
        item = self.update_quality(Item("foo", 0, 10))
        self.assertEqual(8, item.quality)

    def test_normal_item_quality_never_goes_below_zero(self):
        item = self.update_quality(Item("foo", 5, 0))
        self.assertEqual(0, item.quality)

    def test_normal_item_quality_never_goes_below_zero_after_sell_date(self):
        item = self.update_quality(Item("foo", 0, 1))
        self.assertEqual(0, item.quality)

    # Aged Brie
    def test_aged_brie_quality_increases_by_one_before_sell_date(self):
        item = self.update_quality(Item(AGED_BRIE, 5, 10))
        self.assertEqual(11, item.quality)
        self.assertEqual(4, item.sell_in)

    def test_aged_brie_quality_increases_by_two_after_sell_date(self):
        item = self.update_quality(Item(AGED_BRIE, 0, 10))
        self.assertEqual(12, item.quality)

    def test_aged_brie_quality_never_exceeds_fifty(self):
        item = self.update_quality(Item(AGED_BRIE, 5, 50))
        self.assertEqual(50, item.quality)

    def test_aged_brie_quality_never_exceeds_fifty_after_sell_date(self):
        item = self.update_quality(Item(AGED_BRIE, 0, 49))
        self.assertEqual(50, item.quality)

    # Sulfuras
    def test_sulfuras_sell_in_never_changes(self):
        item = self.update_quality(Item(SULFURAS, 5, 80))
        self.assertEqual(5, item.sell_in)

    def test_sulfuras_quality_stays_at_eighty(self):
        item = self.update_quality(Item(SULFURAS, 0, 80))
        self.assertEqual(80, item.quality)

    def test_sulfuras_quality_stays_at_eighty_after_sell_date(self):
        item = self.update_quality(Item(SULFURAS, -1, 80))
        self.assertEqual(80, item.quality)

    # Backstage passes
    def test_backstage_passes_quality_increases_by_one_when_more_than_ten_days(self):
        item = self.update_quality(Item(BACKSTAGE_PASSES, 11, 20))
        self.assertEqual(21, item.quality)
        self.assertEqual(10, item.sell_in)

    def test_backstage_passes_quality_increases_by_two_when_ten_days_or_less(self):
        item = self.update_quality(Item(BACKSTAGE_PASSES, 10, 20))
        self.assertEqual(22, item.quality)

    def test_backstage_passes_quality_increases_by_two_when_six_days(self):
        item = self.update_quality(Item(BACKSTAGE_PASSES, 6, 20))
        self.assertEqual(22, item.quality)

    def test_backstage_passes_quality_increases_by_three_when_five_days_or_less(self):
        item = self.update_quality(Item(BACKSTAGE_PASSES, 5, 20))
        self.assertEqual(23, item.quality)

    def test_backstage_passes_quality_increases_by_three_when_one_day(self):
        item = self.update_quality(Item(BACKSTAGE_PASSES, 1, 20))
        self.assertEqual(23, item.quality)

    def test_backstage_passes_quality_drops_to_zero_after_concert(self):
        item = self.update_quality(Item(BACKSTAGE_PASSES, 0, 20))
        self.assertEqual(0, item.quality)

    def test_backstage_passes_quality_stays_at_zero_well_after_concert(self):
        item = self.update_quality(Item(BACKSTAGE_PASSES, -1, 0))
        self.assertEqual(0, item.quality)

    def test_backstage_passes_quality_never_exceeds_fifty(self):
        item = self.update_quality(Item(BACKSTAGE_PASSES, 5, 49))
        self.assertEqual(50, item.quality)

    # Conjured
    def test_conjured_item_quality_decreases_by_two_before_sell_date(self):
        item = self.update_quality(Item(CONJURED, 5, 10))
        self.assertEqual(8, item.quality)
        self.assertEqual(4, item.sell_in)

    def test_conjured_item_quality_decreases_by_four_after_sell_date(self):
        item = self.update_quality(Item(CONJURED, 0, 10))
        self.assertEqual(6, item.quality)

    def test_conjured_item_quality_never_goes_below_zero(self):
        item = self.update_quality(Item(CONJURED, 5, 1))
        self.assertEqual(0, item.quality)

    def test_conjured_item_quality_never_goes_below_zero_after_sell_date(self):
        item = self.update_quality(Item(CONJURED, 0, 3))
        self.assertEqual(0, item.quality)

    # Dispatch
    def test_update_quality_applies_each_items_own_rule(self):
        normal = Item("foo", 5, 10)
        brie = Item(AGED_BRIE, 5, 10)
        sulfuras = Item(SULFURAS, 5, 80)
        GildedRose([normal, brie, sulfuras]).update_quality()
        self.assertEqual(9, normal.quality)
        self.assertEqual(11, brie.quality)
        self.assertEqual(80, sulfuras.quality)


if __name__ == "__main__":
    unittest.main()
