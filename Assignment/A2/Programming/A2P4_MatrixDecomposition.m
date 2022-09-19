clc
clear all

%% 4.1 QR Decomposition test

A = randn(5, 4)
[Q_package, R_package] = qr(A, 'econ')
[Q_mine, R_mine] = QR_Decomposition(A)

%% 4.2 LU Decomposition test
B = magic(5)*100
[L_package, U_package] = lu(B)
[L_mine, U_mine] = LU_Decomposition(B)