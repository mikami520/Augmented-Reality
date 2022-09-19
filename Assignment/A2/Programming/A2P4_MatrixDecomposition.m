clc
clear all

%% 4.1 QR Decomposition test

A = randn(5, 4)
[Q_package, R_package] = qr(A)
[Q_mine, R_mine] = QR_Decomposition(A)

%% 4.2 LU Decomposition test