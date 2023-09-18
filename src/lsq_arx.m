function [theta, AIC] = lsq_arx(u_input, y_output, Na, Nb)
% estimate model parameters of ARX model.

assert(length(u_input)==length(y_output), "input and output data must be same length.");
% assert(Na >= Nb, "Na must be greater than Nb.");

NT = length(u_input);

% compute phi matrix
phi = zeros(NT, Na+Nb+1);
for k=1:NT
    for l=1:Na+Nb+1
        if l<=Na
            if k-l>0
                phi(k, l) = -y_output(k-l);
            else
                phi(k, l) = 0; % assume that the negative time is zero output
            end
        else
            if k-l+Na+1>0
                phi(k, l) = u_input(k-l+Na+1);
            else
                phi(k, l) = 0;  % assume that the negative time is zero input
            end
            %            fprintf("k, m = %d, %d\n", k, -l+Na+1)
        end
    end
end

% compute sum of phi
ZZ = zeros(Na+Nb+1, Na+Nb+1);
for k = 1:NT
    ZZ = ZZ + phi(k, :)' * phi(k, :);
end

% compute sum of phi * y
ZY = zeros(Na+Nb+1, 1);
for k = 1:NT
    ZY = ZY + phi(k, :)' * y_output(k);
end

% estimate parameters with least square
% rcond(ZZ)
theta = (ZZ)\(ZY);

%% Compute 1-step 
y1pred = zeros(NT, 1); % 1-step predictor

for k = 1:NT
    for l=1:Na+Nb+1
        if l<=Na
           if k-l>0
               y1pred(k) = y1pred(k) + theta(l) * -y_output(k-l);
           end
       else
           if k-l+Na+1>0
               y1pred(k) = y1pred(k) + theta(l) * u_input(k-l+Na+1);
           end
       end
    end
end

%% Compute AIC
residu = 0;
for k = 1:NT
    residu = residu + abs(y_output(k) - y1pred(k))^2;
end

AIC = NT*log(residu/NT) + 2*(Na+Nb+1);
% fprintf("residu:%4.4e AIC is %4.2f\n", residu,AIC);

end