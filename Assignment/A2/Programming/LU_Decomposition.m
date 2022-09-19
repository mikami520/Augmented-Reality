function [L, U] = LU_Decomposition(A)
    assert(size(A, 1) == size(A, 2))
    assert(det(A) ~= 0)
    L = zeros(size(A));
    U = zeros(size(A));
    [L, U] = next(A, 1, L, U, size(A, 1));
end

function [L, U] = next(A, i, L, U, n)
    beta = A(i, i);
    x = A(i, i+1:n);
    v = A(i+1:n, i);
    w = v / beta;
    L(i,i) = 1;
    U(i,i) = beta;
    U(i, i+1:n) = x;
    L(i+1:n, i) = w;
    %L_star = 
    if i == n
        return
    end
    [L, U] = next(A, i+1, L, U, n);
end
