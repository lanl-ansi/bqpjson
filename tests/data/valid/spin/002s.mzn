% id : 0
% description : simple model with solutions
% 

set of int: Domain = {-1,1};
float: offset = 1.23;
float: scale = 2.7;

var Domain: x1;
var Domain: x3;
var Domain: x5;

var float: objective = 1.3*x1 + -0.7*x5 + -0.2*x1*x3 + 1.5*x1*x5;

solve minimize objective;

output [show(scale*(objective + offset)), " - ", show(objective), " - ", show([x1, x3, x5])];
