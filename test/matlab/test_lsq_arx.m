% Test script for lsq_arx.m
clear all;
addpath("../../src");

% Read the true data
load("../../data/testdata_lsq_arx.mat");

% figure(1); clf; hold on;
% plot(u_input_scaled);
% plot(y_output_scaled);

% Order of ARX model
Na = 24; % order of Auto-regressive model
Nb = 11; % order of Moving-average associated with the input

[theta_test, AIC_test] = lsq_arx(u_input_scaled, y_output_scaled, Na, Nb); % see lsq_arx.m for the details.

disp(theta)
disp(theta_test)
disp(theta - theta_test)
disp(norm(theta - theta_test));
assert(norm(theta - theta_test) < 1e-1);
assert(abs(AIC - AIC_test) < 1e-2);
