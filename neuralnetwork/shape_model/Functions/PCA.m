function [Evalues, Evectors, x_mean]=PCA(x)
disp('PCA iniciado')

s=size(x,2);
% Calculate the mean
x_mean=sum(x,2)/s;

% Substract the mean

matri=repmat(x_mean,1,s)

first=(x-matri)

x2=first/ sqrt(s-1);

% Do the SVD
[U2,S2,V] = svd(x2, 0);

Evalues=diag(S2).^2;
Evectors=bsxfun(@times,U2,sign(U2(1,:)));

