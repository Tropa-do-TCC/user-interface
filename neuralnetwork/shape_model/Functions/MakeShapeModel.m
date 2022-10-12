function [ShapeData TrainingData]= MakeShapeModel(TrainingData,eigVecPer)

% "Number of datasets"
s=length(TrainingData);
disp('Number of datasets')
disp(s)

% Number of landmarks
nl = size(TrainingData(1).Vertices,1);
disp('Number of landmarks')
disp(nl)

%% Shape model
% Construct a matrix with all contour point data of the training data set
x=zeros(nl*3,s);
array_points = []

for i=1:length(TrainingData)
    land_posi = []
    for j=1:nl
        x_land = ((TrainingData(i).Vertices(j)))
        y_land = ((TrainingData(i).Vertices(j + 9)))
        z_land = ((TrainingData(i).Vertices(j + 18)))
        land_posi = [x_land y_land z_land]
        array_points = [array_points; land_posi]
    end
    x(:,i)=reshape(TrainingData(i).Vertices', [], 1);
end
disp('Nova mtariz criada')

xrange=[-512/4, 512/4];
yrange=[-512/4, 512/4];
zrange=[-256/4, 256/4];

if(true)
    disp("Figura antes do PCA")
    subplot(1,1,1);
    scatter3(array_points(:,1), array_points(:,2), array_points(:,3), 10);
    axis equal; xlabel('x'); ylabel('y'); zlabel('z');
    xlim(xrange); ylim(yrange); zlim(zrange);
    title(['Shape Model Antes do PCA - Número de CTS lidas: ' num2str(i)]);
    drawnow;
    saveas(gcf,['./shape_model/' 'VariationBeforePCA' num2str(s) 'datasets.png']);
end

[Evalues, Evectors, x_mean]=PCA(x);

disp("Evalues, Evectors e x_mean criados")

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