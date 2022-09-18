function [Evalues, Evectors, x_mean]=PCA(x)
disp('PCA')
disp(x)

s=size(x,2);
% Calculate the mean
x_mean=sum(x,2)/s;
disp('X_MEAN')
disp(x_mean)
disp('size')
disp(s)

% Substract the mean

matri=repmat(x_mean,1,s)
disp(matri)

first=(x-matri)
disp(first)

x2=first/ sqrt(s-1);
disp('x2')
disp(x2)

% Do the SVD
[U2,S2,V] = svd(x2, 0);

disp("S2")
disp(S2)
disp("U2")
disp(U2)
Evalues=diag(S2).^2;
Evectors=bsxfun(@times,U2,sign(U2(1,:)));
disp("evalues e evectors criados")
disp(Evalues)
disp(size(Evalues))
disp(Evectors)
disp(size(Evectors))
