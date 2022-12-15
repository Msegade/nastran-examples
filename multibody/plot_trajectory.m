% plot_trajectory.m
clear; close all;

M = dlmread('free_falling_body.mov');

x = M(:,2); y = M(:,3); z = M(:,4);

t = 0:1.e-3:1;

td = 0:0.1:1;

for k=1:length(td)
    yd(k) = y(min(find(t>=td(k))));
    zd(k) = z(min(find(t>=td(k))));
end

plot(y,z,'-',yd,zd,'o','LineWidth',2,'MarkerSize',8);
grid on;
axis([0,5,-5,0]);
axis square;
xlabel('y (m)','FontSize',14);
ylabel('z (m)','FontSize',14);
title('Trajectory on y-z plane','FontSize',14);
set(gca,'FontSize',14);
