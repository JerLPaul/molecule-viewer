import os
import sqlite3
import MolDisplay

class Database():
    def __init__(self, reset=True):
        if (reset):
            if os.path.exists('molecules.db'):
                os.remove('molecules.db')
        self.conn = sqlite3.connect('molecules.db')

    def create_tables(self):
        #Element table
        self.conn.execute("""CREATE TABLE ELEMENTS (
                             ELEMENT_NO     INTEGER NOT NULL,
                             ELEMENT_CODE   VARCHAR(3) NOT NULL,
                             ELEMENT_NAME   VARCHAR(32) NOT NULL,
                             COLOUR1     CHAR(6) NOT NULL,
                             COLOUR2     CHAR(6) NOT NULL,
                             COLOUR3     CHAR(6) NOT NULL,
                             RADIUS     DECIMAL(3) NOT NULL,
                             PRIMARY KEY (ELEMENT_CODE)
                            );""")

        #Atoms table
        self.conn.execute("""CREATE TABLE ATOMS (
                             ATOM_ID            INTEGER NOT NULL,
                             ELEMENT_CODE       VARCHAR(3) NOT NULL,
                             X                  DECIMAL(7,4) NOT NULL,
                             Y                  DECIMAL(7,4) NOT NULL,
                             Z                  DECIMAL(7,4) NOT NULL,
                             PRIMARY KEY(ATOM_ID),
                             FOREIGN KEY(ELEMENT_CODE) REFERENCES ELEMENTS);""")

        #Bonds table
        self.conn.execute("""CREATE TABLE BONDS (
                             BOND_ID            INTEGER NOT NULL,
                             A1                 INTEGER NOT NULL,
                             A2                 INTEGER NOT NULL,
                             EPAIRS             INTEGER NOT NULL,
                             PRIMARY KEY(BOND_ID)
                             );""")

        #Molecules table
        self.conn.execute("""CREATE TABLE MOLECULES (
                             MOLECULE_ID        INTEGER NOT NULL,
                             NAME               TEXT NOT NULL,
                             PRIMARY KEY(MOLECULE_ID),
                             UNIQUE(NAME)
                             );""")

        #Molecule Atom table
        self.conn.execute("""CREATE TABLE MOLECULEATOM (
                             MOLECULE_ID        INTEGER NOT NULL,
                             ATOM_ID            INTEGER NOT NULL,
                             PRIMARY KEY(MOLECULE_ID, ATOM_ID),
                             FOREIGN KEY(ATOM_ID) REFERENCES ATOMS,
                             FOREIGN KEY(MOLECULE_ID) REFERENCES MOLECULES
                             );""")

        #Molecule Bond table
        self.conn.execute("""CREATE TABLE MOLECULEBOND (
                             MOLECULE_ID        INTEGER NOT NULL,
                             BOND_ID            INTEGER NOT NULL,
                             PRIMARY KEY (MOLECULE_ID, BOND_ID),
                             FOREIGN KEY (BOND_ID) REFERENCES BONDS,
                             FOREIGN KEY (MOLECULE_ID) REFERENCES MOLECULES
                             );""")


    def __setitem__(self, table, values):
        self.conn.execute("""INSERT INTO {}
                              VALUES {};""".format(table, values))
        self.conn.commit()

    def add_atom(self, molname, atom):
        self.conn.execute("""INSERT INTO ATOMS (ELEMENT_CODE, X, Y, Z)
                              VALUES ("{}", {}, {}, {});
                              """.format(atom.element, atom.x, atom.y, atom.z))

        #Finds the tuple containing Molecule ID and recent Atom ID
        id = self.conn.execute("""SELECT MOLECULE_ID, MAX(ATOM_ID)
                                  FROM MOLECULES, ATOMS
                                  WHERE MOLECULES.NAME = "{}";
                                """.format(molname)).fetchall()

        self.conn.execute("""INSERT INTO MOLECULEATOM (MOLECULE_ID, ATOM_ID)
                             VALUES ({}, {});
                             """.format(id[0][0], id[0][1]))
        self.conn.commit()

    def add_bond(self, molname, bond):
        self.conn.execute("""INSERT INTO BONDS (A1, A2, EPAIRS)
                              VALUES ({}, {}, {});
                              """.format(bond.a1, bond.a2, bond.epairs))

        #Finds the tuple containing Molecule ID and recent Bond ID
        id = self.conn.execute("""SELECT MOLECULE_ID, MAX(BOND_ID)
                                  FROM MOLECULES, BONDS
                                  WHERE MOLECULES.NAME = "{}";
                                """.format(molname)).fetchall()


        self.conn.execute("""INSERT INTO MOLECULEBOND (MOLECULE_ID, BOND_ID)
                             VALUES ({}, {});
                             """.format(id[0][0], id[0][1]))
        self.conn.commit()

    def add_molecule(self, name, fp):
        mol = MolDisplay.Molecule()
        mol = mol.parse(fp)

        self.conn.execute("""INSERT INTO MOLECULES (NAME)
                              VALUES ("{}");
                              """.format(name))

        for i in range(mol.atom_no):
            self.add_atom(name, mol.get_atom(i))

        for i in range(mol.bond_no):
            self.add_bond(name, mol.get_bond(i))

        self.conn.commit()

    def load_mol(self, name):
        #Gets a list of the atoms and bonds according to name
        atoms = self.conn.execute("""SELECT ATOMS.ELEMENT_CODE, ATOMS.X, ATOMS.Y, ATOMS.Z
                                     FROM ATOMS
                                     INNER JOIN MOLECULEATOM ON MOLECULEATOM.ATOM_ID = ATOMS.ATOM_ID AND MOLECULEATOM.MOLECULE_ID = MOLECULES.MOLECULE_ID
                                     INNER JOIN MOLECULES ON MOLECULES.MOLECULE_ID = MOLECULEATOM.MOLECULE_ID
                                     WHERE MOLECULES.NAME = "{}";
                                    """.format(name)).fetchall()

        bonds = self.conn.execute("""SELECT A1, A2, EPAIRS
                                     FROM BONDS
                                     INNER JOIN MOLECULEBOND ON MOLECULEBOND.BOND_ID = BONDS.BOND_ID
                                     INNER JOIN MOLECULES ON MOLECULES.MOLECULE_ID = MOLECULEBOND.MOLECULE_ID
                                     WHERE MOLECULES.NAME = "{}";
                                    """.format(name)).fetchall()

        mol = MolDisplay.Molecule()

        for atom in atoms:
            mol.append_atom(atom[0], atom[1], atom[2], atom[3])

        for bond in bonds:
            mol.append_bond(bond[0], bond[1], bond[2])

        return mol

    def radius(self):
        radius_dict = self.conn.execute("""SELECT ELEMENT_CODE, RADIUS
                                           FROM ELEMENTS;
                                        """)
        return {item[0]:item[1] for item in radius_dict}

    def element_name(self):
        element_dict = self.conn.execute("""SELECT ELEMENT_CODE, ELEMENT_NAME
                                           FROM ELEMENTS;
                                        """)
        return {item[0]:item[1] for item in element_dict}

    def radial_gradients(self):
        output = """"""
        gradient_list = self.conn.execute("""SELECT ELEMENT_NAME, COLOUR1, COLOUR2, COLOUR3
                                           FROM ELEMENTS;
                                        """)

        for item in gradient_list:
            output += """
                <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
                <stop offset="0%%" stop-color="#%s"/>
                <stop offset="50%%" stop-color="#%s"/>
                <stop offset="100%%" stop-color="#%s"/>
                </radialGradient>""" %(item[0], item[1], item[2], item[3])

        return output

    def get_molecule_names(self):
        mol_names = self.conn.execute("""SELECT NAME
                                         FROM MOLECULES;
                                      """).fetchall()
        return mol_names

    def get_element_names(self):
        element_names = self.conn.execute("""SELECT ELEMENT_NAME
                                             FROM ELEMENTS;
                                          """).fetchall()
        return element_names

    def remove_element(self, element_name):
        self.conn.execute("""DELETE
                             FROM ELEMENTS
                             WHERE ELEMENTS.ELEMENT_NAME = "{}";
                          """.format(element_name))

        self.conn.commit()

if __name__ == "__main__":
    db = Database(reset=True);
    db.create_tables();
    db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
    db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
    db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
    db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
    # fp = open( 'water-3D-structure-CT1000292221.sdf' );
    # db.add_molecule( 'Water', fp );
    # fp = open( 'caffeine-3D-structure-CT1001987571.sdf' );
    # db.add_molecule( 'Caffeine', fp );
    # fp = open( 'CID_31260.sdf' );
    # db.add_molecule( 'Isopentanol', fp );
    # display tables
    print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM Atoms;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM Bonds;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() );
    print( db.conn.execute( "SELECT * FROM MoleculeBond;" ).fetchall() );
