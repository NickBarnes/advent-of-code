import numbers
# Variety of useful linear algebra:

class Vector:
    def __init__(self, *rest):
        self.v = rest
        self.dim = len(rest)
    
    def __add__(self,other):
        assert isinstance(other, Vector)
        assert self.dim == other.dim
        return Vector(*(self.v[i] + other.v[i] for i in range(self.dim)))

    def __sub__(self,other):
        assert isinstance(other, Vector)
        assert self.dim == other.dim
        return Vector(*(self.v[i] - other.v[i] for i in range(self.dim)))

    def __getitem__(self, index):
        return self.v[index]

    # dot product
    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return Vector(*(self.v[i] * other for i in range(self.dim)))
        else: # dot product
            assert isinstance(other, Vector)
            assert self.dim == other.dim
            return sum(self.v[i] * other.v[i] for i in range(self.dim))

    def cross(self, other):
        assert isinstance(other, Vector)
        assert self.dim == other.dim == 3
        return Vector(self.v[1] * other.v[2] - self.v[2] * other.v[1],
                      self.v[2] * other.v[0] - self.v[0] * other.v[2],
                      self.v[0] * other.v[1] - self.v[1] * other.v[0])

    def __eq__(self, other):
        return self.v == other.v

    def __repr__(self):
        return f"<{self.v[0]},{self.v[1]},{self.v[2]}>"

class Matrix:
    # Each matrix is a list of rows; each row is a list of values.
    def __init__(self, rows):
        self.rows = len(rows)
        self.cols = len(rows[0])
        self.a = rows

    def transpose(self):
        return Matrix(list(map(list, zip(*self.a))))

    # sub-matrix: remove row i and column j
    def sub_matrix(self,i,j):
        return Matrix([row[:j] + row[j+1:]
                       for row in (self.a[:i]+self.a[i+1:])])

    # minor: determinant of sub-matrix
    def minor(self,i,j):
        return self.sub_matrix(i,j).determinant()

    # cofactor
    def cofactor(self,i,j):
        return (-1) ** (i+j) * self.minor(i,j)

    def determinant(self):
        assert self.rows == self.cols
        # 2x2 base case
        if self.rows == 2:
            return self.a[0][0] * self.a[1][1] - self.a[0][1] * self.a[1][0]
        
        return sum(((-1)**c) * self.a[0][c] * self.minor(0,c)
                   for c in range(self.cols))

    # Matrix inversion.
    # 
    # If the determinant is zero, returns None.
    # If 'divided' is True, returns the inverted matrix (as floats, if
    # the original matrix contains ints or floats).
    # If 'divided' is False, returns the inverted matrix multiplied by
    # the determinant (this is guaranteed to be all ints if the
    # original matrix contents are ints), and the determinant itself
    # as a separate
    def inverse(self, divided=True):
        assert self.rows == self.cols
        N = self.rows
        d = self.determinant()
        if d == 0:
            if divided: return None, d
        divide = lambda c: c/d if divided else c
        divisor = d if divided else 1
        # 2x2 base case
        if N == 2:
            return Matrix(((divide(self.a[1][1]), -1 *
                            divide(self.a[0][1])),
                           (-1 * divide(self.a[1][0]),
                            divide(self.a[0][0])))), d
        else:
            # Cramer's rule: the inverse is the transposed matrix of
            # cofactors divided by the determinant.
            return Matrix([[divide(self.cofactor(r,c)) for r in range(N)]
                           for c in range(N)]), d

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return Matrix([[v * other for v in r] for r in self.a])
        else: # dot product
            assert isinstance(other, Matrix)
            assert self.cols == other.rows
            return Matrix([[sum(self.a[i][k] * other.a[k][j]
                                for k in range(other.rows))
                            for j in range(other.cols)]
                           for i in range(self.rows)])

    def vector(self):
        assert self.cols == 1
        return [v for r in self.a for v in r]

# return a 1 x N matrix of a list.
def matrix(l):
    return Matrix([[v] for v in l])

