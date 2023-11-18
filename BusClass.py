import imports

class Bus():
    def __init__(self, ras : dict, city : str, station : str, side : str, num : str):
        self.ras = ras[city][station][side][num]
        self.city = city
        self.station = station
        self.side = side
        self.num = num

    def next(self):
            num = self.num
            ras_keys_int = sorted(map(int, self.ras.keys()))
            cur = datetime.now()
            nexth = cur.hour
            nextm = None
            while nextm is None:
                while nexth not in ras_keys_int:
                    if nexth < max(ras_keys_int):
                        nexth += 1
                    else: nexth = min(ras_keys_int)
                for i in self.ras[str(nexth)]:
                    i = int(i)
                    if cur.hour == nexth and cur.minute <= i:
                        nextm = i
                        break
                    elif cur.hour != nexth: nextm = i; break
                if nextm is None and nexth in ras_keys_int:
                    nexth += 1
                elif nextm is None and nexth > max(ras_keys_int): nexth = min(ras_keys_int)
            d = self.ras[str(nexth)][str(nextm)][0]
            nextm = str(nextm)
            if len(nextm) < 2: nextm = '0' + nextm
            print(f" ---|Следующий автобус {self.num} приедет в {nexth}:{nextm}|---\n\t  ---|Отклонение: {min(d)} {round(sum(d) / len(d), 2)} +{max(d)}|---")

    def print_one(self, smt):
        for i in range(len(smt[1].keys())):
            mins = str(list(smt[1].keys())[i])
            if len(mins) < 2: mins = '0' + mins
            print(f'''\t    ▏___________│__________│
    \t    ▏   {smt[0]}:{mins.ljust(5)}│     {str(list(smt[1].values())[i][1]).ljust(5)}│''')

    def print_table(self):
        print(f'───┐\n{self.num}▕\n───┘\n')
        print('\t    ________________________')
        print("\t    ▏   время   │ пропуски │")
        for i in sorted(self.ras.items()):
            self.print_one(i)
        print('\t    ▏___________│__________│\n')
        self.next()