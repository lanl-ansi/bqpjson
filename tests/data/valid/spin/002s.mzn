% id : 0
% description : simple model with solutions
% 

set of int: Domain = {-1,1};
float: offset = 1.23;
float: scale = 2.7;

var Domain: x2;
var Domain: x4;
var Domain: x6;

var float: objective = 1.3*x2 + -0.7*x6 + -0.2*x2*x4 + 1.5*x2*x6;

solve minimize objective;

output [show(scale*(objective + offset)), " - ", show(objective), " - ", show([x2, x4, x6])];
