# -*- coding: utf-8 -*-

MIN_QUALITY = 0
MAX_QUALITY = 50

AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASSES = "Backstage passes to a TAFKAL80ETC concert"
CONJURED_MANA_CAKE = "Conjured Mana Cake"


def _increase_quality(quality, amount):
    return min(MAX_QUALITY, quality + amount)


def _decrease_quality(quality, amount):
    return max(MIN_QUALITY, quality - amount)


class RateBasedItem:
    """Quality moves by a fixed daily rate, doubling once sell_in <= 0."""

    def __init__(self, rate, adjust_quality):
        self._rate = rate
        self._adjust_quality = adjust_quality

    def update(self, item):
        rate = self._rate if item.sell_in > 0 else self._rate * 2
        item.quality = self._adjust_quality(item.quality, rate)
        item.sell_in -= 1


class Sulfuras:
    """Legendary item: never sold, never changes."""

    def update(self, item):
        pass


class BackstagePass:
    def update(self, item):
        if item.sell_in <= 0:
            item.quality = 0
        else:
            if item.sell_in <= 5:
                increase = 3
            elif item.sell_in <= 10:
                increase = 2
            else:
                increase = 1
            item.quality = _increase_quality(item.quality, increase)
        item.sell_in -= 1


UPDATERS_BY_NAME = {
    AGED_BRIE: RateBasedItem(1, _increase_quality),
    SULFURAS: Sulfuras(),
    BACKSTAGE_PASSES: BackstagePass(),
    CONJURED_MANA_CAKE: RateBasedItem(2, _decrease_quality),
}

DEFAULT_UPDATER = RateBasedItem(1, _decrease_quality)


class GildedRose:

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            updater = UPDATERS_BY_NAME.get(item.name, DEFAULT_UPDATER)
            updater.update(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
