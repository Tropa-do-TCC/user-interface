function y = myScript()
    clear all; clc; close all;
    addpath('./Functions/')

    %% Set options
    % folder containing the training landmarks
    landmarkFolder='../data/landmarks_from_ct/';
    % file containing list of shape images to use
    shapeListFile = '../data/list_train.txt';
    % folder storing the shape model txt and mat file
    shapeModelFolder='./shape_model/';
    % Percentage of variance used to keep the eigenvectors used in the model. (ie. 0.98)
    options.eigVecPer=1;
    % New image size that is required by the CNN
    imgSizeCNN = [512 512 256];
    % unwanted landmark indices for aligned images
    landmark_unwant = [];
    % If verbose is true all debug images will be shown.
    options.verbose=true;

    if ~exist(shapeModelFolder, 'dir')
      mkdir(shapeModelFolder)
    end
    %% Load training data
    % First Load the Landmarks Training DataSets
    fileID = fopen(shapeListFile,'r');
    ids = textscan(fileID,'%s');
    ids = ids{1};
    fclose(fileID);

    TrainingData=struct;
    num_ex = length(ids);
    for i=1:num_ex
        disp(['loading image ' num2str(i) '/' num2str(num_ex)])

        % Load landmarks

        fid = fopen([landmarkFolder ids{i} '_ps.txt'], 'r');
        landmarks = fscanf(fid, '%f %f %f', [3 Inf]);
        landmarks = landmarks';
        fclose(fid);

        % Remove unwanted landmarks
        landmarks(landmark_unwant, :) = [];
        TrainingData(i).Vertices=landmarks;
    end

    num_landmarks = size(TrainingData(1).Vertices,1);

    %% Shape Model %%
    % Make the Shape model, which finds the variations between contours
    % in the training data sets. And makes a PCA model describing normal
    % contours
    [ShapeData TrainingData]= MakeShapeModel(TrainingData,options.eigVecPer);
    disp("Shape model foi retornado")
    disp(ShapeData)

    % Show +-3s.d. of each mode for the top six modes
    w=1;
    xrange=[-imgSizeCNN(1)/4, imgSizeCNN(1)/4];
    yrange=[-imgSizeCNN(2)/4, imgSizeCNN(2)/4];
    zrange=[-imgSizeCNN(3)/4, imgSizeCNN(3)/4];

    if(options.verbose)
        subplot(1,1,1);
        xtest = (reshape(ShapeData.x_mean, 3, num_landmarks))';
        scatter3(xtest(:,1), xtest(:,2), xtest(:,3), 10);
        axis equal; xlabel('x'); ylabel('y'); zlabel('z');
        xlim(xrange); ylim(yrange); zlim(zrange);
        title(['Shape Model Depois do PCA - Quantidade de CTS lidas: ' num2str(i)]);
        drawnow;
        saveas(gcf,[shapeModelFolder, 'VariationAfterPCA' num2str(num_ex) 'datasets.png']);
    end

    % Save shape model in .mat file
    ShapeData.landmark_unwant = landmark_unwant;
    ShapeData.imgSizeCNN = imgSizeCNN;
    y = ShapeData
end


