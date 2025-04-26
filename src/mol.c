#include "mol.h"

void atomset( atom *atom, char element[3], double *x, double *y, double *z ) {
    atom->element[0] = element[0];
    atom->element[1] = element[1];
    atom->element[2] = element[2];

    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
}

void atomget( atom *atom, char element[3], double *x, double *y, double *z ) {
    element[0] = atom->element[0];
    element[1] = atom->element[1];
    element[2] = atom->element[2];

    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
}

void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ) {
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->epairs = *epairs;
    bond->atoms = *atoms;
    compute_coords(bond);
}

void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ) {
    *a1 = bond->a1;
    *a2 = bond->a2;
    *epairs = bond->epairs;
    *atoms = bond->atoms;
}

molecule *molmalloc( unsigned short atom_max, unsigned short bond_max ) {
    molecule* mol;

    mol = (molecule*) malloc(sizeof(molecule));

    if (mol == NULL) {
        return mol;
    }

    mol->atoms = (atom*) malloc(sizeof(atom) * atom_max);
    mol->atom_ptrs = (atom**) malloc(sizeof(atom*) * atom_max);
    mol->atom_max = atom_max;
    mol->atom_no = 0;

    mol->bonds = (bond*) malloc(sizeof(bond) * bond_max);
    mol->bond_ptrs = (bond**) malloc(sizeof(bond*) * bond_max);
    mol->bond_max = bond_max;
    mol->bond_no = 0;

    return mol;
}

molecule *molcopy( molecule *src ) {
    molecule* res;

    res = molmalloc(src->atom_max, src->bond_max);

    for (int i=0; i<src->atom_no; i++) {
       molappend_atom(res, &src->atoms[i]);
    }

    for (int i=0; i<src->bond_no; i++) {
       molappend_bond(res, &src->bonds[i]);
    }

    return res;
}

void molfree( molecule *ptr ) {
    free(ptr->atom_ptrs);
    free(ptr->bond_ptrs);
    free(ptr->atoms);
    free(ptr->bonds);

    free(ptr);
}

void molappend_atom( molecule *molecule, atom *atom ) {
    molecule->atom_no++;
    if (molecule->atom_max == 0) {
        molecule->atom_max++;
        molecule->atoms = realloc(molecule->atoms, sizeof(struct atom));
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom*));
    }
    else if (molecule->atom_no > molecule->atom_max) {
        //doubles size if max is exceeded
        molecule->atom_max *= 2;
        molecule->atoms = realloc(molecule->atoms, sizeof(struct atom) * molecule->atom_max);
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, sizeof(struct atom*) * molecule->atom_max);
    }

    if (molecule->atoms != NULL && molecule->atom_ptrs != NULL) {
        molecule->atoms[molecule->atom_no - 1] = *atom;
        //links the new array to atom array
        for (int i=0; i<molecule->atom_no; i++) {
            molecule->atom_ptrs[i] = &molecule->atoms[i];
        }
    }
}

void molappend_bond( molecule *molecule, bond *bond ) {
    molecule->bond_no++;
    if (molecule->bond_max == 0) {
        molecule->bond_max++;
        molecule->bonds = realloc(molecule->bonds, sizeof(struct bond));
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond*));
    }
    else if (molecule->bond_no > molecule->bond_max) {
        //doubles size if max is exceeded
        molecule->bond_max *= 2;
        molecule->bonds = realloc(molecule->bonds, sizeof(struct bond) * molecule->bond_max);
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, sizeof(struct bond*) * molecule->bond_max);
    }

    if (molecule->bonds != NULL && molecule->bond_ptrs != NULL) {
        molecule->bonds[molecule->bond_no - 1] = *bond;
        //links the new array to bond array
        for (int i=0; i<molecule->bond_no; i++) {
            molecule->bond_ptrs[i] = &molecule->bonds[i];
        }
    }

}

void molsort( molecule *molecule ) {
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(atom*), comparAtom);

    qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(bond*), comparBond);
}

void xrotation( xform_matrix xform_matrix, unsigned short deg ) {
    double rad = (double)deg/180 * M_PI;

    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = sin(rad) * -1;

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(rad);
    xform_matrix[2][2] = cos(rad);
}

void yrotation( xform_matrix xform_matrix, unsigned short deg ) {
    double rad = (double)deg/180 * M_PI;

    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin(rad);

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = sin(rad) * -1;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos(rad);
}

void zrotation( xform_matrix xform_matrix, unsigned short deg ) {
    double rad = (double)deg/180 * M_PI;

    xform_matrix[0][0] = cos(rad);
    xform_matrix[0][1] = sin(rad) * -1;
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = sin(rad);
    xform_matrix[1][1] = cos(rad);
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;
}

void mol_xform( molecule *molecule, xform_matrix matrix ) {
    double x, y, z;
    //computes a basic rotation on each atom
    for (int i=0; i<molecule->atom_no; i++) {
        x = matrix[0][0] * molecule->atoms[i].x + matrix[0][1] * molecule->atoms[i].y +
        matrix[0][2] * molecule->atoms[i].z;

        y = matrix[1][0] * molecule->atoms[i].x + matrix[1][1] * molecule->atoms[i].y +
        matrix[1][2] * molecule->atoms[i].z;

        z = matrix[2][0] * molecule->atoms[i].x + matrix[2][1] * molecule->atoms[i].y +
        matrix[2][2] * molecule->atoms[i].z;

        atomset(molecule->atom_ptrs[i], molecule->atom_ptrs[i]->element, &x, &y, &z);

        molecule->atoms[i].x = x;
        molecule->atoms[i].y = y;
        molecule->atoms[i].z = z;
    }

    //do compute coords function to each bond
    for (int i=0; i<molecule->bond_no; i++) {
        compute_coords(molecule->bond_ptrs[i]);
    }
}

void compute_coords( bond *bond ) {
    bond->x1 = bond->atoms[bond->a1].x;
    bond->y1 = bond->atoms[bond->a1].y;

    bond->x2 = bond->atoms[bond->a2].x;
    bond->y2 = bond->atoms[bond->a2].y;

    bond->z = (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z) / 2;

    //Calculate length
    bond->len = 0;
    bond->len = pow(bond->atoms[bond->a1].x - bond->atoms[bond->a2].x, 2);
    bond->len += pow(bond->atoms[bond->a1].y - bond->atoms[bond->a2].y, 2);
    bond->len = sqrt(bond->len);

    bond->dx = (bond->atoms[bond->a2].x - bond->atoms[bond->a1].x) / bond->len;
    bond->dy = (bond->atoms[bond->a2].y - bond->atoms[bond->a1].y) / bond->len;
}

int comparAtom(const void *a, const void *b) {
    atom** a1 = (atom**) a;
    atom** b1 = (atom**) b;

    if ((*a1)->z > (*b1)->z) {
        return 1;
    }
    else if ((*a1)->z == (*b1)->z) {
        return 0;
    }
    else {
        return -1;
    }
}

int comparBond(const void *a, const void *b) {
    bond** b1 = (bond**) a;
    bond** b2 = (bond**) b;

    if ((*b1)->z > (*b2)->z) {
        return 1;
    } else if ((*b1)->z == (*b2)->z) {
        return 0;
    } else {
        return -1;
    }
}
