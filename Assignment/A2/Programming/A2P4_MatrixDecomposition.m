clc
clear all

%% 4.1 QR Decomposition test

A = randn(5, 4);
[Q_package, R_package] = qr(A, 'econ');
[Q_mine, R_mine] = QR_Decomposition(A);
if Q_mine*R_mine - A < 0.005 * min(abs(A), abs(Q_mine*R_mine))
    disp('Correct RQ implementation')
else
    disp('Incorrect RQ implementation')
end
%% 4.2 LU Decomposition test
B = magic(6);
[L_package, U_package, P_package] = lu(B);
[L_mine, U_mine] = LU_Decomposition(B);

if L_mine*U_mine - B < 0.005 * min(abs(B), abs(L_mine*U_mine))
    disp('Correct LU implementation')
else
    disp('Incorrect LU implementation')
end