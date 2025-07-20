class Stats:
    def __init__(self, hp, spd, ea, pa, ed, pd):
        self._hp = hp
        self._spd = spd
        self._ea = ea
        self._pa = pa
        self._ed = ed
        self._pd = pd

    @property
    def hp(self):
        return self._hp

    @property
    def spd(self):
        return self._spd

    @property
    def ea(self):
        return self._ea

    @property
    def pa(self):
        return self._pa

    @property
    def ed(self):
        return self._ed

    @property
    def pd(self):
        return self._pd