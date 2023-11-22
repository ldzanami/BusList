from datetime import datetime
import imports

class Bus():
    def __init__(self, ras : dict, city : str, station : str, side : str, num : str, message : imports.Message):
        self.ras = ras[city][station][side][num]
        self.city = city
        self.station = station
        self.side = side
        self.num = num
        self.list_commands = list()
        self.cur = datetime.now()

    async def next(self):
            num = self.num
            ras_keys_int = sorted(map(int, self.ras.keys()))
            cur = self.cur
            nexth = cur.hour
            nextm = None
            while nextm is None:
                while nexth not in ras_keys_int:
                    if nexth < max(ras_keys_int):
                        nexth += 1
                    else: nexth = min(ras_keys_int)
                for i in self.ras[str(nexth)]:
                    i = int(i)
                    if cur.hour == nexth and cur.minute <= i or nexth == min(self.ras) and nexth == max(self.ras):
                        nextm = i
                        break
                    elif cur.hour != nexth: nextm = i; break
                if nextm is None and nexth in ras_keys_int:
                    nexth += 1
                elif nextm is None and nexth > max(ras_keys_int): nexth = min(ras_keys_int)
            nextm = str(nextm)
            if len(nextm) < 2: nextm = '0' + nextm
            self.list_commands.append(f'Следующий автобус {self.num} на остановке {self.station} приедет в {nexth}:{nextm} по томскому времени')

    async def print_one(self, smt):
        for i in range(len(smt[1].keys())):
            mins = str(list(smt[1].keys())[i])
            if len(mins) < 2: mins = '0' + mins
            self.list_commands.append(f'{smt[0]}:{mins}')

    async def print_table(self):
        self.list_commands.append("время")
        for i in sorted(self.ras.items()):
            await self.print_one(i)
        await self.next()
