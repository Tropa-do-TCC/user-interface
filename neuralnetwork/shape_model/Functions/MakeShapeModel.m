function [ShapeData TrainingData]= MakeShapeModel(TrainingData,eigVecPer)

% "Number of datasets"
disp('Number of datasets')
s=length(TrainingData);
disp(s)

% Number of landmarks
nl = size(TrainingData(1).Vertices,1);
disp('Number of landmarks')
disp(nl)

%% Shape model
% Construct a matrix with all contour point data of the training data set
x=zeros(nl*3,s);
for i=1:length(TrainingData)
    disp("dataset")
    disp(i)
    x(:,i)=reshape(TrainingData(i).Vertices', [], 1);
end
disp('new matrix')
disp(x)

[Evalues, Evectors, x_mean]=PCA(x);

% Keep only eigVecper of all eigen vectors, (remove contour noise)
if (eigVecPer~=1)
    i=find(cumsum(Evalues)>sum(Evalues)*eigVecPer,1,'first');
    Evectors=Evectors(:,1:i);
    Evalues=Evalues(1:i);
end

% Store the Eigen Vectors and Eigen Values
ShapeData.Evectors=Evectors;
ShapeData.Evalues=Evalues;
ShapeData.x_mean=x_mean;