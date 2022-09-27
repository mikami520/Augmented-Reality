clc
clear all

%% 4.1 QR Decomposition test
A = randn(5, 4);
[Q_package, R_package] = qr(A, 'econ');
[Q_mine, R_mine] = QR_Decomposition(A);
%% Verification of 4.1
% compute the norm of difference between estimated A'=Q*R and true input A
disp("norm of difference between estimated A'=Q*R and true input A:")
disp(norm(Q_mine*R_mine - A))
% another check for the difference between estimated A'=Q*R and true input A
if Q_mine*R_mine - A < 0.000005 * min(abs(A), abs(Q_mine*R_mine))
    disp('Correct RQ implementation')
else
    disp('Incorrect RQ implementation')
end
disp("-------------------------------------------------------------")
%% 4.2 LU Decomposition test
B = randn(6);
[~, ~, P_package] = lu(B);
C = P_package * B;
[L_package, U_package] = lu(C);
[L_mine, U_mine] = LU_Decomposition(C);
%% Verification of 4.2
% compute the norm of difference between estimated C'=Q*R and true input C
disp("norm of difference between estimated C'=L*U and true input C:")
disp(norm(L_mine*U_mine - C))
% another check for the difference between estimated C'=L*U and true input C
if L_mine*U_mine - C < 0.000005 * min(abs(C), abs(L_mine*U_mine))
    disp('Correct LU implementation')
else
    disp('Incorrect LU implementation')
end