import molecule

header = """<svg version="1.1" width="1000" height="1000"
xmlns="http://www.w3.org/2000/svg">"""
footer = """</svg>"""
offsetx = 500
offsety = 500

class Atom():
    def __init__(self, c_atom):
        self.a = c_atom
        self.z = c_atom.z

    def __str__(self):
        return '%s %f %f %f\n' %(self.a.element, self.a.x, self.a.y, self.a.z)

    def svg(self):
        return ' <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' %(self.a.x * 100 + offsetx, self.a.y * 100 + offsety,
                                                                    radius[self.a.element], element_name[self.a.element])


class Bond():

    def __init__(self, c_bond):
        self.b = c_bond
        self.z = c_bond.z

    def __str__(self):
        return 'x1=%.5f x2=%.5f y1=%.5f y2=%.5f len=%.5f dx=%.5f dy=%.2f\n' %(self.b.x1, self.b.x2,
                                                                            self.b.y1, self.b.y2, self.b.len, self.b.dx, self.b.dy)

    def svg(self):
        return ' <polygon points="%.2f,%.2f %.2f,%.2f,%.2f,%.2f %.2f,%.2f" fill="green"/>\n' %(self.b.x1 * 100 - self.b.dy * 10 + offsetx,
                                                                                               self.b.y1 * 100 + self.b.dx * 10 + offsety,
                                                                                               self.b.x1 * 100 + self.b.dy * 10 + offsetx,
                                                                                               self.b.y1 * 100 - self.b.dx * 10 + offsety,
                                                                                               self.b.x2 * 100 + self.b.dy * 10 + offsetx,
                                                                                               self.b.y2 * 100 - self.b.dx * 10 + offsety,
                                                                                               self.b.x2 * 100 - self.b.dy * 10 + offsetx,
                                                                                               self.b.y2 * 100 + self.b.dx * 10 + offsety)

class Molecule(molecule.molecule):

    def __str__(self):
        output = ""
        for i in range(self.atom_no):
            output += str(Atom(self.get_atom(i)))

        for i in range(self.bond_no):
            output += str(Bond(self.get_bond(i)))

        return output

    def svg(self):
        output = header
        i = 0
        j = 0

        while i < self.atom_no and j < self.bond_no:
            if self.get_atom(i).z <= self.get_bond(j).z:
                a = Atom(self.get_atom(i))
                output += a.svg()
                i+=1
            else:
                b = Bond(self.get_bond(j))
                output += b.svg()
                j+=1


        while i < self.atom_no:
            a = Atom(self.get_atom(i))
            output += a.svg()
            i+=1

        while j < self.bond_no:
            b = Bond(self.get_bond(j))
            output += b.svg()
            j+=1

        output += footer

        return output

    def parse(self, file):
        for i in range(4):
            file.readline()

        for line in file:
            #trims string of "'b" from binary files
            line = line.rstrip()
            items = line.split()
            #checks EOF
            if 'M' in items and 'END' in items:
                break
            if items[3].isalpha():
                self.append_atom(items[3], float(items[0]), float(items[1]), float(items[2]))
            else:
                self.append_bond((int((items[0])) & 0xffff) - 1, ((int(items[1])) & 0xffff) - 1, int(items[2]) & 0xff)

        return self

if __name__ == '__main__':
    fptr = open("t.sdf", "rb")
    f = open("w.txt", "w")

    mol = Molecule()
    mol = mol.parse(fptr)
    mol.sort()
    print(mol)

    f.write(mol.svg())
