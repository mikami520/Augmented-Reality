clc
clear all

%% Problem 5(a)
X = zeros(4,2);
X_dot = zeros(4,2);
X(1, :) = [0, 0];
X(2, :) = [0, 1];
X(3, :) = [1, 1];
X(4, :) = [1, 0];
X_dot(1, :) = [1, 1];
X_dot(2, :) = [1, 0];
X_dot(3, :) = [2, 0];
X_dot(4, :) = [2, 1];

% define A
A = [];

for i=1:length(X)
    x = X(i, 1);
    y = X(i, 2);
    x_dot = X_dot(i, 1);
    y_dot = X_dot(i, 2);
    % for each correspondence, define Ai
    Ai = [-x, -y, -1, zeros(1, 3), x_dot*x, x_dot*y, x_dot; zeros(1, 3), -x, -y, -1, y_dot*x, y_dot*y, y_dot];
    A = [A; Ai];
end
[V, D] = eig(A' * A);
[d, ind] = sort(diag(D));
h_ATA = V(:, ind(1));
H_ATA = reshape(h_ATA', [3, 3])';
%% Problem 5(b)
[U, S, V] = svd(A);
h_SVD = V(:, size(V, 2));
H_SVD = reshape(h_SVD', [3, 3])';