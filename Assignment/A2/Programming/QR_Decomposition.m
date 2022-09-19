function [Q, R] = QR_Decomposition(A)
    [m, n] = size(A);
    Q = zeros(m, n);
    R = zeros(n, n);
    for i=1:n
        ai = A(:, i);
        ui = ai;
        for j=1:(i-1)
            ui = ui - project(Q(:, j), ai);
        end
        R(i, i) = norm(ui);
        qi = ui / norm(ui);
        for k=i+1:n
            R(i, k) = dot(A(:, k), qi);
        end
        Q(:, i) = qi;
    end
end

function P = project(u, v)
    P = (dot(v, u) / norm(u)^2) * u;
end