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
        return Matrix([row[:j] + row[j+1:] for row in (self.a[:i]+self.a[i+1:])])

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

    def inverse(self):
        assert self.rows == self.cols
        N = self.rows
        d = self.determinant()
        # 2x2 base case
        if N == 2:
            return Matrix([[     self.a[1][1]/d, -1 * self.a[0][1]/d],
                           [-1 * self.a[1][0]/d,      self.a[0][0]/d]])
        # Cramer's rule: the inverse is the transposed matrix of
        # cofactors divided by the determinant.
        return Matrix([[self.cofactor(r,c)/d for r in range(N)]
                       for c in range(N)])

    def product(self, other):
        assert self.cols == other.rows
        return Matrix([[sum(self.a[i][k] * other.a[k][j] for k in range(other.rows))
                        for j in range(other.cols)]
                       for i in range(self.rows)])

    def vector(self):
        assert self.cols == 1
        return [v for r in self.a for v in r]

def matrix(l):
    return Matrix([[v] for v in l])

