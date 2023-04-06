%% Setup

clc
close all
clear all

%% Parameters

file_path = 'compiled_data/num_cells_data_expanded.csv';
figures_path = 'result_figures/';

max_num_gates_per_cell = 131;
max_num_total_channels = 131;

plotted_num_gates_per_cell = [8];
plotted_num_total_channels = [4 10 20];

%% Data Loading

data = load(file_path);

% Select a subset of rows and columns
rows = 1:max_num_gates_per_cell;
cols = 1:max_num_total_channels;
data_subset = data(rows, cols);

%% Directory Creation

mkdir(figures_path);

%% Max Gates per Cell Plots

for num_gates_per_cell = plotted_num_gates_per_cell
    row_data = data_subset(num_gates_per_cell,:);
    figure;
    scatter(1:size(row_data,2), row_data, 'filled');
    xlabel('Max Channels Total');
    ylabel('Number of Cells');
    title(['Max Gates per Cell = ' num2str(num_gates_per_cell)]);

    saveas(gcf, [figures_path 'max_num_gates_per_cell_' num2str(num_gates_per_cell) '.png']);
end

%% Max Total Channels Plots

for num_total_channels = plotted_num_total_channels
    col_index = num_total_channels;
    col_data = data_subset(:,col_index);
    figure;
    scatter(1:size(col_data,1), col_data, 'filled');
    xlabel('Max Gates per Cell');
    ylabel('Number of Cells');
    title(['Max Channels Total = ' num2str(num_total_channels)]);

    saveas(gcf, [figures_path 'max_num_total_channels_' num2str(num_total_channels) '.png']);
end

%% Heatmap with Linear Scale

figure

[X,Y] = meshgrid(cols, rows);

imagesc(X(1,:), Y(:,1), data_subset);

colormap(jet);
h = colorbar;

xlabel('Max Channels Total');
ylabel('Max Gates per Cell');
title('Number of Cells (Linear Scale)');

h.TickLabelInterpreter = 'tex';
ytick = get(h,'YTick');
h.YTickLabel = ytick;

saveas(gcf, [figures_path 'num_cells_linear_scale.png']);

%% Heatmap with Log Scale

figure

[X,Y] = meshgrid(cols, rows);

imagesc(X(1,:), Y(:,1), data_subset);

colormap(jet);
clim([0 ceil(log2(132))]);
h = colorbar;
set(gca, 'colorscale', 'log', 'clim', [1 2^ceil(log2(max_num_gates_per_cell))]);

xlabel('Max Channels Total');
ylabel('Max Gates per Cell');
title('Number of Cells (Logarithmic Scale)');

h.TickLabelInterpreter = 'tex';
ytick = get(h,'YTick');
h.YTickLabel = ytick;

saveas(gcf, [figures_path 'num_cells_logarithmic_scale.png']);
