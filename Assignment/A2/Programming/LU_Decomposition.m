function [L, U] = LU_Decomposition(A)
    assert(size(A, 1) == size(A, 2))
    assert(det(A) ~= 0)
    L = zeros(size(A));
    U = zeros(size(A));
    n = size(A, 1);
    [L, U] = next(A, L, U, n);
end

function [L, U] = next(A, L, U, n)
    if n == 1
        L(1, 1) = 1;
        U(1, 1) = A(1,1);
        return
    end
    beta = A(1, 1);
    x = A(1, 2:n);
    v = A(2:n, 1);
    w = v / beta;
    L(1,1) = 1;
    U(1,1) = beta;
    U(1, 2:n) = x;
    L(2:n, 1) = w;
    LU_star = A(2:n, 2:n) - w * x;
    [L1, U1] = next(LU_star, L(2:n, 2:n), U(2:n,2:n), n-1);
    L(2:n, 2:n) = L1;
    U(2:n, 2:n) = U1;
end
