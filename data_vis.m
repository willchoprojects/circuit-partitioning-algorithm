clc
close all
clear all

data = load('data_merged_1680621616.csv');

% Split the data into independent and dependent variables
x1 = data(:,1);
x2 = data(:,2);
y = data(:,3);

% Define the grid
n1 = length(unique(x1));
n2 = length(unique(x2));
xi = linspace(min(x1), max(x1), n1);
yi = linspace(min(x2), max(x2), n2);
[X,Y] = meshgrid(xi,yi);

% Interpolate the data onto the grid
Z = griddata(x1,x2,y,X,Y,'linear');

figure
subset = data(data(:,1) == 8, :);
scatter(subset(:,2), subset(:,3), 'filled');
xlabel('Max Channels Total');
ylabel('Number of Cells');
title('Max Gates per Cell = 8');

figure
subset = data(data(:,2) == 4, :);
scatter(subset(:,1), subset(:,3), 'filled');
xlabel('Max Gates per Cell');
ylabel('Number of Cells');
title('Max Channels Total = 4');

% Create a heatmap
figure
imagesc(xi, yi, Z);
colorbar;
xlabel('Max Gates per Cell');
ylabel('Max Channels Total');
title('Number of Cells');

figure
imagesc(xi, yi, Z);
colormap(jet); % or any other colormap of your choice
clim([0 ceil(log2(max(y(:))))]); % set the color axis limits to cover the range of data
h = colorbar;
set(gca, 'colorscale', 'log', 'clim', [1 2^ceil(log2(max(y(:))))]); % set logarithmic color scale with base 2
xlabel('Max Gates per Cell');
ylabel('Max Channels Total');
title('Number of Cells');
h.TickLabelInterpreter = 'tex'; % set the tick label interpreter to TeX
ytick = get(h,'YTick'); % get the current tick locations
h.YTickLabel = ytick; % set the tick labels to 2 raised to the power of the tick locations
