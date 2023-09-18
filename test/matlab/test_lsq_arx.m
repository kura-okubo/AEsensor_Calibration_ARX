% Test script for lsq_arx.m
clear all;
addpath("../../code");

% Read the true data
load("../../data/testdata_lsq_arx.mat");

% figure(1); clf; hold on;
% plot(u_input_scaled);
% plot(y_output_scaled);

% Order of ARX model
Na = 20; % order of Auto-regressive model
Nb = 6; % order of Moving-average associated with the input

[theta_test, AIC_test] = lsq_arx(u_input_scaled, y_output_scaled, Na, Nb); % see lsq_arx.m for the details.

assert(all((theta - theta_test) == 0));
assert((AIC - AIC_test) == 0);